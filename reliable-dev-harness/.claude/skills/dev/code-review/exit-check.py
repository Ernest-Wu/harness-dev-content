#!/usr/bin/env python3
"""
Exit Check: code-review
Deterministic gate to prevent LLM reviewer leniency bias.
"""

import re
import sys
from pathlib import Path

REVIEW_PATH = Path(".claude/state/LAST_REVIEW.md")
ISSUES = []


def check():
    if not REVIEW_PATH.exists():
        ISSUES.append(("review_file_missing", ".claude/state/LAST_REVIEW.md does not exist."))
        return

    text = REVIEW_PATH.read_text(encoding="utf-8")

    # 1. Must contain Stage 1 and Stage 2 sections
    if not re.search(r"Stage\s+1", text, re.IGNORECASE):
        ISSUES.append(("stage1_missing", "Review does not contain a Stage 1 section."))

    if not re.search(r"Stage\s+2", text, re.IGNORECASE):
        ISSUES.append(("stage2_missing", "Review does not contain a Stage 2 section."))

    # 2. Must have at least one actionable issue or suggestion
    action_words = ["should", "needs to", "missing", "incorrect", "rename", "refactor", "fix", "add", "remove"]
    if not any(w in text.lower() for w in action_words):
        ISSUES.append((
            "review_too_lenient",
            "Review contains no actionable issues or suggestions. "
            "Leniency bias detected. Every review must find at least one concrete problem or improvement."
        ))

    # 3. If Stage 1 has HIGH, must NOT proceed to Stage 2 approval
    stage1_high = re.search(
        r"Stage\s+1.*?HIGH", text, re.IGNORECASE | re.DOTALL
    )
    stage2_approved = re.search(
        r"Stage\s+2.*?(passed|approve)", text, re.IGNORECASE | re.DOTALL
    )
    if stage1_high and stage2_approved:
        ISSUES.append((
            "high_issue_ignored",
            "Stage 1 has HIGH issues but Stage 2 was approved. This is a protocol violation."
        ))

    # 4. Length check - extremely short reviews are suspect
    if len(text.strip()) < 200:
        ISSUES.append((
            "review_too_short",
            f"Review is only {len(text.strip())} chars. A meaningful review needs at least 200 chars."
        ))


def main() -> int:
    check()
    if not ISSUES:
        print("✅ code-review exit check passed. Review meets minimum rigor.")
        return 0

    print("❌ code-review exit check failed:\n")
    for code, detail in ISSUES:
        print(f"  [{code}] {detail}")
    print()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
