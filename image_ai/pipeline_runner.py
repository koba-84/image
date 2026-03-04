from __future__ import annotations

import base64
import json
import os
import platform
from dataclasses import dataclass
from math import gcd
from io import BytesIO
from pathlib import Path
from sys import version as python_version
from typing import Any, Literal
from urllib import request as urllib_request

import torch
from PIL import Image

from image_ai.config import RuntimeConfig


Mode = Literal["text2img", "img2img", "inpaint"]
BackendType = Literal["local", "api"]
_KNOWN_API_PREFIXES = {"openai", "google", "ideogram"}


@dataclass(frozen=True)
class BackendSelection:
    backend: BackendType
    provider: str | None
    model_name: str


def resolve_backend(model_id: str) -> BackendSelection:
    if ":" not in model_id:
        return BackendSelection(backend="local", provider=None, model_name=model_id)

    provider, model_name = model_id.split(":", 1)
    if not model_name:
        raise ValueError(
            "model_id with provider prefix must include model name (e.g. openai:gpt-image-1)."
        )
    if provider in _KNOWN_API_PREFIXES:
        return BackendSelection(backend="api", provider=provider, model_name=model_name)
    return BackendSelection(backend="local", provider=None, model_name=model_id)


class OpenAIImageAPIBackend:
    is_api_backend = True
    provider = "openai"

    def __init__(self, model_name: str) -> None:
        self.model_name = model_name

    def generate(self, config: RuntimeConfig) -> Image.Image:
        if config.mode != "text2img":
            raise NotImplementedError(
                "API backend currently supports only text2img mode."
            )
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY is required for openai API backend.")

        base_url = (
            config.api_base_url
            or os.getenv("OPENAI_BASE_URL")
            or "https://api.openai.com/v1"
        )
        endpoint = base_url.rstrip("/") + "/images/generations"

        payload: dict[str, Any] = {
            "model": self.model_name,
            "prompt": config.prompt,
        }
        if config.height is not None and config.width is not None:
            payload["size"] = f"{config.width}x{config.height}"

        req = urllib_request.Request(
            endpoint,
            data=json.dumps(payload).encode("utf-8"),
            method="POST",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
        )
        with urllib_request.urlopen(req) as res:
            data = json.loads(res.read().decode("utf-8"))

        first = data.get("data", [{}])[0]
        image_bytes = _extract_image_bytes(first, "openai")
        return Image.open(BytesIO(image_bytes)).convert("RGB")


class GoogleImagenAPIBackend:
    is_api_backend = True
    provider = "google"

    def __init__(self, model_name: str) -> None:
        self.model_name = model_name

    def generate(self, config: RuntimeConfig) -> Image.Image:
        if config.mode != "text2img":
            raise NotImplementedError(
                "API backend currently supports only text2img mode."
            )
        access_token = os.getenv("GOOGLE_VERTEX_ACCESS_TOKEN")
        project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
        location = os.getenv("GOOGLE_CLOUD_LOCATION")
        missing = [
            name
            for name, value in (
                ("GOOGLE_VERTEX_ACCESS_TOKEN", access_token),
                ("GOOGLE_CLOUD_PROJECT", project_id),
                ("GOOGLE_CLOUD_LOCATION", location),
            )
            if not value
        ]
        if missing:
            raise RuntimeError(
                f"Missing required Google Vertex env vars: {', '.join(missing)}"
            )

        endpoint = config.api_base_url or (
            "https://"
            f"{location}-aiplatform.googleapis.com/v1/projects/{project_id}/locations/{location}"
            f"/publishers/google/models/{self.model_name}:predict"
        )

        parameters: dict[str, Any] = {"sampleCount": 1, "seed": config.seed}
        if config.width is not None and config.height is not None:
            parameters["aspectRatio"] = _to_aspect_ratio(config.width, config.height)

        payload = {
            "instances": [{"prompt": config.prompt}],
            "parameters": parameters,
        }
        req = urllib_request.Request(
            endpoint,
            data=json.dumps(payload).encode("utf-8"),
            method="POST",
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json",
            },
        )
        with urllib_request.urlopen(req) as res:
            data = json.loads(res.read().decode("utf-8"))

        first = data.get("predictions", [{}])[0]
        image_bytes = _extract_image_bytes(first, "google")
        return Image.open(BytesIO(image_bytes)).convert("RGB")


