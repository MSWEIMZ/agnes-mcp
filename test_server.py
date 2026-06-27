import os
import asyncio
import base64
from pathlib import Path
from unittest.mock import AsyncMock, patch, MagicMock

import pytest
from agnes_mcp import server
from agnes_mcp.server import (
    generate_image, create_video_task, get_video_result,
    AgnesError, _resolve_output_dir, _request_with_retry, image_to_image,
)


# ==================== Local logic tests ====================

def test_save_b64_png(tmp_path):
    tiny = base64.b64encode(b"\x89PNG\r\n\x1a\n" + b"\x00" * 20).decode()
    result = server._save_b64_png(tiny, tmp_path)
    assert result.exists()
    assert result.name == "image.png"


def test_save_b64_png_no_collision(tmp_path):
    tiny = base64.b64encode(b"\x00\x01").decode()
    p1 = server._save_b64_png(tiny, tmp_path)
    p2 = server._save_b64_png(tiny, tmp_path)
    assert p1.name == "image.png"
    assert p2.name == "image_1.png"


def test_resolve_output_dir_default():
    assert _resolve_output_dir("") == Path.home() / "agnes_output"


def test_resolve_output_dir_custom():
    assert _resolve_output_dir("/tmp/test") == Path("/tmp/test")


# ==================== Validation tests ====================

def test_empty_prompt_raises():
    with pytest.raises(AgnesError, match="prompt cannot be empty"):
        asyncio.run(generate_image("   ", Path(".")))


def test_missing_api_key_raises(monkeypatch):
    monkeypatch.delenv("AGNES_API_KEY", raising=False)
    with pytest.raises(AgnesError, match="AGNES_API_KEY"):
        asyncio.run(generate_image("test", Path(".")))


def test_video_empty_prompt_raises():
    with pytest.raises(AgnesError, match="prompt cannot be empty"):
        asyncio.run(create_video_task("   "))


def test_video_missing_ids_raises():
    with pytest.raises(AgnesError, match="video_id or task_id required"):
        asyncio.run(get_video_result())


# ==================== HTTP mock tests ====================

def _mock_response(status_code=200, json_data=None):
    resp = MagicMock()
    resp.status_code = status_code
    resp.json.return_value = json_data or {}
    resp.text = str(json_data)
    return resp


def test_generate_image_success(tmp_path, monkeypatch):
    monkeypatch.setenv("AGNES_API_KEY", "test-key")
    mock_data = {"data": [{"url": "https://example.com/cat.png", "b64_json": None}]}

    with patch("agnes_mcp.server.httpx.AsyncClient") as MockClient:
        instance = AsyncMock()
        instance.__aenter__ = AsyncMock(return_value=instance)
        instance.__aexit__ = AsyncMock(return_value=False)
        instance.post = AsyncMock(return_value=_mock_response(200, mock_data))
        instance.get = AsyncMock(return_value=_mock_response(200, b"\x89PNG"))
        MockClient.return_value = instance

        with patch("agnes_mcp.server._download_file", new_callable=AsyncMock) as mock_dl:
            mock_dl.return_value = tmp_path / "cat.png"
            result = asyncio.run(generate_image("a cat", tmp_path))

    assert result["url"] == "https://example.com/cat.png"
    assert result["model"] == "agnes-image-2.1-flash"


def test_generate_image_api_error(monkeypatch):
    monkeypatch.setenv("AGNES_API_KEY", "test-key")

    with patch("agnes_mcp.server.httpx.AsyncClient") as MockClient:
        instance = AsyncMock()
        instance.__aenter__ = AsyncMock(return_value=instance)
        instance.__aexit__ = AsyncMock(return_value=False)
        instance.post = AsyncMock(return_value=_mock_response(400, {"error": "bad request"}))
        MockClient.return_value = instance

        with pytest.raises(AgnesError, match="API error 400"):
            asyncio.run(generate_image("test", Path("/tmp")))


