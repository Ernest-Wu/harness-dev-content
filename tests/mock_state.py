#!/usr/bin/env python3
"""
Mock state generator for exit-check unit tests.

Provides utilities to create temporary project structures and run
exit-check scripts in isolation.
"""

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Optional, Union

# Path to the real harness
HARNESS_DIR = Path(__file__).parent.parent
SKILLS_DIR = HARNESS_DIR / ".claude" / "skills"


def run_exit_check(skill_path: str, cwd: Union[str, Path]) -> subprocess.CompletedProcess:
    """Run an exit-check.py in the given working directory.

    Args:
        skill_path: Relative path under .claude/skills/, e.g. "dev/release-builder"
        cwd: Working directory to run in (must have .claude/state/ for ensure_project_root)

    Returns:
        CompletedProcess with exit_code, stdout, stderr
    """
    exit_check = SKILLS_DIR / skill_path / "exit-check.py"
    if not exit_check.exists():
        raise FileNotFoundError(f"Exit check not found: {exit_check}")

    env = {**os.environ, "PYTHONPATH": str(SKILLS_DIR)}
    result = subprocess.run(
        [sys.executable, str(exit_check)],
        cwd=cwd,
        capture_output=True,
        text=True,
        env=env,
    )
    return result


def create_state_dir(project_dir: Union[str, Path]) -> Path:
    """Create .claude/state/ directory in the given project directory."""
    state_dir = Path(project_dir) / ".claude" / "state"
    state_dir.mkdir(parents=True, exist_ok=True)
    return state_dir


# ── Default state templates ──────────────────────────────────────────

DEFAULT_L1_SUMMARY = """# L1 Project Summary

**Project Goal:** Build an AI writing assistant
**Target User:** Content creators and marketers
**Core Features:**
1. AI-powered writing suggestions
2. Real-time grammar correction
3. Content optimization
**Tech Stack:** Next.js + TypeScript + Tailwind
**Current Active Phase:** Phase 1: Implementation
**Next Task:** Implement login API
"""

DEFAULT_L2_SPEC = """# Product Spec

## Problem Statement
Writers struggle with writer's block and inconsistent quality.

## Target User
Content creators who publish 3+ articles per week.

## Core Features

### P0 (MVP — Must Have)
- **AI Suggestions** — Real-time writing assistance
- **Grammar Check** — Error detection and correction
- **Export** — Save to Markdown and PDF

### P1 (Should Have)
- **Team Collaboration** — Share documents with team

### P2 (Nice to Have)
- **AI Voice** — Read content aloud

## Business Goal
Increase content output by 30% within 90 days.

## Success Metrics
| Metric | Target | Measurement |
|--------|--------|-------------|
| Weekly articles | 5 per user | In-app tracking |
| User retention | 60% at 30 days | Mixpanel |

## Out of Scope
- Social media scheduling
- Stock photo integration

## Assumptions
- Users have basic writing skills: validated
- AI latency under 500ms: pending

## MVP Boundary
**In MVP (Phase 0):** AI Suggestions, Grammar Check, Export
**Post MVP (Phase 1+):** Team Collaboration, AI Voice
"""

DEFAULT_L3_DESIGN = """# Design Brief

## Design Tokens
- Primary: #3B82F6
- Background: #FFFFFF
- Text: #1F2937

## Brand
No external brand constraints. Clean, minimal aesthetic.

## Accessibility
WCAG 2.1 AA compliance required.
"""

DEFAULT_L4_PLAN = """# Dev Plan

## Business Goal
Deliver MVP in 4 weeks with 3 core features.

## Feature-Phase Mapping
- Phase 0 (MVP): AI Suggestions, Grammar Check, Export
- Phase 1: Team Collaboration
- Phase 2: AI Voice

## Risk Flags
- [ ] AI latency > 500ms: high — use caching
- [ ] Third-party API costs: medium — implement rate limiting

## MVP Boundary Confirmation
- MVP Scope: AI Suggestions, Grammar Check, Export
- Post-MVP: Team Collaboration, AI Voice

## Completed Phases
- Phase 0: 2026-04-01

## Spec Gaps
<!-- None yet -->
"""

DEFAULT_L0_STRATEGY = """# Content Strategy

## Business Goal
Increase brand awareness among tech-savvy professionals.

## Target Audience
25-40 year old developers and product managers interested in AI tools.

## KPI
- Views: 10,000 per video
- Completion rate: 45%
- Engagement rate: 5%

## Core Message
AI writing tools can 3x your content output without sacrificing quality.

## Differentiation Strategy
Focus on practical workflows, not just features.

## Compliance
No special compliance requirements.
"""

DEFAULT_L2_CONTENT_SPEC = """# Content Spec

Platform: 9:16 (Douyin/Xiaohongshu vertical)
Mood: Professional but approachable
Duration: 60-90 seconds

## Business Goal
Drive sign-ups for the AI writing assistant.

## Core Message
Write faster, write better with AI.

## Differentiation
Show real workflows, not just feature lists.

Input: topic
"""

DEFAULT_TASK_HISTORY = """# Task History

- task: "Implement login page"
  skill: dev-builder
  status: completed
  output: "Login page implemented"
  timestamp: "2026-04-19T10:00:00"

- task: "Review login implementation"
  skill: code-review
  status: completed
  output: "Review passed"
  timestamp: "2026-04-19T11:00:00"
"""

DEFAULT_REVIEW = """# Code Review

## Stage 1: Spec Compliance

- [x] **Login form** — Fully implemented per spec
- [x] **Email validation** — Regex pattern matches spec
- [ ] **Password strength** — Partially implemented (missing special char check)
- [x] **Error messages** — User-friendly messages implemented

### Spec Gap
GAP-001: Password strength requirements unclear — Type: B

## Stage 2: Code Quality

### Issues Found
- **HIGH**: No rate limiting on login endpoint (auth/login.ts:42) — user impact: brute force risk
- **MEDIUM**: Duplicate validation logic in frontend and backend — needs refactoring
- **LOW**: Consider adding loading state to LoginButton component

### Suggestions
- Should extract validation logic into shared module
- Needs to add unit tests for auth service
- Fix naming: `handleClick` should be `handleLoginSubmit`

## Verdict
Stage 1: PASSED (with 1 partial implementation)
Stage 2: CONDITIONAL PASS (fix HIGH issue before merge)
"""

DEFAULT_SCENES = {
    "scenes": [
        {
            "id": "hook",
            "text": "Do you spend 4 hours writing one article? What if you could do it in 30 minutes?",
            "estimatedDuration": 8,
            "visualBeats": ["excited_face", "clock_spinning"],
        },
        {
            "id": "problem",
            "text": "Writer's block hits everyone. The blank page stares back. Nothing comes out.",
            "estimatedDuration": 10,
            "visualBeats": ["blank_page", "frustrated_writer"],
        },
        {
            "id": "solution",
            "text": "Our AI writing assistant gives you real-time suggestions based on your style.",
            "estimatedDuration": 15,
            "visualBeats": ["app_demo", "typing_with_suggestions"],
        },
    ]
}
