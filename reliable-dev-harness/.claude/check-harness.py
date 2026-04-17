#!/usr/bin/env python3
"""
Harness Health Check - Dual-Track Edition
Verify that the Harness infrastructure is intact for both dev and content domains.
"""

import sys
from pathlib import Path

ROOT = Path(__file__).parent
ISSUES = []

DEV_SKILLS = [
    "product-spec-builder",
    "design-brief-builder",
    "design-maker",
    "dev-planner",
    "dev-builder",
    "bug-fixer",
    "code-review",
    "release-builder",
]

CONTENT_SKILLS = [
    "script-writer",
    "visual-designer",
    "tts-engine",
    "video-compositor",
]

STATE_FILES = [
    "L1-summary.md",
    "L2-spec.md",
    "L3-design.md",
    "L4-plan.md",
    "L5-media.md",
]

DOC_FILES = [
    "CLAUDE.md",
    "docs/HARNESS-ARCHITECTURE.md",
    "docs/EVOLUTION-PROTOCOL.md",
    "docs/CONTENT-PIPELINE.md",
]


def check_skills():
    skills_dir = ROOT / "skills"

    # Check dev skills
    for name in DEV_SKILLS:
        skill_md = skills_dir / "dev" / name / "SKILL.md"
        exit_check = skills_dir / "dev" / name / "exit-check.py"
        if not skill_md.exists():
            ISSUES.append(
                ("dev_skill_missing", f"Dev skill SKILL.md not found: {skill_md}")
            )
        if not exit_check.exists():
            ISSUES.append(
                (
                    "dev_exit_check_missing",
                    f"Dev skill exit-check.py not found: {exit_check}",
                )
            )

    # Check content skills
    for name in CONTENT_SKILLS:
        skill_md = skills_dir / "content" / name / "SKILL.md"
        exit_check = skills_dir / "content" / name / "exit-check.py"
        if not skill_md.exists():
            ISSUES.append(
                (
                    "content_skill_missing",
                    f"Content skill SKILL.md not found: {skill_md}",
                )
            )
        if not exit_check.exists():
            ISSUES.append(
                (
                    "content_exit_check_missing",
                    f"Content skill exit-check.py not found: {exit_check}",
                )
            )


def check_hooks():
    hooks_dir = ROOT / "hooks"
    expected = ["pre-commit-check.sh", "stop-gate.sh", "content-validator.sh"]
    for name in expected:
        if not (hooks_dir / name).exists():
            ISSUES.append(("hook_missing", f"{hooks_dir / name} not found"))


def check_state():
    state_dir = ROOT / "state"
    if not state_dir.exists():
        ISSUES.append(("state_dir_missing", f"{state_dir} not found"))
    else:
        for name in STATE_FILES:
            if not (state_dir / name).exists():
                ISSUES.append(
                    ("state_file_missing", f"State file not found: {state_dir / name}")
                )


def check_docs():
    for doc in DOC_FILES:
        if not (ROOT / doc).exists():
            ISSUES.append(("doc_missing", f"Doc not found: {ROOT / doc}"))


def main() -> int:
    check_skills()
    check_hooks()
    check_state()
    check_docs()

    if not ISSUES:
        print(
            "✅ Harness health check passed. Both dev/ and content/ domains are intact."
        )
        return 0

    print("❌ Harness health issues detected:\n")
    for code, detail in ISSUES:
        print(f"  [{code}] {detail}")
    print()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
