from __future__ import annotations

import json
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


REGISTRY_PATH = Path(__file__).with_name("model_registry.json")
HF_TOP_MODELS_API = (
    "https://huggingface.co/api/models"
    "?pipeline_tag=text-to-image&sort=downloads&direction=-1&limit=200"
)

FAMILY_KEYWORDS = {
    "qwen-image": ("qwen-image",),
    "hidream-i1": ("hidream-i1",),
    "cogview4": ("cogview4",),
    "janus-pro": ("janus-pro",),
    "glm-4.1v": ("glm-4.1v",),
    "flux1": ("flux.1",),
    "sdxl-lightning": ("sdxl-lightning",),
    "hunyuan-dit": ("hunyuan dit", "hunyuandit"),
}


def _load_registry() -> dict:
    return json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))


def _fetch_json(url: str) -> dict | list:
    req = urllib.request.Request(url, headers={"User-Agent": "image-ai-audit"})
    with urllib.request.urlopen(req, timeout=30) as res:
        return json.loads(res.read().decode("utf-8"))


def _validate_unique_family(models: list[dict], label: str, errors: list[str]) -> None:
    seen: set[str] = set()
    for model in models:
        family = model.get("family")
        if not family:
            errors.append(f"{label}: missing family field")
            continue
        if family in seen:
            errors.append(f"{label}: duplicate family '{family}'")
        seen.add(family)


def _validate_fields(models: list[dict], required: tuple[str, ...], label: str, errors: list[str]) -> None:
    for model in models:
        missing = [key for key in required if not model.get(key)]
        if missing:
            errors.append(f"{label}: {model.get('family', '<unknown>')} missing {', '.join(missing)}")


def _verify_hf_models(models: list[dict], errors: list[str]) -> None:
    for model in models:
        model_id = model["model_id"]
        api_url = f"https://huggingface.co/api/models/{urllib.parse.quote(model_id, safe='/')}"
        try:
            meta = _fetch_json(api_url)
        except urllib.error.HTTPError as exc:
            errors.append(f"open_weight_models: {model_id} metadata fetch failed ({exc.code})")
            continue
        if isinstance(meta, dict) and meta.get("disabled"):
            errors.append(f"open_weight_models: {model_id} is disabled on HF")


def _verify_coverage(models: list[dict], warnings: list[str]) -> None:
    top_models = _fetch_json(HF_TOP_MODELS_API)
    if not isinstance(top_models, list):
        warnings.append("coverage: failed to fetch HF top model list")
        return

    top_ids = [str(model.get("id", "")).lower() for model in top_models]
    selected_families = {model["family"] for model in models}

    for family, needles in FAMILY_KEYWORDS.items():
        present_in_top = any(any(n in model_id for n in needles) for model_id in top_ids)
        if present_in_top and family not in selected_families:
            warnings.append(f"coverage: family '{family}' appears in HF top list but is not selected")


def main() -> int:
    registry = _load_registry()
    open_models = registry.get("open_weight_models", [])
    closed_models = registry.get("closed_api_models", [])

    errors: list[str] = []
    warnings: list[str] = []

    _validate_unique_family(open_models, "open_weight_models", errors)
    _validate_unique_family(closed_models, "closed_api_models", errors)
    _validate_fields(
        open_models,
        ("family", "model_id", "evidence"),
        "open_weight_models",
        errors,
    )
    _validate_fields(
        closed_models,
        ("family", "model_id", "provider", "api_reference"),
        "closed_api_models",
        errors,
    )
    _verify_hf_models(open_models, errors)
    _verify_coverage(open_models, warnings)

    print("=== Model Audit Report ===")
    print(f"open_weight_models: {len(open_models)}")
    print(f"closed_api_models: {len(closed_models)}")
    if warnings:
        print("warnings:")
        for warning in warnings:
            print(f"- {warning}")
    if errors:
        print("errors:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("status: ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
