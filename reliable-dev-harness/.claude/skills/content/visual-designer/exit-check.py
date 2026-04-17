#!/usr/bin/env python3
"""
Exit Check: visual-designer (Content Domain)
Deterministic gate verifying HTML slides output quality.
"""

import re
import sys
from pathlib import Path

SLIDES_PATH = Path("slides-preview.html")
DESIGN_SPEC_PATH = Path(".claude/state/L3-design.md")
SCENES_PATH = Path("scenes.json")

ISSUES = []


def check():
    # 1. slides-preview.html must exist and be valid HTML
    if not SLIDES_PATH.exists():
        ISSUES.append(
            (
                "file_missing",
                f"{SLIDES_PATH} does not exist. visual-designer must produce this file.",
            )
        )
        return

    html_content = SLIDES_PATH.read_text(encoding="utf-8")

    if (
        not html_content.strip().startswith("<")
        and not "<html" in html_content.lower()[:200]
    ):
        ISSUES.append(
            (
                "invalid_html",
                f"{SLIDES_PATH} does not appear to be valid HTML. Must start with <!DOCTYPE html> or <html>.",
            )
        )

    # 2. Must contain data-beat-at attributes
    if "data-beat-at" not in html_content:
        ISSUES.append(
            (
                "missing_beat_attributes",
                f"{SLIDES_PATH} contains no 'data-beat-at' attributes. Visual beats from scenes.json must be injected into HTML elements.",
            )
        )

    # 3. Must contain platform override CSS
    has_platform_css = any(
        marker in html_content
        for marker in [
            "--platform-aspect",
            "9:16",
            "16:9",
            "4:5",
            "platform-override",
            "aspect-ratio",
        ]
    )
    if not has_platform_css:
        ISSUES.append(
            (
                "missing_platform_css",
                f"{SLIDES_PATH} missing platform override CSS. Must include aspect ratio variables for the target platform.",
            )
        )

    # 4. Check referenced image files exist
    img_refs = re.findall(
        r'(?:src|href)=["\']([^"\']+\.(?:png|jpg|jpeg|webp|svg|gif))["\']',
        html_content,
        re.IGNORECASE,
    )
    for img_ref in img_refs:
        img_path = Path(img_ref)
        if not img_path.is_absolute():
            img_path = Path(".") / img_ref
        if not img_path.exists():
            ISSUES.append(("image_missing", f"Referenced image not found: {img_ref}"))

    # 5. L3-design.md must exist with Mood and Style
    if not DESIGN_SPEC_PATH.exists():
        ISSUES.append(
            (
                "design_spec_missing",
                f"{DESIGN_SPEC_PATH} does not exist. Visual design spec is required for downstream TTS.",
            )
        )
    else:
        content = DESIGN_SPEC_PATH.read_text(encoding="utf-8")
        if "Mood" not in content and "mood" not in content.lower():
            ISSUES.append(
                ("design_spec_missing_mood", f"{DESIGN_SPEC_PATH} must specify Mood.")
            )
        if "Style" not in content and "style" not in content.lower():
            ISSUES.append(
                (
                    "design_spec_missing_style",
                    f"{DESIGN_SPEC_PATH} must specify Style selection.",
                )
            )


def main() -> int:
    check()
    if not ISSUES:
        print(
            "✅ visual-designer exit check passed. HTML slides are valid and complete."
        )
        return 0

    print("❌ visual-designer exit check failed:\n")
    for code, detail in ISSUES:
        print(f"  [{code}] {detail}")
    print()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
