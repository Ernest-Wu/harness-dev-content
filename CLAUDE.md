# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Workspace Overview

This workspace contains two complementary projects:

1. **`pm-skills/`** — The Product Manager Skills library (English). A catalog of 47 agent-ready PM skills plus 6 command workflows, built on the philosophy that skills should teach humans *and* execute for agents.
2. **`reliable-dev-harness/`** — The Reliable Dev Harness (中文/Chinese). A runtime engineering framework that enforces hard gates, context firewalls, and deterministic exit checks to make AI-driven software development reliable.

> **Key relationship:** `pm-skills` defines *how to write a great skill* (pedagogic-first). `reliable-dev-harness` defines *how to enforce that skill in real product development* (hard-gate execution). They are designed to work together.

---

## Common Commands

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
# Check harness health
python3 .claude/check-harness.py

# Run any skill's deterministic exit check
python3 .claude/skills/<skill-name>/exit-check.py

# Route a user request to the right Skill
python3 .claude/router.py "I want to build a writing tool"

# Check a PRD before it reaches engineering
python3 scripts/check-prd.py docs/your-prd.md
```

There is no top-level test suite for the harness; correctness is enforced per-skill via `exit-check.py` and per-phase via hook scripts in `.claude/hooks/`.

---

## High-Level Architecture

### `pm-skills/` — Pedagogic-First Skill Library

- **Primary format:** Markdown with YAML frontmatter (`name`, `description`, `intent`, `type`)
- **Skill anatomy:** Purpose → Key Concepts → Application → Examples → Common Pitfalls → References
- **Three skill types:** Component (templates/artifacts), Interactive (guided discovery with adaptive questions), Workflow (end-to-end processes)
- **Scripts layer:** Deterministic Python/Bash helpers in `scripts/` for validation, discovery, packaging, and catalog generation
- **Beta app:** Streamlit interface in `app/main.py` for local skill browsing and execution

**Critical design principle:** This repo is *pedagogic-first*. Stripping explanations, anti-patterns, or learning scaffolding to tighten copy is considered a defect, not an improvement. Skills must serve both human PMs (teaching) and AI agents (execution).

### `reliable-dev-harness/` — Hard-Gate Execution Framework

- **Five-layer architecture:** Orchestrator (you) → Sub-Agents → Skills → Sensors (Hooks/exit-check) → Steering Loop
- **Context Firewall:** Each Sub-Agent task uses a fresh instance; state is passed only through `.claude/state/` files (L1-summary.md, L2-spec.md, L3-design.md, L4-plan.md)
- **Physical gates:** Every skill has a deterministic `exit-check.py`. Exit code ≠ 0 means stop — no commit, no next phase, no exceptions
- **Two-stage code review:** Stage 1 (spec compliance) → Stage 2 (code quality). Stage 1 failures return to `dev-builder`; Stage 2 failures route to `bug-fixer` then re-review
- **Steering Loop safety:** `evolution-runner` may only generate proposals. It cannot directly modify `.claude/skills/` files. All rule changes require human confirmation
- **Visual authority chain:** Design mockups (Figma/Pencil) > `Design-Brief.md` > `Product-Spec.md`. UI changes must sync the design mockup

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
python3 .claude/check-harness.py
# Also manually run affected exit-check.py scripts
```
