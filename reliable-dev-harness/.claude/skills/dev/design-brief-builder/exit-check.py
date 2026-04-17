#!/usr/bin/env python3
"""
Exit Check: design-brief-builder
"""

import re
import sys
from pathlib import Path

DESIGN_PATH = Path(".claude/state/L3-design.md")
ISSUES = []


def check():
    if not DESIGN_PATH.exists():
        ISSUES.append(("file_missing", f"{DESIGN_PATH} does not exist."))
        return

    text = DESIGN_PATH.read_text(encoding="utf-8")

    # Must contain at least one hex color
    if not re.search(r"#[0-9A-Fa-f]{3,6}", text):
        ISSUES.append(("color_missing", "No hex color values found. Design Brief must specify exact colors."))

    # Must mention interaction or motion
    if not re.search(r"interaction|motion|animation|transition", text, re.IGNORECASE):
        ISSUES.append(("interaction_missing", "No interaction or motion guidelines found."))


def main() -> int:
    check()
    if not ISSUES:
        print("✅ Design Brief passes exit check.")
        return 0
    print("❌ Design Brief exit check failed:\n")
    for code, detail in ISSUES:
        print(f"  [{code}] {detail}")
    print()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
