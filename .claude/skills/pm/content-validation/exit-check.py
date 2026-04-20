#!/usr/bin/env python3
"""
PM Content Validation Gate (CG5) — Exit Check
Validates that content performance is measured against KPIs after publishing.
Ensures metrics, decision, and learnings are documented.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from _utils.exit_check_base import add_issue, print_and_exit

PROJECT_ROOT = Path(".")
STATE_DIR = PROJECT_ROOT / ".claude" / "state"
L0_STRATEGY = STATE_DIR / "L0-strategy.md"
L5_VALIDATION = STATE_DIR / "L5-content-validation.md"
L6_DISTRIBUTION = STATE_DIR / "L6-distribution.md"


def check_l5_exists():
    if not L5_VALIDATION.exists():
        add_issue(
            "file_missing",
            "L5-content-validation.md does not exist — create content validation report",
            level="high",
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
            add_issue(
                code,
                f"L5-content-validation.md missing required section: {section}",
                level="high",
            )


def check_decision_content():
    if not L5_VALIDATION.exists():
        return

    content = L5_VALIDATION.read_text(encoding="utf-8")

    if "## Decision" in content:
        section = content.split("## Decision")[1].split("##")[0]
        valid_decisions = ["ITERATE", "REFRESH", "RETIRE"]
        if not any(d in section for d in valid_decisions):
            add_issue(
                "decision_invalid",
                "Decision must be ITERATE, REFRESH, or RETIRE",
                level="high",
            )


def check_kpi_has_status():
    if not L5_VALIDATION.exists():
        return

    content = L5_VALIDATION.read_text(encoding="utf-8")

    if "## KPI Performance" in content:
        section = content.split("## KPI Performance")[1].split("##")[0]
        has_status = any(marker in section for marker in ["✅", "⚠️", "❌"])
        if not has_status and len(section.strip()) > 10:
            add_issue(
                "kpi_no_status",
                "KPI Performance section has no status indicators (✅/⚠️/❌)",
                level="warning",
            )


def check_kpi_alignment():
    if not L0_STRATEGY.exists() or not L5_VALIDATION.exists():
        return

    l0_content = L0_STRATEGY.read_text(encoding="utf-8")
    if "## KPI" not in l0_content:
        add_issue(
            "l0_no_kpi",
            "L0-strategy.md has no KPI section — CG0 may be incomplete",
            level="warning",
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
            add_issue(
                "no_utm_reference",
                "Consider adding UTM-based attribution data to platform breakdown for CG4 traceability",
                level="info",
            )


def main() -> int:
    check_l5_exists()
    check_required_sections()
    check_decision_content()
    check_kpi_has_status()
    check_kpi_alignment()
    check_utm_tracking()

    print_and_exit("PM Content Validation Gate")


if __name__ == "__main__":
    raise SystemExit(main())
