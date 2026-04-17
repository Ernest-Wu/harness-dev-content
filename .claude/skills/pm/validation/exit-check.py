#!/usr/bin/env python3
"""
PM Validation Gate (G5) — Exit Check
Validates that product outcomes are measured against spec metrics.
Runs at 7-day and 30-day checkpoints after release.
"""

import sys
from pathlib import Path

# Use relative path for PROJECT_ROOT
PROJECT_ROOT = Path(".")

STATE_DIR = PROJECT_ROOT / ".claude" / "state"
L2_SPEC = STATE_DIR / "L2-spec.md"
L4_PLAN = STATE_DIR / "L4-plan.md"
L5_VALIDATION = STATE_DIR / "L5-validation.md"

ISSUES = []


def check_l5_exists():
    """L5-validation.md must exist for G5."""
    if not L5_VALIDATION.exists():
        ISSUES.append(
            (
                "high",
                "file_missing",
                "L5-validation.md does not exist — create it before G5 validation",
            )
        )
        return False
    return True


def check_validation_report_structure():
    """L5-validation.md must contain required sections."""
    if not L5_VALIDATION.exists():
        return  # Already caught by check_l5_exists

    content = L5_VALIDATION.read_text(encoding="utf-8")

    required_sections = [
        "## Checkpoint",
        "## Metrics",
        "## Decision",
        "## Learnings",
    ]

    for section in required_sections:
        if section not in content:
            ISSUES.append(
                (
                    "high",
                    "section_missing",
                    f"L5-validation.md missing required section: {section}",
                )
            )


def check_metrics_have_status():
    """Each metric row must have a status indicator (✅/⚠️/❌)."""
    if not L5_VALIDATION.exists():
        return

    content = L5_VALIDATION.read_text(encoding="utf-8")

    # Check that Metrics section exists and has status indicators
    if "## Metrics" in content:
        metrics_section = (
            content.split("## Metrics")[1].split("##")[0]
            if "## Metrics" in content
            else ""
        )
        # Should have at least one status indicator
        has_status = any(marker in metrics_section for marker in ["✅", "⚠️", "❌"])
        if not has_status and len(metrics_section.strip()) > 10:
            ISSUES.append(
                (
                    "warning",
                    "metrics_no_status",
                    "Metrics section has no status indicators (✅/⚠️/❌)",
                )
            )


def check_decision_made():
    """A GO/PIVOT/KILL decision must be documented."""
    if not L5_VALIDATION.exists():
        return

    content = L5_VALIDATION.read_text(encoding="utf-8")

    if "## Decision" in content:
        decision_section = (
            content.split("## Decision")[1].split("##")[0]
            if "## Decision" in content
            else ""
        )
        has_decision = any(kw in decision_section for kw in ["GO", "PIVOT", "KILL"])
        if not has_decision:
            ISSUES.append(
                (
                    "high",
                    "decision_missing",
                    "Decision section must contain GO, PIVOT, or KILL",
                )
            )


def check_spec_alignment():
    """Metrics in L5 should reference metrics defined in L2-spec."""
    if not L2_SPEC.exists() or not L5_VALIDATION.exists():
        return

    l2_content = L2_SPEC.read_text(encoding="utf-8")
    l5_content = L5_VALIDATION.read_text(encoding="utf-8")

    # L2-spec should have a Success Metrics section
    if "## Success Metrics" not in l2_content:
        ISSUES.append(
            (
                "warning",
                "l2_no_metrics",
                "L2-spec has no Success Metrics section — G0 may be incomplete",
            )
        )

    # L5 should reference L2 metrics or have its own metrics table
    if "## Metrics" in l5_content:
        metrics_section = l5_content.split("## Metrics")[1].split("##")[0]
        # Should have a table with columns
        if "|" not in metrics_section:
            ISSUES.append(
                (
                    "warning",
                    "metrics_format",
                    "Metrics section should use a table format with columns for baseline, current, target, status",
                )
            )


def check_pivot_has_plan():
    """If decision is PIVOT, must have a PIVOT Plan section."""
    if not L5_VALIDATION.exists():
        return

    content = L5_VALIDATION.read_text(encoding="utf-8")

    if "PIVOT" in content and "## Decision" in content:
        decision_section = (
            content.split("## Decision")[1].split("##")[0]
            if "## Decision" in content
            else ""
        )
        if "PIVOT" in decision_section and "## PIVOT Plan" not in content:
            ISSUES.append(
                (
                    "high",
                    "pivot_no_plan",
                    "Decision is PIVOT but no PIVOT Plan section found",
                )
            )


def main() -> int:
    check_l5_exists()
    check_validation_report_structure()
    check_metrics_have_status()
    check_decision_made()
    check_spec_alignment()
    check_pivot_has_plan()

    if not ISSUES:
        print("✅ PM Validation Gate (G5) exit check passed.")
        return 0

    print("❌ PM Validation Gate (G5) exit check FAILED:\n")
    for level, code, detail in ISSUES:
        icon = "🔴" if level == "high" else "🟡"
        print(f"  {icon} [{level.upper()}] {code}: {detail}")
    print()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
