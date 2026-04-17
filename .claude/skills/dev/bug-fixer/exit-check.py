#!/usr/bin/env python3
"""
Exit Check: bug-fixer (Hard Gate)

Deterministic gate verifying that bug fixes are properly documented
and follow the systematic debugging methodology.

Severity levels:
  - high:   Blocks progress. Must fix before proceeding.
  - warning: Does not block, but PM should review.
  - info:   Informational, for traceability.
"""

import re
import sys
from pathlib import Path

REPORT_PATH = Path(".claude/state/LAST_BUGFIX.md")

ISSUES = []


def check():
    # ── HARD GATE: LAST_BUGFIX.md must exist ──
    if not REPORT_PATH.exists():
        ISSUES.append(
            (
                "high",
                "fix_report_missing",
                f"{REPORT_PATH} does not exist. "
                "bug-fixer must document the fix before marking complete.",
            )
        )
        return

    text = REPORT_PATH.read_text(encoding="utf-8")

    # ── HARD GATE: Report must contain structured debugging evidence ──
    has_hypothesis = bool(re.search(r"hypothesis|假设", text, re.IGNORECASE))
    has_evidence = bool(
        re.search(r"evidence|证据|stack.?trace|日志|log", text, re.IGNORECASE)
    )
    has_root_cause = bool(re.search(r"root.?cause|根因|根本原因", text, re.IGNORECASE))

    evidence_count = sum([has_hypothesis, has_evidence, has_root_cause])
    if evidence_count == 0:
        ISSUES.append(
            (
                "high",
                "fix_report_weak",
                "Bug fix report lacks hypothesis, evidence, or root cause. "
                "Must include at least one structured debugging element.",
            )
        )
    elif evidence_count == 1:
        ISSUES.append(
            (
                "warning",
                "fix_report_partial",
                "Bug fix report has only one debugging element. "
                "Best practice: include hypothesis, evidence, AND root cause.",
            )
        )

    # ── HARD GATE: Minimum report length ──
    if len(text.strip()) < 100:
        ISSUES.append(
            (
                "high",
                "fix_report_too_short",
                f"Bug fix report is only {len(text.strip())} chars. "
                "A meaningful fix report needs at least 100 chars.",
            )
        )

    # ── WARNING: Check for escalation pattern (3+ attempts) ──
    attempt_markers = re.findall(
        r"(?:attempt|try|attempt|尝试|第\s*\d+\s*次)", text, re.IGNORECASE
    )
    if len(attempt_markers) >= 3:
        ISSUES.append(
            (
                "warning",
                "escalation_needed",
                f"Bug fix has {len(attempt_markers)}+ attempt markers. "
                "Consider architectural review per SKILL.md Pitfall 3.",
            )
        )

    # ── INFO: Check for test verification ──
    has_test_verification = bool(
        re.search(
            r"test.*pass|regression|verified|验证|测试通过|回归", text, re.IGNORECASE
        )
    )
    if not has_test_verification:
        ISSUES.append(
            (
                "info",
                "no_test_verification",
                "Bug fix report does not mention test verification. "
                "SKILL.md Stage 4 requires running failing test + full test suite.",
            )
        )

    # ── INFO: Check for business impact ──
    has_impact = bool(
        re.search(
            r"business.?impact|user.?impact|priority|业务影响|用户影响|优先级",
            text,
            re.IGNORECASE,
        )
    )
    if not has_impact:
        ISSUES.append(
            (
                "info",
                "no_business_impact",
                "Bug fix report does not mention business/user impact. "
                "PM Gate: bug priority should map to business impact (MoSCoW).",
            )
        )


def main() -> int:
    check()

    high_issues = [i for i in ISSUES if i[0] == "high"]
    warning_issues = [i for i in ISSUES if i[0] == "warning"]
    info_issues = [i for i in ISSUES if i[0] == "info"]

    print("═══ Bug Fixer Exit Check ═══")
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
        print("❌ Bug fixer exit check FAILED — resolve HIGH issues before proceeding.")
        return 1

    if warning_issues:
        print(
            "⚠️  Bug fixer exit check PASSED with warnings — "
            "PM should review before proceeding."
        )
    else:
        print("✅ Bug fixer exit check passed. Fix is documented and verified.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
