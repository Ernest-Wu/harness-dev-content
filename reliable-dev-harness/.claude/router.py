#!/usr/bin/env python3
"""
Skill Router - Match user intent to the best Skill.
Supports dual-domain routing: dev/ and content/
"""

import argparse
import sys
from pathlib import Path

SKILLS_DIR = Path(__file__).parent / "skills"

SKILL_INDEX = [
    # dev/ domain (software development)
    {
        "name": "dev/product-spec-builder",
        "triggers": ["idea", "spec", "requirement", "PRD", "scope", "what to build"],
        "domain": "dev",
    },
    {
        "name": "dev/design-brief-builder",
        "triggers": ["design", "style", "theme", "color", "visual", "UI direction"],
        "domain": "dev",
    },
    {
        "name": "dev/design-maker",
        "triggers": ["mockup", "figma", "prototype", "design file", "screen"],
        "domain": "dev",
    },
    {
        "name": "dev/dev-planner",
        "triggers": ["plan", "phase", "roadmap", "tech stack", "architecture"],
        "domain": "dev",
    },
    {
        "name": "dev/dev-builder",
        "triggers": ["implement", "build", "code", "develop", "feature", "task"],
        "domain": "dev",
    },
    {
        "name": "dev/bug-fixer",
        "triggers": ["bug", "fix", "error", "crash", "broken", "failing test"],
        "domain": "dev",
    },
    {
        "name": "dev/code-review",
        "triggers": ["review", "check code", "audit", "quality", "inspect"],
        "domain": "dev",
    },
    {
        "name": "dev/release-builder",
        "triggers": ["release", "deploy", "publish", "ship", "build package"],
        "domain": "dev",
    },
    # content/ domain (content production)
    {
        "name": "content/script-writer",
        "triggers": [
            "口播",
            "视频",
            "script",
            "场景",
            "scene",
            "短视频",
            "文稿",
            "口播稿",
            "拆分场景",
        ],
        "domain": "content",
    },
    {
        "name": "content/visual-designer",
        "triggers": [
            "配图",
            "风格",
            "Mood",
            "HTML预览",
            "style preview",
            "幻灯片",
            "slides",
            "视觉设计",
            "出场动画",
        ],
        "domain": "content",
    },
    {
        "name": "content/tts-engine",
        "triggers": [
            "配音",
            "TTS",
            "语音",
            "字幕",
            "语音合成",
            "narration",
            "audio",
            "朗读",
        ],
        "domain": "content",
    },
    {
        "name": "content/video-compositor",
        "triggers": [
            "渲染",
            "合成",
            "输出视频",
            "render",
            "Remotion",
            "视频输出",
            "compositing",
            "MP4",
        ],
        "domain": "content",
    },
]


def route(query: str, domain: str | None = None) -> list[str]:
    """Route a user query to the best Skill(s).

    Args:
        query: User intent description
        domain: Optional domain filter ('dev' or 'content')
    """
    query_lower = query.lower()
    scores = []
    for skill in SKILL_INDEX:
        if domain and skill["domain"] != domain:
            continue
        score = sum(1 for t in skill["triggers"] if t.lower() in query_lower)
        if score > 0:
            scores.append((score, skill["name"], skill["domain"]))
    scores.sort(reverse=True)
    return [name for _, name, _ in scores[:3]]


def main() -> int:
    parser = argparse.ArgumentParser(description="Route user query to best Skill(s)")
    parser.add_argument("query", help="User intent description")
    parser.add_argument(
        "--domain",
        choices=["dev", "content"],
        help="Restrict routing to a specific domain",
    )
    args = parser.parse_args()

    matches = route(args.query, args.domain)
    if not matches:
        print("No strong Skill match. Defaulting to: dev/product-spec-builder")
        matches = ["dev/product-spec-builder"]

    print("Top matches:")
    for m in matches:
        skill_dir = SKILLS_DIR / m
        exists = "✓" if skill_dir.exists() else "✗"
        print(f"  {exists} {m}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
