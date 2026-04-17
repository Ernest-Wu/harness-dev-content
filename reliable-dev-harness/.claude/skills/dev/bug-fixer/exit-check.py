#!/usr/bin/env python3
"""
Exit Check: bug-fixer
"""

import re
import sys
from pathlib import Path

ISSUES = []


def check():
    # Optional - check that a bug fix write-up exists
    report = Path(".claude/state/LAST_BUGFIX.md")
    if report.exists():
        text = report.read_text(encoding="utf-8")
        if not re.search(r"hypothesis|evidence|root cause", text, re.IGNORECASE):
            ISSUES.append(("fix_report_weak", "Bug fix report lacks evidence or hypothesis."))


def main() -> int:
    check()
    if not ISSUES:
        print("✅ Bug fixer exit check passed.")
        return 0
    print("❌ Bug fixer exit check failed:\n")
    for code, detail in ISSUES:
        print(f"  [{code}] {detail}")
    print()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
