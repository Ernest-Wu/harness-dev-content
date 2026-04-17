#!/usr/bin/env python3
"""
Exit Check: frontend-slides (Content Domain)
Deterministic gate verifying HTML slides output quality.
"""

import re
import sys
from pathlib import Path

SLIDES_PATH = Path("slides-preview.html")
DESIGN_SPEC_PATH = Path(".claude/state/L3-design.md")

ISSUES = []


def check():
    # ── HARD GATE: slides-preview.html must exist and be valid HTML ──
    if not SLIDES_PATH.exists():
        ISSUES.append(
            (
                "high",
                "file_missing",
                f"{SLIDES_PATH} does not exist. frontend-slides must produce this file.",
            )
        )
        return

    html_content = SLIDES_PATH.read_text(encoding="utf-8")

    if not (
        html_content.strip().startswith("<")
        or "<html" in html_content.lower()[:500]
        or "<!doctype" in html_content.lower()[:500]
    ):
        ISSUES.append(
            (
                "high",
                "invalid_html",
                f"{SLIDES_PATH} does not appear to be valid HTML.",
            )
        )

    # ── HARD GATE: Must contain slide structure ──
    has_sections = bool(re.search(r"<section[^>]*class", html_content, re.IGNORECASE))
    has_divs = bool(re.search(r"<div[^>]*class.*slide", html_content, re.IGNORECASE))
    if not has_sections and not has_divs:
        ISSUES.append(
            (
                "high",
                "no_slide_structure",
                f"{SLIDES_PATH} contains no slide structure. "
                "Must have <section> or <div> elements with slide classes.",
            )
        )

    # ── HARD GATE: Must contain CSS styling ──
    has_style_tag = "<style" in html_content.lower()
    has_css_vars = "--primary" in html_content or "--bg" in html_content
    has_inline_style = "style=" in html_content.lower()
    if not has_style_tag and not has_css_vars and not has_inline_style:
        ISSUES.append(
            (
                "high",
                "no_styling",
                f"{SLIDES_PATH} contains no CSS styling. "
                "Slides must have visual design applied.",
            )
        )

    # ── WARNING: Check referenced images ──
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
            ISSUES.append(
                ("warning", "image_missing", f"Referenced image not found: {img_ref}")
            )

    # ── HARD GATE: L3-design.md must exist with Mood and Style ──
    if not DESIGN_SPEC_PATH.exists():
        ISSUES.append(
            (
                "high",
                "design_spec_missing",
                f"{DESIGN_SPEC_PATH} does not exist. "
                "Mood and Style selection must be recorded.",
            )
        )
    else:
        content = DESIGN_SPEC_PATH.read_text(encoding="utf-8")
        if "Mood" not in content and "mood" not in content.lower():
            ISSUES.append(
                (
                    "high",
                    "design_spec_missing_mood",
                    f"{DESIGN_SPEC_PATH} must specify Mood selection.",
                )
            )
        if "Style" not in content and "style" not in content.lower():
            ISSUES.append(
                (
                    "high",
                    "design_spec_missing_style",
                    f"{DESIGN_SPEC_PATH} must specify Style selection.",
                )
            )


def main() -> int:
    check()

    high_issues = [i for i in ISSUES if i[0] == "high"]
    warning_issues = [i for i in ISSUES if i[0] == "warning"]
    info_issues = [i for i in ISSUES if i[0] == "info"]

    print("═══ frontend-slides Exit Check ═══")
    print()
    for level, code, detail in info_issues:
        print(f"  ℹ️  [{code}] {detail}")
    print()
    for level, code, detail in warning_issues:
        print(f"  ⚠️  [{code}] {detail}")
    print()
    for level, code, detail in high_issues:
        print(f"  ❌ [{code}] {detail}")

    print()
    print(
        f"  Total: {len(high_issues)} high, "
        f"{len(warning_issues)} warning, {len(info_issues)} info"
    )
    print()

    if high_issues:
        print(
            "❌ frontend-slides exit check FAILED — "
            "resolve HIGH issues before proceeding."
        )
        return 1

    if warning_issues:
        print(
            "⚠️  frontend-slides exit check PASSED with warnings — "
            "review before proceeding."
        )
    else:
        print("✅ frontend-slides exit check passed. HTML slides are valid and styled.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
