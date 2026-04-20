#!/usr/bin/env python3
"""
Skill Router - Match user intent to the best Skill.
Supports three-domain routing: dev/, content/, and pm/
"""

import argparse
import re
import sys
from pathlib import Path
from typing import List, Optional

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
        "name": "content/frontend-slides",
        "triggers": [
            "HTML slides",
            "slide design",
            "slide style",
            "mood selection",
            "style preview",
            "幻灯片设计",
            "风格预览",
            "mood",
            "slide layout",
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
    # pm/ domain (product management decision gates)
    {
        "name": "pm/validation",
        "triggers": [
            "validate",
            "validation",
            "post-launch",
            "metrics review",
            "GO",
            "PIVOT",
            "KILL",
            "验证",
            "效果验证",
            "指标复查",
            "产品验证",
            "上线后验证",
            "go/no-go",
            "7-day",
            "30-day",
        ],
        "domain": "pm",
    },
    {
        "name": "pm/content-strategy",
        "triggers": [
            "content strategy",
            "内容策略",
            "audience targeting",
            "KPI definition",
            "CG0",
            "target audience",
            "differentiation",
            "差异化",
            "目标受众",
        ],
        "domain": "pm",
    },
    {
        "name": "pm/distribution-planner",
        "triggers": [
            "distribution",
            "publishing",
            "UTM",
            "platform metadata",
            "分发",
            "发布计划",
            "platform strategy",
            "CG4",
            "SEO",
            "分发策略",
        ],
        "domain": "pm",
    },
    {
        "name": "pm/content-validation",
        "triggers": [
            "content performance",
            "content KPI",
            "content review",
            "ITERATE",
            "REFRESH",
            "RETIRE",
            "内容验证",
            "内容效果",
            "CG5",
            "post-publish review",
            "内容指标",
        ],
        "domain": "pm",
    },
]


def route(query: str, domain: Optional[str] = None) -> List[str]:
    """Route a user query to the best Skill(s).

    Args:
        query: User intent description
        domain: Optional domain filter ('dev', 'content', or 'pm')
    """
    query_lower = query.lower()
    # Tokenize query for exact-word matching bonus
    query_tokens = set(re.findall(r"[a-z0-9\u4e00-\u9fff]+", query_lower))
    scores = []
    for skill in SKILL_INDEX:
        if domain and skill["domain"] != domain:
            continue
        score = 0
        for t in skill["triggers"]:
            t_lower = t.lower()
            if t_lower in query_lower:
                # Base score for substring match
                score += 1
                # Bonus for exact token match (reduces false positives)
                if t_lower in query_tokens:
                    score += 1
        if score > 0:
            scores.append((score, skill["name"], skill["domain"]))
    scores.sort(reverse=True)
    return [name for _, name, _ in scores[:3]]


def main() -> int:
    parser = argparse.ArgumentParser(description="Route user query to best Skill(s)")
    parser.add_argument("query", help="User intent description")
    parser.add_argument(
        "--domain",
        choices=["dev", "content", "pm"],
        help="Restrict routing to a specific domain",
    )
    args = parser.parse_args()

    matches = route(args.query, args.domain)
    if not matches:
        print("⚠ No strong Skill match found.")
        print(
            "  Consider specifying a domain with --domain dev, --domain content, or --domain pm."
        )
        print("  Or rephrase your query with more specific keywords.")
        return 1

    print("Top matches:")
    for m in matches:
        skill_dir = SKILLS_DIR / m
        exists = "✓" if skill_dir.exists() else "✗"
        print(f"  {exists} {m}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
