from __future__ import annotations

import json
from pathlib import Path

import pytest

pytestmark = pytest.mark.unit


def test_model_registry_schema() -> None:
    registry_path = Path(__file__).resolve().parents[2] / "image_ai" / "model_registry.json"
    registry = json.loads(registry_path.read_text(encoding="utf-8"))

    open_models = registry["open_weight_models"]
    closed_models = registry["closed_api_models"]

    open_families = [item["family"] for item in open_models]
    closed_families = [item["family"] for item in closed_models]

    assert len(open_families) == len(set(open_families))
    assert len(closed_families) == len(set(closed_families))

    for item in open_models:
        assert item["family"]
        assert item["model_id"]
        assert item["evidence"]

    for item in closed_models:
        assert item["family"]
        assert item["model_id"]
        assert item["provider"]
        assert item["api_reference"]
