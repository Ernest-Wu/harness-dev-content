# Reliable Dev Harness

A dual-track product development harness combining spec-driven skill design with hard-gate engineering discipline. Supports both software development and content production workflows.

[中文文档](README-zh.md)

## Core Idea

> Vibe Coding fails not because models are dumb, but because there is no system around the model.

This harness provides:
- **Guides (前馈控制)**: Skills that inject methodology and acceptance criteria before any work begins
- **Sensors (反馈控制)**: Deterministic hooks and exit-check scripts that physically block bad output from moving forward
- **Steering Loop (进化层)**: Feedback accumulates into proposals, but **humans must confirm** before rules change
- **Context Firewall (执行隔离)**: Every Sub-Agent task runs in a fresh instance with zero inherited context

## Quick Start

### Step 1: Install in your project

```bash
# Option A: Copy directly (recommended for existing projects)
cp -r /path/to/harness-video-generator/.claude /your/project/

# Option B: Use the init script
cd /your/project
/path/to/harness-video-generator/scripts/init-harness.sh .

# Verify installation
python3 .claude/check-harness.py
# → ✅ Harness health check passed. Both dev/ and content/ domains are intact.
```

### Step 2: Use Dev Track (Software Development)

Start a conversation with Claude Code in your project. The Orchestrator reads `CLAUDE.md` and routes automatically:

```text
You: "I want to build a user authentication system"

Claude will:
  1. Route to dev/product-spec-builder → writes L2-spec
  2. Run exit-check.py → blocks if spec is incomplete
  3. You confirm the spec (Creative Gate)
  4. Route to dev/design-brief-builder → writes L3-design
  5. ... continues through dev-planner → dev-builder → code-review → release
  6. Each step: Hard Gate (exit-check.py) blocks bad output
```

**You do**: Confirm specs, make design decisions, review quality.
**Harness does**: Enforce flow, run validation, block incomplete work.

### Step 3: Use Content Track (Oral Video Production)

```text
You: "帮我把这个口播稿做成短视频"

Claude will:
  1. Route to content/script-writer → parses script → scenes.json
  2. Hard Gate: validates JSON structure
  3. Creative Gate: you confirm platform (9:16/16:9/4:5) + Mood + scene breakdown
  4. Route to content/visual-designer → generates HTML slides
  5. Creative Gate: you select style from 3 previews
  6. Route to content/tts-engine → generates audio + subtitles
  7. Route to content/video-compositor → renders final video
  8. Creative Gate: you approve the final video
```

**You do**: Choose platform/style, confirm scenes, approve quality.
**Harness does**: Generate assets, validate outputs, ensure pipeline consistency.

### Step 4: CLI Tools (optional)

```bash
# Check which skill a request routes to
python3 .claude/router.py "build login page"
# → dev/dev-builder

python3 .claude/router.py "制作口播视频" --domain content
# → content/script-writer

# Validate a content skill's output
python3 .claude/skills/content/script-writer/exit-check.py
# → ❌ [file_missing] scenes.json does not exist
# → ✅ script-writer exit check passed

# Health check
python3 .claude/check-harness.py
# → ✅ Harness health check passed
```

## Architecture

📊 [View Architecture Diagram](architecture.svg) | [Interactive Version](architecture.html)

