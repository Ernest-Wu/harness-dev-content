#!/usr/bin/env python3
"""
Exit Check: design-maker
"""

import re
import sys
from pathlib import Path

DATA_PATH = Path(".claude/state/L5-design-data.yaml")
ISSUES = []


def check():
    if not DATA_PATH.exists():
        ISSUES.append(("file_missing", f"{DATA_PATH} does not exist."))
        return

    text = DATA_PATH.read_text(encoding="utf-8")

    # Must reference a source and at least one page
    if not re.search(r"source:\s*(figma|pencil|json|yaml)", text, re.IGNORECASE):
        ISSUES.append(("source_missing", "No design source (figma/pencil/json/yaml) found."))

    if not re.search(r"pages?:", text, re.IGNORECASE):
        ISSUES.append(("pages_missing", "No pages list found. Design deliverable must name the screens/components it covers."))


def main() -> int:
    check()
    if not ISSUES:
        print("✅ Design maker exit check passed.")
        return 0
    print("❌ Design maker exit check failed:\n")
    for code, detail in ISSUES:
        print(f"  [{code}] {detail}")
    print()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
