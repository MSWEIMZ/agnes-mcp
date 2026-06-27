"""Agnes AI MCP Server.

Provides text-to-image, image-to-image, text-to-video, and video status
checking via the Agnes AI API (https://agnes-ai.com).

Environment variables:
    AGNES_API_KEY (required): Your Agnes AI API key.
    AGNES_API_BASE (optional): API base URL override.
    AGNES_DEFAULT_MODEL (optional): Default image model override.
    AGNES_DEFAULT_SIZE (optional): Default image size override.
"""

import os
import asyncio
import base64
import logging
from pathlib import Path
from urllib.parse import urlparse
from typing import Any

import httpx
from mcp.server.fastmcp import FastMCP

__version__ = "0.2.0"

logger = logging.getLogger(__name__)

# ==================== Configuration ====================

DEFAULT_API_BASE = "https://apihub.agnes-ai.com/v1"
DEFAULT_IMAGE_MODEL = "agnes-image-2.1-flash"
DEFAULT_VIDEO_MODEL = "agnes-video-v2.0"
DEFAULT_IMAGE_SIZE = "1024x768"
DEFAULT_TIMEOUT = 180.0
VIDEO_POLL_INTERVAL = 5.0
VIDEO_POLL_TIMEOUT = 600.0
MAX_RETRIES = 3
RETRY_BACKOFF = 2.0

AVAILABLE_IMAGE_MODELS = {
    "agnes-image-2.0-flash": "Agnes Image 2.0 Flash",
    "agnes-image-2.1-flash": "Agnes Image 2.1 Flash (recommended)",
}
AVAILABLE_VIDEO_MODELS = {
    "agnes-video-v2.0": "Agnes Video V2.0",
}


class AgnesError(Exception):
    """Custom exception for Agnes API errors."""
    pass


# ==================== Internal Helpers ====================

def _get_api_key() -> str:
    key = os.getenv("AGNES_API_KEY", "")
    if not key:
        raise AgnesError(
            "Missing AGNES_API_KEY. "
            "Set it in your MCP server config env section."
        )
    return key


def _headers() -> dict[str, str]:
    return {
        "Authorization": f"Bearer {_get_api_key()}",
        "Content-Type": "application/json",
    }


def _resolve_output_dir(output_dir: str | None) -> Path:
    if output_dir:
        return Path(output_dir)
    return Path.home() / "agnes_output"


