# Content Pipeline Dual-Track Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Transform reliable-dev-harness from a dev-only framework into a dual-track system supporting both software development and content production (oral video pipeline).

**Architecture:** Keep existing 8 dev/ skills intact under `dev/` subdirectory. Add 4 new content/ skills (script-writer, visual-designer, tts-engine, video-compositor) that follow the same SKILL.md + exit-check.py pattern but with dual-gate mechanism (Hard Gate + Creative Gate). Enhance router, check-harness, and CLAUDE.md for domain-aware routing.

**Tech Stack:** Python 3 (exit-check.py, router.py, check-harness.py), Markdown (SKILL.md), Bash (hooks), YAML (state files)

---

## File Structure Map

Files to be created or modified in this plan:

| # | Action | Path | Responsibility |
|---|--------|------|---------------|
| 1 | Move | `.claude/skills/product-spec-builder/` → `.claude/skills/dev/product-spec-builder/` | Directory restructure |
| 2 | Move | `.claude/skills/design-brief-builder/` → `.claude/skills/dev/design-brief-builder/` | Directory restructure |
| 3 | Move | `.claude/skills/design-maker/` → `.claude/skills/dev/design-maker/` | Directory restructure |
| 4 | Move | `.claude/skills/dev-planner/` → `.claude/skills/dev/dev-planner/` | Directory restructure |
| 5 | Move | `.claude/skills/dev-builder/` → `.claude/skills/dev/dev-builder/` | Directory restructure |
| 6 | Move | `.claude/skills/bug-fixer/` → `.claude/skills/dev/bug-fixer/` | Directory restructure |
| 7 | Move | `.claude/skills/code-review/` → `.claude/skills/dev/code-review/` | Directory restructure |
| 8 | Move | `.claude/skills/release-builder/` → `.claude/skills/dev/release-builder/` | Directory restructure |
| 9 | Create | `.claude/skills/content/script-writer/SKILL.md` | Script writing methodology |
| 10 | Create | `.claude/skills/content/script-writer/exit-check.py` | Scenes.json validation gate |
| 11 | Create | `.claude/skills/content/script-writer/scripts/` | Migrated from self-media-video |
| 12 | Create | `.claude/skills/content/visual-designer/SKILL.md` | Visual orchestration methodology |
| 13 | Create | `.claude/skills/content/visual-designer/exit-check.py` | HTML preview validation gate |
| 14 | Create | `.claude/skills/content/visual-designer/templates/` | Migrated platform-overrides, visual-beats, etc. |
| 15 | Create | `.claude/skills/content/tts-engine/SKILL.md` | TTS + subtitle methodology |
| 16 | Create | `.claude/skills/content/tts-engine/exit-check.py` | Audio + subtitle validation gate |
| 17 | Create | `.claude/skills/content/tts-engine/scripts/` | Migrated tts-edge.ts, tts-manager.ts |
| 18 | Create | `.claude/skills/content/tts-engine/presets/` | TTS voice presets |
| 19 | Create | `.claude/skills/content/video-compositor/SKILL.md` | Video composition methodology |
| 20 | Create | `.claude/skills/content/video-compositor/exit-check.py` | Video output validation gate |
| 21 | Create | `.claude/skills/content/video-compositor/project-template/` | Migrated Remotion template |
| 22 | Create | `.claude/skills/content/video-compositor/scripts/` | Migrated render scripts |
| 23 | Modify | `.claude/router.py` | Add domain-aware routing with content triggers |
| 24 | Modify | `.claude/check-harness.py` | Add content skill verification |
| 25 | Modify | `.claude/CLAUDE.md` | Dual-domain orchestrator protocol |
| 26 | Modify | `.claude/docs/HARNESS-ARCHITECTURE.md` | Add dual-track documentation |
| 27 | Create | `.claude/docs/CONTENT-PIPELINE.md` | Content production flow documentation |
| 28 | Create | `.claude/state/L5-media.md` | Media asset manifest template |
| 29 | Create | `.claude/hooks/content-validator.sh` | Content domain hook |
| 30 | Create | `.claude/skills/content/script-writer/scripts/parse-script.ts` | Migrated from self-media-video |

---

## Task 1: Restructure Directories — Move dev skills under `dev/` subdirectory

**Files:**
- Move: `.claude/skills/product-spec-builder/` → `.claude/skills/dev/product-spec-builder/`
- Move: `.claude/skills/design-brief-builder/` → `.claude/skills/dev/design-brief-builder/`
- Move: `.claude/skills/design-maker/` → `.claude/skills/dev/design-maker/`
- Move: `.claude/skills/dev-planner/` → `.claude/skills/dev/dev-planner/`
- Move: `.claude/skills/dev-builder/` → `.claude/skills/dev/dev-builder/`
- Move: `.claude/skills/bug-fixer/` → `.claude/skills/dev/bug-fixer/`
- Move: `.claude/skills/code-review/` → `.claude/skills/dev/code-review/`
- Move: `.claude/skills/release-builder/` → `.claude/skills/dev/release-builder/`
- Create: `.claude/skills/content/` directory (empty, ready for Task 2+)

- [ ] **Step 1: Create target directories**

```bash
cd /Users/wuzhijing/learning/workflows/pm-demo1/reliable-dev-harness
mkdir -p .claude/skills/dev
mkdir -p .claude/skills/content
```

- [ ] **Step 2: Move all 8 dev skills into dev/ subdirectory**

```bash
cd /Users/wuzhijing/learning/workflows/pm-demo1/reliable-dev-harness/.claude/skills

# Move each skill directory
for skill in product-spec-builder design-brief-builder design-maker dev-planner dev-builder bug-fixer code-review release-builder; do
  mv "$skill" dev/"$skill"
done
```

- [ ] **Step 3: Verify the move succeeded**

```bash
ls -la /Users/wuzhijing/learning/workflows/pm-demo1/reliable-dev-harness/.claude/skills/dev/
ls -la /Users/wuzhijing/learning/workflows/pm-demo1/reliable-dev-harness/.claude/skills/content/
```

Expected: dev/ contains 8 skill directories, content/ is empty.

- [ ] **Step 4: Update check-harness.py path references (temporarily disabled — will be fully updated in Task 7)**

At this point, check-harness.py will break because it looks for skills in the old flat structure. This is expected — Task 7 will fix it. For now, verify the move is correct by listing:

```bash
find /Users/wuzhijing/learning/workflows/pm-demo1/reliable-dev-harness/.claude/skills/dev -name "SKILL.md" | sort
```

Expected: 8 SKILL.md files listed under `dev/` subdirectories.

- [ ] **Step 5: Commit**

```bash
cd /Users/wuzhijing/learning/workflows/pm-demo1/reliable-dev-harness
git add -A
git commit -m "refactor: move dev skills into dev/ subdirectory for dual-track architecture"
```

---

## Task 2: Write script-writer Skill (SKILL.md + exit-check.py)

**Files:**
- Create: `.claude/skills/content/script-writer/SKILL.md`
- Create: `.claude/skills/content/script-writer/exit-check.py`
- Create: `.claude/skills/content/script-writer/scripts/parse-script.ts`

**Context:** This is the first and simplest content skill. It covers G0 (platform/style selection) and G1 (scene breakdown) from the self-media-video pipeline. The script-writer takes Markdown oral scripts or topic descriptions and produces `scenes.json` + `state/L2-spec.md` (content spec).

- [ ] **Step 1: Create script-writer directory structure**

```bash
mkdir -p /Users/wuzhijing/learning/workflows/pm-demo1/reliable-dev-harness/.claude/skills/content/script-writer/scripts
```

- [ ] **Step 2: Write script-writer SKILL.md**

Create `.claude/skills/content/script-writer/SKILL.md` with the following structure (full content below):

```markdown
# script-writer — 口播文稿解析与场景拆分

## Purpose

将 Markdown 口播文稿或主题描述转化为结构化的场景拆分（scenes.json）和内容规格（L2-spec.md），为后续视觉设计和视频合成提供可验证的输入。

## Key Concepts

### 场景（Scene）
一段完整的表达单元，包含：唯一ID、口播文本、预估时长、可选的视觉节拍（visualBeats）。

### 视觉节拍（Visual Beat）
场景内部的时间锚点，标记"此时应出现配图/动画"的时刻。格式：`{ timeMs, type, description }`

### 平台规格（Platform Spec）
决定视频尺寸、布局约束、字幕安全区等技术参数。

### Mood（情绪基调）
决定视觉风格的整体基调。四种选项：
| Mood | 视觉感受 | 典型配色 |
|------|---------|---------|
| Impressed | 厚重、震撼 | 深色 + 金色 |
| Excited | 活力、跳动 | 高饱和彩色 |
| Calm | 宁静、专注 | 低饱和冷色 |
| Inspired | 温暖、向上 | 暖色 - 橙 - 黄绿 |

### 反模式（Anti-Patterns）
- ❌ 不要把标题/列表强行当作场景分割点——场景应该按语义段落切分
- ❌ 不要在场景文本中嵌入排版指令（如"放大"、"切换"）——这些属于 visualBeats
- ❌ 不要跳过 Creative Gate 直接进入 visual-designer——平台和风格的选择必须经人类确认

## Application

### 步骤 1：Creative Gate G0 — 平台与风格选择

与用户确认：
1. **目标平台**：短视频平台（9:16）、横屏演示（16:9）、社交媒体（4:5）
2. **Mood 选择**：Impressed / Excited / Calm / Inspired
3. **大致时长**：30秒-5分钟

如果用户已提供这些信息，确认即可。如果未提供，使用推荐默认值（9:16, Excited, 60-90秒）并请用户确认。

将确认结果写入 `state/L2-spec.md` 的头部 metadata。

### 步骤 2：解析文稿为场景

1. 读取 Markdown 口播文稿
2. 按语义段落（不是按段落标记）拆分为 2-15 个场景
3. 每个场景包含：
   - `id`: "scene-01", "scene-02", ...
   - `text`: 口播文字（不是标题，是说出来的话）
   - `estimatedDuration`: 根据字数估算（中文约 4字/秒）
   - `visualBeats`: 数组，标记需要视觉变化的时刻（可以为空）
4. 输出 `scenes.json`

### 步骤 3：Creative Gate G1 — 场景拆分确认

展示 scenes.json 摘要给用户：
- 场景数量和总时长
- 每个场景的关键词概要
- 预估的视觉节奏

等待用户确认或要求调整。

### 步骤 4：更新状态文件

将内容规格写入 `state/L2-spec.md`，格式如下：

```markdown
# Content Spec