class IdeogramAPIBackend:
    is_api_backend = True
    provider = "ideogram"

    def __init__(self, model_name: str) -> None:
        self.model_name = model_name

    def generate(self, config: RuntimeConfig) -> Image.Image:
        if config.mode != "text2img":
            raise NotImplementedError(
                "API backend currently supports only text2img mode."
            )
        api_key = os.getenv("IDEOGRAM_API_KEY")
        if not api_key:
            raise RuntimeError("IDEOGRAM_API_KEY is required for ideogram API backend.")

        endpoint = config.api_base_url or "https://api.ideogram.ai/generate"
        image_request: dict[str, Any] = {
            "prompt": config.prompt,
            "model": _to_ideogram_model(self.model_name),
        }
        if config.width is not None and config.height is not None:
            image_request["aspect_ratio"] = _to_aspect_ratio(config.width, config.height)
        payload = {"image_request": image_request}

        req = urllib_request.Request(
            endpoint,
            data=json.dumps(payload).encode("utf-8"),
            method="POST",
            headers={"Api-Key": api_key, "Content-Type": "application/json"},
        )
        with urllib_request.urlopen(req) as res:
            data = json.loads(res.read().decode("utf-8"))

        first = data.get("data", [{}])[0]
        image_bytes = _extract_image_bytes(first, "ideogram")
        return Image.open(BytesIO(image_bytes)).convert("RGB")


def _to_ideogram_model(model_name: str) -> str:
    normalized = model_name.strip().lower()
    if normalized == "v2":
        return "V_2"
    if normalized == "v1":
        return "V_1"
    return model_name


def _to_aspect_ratio(width: int, height: int) -> str:
    ratio = gcd(width, height)
    return f"{width // ratio}:{height // ratio}"


def _extract_image_bytes(item: dict[str, Any], provider: str) -> bytes:
    if "b64_json" in item:
        return base64.b64decode(item["b64_json"])
    if "bytesBase64Encoded" in item:
        return base64.b64decode(item["bytesBase64Encoded"])
    if "base64" in item:
        return base64.b64decode(item["base64"])

    image_obj = item.get("image")
    if isinstance(image_obj, dict):
        if "b64_json" in image_obj:
            return base64.b64decode(image_obj["b64_json"])
        if "base64" in image_obj:
            return base64.b64decode(image_obj["base64"])
        if "url" in image_obj:
            return _fetch_image_bytes(image_obj["url"])

    for url_key in ("url", "image_url"):
        if url_key in item:
            return _fetch_image_bytes(item[url_key])

    raise RuntimeError(
        f"{provider} image response did not include base64 or image url payload."
    )


def _fetch_image_bytes(url: str) -> bytes:
    with urllib_request.urlopen(url) as image_res:
        return image_res.read()


def select_torch_device(raw: str) -> str:
    if raw != "auto":
        return raw
    if torch.cuda.is_available():
        return "cuda"
    if torch.backends.mps.is_available():
        return "mps"
    return "cpu"


def select_torch_dtype(device: str) -> torch.dtype:
    if device == "cuda":
        return torch.float16
    if device == "cpu":
        return torch.float32
    return torch.float16


def load_pipeline_for_mode(mode: Mode, model_id: str, dtype: torch.dtype) -> Any:
    backend = resolve_backend(model_id)
    if backend.backend == "api":
        if backend.provider == "openai":
            return OpenAIImageAPIBackend(backend.model_name)
        if backend.provider == "google":
            return GoogleImagenAPIBackend(backend.model_name)
        if backend.provider == "ideogram":
            return IdeogramAPIBackend(backend.model_name)
        raise NotImplementedError(
            f"API provider '{backend.provider}' is not supported yet."
        )

    from diffusers import (
        AutoPipelineForImage2Image,
        AutoPipelineForInpainting,
        AutoPipelineForText2Image,
    )

    if mode == "text2img":
        return AutoPipelineForText2Image.from_pretrained(
            backend.model_name, torch_dtype=dtype
        )
    if mode == "img2img":
        return AutoPipelineForImage2Image.from_pretrained(
            backend.model_name, torch_dtype=dtype
        )
    return AutoPipelineForInpainting.from_pretrained(backend.model_name, torch_dtype=dtype)