def _save_b64_png(b64_text: str, output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    target = output_dir / "image.png"
    counter = 1
    while target.exists():
        target = output_dir / f"image_{counter}.png"
        counter += 1
    target.write_bytes(base64.b64decode(b64_text))
    return target


async def _download_file(url: str, output_dir: Path, ext: str = ".png") -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    fname = urlparse(url).path.split("/")[-1] or f"file{ext}"
    if not fname.endswith(ext):
        base = fname.rsplit(".", 1)[0] if "." in fname else fname
        fname = base + ext
    target = output_dir / fname
    counter = 1
    while target.exists():
        stem = fname.rsplit(".", 1)[0]
        target = output_dir / f"{stem}_{counter}{ext}"
        counter += 1
    async with httpx.AsyncClient(timeout=DEFAULT_TIMEOUT, follow_redirects=True) as client:
        resp = await client.get(url)
        if resp.status_code >= 400:
            raise AgnesError(f"Download failed: HTTP {resp.status_code}")
        target.write_bytes(resp.content)
    return target


async def _request_with_retry(
    method: str,
    url: str,
    *,
    json: dict[str, Any] | None = None,
    timeout: float = DEFAULT_TIMEOUT,
) -> dict[str, Any]:
    """Make an HTTP request with automatic retry on transient errors."""
    last_error: Exception | None = None
    for attempt in range(MAX_RETRIES):
        try:
            async with httpx.AsyncClient(timeout=timeout) as client:
                if method.upper() == "GET":
                    resp = await client.get(url, headers=_headers())
                else:
                    resp = await client.post(url, headers=_headers(), json=json)
                if resp.status_code == 429 or resp.status_code >= 500:
                    raise AgnesError(f"Transient error {resp.status_code}: {resp.text}")
                if resp.status_code >= 400:
                    raise AgnesError(f"API error {resp.status_code}: {resp.text}")
                return resp.json()
        except (httpx.TimeoutException, httpx.ConnectError, httpx.ReadError) as e:
            last_error = e
            if attempt < MAX_RETRIES - 1:
                wait = RETRY_BACKOFF * (2 ** attempt)
                logger.warning("Request failed (attempt %d/%d): %s. Retrying in %.1fs...",
                               attempt + 1, MAX_RETRIES, e, wait)
                await asyncio.sleep(wait)
        except AgnesError as e:
            if "Transient" in str(e) and attempt < MAX_RETRIES - 1:
                last_error = e
                wait = RETRY_BACKOFF * (2 ** attempt)
                logger.warning("Transient error (attempt %d/%d): %s. Retrying in %.1fs...",
                               attempt + 1, MAX_RETRIES, e, wait)
                await asyncio.sleep(wait)
            else:
                raise

    raise AgnesError(f"Request failed after {MAX_RETRIES} attempts: {last_error}")


# ==================== Image API ====================

async def generate_image(
    prompt: str,
    output_dir: Path,
    model: str | None = None,
    size: str | None = None,
    return_mode: str = "url",
    n: int = 1,
    images: list[str] | None = None,
) -> dict[str, Any]:
    """Generate one or more images from text + optional reference images.

    Args:
        prompt: Text description of the image to generate.
        output_dir: Directory to save downloaded images.
        model: Model name override.
        size: Output size override.
        return_mode: 'url' for image URL, 'b64' for base64 + local save.
        n: Number of images to generate (1-4).
        images: Optional list of image URLs for multi-image composition / image-to-image.

    Returns:
        dict with url, local_path, model, size, n, images (list of all generated results).
    """
    if not prompt or not prompt.strip():
        raise AgnesError("prompt cannot be empty")

    base_url = os.getenv("AGNES_API_BASE", DEFAULT_API_BASE).rstrip("/")
    resolved_model = model or os.getenv("AGNES_DEFAULT_MODEL") or DEFAULT_IMAGE_MODEL
    resolved_size = size or os.getenv("AGNES_DEFAULT_SIZE") or DEFAULT_IMAGE_SIZE

    extra_body: dict[str, Any] = {
        "response_format": "b64_json" if return_mode == "b64" else "url",
    }
    if n > 1:
        extra_body["n"] = n
    if images:
        extra_body["images"] = images

    payload: dict[str, Any] = {
        "model": resolved_model,
        "prompt": prompt.strip(),
        "size": resolved_size,
        "extra_body": extra_body,
    }

    data = await _request_with_retry("POST", f"{base_url}/images/generations", json=payload)

    results: list[dict[str, Any]] = []
    primary_url = None
    primary_local = None

    try:
        items = data["data"]
    except (KeyError, TypeError):
        raise AgnesError(f"Unexpected API response: {data}")

    for i, item in enumerate(items):
        b64_json = item.get("b64_json")
        image_url = item.get("url")
        local_path = None

        if b64_json:
            if len(items) > 1:
                output_dir.mkdir(parents=True, exist_ok=True)
                target = output_dir / f"image_{i}.png"
                target.write_bytes(base64.b64decode(b64_json))
                local_path = str(target)
            else:
                local_path = str(_save_b64_png(b64_json, output_dir))
        elif image_url:
            local_path = str(await _download_file(image_url, output_dir, ".png"))

        if i == 0:
            primary_url = image_url
            primary_local = local_path

        results.append({
            "url": image_url,
            "local_path": local_path,
        })

    return {
        "url": primary_url,
        "local_path": primary_local,
        "model": resolved_model,
        "size": resolved_size,
        "n": len(results),
        "images": results,
    }


# ==================== Video API ====================

async def create_video_task(
    prompt: str,
    model: str | None = None,
    width: int = 1152,
    height: int = 768,
    num_frames: int = 121,
    frame_rate: int = 24,
    image: str | None = None,
    images: list[str] | None = None,
    negative_prompt: str | None = None,
    seed: int | None = None,
) -> dict[str, Any]:
    if not prompt or not prompt.strip():
        raise AgnesError("prompt cannot be empty")

    base_url = os.getenv("AGNES_API_BASE", DEFAULT_API_BASE).rstrip("/")
    resolved_model = model or DEFAULT_VIDEO_MODEL

    payload: dict[str, Any] = {
        "model": resolved_model,
        "prompt": prompt.strip(),
        "width": width,
        "height": height,
        "num_frames": num_frames,
        "frame_rate": frame_rate,
    }
    # Single image (image-to-video shortcut)
    if image and not images:
        payload["image"] = image
    # Multiple images (multi-image video / keyframe animation)
    if images:
        payload["images"] = images
    if negative_prompt:
        payload["negative_prompt"] = negative_prompt
    if seed is not None:
        payload["seed"] = seed

    data = await _request_with_retry("POST", f"{base_url}/videos", json=payload)

    return {
        "task_id": data.get("id"),
        "video_id": data.get("video_id"),
        "model": resolved_model,
        "status": data.get("status", "queued"),
    }


async def get_video_result(
    video_id: str | None = None,
    task_id: str | None = None,
) -> dict[str, Any]:
    if not video_id and not task_id:
        raise AgnesError("video_id or task_id required")

    base_url = os.getenv("AGNES_API_BASE", DEFAULT_API_BASE).rstrip("/")

    if video_id:
        url = f"{base_url}/agnesapi?video_id={video_id}"
    else:
        url = f"{base_url}/videos/{task_id}"

    data = await _request_with_retry("GET", url)

    video_url = None
    if data.get("status") == "completed":
        video_url = data.get("remixed_from_video_id") or data.get("video_url")

    return {
        "task_id": data.get("id"),
        "video_id": data.get("video_id"),
        "status": data.get("status"),
        "progress": data.get("progress"),
        "video_url": video_url,
        "seconds": data.get("seconds"),
        "size": data.get("size"),
        "error": data.get("error"),
    }


async def generate_video(
    prompt: str,
    output_dir: Path,
    model: str | None = None,
    width: int = 1152,
    height: int = 768,
    num_frames: int = 121,
    frame_rate: int = 24,
    image: str | None = None,
    images: list[str] | None = None,
    negative_prompt: str | None = None,
    seed: int | None = None,
    poll_timeout: float = VIDEO_POLL_TIMEOUT,
) -> dict[str, Any]:
    task = await create_video_task(
        prompt=prompt, model=model, width=width, height=height,
        num_frames=num_frames, frame_rate=frame_rate,
        image=image, images=images,
        negative_prompt=negative_prompt, seed=seed,
    )

    video_id = task.get("video_id")
    task_id = task.get("task_id")
    if not video_id and not task_id:
        raise AgnesError(f"No video_id or task_id returned: {task}")

    start = asyncio.get_event_loop().time()
    while asyncio.get_event_loop().time() - start < poll_timeout:
        result = await get_video_result(video_id=video_id, task_id=task_id)
        status = result.get("status")
        if status == "completed":
            video_url = result.get("video_url")
            local_path = None
            if video_url:
                local_path = str(await _download_file(video_url, output_dir, ".mp4"))
            return {**result, "local_path": local_path}
        if status == "failed":
            raise AgnesError(f"Video generation failed: {result.get('error')}")
        await asyncio.sleep(VIDEO_POLL_INTERVAL)

    raise AgnesError(f"Video generation timed out after {poll_timeout}s")


# ==================== MCP Server ====================

mcp = FastMCP("agnes-mcp")


@mcp.tool()
async def text_to_image(
    prompt: str,
    model: str = "agnes-image-2.1-flash",
    size: str = "1024x768",
    n: int = 1,
    images: list[str] | None = None,
    output_dir: str = "",
    return_mode: str = "url",
) -> dict[str, Any]:
    """Generate images from text using Agnes AI.

    Supports two models:
    - agnes-image-2.0-flash: Standard quality
    - agnes-image-2.1-flash: Enhanced quality (recommended)

    Args:
        prompt: Text description of the image to generate.
        model: Model name (agnes-image-2.0-flash or agnes-image-2.1-flash).
        size: Output size (e.g. 1024x768, 1024x1024, 768x1024).
        n: Number of images to generate (1-4). Default: 1.
        images: Optional list of reference image URLs for multi-image composition.
        output_dir: Directory to save the downloaded image(s). Defaults to ~/agnes_output.
        return_mode: 'url' for image URL, 'b64' for base64 + local save.

    Returns:
        dict with url, local_path, model, size, n, images.
    """
    return await generate_image(
        prompt=prompt,
        output_dir=_resolve_output_dir(output_dir),
        model=model,
        size=size,
        return_mode=return_mode,
        n=max(1, min(n, 4)),
        images=images or None,
    )


@mcp.tool()
async def image_to_image(
    prompt: str,
    images: list[str],
    model: str = "agnes-image-2.1-flash",
    size: str = "1024x768",
    n: int = 1,
    output_dir: str = "",
    return_mode: str = "url",
) -> dict[str, Any]:
    """Generate new image(s) based on reference image(s) and a text prompt.

    This is image-to-image generation: provide one or more reference images
    (as URLs) along with a text prompt describing the desired output.

    Args:
        prompt: Text description guiding the generation.
        images: List of reference image URLs (at least one required).
        model: Model name (agnes-image-2.0-flash or agnes-image-2.1-flash).
        size: Output size (e.g. 1024x768, 1024x1024, 768x1024).
        n: Number of images to generate (1-4). Default: 1.
        output_dir: Directory to save the downloaded image(s). Defaults to ~/agnes_output.
        return_mode: 'url' for image URL, 'b64' for base64 + local save.

    Returns:
        dict with url, local_path, model, size, n, images.
    """
    if not images:
        raise AgnesError("images list cannot be empty for image-to-image generation")

    return await generate_image(
        prompt=prompt,
        output_dir=_resolve_output_dir(output_dir),
        model=model,
        size=size,
        return_mode=return_mode,
        n=max(1, min(n, 4)),
        images=images,
    )


@mcp.tool()
async def text_to_video(
    prompt: str,
    model: str = "agnes-video-v2.0",
    width: int = 1152,
    height: int = 768,
    num_frames: int = 121,
    frame_rate: int = 24,
    image: str = "",
    images: list[str] | None = None,
    negative_prompt: str = "",
    seed: int = -1,
    output_dir: str = "",
) -> dict[str, Any]:
    """Generate a video from text (and optional image(s)) using Agnes AI.

    This is an async operation that polls until completion (may take several minutes).

    Args:
        prompt: Text description of the video content.
        model: Model name. Default: agnes-video-v2.0
        width: Video width. Default: 1152
        height: Video height. Default: 768
        num_frames: Total frames (8n+1 rule, max 441).
            Common values: 81(~3s), 121(~5s), 241(~10s), 441(~18s)
        frame_rate: FPS, 1-60. Default: 24
        image: Optional single image URL for image-to-video.
        images: Optional list of image URLs for multi-image video / keyframe animation.
            When provided, 'image' is ignored.
        negative_prompt: Optional negative prompt to exclude from generation.
        seed: Optional random seed (-1 for random).
        output_dir: Directory to save the downloaded video. Defaults to ~/agnes_output.

    Returns:
        dict with video_id, status, video_url, local_path, seconds, size.
    """
    return await generate_video(
        prompt=prompt,
        output_dir=_resolve_output_dir(output_dir),
        model=model,
        width=width,
        height=height,
        num_frames=num_frames,
        frame_rate=frame_rate,
        image=image or None,
        images=images or None,
        negative_prompt=negative_prompt or None,
        seed=seed if seed >= 0 else None,
    )


@mcp.tool()
async def check_video_status(
    video_id: str = "",
    task_id: str = "",
) -> dict[str, Any]:
    """Check the status of a video generation task.

    Args:
        video_id: The video_id returned from text_to_video.
        task_id: The task_id returned from text_to_video (alternative).

    Returns:
        dict with task_id, video_id, status, progress, video_url, seconds, size, error.
    """
    return await get_video_result(
        video_id=video_id or None,
        task_id=task_id or None,
    )


@mcp.resource("agnes://config")
def get_agnes_config() -> str:
    """Show current Agnes MCP configuration (API key masked)."""
    api_key = os.getenv("AGNES_API_KEY", "")
    api_base = os.getenv("AGNES_API_BASE", DEFAULT_API_BASE)
    default_model = os.getenv("AGNES_DEFAULT_MODEL", DEFAULT_IMAGE_MODEL)

    if len(api_key) >= 10:
        masked_key = api_key[:6] + "..." + api_key[-4:]
    elif api_key:
        masked_key = "***set***"
    else:
        masked_key = "***NOT SET***"

    return (
        f"AGNES_API_BASE={api_base}\n"
        f"AGNES_DEFAULT_MODEL={default_model}\n"
        f"AGNES_API_KEY={masked_key}\n"
        f"Image models: {', '.join(AVAILABLE_IMAGE_MODELS.keys())}\n"
        f"Video models: {', '.join(AVAILABLE_VIDEO_MODELS.keys())}\n"
    )


def main():
    """Entry point for the MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()