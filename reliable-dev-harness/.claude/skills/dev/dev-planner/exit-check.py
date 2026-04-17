#!/usr/bin/env python3
"""
Exit Check: dev-planner
"""

import re
import sys
from pathlib import Path

PLAN_PATH = Path(".claude/state/L4-plan.md")
ISSUES = []


def check():
    if not PLAN_PATH.exists():
        ISSUES.append(("file_missing", f"{PLAN_PATH} does not exist."))
        return

    text = PLAN_PATH.read_text(encoding="utf-8")

    # Must have Phase sections
    phases = re.findall(r"^##\s+.*Phase.*$", text, re.MULTILINE | re.IGNORECASE)
    if len(phases) < 2:
        ISSUES.append(("phases_too_few", "DEV-PLAN should have at least 2 Phases."))

    # Must mention deliverables or dependencies
    if not re.search(r"deliverable|dependency|task", text, re.IGNORECASE):
        ISSUES.append(("plan_too_vague", "No deliverables, dependencies, or tasks found."))


def main() -> int:
    check()
    if not ISSUES:
        print("✅ DEV-PLAN passes exit check.")
        return 0
    print("❌ DEV-PLAN exit check failed:\n")
    for code, detail in ISSUES:
        print(f"  [{code}] {detail}")
    print()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