## Metadata
- Platform: {9:16 | 16:9 | 4:5}
- Mood: {Impressed | Excited | Calm | Inspired}
- Target Duration: {N}s

## Scene Summary
{scenes.json 的关键信息摘要，不超过 2000 tokens}

## Source
- Input: {原始文稿路径或描述}
- Scenes: scenes.json
```

### 步骤 5：Hard Gate — 运行 exit-check.py

```bash
python3 .claude/skills/content/script-writer/exit-check.py
```

退出码 ≠ 0 时，**必须修复后才能进入下一个 Skill**。

## Examples

### ✅ 好的场景拆分（语义段落）

```json
{
  "scenes": [
    {
      "id": "scene-01",
      "text": "今天我们要聊一个让很多人头疼的问题——为什么你的短视频总是没人看？",
      "estimatedDuration": 6,
      "visualBeats": [
        {"timeMs": 0, "type": "hook", "description": "问号符号动画"}
      ]
    }
  ]
}
```

### ❌ 坏的场景拆分（按标题切割）

```json
{
  "scenes": [
    {"id": "scene-01", "text": "# 为什么没人看", "estimatedDuration": 0},
    {"id": "scene-02", "text": "首先我们来分析原因", "estimatedDuration": 2}
  ]
}
```

问题：标题不是口播文本，时长为0，缺少 visualBeats。

## Common Pitfalls

1. **场景太碎**：2-3秒一个场景会导致视觉跳跃。每个场景至少 8-15 秒。
2. **遗漏 visualBeats**：即使不确定视觉细节，也要标记关键节奏点。这为 visual-designer 提供了锚点。
3. **跳过 Creative Gate**：平台/风格选择影响所有下游 Skill。不确认就继续是最大的质量风险。
4. **L2-spec 太长**：保持在 2000 tokens 以内。详尽信息在 scenes.json，不在状态文件里。

## Exit-Check Criteria

运行 `exit-check.py` 检查：
1. `scenes.json` 存在且是有效 JSON
2. 每个场景有 `id`、`text`、`estimatedDuration`
3. 场景数量在 2-15 之间
4. `visualBeats` 数组存在（可以为空数组）
5. `state/L2-spec.md` 存在且包含平台和 Mood 元数据

## References

- 下游 Skill: `content/visual-designer`
- 状态管理: `.claude/state/L2-spec.md`
- 迁移来源: self-media-video G0 + G1
```

- [ ] **Step 3: Write script-writer exit-check.py**

Create `.claude/skills/content/script-writer/exit-check.py`:

```python
#!/usr/bin/env python3
"""
Exit Check: script-writer (Content Domain)
Deterministic gate verifying scene breakdown output quality.
"""

import json
import sys
from pathlib import Path

SCENES_PATH = Path("scenes.json")
SPEC_PATH = Path(".claude/state/L2-spec.md")

ISSUES = []


def check():
    # 1. scenes.json must exist and be valid JSON
    if not SCENES_PATH.exists():
        ISSUES.append(("file_missing", f"{SCENES_PATH} does not exist. Script-writer must produce this file."))
        return  # Can't check anything else without scenes.json

    try:
        with open(SCENES_PATH, encoding="utf-8") as f:
            scenes = json.load(f)
    except json.JSONDecodeError as e:
        ISSUES.append(("invalid_json", f"{SCENES_PATH} is not valid JSON: {e}"))
        return

    # 2. Must be a list or dict with "scenes" key
    if isinstance(scenes, dict):
        scene_list = scenes.get("scenes", [])
    elif isinstance(scenes, list):
        scene_list = scenes
    else:
        ISSUES.append(("invalid_format", f"{SCENES_PATH} must be a list or dict with 'scenes' key. Got: {type(scenes).__name__}"))
        return

    # 3. Scene count: 2-15
    count = len(scene_list)
    if count < 2:
        ISSUES.append(("too_few_scenes", f"Found {count} scenes. Minimum is 2. Scenes that are too short cannot convey meaningful content."))
    if count > 15:
        ISSUES.append(("too_many_scenes", f"Found {count} scenes. Maximum is 15. Consider merging related scenes."))

    # 4. Each scene must have required fields
    for i, scene in enumerate(scene_list):
        sid = scene.get("id", f"index-{i}")
        if "id" not in scene:
            ISSUES.append(("missing_field", f"Scene {i} missing 'id'."))
        if "text" not in scene:
            ISSUES.append(("missing_field", f"Scene {sid} missing 'text'. Scenes must have spoken content."))
        if "estimatedDuration" not in scene:
            ISSUES.append(("missing_field", f"Scene {sid} missing 'estimatedDuration'. Duration is needed for downstream TTS scheduling."))
        elif not isinstance(scene["estimatedDuration"], (int, float)) or scene["estimatedDuration"] < 1:
            ISSUES.append(("invalid_duration", f"Scene {sid} has invalid estimatedDuration: {scene['estimatedDuration']}. Must be a number >= 1 second."))
        if "visualBeats" not in scene:
            ISSUES.append(("missing_field", f"Scene {sid} missing 'visualBeats'. Add an empty array if no beats needed."))

    # 5. L2-spec.md must exist with platform and mood metadata
    if not SPEC_PATH.exists():
        ISSUES.append(("spec_missing", f"{SPEC_PATH} does not exist. Content spec is required for downstream skills."))
    else:
        content = SPEC_PATH.read_text(encoding="utf-8")
        if "Platform" not in content and "platform" not in content.lower():
            ISSUES.append(("spec_missing_platform", f"{SPEC_PATH} must specify Platform (9:16, 16:9, or 4:5)."))
        if "Mood" not in content and "mood" not in content.lower():
            ISSUES.append(("spec_missing_mood", f"{SPEC_PATH} must specify Mood (Impressed, Excited, Calm, or Inspired)."))


def main() -> int:
    check()
    if not ISSUES:
        print("✅ script-writer exit check passed. Scenes are structured and spec is complete.")
        return 0

    print("❌ script-writer exit check failed:\n")
    for code, detail in ISSUES:
        print(f"  [{code}] {detail}")
    print()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 4: Migrate parse-script.ts from self-media-video**

```bash
cp /Users/wuzhijing/.claude/skills/self-media-video/scripts/parse-script.ts \
   /Users/wuzhijing/learning/workflows/pm-demo1/reliable-dev-harness/.claude/skills/content/script-writer/scripts/parse-script.ts
```

- [ ] **Step 5: Verify script-writer skill structure**

```bash
ls -la /Users/wuzhijing/learning/workflows/pm-demo1/reliable-dev-harness/.claude/skills/content/script-writer/
ls -la /Users/wuzhijing/learning/workflows/pm-demo1/reliable-dev-harness/.claude/skills/content/script-writer/scripts/
```

Expected: SKILL.md, exit-check.py, and scripts/parse-script.ts all present.

- [ ] **Step 6: Commit**

```bash
cd /Users/wuzhijing/learning/workflows/pm-demo1/reliable-dev-harness
git add -A
git commit -m "feat(content): add script-writer skill with SKILL.md, exit-check.py, and parse-script.ts"
```

---

## Task 3: Write visual-designer Skill (SKILL.md + exit-check.py + template migration)

**Files:**
- Create: `.claude/skills/content/visual-designer/SKILL.md`
- Create: `.claude/skills/content/visual-designer/exit-check.py`
- Copy: templates from self-media-video → `.claude/skills/content/visual-designer/templates/`

**Context:** visual-designer is the orchestrator for G2+G3. It delegates HTML slide generation to the `frontend-slides` skill (external, not inside the Harness) and handles scene→slide data transformation, video-specific CSS injection, and image management.

- [ ] **Step 1: Create visual-designer directory structure**

```bash
mkdir -p /Users/wuzhijing/learning/workflows/pm-demo1/reliable-dev-harness/.claude/skills/content/visual-designer/templates
```

- [ ] **Step 2: Write visual-designer SKILL.md**

Create `.claude/skills/content/visual-designer/SKILL.md`:

```markdown
# visual-designer — 视觉设计与HTML幻灯片编排

## Purpose

将 script-writer 产出的 scenes.json 转化为视觉风格化的 HTML 幻灯片预览。visual-designer 是编排器（Orchestrator），它负责场景→幻灯片数据转换、图片生成/管理、平台样式注入，并将实际的 HTML 生成委托给 `frontend-slides` skill。

## Key Concepts

### 编排器 vs 执行器
- **visual-designer（编排器）**：负责 video-specific 逻辑（场景→幻灯片映射、平台 CSS、beat 属性注入、图片管理）
- **frontend-slides（执行器）**：负责 HTML 幻灯片的视觉设计（Mood Selection、3 Style Previews、自由排版）

### 平台覆盖 CSS
不同视频尺寸需要不同的布局约束。platform-overrides 模板定义了 9:16、16:9、4:5 的 CSS 变量。

### Visual Beats → HTML 属性
`scenes.json` 中的 `visualBeats` 被转化为 HTML 元素上的 `data-beat-at` 属性，供 video-compositor 在正确时间点触发动画。

### 反模式（Anti-Patterns）
- ❌ 不要自己写 HTML 幻灯片——调用 frontend-slides 来生成
- ❌ 不要在 frontend-slides 的输出中修改视觉风格——只注入 video-specific 的属性和 CSS
- ❌ 不要跳过 Creative Gate 的 Style Preview 确认——用户必须在 3 个预览中做出选择
- ❌ 不要在没有 scenes.json 的情况下开始工作——这是 Hard Gate 的前置条件

## Application

### 前置条件（Hard Gate from script-writer）

确认以下文件存在且通过 exit-check：
1. `scenes.json` — 结构化的场景数据
2. `.claude/state/L2-spec.md` — 包含 Platform 和 Mood 元数据

### 步骤 1：Creative Gate G2a — 图片策略确认

分析 scenes.json，确定哪些场景需要配图：
1. 读取每个场景的 visualBeats，提取需要配图的时刻
2. 为需要配图的场景生成图片提示词（keywords + scene context）
3. 展示图片列表给用户确认

### 步骤 2：Creative Gate G2b — Mood + Style Preview

调用 `frontend-slides` 技能的 Mood Selection 流程：
1. 根据 L2-spec.md 的 Mood 设置，让 frontend-slides 生成 3 个 Style Previews
2. 等待用户选择风格方案
3. 记录选择结果到 `state/L3-design.md`

