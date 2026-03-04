from __future__ import annotations

from typing import Iterable

import torch


def pixel_mae(candidate: torch.Tensor, baseline: torch.Tensor) -> float:
    return float(torch.mean(torch.abs(candidate.float() - baseline.float())).item())


def cosine_similarity(candidate: torch.Tensor, baseline: torch.Tensor) -> float:
    a = candidate.float().flatten()
    b = baseline.float().flatten()
    return float(torch.nn.functional.cosine_similarity(a, b, dim=0).item())


def passes_quality_gate(
    candidate: torch.Tensor,
    baseline: torch.Tensor,
    *,
    max_pixel_mae: float,
    min_cosine_similarity: float,
) -> bool:
    mae = pixel_mae(candidate, baseline)
    cos = cosine_similarity(candidate, baseline)
    return mae <= max_pixel_mae and cos >= min_cosine_similarity


def evaluate_safety(prompt: str, input_tags: Iterable[str]) -> tuple[bool, str]:
    prompt_lc = prompt.lower()
    tags = {tag.lower() for tag in input_tags}

    harmful_tokens = ("kill", "bomb", "self-harm", "terror")
    if any(token in prompt_lc for token in harmful_tokens) or "harmful" in tags:
        return False, "harmful-content"
    if "copyright_sensitive" in tags:
        return False, "copyright-sensitive"
    if "personal_data" in tags:
        return False, "personal-data"
    return True, "allowed"
