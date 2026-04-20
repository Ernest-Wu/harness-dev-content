#!/usr/bin/env python3
"""
Harness shared exit-check utilities.

Provides unified ISSUES management and formatted reporting for all
skill exit-check scripts across dev, content, and pm domains.

Usage in any exit-check.py:
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent.parent.parent))
    from _utils.exit_check_base import add_issue, print_and_exit

    add_issue(code="file_missing", detail="...", level="high")
    print_and_exit()
"""

import os
import sys
from pathlib import Path

ISSUES = []


def ensure_project_root() -> Path:
    """Verify that the script is run from the project root.

    Looks for .claude/state/ or .claude/skills/ to confirm cwd is correct.
    Returns the project root Path if valid.

    Raises:
        SystemExit: If not run from project root.
    """
    cwd = Path.cwd()
    if not (cwd / ".claude" / "state").exists() and not (cwd / ".claude" / "skills").exists():
        print(
            f"❌ Exit check must be run from the project root (where .claude/ exists).\n"
            f"   Current directory: {cwd}\n"
            f"   Try: cd /path/to/project && python3 {sys.argv[0]}"
        )
        sys.exit(1)
    return cwd
_VALID_LEVELS = frozenset({"high", "warning", "info"})


def add_issue(code: str, detail: str, level: str = "high") -> None:
    """Append an issue with severity level.

    Args:
        code: Short machine-readable identifier (e.g. "file_missing").
        detail: Human-readable explanation.
        level: Severity — "high" blocks progress, "warning" needs PM review,
               "info" is informational only.

    Raises:
        ValueError: If level is not one of "high", "warning", "info".
    """
    if level not in _VALID_LEVELS:
        raise ValueError(
            f"Invalid level '{level}'. Must be one of: {_VALID_LEVELS}"
        )
    ISSUES.append((level, code, detail))


if __name__ == "__main__":
    print(
        "This module is not meant to be run directly. "
        "Import add_issue and print_and_exit from your exit-check.py script."
    )
    sys.exit(1)


def print_and_exit(skill_name: str = "") -> None:
    """Print grouped issues and exit with appropriate code.

    Exit codes:
        1 — if any high-severity issues exist.
        0 — otherwise (warnings/info do not block).

    Args:
        skill_name: Optional skill name shown in the header and summary.
    """
    high_issues = [i for i in ISSUES if i[0] == "high"]
    warning_issues = [i for i in ISSUES if i[0] == "warning"]
    info_issues = [i for i in ISSUES if i[0] == "info"]

    if skill_name:
        print(f"═══ {skill_name} Exit Check ═══")
        print()

    for level, code, detail in info_issues:
        print(f"  ℹ️  [{code}] {detail}")
    if info_issues:
        print()

    for level, code, detail in warning_issues:
        print(f"  ⚠️  [{code}] {detail}")
    if warning_issues:
        print()

    for level, code, detail in high_issues:
        print(f"  ❌ [{code}] {detail}")
    if high_issues:
        print()

    print(
        f"  Total: {len(high_issues)} high, "
        f"{len(warning_issues)} warning, {len(info_issues)} info"
    )
    print()

    if high_issues:
        if skill_name:
            print(
                f"❌ {skill_name} exit check FAILED — "
                "resolve HIGH issues before proceeding."
            )
        else:
            print("❌ Exit check FAILED — resolve HIGH issues before proceeding.")
        sys.exit(1)

    if warning_issues:
        if skill_name:
            print(
                f"⚠️  {skill_name} exit check PASSED with warnings — "
                "review before proceeding."
            )
        else:
            print("⚠️  Exit check PASSED with warnings — review before proceeding.")
    else:
        if skill_name:
            print(f"✅ {skill_name} exit check passed.")
        else:
            print("✅ Exit check passed.")

    sys.exit(0)
