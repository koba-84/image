from __future__ import annotations

import base64
import json
from io import BytesIO

import pytest
import torch
from PIL import Image

from image_ai.config import RuntimeConfig
from image_ai.pipeline_runner import (
    GoogleImagenAPIBackend,
    IdeogramAPIBackend,
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


def _base_cfg(model_id: str = "openai:gpt-image-1") -> RuntimeConfig:
    return RuntimeConfig(
        mode="text2img",
        model_id=model_id,
        prompt="test",
        output="outputs/test.png",
    )


def _png_bytes() -> bytes:
    image = Image.new("RGB", (2, 2), color=(255, 0, 0))
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    return buffer.getvalue()


@pytest.mark.parametrize(
    ("model_id", "provider", "model_name"),
    [
        ("openai:gpt-image-1", "openai", "gpt-image-1"),
        ("google:imagen-3.0-generate-002", "google", "imagen-3.0-generate-002"),
        ("ideogram:v2", "ideogram", "v2"),
    ],
)
def test_resolve_backend_for_api_prefix(
    model_id: str, provider: str, model_name: str
) -> None:
    backend = resolve_backend(model_id)
    assert backend.backend == "api"
    assert backend.provider == provider
    assert backend.model_name == model_name


def test_load_pipeline_for_mode_returns_openai_backend() -> None:
    pipe = load_pipeline_for_mode("text2img", "openai:gpt-image-1", torch.float16)
    assert getattr(pipe, "is_api_backend", False)
    assert pipe.provider == "openai"


def test_load_pipeline_for_mode_returns_google_backend() -> None:
    pipe = load_pipeline_for_mode(
        "text2img", "google:imagen-3.0-generate-002", torch.float16
    )
    assert getattr(pipe, "is_api_backend", False)
    assert pipe.provider == "google"


def test_load_pipeline_for_mode_returns_ideogram_backend() -> None:
    pipe = load_pipeline_for_mode("text2img", "ideogram:v2", torch.float16)
    assert getattr(pipe, "is_api_backend", False)
    assert pipe.provider == "ideogram"


def test_openai_backend_rejects_unsupported_modes() -> None:
    backend = OpenAIImageAPIBackend("gpt-image-1")
    cfg = _base_cfg()
    cfg.mode = "img2img"

    with pytest.raises(NotImplementedError, match="only text2img"):
        backend.generate(cfg)


def test_google_backend_rejects_unsupported_modes() -> None:
    backend = GoogleImagenAPIBackend("imagen-3.0-generate-002")
    cfg = _base_cfg("google:imagen-3.0-generate-002")
    cfg.mode = "inpaint"

    with pytest.raises(NotImplementedError, match="only text2img"):
        backend.generate(cfg)


def test_ideogram_backend_rejects_unsupported_modes() -> None:
    backend = IdeogramAPIBackend("v2")
    cfg = _base_cfg("ideogram:v2")
    cfg.mode = "img2img"

    with pytest.raises(NotImplementedError, match="only text2img"):
        backend.generate(cfg)


def test_openai_backend_requires_api_key(monkeypatch: pytest.MonkeyPatch) -> None:
    backend = OpenAIImageAPIBackend("gpt-image-1")
    cfg = _base_cfg()
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    with pytest.raises(RuntimeError, match="OPENAI_API_KEY"):
        backend.generate(cfg)


def test_google_backend_requires_env_vars(monkeypatch: pytest.MonkeyPatch) -> None:
    backend = GoogleImagenAPIBackend("imagen-3.0-generate-002")
    cfg = _base_cfg("google:imagen-3.0-generate-002")
    monkeypatch.delenv("GOOGLE_VERTEX_ACCESS_TOKEN", raising=False)
    monkeypatch.delenv("GOOGLE_CLOUD_PROJECT", raising=False)
    monkeypatch.delenv("GOOGLE_CLOUD_LOCATION", raising=False)

    with pytest.raises(RuntimeError, match="GOOGLE_VERTEX_ACCESS_TOKEN"):
        backend.generate(cfg)


def test_ideogram_backend_requires_api_key(monkeypatch: pytest.MonkeyPatch) -> None:
    backend = IdeogramAPIBackend("v2")
    cfg = _base_cfg("ideogram:v2")
    monkeypatch.delenv("IDEOGRAM_API_KEY", raising=False)

    with pytest.raises(RuntimeError, match="IDEOGRAM_API_KEY"):
        backend.generate(cfg)


def test_openai_backend_decodes_b64_response(monkeypatch: pytest.MonkeyPatch) -> None:
    backend = OpenAIImageAPIBackend("gpt-image-1")
    cfg = _base_cfg()
    monkeypatch.setenv("OPENAI_API_KEY", "dummy-key")

    encoded = base64.b64encode(_png_bytes()).decode("utf-8")
    payload = json.dumps({"data": [{"b64_json": encoded}]}).encode("utf-8")

    def _fake_urlopen(_request):
        return _UrlopenResponse(payload)

    monkeypatch.setattr("image_ai.pipeline_runner.urllib_request.urlopen", _fake_urlopen)

    result = backend.generate(cfg)
    assert isinstance(result, Image.Image)
    assert result.size == (2, 2)


def test_google_backend_decodes_b64_response(monkeypatch: pytest.MonkeyPatch) -> None:
    backend = GoogleImagenAPIBackend("imagen-3.0-generate-002")
    cfg = _base_cfg("google:imagen-3.0-generate-002")
    monkeypatch.setenv("GOOGLE_VERTEX_ACCESS_TOKEN", "token")
    monkeypatch.setenv("GOOGLE_CLOUD_PROJECT", "proj")
    monkeypatch.setenv("GOOGLE_CLOUD_LOCATION", "us-central1")

    encoded = base64.b64encode(_png_bytes()).decode("utf-8")
    payload = json.dumps({"predictions": [{"bytesBase64Encoded": encoded}]}).encode(
        "utf-8"
    )

    def _fake_urlopen(_request):
        return _UrlopenResponse(payload)

    monkeypatch.setattr("image_ai.pipeline_runner.urllib_request.urlopen", _fake_urlopen)

    result = backend.generate(cfg)
    assert isinstance(result, Image.Image)
    assert result.size == (2, 2)


def test_ideogram_backend_fetches_image_url(monkeypatch: pytest.MonkeyPatch) -> None:
    backend = IdeogramAPIBackend("v2")
    cfg = _base_cfg("ideogram:v2")
    monkeypatch.setenv("IDEOGRAM_API_KEY", "dummy-key")

    api_payload = json.dumps({"data": [{"url": "https://example.test/image.png"}]}).encode(
        "utf-8"
    )
    image_bytes = _png_bytes()

    def _fake_urlopen(request_or_url):
        url = (
            request_or_url
            if isinstance(request_or_url, str)
            else request_or_url.full_url
        )
        if url == "https://example.test/image.png":
            return _UrlopenResponse(image_bytes)
        return _UrlopenResponse(api_payload)

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
