#!/usr/bin/env python3
"""
Skill Router - Match user intent to the best Skill.
"""

import argparse
import sys
from pathlib import Path

SKILLS_DIR = Path(__file__).parent / "skills"

SKILL_INDEX = [
    {
        "name": "product-spec-builder",
        "triggers": ["idea", "spec", "requirement", "PRD", "scope", "what to build"],
    },
    {
        "name": "design-brief-builder",
        "triggers": ["design", "style", "theme", "color", "visual", "UI direction"],
    },
    {
        "name": "design-maker",
        "triggers": ["mockup", "figma", "prototype", "design file", "screen"],
    },
    {
        "name": "dev-planner",
        "triggers": ["plan", "phase", "roadmap", "tech stack", "architecture"],
    },
    {
        "name": "dev-builder",
        "triggers": ["implement", "build", "code", "develop", "feature", "task"],
    },
    {
        "name": "bug-fixer",
        "triggers": ["bug", "fix", "error", "crash", "broken", "failing test"],
    },
    {
        "name": "code-review",
        "triggers": ["review", "check code", "audit", "quality", "inspect"],
    },
    {
        "name": "release-builder",
        "triggers": ["release", "deploy", "publish", "ship", "build package"],
    },
]


def route(query: str) -> list[str]:
    query_lower = query.lower()
    scores = []
    for skill in SKILL_INDEX:
        score = sum(1 for t in skill["triggers"] if t.lower() in query_lower)
        if score > 0:
            scores.append((score, skill["name"]))
    scores.sort(reverse=True)
    return [name for _, name in scores[:3]]


def main() -> int:
    parser = argparse.ArgumentParser(description="Route user query to best Skill(s)")
    parser.add_argument("query", help="User intent description")
    args = parser.parse_args()

    matches = route(args.query)
    if not matches:
        print("No strong Skill match. Defaulting to: product-spec-builder")
        matches = ["product-spec-builder"]

    print("Top matches:")
    for m in matches:
        print(f"  - {m}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
