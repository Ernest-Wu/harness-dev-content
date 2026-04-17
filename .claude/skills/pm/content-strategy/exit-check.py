#!/usr/bin/env python3
"""
PM Content Strategy Gate (CG0) — Exit Check
Validates that content strategy is defined before production begins.
Ensures target audience, business goal, and KPI are specified.
"""

import re
import sys
from pathlib import Path

# Use relative path for PROJECT_ROOT
PROJECT_ROOT = Path(".")

STATE_DIR = PROJECT_ROOT / ".claude" / "state"
L0_STRATEGY = STATE_DIR / "L0-strategy.md"

ISSUES = []


def check_l0_exists():
    """L0-strategy.md must exist for CG0."""
    if not L0_STRATEGY.exists():
        ISSUES.append(
            (
                "high",
                "file_missing",
                "L0-strategy.md does not exist — create content strategy before production",
            )
        )
        return False
    return True


def check_required_sections():
    """L0-strategy.md must contain required strategic sections."""
    if not L0_STRATEGY.exists():
        return

    content = L0_STRATEGY.read_text(encoding="utf-8")

    required_sections = {
        "## Target Audience": "target_audience_missing",
        "## Business Goal": "business_goal_missing",
        "## KPI": "kpi_missing",
    }

    for section, code in required_sections.items():
        if section not in content:
            ISSUES.append(
                ("high", code, f"L0-strategy.md missing required section: {section}")
            )


def check_target_audience_specificity():
    """Target audience must be specific (not just 'everyone' or 'users')."""
    if not L0_STRATEGY.exists():
        return

    content = L0_STRATEGY.read_text(encoding="utf-8")

    # Extract Target Audience section
    if "## Target Audience" in content:
        section = content.split("## Target Audience")[1].split("##")[0]

        # Check for vague audience references
        vague_patterns = [
            r"anyone",
            r"everyone",
            r"all users",
            r"general audience",
            r"any person",
        ]
        for pattern in vague_patterns:
            if re.search(pattern, section, re.IGNORECASE):
                ISSUES.append(
                    (
                        "warning",
                        "vague_audience",
                        f"Target audience is too vague — define specific segment (age, interests, pain points)",
                    )
                )
                break


def check_kpi_quantified():
    """KPI must include at least one quantified metric with target number."""
    if not L0_STRATEGY.exists():
        return

    content = L0_STRATEGY.read_text(encoding="utf-8")

    if "## KPI" in content:
        kpi_section = content.split("## KPI")[1].split("##")[0]

        # Should contain at least one number (%, views, rate, etc.)
        has_number = bool(re.search(r"\d+", kpi_section))
        if not has_number:
            ISSUES.append(
                (
                    "high",
                    "kpi_not_quantified",
                    "KPI section must include at least one quantified metric with a target number",
                )
            )


def check_differentiation():
    """Differentiation strategy should be present."""
    if not L0_STRATEGY.exists():
        return

    content = L0_STRATEGY.read_text(encoding="utf-8")

    if "## Differentiation Strategy" not in content:
        if "## Differentiation" not in content:
            ISSUES.append(
                (
                    "warning",
                    "diff_missing",
                    "L0-strategy.md missing Differentiation Strategy — how does this content stand out?",
                )
            )


def check_compliance():
    """Compliance requirements section should exist."""
    if not L0_STRATEGY.exists():
        return

    content = L0_STRATEGY.read_text(encoding="utf-8")

    if "## Compliance" not in content:
        ISSUES.append(
            (
                "warning",
                "compliance_missing",
                "L0-strategy.md missing Compliance Requirements section — add even if 'none'",
            )
        )


def main() -> int:
    check_l0_exists()
    check_required_sections()
    check_target_audience_specificity()
    check_kpi_quantified()
    check_differentiation()
    check_compliance()

    if not ISSUES:
        print("✅ PM Content Strategy Gate (CG0) exit check passed.")
        return 0

    print("❌ PM Content Strategy Gate (CG0) exit check FAILED:\n")
    for level, code, detail in ISSUES:
        icon = "🔴" if level == "high" else "🟡"
        print(f"  {icon} [{level.upper()}] {code}: {detail}")
    print()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
