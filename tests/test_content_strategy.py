#!/usr/bin/env python3
"""Unit tests for content-strategy exit-check."""

import tempfile
import unittest

from tests.mock_state import (
    DEFAULT_L0_STRATEGY,
    create_state_dir,
    run_exit_check,
)

SKILL_PATH = "pm/content-strategy"


class TestContentStrategy(unittest.TestCase):

    def _setup_state(self, tmpdir, l0=None):
        state_dir = create_state_dir(tmpdir)
        if l0 is not None:
            (state_dir / "L0-strategy.md").write_text(l0, encoding="utf-8")

    def test_passes_with_complete_strategy(self):
        with tempfile.TemporaryDirectory() as tmp:
            self._setup_state(tmp, l0=DEFAULT_L0_STRATEGY)
            result = run_exit_check(SKILL_PATH, tmp)
            self.assertEqual(
                result.returncode,
                0,
                f"Expected pass, got:\nstdout: {result.stdout}\nstderr: {result.stderr}",
            )
            self.assertIn("passed", result.stdout)

    def test_blocks_when_l0_missing(self):
        with tempfile.TemporaryDirectory() as tmp:
            self._setup_state(tmp, l0=None)
            result = run_exit_check(SKILL_PATH, tmp)
            self.assertEqual(result.returncode, 1)
            self.assertIn("file_missing", result.stdout)

    def test_blocks_when_required_section_missing(self):
        l0 = DEFAULT_L0_STRATEGY.replace("## Target Audience", "## Audience")
        with tempfile.TemporaryDirectory() as tmp:
            self._setup_state(tmp, l0=l0)
            result = run_exit_check(SKILL_PATH, tmp)
            self.assertEqual(result.returncode, 1)
            self.assertIn("target_audience_missing", result.stdout)

    def test_blocks_when_kpi_not_quantified(self):
        l0 = DEFAULT_L0_STRATEGY.replace("10,000", "high").replace("45%", "good").replace("5%", "strong")
        with tempfile.TemporaryDirectory() as tmp:
            self._setup_state(tmp, l0=l0)
            result = run_exit_check(SKILL_PATH, tmp)
            self.assertEqual(result.returncode, 1)
            self.assertIn("kpi_not_quantified", result.stdout)

    def test_warns_when_audience_vague(self):
        l0 = DEFAULT_L0_STRATEGY.replace(
            "25-40 year old developers and product managers",
            "everyone who uses computers"
        )
        with tempfile.TemporaryDirectory() as tmp:
            self._setup_state(tmp, l0=l0)
            result = run_exit_check(SKILL_PATH, tmp)
            self.assertEqual(result.returncode, 0)
            self.assertIn("vague_audience", result.stdout)

    def test_warns_when_differentiation_missing(self):
        l0 = DEFAULT_L0_STRATEGY.replace("## Differentiation", "## Unique Value")
        with tempfile.TemporaryDirectory() as tmp:
            self._setup_state(tmp, l0=l0)
            result = run_exit_check(SKILL_PATH, tmp)
            self.assertEqual(result.returncode, 0)
            self.assertIn("diff_missing", result.stdout)


if __name__ == "__main__":
    unittest.main()
