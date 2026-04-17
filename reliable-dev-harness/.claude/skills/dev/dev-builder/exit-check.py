#!/usr/bin/env python3
"""
Exit Check: dev-builder
Deterministic gate before a Task can be considered complete.
"""

import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(".")
BUILD_COMMANDS = [
    ["npm", "run", "build"],
    ["pnpm", "build"],
    ["yarn", "build"],
    ["python", "-m", "compileall", "src/"],
    ["cargo", "build"],
    ["go", "build", "./..."],
]
TEST_COMMANDS = [
    ["npm", "test", "--", "--run"],
    ["pnpm", "test", "--run"],
    ["vitest", "run"],
    ["pytest"],
    ["cargo", "test"],
    ["go", "test", "./..."],
]

ISSUES = []


def detect_command(candidates: list[list[str]]) -> list[str] | None:
    for cmd in candidates:
        if which(cmd[0]):
            # Quick heuristic: npm needs package.json
            if cmd[0] in ("npm", "pnpm", "yarn") and not (PROJECT_ROOT / "package.json").exists():
                continue
            if cmd[0] == "cargo" and not (PROJECT_ROOT / "Cargo.toml").exists():
                continue
            if cmd[0] == "go" and not list(PROJECT_ROOT.glob("go.mod")):
                continue
            if cmd[0] == "pytest" and not list(PROJECT_ROOT.rglob("*_test.py")) and not list(PROJECT_ROOT.rglob("test_*.py")):
                continue
            return cmd
    return None


def which(program: str) -> bool:
    return subprocess.run(["which", program], capture_output=True).returncode == 0


def run_cmd(cmd: list[str], label: str) -> bool:
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        if result.returncode != 0:
            ISSUES.append((
                f"{label}_failed",
                f"'{ ' '.join(cmd) }' failed with exit code {result.returncode}.\n"
                f"stdout: {result.stdout[-500:]}\nstderr: {result.stderr[-500:]}"
            ))
            return False
        return True
    except Exception as e:
        ISSUES.append((f"{label}_error", f"Error running '{' '.join(cmd)}': {e}"))
        return False


def check():
    # 1. Build check
    build_cmd = detect_command(BUILD_COMMANDS)
    if build_cmd:
        run_cmd(build_cmd, "build")
    else:
        ISSUES.append((
            "build_command_not_found",
            "No recognizable build command found. Add one to BUILD_COMMANDS in exit-check.py."
        ))

    # 2. Test check (warn if no tests found, but don't block)
    test_cmd = detect_command(TEST_COMMANDS)
    if test_cmd:
        run_cmd(test_cmd, "test")
    else:
        ISSUES.append((
            "test_command_not_found",
            "No recognizable test command found. If this project has tests, add the command to TEST_COMMANDS."
        ))

    # 3. Ensure task-history.yaml exists and was updated recently
    history_path = PROJECT_ROOT / ".claude" / "state" / "task-history.yaml"
    if not history_path.exists():
        ISSUES.append((
            "task_history_missing",
            ".claude/state/task-history.yaml does not exist. Every completed Task must be recorded."
        ))
    else:
        content = history_path.read_text(encoding="utf-8")
        if "status: completed" not in content:
            ISSUES.append((
                "task_history_empty",
                "task-history.yaml exists but contains no 'completed' entries. Record this Task before finishing."
            ))


def main() -> int:
    check()
    if not ISSUES:
        print("✅ dev-builder exit check passed. Task is complete and review-ready.")
        return 0

    print("❌ dev-builder exit check failed:\n")
    for code, detail in ISSUES:
        print(f"  [{code}] {detail}")
    print()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
