import os
from pathlib import Path
import pytest
from agnes_mcp import server
from agnes_mcp.server import generate_image, create_video_task, get_video_result, AgnesError, _resolve_output_dir


def test_empty_prompt_raises():
    with pytest.raises(AgnesError, match="prompt cannot be empty"):
        generate_image("   ", Path("."))


def test_missing_api_key_raises(monkeypatch):
    monkeypatch.delenv("AGNES_API_KEY", raising=False)
    with pytest.raises(AgnesError, match="AGNES_API_KEY"):
        generate_image("test", Path("."))


def test_video_empty_prompt_raises():
    with pytest.raises(AgnesError, match="prompt cannot be empty"):
        create_video_task("   ")


def test_video_missing_ids_raises():
    with pytest.raises(AgnesError, match="video_id or task_id required"):
        get_video_result()


def test_save_b64_png(tmp_path):
    import base64
    tiny = base64.b64encode(b"\x89PNG\r\n\x1a\n" + b"\x00" * 20).decode()
    result = server._save_b64_png(tiny, tmp_path)
    assert result.exists()
    assert result.name == "image.png"


def test_save_b64_png_no_collision(tmp_path):
    import base64
    tiny = base64.b64encode(b"\x00\x01").decode()
    p1 = server._save_b64_png(tiny, tmp_path)
    p2 = server._save_b64_png(tiny, tmp_path)
    assert p1.name == "image.png"
    assert p2.name == "image_1.png"


def test_resolve_output_dir_default():
    result = _resolve_output_dir("")
    assert result == Path.home() / "agnes_output"


def test_resolve_output_dir_custom():
    result = _resolve_output_dir("/tmp/test")
    assert result == Path("/tmp/test")