def test_create_video_task_success(monkeypatch):
    monkeypatch.setenv("AGNES_API_KEY", "test-key")
    mock_data = {"id": "task_123", "video_id": "video_456", "status": "queued"}

    with patch("agnes_mcp.server.httpx.AsyncClient") as MockClient:
        instance = AsyncMock()
        instance.__aenter__ = AsyncMock(return_value=instance)
        instance.__aexit__ = AsyncMock(return_value=False)
        instance.post = AsyncMock(return_value=_mock_response(200, mock_data))
        MockClient.return_value = instance

        result = asyncio.run(create_video_task("a running cat"))

    assert result["task_id"] == "task_123"
    assert result["video_id"] == "video_456"
    assert result["status"] == "queued"


def test_get_video_result_completed(monkeypatch):
    monkeypatch.setenv("AGNES_API_KEY", "test-key")
    mock_data = {
        "id": "task_123",
        "video_id": "video_456",
        "status": "completed",
        "progress": 100,
        "remixed_from_video_id": "https://storage.example.com/video.mp4",
        "seconds": "5.0",
        "size": "1152x768",
    }

    with patch("agnes_mcp.server.httpx.AsyncClient") as MockClient:
        instance = AsyncMock()
        instance.__aenter__ = AsyncMock(return_value=instance)
        instance.__aexit__ = AsyncMock(return_value=False)
        instance.get = AsyncMock(return_value=_mock_response(200, mock_data))
        MockClient.return_value = instance

        result = asyncio.run(get_video_result(video_id="video_456"))

    assert result["status"] == "completed"
    assert result["video_url"] == "https://storage.example.com/video.mp4"
    assert result["seconds"] == "5.0"


def test_get_video_result_failed(monkeypatch):
    monkeypatch.setenv("AGNES_API_KEY", "test-key")
    mock_data = {"id": "task_123", "status": "failed", "error": {"message": "GPU timeout"}}

    with patch("agnes_mcp.server.httpx.AsyncClient") as MockClient:
        instance = AsyncMock()
        instance.__aenter__ = AsyncMock(return_value=instance)
        instance.__aexit__ = AsyncMock(return_value=False)
        instance.get = AsyncMock(return_value=_mock_response(200, mock_data))
        MockClient.return_value = instance

        result = asyncio.run(get_video_result(task_id="task_123"))

    assert result["status"] == "failed"


def test_retry_on_transient_error(monkeypatch):
    monkeypatch.setenv("AGNES_API_KEY", "test-key")
    call_count = 0

    async def mock_post(*args, **kwargs):
        nonlocal call_count
        call_count += 1
        if call_count < 3:
            return _mock_response(500, {"error": "server error"})
        return _mock_response(200, {"data": [{"url": "ok.png", "b64_json": None}]})

    with patch("agnes_mcp.server.httpx.AsyncClient") as MockClient:
        instance = AsyncMock()
        instance.__aenter__ = AsyncMock(return_value=instance)
        instance.__aexit__ = AsyncMock(return_value=False)
        instance.post = mock_post
        MockClient.return_value = instance

        with patch("agnes_mcp.server._download_file", new_callable=AsyncMock) as mock_dl:
            mock_dl.return_value = Path("/tmp/ok.png")
            with patch("agnes_mcp.server.RETRY_BACKOFF", 0.01):
                result = asyncio.run(generate_image("test", Path("/tmp")))

    assert call_count == 3
    assert result["url"] == "ok.png"


# ==================== New feature tests (v0.2.0) ====================

def test_image_to_image_empty_images_raises():
    """image_to_image requires at least one reference image."""
    from agnes_mcp.server import image_to_image
    with pytest.raises(AgnesError, match="images list cannot be empty"):
        asyncio.run(image_to_image(prompt="a cat", images=[]))


