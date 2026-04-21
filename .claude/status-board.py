#!/usr/bin/env python3
"""
Harness Status Board — Project progress dashboard.

Reads all .claude/state/ files and outputs a visual progress board
showing Gate status, track progress, and blocking items.

Usage:
    python3 .claude/status-board.py
"""

import argparse
import re
from datetime import datetime
from pathlib import Path
from typing import List, Optional

STATE_DIR = Path(".claude/state")
PROJECT_ROOT = Path(".")


def read_state(filename: str) -> Optional[str]:
    path = STATE_DIR / filename
    if not path.exists():
        return None
    return path.read_text(encoding="utf-8")


def has_heading(content: str, pattern: str) -> bool:
    return bool(re.search(rf"^##\s+.*{pattern}.*$", content, re.MULTILINE | re.IGNORECASE))


def extract_section(content: str, heading: str) -> str:
    regex = re.compile(
        rf"^##\s+{re.escape(heading)}\s*\n(.*?)(?=^##\s|\Z)",
        re.MULTILINE | re.IGNORECASE | re.DOTALL,
    )
    match = regex.search(content)
    return match.group(1).strip() if match else ""


class GateChecker:
    def __init__(self):
        self.l1 = read_state("L1-summary.md") or ""
        self.l0 = read_state("L0-strategy.md") or ""
        self.l2 = read_state("L2-spec.md") or ""
        self.l2c = read_state("L2-content-spec.md") or ""
        self.l3 = read_state("L3-design.md") or ""
        self.l4 = read_state("L4-plan.md") or ""
        self.l5m = read_state("L5-media.md") or ""
        self.l5v = read_state("L5-validation.md") or ""
        self.l5cv = read_state("L5-content-validation.md") or ""
        self.l6 = read_state("L6-distribution.md") or ""
        self.history = read_state("task-history.yaml") or ""
        self.rollback = (PROJECT_ROOT / "ROLLBACK.md").exists()
        self.release_notes = (PROJECT_ROOT / "RELEASE-NOTES.md").exists()

    def _l2_has_p0(self) -> bool:
        return bool(re.search(r"P0|Must\s+Have|优先级", self.l2, re.IGNORECASE))

    def _l2_has_business_goal(self) -> bool:
        return has_heading(self.l2, "Business Goal")

    def _l4_has_phases(self) -> bool:
        return bool(
            re.search(r"Phase\s+\d+|阶段\s*\d", self.l4, re.IGNORECASE)
        )

    def _history_has_review(self) -> bool:
        return "code-review" in self.history.lower() and "completed" in self.history.lower()

    def _l5_has_tts(self) -> bool:
        return bool(re.search(r"tts|配音|audio|voice", self.l5m, re.IGNORECASE))

    def _l5_has_video(self) -> bool:
        return bool(re.search(r"video|mp4|final", self.l5m, re.IGNORECASE))

    def _l6_complete(self) -> bool:
        return bool(
            self.l6
            and has_heading(self.l6, "Platform")
            and has_heading(self.l6, "Tracking")
        )

    def _l5v_has_data(self) -> bool:
        return bool(re.search(r"7.?Day|30.?Day|Actual", self.l5v, re.IGNORECASE))

    def _l5cv_has_data(self) -> bool:
        return bool(re.search(r"metric|kpi|actual|performance", self.l5cv, re.IGNORECASE))

    def check_g0(self):
        if not self.l2:
            return "⬜", "L2-spec.md not found"
        if len(self.l2.strip()) < 200:
            return "⬜", "L2-spec.md nearly empty"
        if not self._l2_has_p0():
            return "⬜", "L2-spec.md missing P0 markers"
        bg = self._l2_has_business_goal()
        p0_count = len(re.findall(r"^[-*]\s+\*\*", self.l2, re.MULTILINE))
        detail = f"P0: {p0_count} features" if p0_count else "P0 section present"
        if bg:
            return "✅", f"L2-spec.md ({detail}, Business Goal: defined)"
        return "⚠️", f"L2-spec.md ({detail}, Business Goal: missing)"

    def check_g1(self):
        if not self.l3:
            return "⬜", "L3-design.md not found"
        if len(self.l3.strip()) < 100:
            return "⬜", "L3-design.md nearly empty"
        has_brand = re.search(r"brand|品牌|no brand|无品牌", self.l3, re.IGNORECASE)
        has_a11y = re.search(r"a11y|accessib|无障碍|wcag", self.l3, re.IGNORECASE)
        brand_str = "brand: defined" if has_brand else "brand: not declared"
        a11y_str = "a11y: declared" if has_a11y else "a11y: not declared"
        return "✅", f"L3-design.md ({brand_str}, {a11y_str})"

    def check_g2(self):
        if not self.l4:
            return "⬜", "L4-plan.md not found"
        if not self._l4_has_phases():
            return "⬜", "L4-plan.md has no phases"
        phases = len(re.findall(r"Phase\s+\d+|阶段\s*\d", self.l4, re.IGNORECASE))
        has_mvp = bool(re.search(r"MVP|最小可行", self.l4, re.IGNORECASE))
        mvp_str = "MVP confirmed" if has_mvp else "MVP not declared"
        return "✅", f"L4-plan.md ({phases} phase(s), {mvp_str})"

    def check_g3(self):
        if not self._history_has_review():
            return "⬜", "No completed code-review in task-history"
        return "✅", "code-review completed"

    def check_g4(self):
        issues = []
        if not self.rollback:
            issues.append("ROLLBACK.md missing")
        if not self.release_notes:
            issues.append("RELEASE-NOTES.md missing")
        if self.history and re.search(r"status:\s*(?:in.progress|pending|blocked)", self.history, re.IGNORECASE):
            issues.append("incomplete tasks in history")
        if issues:
            return "⬜", ", ".join(issues)
        return "✅", "All release gates cleared"

    def check_g5(self):
        if not self.l5v:
            return "⏸", "Waiting for 7-day data (L5-validation.md not found)"
        if not self._l5v_has_data():
            return "⏸", "L5-validation.md exists but no metrics data"
        return "✅", "L5-validation.md has metrics data"

    def check_cg0(self):
        if not self.l0:
            return "⬜", "L0-strategy.md not found"
        if len(self.l0.strip()) < 100:
            return "⬜", "L0-strategy.md nearly empty"
        has_bg = has_heading(self.l0, "Business Goal")
        has_kpi = has_heading(self.l0, "KPI")
        bg_str = "Business Goal: defined" if has_bg else "Business Goal: missing"
        kpi_str = "KPI: defined" if has_kpi else "KPI: missing"
        return "✅", f"L0-strategy.md ({bg_str}, {kpi_str})"

    def check_cg1(self):
        if not self.l3:
            return "⬜", "L3-design.md (content) not found"
        has_mood = re.search(r"mood|style|风格", self.l3, re.IGNORECASE)
        mood_str = "Mood/Style defined" if has_mood else "Mood/Style not found"
        return "✅", f"L3-design.md ({mood_str})"

    def check_cg2(self):
        if not self.l5m:
            return "⬜", "L5-media.md not found"
        if not self._l5_has_tts():
            return "⬜", "L5-media.md missing TTS records"
        return "✅", "L5-media.md has TTS recorded"

    def check_cg3(self):
        if not self.l5m:
            return "⬜", "No media manifest found"
        if not self._l5_has_video():
            return "⬜", "No final video reference in L5-media.md"
        return "✅", "Final video referenced"

    def check_cg4(self):
        if not self.l6:
            return "⬜", "L6-distribution.md not found"
        if not self._l6_complete():
            return "⚠️", "L6-distribution.md incomplete (missing Platform or Tracking)"
        return "✅", "L6-distribution.md complete"

    def check_cg5(self):
        if not self.l5cv:
            return "⏸", "Waiting for post-publish data (L5-content-validation.md not found)"
        if not self._l5cv_has_data():
            return "⏸", "L5-content-validation.md exists but no performance data"
        return "✅", "Content validation data recorded"


