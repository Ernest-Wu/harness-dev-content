#!/usr/bin/env python3
"""
Harness Health Check
Verify that the Harness infrastructure itself is intact.
"""

import sys
from pathlib import Path

ROOT = Path(__file__).parent
ISSUES = []


def check_skills():
    skills_dir = ROOT / "skills"
    expected = [
        "product-spec-builder",
        "design-brief-builder",
        "design-maker",
        "dev-planner",
        "dev-builder",
        "bug-fixer",
        "code-review",
        "release-builder",
    ]
    for name in expected:
        skill_md = skills_dir / name / "SKILL.md"
        exit_check = skills_dir / name / "exit-check.py"
        if not skill_md.exists():
            ISSUES.append(("skill_missing", f"{skill_md} not found"))
        if not exit_check.exists():
            ISSUES.append(("exit_check_missing", f"{exit_check} not found"))


def check_hooks():
    hooks_dir = ROOT / "hooks"
    expected = ["pre-commit-check.sh", "stop-gate.sh"]
    for name in expected:
        if not (hooks_dir / name).exists():
            ISSUES.append(("hook_missing", f"{hooks_dir / name} not found"))


def check_state():
    state_dir = ROOT / "state"
    if not state_dir.exists():
        ISSUES.append(("state_dir_missing", f"{state_dir} not found"))


def check_docs():
    for doc in ["CLAUDE.md", "docs/HARNESS-ARCHITECTURE.md", "docs/EVOLUTION-PROTOCOL.md"]:
        if not (ROOT / doc).exists():
            ISSUES.append(("doc_missing", f"{doc} not found"))


def main() -> int:
    check_skills()
    check_hooks()
    check_state()
    check_docs()

    if not ISSUES:
        print("✅ Harness health check passed. All critical components present.")
        return 0

    print("❌ Harness health issues detected:\n")
    for code, detail in ISSUES:
        print(f"  [{code}] {detail}")
    print()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
