from __future__ import annotations

import sys
from types import SimpleNamespace

import pytest
import torch

from image_ai.pipeline_runner import load_pipeline_for_mode

pytestmark = pytest.mark.unit


class _AutoPipelineStub:
    def __init__(
        self, pipeline_kind: str, load_calls: list[tuple[str, str, torch.dtype]]
    ) -> None:
        self._pipeline_kind = pipeline_kind
        self._load_calls = load_calls

    def from_pretrained(self, model_id: str, *, torch_dtype: torch.dtype):
        self._load_calls.append((self._pipeline_kind, model_id, torch_dtype))
        return {
            "pipeline_kind": self._pipeline_kind,
            "model_id": model_id,
            "torch_dtype": torch_dtype,
        }


@pytest.mark.parametrize(
    ("task_mode", "expected_pipeline_kind"),
    [
        ("text2img", "text2img"),
        ("img2img", "img2img"),
        ("inpaint", "inpaint"),
    ],
)
def test_load_pipeline_for_mode_selects_task_specific_auto_pipeline(
    monkeypatch: pytest.MonkeyPatch, task_mode: str, expected_pipeline_kind: str
) -> None:
    load_calls: list[tuple[str, str, torch.dtype]] = []
    fake_diffusers = SimpleNamespace(
        AutoPipelineForText2Image=_AutoPipelineStub("text2img", load_calls),
        AutoPipelineForImage2Image=_AutoPipelineStub("img2img", load_calls),
        AutoPipelineForInpainting=_AutoPipelineStub("inpaint", load_calls),
    )
    monkeypatch.setitem(sys.modules, "diffusers", fake_diffusers)

    result = load_pipeline_for_mode(task_mode, "example/model", torch.float16)

    assert load_calls == [(expected_pipeline_kind, "example/model", torch.float16)]
    assert result["pipeline_kind"] == expected_pipeline_kind
