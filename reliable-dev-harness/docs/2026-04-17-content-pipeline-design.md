# Content Pipeline Design for Reliable Dev Harness

> Date: 2026-04-17
> Status: Approved
> Approach: Dual-track (方案 B)

## 1. Background & Motivation

The Reliable Dev Harness was originally designed for AI-driven software development, with 8 skills covering the full lifecycle from product spec to release. Its core philosophy — Hard Gates, Context Firewall, Steering Loop — is valuable for any domain where AI needs to produce reliable output.

The `self-media-video` skill is an end-to-end pipeline for producing short videos from spoken scripts (口播稿). It has a well-structured 5-Gate process (G0-G4) but operates as a monolithic skill without the Harness's quality enforcement mechanisms.

**Key insight**: The Harness philosophy ("don't trust self-discipline, trust physical verification") applies equally to content production. The difference is what constitutes "verification" — in software, it's compilation and tests; in content, it's a mix of deterministic checks (file exists, format correct) and human judgment (does this look good?).

## 2. Design Decision: Dual-Track Architecture

**Chosen approach**: Keep the existing dev/ skills intact and add a content/ domain alongside it. Both share the Harness's core mechanisms (Context Firewall, Steering Loop, L1-L5 state management) but each has domain-appropriate Gate types.

**Why not rewrite** (方案 A): Discards working infrastructure. The dev/ skills are already usable.

**Why not start from scratch** (方案 C): Loses the Harness's accumulated wisdom on quality enforcement and evolution.

**Why not keep self-media-video as one skill**: Violates the Harness principle of "one Skill, one focused responsibility." Each content skill maps to a clear production phase with its own verification criteria.

## 3. Skill Decomposition

The self-media-video G0-G4 pipeline decomposes into 4 content skills:

### 3.1 script-writer (covers G0 + G1)

**Input**: Spoken script (Markdown) or topic description
**Output**: `state/L2-spec.md` (content spec) + `scenes.json` (scene breakdown)

**Hard Gate** (exit-check.py):
- scenes.json is valid JSON
- Each scene has `id`, `text`, `estimatedDuration`
- Scene count between 2 and 15
- `visualBeats` array exists (can be empty)

**Creative Gate** (human confirmation):
- Platform + style choice (G0)
- Scene breakdown approval (G1)

**SKILL.md must include**:
- Platform selection table (9:16, 16:9, 4:5)
- Mood Selection table (Impressed, Excited, Calm, Inspired)
- Scene parsing methodology from `parse-script.ts`
- Anti-pattern: do not extract headlines/bullets as forced layout templates

### 3.2 visual-designer (covers G2 + G3)

**Input**: scenes.json + L2-spec + L3-design
**Output**: `slides-preview.html` + image assets

**Key design**: visual-designer is an **orchestrator** that delegates HTML generation to the `frontend-slides` skill. It handles:
1. Image analysis and generation (which scenes need images, unified style)
2. Transforming scenes.json into frontend-slides input format
3. Post-processing: injecting platform-override CSS, beat animations, `data-beat-at` attributes

**Hard Gate** (exit-check.py):
- slides-preview.html exists and is valid HTML
- Contains `data-beat-at` attributes
- Platform override CSS is present
- Referenced image files exist

**Creative Gate** (human confirmation):
- 3 Style Preview selection (G2)
- Image batch approval (G2)
- Final HTML preview (G3)

**Relationship with frontend-slides**:
- frontend-slides handles: Mood Selection, 3 Style Previews, HTML generation, visual design quality
- visual-designer handles: scene→slide data transformation, video-specific constraints (platform CSS, beats), image generation and management
- frontend-slides does NOT need to know about "video" — it produces slides, visual-designer adapts them for video

### 3.3 tts-engine (covers G4a)

**Input**: scenes.json (text fields) + TTS style preset
**Output**: `audio/` directory (one .mp3 per scene) + `subtitles.json`

**Hard Gate** (exit-check.py):
- Audio file exists for each scene
- Audio duration > 0
- subtitles.json is valid (text + startMs + endMs per line)
- Total audio duration within 30% of estimated total duration

**Creative Gate** (human confirmation, configurable skip):
- TTS style selection (professional, casual, energetic, etc.)
- Pronunciation quality spot-check

**TTS preset table** (carried over from self-media-video):
| Preset | Style | Voice | Speed |
|--------|-------|-------|-------|
| 专业科普-女 | 清晰正式 | YunyangNeural | +0% |
| 专业科普-男 | 沉稳深度 | YunhaoNeural | -5% |
| 轻松闲聊-女 | 亲切活人感 | XiaoshuangNeural | +5% |
| ... | ... | ... | ... |

### 3.4 video-compositor (covers G4b)

**Input**: slides-preview.html + audio/ + subtitles.json + scenes.json
**Output**: Final video file (MP4)

**Hard Gate** (exit-check.py):
- base-video.mp4 exists and resolution matches platform spec
- Final video file exists and is playable (ffprobe check)
- Video duration within 5% of total audio duration
- fps ≥ 24