```
.claude/
├── CLAUDE.md                          # Orchestrator protocol (three-domain + PM decision gates)
├── router.py                          # Skill matcher with --domain filter (dev/content/pm)
├── check-harness.py                   # Three-domain health check (dev + content + pm)
│
├── skills/
│   ├── dev/                           # Software development domain
│   │   ├── product-spec-builder/      #   PRD → L2-spec [G0 PM Discovery Gate]
│   │   ├── design-brief-builder/      #   Design brief → L3-design [G1 PM Direction Gate]
│   │   ├── design-maker/              #   Design mockup generation
│   │   ├── dev-planner/               #   Development planning → L4-plan [G2 PM Scope Gate]
│   │   ├── dev-builder/               #   Implementation
│   │   ├── bug-fixer/                 #   Bug resolution
│   │   ├── code-review/               #   Two-stage code review [G3 PM Compliance Gate + Spec Gap]
│   │   └── release-builder/           #   Release packaging [G4 PM Release Gate]
│   │
│   ├── content/                       # Content production domain
│   │   ├── script-writer/             #   口播文稿 → scenes.json + L2-spec [CG0]
│   │   ├── visual-designer/           #   Scene → HTML slides [CG1 Visual Direction Gate]
│   │   ├── tts-engine/                #   TTS → audio/ + subtitles.json [CG2 Voice Direction Gate - NOT skippable]
│   │   └── video-compositor/          #   Compositing → final video [CG3 Final Review Gate]
│   │
│   └── pm/                             # Product management decision domain
│       ├── validation/                 #   Post-launch PM validation [G5 PM Validation Gate]
│       ├── content-strategy/           #   Content strategy definition [CG0 PM Content Strategy Gate]
│       ├── distribution-planner/       #   Distribution planning [CG4 PM Distribution Gate]
│       └── content-validation/          #   Post-publish content validation [CG5 PM Content Validation Gate]
│
├── hooks/                              # Sensors (检查层)
│   ├── pre-commit-check.sh            #   Dev domain
│   ├── stop-gate.sh                   #   Dev domain
│   └── content-validator.sh           #   Content domain
│
├── state/                              # Hierarchical context (L0-L6)
│   ├── L0-strategy.md                #   Content Strategy (Business Goal, Audience, KPI)
│   ├── L1-summary.md                  #   Project overview (shared)
│   ├── L2-spec.md                     #   Dev: Product Spec / Content: Content Spec
│   ├── L3-design.md                   #   Dev: Design Brief / Content: Visual Spec
│   ├── L4-plan.md                     #   Dev: Dev Plan / Content: Pipeline Progress
│   ├── L5-media.md                   #   Content: Media Asset Manifest
│   └── L6-distribution.md             #   Distribution Plan (Platform, Timing, UTM, Compliance)
│
├── feedback/                           # Steering Loop inputs
├── agents/                             # Sub-Agent role definitions
│   ├── IMPLEMENTER.md
│   ├── REVIEWER.md
│   ├── FEEDBACK-OBSERVER.md           #   PM/Content/Dev feedback types (3-domain graduation)
│   └── EVOLUTION-RUNNER.md
│
└── docs/
    ├── HARNESS-ARCHITECTURE.md         #   Architecture documentation (three-domain)
    ├── EVOLUTION-PROTOCOL.md           #   Steering Loop protocol
    └── CONTENT-PIPELINE.md             #   Content production flow
```

## Three-Domain System

The harness now supports three domains, each with its own skill chain and gate types:

### Dev Track (Software Development)

```
idea → product-spec-builder → design-brief-builder → design-maker
  → dev-planner → dev-builder → code-review → release-builder
  → pm/validation (7/30 day post-launch)
  [Hard Gate: exit-check.py at each step]
  [PM Gates: G0→G1→G2→G3+G3b→G4→G5 with human decision points]
```

### Content Track (Oral Video Production)

```
script/topic → script-writer → visual-designer → tts-engine → video-compositor
  [Hard Gate: exit-check.py] + [Creative Gate: human confirmation]
  [PM Gates: CG0→CG1→CG2→CG3→CG4→CG5 with human decision points]
```

Content track uses **Dual Gates**: deterministic exit-check.py (Hard Gate) PLUS human judgment points (Creative Gate) for style, pacing, and quality decisions.

### PM Track (Product Management Decision Gates)

PM is a **cross-cutting decision layer** — not a parallel execution track, but a set of decision points that both Dev and Content tracks must pass through:

```
Dev Track:   idea → [G0] → [G1] → [G2] → [G3] → [G4] → [G5: pm/validation]
Content Track: topic → [CG0: pm/content-strategy] → [CG1] → [CG2] → [CG3] → [CG4: pm/distribution-planner] → [CG5: pm/content-validation]
                        ↑ PM横切决策层贯穿所有阶段 ↑
```

PM Skills provide **methodology and decision frameworks** at critical gates, ensuring both tracks make product decisions with rigor.

## Key Design Decisions

1. **Every Skill has an exit-check.py**
   Natural language rules are unreliable. `exit-check.py` is a physical gate.

2. **Steering Loop has a Human Gate**
   `evolution-runner` may only generate proposals. It cannot directly modify Skill files.

3. **Design Mockup > Design Brief > Product Spec** (dev track)
   Visual ambiguity kills UI quality. The mockup is the single source of truth.

4. **Hard Gate + Creative Gate** (content track)
   Deterministic checks (file exists, JSON valid) + human judgment (does this look good?). Creative Gates are not skippable by default.

5. **Sub-Agent Context Firewall**
   Each task is a fresh instance. State is passed through `.claude/state/` files only.

6. **Domain-Aware Routing**
   `router.py` supports `--domain dev|content` to restrict routing to a specific domain. When domain is ambiguous, the Orchestrator asks the user.

## Non-Negotiable Rules

- Exit Code ≠ 0 means **stop**. No exceptions.
- Code changes must pass `code-review` before commit.
- No automatic rule changes without human approval.
- UI changes must sync the design mockup.
- Creative Gates in content track are not skippable unless explicitly configured.
- Content Steering Loop threshold: ≥5 same-type feedback (vs dev ≥3).

## Credits

- **Product-Manager-Skills** (deanpeters) - Pedagogic-first skill design and standardization
- **self-media-video** - Content pipeline logic (migrated into content/ skills)