### 步骤 3：场景→幻灯片数据转换

将 scenes.json 转换为 frontend-slides 能理解的输入格式：
1. 每个场景映射为一个幻灯片 section
2. 口播文本作为幻灯片内容
3. visualBeats 转化为 HTML 属性（`data-beat-at="TIMESTAMP_MS"`, `data-beat-type="focus|transition|highlight"`)
4. 图片引用嵌入幻灯片数据

### 步骤 4：调用 frontend-slides 生成 HTML

委托给 frontend-slides 技能生成完整的 HTML 幻灯片。frontend-slides 负责所有视觉设计质量。

### 步骤 5：后处理 — 注入 video-specific 属性

frontend-slides 生成的 HTML 需要后续注入：
1. **平台覆盖 CSS**：根据 L2-spec.md 的 Platform，在 `<head>` 中添加 platform-override CSS 变量
2. **Beat 属性**：在每个需要的时间点元素上添加 `data-beat-at` 属性
3. **三分之一字幕区**：注入 lower-thirds CSS 样式（如果 scenes.json 中有字幕需求）
4. **动画预设**：注入 transition 和 animation CSS

输出文件：`slides-preview.html`

### 步骤 6：更新状态文件

将视觉设计规格写入 `state/L3-design.md`：

```markdown
# Visual Design Spec

## Design Decision
- Mood: {Mood from L2}
- Platform: {9:16 | 16:9 | 4:5}
- Style: {selected style name}
- Primary Color: {hex}
- Font Pair: {heading font} + {body font}

## Assets
- Slides Preview: slides-preview.html
- Image Count: {N} images generated/referenced
- Beat Markers: {N} visual beats injected

## Slides Structure
{每个幻灯片的标题和关键内容摘要}
```

### 步骤 7：Hard Gate — 运行 exit-check.py

```bash
python3 .claude/skills/content/visual-designer/exit-check.py
```

退出码 ≠ 0 时，**必须修复后才能进入 tts-engine**。

## Examples

### ✅ 好的 slides-preview.html 片段

```html
<section data-beat-at="0" data-beat-type="hook" class="slide">
  <h2>为什么短视频没人看？</h2>
  <p>3个你没想到的原因</p>
</section>
```

### ❌ 坏的做法 — 自己生成 HTML 而不使用 frontend-slides

```html
<!-- 错误：visual-designer 不应该直接写幻灯片 HTML -->
<style>.slide { background: #333; }</style>
<div class="slide">...</div>
```

应该委托给 frontend-slides，然后只做后处理注入。

## Common Pitfalls

1. **跳过 frontend-slides**：直接写 HTML 会导致视觉质量下降。frontend-slides 有完整的 Mood Selection + Style Preview 流程。
2. **忘记平台覆盖**：9:16 和 16:9 的布局差异很大。不注入 platform-override CSS 会导致视频输出比例错误。
3. **过度修改 frontend-slides 输出**：只注入 video-specific 属性（data-beat-at、platform CSS），不要修改视觉风格。
4. **图片未就绪就开始 HTML 生成**：所有配图必须在调用 frontend-slides 之前准备好。

## Exit-Check Criteria

运行 `exit-check.py` 检查：
1. `slides-preview.html` 存在且是有效 HTML
2. HTML 包含 `data-beat-at` 属性
3. HTML 包含平台覆盖 CSS（9:16/16:9/4:5 变量）
4. 所有引用的图片文件存在
5. `state/L3-design.md` 存在且包含 Mood 和 Style 信息

## References

- 上游 Skill: `content/script-writer`
- 委托 Skill: `frontend-slides`（外部技能，不在 Harness 内）
- 下游 Skill: `content/tts-engine`
- 状态管理: `.claude/state/L2-spec.md`, `.claude/state/L3-design.md`
- 模板目录: `templates/`（platform-overrides, visual-beats, scene-layouts, lower-thirds, animation-presets, slide-presets）
- 迁移来源: self-media-video G2 + G3
```

- [ ] **Step 3: Write visual-designer exit-check.py**

Create `.claude/skills/content/visual-designer/exit-check.py`:

```python
#!/usr/bin/env python3
"""
Exit Check: visual-designer (Content Domain)
Deterministic gate verifying HTML slides output quality.
"""

import re
import sys
from pathlib import Path

SLIDES_PATH = Path("slides-preview.html")
DESIGN_SPEC_PATH = Path(".claude/state/L3-design.md")
SCENES_PATH = Path("scenes.json")

ISSUES = []


def check():
    # 1. slides-preview.html must exist and be valid HTML
    if not SLIDES_PATH.exists():
        ISSUES.append(("file_missing", f"{SLIDES_PATH} does not exist. visual-designer must produce this file."))
        return
    
    html_content = SLIDES_PATH.read_text(encoding="utf-8")
    
    if not html_content.strip().startswith("<") and not "<html" in html_content.lower()[:200]:
        ISSUES.append(("invalid_html", f"{SLIDES_PATH} does not appear to be valid HTML. Must start with <!DOCTYPE html> or <html>."))
    
    # 2. Must contain data-beat-at attributes
    if "data-beat-at" not in html_content:
        ISSUES.append(("missing_beat_attributes", f"{SLIDES_PATH} contains no 'data-beat-at' attributes. Visual beats from scenes.json must be injected into HTML elements."))
    
    # 3. Must contain platform override CSS
    has_platform_css = any(marker in html_content for marker in [
        "--platform-aspect", "9:16", "16:9", "4:5", "platform-override", "aspect-ratio"
    ])
    if not has_platform_css:
        ISSUES.append(("missing_platform_css", f"{SLIDES_PATH} missing platform override CSS. Must include aspect ratio variables for the target platform."))
    
    # 4. Check referenced image files exist
    img_refs = re.findall(r'(?:src|href)=["\']([^"\']+\.(?:png|jpg|jpeg|webp|svg|gif))["\']', html_content, re.IGNORECASE)
    for img_ref in img_refs:
        img_path = Path(img_ref)
        if not img_path.is_absolute():
            img_path = Path(".") / img_ref
        if not img_path.exists():
            ISSUES.append(("image_missing", f"Referenced image not found: {img_ref}"))
    
    # 5. L3-design.md must exist with Mood and Style
    if not DESIGN_SPEC_PATH.exists():
        ISSUES.append(("design_spec_missing", f"{DESIGN_SPEC_PATH} does not exist. Visual design spec is required for downstream TTS."))
    else:
        content = DESIGN_SPEC_PATH.read_text(encoding="utf-8")
        if "Mood" not in content and "mood" not in content.lower():
            ISSUES.append(("design_spec_missing_mood", f"{DESIGN_SPEC_PATH} must specify Mood."))
        if "Style" not in content and "style" not in content.lower():
            ISSUES.append(("design_spec_missing_style", f"{DESIGN_SPEC_PATH} must specify Style selection."))


def main() -> int:
    check()
    if not ISSUES:
        print("✅ visual-designer exit check passed. HTML slides are valid and complete.")
        return 0

    print("❌ visual-designer exit check failed:\n")
    for code, detail in ISSUES:
        print(f"  [{code}] {detail}")
    print()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 4: Migrate template directories from self-media-video**

```bash
SRC=/Users/wuzhijing/.claude/skills/self-media-video/templates
DST=/Users/wuzhijing/learning/workflows/pm-demo1/reliable-dev-harness/.claude/skills/content/visual-designer/templates

# Copy all template subdirectories
for dir in platform-overrides visual-beats scene-layouts lower-thirds animation-presets slide-presets; do
  cp -r "$SRC/$dir" "$DST/$dir" 2>/dev/null || echo "Warning: $dir not found in source, skipping"
done

# Also copy video-slide-contract.md if it exists
cp "$SRC/video-slide-contract.md" "$DST/" 2>/dev/null || true
cp "$SRC/visual-elements/" "$DST/visual-elements/" -r 2>/dev/null || true
```

- [ ] **Step 5: Verify visual-designer skill structure**

```bash
find /Users/wuzhijing/learning/workflows/pm-demo1/reliable-dev-harness/.claude/skills/content/visual-designer -type f | head -20
```

Expected: SKILL.md, exit-check.py, templates/ with 6-8 subdirectories.

- [ ] **Step 6: Commit**

```bash
cd /Users/wuzhijing/learning/workflows/pm-demo1/reliable-dev-harness
git add -A
git commit -m "feat(content): add visual-designer skill with SKILL.md, exit-check.py, and migrated templates"
```

---

## Task 4: Write tts-engine Skill (SKILL.md + exit-check.py + script migration)

**Files:**
- Create: `.claude/skills/content/tts-engine/SKILL.md`
- Create: `.claude/skills/content/tts-engine/exit-check.py`
- Create: `.claude/skills/content/tts-engine/scripts/` (migrated TTS scripts)
- Create: `.claude/skills/content/tts-engine/presets/` (voice presets)

- [ ] **Step 1: Create tts-engine directory structure**

```bash
mkdir -p /Users/wuzhijing/learning/workflows/pm-demo1/reliable-dev-harness/.claude/skills/content/tts-engine/scripts
mkdir -p /Users/wuzhijing/learning/workflows/pm-demo1/reliable-dev-harness/.claude/skills/content/tts-engine/presets
```

- [ ] **Step 2: Write tts-engine SKILL.md**

Create `.claude/skills/content/tts-engine/SKILL.md`:

