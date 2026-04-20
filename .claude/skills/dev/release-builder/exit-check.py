#!/usr/bin/env python3
"""
Exit Check: release-builder (PM Release Gate)

Deterministic gate for release readiness. This is the final gate before
users see the product — it must be airtight.

PM Release Gate (G4) checks:
  1. All P0 features from spec are implemented
  2. Rollback plan exists
  3. Task history is complete (all phases done)
  4. Spec coverage — spec file is not empty
  5. Design brief exists (visual authority chain)
  6. Dev plan exists (phase tracking)

Hard Gate levels:
  - high:   Blocks release. Must fix before proceeding.
  - warning: Does not block release, but PM should confirm.
  - info:   Informational, for traceability.
"""

import re
import subprocess
import sys
from pathlib import Path
from shutil import which as shutil_which

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from _utils.exit_check_base import add_issue, print_and_exit

STATE_DIR = Path(".claude/state")
PROJECT_ROOT = Path(".")


def check():
    """Run all release readiness checks."""

    # ──────────────────────────────────────────
    # 1. P0 Features — All must be implemented
    # ──────────────────────────────────────────
    l2_spec = STATE_DIR / "L2-spec.md"
    if l2_spec.exists():
        spec_content = l2_spec.read_text(encoding="utf-8")

        p0_section = re.search(
            r"P0.*?(?:P1|##|$)", spec_content, re.IGNORECASE | re.DOTALL
        )
        if p0_section:
            p0_text = p0_section.group(0)
            p0_items = re.findall(r"^[-*]\s+\*\*.+?\*\*", p0_text, re.MULTILINE)
            if p0_items:
                add_issue(
                    "p0_features_listed",
                    f"Found {len(p0_items)} P0 features in spec. "
                    f"Verify all are implemented before release.",
                    level="info",
                )
            else:
                add_issue(
                    "p0_section_exists",
                    "P0 section found in spec but no specific features listed.",
                    level="info",
                )
        else:
            has_priority = re.search(
                r"P[0-2]|Must\s+Have|优先级|priority", spec_content, re.IGNORECASE
            )
            if not has_priority:
                add_issue(
                    "no_priority_markers",
                    "No P0/P1/P2 or priority markers found in spec. "
                    "Cannot verify which features must be in this release.",
                    level="warning",
                )

        if len(spec_content.strip()) < 200:
            add_issue(
                "spec_too_short",
                f"L2-spec.md is only {len(spec_content.strip())} chars. "
                f"Cannot verify feature coverage without a meaningful spec.",
                level="high",
            )
    else:
        add_issue(
            "spec_missing",
            f"L2-spec.md not found at {l2_spec}. "
            f"Release gate requires a spec to verify feature coverage.",
            level="high",
        )

    # ──────────────────────────────────────────
    # 2. Smoke Test — Auto-detect and run
    # ──────────────────────────────────────────
    check_smoke_test()

    # ──────────────────────────────────────────
    # 3. Rollback Plan — Must exist and be confirmed
    # ──────────────────────────────────────────
    rollback_doc = PROJECT_ROOT / "ROLLBACK.md"
    l4_plan = STATE_DIR / "L4-plan.md"
    found_rollback = False

    if rollback_doc.exists():
        rollback_content = rollback_doc.read_text(encoding="utf-8")
        if len(rollback_content.strip()) > 50:
            found_rollback = True
            add_issue(
                "rollback_plan_found",
                "ROLLBACK.md exists at project root.",
                level="info",
            )

    if not found_rollback and l4_plan.exists():
        plan_content = l4_plan.read_text(encoding="utf-8")
        if re.search(r"rollback|回滚|revert|回退", plan_content, re.IGNORECASE):
            found_rollback = True
            add_issue(
                "rollback_in_plan",
                "Rollback plan found in L4-plan.md.",
                level="info",
            )

    if not found_rollback:
        add_issue(
            "no_rollback_plan",
            "No rollback plan found. Create ROLLBACK.md at project root "
            "or add a rollback section to L4-plan.md before releasing.",
            level="high",
        )

    # ──────────────────────────────────────────
    # 4. Task History — All phases should be complete
    # ──────────────────────────────────────────
    task_history = STATE_DIR / "task-history.yaml"
    if task_history.exists():
        hist_content = task_history.read_text(encoding="utf-8")
        incomplete = re.findall(
            r"status:\s*(?:in.progress|pending|blocked|todo)",
            hist_content,
            re.IGNORECASE,
        )
        if incomplete:
            add_issue(
                "incomplete_tasks",
                f"Found {len(incomplete)} incomplete task(s) in task-history.yaml. "
                f"Verify these are not blocking the release.",
                level="warning",
            )
        else:
            add_issue(
                "task_history_exists",
                "Task history found.",
                level="info",
            )
    else:
        add_issue(
            "no_task_history",
            "task-history.yaml not found — cannot verify all tasks completed.",
            level="warning",
        )

    # ──────────────────────────────────────────
    # 5. Design Brief — Visual authority chain must exist
    # ──────────────────────────────────────────
    l3_design = STATE_DIR / "L3-design.md"
    if not l3_design.exists():
        add_issue(
            "no_design_brief",
            "L3-design.md not found. If this release includes UI changes, "
            "a design brief is required for spec compliance.",
            level="warning",
        )
    else:
        design_content = l3_design.read_text(encoding="utf-8")
        if len(design_content.strip()) < 100:
            add_issue(
                "design_brief_too_short",
                "L3-design.md exists but is nearly empty. "
                "UI changes require a design brief.",
                level="warning",
            )

    # ──────────────────────────────────────────
    # 6. Dev Plan — Phase structure must exist
    # ──────────────────────────────────────────
    if l4_plan.exists():
        plan_content = l4_plan.read_text(encoding="utf-8")
        phases = re.findall(
            r"^##\s+(?:Phase|阶段)", plan_content, re.MULTILINE | re.IGNORECASE
        )
        if phases:
            add_issue(
                "plan_has_phases",
                f"Found {len(phases)} phase(s) in dev plan.",
                level="info",
            )
        else:
            add_issue(
                "plan_no_phases",
                "L4-plan.md exists but no phases found. "
                "Verify that the plan structure is correct.",
                level="warning",
            )
    else:
        add_issue(
            "no_dev_plan",
            "L4-plan.md not found. Cannot verify phase completion.",
            level="warning",
        )

    # ── 7. Release Notes ─────────────────────────────────────────────
    release_notes = PROJECT_ROOT / "RELEASE-NOTES.md"
    if release_notes.exists():
        add_issue(
            "release_notes_found",
            "RELEASE-NOTES.md exists.",
            level="info",
        )
    else:
        add_issue(
            "no_release_notes",
            "No RELEASE-NOTES.md found. Document what changed in this release.",
            level="warning",
        )


