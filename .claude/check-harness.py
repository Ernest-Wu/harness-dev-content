#!/usr/bin/env python3
"""
Harness Health Check - Three-Domain Edition
Verify that the Harness infrastructure is intact for dev, content, and pm domains.
"""

import ast
import py_compile
import re
import subprocess
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
    "frontend-slides",
    "tts-engine",
    "video-compositor",
]

PM_SKILLS = [
    "validation",
    "content-strategy",
    "distribution-planner",
    "content-validation",
]

STATE_FILES = [
    "L0-strategy.md",
    "L1-summary.md",
    "L2-spec.md",
    "L2-content-spec.md",
    "L3-design.md",
    "L4-plan.md",
    "L5-media.md",
    "L5-content-validation.md",
    "L6-distribution.md",
    "task-history.yaml",
]

DOC_FILES = [
    "CLAUDE.md",
    "docs/HARNESS-ARCHITECTURE.md",
    "docs/EVOLUTION-PROTOCOL.md",
    "docs/CONTENT-PIPELINE.md",
    "docs/FIGMA_MCP_SETUP.md",
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

    # Check pm skills
    for name in PM_SKILLS:
        skill_md = skills_dir / "pm" / name / "SKILL.md"
        exit_check = skills_dir / "pm" / name / "exit-check.py"
        if not skill_md.exists():
            ISSUES.append(
                (
                    "pm_skill_missing",
                    f"PM skill SKILL.md not found: {skill_md}",
                )
            )
        if not exit_check.exists():
            ISSUES.append(
                (
                    "pm_exit_check_missing",
                    f"PM skill exit-check.py not found: {exit_check}",
                )
            )


def check_hooks():
    hooks_dir = ROOT / "hooks"
    expected = [
        "pre-commit-check.sh",
        "stop-gate.sh",
        "content-validator.sh",
        "detect-feedback-signal.py",
        "mark-review-needed.sh",
    ]
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


def check_syntax():
    """T7: Verify all .py files compile and all .sh files pass bash -n."""
    # Python files
    py_files = list((ROOT / "skills").rglob("*.py"))
    py_files.append(ROOT / "router.py")
    py_files.append(ROOT / "check-harness.py")
    for py_file in py_files:
        try:
            py_compile.compile(str(py_file), doraise=True)
        except py_compile.PyCompileError as e:
            ISSUES.append(("syntax_error", f"{py_file}: {e}"))

    # Bash files
    hooks_dir = ROOT / "hooks"
    for sh_file in hooks_dir.glob("*.sh"):
        result = subprocess.run(
            ["bash", "-n", str(sh_file)],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            ISSUES.append(
                ("hook_syntax_error", f"{sh_file}: {result.stderr.strip()}")
            )


def check_skill_frontmatter():
    """T8: Verify all SKILL.md files contain basic frontmatter."""
    skills_dir = ROOT / "skills"
    for skill_md in skills_dir.rglob("SKILL.md"):
        content = skill_md.read_text(encoding="utf-8")
        if not content.startswith("---"):
            ISSUES.append(
                ("skill_frontmatter_missing", f"{skill_md} missing YAML frontmatter")
            )
        elif "name:" not in content or "description:" not in content:
            ISSUES.append(
                (
                    "skill_frontmatter_incomplete",
                    f"{skill_md} frontmatter missing name or description",
                )
            )


def check_state_schema():
    """T10: Verify existing state files are non-empty and have structure."""
    state_dir = ROOT / "state"
    if not state_dir.exists():
        return
    for name in STATE_FILES:
        path = state_dir / name
        if not path.exists():
            continue
        content = path.read_text(encoding="utf-8").strip()
        if not content:
            ISSUES.append(("state_file_empty", f"State file is empty: {path}"))
        elif path.suffix == ".md":
            if not re.search(r"^#\s+", content, re.MULTILINE):
                ISSUES.append(
                    ("state_file_no_heading", f"State file missing Markdown heading: {path}")
                )


def check_exit_check_format():
    """T11: Verify all exit-check.py scripts use _utils/exit_check_base."""
    skills_dir = ROOT / "skills"
    for exit_check in skills_dir.rglob("exit-check.py"):
        source = exit_check.read_text(encoding="utf-8")
        try:
            tree = ast.parse(source)
        except SyntaxError as e:
            ISSUES.append(
                ("exit_check_ast_error", f"{exit_check}: syntax error - {e}")
            )
            continue

        uses_base = False
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name == "_utils.exit_check_base":
                        uses_base = True
            elif isinstance(node, ast.ImportFrom):
                if node.module == "_utils.exit_check_base":
                    uses_base = True
                elif node.module == "_utils":
                    for alias in node.names:
                        if alias.name == "exit_check_base":
                            uses_base = True

        if not uses_base:
            ISSUES.append(
                (
                    "exit_check_not_using_base",
                    f"{exit_check} does not import from _utils.exit_check_base",
                )
            )


def main() -> int:
    check_skills()
    check_hooks()
    check_state()
    check_docs()
    check_syntax()
    check_skill_frontmatter()
    check_state_schema()
    check_exit_check_format()

    if not ISSUES:
        print(
            "✅ Harness health check passed. All three domains (dev/, content/, pm/) are intact."
        )
        return 0

    print("❌ Harness health issues detected:\n")
    for code, detail in ISSUES:
        print(f"  [{code}] {detail}")
    print()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