```markdown
# tts-engine — 语音合成与字幕生成

## Purpose

将 scenes.json 中每个场景的口播文本转化为对应的音频文件（.mp3）和时间对齐的字幕（subtitles.json），为最终的 video-compositor 提供音频轨道和字幕数据。

## Key Concepts

### TTS 预设（Preset）
预定义的语音配置，包含风格、音色、语速。用户可以选择现有预设或创建自定义预设。

### 字幕时间对齐
每个字幕条目包含：文本、开始毫秒（startMs）、结束毫秒（endMs）。时间对齐的精确性直接影响视频观感。

### 音频时长校验
总音频时长应在预估总时长的 ±30% 以内。超出此范围说明场景文本与预估时长严重不匹配。

### 反模式（Anti-Patterns）
- ❌ 不要跳过 TTS 风格选择的 Creative Gate——即使使用默认预设也需要确认
- ❌ 不要手动估算时长——必须用实际音频时长
- ❌ 不要在没有 scenes.json 的情况下开始工作

## Application

### 前置条件（Hard Gate from visual-designer）

确认以下文件存在且通过 exit-check：
1. `scenes.json` — 场景数据
2. `.claude/state/L3-design.md` — 包含视觉设计规格

### 步骤 1：Creative Gate G4a-1 — TTS 风格选择

与用户确认 TTS 风格：
1. 展示预设表（专业科普、轻松闲聊等）
2. 如果用户已有偏好，直接确认
3. 如果 Creative Gate 被标记为 "configurable skip"，可使用默认预设并跳过确认

**TTS 预设表：**

| Preset | 风格 | 音色 | 语速 |
|--------|------|------|------|
| 专业科普-女 | 清晰正式 | YunyangNeural | +0% |
| 专业科普-男 | 沉稳深度 | YunhaoNeural | -5% |
| 轻松闲聊-女 | 亲切活人感 | XiaoshuangNeural | +5% |
| 轻松闲聊-男 | 随和自然 | YunxiNeural | +0% |
| 激情解说-男 | 高能量快节奏 | YunzeNeural | +10% |
| 温柔讲述-女 | 柔和缓慢 | XiaohanNeural | -10% |

将选择记录到 `state/L3-design.md` 的 TTS 部分。

### 步骤 2：逐场景生成音频

对 scenes.json 中每个场景：
1. 提取场景文本
2. 调用 TTS 引擎（Edge TTS 或其他）生成 .mp3 文件
3. 保存到 `audio/scene-{id}.mp3`
4. 记录实际音频时长

### 步骤 3：生成字幕文件

基于实际音频时长，生成 `subtitles.json`：
```json
[
  {
    "text": "场景1的口播文本",
    "startMs": 0,
    "endMs": 5800
  },
  {
    "text": "场景2的口播文本",
    "startMs": 5800,
    "endMs": 12400
  }
]
```

### 步骤 4：更新状态文件

记录媒体资产清单到 `state/L5-media.md`：
```markdown
# Media Asset Manifest

## Audio
| Scene | File | Duration |
|-------|------|----------|
| scene-01 | audio/scene-01.mp3 | 5.8s |
| scene-02 | audio/scene-02.mp3 | 6.6s |
| ... | ... | ... |

## Subtitles
- File: subtitles.json
- Total entries: {N}
- Total duration: {T}s

## TTS Config
- Preset: {preset name}
- Voice: {voice name}
- Speed: {speed adjustment}
```

### 步骤 5：Hard Gate — 运行 exit-check.py

```bash
python3 .claude/skills/content/tts-engine/exit-check.py
```

退出码 ≠ 0 时，**必须修复后才能进入 video-compositor**。

## Examples

### ✅ 好的音频文件结构

```
audio/
├── scene-01.mp3   # 5.8s
├── scene-02.mp3   # 6.6s
├── scene-03.mp3   # 8.2s
└── scene-04.mp3   # 4.1s
```

### ❌ 坏的做法 — 时长不匹配

如果 scenes.json 估计总时长 60s 但实际音频总时长 120s，说明场景文本量远超预估。应该回到 script-writer 重新拆分场景。

## Common Pitfalls

1. **忽略音频时长偏差**：实际时长与预估相差超过 30% 是严重问题，需要回溯。
2. **缺少音频文件**：每个场景必须有对应的 .mp3 文件，缺失任何一个都会导致 video-compositor 失败。
3. **字幕时间不对齐**：subtitles.json 的时间必须与实际音频播放时间严格对齐。
4. **跳过 Creative Gate**：即使用户信任默认预设，也需要至少记录选择了哪个预设。

## Exit-Check Criteria

运行 `exit-check.py` 检查：
1. `audio/` 目录存在且包含每个场景对应的 .mp3 文件
2. 每个音频文件时长 > 0
3. `subtitles.json` 存在且是有效 JSON
4. subtitles.json 中每项有 `text`、`startMs`、`endMs`
5. 总音频时长在预估总时长的 ±30% 以内

## References

- 上游 Skill: `content/visual-designer`
- 下游 Skill: `content/video-compositor`
- 状态管理: `.claude/state/L3-design.md`, `.claude/state/L5-media.md`
- 脚本目录: `scripts/`（tts-edge.ts, tts-manager.ts）
- 预设目录: `presets/`
- 迁移来源: self-media-video G4a
```

- [ ] **Step 3: Write tts-engine exit-check.py**

Create `.claude/skills/content/tts-engine/exit-check.py`:

```python
#!/usr/bin/env python3
"""
Exit Check: tts-engine (Content Domain)
Deterministic gate verifying TTS audio output and subtitle quality.
"""

import json
import os
import sys
from pathlib import Path

SCENES_PATH = Path("scenes.json")
AUDIO_DIR = Path("audio")
SUBTITLES_PATH = Path("subtitles.json")
SPEC_PATH = Path(".claude/state/L2-spec.md")

ISSUES = []


def check():
    # 1. Audio directory must exist
    if not AUDIO_DIR.exists() or not AUDIO_DIR.is_dir():
        ISSUES.append(("audio_dir_missing", f"{AUDIO_DIR} directory does not exist. TTS must produce per-scene audio files."))
        # Can't check audio files without the directory
        return

    # 2. Load scenes to check each has corresponding audio
    scene_ids = []
    if SCENES_PATH.exists():
        try:
            with open(SCENES_PATH, encoding="utf-8") as f:
                scenes = json.load(f)
            if isinstance(scenes, dict):
                scene_list = scenes.get("scenes", [])
            else:
                scene_list = scenes
            scene_ids = [s.get("id", "") for s in scene_list if "id" in s]
        except json.JSONDecodeError:
            ISSUES.append(("scenes_invalid", f"{SCENES_PATH} is not valid JSON. Cannot verify audio-file correspondence."))
    
    # 3. Check each scene has an audio file
    if scene_ids:
        for sid in scene_ids:
            audio_file = AUDIO_DIR / f"{sid}.mp3"
            if not audio_file.exists():
                ISSUES.append(("audio_missing", f"Audio file missing for scene {sid}: expected {audio_file}"))
            elif audio_file.stat().st_size < 100:  # Suspiciously small
                ISSUES.append(("audio_too_small", f"Audio file {audio_file} is suspiciously small ({audio_file.stat().st_size} bytes). May be corrupt."))
    else:
        # Fallback: check at least some mp3 files exist
        mp3_files = list(AUDIO_DIR.glob("*.mp3"))
        if not mp3_files:
            ISSUES.append(("no_audio_files", f"No .mp3 files found in {AUDIO_DIR}. TTS must produce audio output."))

    # 4. subtitles.json must exist and be valid
    if not SUBTITLES_PATH.exists():
        ISSUES.append(("subtitles_missing", f"{SUBTITLES_PATH} does not exist. TTS must produce timed subtitles."))
    else:
        try:
            with open(SUBTITLES_PATH, encoding="utf-8") as f:
                subs = json.load(f)
            
            if not isinstance(subs, list) or len(subs) == 0:
                ISSUES.append(("subtitles_empty", f"{SUBTITLES_PATH} must be a non-empty array of subtitle entries."))
            else:
                for i, sub in enumerate(subs):
                    if "text" not in sub:
                        ISSUES.append(("subtitle_missing_field", f"Subtitle entry {i} missing 'text'."))
                    if "startMs" not in sub:
                        ISSUES.append(("subtitle_missing_field", f"Subtitle entry {i} missing 'startMs'."))
                    if "endMs" not in sub:
                        ISSUES.append(("subtitle_missing_field", f"Subtitle entry {i} missing 'endMs'."))
                    elif sub.get("endMs", 0) <= sub.get("startMs", 0):
                        ISSUES.append(("subtitle_invalid_time", f"Subtitle entry {i}: endMs ({sub.get('endMs')}) must be > startMs ({sub.get('startMs')})."))
        except json.JSONDecodeError:
            ISSUES.append(("subtitles_invalid_json", f"{SUBTITLES_PATH} is not valid JSON."))

    # 5. Basic duration sanity check (if we have both scenes and audio files)
    estimated_total = 0
    if SCENES_PATH.exists():
        try:
            with open(SCENES_PATH, encoding="utf-8") as f:
                scenes = json.load(f)
            if isinstance(scenes, dict):
                scene_list = scenes.get("scenes", [])
            else:
                scene_list = scenes
            estimated_total = sum(s.get("estimatedDuration", 0) for s in scene_list)
        except (json.JSONDecodeError, KeyError):
            pass

    if estimated_total > 0 and SUBTITLES_PATH.exists():
        try:
            with open(SUBTITLES_PATH, encoding="utf-8") as f:
                subs = json.load(f)
            if isinstance(subs, list) and len(subs) > 0:
                actual_total_ms = subs[-1].get("endMs", 0)
                actual_total_s = actual_total_ms / 1000
                ratio = actual_total_s / estimated_total
                if ratio < 0.7 or ratio > 1.3:
                    ISSUES.append(("duration_mismatch", 
                        f"Total audio duration ({actual_total_s:.1f}s) is {ratio:.0%} of estimated ({estimated_total}s). "
                        f"Expected within 70%-130%. Consider revisiting scene segmentation."))
        except (json.JSONDecodeError, KeyError, IndexError):
            pass


def main() -> int:
    check()
    if not ISSUES:
        print("✅ tts-engine exit check passed. Audio files and subtitles are valid and complete.")
        return 0

    print("❌ tts-engine exit check failed:\n")
    for code, detail in ISSUES:
        print(f"  [{code}] {detail}")
    print()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 4: Migrate TTS scripts from self-media-video**

```bash
SRC=/Users/wuzhijing/.claude/skills/self-media-video/scripts
DST=/Users/wuzhijing/learning/workflows/pm-demo1/reliable-dev-harness/.claude/skills/content/tts-engine/scripts

cp "$SRC/tts-edge.ts" "$DST/"
cp "$SRC/tts-manager.ts" "$DST/"

