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
SPEC_PATH = Path(".claude/state/L2-content-spec.md")
L0_STRATEGY = Path(".claude/state/L0-strategy.md")


def check():
    # 1. scenes.json must exist and be valid JSON
    if not SCENES_PATH.exists():
        add_issue(
            "file_missing",
            f"{SCENES_PATH} does not exist. Script-writer must produce this file.",
            level="high",
        )
        return  # Can't check anything else without scenes.json

    try:
        with open(SCENES_PATH, encoding="utf-8") as f:
            scenes = json.load(f)
    except json.JSONDecodeError as e:
        add_issue("invalid_json", f"{SCENES_PATH} is not valid JSON: {e}", level="high")
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
            level="high",
        )
    if count > 15:
        add_issue(
            "too_many_scenes",
            f"Found {count} scenes. Maximum is 15. Consider merging related scenes.",
            level="high",
        )

    # 4. Each scene must have required fields
    for i, scene in enumerate(scene_list):
        sid = scene.get("id", f"index-{i}")
        if "id" not in scene:
            add_issue("missing_field", f"Scene {i} missing 'id'.", level="high")
        if "text" not in scene:
            add_issue(
                "missing_field",
                f"Scene {sid} missing 'text'. Scenes must have spoken content.",
                level="high",
            )
        if "estimatedDuration" not in scene:
            add_issue(
                "missing_field",
                f"Scene {sid} missing 'estimatedDuration'. Duration is needed for downstream TTS scheduling.",
                level="high",
            )
        elif (
            not isinstance(scene["estimatedDuration"], (int, float))
            or scene["estimatedDuration"] < 1
        ):
            add_issue(
                "invalid_duration",
                f"Scene {sid} has invalid estimatedDuration: {scene['estimatedDuration']}. Must be a number >= 1 second.",
                level="high",
            )
        if "visualBeats" not in scene:
            add_issue(
                "missing_field",
                f"Scene {sid} missing 'visualBeats'. Add an empty array if no beats needed.",
                level="high",
            )

    # 5. L2-content-spec.md must exist with platform and mood metadata
    if not SPEC_PATH.exists():
        add_issue(
            "spec_missing",
            f"{SPEC_PATH} does not exist. Content spec is required for downstream skills.",
            level="high",
        )
    else:
        content = SPEC_PATH.read_text(encoding="utf-8")
        if "Platform" not in content and "platform" not in content.lower():
            add_issue(
                "spec_missing_platform",
                f"{SPEC_PATH} must specify Platform (9:16, 16:9, or 4:5).",
                level="high",
            )
        if "Mood" not in content and "mood" not in content.lower():
            add_issue(
                "spec_missing_mood",
                f"{SPEC_PATH} must specify Mood (Impressed, Excited, Calm, or Inspired).",
                level="high",
            )

        # 5a. PM Gate: Business Goal, Core Message, Differentiation from L0
        if "## Business Goal" not in content:
            add_issue(
                "spec_missing_business_goal",
                f"{SPEC_PATH} missing Business Goal. CG0 requires alignment with strategic intent.",
                level="warning",
            )
        if "## Core Message" not in content:
            add_issue(
                "spec_missing_core_message",
                f"{SPEC_PATH} missing Core Message. What is the ONE thing the audience should remember?",
                level="warning",
            )
        if "## Differentiation" not in content:
            add_issue(
                "spec_missing_differentiation",
                f"{SPEC_PATH} missing Differentiation. How does this content stand out?",
                level="warning",
            )

        # 6. If topic input, draft-script.md must exist and be non-empty
        if re.search(r"Input\s*:\s*topic", content, re.IGNORECASE):
            draft_path = Path("draft-script.md")
            if not draft_path.exists():
                add_issue(
                    "draft_script_missing",
                    "L2-content-spec.md indicates topic input but draft-script.md does not exist. "
                    "Entry B must produce a draft script before scene breakdown.",
                    level="high",
                )
            elif not draft_path.read_text(encoding="utf-8").strip():
                add_issue(
                    "draft_script_empty",
                    "draft-script.md exists but is empty. "
                    "Entry B must produce non-empty spoken script content.",
                    level="high",
                )

    # 7. L0-strategy.md → L2-content-spec.md traceability (CG0 alignment)
    if L0_STRATEGY.exists() and SPEC_PATH.exists():
        l0_content = L0_STRATEGY.read_text(encoding="utf-8")
        l2_content = SPEC_PATH.read_text(encoding="utf-8")

        # If L0 has Target Audience, L2 should reference audience
        if "## Target Audience" in l0_content:
            if "audience" not in l2_content.lower() and "受众" not in l2_content:
                add_issue(
                    "l0_l2_audience_gap",
                    "L0-strategy.md defines Target Audience but L2-content-spec.md does not reference it. "
                    "CG0 traceability requires audience alignment.",
                    level="warning",
                )

        # If L0 has KPI, L2 should reference metrics or KPI
        if "## KPI" in l0_content:
            if "kpi" not in l2_content.lower() and "metric" not in l2_content.lower():
                add_issue(
                    "l0_l2_kpi_gap",
                    "L0-strategy.md defines KPI but L2-content-spec.md does not reference metrics. "
                    "CG0 traceability requires KPI alignment.",
                    level="warning",
                )
    elif L0_STRATEGY.exists() and not SPEC_PATH.exists():
        add_issue(
            "l0_exists_but_l2_missing",
            "L0-strategy.md exists but L2-content-spec.md is missing. Cannot verify CG0 traceability.",
            level="info",
        )


def main() -> int:
    check()
    print_and_exit("script-writer")


if __name__ == "__main__":
    raise SystemExit(main())
