from __future__ import annotations

import json

import pytest
import torch

from image_ai.config import RuntimeConfig
from image_ai.pipeline_runner import run_inference, save_inference_metadata

pytestmark = pytest.mark.integration


class _Result:
    def __init__(self, image: torch.Tensor) -> None:
        self.images = [image]


class _DeterministicPipe:
    def __call__(self, **kwargs):
        seed = int(kwargs["generator"].initial_seed())
        image = torch.full((4, 4), float(seed % 17), dtype=torch.float32)
        return _Result(image)


def _base_config(output_path: str, seed: int) -> RuntimeConfig:
    return RuntimeConfig(
        mode="text2img",
        model_id="dummy-model",
        prompt="test prompt",
        output=output_path,
        seed=seed,
    )


def test_run_inference_is_reproducible_for_same_seed(tmp_path) -> None:
    pipe = _DeterministicPipe()
    first = run_inference(pipe, _base_config(str(tmp_path / "a.png"), seed=123))
    second = run_inference(pipe, _base_config(str(tmp_path / "b.png"), seed=123))
    third = run_inference(pipe, _base_config(str(tmp_path / "c.png"), seed=124))

    assert torch.equal(first, second)
    assert not torch.equal(first, third)


def test_save_inference_metadata_contains_runtime_environment_fields(tmp_path) -> None:
    output = tmp_path / "result.png"
    cfg = _base_config(str(output), seed=42)
    save_inference_metadata(cfg, "cpu", torch.float32)
    metadata = json.loads(output.with_suffix(".json").read_text(encoding="utf-8"))

    assert metadata["model_id"] == "dummy-model"
    assert metadata["seed"] == 42
    assert "runtime_environment" in metadata
    assert metadata["runtime_environment"]["python_version"]
    assert metadata["runtime_environment"]["platform"]
    assert metadata["runtime_environment"]["torch_version"]