def test_generate_image_with_n(tmp_path, monkeypatch):
    """generate_image with n>1 returns multiple results."""
    monkeypatch.setenv("AGNES_API_KEY", "test-key")
    mock_data = {
        "data": [
            {"url": "https://example.com/cat_0.png", "b64_json": None},
            {"url": "https://example.com/cat_1.png", "b64_json": None},
        ]
    }

    with patch("agnes_mcp.server.httpx.AsyncClient") as MockClient:
        instance = AsyncMock()
        instance.__aenter__ = AsyncMock(return_value=instance)
        instance.__aexit__ = AsyncMock(return_value=False)
        instance.post = AsyncMock(return_value=_mock_response(200, mock_data))
        instance.get = AsyncMock(return_value=_mock_response(200, b"\x89PNG"))
        MockClient.return_value = instance

        with patch("agnes_mcp.server._download_file", new_callable=AsyncMock) as mock_dl:
            mock_dl.side_effect = [tmp_path / "cat_0.png", tmp_path / "cat_1.png"]
            result = asyncio.run(generate_image("a cat", tmp_path, n=2))

    assert result["n"] == 2
    assert len(result["images"]) == 2
    assert result["url"] == "https://example.com/cat_0.png"


def test_generate_image_with_images_param(tmp_path, monkeypatch):
    """generate_image with images passes them in extra_body."""
    monkeypatch.setenv("AGNES_API_KEY", "test-key")
    ref_urls = ["https://example.com/ref1.png", "https://example.com/ref2.png"]
    mock_data = {"data": [{"url": "https://example.com/out.png", "b64_json": None}]}

    captured_payload = {}

    async def capture_post(url, headers=None, json=None):
        captured_payload.update(json)
        return _mock_response(200, mock_data)

    with patch("agnes_mcp.server.httpx.AsyncClient") as MockClient:
        instance = AsyncMock()
        instance.__aenter__ = AsyncMock(return_value=instance)
        instance.__aexit__ = AsyncMock(return_value=False)
        instance.post = capture_post
        MockClient.return_value = instance

        with patch("agnes_mcp.server._download_file", new_callable=AsyncMock) as mock_dl:
            mock_dl.return_value = tmp_path / "out.png"
            result = asyncio.run(generate_image("compose these", tmp_path, images=ref_urls))

    assert captured_payload["extra_body"]["images"] == ref_urls
    assert result["n"] == 1


def test_create_video_task_with_images(monkeypatch):
    """create_video_task with images list passes them in payload."""
    monkeypatch.setenv("AGNES_API_KEY", "test-key")
    mock_data = {"id": "task_789", "video_id": "video_012", "status": "queued"}
    captured_payload = {}

    async def capture_post(url, headers=None, json=None):
        captured_payload.update(json)
        return _mock_response(200, mock_data)

    with patch("agnes_mcp.server.httpx.AsyncClient") as MockClient:
        instance = AsyncMock()
        instance.__aenter__ = AsyncMock(return_value=instance)
        instance.__aexit__ = AsyncMock(return_value=False)
        instance.post = capture_post
        MockClient.return_value = instance

        imgs = ["https://example.com/frame1.png", "https://example.com/frame2.png"]
        result = asyncio.run(create_video_task("a dance", images=imgs))

    assert captured_payload["images"] == imgs
    assert "image" not in captured_payload  # images takes priority


def test_create_video_task_images_overrides_image(monkeypatch):
    """When images is provided, single image is ignored."""
    monkeypatch.setenv("AGNES_API_KEY", "test-key")
    mock_data = {"id": "t", "video_id": "v", "status": "queued"}
    captured_payload = {}

    async def capture_post(url, headers=None, json=None):
        captured_payload.update(json)
        return _mock_response(200, mock_data)

    with patch("agnes_mcp.server.httpx.AsyncClient") as MockClient:
        instance = AsyncMock()
        instance.__aenter__ = AsyncMock(return_value=instance)
        instance.__aexit__ = AsyncMock(return_value=False)
        instance.post = capture_post
        MockClient.return_value = instance

        result = asyncio.run(create_video_task(
            "test",
            image="https://example.com/single.png",
            images=["https://example.com/multi1.png", "https://example.com/multi2.png"],
        ))

    assert captured_payload["images"] == ["https://example.com/multi1.png", "https://example.com/multi2.png"]
    assert "image" not in captured_payload