from __future__ import annotations

import json
import platform
from pathlib import Path
from sys import version as python_version
from typing import Any, Literal

import torch

from image_ai.config import RuntimeConfig


Mode = Literal["text2img", "img2img", "inpaint"]


def select_torch_device(raw: str) -> str:
    if raw != "auto":
        return raw
    if torch.cuda.is_available():
        return "cuda"
    if torch.backends.mps.is_available():
        return "mps"
    return "cpu"


def select_torch_dtype(raw: str, device: str) -> torch.dtype:
    if raw == "fp16":
        return torch.float16
    if raw == "bf16":
        return torch.bfloat16
    if raw == "fp32":
        return torch.float32
    if device == "cuda":
        return torch.float16
    if device == "cpu":
        return torch.float32
    return torch.float16


def apply_low_vram_optimizations(config: RuntimeConfig) -> None:
    if config.low_vram_preset == "none":
        return
    config.enable_attention_slicing = True
    config.enable_vae_slicing = True
    if config.low_vram_preset == "aggressive":
        config.enable_vae_tiling = True
        config.offload = "sequential"


def load_pipeline_for_mode(mode: Mode, model_id: str, dtype: torch.dtype) -> Any:
    from diffusers import (
        AutoPipelineForImage2Image,
        AutoPipelineForInpainting,
        AutoPipelineForText2Image,
    )

    if mode == "text2img":
        return AutoPipelineForText2Image.from_pretrained(model_id, torch_dtype=dtype)
    if mode == "img2img":
        return AutoPipelineForImage2Image.from_pretrained(model_id, torch_dtype=dtype)
    return AutoPipelineForInpainting.from_pretrained(model_id, torch_dtype=dtype)




def configure_diffusers_pipeline(pipe: Any, config: RuntimeConfig, device: str) -> None:
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
        "low_vram_preset": config.low_vram_preset,
        "controlnet_enabled": config.controlnet_enabled,
        "controlnet_model_id": config.controlnet_model_id,
        "controlnet_conditioning_scale": config.controlnet_conditioning_scale,
        "controlnet_image": config.controlnet_image,
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