def configure_diffusers_pipeline(pipe: Any, config: RuntimeConfig, device: str) -> None:
    if getattr(pipe, "is_api_backend", False):
        return

    if config.enable_attention_slicing:
        pipe.enable_attention_slicing("auto")
    if config.enable_vae_slicing:
        pipe.enable_vae_slicing()
    if config.enable_vae_tiling:
        pipe.enable_vae_tiling()
    if config.enable_xformers:
        if not hasattr(pipe, "enable_xformers_memory_efficient_attention"):
            raise RuntimeError("xFormers attention is not supported by this pipeline.")
        pipe.enable_xformers_memory_efficient_attention()
    if config.enable_channels_last and hasattr(pipe, "unet"):
        pipe.unet.to(memory_format=torch.channels_last)

    if config.offload == "model":
        if device != "cuda":
            raise RuntimeError("--offload=model requires CUDA device.")
        pipe.enable_model_cpu_offload()
        return
    if config.offload == "sequential":
        if device != "cuda":
            raise RuntimeError("--offload=sequential requires CUDA device.")
        pipe.enable_sequential_cpu_offload()
        return
    pipe.to(device)


def load_edit_inputs(mode: Mode, image_arg: str | None, mask_arg: str | None):
    if mode == "text2img":
        return None, None
    if not image_arg:
        raise ValueError("image is required for img2img/inpaint mode.")
    from diffusers.utils import load_image

    image = load_image(image_arg)
    if mode == "img2img":
        return image, None
    if not mask_arg:
        raise ValueError("mask_image is required for inpaint mode.")
    mask_image = load_image(mask_arg).convert("L")
    if mask_image.size != image.size:
        raise ValueError(
            f"mask size {mask_image.size} must match image size {image.size}."
        )
    return image, mask_image


def run_inference(pipe: Any, config: RuntimeConfig):
    if getattr(pipe, "is_api_backend", False):
        return pipe.generate(config)

    generator = torch.Generator(device="cpu").manual_seed(config.seed)
    shared = dict(
        prompt=config.prompt,
        negative_prompt=config.negative_prompt,
        num_inference_steps=config.steps,
        guidance_scale=config.guidance_scale,
        generator=generator,
    )
    if config.height is not None:
        shared["height"] = config.height
    if config.width is not None:
        shared["width"] = config.width

    image, mask_image = load_edit_inputs(config.mode, config.image, config.mask_image)
    if config.mode == "text2img":
        return pipe(**shared).images[0]
    if config.mode == "img2img":
        return pipe(**shared, image=image, strength=config.strength).images[0]
    return pipe(
        **shared,
        image=image,
        mask_image=mask_image,
        strength=config.strength,
    ).images[0]


def save_inference_metadata(
    config: RuntimeConfig, device: str, dtype: torch.dtype
) -> None:
    backend = resolve_backend(config.model_id)
    metadata = {
        "mode": config.mode,
        "model_variant": config.model_variant,
        "model_id": config.model_id,
        "prompt": config.prompt,
        "negative_prompt": config.negative_prompt,
        "seed": config.seed,
        "steps": config.steps,
        "guidance_scale": config.guidance_scale,
        "height": config.height,
        "width": config.width,
        "strength": config.strength,
        "image": config.image,
        "mask_image": config.mask_image,
        "device": device,
        "dtype": str(dtype),
        "offload": config.offload,
        "attention_slicing": config.enable_attention_slicing,
        "vae_slicing": config.enable_vae_slicing,
        "vae_tiling": config.enable_vae_tiling,
        "xformers": config.enable_xformers,
        "channels_last": config.enable_channels_last,
        "controlnet_enabled": config.controlnet_enabled,
        "controlnet_model_id": config.controlnet_model_id,
        "controlnet_conditioning_scale": config.controlnet_conditioning_scale,
        "controlnet_image": config.controlnet_image,
        "backend": backend.backend,
        "provider": backend.provider,
        "runtime_environment": {
            "python_version": python_version,
            "platform": platform.platform(),
            "torch_version": torch.__version__,
        },
    }
    metadata_path = Path(config.output).with_suffix(".json")
    metadata_path.write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"[INFO] metadata: {metadata_path}")
