#!/usr/bin/env python3
"""
Exit Check: product-spec-builder
Deterministic compliance checker for Product Spec outputs.
"""

import re
import sys
from pathlib import Path
from typing import Optional

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from _utils.exit_check_base import add_issue, print_and_exit, ensure_project_root

SPEC_PATH = Path(".claude/state/L2-spec.md")
L0_STRATEGY = Path(".claude/state/L0-strategy.md")

REQUIRED_SECTIONS = [
    ("problem", r"Problem\s+Statement|问题陈述|背景"),
    ("user", r"Target\s+User|目标用户|用户画像"),
    ("features", r"Core\s+Features|核心功能|功能列表"),
    ("metrics", r"Success\s+Metrics|成功指标|验收标准|Metrics"),
    ("scope", r"Scope|范围|In\s+Scope|Out\s+of\s+Scope"),
]

QUANTIFIER_RE = re.compile(
    r"\d+%?|\d+\s*(days?|weeks?|months?|hours?|minutes?)"
    r"|提升|降低|减少|增加|baseline|target|from\s+\d",
    re.IGNORECASE,
)


def check():
    if not SPEC_PATH.exists():
        add_issue("file_missing", f"{SPEC_PATH} does not exist.", level="high")
        return

    text = SPEC_PATH.read_text(encoding="utf-8")
    lines = text.splitlines()

    # 1. Required sections
    for code, pattern in REQUIRED_SECTIONS:
        if not any(
            re.search(rf"^##\s+.*{pattern}.*$", line, re.IGNORECASE) for line in lines
        ):
            add_issue(
                f"section_missing:{code}",
                f"Missing required section matching: {pattern}. "
                f"Downstream Agents will have no execution baseline.",
                level="high",
            )

    # 2. Metrics must be quantified
    metrics_section = extract_section(
        text, r"Success\s+Metrics|成功指标|验收标准|Metrics"
    )
    if metrics_section and not QUANTIFIER_RE.search(metrics_section):
        add_issue(
            "metrics_not_quantified",
            "Success Metrics contains no numbers, percentages, or time units. "
            "'Improve productivity' is not a metric. 'Increase weekly output from 2000 to 2500 words within 30 days' is.",
            level="high",
        )

    # 3. Scope must have Out-of-Scope
    scope_section = extract_section(text, r"Scope|范围")
    if scope_section:
        if not re.search(
            r"Out\s+of\s+[Ss]cope|不在范围|排除|Not\s+included",
            scope_section,
            re.IGNORECASE,
        ):
            add_issue(
                "scope_boundary_missing",
                "No explicit Out-of-Scope found. Scope creep is guaranteed.",
                level="high",
            )

    # 4. Length check
    body = text.split("---", 2)[-1] if text.startswith("---") else text
    if len(body.strip()) < 400:
        add_issue(
            "spec_too_short",
            f"Body is only {len(body.strip())} chars. A usable spec needs at least 400 chars to constrain downstream Agents.",
            level="high",
        )

    # 5. Must not be marketing fluff
    fluff_words = [
        "revolutionize",
        "disrupt",
        "leverage",
        "synergy",
        "transform",
        "ecosystem",
    ]
    found_fluff = [w for w in fluff_words if w.lower() in body.lower()]
    if found_fluff:
        add_issue(
            "marketing_fluff_detected",
            f"Spec contains buzzwords: {', '.join(found_fluff)}. This is an execution contract, not a pitch deck.",
            level="warning",
        )

    # ── PM Decision Quality Checks (warning level) ─────────────
    check_decision_quality(text)

    # ── L0→L2 Traceability Checks ─────────────────────────────
    check_l0_l2_alignment(text)


STOPWORDS = frozenset({
    "the", "a", "an", "is", "are", "was", "were", "be", "been", "being",
    "of", "and", "or", "to", "in", "for", "with", "on", "at", "by", "from",
    "as", "it", "its", "this", "that", "these", "those", "i", "we", "you",
    "they", "them", "their", "our", "my", "your", "his", "her", "has", "have",
    "had", "do", "does", "did", "will", "would", "could", "should", "may",
    "might", "can", "shall", "的", "了", "在", "是", "和", "或", "与", "有",
    "为", "对", "到", "从", "等", "及", "将", "以", "并", "中", "上", "下",
})


# Common short technical terms that should be treated as keywords
EXTRA_SHORT = frozenset({"ai", "ux", "ui", "ar", "vr", "kpi", "okr", "cta", "tts", "api", "id", "qa", "pwa", "sdk", "mvp"})


def extract_keywords(text: str) -> set[str]:
    """Extract meaningful keywords from text (English words + Chinese chars)."""
    words = re.findall(r"[a-zA-Z]{2,}", text.lower())
    chars = re.findall(r"[\u4e00-\u9fff]{2,}", text)
    return (set(words) | set(chars)) - STOPWORDS


