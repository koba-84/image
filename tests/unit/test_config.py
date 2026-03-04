from __future__ import annotations

import pytest
from omegaconf import OmegaConf

from image_ai.config import RuntimeConfig, build_runtime_config

pytestmark = pytest.mark.unit


def _base_cfg():
    return {
        "mode": "text2img",
        "model_id": "test-model",
        "prompt": "test prompt",
        "output": "outputs/out.png",
    }


def test_build_runtime_config_returns_dataclass() -> None:
    cfg = OmegaConf.create(_base_cfg())
    runtime = build_runtime_config(cfg)
    assert isinstance(runtime, RuntimeConfig)
    assert runtime.mode == "text2img"


@pytest.mark.parametrize(
    "key",
    ["model_id", "prompt", "output"],
)
def test_build_runtime_config_requires_common_fields(key: str) -> None:
    raw = _base_cfg()
    raw[key] = ""
    cfg = OmegaConf.create(raw)
    with pytest.raises(ValueError):
        build_runtime_config(cfg)


def test_build_runtime_config_requires_image_for_edit_modes() -> None:
    cfg = OmegaConf.create(
        {
            **_base_cfg(),
            "mode": "img2img",
            "image": None,
        }
    )
    with pytest.raises(ValueError):
        build_runtime_config(cfg)


def test_build_runtime_config_requires_mask_for_inpaint() -> None:
    cfg = OmegaConf.create(
        {
            **_base_cfg(),
            "mode": "inpaint",
            "image": "inputs/image.png",
            "mask_image": None,
        }
    )
    with pytest.raises(ValueError):
        build_runtime_config(cfg)


def test_build_runtime_config_requires_controlnet_model_id_when_enabled() -> None:
    cfg = OmegaConf.create(
        {
            **_base_cfg(),
            "controlnet_enabled": True,
            "controlnet_model_id": None,
            "controlnet_image": "inputs/control.png",
        }
    )
    with pytest.raises(ValueError):
        build_runtime_config(cfg)


def test_build_runtime_config_requires_controlnet_image_when_enabled() -> None:
    cfg = OmegaConf.create(
        {
            **_base_cfg(),
            "controlnet_enabled": True,
            "controlnet_model_id": "lllyasviel/sd-controlnet-canny",
            "controlnet_image": None,
        }
    )
    with pytest.raises(ValueError):
        build_runtime_config(cfg)
