#!/usr/bin/env python3
"""Unit tests for release-builder exit-check."""

import tempfile
import unittest
from pathlib import Path

from tests.mock_state import (
    DEFAULT_L2_SPEC,
    DEFAULT_L3_DESIGN,
    DEFAULT_L4_PLAN,
    DEFAULT_TASK_HISTORY,
    create_state_dir,
    run_exit_check,
)

SKILL_PATH = "dev/release-builder"


class TestReleaseBuilder(unittest.TestCase):

    def _setup_state(self, tmpdir, **overrides):
        state_dir = create_state_dir(tmpdir)
        files = {
            "L1-summary.md": "# L1\n\n**Project Goal:** Test\n**Tech Stack:** Python\n",
            "L2-spec.md": overrides.get("l2", DEFAULT_L2_SPEC),
            "L3-design.md": overrides.get("l3", DEFAULT_L3_DESIGN),
            "L4-plan.md": overrides.get("l4", DEFAULT_L4_PLAN),
            "task-history.yaml": overrides.get("history", DEFAULT_TASK_HISTORY),
            "L5-validation.md": "# Validation\n\n## 7-Day Check\nDone.\n",
        }
        for name, content in files.items():
            if content is not None:
                (state_dir / name).write_text(content, encoding="utf-8")

        project_root = Path(tmpdir)
        if overrides.get("rollback", False):
            (project_root / "ROLLBACK.md").write_text(
                "# Rollback Plan\n\nRevert to v1.2 if error rate > 5%.\n",
                encoding="utf-8",
            )
        if overrides.get("release_notes", False):
            (project_root / "RELEASE-NOTES.md").write_text(
                "# Release Notes\n\nv1.0.0 - Initial release.\n",
                encoding="utf-8",
            )

    def test_passes_with_complete_state(self):
        with tempfile.TemporaryDirectory() as tmp:
            self._setup_state(tmp, rollback=True, release_notes=True)
            result = run_exit_check(SKILL_PATH, tmp)
            self.assertEqual(
                result.returncode,
                0,
                f"Expected pass, got:\nstdout: {result.stdout}\nstderr: {result.stderr}",
            )
            self.assertIn("PASSED", result.stdout)

    def test_blocks_when_no_rollback(self):
        with tempfile.TemporaryDirectory() as tmp:
            self._setup_state(tmp, rollback=False, release_notes=True)
            result = run_exit_check(SKILL_PATH, tmp)
            self.assertEqual(result.returncode, 1)
            self.assertIn("no_rollback_plan", result.stdout)

    def test_warns_when_incomplete_tasks(self):
        history = """# Task History

- task: "Fix bug"
  skill: bug-fixer
  status: in-progress
  output: ""
  timestamp: "2026-04-19T10:00:00"
"""
        with tempfile.TemporaryDirectory() as tmp:
            self._setup_state(tmp, rollback=True, release_notes=True, history=history)
            result = run_exit_check(SKILL_PATH, tmp)
            self.assertEqual(result.returncode, 0)  # warning 不阻断
            self.assertIn("incomplete_tasks", result.stdout)

    def test_blocks_when_spec_missing(self):
        with tempfile.TemporaryDirectory() as tmp:
            self._setup_state(tmp, rollback=True, release_notes=True, l2=None)
            result = run_exit_check(SKILL_PATH, tmp)
            self.assertEqual(result.returncode, 1)
            self.assertIn("spec_missing", result.stdout)


if __name__ == "__main__":
    unittest.main()
