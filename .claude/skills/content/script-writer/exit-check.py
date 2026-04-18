#!/usr/bin/env python3
"""
Exit Check: script-writer (Content Domain)
Deterministic gate verifying scene breakdown output quality.
"""

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from _utils.exit_check_base import add_issue, print_and_exit

SCENES_PATH = Path("scenes.json")
SPEC_PATH = Path(".claude/state/L2-spec.md")


def check():
    # 1. scenes.json must exist and be valid JSON
    if not SCENES_PATH.exists():
        add_issue(
            "file_missing",
            f"{SCENES_PATH} does not exist. Script-writer must produce this file.",
        )
        return  # Can't check anything else without scenes.json

    try:
        with open(SCENES_PATH, encoding="utf-8") as f:
            scenes = json.load(f)
    except json.JSONDecodeError as e:
        add_issue("invalid_json", f"{SCENES_PATH} is not valid JSON: {e}")
        return

    # 2. Must be a list or dict with "scenes" key
    if isinstance(scenes, dict):
        scene_list = scenes.get("scenes", [])
    elif isinstance(scenes, list):
        scene_list = scenes
    else:
        add_issue(
            "invalid_format",
            f"{SCENES_PATH} must be a list or dict with 'scenes' key. Got: {type(scenes).__name__}",
        )
        return

    # 3. Scene count: 2-15
    count = len(scene_list)
    if count < 2:
        add_issue(
            "too_few_scenes",
            f"Found {count} scenes. Minimum is 2. Scenes that are too short cannot convey meaningful content.",
        )
    if count > 15:
        add_issue(
            "too_many_scenes",
            f"Found {count} scenes. Maximum is 15. Consider merging related scenes.",
        )

    # 4. Each scene must have required fields
    for i, scene in enumerate(scene_list):
        sid = scene.get("id", f"index-{i}")
        if "id" not in scene:
            add_issue("missing_field", f"Scene {i} missing 'id'.")
        if "text" not in scene:
            add_issue(
                "missing_field",
                f"Scene {sid} missing 'text'. Scenes must have spoken content.",
            )
        if "estimatedDuration" not in scene:
            add_issue(
                "missing_field",
                f"Scene {sid} missing 'estimatedDuration'. Duration is needed for downstream TTS scheduling.",
            )
        elif (
            not isinstance(scene["estimatedDuration"], (int, float))
            or scene["estimatedDuration"] < 1
        ):
            add_issue(
                "invalid_duration",
                f"Scene {sid} has invalid estimatedDuration: {scene['estimatedDuration']}. Must be a number >= 1 second.",
            )
        if "visualBeats" not in scene:
            add_issue(
                "missing_field",
                f"Scene {sid} missing 'visualBeats'. Add an empty array if no beats needed.",
            )

    # 5. L2-spec.md must exist with platform and mood metadata
    if not SPEC_PATH.exists():
        add_issue(
            "spec_missing",
            f"{SPEC_PATH} does not exist. Content spec is required for downstream skills.",
        )
    else:
        content = SPEC_PATH.read_text(encoding="utf-8")
        if "Platform" not in content and "platform" not in content.lower():
            add_issue(
                "spec_missing_platform",
                f"{SPEC_PATH} must specify Platform (9:16, 16:9, or 4:5).",
            )
        if "Mood" not in content and "mood" not in content.lower():
            add_issue(
                "spec_missing_mood",
                f"{SPEC_PATH} must specify Mood (Impressed, Excited, Calm, or Inspired).",
            )

        # 6. If topic input, draft-script.md must exist and be non-empty
        if re.search(r"Input\s*:\s*topic", content, re.IGNORECASE):
            draft_path = Path("draft-script.md")
            if not draft_path.exists():
                add_issue(
                    "draft_script_missing",
                    "L2-spec.md indicates topic input but draft-script.md does not exist. "
                    "Entry B must produce a draft script before scene breakdown.",
                )
            elif not draft_path.read_text(encoding="utf-8").strip():
                add_issue(
                    "draft_script_empty",
                    "draft-script.md exists but is empty. "
                    "Entry B must produce non-empty spoken script content.",
                )


def main() -> int:
    check()
    print_and_exit("script-writer")


if __name__ == "__main__":
    raise SystemExit(main())
