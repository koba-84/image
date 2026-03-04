from __future__ import annotations

import json
from pathlib import Path

import pytest

from image_ai.testing import evaluate_safety


def _load_cases() -> list[dict]:
    path = Path(__file__).with_name("data") / "safety_cases.json"
    return json.loads(path.read_text(encoding="utf-8"))


@pytest.mark.safety
@pytest.mark.parametrize("case", _load_cases())
def test_safety_cases(case: dict) -> None:
    allowed, reason = evaluate_safety(case["prompt"], case["tags"])
    assert allowed is case["expected_allowed"]
    assert reason == case["expected_reason"]
