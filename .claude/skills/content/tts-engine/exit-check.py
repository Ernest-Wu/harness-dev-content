#!/usr/bin/env python3
"""
Exit Check: tts-engine (Content Domain)
Deterministic gate verifying TTS audio output and subtitle quality.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from _utils.exit_check_base import add_issue, print_and_exit

SCENES_PATH = Path("scenes.json")
AUDIO_DIR = Path("audio")
SUBTITLES_PATH = Path("subtitles.json")
SPEC_PATH = Path(".claude/state/L2-content-spec.md")


def check():
    # 1. Audio directory must exist
    if not AUDIO_DIR.exists() or not AUDIO_DIR.is_dir():
        add_issue(
            "audio_dir_missing",
            f"{AUDIO_DIR} directory does not exist. TTS must produce per-scene audio files.",
        )
        # Can't check audio files without the directory
        return

    # 2. Load scenes to check each has corresponding audio
    scene_ids = []
    if SCENES_PATH.exists():
        try:
            with open(SCENES_PATH, encoding="utf-8") as f:
                scenes = json.load(f)
            if isinstance(scenes, dict):
                scene_list = scenes.get("scenes", [])
            else:
                scene_list = scenes
            scene_ids = [s.get("id", "") for s in scene_list if "id" in s]
        except json.JSONDecodeError:
            add_issue(
                "scenes_invalid",
                f"{SCENES_PATH} is not valid JSON. Cannot verify audio-file correspondence.",
            )

    # 3. Check each scene has an audio file
    if scene_ids:
        for sid in scene_ids:
            audio_file = AUDIO_DIR / f"{sid}.mp3"
            if not audio_file.exists():
                add_issue(
                    "audio_missing",
                    f"Audio file missing for scene {sid}: expected {audio_file}",
                )
            elif audio_file.stat().st_size < 100:  # Suspiciously small
                add_issue(
                    "audio_too_small",
                    f"Audio file {audio_file} is suspiciously small ({audio_file.stat().st_size} bytes). May be corrupt.",
                )
    else:
        # Fallback: check at least some mp3 files exist
        mp3_files = list(AUDIO_DIR.glob("*.mp3"))
        if not mp3_files:
            add_issue(
                "no_audio_files",
                f"No .mp3 files found in {AUDIO_DIR}. TTS must produce audio output.",
            )

    # 4. subtitles.json must exist and be valid
    if not SUBTITLES_PATH.exists():
        add_issue(
            "subtitles_missing",
            f"{SUBTITLES_PATH} does not exist. TTS must produce timed subtitles.",
        )
    else:
        try:
            with open(SUBTITLES_PATH, encoding="utf-8") as f:
                subs = json.load(f)

            if not isinstance(subs, list) or len(subs) == 0:
                add_issue(
                    "subtitles_empty",
                    f"{SUBTITLES_PATH} must be a non-empty array of subtitle entries.",
                )
            else:
                for i, sub in enumerate(subs):
                    if "text" not in sub:
                        add_issue(
                            "subtitle_missing_field",
                            f"Subtitle entry {i} missing 'text'.",
                        )
                    if "startMs" not in sub:
                        add_issue(
                            "subtitle_missing_field",
                            f"Subtitle entry {i} missing 'startMs'.",
                        )
                    if "endMs" not in sub:
                        add_issue(
                            "subtitle_missing_field",
                            f"Subtitle entry {i} missing 'endMs'.",
                        )
                    elif sub.get("endMs", 0) <= sub.get("startMs", 0):
                        add_issue(
                            "subtitle_invalid_time",
                            f"Subtitle entry {i}: endMs ({sub.get('endMs')}) must be > startMs ({sub.get('startMs')}).",
                        )
        except json.JSONDecodeError:
            add_issue("subtitles_invalid_json", f"{SUBTITLES_PATH} is not valid JSON.")

    # 5. Basic duration sanity check (if we have both scenes and audio files)
    estimated_total = 0
    if SCENES_PATH.exists():
        try:
            with open(SCENES_PATH, encoding="utf-8") as f:
                scenes = json.load(f)
            if isinstance(scenes, dict):
                scene_list = scenes.get("scenes", [])
            else:
                scene_list = scenes
            estimated_total = sum(s.get("estimatedDuration", 0) for s in scene_list)
        except (json.JSONDecodeError, KeyError):
            pass

    if estimated_total > 0 and SUBTITLES_PATH.exists():
        try:
            with open(SUBTITLES_PATH, encoding="utf-8") as f:
                subs = json.load(f)
            if isinstance(subs, list) and len(subs) > 0:
                actual_total_ms = subs[-1].get("endMs", 0)
                actual_total_s = actual_total_ms / 1000
                ratio = actual_total_s / estimated_total
                if ratio < 0.7 or ratio > 1.3:
                    add_issue(
                        "duration_mismatch",
                        f"Total audio duration ({actual_total_s:.1f}s) is {ratio:.0%} of estimated ({estimated_total}s). "
                        f"Expected within 70%-130%. Consider revisiting scene segmentation.",
                    )
        except (json.JSONDecodeError, KeyError, IndexError):
            pass


def main() -> int:
    check()
    print_and_exit("tts-engine")


if __name__ == "__main__":
    raise SystemExit(main())
