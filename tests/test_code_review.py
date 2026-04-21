#!/usr/bin/env python3
"""Unit tests for code-review exit-check."""

import tempfile
import unittest
from pathlib import Path

from tests.mock_state import (
    DEFAULT_L2_SPEC,
    DEFAULT_REVIEW,
    create_state_dir,
    run_exit_check,
)

SKILL_PATH = "dev/code-review"


class TestCodeReview(unittest.TestCase):

    def _setup_state(self, tmpdir, review=None, spec=None):
        state_dir = create_state_dir(tmpdir)
        if review is not None:
            (state_dir / "LAST_REVIEW.md").write_text(review, encoding="utf-8")
        if spec is not None:
            (state_dir / "L2-spec.md").write_text(spec, encoding="utf-8")

    def test_passes_with_good_review(self):
        with tempfile.TemporaryDirectory() as tmp:
            self._setup_state(tmp, review=DEFAULT_REVIEW, spec=DEFAULT_L2_SPEC)
            result = run_exit_check(SKILL_PATH, tmp)
            self.assertEqual(
                result.returncode,
                0,
                f"Expected pass, got:\nstdout: {result.stdout}\nstderr: {result.stderr}",
            )
            self.assertIn("PASSED", result.stdout)

    def test_blocks_when_review_missing(self):
        with tempfile.TemporaryDirectory() as tmp:
            self._setup_state(tmp, review=None, spec=DEFAULT_L2_SPEC)
            result = run_exit_check(SKILL_PATH, tmp)
            self.assertEqual(result.returncode, 1)
            self.assertIn("review_file_missing", result.stdout)

    def test_blocks_when_stage1_missing(self):
        review = """# Code Review

## Stage 2: Code Quality
Some comments here.
"""
        with tempfile.TemporaryDirectory() as tmp:
            self._setup_state(tmp, review=review, spec=DEFAULT_L2_SPEC)
            result = run_exit_check(SKILL_PATH, tmp)
            self.assertEqual(result.returncode, 1)
            self.assertIn("stage1_missing", result.stdout)

    def test_blocks_when_high_ignored(self):
        review = """# Code Review

## Stage 1: Spec Compliance

- **HIGH**: Security issue found — must fix before release

## Stage 2: Code Quality

### Verdict
Stage 2: PASSED
"""
        with tempfile.TemporaryDirectory() as tmp:
            self._setup_state(tmp, review=review, spec=DEFAULT_L2_SPEC)
            result = run_exit_check(SKILL_PATH, tmp)
            self.assertEqual(result.returncode, 1)
            self.assertIn("high_issue_ignored", result.stdout)

    def test_warns_when_too_lenient(self):
        # Must be > 200 chars, have Stage 1/2, checklist structure, code locations
        # But NO action words (should, fix, refactor, etc.) to trigger review_too_lenient
        review = """# Code Review

## Stage 1: Spec Compliance

- [x] **Login form** — Fully implemented
- [x] **Email validation** — Verified at auth/login.ts:42
- [x] **Password reset** — Working correctly

All requirements from the specification document are met. The code looks great and everything appears correct. No problems detected during review.

## Stage 2: Code Quality

The code is clean and well-structured. All naming conventions are followed. The code is readable and maintainable.
"""
        with tempfile.TemporaryDirectory() as tmp:
            self._setup_state(tmp, review=review, spec=DEFAULT_L2_SPEC)
            result = run_exit_check(SKILL_PATH, tmp)
            self.assertEqual(result.returncode, 0)
            self.assertIn("review_too_lenient", result.stdout)


if __name__ == "__main__":
    unittest.main()
