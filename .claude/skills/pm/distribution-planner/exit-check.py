#!/usr/bin/env python3
"""
PM Distribution Gate (CG4) — Exit Check
Validates that content has a complete distribution plan before publishing.
Ensures metadata, UTM tracking, and compliance are defined.
"""

import re
import sys
from pathlib import Path

PROJECT_ROOT = Path(".")
STATE_DIR = PROJECT_ROOT / ".claude" / "state"
L6_DISTRIBUTION = STATE_DIR / "L6-distribution.md"

ISSUES = []


def check_l6_exists():
    if not L6_DISTRIBUTION.exists():
        ISSUES.append(
            (
                "high",
                "file_missing",
                "L6-distribution.md does not exist — create distribution plan before publishing",
            )
        )
        return False
    return True


def check_required_sections():
    if not L6_DISTRIBUTION.exists():
        return

    content = L6_DISTRIBUTION.read_text(encoding="utf-8")

    required = {
        "## Platform Strategy": "platform_strategy_missing",
        "## Compliance Checklist": "compliance_missing",
    }

    for section, code in required.items():
        if section not in content:
            ISSUES.append(
                (
                    "high",
                    code,
                    f"L6-distribution.md missing required section: {section}",
                )
            )


def check_platform_count():
    if not L6_DISTRIBUTION.exists():
        return

    content = L6_DISTRIBUTION.read_text(encoding="utf-8")

    platform_count = content.count("### ")
    if platform_count < 1:
        ISSUES.append(
            (
                "high",
                "no_platforms",
                "L6-distribution.md must list at least one platform",
            )
        )


def check_utm_tracking():
    if not L6_DISTRIBUTION.exists():
        return

    content = L6_DISTRIBUTION.read_text(encoding="utf-8")

    if "## UTM Tracking" not in content:
        ISSUES.append(
            (
                "warning",
                "utm_missing",
                "L6-distribution.md missing UTM Tracking section — CG5 validation will be impossible without tracking",
            )
        )


def check_compliance_items():
    if not L6_DISTRIBUTION.exists():
        return

    content = L6_DISTRIBUTION.read_text(encoding="utf-8")

    if "## Compliance Checklist" in content:
        section = content.split("## Compliance Checklist")[1].split("##")[0]
        unchecked = section.count("[ ]")
        checked = section.count("[x]")
        if unchecked == 0 and checked == 0:
            ISSUES.append(
                (
                    "warning",
                    "compliance_empty",
                    "Compliance Checklist has no items — add at least copyright and ad disclosure checks",
                )
            )


def main() -> int:
    check_l6_exists()
    check_required_sections()
    check_platform_count()
    check_utm_tracking()
    check_compliance_items()

    if not ISSUES:
        print("✅ PM Distribution Gate (CG4) exit check passed.")
        return 0

    print("❌ PM Distribution Gate (CG4) exit check FAILED:\n")
    for level, code, detail in ISSUES:
        icon = "🔴" if level == "high" else "🟡"
        print(f"  {icon} [{level.upper()}] {code}: {detail}")
    print()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