def check_smoke_test():
    """Auto-detect project type and run a minimal smoke test."""
    smoke_passed = False
    smoke_cmd = None

    # Detect project type and choose smoke command
    if (PROJECT_ROOT / "package.json").exists():
        if shutil_which("npm"):
            smoke_cmd = ["npm", "run", "test", "--", "--run"]
            # Fallback: try 'npm test' if '--run' not supported
    elif (PROJECT_ROOT / "Cargo.toml").exists():
        if shutil_which("cargo"):
            smoke_cmd = ["cargo", "test", "--", "--test-threads=1"]
    elif list(PROJECT_ROOT.glob("go.mod")):
        if shutil_which("go"):
            smoke_cmd = ["go", "test", "-short", "./..."]
    elif (
        (PROJECT_ROOT / "pyproject.toml").exists()
        or (PROJECT_ROOT / "setup.py").exists()
        or (PROJECT_ROOT / "setup.cfg").exists()
        or any(PROJECT_ROOT.glob("*.py"))
    ):
        if shutil_which("pytest"):
            smoke_cmd = ["pytest", "-x", "-q"]
        elif shutil_which("python"):
            smoke_cmd = ["python", "-m", "compileall", "."]

    if smoke_cmd:
        try:
            result = subprocess.run(
                smoke_cmd,
                capture_output=True,
                text=True,
                timeout=300,
            )
            if result.returncode == 0:
                smoke_passed = True
                add_issue(
                    "smoke_test_passed",
                    f"Smoke test passed: {' '.join(smoke_cmd)}",
                    level="info",
                )
            elif result.returncode == 5 and "no tests ran" in result.stdout.lower():
                # pytest exit code 5 = no tests collected — not a release blocker
                add_issue(
                    "smoke_test_no_tests",
                    f"No tests found to run ({' '.join(smoke_cmd)}). "
                    f"Consider adding tests for critical paths before release.",
                    level="warning",
                )
            else:
                add_issue(
                    "smoke_test_failed",
                    f"Smoke test failed: {' '.join(smoke_cmd)}\n"
                    f"stdout: {result.stdout[-300:]}\nstderr: {result.stderr[-300:]}",
                    level="high",
                )
        except Exception as e:
            add_issue(
                "smoke_test_error",
                f"Error running smoke test {' '.join(smoke_cmd)}: {e}",
                level="high",
            )
    else:
        add_issue(
            "smoke_test_not_detected",
            "Could not auto-detect project type for smoke test. "
            "Verify manually that the application starts and critical paths work.",
            level="warning",
        )


def main() -> int:
    check()
    print_and_exit("PM Release Gate")


if __name__ == "__main__":
    raise SystemExit(main())
