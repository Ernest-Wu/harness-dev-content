# Reliable Dev Harness

A product development harness that combines **Product-Manager-Skills** pedagogy with **毒舌产品经理 4.0** engineering discipline.

## Core Idea

> Vibe Coding fails not because models are dumb, but because there is no system around the model.

This harness provides:
- **Guides (前馈控制)**: 7 Skills that inject methodology and acceptance criteria before any code is written
- **Sensors (反馈控制)**: Deterministic hooks and exit-check scripts that physically block bad code from moving forward
- **Steering Loop (进化层)**: Feedback accumulates into proposals, but **humans must confirm** before rules change
- **Context Firewall (执行隔离)**: Every Sub-Agent task runs in a fresh instance with zero inherited context

## Quick Start

```bash
# 1. Verify harness health
python3 .claude/check-harness.py

# 2. Check a PRD before it reaches engineering
python3 scripts/check-prd.py docs/your-prd.md

# 3. Route a user request to the right Skill
python3 .claude/router.py "I want to build a writing tool"
```

## Architecture

```
.claude/
├── CLAUDE.md              # Orchestrator protocol (调度层)
├── skills/                # Guides (引导层)
│   ├── product-spec-builder/
│   ├── design-brief-builder/
│   ├── dev-planner/
│   ├── dev-builder/
│   ├── bug-fixer/
│   ├── code-review/
│   └── release-builder/
│   └── (each with exit-check.py deterministic gate)
├── hooks/                 # Sensors (检查层)
│   ├── pre-commit-check.sh
│   └── stop-gate.sh
├── state/                 # Hierarchical context (L1-L4)
├── feedback/              # Steering Loop inputs
├── docs/
│   ├── HARNESS-ARCHITECTURE.md
│   └── EVOLUTION-PROTOCOL.md
├── router.py              # Skill matcher
└── check-harness.py       # Infrastructure health check
```

## Key Design Decisions

1. **Every Skill has an exit-check.py**
   Natural language rules are unreliable. `exit-check.py` is a physical gate.

2. **Steering Loop has a Human Gate**
   `evolution-runner` may only generate proposals. It cannot directly modify Skill files.

3. **Design Mockup > Design Brief > Product Spec**
   Visual ambiguity kills UI quality. The mockup is the single source of truth.

4. **Sub-Agent Context Firewall**
   Each task is a fresh instance. State is passed through `.claude/state/` files only.

## Non-Negotiable Rules

- Exit Code ≠ 0 means **stop**. No exceptions.
- Code changes must pass `code-review` before commit.
- No automatic rule changes without human approval.
- UI changes must sync the design mockup.

## Credits

- **Product-Manager-Skills** (deanpeters) - Pedagogic-first skill design and standardization
- **毒舌产品经理 4.0** - Runtime harness architecture, Context Firewall, and Steering Loop
