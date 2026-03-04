from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from omegaconf import DictConfig, OmegaConf


Mode = Literal["text2img", "img2img", "inpaint"]


@dataclass
class RuntimeConfig:
    mode: Mode = "text2img"
    model_variant: str = "custom"
    model_id: str = ""
    prompt: str = ""
    negative_prompt: str | None = None
    output: str = ""
    seed: int = 42
    steps: int = 28
    guidance_scale: float = 7.0
    height: int | None = None
    width: int | None = None
    strength: float = 0.65
    image: str | None = None
    mask_image: str | None = None
    device: Literal["auto", "cuda", "mps", "cpu"] = "auto"
    dtype: Literal["auto", "fp16", "bf16", "fp32"] = "auto"
    offload: Literal["none", "model", "sequential"] = "model"
    enable_attention_slicing: bool = False
    enable_vae_slicing: bool = False
    enable_vae_tiling: bool = False
    enable_xformers: bool = False
    enable_channels_last: bool = False
    low_vram_preset: Literal["none", "balanced", "aggressive"] = "balanced"
    controlnet_enabled: bool = False
    controlnet_model_id: str | None = None
    controlnet_conditioning_scale: float = 1.0
    controlnet_image: str | None = None


def _validate_runtime_config(config: RuntimeConfig) -> None:
    if not config.model_id:
        raise ValueError("model_id is required.")
    if not config.prompt:
        raise ValueError("prompt is required.")
    if not config.output:
        raise ValueError("output is required.")
    if config.mode in {"img2img", "inpaint"} and not config.image:
        raise ValueError("image is required for img2img/inpaint mode.")
    if config.mode == "inpaint" and not config.mask_image:
        raise ValueError("mask_image is required for inpaint mode.")
    if config.controlnet_enabled and not config.controlnet_model_id:
        raise ValueError("controlnet_model_id is required when controlnet is enabled.")
    if config.controlnet_enabled and not config.controlnet_image:
        raise ValueError("controlnet_image is required when controlnet is enabled.")


def build_runtime_config(cfg: DictConfig) -> RuntimeConfig:
    raw = OmegaConf.to_container(cfg, resolve=True)
    if not isinstance(raw, dict):
        raise TypeError("Hydra config must be a mapping.")
    runtime = RuntimeConfig(**raw)
    _validate_runtime_config(runtime)
    return runtime