def progress_bar(percent: int, width: int = 10) -> str:
    filled = int(width * percent / 100)
    return "█" * filled + "░" * (width - filled)


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Harness Status Board — Project progress dashboard."
    )
    parser.add_argument(
        "--track",
        choices=["dev", "content", "pm"],
        help="Filter output to a single track (dev, content, or pm)"
    )
    args = parser.parse_args(argv)

    if not STATE_DIR.exists():
        print("❌ Project not initialized — .claude/state/ not found.")
        print("   Run: bash scripts/init-harness.sh .")
        return 1

    checker = GateChecker()

    # Collect all gate results
    dev_gates = [
        ("G0 Discovery", checker.check_g0()),
        ("G1 Direction", checker.check_g1()),
        ("G2 Scope", checker.check_g2()),
        ("G3 Compliance", checker.check_g3()),
        ("G4 Release", checker.check_g4()),
        ("G5 Validation", checker.check_g5()),
    ]

    content_gates = [
        ("CG0 Strategy", checker.check_cg0()),
        ("CG1 Visual", checker.check_cg1()),
        ("CG2 Voice", checker.check_cg2()),
        ("CG3 Final Review", checker.check_cg3()),
        ("CG4 Distribution", checker.check_cg4()),
        ("CG5 Validation", checker.check_cg5()),
    ]

    pm_gates = [
        ("G0", checker.check_g0()),
        ("G1", checker.check_g1()),
        ("G2", checker.check_g2()),
        ("G3", checker.check_g3()),
        ("G4", checker.check_g4()),
        ("G5", checker.check_g5()),
        ("CG0", checker.check_cg0()),
        ("CG4", checker.check_cg4()),
        ("CG5", checker.check_cg5()),
    ]

    if args.track:
        # Filter to single track
        if args.track == "dev":
            content_gates = []
            pm_gates = []
        elif args.track == "content":
            dev_gates = []
            pm_gates = []
        elif args.track == "pm":
            dev_gates = []
            content_gates = []

    def count_passed(gates):
        return sum(1 for _, (status, _) in gates if status == "✅")

    dev_passed = count_passed(dev_gates)
    content_passed = count_passed(content_gates)
    pm_passed = count_passed(pm_gates)

    dev_pct = int(dev_passed / 5 * 100) if dev_passed < 6 else 100
    content_pct = int(content_passed / 5 * 100) if content_passed < 6 else 100
    pm_pct = int(pm_passed / 9 * 100)

    # Determine project name and tech stack
    project_name = "Unknown Project"
    tech_stack = "Not specified"
    if checker.l1:
        m = re.search(r"\*\*Project Goal:\*\*\s*(.+)", checker.l1)
        if m:
            project_name = m.group(1).strip()
        m = re.search(r"\*\*Tech Stack:\*\*\s*(.+)", checker.l1)
        if m:
            tech_stack = m.group(1).strip()

    # Find blocking items
    blockers = []
    for name, (status, detail) in dev_gates:
        if status == "⬜" and name in ("G4 Release",):
            blockers.append((name, detail))
    if checker.l2 and not checker._l2_has_business_goal():
        blockers.append(("G0", "Business Goal missing in L2-spec.md"))

    # Recommend next action
    recommendations = []
    if not checker.l2:
        recommendations.append("Run product-spec-builder Skill to create L2-spec.md")
    elif not checker.l3:
        recommendations.append("Run design-brief-builder Skill to create L3-design.md")
    elif not checker.l4:
        recommendations.append("Run dev-planner Skill to create L4-plan.md")
    elif not checker._history_has_review():
        recommendations.append("Run code-review Skill to unblock G3 Compliance")
    elif not checker.rollback:
        recommendations.append("Create ROLLBACK.md at project root to unblock G4 Release")
    elif not checker.release_notes:
        recommendations.append("Create RELEASE-NOTES.md to unblock G4 Release")
    else:
        recommendations.append("Project ready for release — run release-builder Skill")

    # ── Output ─────────────────────────────────────────────
    print(f"═══ Harness Status Board ═══")
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    print(f"Project: {project_name}")
    print(f"Tech Stack: {tech_stack}\n")

    print("┌─ Tracks ──────────────────────────────────────┐")
    print(f"│ dev     {progress_bar(dev_pct)} {dev_pct:>3}%  ({dev_passed}/{len(dev_gates)} Gates)   │")
    print(f"│ content {progress_bar(content_pct)} {content_pct:>3}%  ({content_passed}/{len(content_gates)} Gates)   │")
    print(f"│ pm      {progress_bar(pm_pct)} {pm_pct:>3}%  ({pm_passed}/{len(pm_gates)} Gates)   │")
    print("└───────────────────────────────────────────────┘")
    print()

    if dev_gates:
        print("Dev Track Gates:")
        for name, (status, detail) in dev_gates:
            print(f"  {status} {name:<15} {detail}")
        print()

    if content_gates:
        print("Content Track Gates:")
        for name, (status, detail) in content_gates:
            print(f"  {status} {name:<15} {detail}")
        print()

    if pm_gates:
        print("PM Track Gates:")
        for name, (status, detail) in pm_gates:
            print(f"  {status} {name:<15} {detail}")
        print()

    if blockers:
        print("Blocking Items:")
        for gate, detail in blockers:
            print(f"  ❌ [{gate}] {detail}")
        print()

    print("Next Recommended Action:")
    for rec in recommendations[:1]:
        print(f"  → {rec}")
    print()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
