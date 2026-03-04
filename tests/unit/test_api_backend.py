from __future__ import annotations

import base64
import json

import pytest
import torch
from PIL import Image

from image_ai.config import RuntimeConfig
from image_ai.pipeline_runner import (
    OpenAIImageAPIBackend,
    load_pipeline_for_mode,
    resolve_backend,
    run_inference,
)

pytestmark = pytest.mark.unit


class _UrlopenResponse:
    def __init__(self, body: bytes) -> None:
        self._body = body

    def read(self) -> bytes:
        return self._body

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        return None


def _base_cfg() -> RuntimeConfig:
    return RuntimeConfig(
        mode="text2img",
        model_id="openai:gpt-image-1",
        prompt="test",
        output="outputs/test.png",
    )


def test_resolve_backend_for_openai_prefix() -> None:
    backend = resolve_backend("openai:gpt-image-1")
    assert backend.backend == "api"
    assert backend.provider == "openai"
    assert backend.model_name == "gpt-image-1"


def test_load_pipeline_for_mode_returns_openai_backend() -> None:
    pipe = load_pipeline_for_mode("text2img", "openai:gpt-image-1", torch.float16)
    assert getattr(pipe, "is_api_backend", False)
    assert pipe.provider == "openai"


def test_openai_backend_rejects_unsupported_modes() -> None:
    backend = OpenAIImageAPIBackend("gpt-image-1")
    cfg = _base_cfg()
    cfg.mode = "img2img"

    with pytest.raises(NotImplementedError, match="only text2img"):
        backend.generate(cfg)


def test_openai_backend_requires_api_key(monkeypatch: pytest.MonkeyPatch) -> None:
    backend = OpenAIImageAPIBackend("gpt-image-1")
    cfg = _base_cfg()
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    with pytest.raises(RuntimeError, match="OPENAI_API_KEY"):
        backend.generate(cfg)


def test_openai_backend_decodes_b64_response(monkeypatch: pytest.MonkeyPatch) -> None:
    backend = OpenAIImageAPIBackend("gpt-image-1")
    cfg = _base_cfg()
    monkeypatch.setenv("OPENAI_API_KEY", "dummy-key")

    image = Image.new("RGB", (2, 2), color=(255, 0, 0))
    from io import BytesIO

    buffer = BytesIO()
    image.save(buffer, format="PNG")
    encoded = base64.b64encode(buffer.getvalue()).decode("utf-8")

    payload = json.dumps({"data": [{"b64_json": encoded}]}).encode("utf-8")

    def _fake_urlopen(_request):
        return _UrlopenResponse(payload)

    monkeypatch.setattr("image_ai.pipeline_runner.urllib_request.urlopen", _fake_urlopen)

    result = backend.generate(cfg)

    assert isinstance(result, Image.Image)
    assert result.size == (2, 2)


def test_run_inference_uses_api_backend_generate() -> None:
    cfg = _base_cfg()
    expected = object()

    class _APIStub:
        is_api_backend = True

        def generate(self, _cfg: RuntimeConfig):
            assert _cfg is cfg
            return expected

    assert run_inference(_APIStub(), cfg) is expected
