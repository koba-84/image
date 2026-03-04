from __future__ import annotations

import pytest
import torch

from image_ai.testing import passes_quality_gate


@pytest.mark.regression
def test_quality_gate_uses_pixel_and_perceptual_thresholds() -> None:
    baseline = torch.tensor([[0.0, 1.0], [1.0, 0.0]])
    near = torch.tensor([[0.0, 0.95], [0.95, 0.0]])
    far = torch.tensor([[1.0, 0.0], [0.0, 1.0]])

    assert passes_quality_gate(
        near, baseline, max_pixel_mae=0.1, min_cosine_similarity=0.99
    )
    assert not passes_quality_gate(
        far, baseline, max_pixel_mae=0.1, min_cosine_similarity=0.99
    )

