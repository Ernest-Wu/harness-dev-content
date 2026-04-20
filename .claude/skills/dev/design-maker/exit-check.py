#!/usr/bin/env python3
"""
Exit Check: design-maker
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from _utils.exit_check_base import add_issue, print_and_exit

DATA_PATH = Path(".claude/state/L5-design-data.yaml")
SPEC_PATH = Path(".claude/state/L2-spec.md")
BRIEF_PATH = Path(".claude/state/L3-design.md")


def check():
    if not DATA_PATH.exists():
        add_issue("file_missing", f"{DATA_PATH} does not exist.")
        return

    text = DATA_PATH.read_text(encoding="utf-8")

    # Must reference a source
    if not re.search(r"source:\s*(figma|pencil|json|yaml)", text, re.IGNORECASE):
        add_issue("source_missing", "No design source (figma/pencil/json/yaml) found.")

    # Must have at least one page
    pages_match = re.search(r"pages?:", text, re.IGNORECASE)
    if not pages_match:
        add_issue("pages_missing", "No pages list found. Design deliverable must name the screens/components it covers.")
    else:
        # Check each page has elements
        pages_section = re.split(r"pages?:", text, flags=re.IGNORECASE)[1] if pages_match else ""
        page_items = re.findall(r"^\s*-\s+\w+", pages_section, re.MULTILINE)
        if len(page_items) < 1:
            add_issue("pages_empty", "Pages list exists but contains no items.")

    # Check for error/loading/empty state coverage
    state_keywords = ["error", "loading", "empty", "success"]
    found_states = [kw for kw in state_keywords if kw.lower() in text.lower()]
    if len(found_states) < 2:
        add_issue(
            "states_incomplete",
            f"Design may only cover happy path. Found states: {found_states}. "
            "Each screen needs error, loading, and empty states.",
            level="warning",
        )

    # Check color token references (hex values indicate concrete design)
    hex_colors = re.findall(r"#[0-9a-fA-F]{3,8}", text)
    if len(hex_colors) < 2:
        add_issue(
            "colors_vague",
            "Design data has fewer than 2 hex color values. Design must reference exact tokens from L3-design.md.",
            level="warning",
        )

    # Check spacing values (exact numbers)
    spacing_values = re.findall(r"\b\d+\s*(px|rem|em|pt)\b", text, re.IGNORECASE)
    if len(spacing_values) < 3:
        add_issue(
            "spacing_vague",
            "Design data has fewer than 3 exact spacing values. Every spacing must be an exact number from the Design Brief.",
            level="warning",
        )

    # Verify spec alignment: check L2-spec exists
    if not SPEC_PATH.exists():
        add_issue(
            "spec_missing",
            "L2-spec.md not found. Cannot verify design-spec alignment.",
            level="info",
        )

    # Verify design brief exists
    if not BRIEF_PATH.exists():
        add_issue(
            "brief_missing",
            "L3-design.md not found. Design data should reference tokens from the design brief.",
            level="info",
        )


def main() -> int:
    check()
    print_and_exit("design-maker")


if __name__ == "__main__":
    raise SystemExit(main())