**Creative Gate** (human confirmation):
- Final video approval

**Remotion composition** (from self-media-video):
- KenBurnsVideo component for base video motion
- BeatOverlay for focus rings at beat timestamps
- Subtitles with typewriter + spring entrance animation
- TransitionSeries for scene transitions

## 4. Dual Gate Mechanism

### Hard Gate (Deterministic Verification)

Executed by `exit-check.py`. Binary pass/fail. No exceptions.

Philosophy: Only check what a machine can determine with certainty.
- File existence, format validity, numerical thresholds
- NOT: "is the video visually appealing", "is the narration natural"

### Creative Gate (Human Judgment Point)

Executed by the Orchestrator at skill transitions. Requires human input.

Philosophy: Check what requires aesthetic or editorial judgment.
- Style preference, scene pacing, pronunciation quality, visual satisfaction

**Rules**:
- Creative Gates are NOT skippable by default
- Each Creative Gate can be marked as "configurable skip" if the user trusts defaults
- User dissatisfaction at a Creative Gate → return to the corresponding Skill for re-execution (NOT to modify the previous Skill's output)

### Gate Placement in Pipeline

```
script-writer → [Hard Gate] → [Creative Gate: platform + scenes]
    ↓ pass
visual-designer:
  image step → [Creative Gate: image approval]
  HTML step → [Hard Gate] → [Creative Gate: HTML preview]
    ↓ pass
tts-engine → [Hard Gate] → [Creative Gate: TTS style (configurable skip)]
    ↓ pass
video-compositor → [Hard Gate] → [Creative Gate: final video]
    ↓ pass
Done → Output video
```

## 5. Directory Structure

```
.claude/
├── CLAUDE.md                          # Orchestrator protocol v2 (dual-domain routing)
├── router.py                          # Enhanced: dev/ + content/ dual routing
├── check-harness.py                   # Enhanced: check both domains
│
├── skills/
│   ├── dev/                           # Software development domain (existing)
│   │   ├── product-spec-builder/
│   │   ├── design-brief-builder/
│   │   ├── design-maker/
│   │   ├── dev-planner/
│   │   ├── dev-builder/
│   │   ├── bug-fixer/
│   │   ├── code-review/
│   │   └── release-builder/
│   │
│   └── content/                       # Content production domain (new)
│       ├── script-writer/
│       │   ├── SKILL.md
│       │   └── exit-check.py
│       ├── visual-designer/
│       │   ├── SKILL.md
│       │   ├── exit-check.py
│       │   └── templates/             # Video-specific templates
│       │       ├── platform-overrides/
│       │       ├── visual-beats/
│       │       ├── scene-layouts/
│       │       ├── lower-thirds/
│       │       ├── animation-presets/
│       │       └── slide-presets/
│       ├── tts-engine/
│       │   ├── SKILL.md
│       │   ├── exit-check.py
│       │   └── presets/                # TTS voice presets
│       └── video-compositor/
│           ├── SKILL.md
│           ├── exit-check.py
│           └── project-template/      # Remotion project template
│
├── hooks/
│   ├── pre-commit-check.sh            # Dev domain
│   ├── stop-gate.sh                    # Dev domain
│   └── content-validator.sh            # Content domain
│
├── agents/                             # Shared (IMPLEMENTER, REVIEWER, etc.)
│
├── state/                              # Extended
│   ├── L1-summary.md                   # Project overview
│   ├── L2-spec.md                      # Product spec (dev) / Content spec (content)
│   ├── L3-design.md                    # Design brief (dev) / Visual spec (content)
│   ├── L4-plan.md                      # Dev plan (dev) / Pipeline progress (content)
│   ├── L5-media.md                    # Media asset manifest (content)
│   └── task-history.yaml               # Shared
│
├── feedback/                           # Shared Steering Loop
│   └── FEEDBACK-INDEX.md
│
└── docs/
    ├── HARNESS-ARCHITECTURE.md          # Updated: dual-track
    ├── EVOLUTION-PROTOCOL.md            # Existing
    └── CONTENT-PIPELINE.md              # New: content production flow doc
```

## 6. State Management

| Level | File | Content Production Meaning | Size Control |
|-------|------|---------------------------|-------------|
| L1 | `state/L1-summary.md` | Project overview (video type, target platform, style tendency) | < 300 tokens |
| L2 | `state/L2-spec.md` | Content spec = summary version of scenes.json | < 2000 tokens |
| L3 | `state/L3-design.md` | Visual design spec (Mood, preset name, color tokens) | < 1500 tokens |
| L4 | `state/L4-plan.md` | Current pipeline progress (which Skill, which Gate pending) | < 1000 tokens |
| L5 | `state/L5-media.md` | Media asset manifest (image paths, audio paths, video paths) | As needed |

`scenes.json` is the direct output of script-writer, not a state file, but L2-spec.md references its key information.

## 7. Steering Loop Adaptation

Content production feedback follows different graduation thresholds than software development:

| Dimension | Software Development | Content Production |
|-----------|---------------------|-------------------|
| Graduation threshold | ≥ 3 same-type feedback | ≥ 5 same-type feedback |
| Reason | Objective rules emerge faster | Subjective preferences need more samples |
| Auto-propose | ✅ | ✅ |
| Auto-write | ❌ (human confirmation required) | ❌ (same) |

**Content-specific feedback patterns**:
- "场景切分太碎了" → Graduates to: script-writer minimum scene duration ≥ 15s
- "TTS 太机械" → Graduates to: tts-engine default voice preset rule
- "配图风格不搭" → Graduates to: visual-designer must include scene keywords in image prompts

## 8. Router Enhancement

```python
SKILL_INDEX = [
    # dev/ domain (existing)
    {"name": "dev/product-spec-builder", "triggers": ["idea", "spec", "requirement", "PRD"], "domain": "dev"},
    {"name": "dev/design-brief-builder", "triggers": ["design", "style", "theme", "color"], "domain": "dev"},
    {"name": "dev/design-maker", "triggers": ["mockup", "figma", "prototype"], "domain": "dev"},
    {"name": "dev/dev-planner", "triggers": ["plan", "phase", "roadmap"], "domain": "dev"},
    {"name": "dev/dev-builder", "triggers": ["implement", "build", "code", "feature"], "domain": "dev"},
    {"name": "dev/bug-fixer", "triggers": ["bug", "fix", "error", "crash"], "domain": "dev"},
    {"name": "dev/code-review", "triggers": ["review", "check code", "audit"], "domain": "dev"},
    {"name": "dev/release-builder", "triggers": ["release", "deploy", "publish"], "domain": "dev"},
    
    # content/ domain (new)
    {"name": "content/script-writer", "triggers": ["口播", "视频", "script", "场景", "scene", "短视频", "文稿"], "domain": "content"},
    {"name": "content/visual-designer", "triggers": ["配图", "风格", "Mood", "HTML预览", "style preview", "幻灯片"], "domain": "content"},
    {"name": "content/tts-engine", "triggers": ["配音", "TTS", "语音", "字幕", "语音合成", "narration"], "domain": "content"},
    {"name": "content/video-compositor", "triggers": ["渲染", "合成", "输出视频", "render", "Remotion", "视频输出"], "domain": "content"},
]
```

When router cannot determine domain, it asks the user.

## 9. Existing self-media-video Skill Migration

The existing `self-media-video` skill will be **retired** from the skill registry after migration. Its assets are distributed as follows:

| Asset | Destination |
|-------|------------|
| G0-G1 logic (platform selection, scene parsing) | `content/script-writer/SKILL.md` |
| G2 logic (image analysis, style selection) | `content/visual-designer/SKILL.md` |
| G3 logic (HTML generation) | Delegated to `frontend-slides` skill |
| G4a logic (TTS + subtitles) | `content/tts-engine/SKILL.md` |
| G4b logic (Remotion rendering) | `content/video-compositor/SKILL.md` |
| Templates (platform-overrides, visual-beats, etc.) | `content/visual-designer/templates/` |
| project-template (Remotion project) | `content/video-compositor/project-template/` |
| parse-script.ts | `content/script-writer/scripts/` |
| render-base-video.ts | `content/video-compositor/scripts/` |
| tts scripts | `content/tts-engine/scripts/` |
| Quality checklist | Referenced in each content Skill's SKILL.md |

## 10. Implementation Order

1. **Restructure directories** — Create content/ skill folders, migrate dev/ skills
2. **Write script-writer** — SKILL.md + exit-check.py (simplest, most self-contained)
3. **Write visual-designer** — SKILL.md + exit-check.py + template migration from self-media-video
4. **Write tts-engine** — SKILL.md + exit-check.py + TTS script migration
5. **Write video-compositor** — SKILL.md + exit-check.py + Remotion template migration
6. **Update router.py** — Add domain-aware routing
7. **Update check-harness.py** — Verify content/ skill completeness
8. **Update CLAUDE.md** — Dual-domain orchestrator protocol
9. **Update HARNESS-ARCHITECTURE.md** — Dual-track documentation
10. **Write CONTENT-PIPELINE.md** — Content production flow documentation
11. **Test end-to-end** — Run a full oral script through the pipeline

## 11. Open Questions (to resolve during implementation)

1. **frontend-slides integration**: How exactly does visual-designer invoke frontend-slides? As a subprocess? By loading the SKILL.md and following its instructions? This depends on the runtime environment (Claude Code vs. other agents).

2. **State templates**: L2-spec.md and L3-design.md need content-production-specific templates (currently they're empty or dev-focused).

3. **content-validator.sh hook**: Should it run automatically after each content Skill, or only before final video output?

4. **Multi-session resilience**: If the user closes their laptop during G3, how does the Orchestrator resume? The L4-plan.md should track pipeline progress.

5. **Reusable across video types**: The Skill decomposition allows future extensions (tutorials, product demos) by adding new skills to content/ without changing the pipeline structure.