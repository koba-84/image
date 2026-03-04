from __future__ import annotations

import os

import pytest
import torch

from image_ai.pipeline_runner import load_pipeline_for_mode

pytestmark = pytest.mark.integration


@pytest.mark.skipif(
    os.getenv("IMAGE_AI_ENABLE_REAL_MODEL_LOAD") != "1",
    reason="Set IMAGE_AI_ENABLE_REAL_MODEL_LOAD=1 to run real model load test.",
)
def test_load_pipeline_for_mode_loads_real_model_in_colab() -> None:
    if not torch.cuda.is_available():
        pytest.skip("Real model load test requires CUDA (e.g. Colab GPU runtime).")

    pipe = load_pipeline_for_mode(
        "text2img",
        "stable-diffusion-v1-5/stable-diffusion-v1-5",
        torch.float16,
    )

    assert pipe is not None
    assert callable(pipe)
