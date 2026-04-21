#!/usr/bin/env python3
"""
Task Package Generator — Auto-assemble Sub-Agent context packages.

Reads .claude/state/ files and the target SKILL.md, then generates
a filled Task Package following the CLAUDE.md template.

Usage:
    python3 .claude/package-task.py --skill dev/dev-builder --phase "Phase 2" --task "Implement login API"
    python3 .claude/package-task.py --skill content/script-writer --task "Generate script" --compact
    python3 .claude/package-task.py --skill pm/validation --output validation-package.md
"""

import argparse
import re
from datetime import datetime
from pathlib import Path
from typing import Optional

STATE_DIR = Path(".claude/state")
SKILLS_DIR = Path(".claude/skills")


def read_file(path: Path) -> Optional[str]:
    if not path.exists():
        return None
    return path.read_text(encoding="utf-8")


def extract_frontmatter(content: str) -> dict[str, str]:
    meta = {}
    match = re.search(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
    if not match:
        return meta
    for line in match.group(1).splitlines():
        line = line.strip()
        if ":" in line:
            key, _, value = line.partition(":")
            meta[key.strip()] = value.strip().strip('"').strip("'")
    return meta


def extract_section(content: str, heading: str) -> str:
    regex = re.compile(
        rf"^##\s+{re.escape(heading)}\s*\n(.*?)(?=^##\s|\Z)",
        re.MULTILINE | re.IGNORECASE | re.DOTALL,
    )
    match = regex.search(content)
    return match.group(1).strip() if match else ""


def extract_first_paragraph(content: str) -> str:
    lines = content.splitlines()
    paragraphs = []
    for line in lines:
        stripped = line.strip()
        if stripped and not stripped.startswith("#") and not stripped.startswith("---"):
            paragraphs.append(stripped)
        elif paragraphs:
            break
    return " ".join(paragraphs)[:300]


def truncate(text: str, max_len: int = 400) -> str:
    text = text.replace("\n", " ")
    if len(text) <= max_len:
        return text
    return text[: max_len - 3].rsplit(" ", 1)[0] + "..."


def get_l1_context() -> dict[str, str]:
    content = read_file(STATE_DIR / "L1-summary.md") or ""
    result = {
        "project_goal": "[Not set]",
        "target_user": "[Not set]",
        "tech_stack": "[Not set]",
        "current_phase": "[Not set]",
        "next_task": "[Not set]",
    }
    m = re.search(r"\*\*Project Goal:\*\*\s*(.+)", content)
    if m:
        result["project_goal"] = m.group(1).strip()
    m = re.search(r"\*\*Target User:\*\*\s*(.+)", content)
    if m:
        result["target_user"] = m.group(1).strip()
    m = re.search(r"\*\*Tech Stack:\*\*\s*(.+)", content)
    if m:
        result["tech_stack"] = m.group(1).strip()
    m = re.search(r"\*\*Current Active Phase:\*\*\s*(.+)", content)
    if m:
        result["current_phase"] = m.group(1).strip()
    m = re.search(r"\*\*Next Task:\*\*\s*(.+)", content)
    if m:
        result["next_task"] = m.group(1).strip()
    return result


def get_l2_summary(domain: str) -> dict[str, str]:
    if domain == "content":
        content = read_file(STATE_DIR / "L2-content-spec.md") or ""
    else:
        content = read_file(STATE_DIR / "L2-spec.md") or ""

    result = {"exists": bool(content), "business_goal": "[Not found]", "p0_features": "[Not found]"}
    if not content:
        return result

    bg = extract_section(content, "Business Goal")
    if bg:
        result["business_goal"] = truncate(bg, 200)

    # Extract P0 features
    p0_section = extract_section(content, "P0")
    if not p0_section:
        p0_section = extract_section(content, "Core Features")
    if p0_section:
        features = re.findall(r"^[-*]\s+(.+)$", p0_section, re.MULTILINE)
        if features:
            result["p0_features"] = "\n".join(f"  - {f[:80]}" for f in features[:5])
        else:
            result["p0_features"] = truncate(p0_section, 300)

    return result


def get_l3_summary() -> dict[str, str]:
    content = read_file(STATE_DIR / "L3-design.md") or ""
    if not content:
        return {"exists": False, "summary": "[Not found]"}
    # Try to extract key design decisions
    tokens = extract_section(content, "Design Tokens")
    brand = extract_section(content, "Brand")
    summary = ""
    if tokens:
        summary += f"Design tokens: {truncate(tokens, 150)}"
    if brand:
        summary += f" | Brand: {truncate(brand, 100)}"
    if not summary:
        summary = truncate(extract_first_paragraph(content), 250)
    return {"exists": True, "summary": summary or "[Present but no summary extracted]"}


def get_l4_summary(phase: str) -> dict[str, str]:
    content = read_file(STATE_DIR / "L4-plan.md") or ""
    result = {"exists": bool(content), "phase_goal": "[Not found]", "risks": "[Not found]"}
    if not content:
        return result

    bg = extract_section(content, "Business Goal")
    if bg:
        result["phase_goal"] = truncate(bg, 200)

    risks = extract_section(content, "Risk Flags")
    if risks:
        risk_items = re.findall(r"^\s*-\s*\[(.)\]\s*(.+)$", risks, re.MULTILINE)
        if risk_items:
            result["risks"] = "\n".join(f"  - [{s}] {d[:60]}" for s, d in risk_items[:3])
        else:
            result["risks"] = truncate(risks, 200)

    return result


def get_skill_info(skill_path: str) -> dict[str, str]:
    skill_file = SKILLS_DIR / skill_path / "SKILL.md"
    content = read_file(skill_file)
    if not content:
        return {"exists": False, "name": skill_path, "description": "[SKILL.md not found]", "application": ""}

    fm = extract_frontmatter(content)
    app = extract_section(content, "Application")
    return {
        "exists": True,
        "name": fm.get("name", skill_path),
        "description": fm.get("description", "[No description]"),
        "application": app,
    }


def infer_role(skill_path: str, skill_name: str) -> str:
    mapping = {
        "dev-builder": "implementer",
        "code-review": "code-reviewer",
        "bug-fixer": "implementer",
        "product-spec-builder": "pm-validator",
        "design-brief-builder": "pm-validator",
        "dev-planner": "pm-validator",
        "release-builder": "pm-validator",
        "script-writer": "content-strategist",
        "visual-designer": "content-strategist",
        "tts-engine": "content-strategist",
        "video-compositor": "content-strategist",
        "frontend-slides": "content-strategist",
        "validation": "pm-validator",
        "content-strategy": "pm-validator",
        "distribution-planner": "pm-validator",
        "content-validation": "pm-validator",
    }
    for key, role in mapping.items():
        if key in skill_path:
            return role
    return "implementer"


def get_pm_checkpoints(skill_path: str, domain: str) -> str:
    checkpoints = []
    skill_name = skill_path.split("/")[-1]

    if domain == "dev" or skill_name in ("validation",):
        if "product-spec-builder" in skill_path:
            checkpoints.append("- G0 PM Discovery Gate: Feature selection, Scope boundary, MVP definition")
        elif "design-brief-builder" in skill_path:
            checkpoints.append("- G1 PM Direction Gate: Design direction aligns with business goal")
        elif "dev-planner" in skill_path:
            checkpoints.append("- G2 PM Scope Gate: Phase order reflects business priority, MVP confirmed")
        elif "dev-builder" in skill_path:
            checkpoints.append("- G3 PM Compliance Gate: Implementation must match spec; no scope creep")
        elif "release-builder" in skill_path:
            checkpoints.append("- G4 PM Release Gate: Go/No-Go decision required; verify rollback plan")
        elif "validation" in skill_path:
            checkpoints.append("- G5 PM Validation Gate: Compare metrics to spec targets; GO/PIVOT/KILL decision")
        elif "code-review" in skill_path:
            checkpoints.append("- G3 PM Compliance Gate: Stage 1 = Spec compliance (PM is PRIMARY reviewer)")

    if domain == "content" or skill_name in ("content-strategy", "distribution-planner", "content-validation"):
        l0_exists = (STATE_DIR / "L0-strategy.md").exists()
        if "content-strategy" in skill_path:
            checkpoints.append("- CG0 PM Content Strategy Gate: Audience definition, Business Goal, KPI targets, Differentiation strategy")
        elif "script-writer" in skill_path and not l0_exists:
            checkpoints.append("- ⚠️ CG0 PM Content Strategy Gate: L0-strategy.md not found — recommend running pm/content-strategy first")
        elif "script-writer" in skill_path:
            checkpoints.append("- CG0 PM Content Strategy Gate: Verify audience and KPI alignment from L0-strategy.md")
        elif "visual-designer" in skill_path or "frontend-slides" in skill_path:
            checkpoints.append("- CG1 PM Visual Direction Gate: Brand consistency and accessibility check")
        elif "tts-engine" in skill_path:
            checkpoints.append("- CG2 PM Voice Direction Gate: Voice brand confirmation (NOT skippable)")
        elif "video-compositor" in skill_path:
            checkpoints.append("- CG3 PM Final Review Gate: Core message delivery, CTA effectiveness")
        elif "distribution-planner" in skill_path:
            checkpoints.append("- CG4 PM Distribution Gate: Platform metadata, UTM tracking, copyright")
        elif "content-validation" in skill_path:
            checkpoints.append("- CG5 PM Content Validation Gate: KPI achievement, iteration decision")

    if not checkpoints:
        checkpoints.append("- No PM gate checkpoints for this skill")

    return "\n".join(checkpoints)


def generate_package(skill_path: str, phase: str, task: str, compact: bool) -> str:
    domain = skill_path.split("/")[0] if "/" in skill_path else "dev"
    skill = get_skill_info(skill_path)
    l1 = get_l1_context()
    l2 = get_l2_summary(domain)
    l3 = get_l3_summary()
    l4 = get_l4_summary(phase)
    role = infer_role(skill_path, skill["name"])
    pm_checks = get_pm_checkpoints(skill_path, domain)

    objective = task if task else skill["description"]

    if compact:
        return f"""# Task Package (Compact)

**Role:** {role}
**Skill:** {skill_path}
**Objective:** {objective}

**L1:** {l1['project_goal']} | Phase: {phase or l1['current_phase']} | Stack: {l1['tech_stack']}
**L2:** {l2['business_goal'][:80]}
**L3:** {'Present' if l3['exists'] else 'Missing'}
**L4:** {l4['phase_goal'][:80]}

**PM Checks:**
{pm_checks}

**Constraints:** Run `python3 .claude/skills/{skill_path}/exit-check.py` before claiming done.
"""

    l2_file = 'L2-content-spec.md' if domain == 'content' else 'L2-spec.md'
    l3_status = '(✓ present)' if l3['exists'] else '(⬜ not found)'
    l4_status = '(✓ present)' if l4['exists'] else '(⬜ not found)'
    p0_block = l2['p0_features'] if l2['p0_features'] != '[Not found]' else 'P0 Features: [Not extracted]'
    app_block = truncate(skill['application'], 500) if skill['application'] else '[Application section not extracted]'
    state_count = sum([l2['exists'], l3['exists'], l4['exists']]) + 1

    return f"""# Task Package

## Role
{role}

## Objective
{objective}

## L1 Context (Must Read)
- 项目目标：{l1['project_goal']}
- 当前 Phase：{phase or l1['current_phase']}
- 本次 Task 交付项：{task or l1['next_task']}
- 技术栈：{l1['tech_stack']}

## L2-L4 References (Read on Demand)
- Product-Spec / Content-Spec: `.claude/state/{l2_file}`
  - Business Goal: {l2['business_goal']}
  - P0 Features:
{p0_block}
- Design-Brief / Visual-Spec: `.claude/state/L3-design.md` {l3_status}
  - {l3['summary']}
- DEV-PLAN / Pipeline-Progress: `.claude/state/L4-plan.md` {l4_status}
  - Phase Business Goal: {l4['phase_goal']}
  - Risk Flags: {l4['risks']}

## Active Skill
**{skill['name']}** — {skill['description']}

{app_block}

## Constraints
- 禁止修改与本次 Task 无关的文件
- 每完成一个文件修改，必须能解释为什么
- 完成后必须运行 `python3 .claude/skills/{skill_path}/exit-check.py`
- exit-check 通过前，禁止声称"完成"

## PM 横切核对点
{pm_checks}

---
Generated by package-task.py at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Skill: {skill_path} | Phase: {phase or l1['current_phase']} | State files: {state_count}/4 loaded
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate Sub-Agent Task Package")
    parser.add_argument("--skill", required=True, help="Skill path, e.g. dev/dev-builder")
    parser.add_argument("--phase", default="", help="Current phase, e.g. 'Phase 2'")
    parser.add_argument("--task", default="", help="Task description")
    parser.add_argument("--output", default="", help="Output file path (default: stdout)")
    parser.add_argument("--compact", action="store_true", help="Compact mode for chat paste")
    args = parser.parse_args()

    if not (SKILLS_DIR / args.skill / "SKILL.md").exists():
        print(f"❌ Skill not found: {SKILLS_DIR / args.skill}")
        print(f"   Available skills under {SKILLS_DIR}:")
        for domain in ["dev", "content", "pm"]:
            domain_dir = SKILLS_DIR / domain
            if domain_dir.exists():
                for s in sorted(domain_dir.iterdir()):
                    if s.is_dir() and (s / "SKILL.md").exists():
                        print(f"     {domain}/{s.name}")
        return 1

    package = generate_package(args.skill, args.phase, args.task, args.compact)

    if args.output:
        Path(args.output).write_text(package, encoding="utf-8")
        print(f"✅ Task Package written to {args.output}")
        print(f"   Skill: {args.skill} | Phase: {args.phase or 'N/A'} | Mode: {'compact' if args.compact else 'full'}")
    else:
        print(package)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
