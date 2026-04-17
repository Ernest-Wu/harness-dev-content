#!/usr/bin/env python3
"""
PM Content Validation Gate (CG5) — Exit Check
Validates that content performance is measured against KPIs after publishing.
Ensures metrics, decision, and learnings are documented.
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(".")
STATE_DIR = PROJECT_ROOT / ".claude" / "state"
L0_STRATEGY = STATE_DIR / "L0-strategy.md"
L5_VALIDATION = STATE_DIR / "L5-validation.md"
L6_DISTRIBUTION = STATE_DIR / "L6-distribution.md"

ISSUES = []


def check_l5_exists():
    if not L5_VALIDATION.exists():
        ISSUES.append(
            (
                "high",
                "file_missing",
                "L5-validation.md does not exist — create content validation report",
            )
        )
        return False
    return True


def check_required_sections():
    if not L5_VALIDATION.exists():
        return

    content = L5_VALIDATION.read_text(encoding="utf-8")

    required = {
        "## Checkpoint": "checkpoint_missing",
        "## KPI Performance": "kpi_missing",
        "## Decision": "decision_missing",
        "## Learnings": "learnings_missing",
    }

    for section, code in required.items():
        if section not in content:
            ISSUES.append(
                ("high", code, f"L5-validation.md missing required section: {section}")
            )


def check_decision_content():
    if not L5_VALIDATION.exists():
        return

    content = L5_VALIDATION.read_text(encoding="utf-8")

    if "## Decision" in content:
        section = content.split("## Decision")[1].split("##")[0]
        valid_decisions = ["ITERATE", "REFRESH", "RETIRE"]
        if not any(d in section for d in valid_decisions):
            ISSUES.append(
                (
                    "high",
                    "decision_invalid",
                    "Decision must be ITERATE, REFRESH, or RETIRE",
                )
            )


def check_kpi_has_status():
    if not L5_VALIDATION.exists():
        return

    content = L5_VALIDATION.read_text(encoding="utf-8")

    if "## KPI Performance" in content:
        section = content.split("## KPI Performance")[1].split("##")[0]
        has_status = any(marker in section for marker in ["✅", "⚠️", "❌"])
        if not has_status and len(section.strip()) > 10:
            ISSUES.append(
                (
                    "warning",
                    "kpi_no_status",
                    "KPI Performance section has no status indicators (✅/⚠️/❌)",
                )
            )


def check_kpi_alignment():
    if not L0_STRATEGY.exists() or not L5_VALIDATION.exists():
        return

    l0_content = L0_STRATEGY.read_text(encoding="utf-8")
    if "## KPI" not in l0_content:
        ISSUES.append(
            (
                "warning",
                "l0_no_kpi",
                "L0-strategy.md has no KPI section — CG0 may be incomplete",
            )
        )


def check_utm_tracking():
    if not L6_DISTRIBUTION.exists() or not L5_VALIDATION.exists():
        return

    content = L5_VALIDATION.read_text(encoding="utf-8")
    if "## Platform Breakdown" in content:
        section = (
            content.split("## Platform Breakdown")[1].split("##")[0]
            if "## Platform Breakdown" in content
            else ""
        )
        if "utm" not in section.lower() and "UTM" not in content:
            ISSUES.append(
                (
                    "info",
                    "no_utm_reference",
                    "Consider adding UTM-based attribution data to platform breakdown for CG4 traceability",
                )
            )


def main() -> int:
    check_l5_exists()
    check_required_sections()
    check_decision_content()
    check_kpi_has_status()
    check_kpi_alignment()
    check_utm_tracking()

    if not ISSUES:
        print("✅ PM Content Validation Gate (CG5) exit check passed.")
        return 0

    print("❌ PM Content Validation Gate (CG5) exit check FAILED:\n")
    for level, code, detail in ISSUES:
        if level == "high":
            icon = "🔴"
        elif level == "warning":
            icon = "🟡"
        else:
            icon = "ℹ️"
        print(f"  {icon} [{level.upper()}] {code}: {detail}")
    print()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