# Also copy tts-minimax.ts if it exists
cp "$SRC/tts-minimax.ts" "$DST/" 2>/dev/null || true
```

- [ ] **Step 5: Create TTS presets file**

Create `.claude/skills/content/tts-engine/presets/voice-presets.json`:

```json
{
  "presets": [
    {
      "id": "professional-female",
      "label": "专业科普-女",
      "description": "清晰正式",
      "voice": "YunyangNeural",
      "speedAdjustment": 0,
      "language": "zh-CN"
    },
    {
      "id": "professional-male",
      "label": "专业科普-男",
      "description": "沉稳深度",
      "voice": "YunhaoNeural",
      "speedAdjustment": -5,
      "language": "zh-CN"
    },
    {
      "id": "casual-female",
      "label": "轻松闲聊-女",
      "description": "亲切活人感",
      "voice": "XiaoshuangNeural",
      "speedAdjustment": 5,
      "language": "zh-CN"
    },
    {
      "id": "casual-male",
      "label": "轻松闲聊-男",
      "description": "随和自然",
      "voice": "YunxiNeural",
      "speedAdjustment": 0,
      "language": "zh-CN"
    },
    {
      "id": "energetic-male",
      "label": "激情解说-男",
      "description": "高能量快节奏",
      "voice": "YunzeNeural",
      "speedAdjustment": 10,
      "language": "zh-CN"
    },
    {
      "id": "gentle-female",
      "label": "温柔讲述-女",
      "description": "柔和缓慢",
      "voice": "XiaohanNeural",
      "speedAdjustment": -10,
      "language": "zh-CN"
    }
  ]
}
```

- [ ] **Step 6: Verify tts-engine skill structure**

```bash
find /Users/wuzhijing/learning/workflows/pm-demo1/reliable-dev-harness/.claude/skills/content/tts-engine -type f | sort
```

Expected: SKILL.md, exit-check.py, scripts/tts-edge.ts, scripts/tts-manager.ts, presets/voice-presets.json.

- [ ] **Step 7: Commit**

```bash
cd /Users/wuzhijing/learning/workflows/pm-demo1/reliable-dev-harness
git add -A
git commit -m "feat(content): add tts-engine skill with SKILL.md, exit-check.py, TTS scripts, and voice presets"
```

---

## Task 5: Write video-compositor Skill (SKILL.md + exit-check.py + Remotion template migration)

**Files:**
- Create: `.claude/skills/content/video-compositor/SKILL.md`
- Create: `.claude/skills/content/video-compositor/exit-check.py`
- Copy: Remotion project-template from self-media-video
- Copy: render scripts from self-media-video

- [ ] **Step 1: Create video-compositor directory structure**

```bash
mkdir -p /Users/wuzhijing/learning/workflows/pm-demo1/reliable-dev-harness/.claude/skills/content/video-compositor/scripts
```

- [ ] **Step 2: Write video-compositor SKILL.md**

Create `.claude/skills/content/video-compositor/SKILL.md`:

```markdown
# video-compositor — 视频合成与输出

## Purpose

将 slides-preview.html、音频文件、字幕和场景数据合成为最终视频文件（MP4）。video-compositor 使用 Remotion 渲染引擎，将 HTML 幻灯片转化为视频帧，与 TTS 音频和字幕叠加合成完整视频。

## Key Concepts

### Remotion 渲染引擎
video-compositor 使用 Remotion 将 HTML 转化为视频帧。project-template 提供了标准的 Remotion 项目结构，包含 Ken Burns 效果、字幕动画、Beat 叠加等组件。

### 基础视频 vs 最终视频
- **基础视频（base-video.mp4）**：仅包含幻灯片动画和视觉效果，无音频
- **最终视频**：基础视频 + TTS 音频 + 字幕叠加 = 完整产出物

### ffprobe 校验
所有视频产出物必须通过 ffprobe 校验：分辨率匹配、帧率 ≥ 24fps、时长偏差 < 5%。

### 反模式（Anti-Patterns）
- ❌ 不要在没有通过 visual-designer exit-check 的情况下开始渲染
- ❌ 不要手动合成视频——必须通过 Remotion 渲染流程
- ❌ 不要跳过最终 Creative Gate——用户必须确认视频质量
- ❌ 不要在 project-template 中硬编码项目特定数据——使用动态配置

## Application

### 前置条件（Hard Gate from tts-engine）

确认以下文件/目录存在且通过 exit-check：
1. `slides-preview.html` — HTML 幻灯片预览
2. `audio/` — 逐场景 .mp3 文件
3. `subtitles.json` — 时间对齐字幕
4. `scenes.json` — 场景数据

### 步骤 1：初始化 Remotion 项目

1. 从 project-template 复制 Remotion 项目结构
2. 配置项目参数：
   - 目标分辨率（从 L2-spec.md 的 Platform 读取）
   - 帧率：30fps（默认）
   - 场景切换效果配置

### 步骤 2：配置 Video 组件

将 slides-preview.html 的内容映射到 Remotion 的 `<Video>` 组件：
1. 每个 `<section>` 映射为一个 Remotion Sequence
2. `data-beat-at` 属性映射为 BeatOverlay 触发点
3. 字幕从 subtitles.json 加载到 `<Subtitles>` 组件
4. Ken Burns 效果应用于需要强调的场景

### 步骤 3：渲染基础视频

```bash
npx remotion render src/index.ts base-video --output=base-video.mp4
```

基础视频仅包含幻灯片动画和视觉效果，不包含音频。

### 步骤 4：合成最终视频

将基础视频与 TTS 音频合成：
```bash
ffmpeg -i base-video.mp4 -i audio/concatenated.mp3 -c:v copy -c:a aac -shortest final-video.mp4
```

### 步骤 5：更新状态文件

在 `state/L5-media.md` 添加视频产出物信息：
```markdown
## Video Output
- Base video: base-video.mp4 ({resolution}, {fps}fps)
- Final video: final-video.mp4 ({duration}s)
- Audio track: concatenated from {N} scene files
```

### 步骤 6：Hard Gate — 运行 exit-check.py

```bash
python3 .claude/skills/content/video-compositor/exit-check.py
```

退出码 ≠ 0 时，**必须修复**。

### 步骤 7：Creative Gate — 最终视频确认

展示最终视频给用户：
1. 播放预览
2. 确认视觉效果、音频质量、字幕同步
3. 如不满意，指明问题环节（视觉→visual-designer，音频→tts-engine，合成→video-compositor）

## Common Pitfalls

1. **Remotion 配置错误**：分辨率必须与 Platform 匹配（9:16 → 1080x1920，16:9 → 1920x1080，4:5 → 1080x1350）
2. **音频不同步**：ffmpeg 合成时必须使用 `-shortest` 参数避免音频比视频长
3. **字幕闪烁**：确保 subtitles.json 的时间戳与音频严格对齐
4. **忘记 ffprobe 校验**：exit-check 会检查视频参数，不要试图绕过

## Exit-Check Criteria

运行 `exit-check.py` 检查：
1. `base-video.mp4` 存在且分辨率匹配 Platform 规格
2. 最终视频文件存在且可通过 ffprobe 校验
3. 视频时长在总音频时长的 ±5% 以内
4. fps ≥ 24

## References

- 上游 Skills: `content/visual-designer`, `content/tts-engine`
- 状态管理: `.claude/state/L2-spec.md`, `.claude/state/L5-media.md`
- 项目模板: `project-template/`（Remotion 项目结构）
- 脚本目录: `scripts/`（render-slides-to-video 等）
- 迁移来源: self-media-video G4b
```

- [ ] **Step 3: Write video-compositor exit-check.py**

Create `.claude/skills/content/video-compositor/exit-check.py`:

```python
#!/usr/bin/env python3
"""
Exit Check: video-compositor (Content Domain)
Deterministic gate verifying video output quality.
"""

import json
import subprocess
import sys
from pathlib import Path

SCENES_PATH = Path("scenes.json")
SPEC_PATH = Path(".claude/state/L2-spec.md")
BASE_VIDEO_PATH = Path("base-video.mp4")
FINAL_VIDEO_PATH = Path("final-video.mp4")

# Platform resolution map
RESOLUTIONS = {
    "9:16": (1080, 1920),
    "16:9": (1920, 1080),
    "4:5": (1080, 1350),
}

MIN_FPS = 24

ISSUES = []


def get_platform() -> str:
    """Extract platform from L2-spec.md."""
    if not SPEC_PATH.exists():
        return "16:9"  # Default
    content = SPEC_PATH.read_text(encoding="utf-8").lower()
    if "9:16" in content or "9\\:16" in content:
        return "9:16"
    elif "4:5" in content or "4\\:5" in content:
        return "4:5"
    return "16:9"


