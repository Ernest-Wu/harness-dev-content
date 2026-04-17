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