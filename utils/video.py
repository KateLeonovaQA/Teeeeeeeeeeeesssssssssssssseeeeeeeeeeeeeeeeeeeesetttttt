"""Text-to-video through the gateway's video MCP server (ByteDance Seedance 2.5)."""

from __future__ import annotations

import json
from functools import cache
from pathlib import Path

import requests
from clients.litellm_client import get_headers, litellm_request
from core.logging import get_logger

MIN_SECONDS = 4
MAX_SECONDS = 12
DEFAULT_SECONDS = 5

MCP_TIMEOUT = 60

logger = get_logger("video")


class VideoToolError(RuntimeError):
    """The tool said no. A broken gateway raises plain RuntimeError instead."""


@cache
def _server_id() -> str:
    r = litellm_request("GET", "/v1/mcp/server", headers=get_headers())
    if r.status_code != 200:
        raise RuntimeError(
            f"Could not list MCP servers ({r.status_code}): {r.text[:200]}"
        )

    for server in r.json():
        if "video" in (server.get("server_name") or ""):
            return server["server_id"]
    raise RuntimeError("No video MCP server is registered on this gateway.")


def _call_tool(name: str, arguments: dict, timeout: int, max_retries: int = 3) -> dict:
    r = litellm_request(
        "POST",
        "/mcp-rest/tools/call",
        headers=get_headers(),
        json={"name": name, "server_id": _server_id(), "arguments": arguments},
        timeout=timeout,
        max_retries=max_retries,
    )
    if r.status_code != 200:
        logger.error(
            f"MCP call failed: tool={name} status={r.status_code} body={r.text[:300]}"
        )
        raise RuntimeError(f"{name} failed ({r.status_code}): {r.text[:300]}")

    # A refusal is a normal 200 with isError set.
    result = r.json()
    text = result["content"][0]["text"]
    if result.get("isError"):
        logger.error(f"MCP tool reported an error: tool={name} detail={text[:300]}")
        raise VideoToolError(text)
    return json.loads(text)


def submit_video(prompt: str, seconds: int = DEFAULT_SECONDS) -> str:
    """Start a render and return its video_id. Costs money — one call, one clip."""
    if not prompt.strip():
        raise ValueError("prompt is empty — nothing to generate")
    # Callers sometimes pass "8", not 8.
    if not str(seconds).isdigit() or not MIN_SECONDS <= int(seconds) <= MAX_SECONDS:
        raise ValueError(
            f"seconds must be a whole number between {MIN_SECONDS} and {MAX_SECONDS}"
        )
    seconds = int(seconds)

    # No retry: a repeat submit is a second clip and a second charge.
    result = _call_tool(
        "generate_video",
        {"prompt": prompt, "seconds": seconds},
        timeout=MCP_TIMEOUT,
        max_retries=1,
    )

    video_id = result["video_id"]
    logger.info(
        f"Video submitted: id={video_id} seconds={seconds} prompt={prompt[:120]!r}"
    )
    return video_id


def check_video(video_id: str) -> dict:
    """Read a clip's state. Free. A dead job comes back as status 'failed'."""
    try:
        info = _call_tool(
            "check_video_generation_result",
            {"video_id": video_id},
            timeout=MCP_TIMEOUT,
        )
    except VideoToolError as e:
        info = {"status": "failed", "error": str(e)}

    logger.info(f"Video check: id={video_id} status={info.get('status')}")
    return info


def download_video(video_url: str, output: str = "generated_video.mp4") -> str:
    """Save a finished clip. The URL is public, so no auth header."""
    r = requests.get(video_url, timeout=300)
    if r.status_code != 200:
        logger.error(f"Video download failed: status={r.status_code} url={video_url}")
        raise RuntimeError(f"Download failed ({r.status_code}): {r.text[:200]}")

    # An error page saved as .mp4 is what used to make clips unplayable.
    if r.content[4:8] != b"ftyp":
        logger.error(
            f"Video download was not an mp4: bytes={len(r.content)} url={video_url}"
        )
        raise RuntimeError(f"Downloaded {len(r.content)} bytes that are not an mp4.")

    Path(output).parent.mkdir(parents=True, exist_ok=True)
    Path(output).write_bytes(r.content)
    logger.info(f"Video saved: output={output} bytes={len(r.content)}")
    return output
