# Workspace Guidelines — pm-demo1

This workspace contains two complementary projects:

1. **`pm-skills/`** — The Product Manager Skills library (English). A catalog of 47 agent-ready PM skills plus 6 command workflows, built on the philosophy that skills should teach humans *and* execute for agents.
2. **`reliable-dev-harness/`** — The Reliable Dev Harness (中文/Chinese). A runtime engineering framework that enforces hard gates, context firewalls, and deterministic exit checks to make AI-driven software development reliable.

> **Key relationship:** `pm-skills` defines *how to write a great skill* (pedagogic-first). `reliable-dev-harness` defines *how to enforce that skill in real product development* (hard-gate execution). They are designed to work together.

---

## Project Overview

### `pm-skills/` — Product Manager Skills Library
- **What it is:** A markdown-first library of battle-tested product management frameworks, formatted so both human PMs and AI agents can use them.
- **Current version:** v0.75 (March 2026)
- **License:** CC BY-NC-SA 4.0
- **Content:** 47 skills (21 component + 20 interactive + 6 workflow) and 6 reusable command workflows.
- **Technology stack:** Pure Markdown repository with Python helper scripts and an optional Streamlit (beta) playground.

### `reliable-dev-harness/` — Reliable Dev Harness
- **What it is:** An orchestration and execution framework that constrains AI agents with physical verification gates during software development.
- **Language:** Documentation and skills are written in Chinese.
- **Content:** 7+ dev skills (`product-spec-builder`, `design-brief-builder`, `dev-builder`, `dev-planner`, `code-review`, `bug-fixer`, `release-builder`), layered state files (L1-L4), hooks, and a steering-loop evolution protocol.
- **Technology stack:** Markdown + Python deterministic scripts (`exit-check.py`). No package manager or build system.

---

## Directory Structure

```
pm-demo1/
├── pm-skills/
│   ├── skills/                # 47 PM skills: skills/<name>/SKILL.md
│   ├── commands/              # 6 reusable multi-skill workflow commands
│   ├── catalog/               # Generated indexes (skills-by-type.md, commands.md, YAML indexes)
│   ├── scripts/               # Validation, discovery, packaging, and catalog generation scripts
│   ├── app/                   # Streamlit beta playground (main.py, requirements.txt, .env.example)
│   ├── docs/                  # Usage guides for Claude, Codex, ChatGPT, n8n, etc.
│   ├── research/              # Source essays and transcripts that inform skills
│   ├── examples/              # Good/bad example artifacts
│   ├── README.md              # Main project documentation
│   ├── CLAUDE.md              # Skill distillation protocol for Claude
│   ├── CONTRIBUTING.md        # Contributor guidelines
│   ├── PLANS.md               # Roadmap and future skill candidates
│   ├── AGENTS.md              # Subproject-specific agent guidelines
│   └── START_HERE.md          # 60-second onboarding
│
└── reliable-dev-harness/
    ├── .claude/
    │   ├── CLAUDE.md          # Orchestrator protocol (调度层)
    │   ├── docs/
    │   │   ├── HARNESS-ARCHITECTURE.md   # 五层架构说明书
    │   │   └── EVOLUTION-PROTOCOL.md     # Steering Loop 安全协议
    │   ├── skills/            # Dev skills with exit-check.py
    │   ├── hooks/             # Pre-commit and stop-gate sensors
    │   ├── agents/            # Sub-Agent role definitions
    │   ├── state/             # L1-L4 shared context files
    │   └── feedback/          # Feedback index for steering loop
    ├── examples/              # Example outputs or project seeds
    └── scripts/               # Harness automation scripts
```

---

## Technology Stack

### `pm-skills/`
- **Primary format:** Markdown with YAML frontmatter
- **Scripting:** Python 3 + Bash
- **Beta app:** Streamlit (`app/main.py`), with support for Anthropic, OpenAI, and Ollama providers
- **Dependencies (app only):** `streamlit>=1.32.0`, `anthropic>=0.40.0`, `openai>=1.40.0`, `pyyaml>=6.0`, `python-dotenv>=1.0.0`
- **No build system** for the core repository

### `reliable-dev-harness/`
- **Primary format:** Markdown (SKILL.md) + Python scripts (`exit-check.py`)
- **Scripting:** Python 3 + Bash
- **State management:** Plain-text files in `.claude/state/` (L1-summary.md, L2-spec.md, L3-design.md, L4-plan.md, task-history.yaml)
- **No build system, no package manager configuration**

---

## Build and Test Commands

### `pm-skills/`

Run these from inside `pm-skills/`:

```bash
# Validate the full library surface (metadata, triggers, commands, catalog freshness)
./scripts/test-library.sh

# Same, but include smoke tests
./scripts/test-library.sh --smoke

# Validate one skill
./scripts/test-a-skill.sh --skill <skill-name> --smoke

# Run the Streamlit beta app
cd app && pip install -r requirements.txt && streamlit run main.py

# Run a skill via CLI helper
./scripts/run-pm.sh skill <skill-name> "<scenario>"

# Run a command workflow via CLI helper
./scripts/run-pm.sh command <command-name> "<scenario>"

# Discover skills/commands
./scripts/find-a-skill.sh --keyword <term>
./scripts/find-a-command.sh --keyword <term>

# Generate upload-ready ZIPs for Claude web
./scripts/zip-a-skill.sh --skill <skill-name>
```

