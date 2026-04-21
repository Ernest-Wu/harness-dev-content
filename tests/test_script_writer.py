#!/usr/bin/env python3
"""Unit tests for script-writer exit-check."""

import json
import tempfile
import unittest
from pathlib import Path

from tests.mock_state import (
    DEFAULT_L0_STRATEGY,
    DEFAULT_L2_CONTENT_SPEC,
    DEFAULT_SCENES,
    create_state_dir,
    run_exit_check,
)

SKILL_PATH = "content/script-writer"


class TestScriptWriter(unittest.TestCase):

    def _setup_state(self, tmpdir, scenes=None, spec=None, l0=None, draft=None):
        project_dir = Path(tmpdir)
        state_dir = create_state_dir(tmpdir)

        if scenes is not None:
            (project_dir / "scenes.json").write_text(
                json.dumps(scenes) if isinstance(scenes, dict) else scenes,
                encoding="utf-8",
            )
        if spec is not None:
            (state_dir / "L2-content-spec.md").write_text(spec, encoding="utf-8")
        if l0 is not None:
            (state_dir / "L0-strategy.md").write_text(l0, encoding="utf-8")
        if draft is not None:
            (project_dir / "draft-script.md").write_text(draft, encoding="utf-8")

    def test_passes_with_valid_scenes(self):
        draft = "This is the draft script content for the video. It covers the main talking points."
        with tempfile.TemporaryDirectory() as tmp:
            self._setup_state(
                tmp,
                scenes=DEFAULT_SCENES,
                spec=DEFAULT_L2_CONTENT_SPEC,
                draft=draft,
            )
            result = run_exit_check(SKILL_PATH, tmp)
            self.assertEqual(
                result.returncode,
                0,
                f"Expected pass, got:\nstdout: {result.stdout}\nstderr: {result.stderr}",
            )
            self.assertIn("passed", result.stdout)

    def test_blocks_when_scenes_missing(self):
        with tempfile.TemporaryDirectory() as tmp:
            self._setup_state(tmp, scenes=None, spec=DEFAULT_L2_CONTENT_SPEC)
            result = run_exit_check(SKILL_PATH, tmp)
            self.assertEqual(result.returncode, 1)
            self.assertIn("file_missing", result.stdout)

    def test_blocks_when_invalid_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            self._setup_state(tmp, scenes="not json", spec=DEFAULT_L2_CONTENT_SPEC)
            result = run_exit_check(SKILL_PATH, tmp)
            self.assertEqual(result.returncode, 1)
            self.assertIn("invalid_json", result.stdout)

    def test_blocks_when_too_few_scenes(self):
        scenes = {"scenes": [{"id": "only", "text": "One scene", "estimatedDuration": 5, "visualBeats": []}]}
        with tempfile.TemporaryDirectory() as tmp:
            self._setup_state(tmp, scenes=scenes, spec=DEFAULT_L2_CONTENT_SPEC)
            result = run_exit_check(SKILL_PATH, tmp)
            self.assertEqual(result.returncode, 1)
            self.assertIn("too_few_scenes", result.stdout)

    def test_blocks_when_missing_required_fields(self):
        scenes = {
            "scenes": [
                {"text": "Missing id and duration", "visualBeats": []},
            ]
        }
        with tempfile.TemporaryDirectory() as tmp:
            self._setup_state(tmp, scenes=scenes, spec=DEFAULT_L2_CONTENT_SPEC)
            result = run_exit_check(SKILL_PATH, tmp)
            self.assertEqual(result.returncode, 1)
            self.assertIn("missing_field", result.stdout)

    def test_blocks_when_spec_missing_platform(self):
        # Remove the entire Platform line to trigger the missing platform check
        spec = DEFAULT_L2_CONTENT_SPEC.replace("Platform: 9:16 (Douyin/Xiaohongshu vertical)\n", "")
        with tempfile.TemporaryDirectory() as tmp:
            self._setup_state(tmp, scenes=DEFAULT_SCENES, spec=spec, draft="test draft")
            result = run_exit_check(SKILL_PATH, tmp)
            self.assertEqual(result.returncode, 1)
            self.assertIn("spec_missing_platform", result.stdout)

    def test_warns_l0_l2_audience_gap(self):
        draft = "Draft script for testing audience gap."
        l0 = DEFAULT_L0_STRATEGY
        spec = DEFAULT_L2_CONTENT_SPEC.replace("audience", "viewers")
        with tempfile.TemporaryDirectory() as tmp:
            self._setup_state(tmp, scenes=DEFAULT_SCENES, spec=spec, l0=l0, draft=draft)
            result = run_exit_check(SKILL_PATH, tmp)
            self.assertEqual(result.returncode, 0)
            self.assertIn("l0_l2_audience_gap", result.stdout)


if __name__ == "__main__":
    unittest.main()
