#!/usr/bin/env python3
"""Unit tests for product-spec-builder exit-check."""

import tempfile
import unittest

from tests.mock_state import (
    DEFAULT_L0_STRATEGY,
    DEFAULT_L2_SPEC,
    create_state_dir,
    run_exit_check,
)

SKILL_PATH = "dev/product-spec-builder"


class TestProductSpecBuilder(unittest.TestCase):

    def _setup_state(self, tmpdir, spec=None, l0=None):
        state_dir = create_state_dir(tmpdir)
        if spec is not None:
            (state_dir / "L2-spec.md").write_text(spec, encoding="utf-8")
        if l0 is not None:
            (state_dir / "L0-strategy.md").write_text(l0, encoding="utf-8")

    def test_passes_with_complete_spec(self):
        with tempfile.TemporaryDirectory() as tmp:
            self._setup_state(tmp, spec=DEFAULT_L2_SPEC)
            result = run_exit_check(SKILL_PATH, tmp)
            self.assertEqual(
                result.returncode,
                0,
                f"Expected pass, got:\nstdout: {result.stdout}\nstderr: {result.stderr}",
            )
            self.assertIn("passed", result.stdout)

    def test_blocks_when_spec_missing(self):
        with tempfile.TemporaryDirectory() as tmp:
            self._setup_state(tmp, spec=None)
            result = run_exit_check(SKILL_PATH, tmp)
            self.assertEqual(result.returncode, 1)
            self.assertIn("file_missing", result.stdout)

    def test_blocks_when_section_missing(self):
        spec = """# Product Spec

## Problem Statement
We have a problem.

## Target User
Our users.

## Out of Scope
Nothing.
"""
        with tempfile.TemporaryDirectory() as tmp:
            self._setup_state(tmp, spec=spec)
            result = run_exit_check(SKILL_PATH, tmp)
            self.assertEqual(result.returncode, 1)
            self.assertIn("section_missing", result.stdout)

    def test_blocks_when_spec_too_short(self):
        spec = """# Product Spec

## Problem Statement
Small problem.

## Target User
Users.

## Core Features
- Feature 1

## Success Metrics
Better.

## Out of Scope
Nothing.
"""
        with tempfile.TemporaryDirectory() as tmp:
            self._setup_state(tmp, spec=spec)
            result = run_exit_check(SKILL_PATH, tmp)
            self.assertEqual(result.returncode, 1)
            self.assertIn("spec_too_short", result.stdout)

    def test_warns_when_no_priority(self):
        spec = (DEFAULT_L2_SPEC
            .replace("P0", "Feature").replace("P1", "Feature").replace("P2", "Feature")
            .replace("Must Have", "Feature").replace("Should Have", "Feature").replace("Nice to Have", "Feature")
            .replace("MVP", "Feature").replace("MVP Boundary", "Feature Boundary").replace("In MVP", "In Feature").replace("Post MVP", "Post Feature"))
        with tempfile.TemporaryDirectory() as tmp:
            self._setup_state(tmp, spec=spec)
            result = run_exit_check(SKILL_PATH, tmp)
            self.assertEqual(result.returncode, 0)
            self.assertIn("features_not_prioritized", result.stdout)

    def test_warns_l0_l2_misaligned(self):
        l0 = """# Content Strategy

## Business Goal
Teach quantum physics to elementary school children through cartoon characters.

## Target Audience
High school students.

## KPI
- Graduation rate: 95%
"""
        with tempfile.TemporaryDirectory() as tmp:
            self._setup_state(tmp, spec=DEFAULT_L2_SPEC, l0=l0)
            result = run_exit_check(SKILL_PATH, tmp)
            self.assertEqual(result.returncode, 0)
            self.assertIn("l0_l2_business_goal_gap", result.stdout)


if __name__ == "__main__":
    unittest.main()