### `reliable-dev-harness/`

Run these from inside `reliable-dev-harness/`:

```bash
# Check harness health (if check-harness.py exists in the expected location)
python3 .claude/check-harness.py

# Run any skill's deterministic exit check
python3 .claude/skills/<skill-name>/exit-check.py
```

There is no top-level test suite for the harness; correctness is enforced per-skill via `exit-check.py` and per-phase via hook scripts in `.claude/hooks/`.

---

## Code Style and Conventions

### `pm-skills/`

- **Language:** English
- **File format:** Markdown with YAML frontmatter
- **Folder naming:** Lowercase kebab-case (e.g., `skills/user-story/`)
- **Frontmatter (required):** `name`, `description`, `type` (`component` | `interactive` | `workflow`)
- **Frontmatter (recommended):** `intent` (richer repo-facing explanation, separate from trigger-oriented `description`)
- **Standard sections (required):** Purpose, Key Concepts, Application, Examples, Common Pitfalls, References
- **Length limits for Claude web:** `name` ≤ 64 characters, `description` ≤ 200 characters
- **Skill folder name must match frontmatter `name` exactly**
- **Scripts inside skills** (optional) go in `skills/<name>/scripts/`, must be deterministic, avoid network calls, and be documented in the skill file
- **Pedagogic-first rule:** Do not strip explanations, anti-patterns, or examples to tighten copy. That is considered a defect, not an improvement.

### `reliable-dev-harness/`

- **Language:** Chinese (文档和 Skill 说明使用中文)
- **File format:** Markdown (`SKILL.md`) + Python (`exit-check.py`)
- **Core principle:** Every skill must have a deterministic `exit-check.py` that acts as a physical gate.
- **Context firewall:** Each Sub-Agent task uses a fresh instance; state is passed only through `.claude/state/` files.
- **Visual authority chain:** Design mockups (Figma/Pencil) > `Design-Brief.md` > `Product-Spec.md`
- **Evolution safety rule:** Auto-recording and auto-proposal are allowed; auto-writing to SKILL.md or exit-check.py is strictly forbidden without human approval.

---

## Testing Instructions

### `pm-skills/`

There are no automated unit tests for the markdown content. Validation is done via scripts:

1. **`check-skill-metadata.py`** — Validates frontmatter, required sections, and internal links.
2. **`check-skill-triggers.py`** — Audits description and scenario metadata for trigger-readiness.
3. **`check-command-metadata.py`** — Validates command files and their skill references.
4. **`test-a-skill.sh --smoke`** — Performs quick structural and content-quality checks on one skill.
5. **`test-library.sh`** — Runs the full surface check and regenerates catalogs.

Before submitting changes:
- Run `./scripts/test-library.sh` (or at least the relevant metadata check).
- Verify that any new skill is linked correctly in `catalog/`, `README.md`, and the appropriate index.
- For Streamlit changes, test `streamlit run app/main.py` locally.

### `reliable-dev-harness/`

Testing is gate-based rather than suite-based:

- **Every skill completion** must pass its own `exit-check.py`.
- **Every code change** must pass `code-review` (two-stage review) before proceeding.
- **Hooks** in `.claude/hooks/` provide additional deterministic checks (e.g., pre-commit).
- **Harness health** can be verified by running `.claude/check-harness.py` when present.

---

## Security Considerations

### `pm-skills/`
- **Least privilege:** Skills should not require secrets or network access unless explicitly documented.
- **Script safety:** Any `scripts/` inside a skill should be audited before running. They must be deterministic and avoid external network calls.
- **API keys:** The Streamlit app reads API keys only from environment variables (`app/.env.example` shows the expected variables). Never hardcode keys in the app or repository.
- **License:** CC BY-NC-SA 4.0 — non-commercial use with share-alike.

### `reliable-dev-harness/`
- **No auto-write to rules:** The steering loop (`evolution-runner`) is forbidden from directly modifying `.claude/skills/` files. All rule changes require human confirmation.
- **Deterministic gates only:** Quality checks must be script-based (`exit-check.py`, hooks), not LLM self-assessment.
- **Context isolation:** Sub-Agent instances must not inherit conversational context across tasks; all state must go through `.claude/state/` files.

---

## Cross-Repo Boundaries

- `pm-skills/` is the **shared reference library**. Treat it as read-only when supporting work whose primary target is `reliable-dev-harness/` or an external repo, unless explicitly asked to modify `pm-skills/` itself.
- `reliable-dev-harness/` is a **local execution harness**. Changes here should stay local to this workspace and should not leak Productside-specific content back into the shared `pm-skills/` library unless it has been generalized.

---

## Quick Reference: What to Run Before Commits

### If you changed `pm-skills/`:
```bash
cd pm-skills
./scripts/test-library.sh
```

### If you changed `reliable-dev-harness/`:
```bash
cd reliable-dev-harness
python3 .claude/check-harness.py   # if available
# Also manually run affected exit-check.py scripts
```

---

*This AGENTS.md is written for AI coding agents who have no prior knowledge of these projects. When in doubt, prefer physical verification (scripts, exit-checks, metadata validators) over assumption.*
