#!/usr/bin/env python3
"""
Exit Check: video-compositor (Content Domain)
Deterministic gate verifying video output quality.
"""

import json
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Optional

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from _utils.exit_check_base import add_issue, print_and_exit

SCENES_PATH = Path("scenes.json")
SPEC_PATH = Path(".claude/state/L2-content-spec.md")
BASE_VIDEO_PATH = Path("base-video.mp4")
FINAL_VIDEO_PATH = Path("final-video.mp4")

# Platform resolution map
RESOLUTIONS = {
    "9:16": (1080, 1920),
    "16:9": (1920, 1080),
    "4:5": (1080, 1350),
}

MIN_FPS = 24


def get_platform() -> str:
    """Extract platform from L2-content-spec.md."""
    if not SPEC_PATH.exists():
        return "16:9"  # Default
    content = SPEC_PATH.read_text(encoding="utf-8").lower()
    if "9:16" in content or "9\\:16" in content or "9x16" in content:
        return "9:16"
    elif "4:5" in content or "4\\:5" in content or "4x5" in content:
        return "4:5"
    return "16:9"


def get_video_info(video_path: Path) -> Optional[dict]:
    """Use ffprobe to get video info."""
    try:
        result = subprocess.run(
            [
                "ffprobe",
                "-v",
                "quiet",
                "-print_format",
                "json",
                "-show_streams",
                "-show_format",
                str(video_path),
            ],
            capture_output=True,
            text=True,
            timeout=30,
        )
        if result.returncode != 0:
            return None
        return json.loads(result.stdout)
    except (FileNotFoundError, subprocess.TimeoutExpired, json.JSONDecodeError):
        return None


def check():
    # 0. Check ffprobe availability
    if not shutil.which("ffprobe"):
        add_issue(
            "ffprobe_missing",
            "ffprobe is not installed or not in PATH. Video validation requires ffmpeg/ffprobe. "
            "Install with: brew install ffmpeg (macOS) or apt install ffmpeg (Linux).",
        )

    platform = get_platform()
    expected_width, expected_height = RESOLUTIONS.get(platform, (1920, 1080))

    # 1. Base video must exist
    if not BASE_VIDEO_PATH.exists():
        add_issue(
            "base_video_missing",
            f"{BASE_VIDEO_PATH} does not exist. Remotion must produce a base video first.",
        )
    else:
        info = get_video_info(BASE_VIDEO_PATH)
        if info is None:
            add_issue(
                "base_video_unreadable",
                f"Cannot read {BASE_VIDEO_PATH} with ffprobe. Ensure ffmpeg/ffprobe is installed and the file is a valid video.",
            )
        else:
            # Check resolution
            try:
                video_stream = next(
                    s for s in info.get("streams", []) if s.get("codec_type") == "video"
                )
                width = int(video_stream.get("width", 0))
                height = int(video_stream.get("height", 0))
                if width != expected_width or height != expected_height:
                    add_issue(
                        "resolution_mismatch",
                        f"Base video resolution {width}x{height} doesn't match platform {platform} ({expected_width}x{expected_height}).",
                    )

                # Check fps
                fps_str = video_stream.get("r_frame_rate", "0/1")
                if "/" in fps_str:
                    num, den = fps_str.split("/")
                    fps = int(num) / max(int(den), 1)
                else:
                    fps = float(fps_str)
                if fps < MIN_FPS:
                    add_issue(
                        "fps_too_low",
                        f"Base video fps ({fps:.1f}) is below minimum {MIN_FPS}.",
                    )
            except (StopIteration, ValueError, KeyError):
                add_issue(
                    "base_video_no_stream",
                    f"Cannot find video stream in {BASE_VIDEO_PATH}.",
                )

    # 2. Final video must exist
    if not FINAL_VIDEO_PATH.exists():
        add_issue(
            "final_video_missing",
            f"{FINAL_VIDEO_PATH} does not exist. Video composition must produce the final video.",
        )
    else:
        info = get_video_info(FINAL_VIDEO_PATH)
        if info is None:
            add_issue(
                "final_video_unreadable",
                f"Cannot read {FINAL_VIDEO_PATH} with ffprobe.",
            )
        else:
            # Check fps for final video too
            try:
                video_stream = next(
                    s for s in info.get("streams", []) if s.get("codec_type") == "video"
                )
                fps_str = video_stream.get("r_frame_rate", "0/1")
                if "/" in fps_str:
                    num, den = fps_str.split("/")
                    fps = int(num) / max(int(den), 1)
                else:
                    fps = float(fps_str)
                if fps < MIN_FPS:
                    add_issue(
                        "final_fps_too_low",
                        f"Final video fps ({fps:.1f}) is below minimum {MIN_FPS}.",
                    )
            except (StopIteration, ValueError, KeyError):
                add_issue(
                    "final_video_no_stream",
                    f"Cannot find video stream in {FINAL_VIDEO_PATH}.",
                )

    # 3. Duration sanity check (if we have both scenes and video)
    if FINAL_VIDEO_PATH.exists() and SCENES_PATH.exists():
        try:
            with open(SCENES_PATH, encoding="utf-8") as f:
                scenes = json.load(f)
            if isinstance(scenes, dict):
                scene_list = scenes.get("scenes", [])
            else:
                scene_list = scenes
            estimated_total = sum(s.get("estimatedDuration", 0) for s in scene_list)

            if estimated_total > 0 and FINAL_VIDEO_PATH.exists():
                final_info = get_video_info(FINAL_VIDEO_PATH)
                if final_info:
                    try:
                        duration = float(
                            final_info.get("format", {}).get("duration", 0)
                        )
                        if duration > 0:
                            ratio = duration / estimated_total
                            if ratio < 0.95 or ratio > 1.05:
                                add_issue(
                                    "duration_mismatch",
                                    f"Video duration ({duration:.1f}s) is {ratio:.0%} of estimated ({estimated_total}s). "
                                    f"Expected within 95%-105%.",
                                )
                    except (ValueError, KeyError):
                        pass
        except (json.JSONDecodeError, KeyError):
            pass


def main() -> int:
    check()
    print_and_exit("video-compositor")


if __name__ == "__main__":
    raise SystemExit(main())