def get_video_info(video_path: Path) -> dict | None:
    """Use ffprobe to get video info."""
    try:
        result = subprocess.run(
            ["ffprobe", "-v", "quiet", "-print_format", "json",
             "-show_streams", "-show_format", str(video_path)],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode != 0:
            return None
        return json.loads(result.stdout)
    except (FileNotFoundError, subprocess.TimeoutExpired, json.JSONDecodeError):
        return None


def check():
    platform = get_platform()
    expected_width, expected_height = RESOLUTIONS.get(platform, (1920, 1080))
    
    # 1. Base video must exist
    if not BASE_VIDEO_PATH.exists():
        ISSUES.append(("base_video_missing", f"{BASE_VIDEO_PATH} does not exist. Remotion must produce a base video first."))
    else:
        info = get_video_info(BASE_VIDEO_PATH)
        if info is None:
            ISSUES.append(("base_video_unreadable", f"Cannot read {BASE_VIDEO_PATH} with ffprobe. Ensure ffmpeg/ffprobe is installed and the file is a valid video."))
        else:
            # Check resolution
            try:
                video_stream = next(s for s in info.get("streams", []) if s.get("codec_type") == "video")
                width = int(video_stream.get("width", 0))
                height = int(video_stream.get("height", 0))
                if width != expected_width or height != expected_height:
                    ISSUES.append(("resolution_mismatch", 
                        f"Base video resolution {width}x{height} doesn't match platform {platform} ({expected_width}x{expected_height})."))
                
                # Check fps
                fps_str = video_stream.get("r_frame_rate", "0/1")
                if "/" in fps_str:
                    num, den = fps_str.split("/")
                    fps = int(num) / max(int(den), 1)
                else:
                    fps = float(fps_str)
                if fps < MIN_FPS:
                    ISSUES.append(("fps_too_low", f"Base video fps ({fps:.1f}) is below minimum {MIN_FPS}."))
            except (StopIteration, ValueError, KeyError):
                ISSUES.append(("base_video_no_stream", f"Cannot find video stream in {BASE_VIDEO_PATH}."))

    # 2. Final video must exist
    if not FINAL_VIDEO_PATH.exists():
        ISSUES.append(("final_video_missing", f"{FINAL_VIDEO_PATH} does not exist. Video composition must produce the final video."))
    else:
        info = get_video_info(FINAL_VIDEO_PATH)
        if info is None:
            ISSUES.append(("final_video_unreadable", f"Cannot read {FINAL_VIDEO_PATH} with ffprobe."))
        else:
            # Check fps for final video too
            try:
                video_stream = next(s for s in info.get("streams", []) if s.get("codec_type") == "video")
                fps_str = video_stream.get("r_frame_rate", "0/1")
                if "/" in fps_str:
                    num, den = fps_str.split("/")
                    fps = int(num) / max(int(den), 1)
                else:
                    fps = float(fps_str)
                if fps < MIN_FPS:
                    ISSUES.append(("final_fps_too_low", f"Final video fps ({fps:.1f}) is below minimum {MIN_FPS}."))
            except (StopIteration, ValueError, KeyError):
                ISSUES.append(("final_video_no_stream", f"Cannot find video stream in {FINAL_VIDEO_PATH}."))

    # 3. Duration sanity check (if we have both scenes and video)
    if FINAL_VIDEO_PATH.exists() and SCENES_PATH.exists():
        try:
            with open(SCENES_PATH, encoding="utf-8") as f:
                scenes = json.load(f)
            if isinstance(scenes, dict):
                scene_list = scenes.get("scenes", [])
            else:
                scene_list = scenes
            estimated_total = sum(s.get("estimatedDuration", 0) for s in scene_list)
            
            if estimated_total > 0 and FINAL_VIDEO_PATH.exists():
                final_info = get_video_info(FINAL_VIDEO_PATH)
                if final_info:
                    try:
                        duration = float(final_info.get("format", {}).get("duration", 0))
                        if duration > 0:
                            ratio = duration / estimated_total
                            if ratio < 0.95 or ratio > 1.05:
                                ISSUES.append(("duration_mismatch",
                                    f"Video duration ({duration:.1f}s) is {ratio:.0%} of estimated ({estimated_total}s). "
                                    f"Expected within 95%-105%."))
                    except (ValueError, KeyError):
                        pass
        except (json.JSONDecodeError, KeyError):
            pass


def main() -> int:
    check()
    if not ISSUES:
        print("✅ video-compositor exit check passed. Video output is valid and meets quality standards.")
        return 0

    print("❌ video-compositor exit check failed:\n")
    for code, detail in ISSUES:
        print(f"  [{code}] {detail}")
    print()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 4: Migrate Remotion project-template from self-media-video**

```bash
SRC=/Users/wuzhijing/.claude/skills/self-media-video/project-template
DST=/Users/wuzhijing/learning/workflows/pm-demo1/reliable-dev-harness/.claude/skills/content/video-compositor/project-template

# Copy the entire project-template directory (excluding node_modules)
rsync -av --exclude='node_modules' "$SRC/" "$DST/"
```

- [ ] **Step 5: Migrate render scripts from self-media-video**

```bash
SRC=/Users/wuzhijing/.claude/skills/self-media-video/scripts
DST=/Users/wuzhijing/learning/workflows/pm-demo1/reliable-dev-harness/.claude/skills/content/video-compositor/scripts

cp "$SRC/render-slides-to-video.ts" "$DST/" 2>/dev/null || true
cp "$SRC/render-slides-to-video.js" "$DST/" 2>/dev/null || true
cp "$SRC/verify-render.js" "$DST/" 2>/dev/null || true
```

- [ ] **Step 6: Verify video-compositor skill structure**

```bash
find /Users/wuzhijing/learning/workflows/pm-demo1/reliable-dev-harness/.claude/skills/content/video-compositor -type f -not -path "*/node_modules/*" | sort | head -30
```

Expected: SKILL.md, exit-check.py, scripts/, project-template/ (without node_modules).

- [ ] **Step 7: Commit**

```bash
cd /Users/wuzhijing/learning/workflows/pm-demo1/reliable-dev-harness
git add -A
git commit -m "feat(content): add video-compositor skill with SKILL.md, exit-check.py, Remotion template, and render scripts"
```

---

## Task 6: Update router.py — Add domain-aware routing

**Files:**
- Modify: `.claude/router.py`

**Context:** Current router only handles dev skills with flat structure. Need to add content domain triggers and update skill paths to use domain prefixes.

- [ ] **Step 1: Write updated router.py**

The updated router.py must:
1. Add `"domain"` field to all skill entries
2. Update skill `name` fields to include domain prefix (e.g., `dev/product-spec-builder`)
3. Add 4 content skill entries with Chinese + English triggers
4. Update `SKILLS_DIR` resolution to handle `dev/` and `content/` subdirectories
5. Add domain detection logic: if any content trigger matches, prefer content domain

Replace the entire content of `.claude/router.py` with:

```python
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
    {"name": "dev/product-spec-builder", "triggers": ["idea", "spec", "requirement", "PRD", "scope", "what to build"], "domain": "dev"},
    {"name": "dev/design-brief-builder", "triggers": ["design", "style", "theme", "color", "visual", "UI direction"], "domain": "dev"},
    {"name": "dev/design-maker", "triggers": ["mockup", "figma", "prototype", "design file", "screen"], "domain": "dev"},
    {"name": "dev/dev-planner", "triggers": ["plan", "phase", "roadmap", "tech stack", "architecture"], "domain": "dev"},
    {"name": "dev/dev-builder", "triggers": ["implement", "build", "code", "develop", "feature", "task"], "domain": "dev"},
    {"name": "dev/bug-fixer", "triggers": ["bug", "fix", "error", "crash", "broken", "failing test"], "domain": "dev"},
    {"name": "dev/code-review", "triggers": ["review", "check code", "audit", "quality", "inspect"], "domain": "dev"},
    {"name": "dev/release-builder", "triggers": ["release", "deploy", "publish", "ship", "build package"], "domain": "dev"},
    
    # content/ domain (content production)
    {"name": "content/script-writer", "triggers": ["口播", "视频", "script", "场景", "scene", "短视频", "文稿", "口播稿", "拆分场景"], "domain": "content"},
    {"name": "content/visual-designer", "triggers": ["配图", "风格", "Mood", "HTML预览", "style preview", "幻灯片", "slides", "视觉设计", "出场动画"], "domain": "content"},
    {"name": "content/tts-engine", "triggers": ["配音", "TTS", "语音", "字幕", "语音合成", "narration", "audio", "朗读"], "domain": "content"},
    {"name": "content/video-compositor", "triggers": ["渲染", "合成", "输出视频", "render", "Remotion", "视频输出", "compositing", "MP4"], "domain": "content"},
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
    parser.add_argument("--domain", choices=["dev", "content"], help="Restrict routing to a specific domain")
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
```

- [ ] **Step 2: Test the router with domain queries**

```bash
cd /Users/wuzhijing/learning/workflows/pm-demo1/reliable-dev-harness
python3 .claude/router.py "口播视频制作"
python3 .claude/router.py "实现一个新功能"
python3 .claude/router.py "TTS配音" --domain content
```

Expected: First query returns content/script-writer, second returns dev/dev-builder, third restricts to content domain.

- [ ] **Step 3: Commit**

```bash
cd /Users/wuzhijing/learning/workflows/pm-demo1/reliable-dev-harness
git add -A
git commit -m "feat(router): add dual-domain routing with content skill triggers and domain filter"
```

---

## Task 7: Update check-harness.py — Add content skill verification

**Files:**
- Modify: `.claude/check-harness.py`

**Context:** Current check only verifies 8 dev skills in flat structure. Need to update paths to `dev/` subdirectory and add 4 content skills.

- [ ] **Step 1: Write updated check-harness.py**

Replace the entire content of `.claude/check-harness.py` with:

```python
#!/usr/bin/env python3
"""
Harness Health Check - Dual-Track Edition
Verify that the Harness infrastructure is intact for both dev and content domains.
"""

import sys
from pathlib import Path

ROOT = Path(__file__).parent
ISSUES = []

DEV_SKILLS = [
    "product-spec-builder",
    "design-brief-builder",
    "design-maker",
    "dev-planner",
    "dev-builder",
    "bug-fixer",
    "code-review",
    "release-builder",
]

CONTENT_SKILLS = [
    "script-writer",
    "visual-designer",
    "tts-engine",
    "video-compositor",
]

STATE_FILES = [
    "state/L1-summary.md",
    "state/L2-spec.md",
    "state/L3-design.md",
    "state/L4-plan.md",
    "state/L5-media.md",
]

DOC_FILES = [
    "CLAUDE.md",
    "docs/HARNESS-ARCHITECTURE.md",
    "docs/EVOLUTION-PROTOCOL.md",
    "docs/CONTENT-PIPELINE.md",
]


def check_skills():
    skills_dir = ROOT / "skills"
    
    # Check dev skills
    for name in DEV_SKILLS:
        skill_md = skills_dir / "dev" / name / "SKILL.md"
        exit_check = skills_dir / "dev" / name / "exit-check.py"
        if not skill_md.exists():
            ISSUES.append(("dev_skill_missing", f"Dev skill SKILL.md not found: {skill_md}"))
        if not exit_check.exists():
            ISSUES.append(("dev_exit_check_missing", f"Dev skill exit-check.py not found: {exit_check}"))
    
    # Check content skills
    for name in CONTENT_SKILLS:
        skill_md = skills_dir / "content" / name / "SKILL.md"
        exit_check = skills_dir / "content" / name / "exit-check.py"
        if not skill_md.exists():
            ISSUES.append(("content_skill_missing", f"Content skill SKILL.md not found: {skill_md}"))
        if not exit_check.exists():
            ISSUES.append(("content_exit_check_missing", f"Content skill exit-check.py not found: {exit_check}"))


def check_hooks():
    hooks_dir = ROOT / "hooks"
    expected = ["pre-commit-check.sh", "stop-gate.sh", "content-validator.sh"]
    for name in expected:
        if not (hooks_dir / name).exists():
            ISSUES.append(("hook_missing", f"{hooks_dir / name} not found"))


def check_state():
    state_dir = ROOT / "state"
    if not state_dir.exists():
        ISSUES.append(("state_dir_missing", f"{state_dir} not found"))
    else:
        for name in STATE_FILES:
            if not (state_dir / name).exists():
                ISSUES.append(("state_file_missing", f"State file not found: {state_dir / name}"))


def check_docs():
    for doc in DOC_FILES:
        if not (ROOT / doc).exists():
            ISSUES.append(("doc_missing", f"Doc not found: {ROOT / doc}"))


def main() -> int:
    check_skills()
    check_hooks()
    check_state()
    check_docs()

    if not ISSUES:
        print("✅ Harness health check passed. Both dev/ and content/ domains are intact.")
        return 0

    print("❌ Harness health issues detected:\n")
    for code, detail in ISSUES:
        print(f"  [{code}] {detail}")
    print()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 2: Create placeholder state files**

```bash
cd /Users/wuzhijing/learning/workflows/pm-demo1/reliable-dev-harness/.claude/state

# Create L2-L5 with content-domain-aware templates
cat > L2-spec.md << 'EOF'
# Content Spec

## Metadata
<!-- Filled by script-writer -->
- Platform: 
- Mood: 
- Target Duration: 

## Scene Summary
<!-- Auto-generated from scenes.json -->

## Source
- Input: 
- Scenes: scenes.json
EOF

cat > L3-design.md << 'EOF'
# Visual Design Spec

## Design Decision
<!-- Filled by visual-designer -->
- Mood: 
- Platform: 
- Style: 
- Primary Color: 
- Font Pair: 

## Assets
<!-- Auto-generated -->

## Slides Structure
<!-- Auto-generated -->
EOF

cat > L4-plan.md << 'EOF'
# Pipeline Progress

## Current Phase
<!-- Tracks which content skill is active -->
- Active Skill: 
- Gate Status: 
- Next Step: 

## Completed Phases
<!-- List of completed skills with timestamps -->
EOF

cat > L5-media.md << 'EOF'
# Media Asset Manifest

## Audio
| Scene | File | Duration |
|-------|------|----------|
<!-- Filled by tts-engine -->

## Subtitles
- File: subtitles.json
- Total entries: 
- Total duration: 

## TTS Config
- Preset: 
- Voice: 
- Speed: 

## Video Output
<!-- Filled by video-compositor -->
- Base video: 
- Final video: 
EOF
```

- [ ] **Step 3: Create content-validator.sh hook**

Create `.claude/hooks/content-validator.sh`:

```bash
#!/bin/bash
# Content Validator Hook
# Runs exit-checks for content domain skills
# Called by Orchestrator at content pipeline gate points

set -e

SKILLS_DIR="$(dirname "$0")/../skills/content"

echo "🔍 Content Validator Hook"

# Determine which content skill to validate based on argument
SKILL="${1:-}"

if [ -z "$SKILL" ]; then
    echo "Usage: $0 <script-writer|visual-designer|tts-engine|video-compositor>"
    exit 1
fi

EXIT_CHECK="$SKILLS_DIR/$SKILL/exit-check.py"

if [ ! -f "$EXIT_CHECK" ]; then
    echo "❌ Exit check not found: $EXIT_CHECK"
    exit 1
fi

echo "Running exit check for: content/$SKILL"
python3 "$EXIT_CHECK"
EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    echo "✅ content/$SKILL passed exit check"
else
    echo "❌ content/$SKILL failed exit check (exit code: $EXIT_CODE)"
    echo "   Fix the issues above before proceeding."
fi

exit $EXIT_CODE
```

```bash
chmod +x /Users/wuzhijing/learning/workflows/pm-demo1/reliable-dev-harness/.claude/hooks/content-validator.sh
```

- [ ] **Step 4: Run check-harness.py to see current state**

```bash
cd /Users/wuzhijing/learning/workflows/pm-demo1/reliable-dev-harness
python3 .claude/check-harness.py
```

Expected: Will show missing content skills until Task 2-5 create them. After all tasks complete, should pass.

- [ ] **Step 5: Commit**

```bash
cd /Users/wuzhijing/learning/workflows/pm-demo1/reliable-dev-harness
git add -A
git commit -m "feat(harness): update check-harness for dual-track, add content-validator hook and L2-L5 state templates"
```

---

## Task 8: Update CLAUDE.md — Dual-domain orchestrator protocol

**Files:**
- Modify: `.claude/CLAUDE.md`

**Context:** CLAUDE.md is the Orchestrator protocol. Need to add content domain routing, Creative Gate flow, and dual-track pipeline description.

- [ ] **Step 1: Update CLAUDE.md with dual-domain protocol**

Add the following sections to `.claude/CLAUDE.md` (append after the existing "Skill 调用路由" section, before "与用户交互的风格"):

New sections to add:

```markdown
---

## 内容生产标准流程

与软件开发流程并行，内容生产有自己的 Skill 链：

```
口播稿/主题 → content/script-writer → [Hard Gate] → [Creative Gate: 平台+场景]
    ↓ 通过
content/visual-designer:
  图片步骤 → [Creative Gate: 图片确认]
  HTML步骤 → [Hard Gate] → [Creative Gate: 风格确认]
    ↓ 通过
content/tts-engine → [Hard Gate] → [Creative Gate: TTS风格 (可跳过)]
    ↓ 通过
content/video-compositor → [Hard Gate] → [Creative Gate: 最终视频确认]
    ↓ 通过
Done → 视频产出物
```

### 双网关机制（Dual Gate）

内容生产 Skill 有**两类**网关：

1. **Hard Gate**（确定性验证）— 由 `exit-check.py` 执行
   - 文件存在、格式合法、数值阈值
   - 二元通过/失败，没有例外

2. **Creative Gate**（人类判断点）— 由 Orchestrator 在 Skill 过渡时执行
   - 风格偏好、场景拆分、视觉满意度
   - 默认不可跳过，但可标记为 "configurable skip"

### Creative Gate 规则

- Creative Gate 不可跳过（除非用户明确配置为可跳过）
- 用户不满意时，回到**当前 Skill** 重新执行，而非修改上游 Skill 的输出
- 每次通过 Creative Gate 的选择，记录到对应的 state 文件（L2-L5）

---

## 内容生产领域路由

当用户输入匹配内容关键词（口播、视频、script、场景、配图、TTS、配音、渲染、合成等），路由到 content/ Skill。

当无法确定领域时，**询问用户**选择 dev 还是 content 路径。

---

## Steering Loop 适配

内容生产的反馈毕业阈值为 **≥5 次同类反馈**（vs 软件开发的 ≥3 次）：
- 原因：主观偏好需要更多样本才能提炼规则
- 自动提案：✅
- 自动写入规则：❌（仍需人类确认）
```

Also update the "五层架构" section to add L5-media.md:

Change the L4-only state list to include L5:
```markdown
| L4 | `state/L4-plan.md` | 开发计划(content: 流水线进度) | < 1000 tokens |
| L5 | `state/L5-media.md` | 媒体资产清单(content only) | As needed |
```

- [ ] **Step 2: Verify CLAUDE.md updates**

```bash
wc -l /Users/wuzhijing/learning/workflows/pm-demo1/reliable-dev-harness/.claude/CLAUDE.md
```

Expected: Significantly more lines than the original 172.

- [ ] **Step 3: Commit**

```bash
cd /Users/wuzhijing/learning/workflows/pm-demo1/reliable-dev-harness
git add -A
git commit -m "feat(orchestrator): add dual-domain routing protocol, Creative Gate mechanism, and L5 state support to CLAUDE.md"
```

---

## Task 9: Update HARNESS-ARCHITECTURE.md — Add dual-track documentation

**Files:**
- Modify: `.claude/docs/HARNESS-ARCHITECTURE.md`

**Context:** Need to add content domain documentation to the existing architecture doc, updating the five-layer model and adding the content pipeline flow.

- [ ] **Step 1: Add content domain section to HARNESS-ARCHITECTURE.md**

Append the following section after the "与 Product-Manager-Skills 的关系" section:

```markdown

---

## 内容生产领域（Content Domain）

### 设计原则

内容生产领域的 Skill 遵循与软件开发相同的核心原则——Hard Gate、Context Firewall、Steering Loop——但有两处关键适配：

1. **Creative Gate**：内容生产引入了"人类判断点"，用于验证 Hard Gate 无法判断的主观质量（风格、排版、语音自然度）。
2. **Steering Loop 毕业阈值**：≥5 次同类反馈（vs 软件开发的 ≥3 次），因为主观偏好需要更多样本才能提炼规则。

### 双网关模型

```
Skill 完成 → [Hard Gate: exit-check.py] → 通过 → [Creative Gate: 人类确认] → 通过 → 下一个 Skill
                ↓ 失败                       ↓ 不满意
              退回当前 Skill 修复          退回当前 Skill 重做（不是修改上游）
```

Hard Gate 检查机器可判定的事实（文件存在、格式合法、数值阈值）。
Creative Gate 检查需要审美或编辑判断的质量（风格偏好、视觉满意度）。

### Skill 分解

self-media-video 的单体 G0-G4 流程被拆分为 4 个专注于单一职责的 Skill：

| Skill | 覆盖原流程 | Hard Gate | Creative Gate |
|-------|----------|-----------|---------------|
| script-writer | G0+G1 | scenes.json 结构验证 | 平台选择 + 场景确认 |
| visual-designer | G2+G3 | HTML + data-beat-at + 图片存在 | 3 Style Previews + 图片确认 |
| tts-engine | G4a | 音频文件 + 字幕格式 + 时长偏差 | TTS 风格选择 (可跳过) |
| video-compositor | G4b | 分辨率 + fps + 时长匹配 | 最终视频确认 |

### 状态管理扩展

内容生产引入 L5-media.md 用于跟踪媒体资产：

| 层级 | 文件 | 内容含义 |
|------|------|---------|
| L1 | L1-summary.md | 项目概览 (共享) |
| L2 | L2-spec.md | 内容规格 (content) / 产品规格 (dev) |
| L3 | L3-design.md | 视觉设计 (content) / 设计规范 (dev) |
| L4 | L4-plan.md | 流水线进度 (content) / 开发计划 (dev) |
| L5 | L5-media.md | 媒体资产清单 (content only) |

### frontend-slides 集成

visual-designer 是编排器，委托 HTML 幻灯片生成给外部 `frontend-slides` 技能：

- **visual-designer** 处理：场景→幻灯片数据转换、平台覆盖 CSS、beat 属性注入、图片管理
- **frontend-slides** 处理：Mood Selection、3 Style Previews、HTML 生成、视觉设计质量

frontend-slides 不需要知道"视频"——它产出的幻灯片被 visual-designer 后处理为视频可用格式。
```

- [ ] **Step 2: Commit**

```bash
cd /Users/wuzhijing/learning/workflows/pm-demo1/reliable-dev-harness
git add -A
git commit -m "docs(architecture): add content domain documentation with dual-gate model and skill breakdown"
```

---

## Task 10: Write CONTENT-PIPELINE.md — Content production flow documentation

**Files:**
- Create: `.claude/docs/CONTENT-PIPELINE.md`

- [ ] **Step 1: Write CONTENT-PIPELINE.md**

Create `.claude/docs/CONTENT-PIPELINE.md`:

```markdown
# Content Pipeline — 口播视频生产流程说明书

> 本文档描述 Reliable Dev Harness 内容生产领域的标准工作流。
> 配合 `HARNESS-ARCHITECTURE.md` 和 `CLAUDE.md` 阅读。

## 概览

内容生产流水线将口播文稿（Markdown）转化为带配音、动画、字幕的短视频。整个流程分为 4 个 Skill，每个 Skill 有 Hard Gate（确定性验证）和 Creative Gate（人类判断点）双重保证。

```
口播稿 ──→ script-writer ──→ visual-designer ──→ tts-engine ──→ video-compositor ──→ 最终视频
              G0+G1              G2+G3              G4a               G4b
           [H+CG]            [H+CG]            [H+CG]           [H+CG]
```

H = Hard Gate (exit-check.py)
CG = Creative Gate (人类确认)

## Skill 1: script-writer — 口播文稿解析与场景拆分

- **输入**: Markdown 口播文稿 或 主题描述
- **输出**: `scenes.json` + `state/L2-spec.md`
- **Hard Gate**: scenes.json 结构验证（有效 JSON，2-15 个场景，必有字段）
- **Creative Gate**: 平台选择 (9:16/16:9/4:5) + Mood + 场景拆分确认

### scenes.json 结构

```json
{
  "scenes": [
    {
      "id": "scene-01",
      "text": "口播文本内容",
      "estimatedDuration": 8,
      "visualBeats": [
        {"timeMs": 0, "type": "hook", "description": "问号符号动画"}
      ]
    }
  ]
}
```

## Skill 2: visual-designer — 视觉设计与HTML幻灯片编排

- **输入**: scenes.json + L2-spec + L3-design
- **输出**: `slides-preview.html` + 图片资产
- **Hard Gate**: HTML 有效、包含 data-beat-at 和平台 CSS、图片存在
- **Creative Gate**: 3 Style Previews 选择 + 图片确认 + 最终 HTML 预览

### 与 frontend-slides 的关系

```
visual-designer (编排器)          frontend-slides (执行器)
├── 场景→幻灯片数据转换            ├── Mood Selection 流程
├── 图片策略与管理                  ├── 3 Style Previews 生成
├── 平台覆盖 CSS 注入              ├── HTML 幻灯片渲染
├── data-beat-at 属性注入          └── 视觉设计质量保证
└── 字幕区/动画预设注入
```

## Skill 3: tts-engine — 语音合成与字幕生成

- **输入**: scenes.json (text 字段) + TTS 预设
- **输出**: `audio/` 目录 (每个场景一个 .mp3) + `subtitles.json`
- **Hard Gate**: 音频文件完整、字幕格式有效、时长偏差 ±30%
- **Creative Gate**: TTS 风格选择 (标记为 configurable skip)

### TTS 预设表

| Preset | 风格 | 音色 | 语速 |
|--------|------|------|------|
| 专业科普-女 | 清晰正式 | YunyangNeural | +0% |
| 专业科普-男 | 沉稳深度 | YunhaoNeural | -5% |
| 轻松闲聊-女 | 亲切活人感 | XiaoshuangNeural | +5% |
| 轻松闲聊-男 | 随和自然 | YunxiNeural | +0% |
| 激情解说-男 | 高能量快节奏 | YunzeNeural | +10% |
| 温柔讲述-女 | 柔和缓慢 | XiaohanNeural | -10% |

## Skill 4: video-compositor — 视频合成与输出

- **输入**: slides-preview.html + audio/ + subtitles.json + scenes.json
- **输出**: `final-video.mp4`
- **Hard Gate**: base-video 存在、分辨率匹配、fps ≥ 24、时长偏差 ±5%
- **Creative Gate**: 最终视频确认

### Remotion 渲染流程

```
slides-preview.html → Remotion Video 组件 → base-video.mp4
                                              ↓
base-video.mp4 + audio/ → ffmpeg 合成 → final-video.mp4
```

## 状态文件流转

| 阶段 | 写入 | 读取 |
|------|------|------|
| script-writer | L2-spec.md, scenes.json | L1-summary.md |
| visual-designer | L3-design.md, slides-preview.html | L2-spec.md, scenes.json |
| tts-engine | L5-media.md, audio/, subtitles.json | L2-spec.md, L3-design.md, scenes.json |
| video-compositor | L5-media.md (video section) | L2-spec.md, L5-media.md |

## 异常处理

- **Hard Gate 失败**: 退回当前 Skill 修复，不能进入下一个 Skill
- **Creative Gate 不满意**: 退回当前 Skill 重做（不是修改上游 Skill）
- **音频时长超偏差**: 需要回到 script-writer 重新评估场景拆分
- **视频渲染失败**: 检查 Remotion 项目模板配置和 slides-preview.html 有效性

## 迁移来源

本流水线从 `self-media-video` 技能（单体 G0-G4）拆分而来。原有资产分布：

| self-media-video 资产 | 目标位置 |
|----------------------|---------|
| G0-G1 逻辑 | content/script-writer/SKILL.md |
| G2 逻辑 | content/visual-designer/SKILL.md |
| G3 HTML 生成 | 委托给 frontend-slides 技能 |
| G4a TTS+字幕 | content/tts-engine/SKILL.md |
| G4b Remotion 渲染 | content/video-compositor/SKILL.md |
| templates/ | content/visual-designer/templates/ |
| project-template/ | content/video-compositor/project-template/ |
| scripts/parse-script.ts | content/script-writer/scripts/ |
| scripts/tts-*.ts | content/tts-engine/scripts/ |
| scripts/render-*.ts | content/video-compositor/scripts/ |
```

- [ ] **Step 2: Commit**

```bash
cd /Users/wuzhijing/learning/workflows/pm-demo1/reliable-dev-harness
git add -A
git commit -m "docs(content): add CONTENT-PIPELINE.md with full content production flow documentation"
```

---

## Task 11: End-to-end validation — Run check-harness and verify all components

**Context:** After all previous tasks, run the full health check to verify the dual-track architecture is complete.

- [ ] **Step 1: Run check-harness.py and fix any issues**

```bash
cd /Users/wuzhijing/learning/workflows/pm-demo1/reliable-dev-harness
python3 .claude/check-harness.py
```

Expected: ✅ Harness health check passed. If not, fix the reported issues.

- [ ] **Step 2: Test router.py with content queries**

```bash
cd /Users/wuzhijing/learning/workflows/pm-demo1/reliable-dev-harness
python3 .claude/router.py "制作口播视频" --domain content
python3 .claude/router.py "实现登录功能" --domain dev
python3 .claude/router.py "TTS配音"
```

Expected: Content queries return content/ skills, dev queries return dev/ skills.

- [ ] **Step 3: Test content-validator.sh hook**

```bash
cd /Users/wuzhijing/learning/workflows/pm-demo1/reliable-dev-harness
bash .claude/hooks/content-validator.sh script-writer
```

Expected: exit-check.py runs (will fail since no scenes.json exists yet, but the hook itself should work).

- [ ] **Step 4: Verify all skill SKILL.md files exist**

```bash
find /Users/wuzhijing/learning/workflows/pm-demo1/reliable-dev-harness/.claude/skills -name "SKILL.md" | sort
```

Expected: 12 SKILL.md files (8 dev + 4 content).

- [ ] **Step 5: Verify all exit-check.py files exist**

```bash
find /Users/wuzhijing/learning/workflows/pm-demo1/reliable-dev-harness/.claude/skills -name "exit-check.py" | sort
```

Expected: 12 exit-check.py files (8 dev + 4 content).

- [ ] **Step 6: Verify state files exist**

```bash
ls -la /Users/wuzhijing/learning/workflows/pm-demo1/reliable-dev-harness/.claude/state/
```

Expected: L1-summary.md, L2-spec.md, L3-design.md, L4-plan.md, L5-media.md, task-history.yaml.

- [ ] **Step 7: Verify docs exist**

```bash
ls -la /Users/wuzhijing/learning/workflows/pm-demo1/reliable-dev-harness/.claude/docs/
ls -la /Users/wuzhijing/learning/workflows/pm-demo1/reliable-dev-harness/docs/
```

Expected: HARNESS-ARCHITECTURE.md, EVOLUTION-PROTOCOL.md, CONTENT-PIPELINE.md in .claude/docs/.

- [ ] **Step 8: Final commit if any fixes were needed**

```bash
cd /Users/wuzhijing/learning/workflows/pm-demo1/reliable-dev-harness
git add -A
git commit -m "fix: address harness health check issues after dual-track migration"
```

---

## Open Questions to Resolve During Implementation

1. **frontend-slides integration method**: How exactly does visual-designer invoke frontend-slides? Options:
   - Load SKILL.md and follow instructions (Claude Code approach)
   - Subprocess call (if frontend-slides has a CLI)
   - Task delegation (orchestrator delegates to frontend-slides agent)
   **Recommendation**: Defer to implementation time. The SKILL.md should document all three approaches and let the orchestrator choose based on runtime.

2. **State template content**: L2-spec.md through L5-media.md need content-production-specific templates. The plan includes placeholder templates. Actual content will be shaped by real usage through the Steering Loop.

3. **content-validator.sh scope**: The hook currently takes a skill name and runs its exit-check. Whether it runs automatically after each Skill or only before final output is an operational decision, not a design constraint. The SKILL.md will document the recommended flow.

4. **Multi-session resilience**: L4-plan.md tracks pipeline progress. If a session is interrupted, the Orchestrator reads L4 to determine which Skill needs to resume. This is documented in the CLAUDE.md update.

5. **Self-media-video retirement**: After all content skills are implemented and tested, the original `self-media-video` skill can be deprecated. The migration table in CONTENT-PIPELINE.md documents where each asset went. No timeframe is set — retirement happens when the content pipeline is proven stable.