def extract_section_content(text: str, heading: str) -> str:
    """Extract content under a specific ## heading."""
    pattern = rf"^##\s+{re.escape(heading)}\s*\n(.*?)(?=^##\s|\Z)"
    match = re.search(pattern, text, re.MULTILINE | re.IGNORECASE | re.DOTALL)
    return match.group(1).strip() if match else ""


def check_l0_l2_alignment(spec_content: str):
    """Verify L0-strategy.md content is reflected in L2-spec.md."""
    if not L0_STRATEGY.exists():
        return

    l0_content = L0_STRATEGY.read_text(encoding="utf-8")

    # 1. Business Goal alignment
    l0_bg = extract_section_content(l0_content, "Business Goal")
    l2_bg = extract_section_content(spec_content, "Business Goal")

    if l0_bg and l2_bg:
        l0_kw = extract_keywords(l0_bg)
        l2_kw = extract_keywords(l2_bg)
        if l0_kw and not (l0_kw & l2_kw):
            add_issue(
                "l0_l2_business_goal_gap",
                "L0-strategy.md defines Business Goal but L2-spec.md's Business Goal "
                "shares no substantive keywords with it. CG0 traceability requires alignment.",
                level="warning",
            )
    elif l0_bg and not l2_bg:
        add_issue(
            "l2_missing_business_goal",
            "L0-strategy.md has Business Goal but L2-spec.md does not. "
            "CG0 requires strategic intent to flow into product spec.",
            level="warning",
        )

    # 2. Target Audience alignment
    l0_audience = extract_section_content(l0_content, "Target Audience")
    if l0_audience:
        l2_user = extract_section_content(spec_content, "Target User")
        if not l2_user:
            l2_user = extract_section_content(spec_content, "用户画像")
        if l2_user:
            l0_kw = extract_keywords(l0_audience)
            l2_kw = extract_keywords(l2_user)
            if l0_kw and not (l0_kw & l2_kw):
                add_issue(
                    "l0_l2_audience_gap",
                    "L0-strategy.md defines Target Audience but L2-spec.md's Target User "
                    "shares no substantive keywords with it. CG0 traceability requires audience alignment.",
                    level="warning",
                )
        else:
            add_issue(
                "l2_missing_target_user",
                "L0-strategy.md has Target Audience but L2-spec.md has no Target User section. "
                "CG0 requires audience alignment.",
                level="warning",
            )

    # 3. KPI alignment
    l0_kpi = extract_section_content(l0_content, "KPI")
    if l0_kpi:
        l2_metrics = extract_section_content(spec_content, "Success Metrics")
        l0_kw = extract_keywords(l0_kpi)
        l2_kw = extract_keywords(l2_metrics)
        if l0_kw and not (l0_kw & l2_kw):
            add_issue(
                "l0_l2_kpi_gap",
                "L0-strategy.md defines KPI but L2-spec.md's Success Metrics "
                "shares no substantive keywords with it. CG0 traceability requires KPI alignment.",
                level="warning",
            )


def check_decision_quality(spec_content):
    if not re.search(
        r"P[0-2]|优先级|priority|MVP|Must Have", spec_content, re.IGNORECASE
    ):
        add_issue(
            "features_not_prioritized",
            "Core Features lack priority ranking (P0/P1/P2 or Must/Should/Nice). "
            "Without prioritization, downstream Agents cannot distinguish MVP from nice-to-have.",
            level="warning",
        )

    if not re.search(r"假设|assumption|hypothesis", spec_content, re.IGNORECASE):
        add_issue(
            "no_stated_assumptions",
            "Spec has no stated assumptions. Consider using discovery-interview-prep "
            "to validate key assumptions before committing to implementation.",
            level="warning",
        )

    if not re.search(
        r"MVP|最小可行|v1|phase.?0|Must Have", spec_content, re.IGNORECASE
    ):
        add_issue(
            "no_mvp_boundary",
            "No MVP boundary defined. Which features must ship in Phase 0? "
            "Without this, scope creep is guaranteed.",
            level="warning",
        )

    if not re.search(
        r"业务目标|business.goal|Business Goal|objective|OKR",
        spec_content,
        re.IGNORECASE,
    ):
        add_issue(
            "no_business_goal",
            "Spec lacks a Business Goal link. Success Metrics should tie to company strategy, "
            "not just product-level numbers.",
            level="warning",
        )


def extract_section(text: str, pattern: str) -> Optional[str]:
    non_capturing = re.sub(r"\((?!\?)", "(?:", pattern)
    regex = re.compile(
        rf"^##\s+.*{non_capturing}.*$\n?(.*?)(?=^##\s|\Z)",
        re.MULTILINE | re.IGNORECASE | re.DOTALL,
    )
    match = regex.search(text)
    return match.group(1) if match else None


def main() -> int:
    ensure_project_root()
    check()
    print_and_exit("Product Spec")


if __name__ == "__main__":
    raise SystemExit(main())
