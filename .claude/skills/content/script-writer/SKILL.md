---
name: script-writer
description: 将 Markdown 口播文稿或 topic/关键词转化为结构化场景拆分（scenes.json）和内容规格（L2-spec.md）。支持从 topic 自动研究选题并生成口播稿。口播视频生产线的起点。
intent: 双入口 Skill：入口 A 负责语义段落切分、平台选择、Mood 选择、visualBeats 标记；入口 B 负责从 topic 做深度研究、选题判断、生成口播稿。输出结构化的 scenes.json 和 L2-spec.md 供下游 visual-designer 使用。
type: component
---

# script-writer — 口播文稿解析与场景拆分

## Purpose

将 Markdown 口播文稿或主题描述转化为结构化的场景拆分（scenes.json）和内容规格（L2-spec.md），为后续视觉设计和视频合成提供可验证的输入。

支持两类输入起点：
- **已有口播文稿**：直接解析、拆分、标注 visualBeats
- **只有 topic/关键词**：先执行研究选题流程，生成口播稿后再进入拆分

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

### 表达风格（Expression Style）
决定口播语言风格，与 Mood 是独立维度。选项：rational analysis / sharp commentary / story-driven / companion-style conversation / knowledge-creator tone / strong human feel。

### 反模式（Anti-Patterns）
- ❌ 不要把标题/列表强行当作场景分割点——场景应该按语义段落切分
- ❌ 不要在场景文本中嵌入排版指令（如"放大"、"切换"）——这些属于 visualBeats
- ❌ 不要跳过 Creative Gate 直接进入 visual-designer——平台和风格的选择必须经人类确认
- ❌ 不要把研究写成资料堆砌——research 的目标是帮助选题判断，不是行业报告
- ❌ 不要把原观点/延展观点/对立观点压扁成近义改写——必须代表真正不同的内容路径

## Application

### 入口判断

script-writer 接受两类输入：

1. **入口 A**：用户已有 Markdown 口播文稿（或已有明确文稿内容）
2. **入口 B**：用户只有 topic / 关键词 / 初步想法，需要先做研究再生成文稿

判断方法：如果用户提供了可直接朗读的口播文本（Markdown 格式），走入口 A。如果用户只给了一个主题、关键词或模糊想法，走入口 B。

---

### 入口 A：已有口播文稿

#### 步骤 1：Creative Gate G0 — 平台与风格选择

与用户确认：
1. **目标平台**：短视频平台（9:16）、横屏演示（16:9）、社交媒体（4:5）
2. **Mood 选择**：Impressed / Excited / Calm / Inspired
3. **大致时长**：30秒-5分钟

如果用户已提供这些信息，确认即可。如果未提供，使用推荐默认值（9:16, Excited, 60-90秒）并请用户确认。

将确认结果写入 `state/L2-spec.md` 的头部 metadata。

#### 步骤 2：解析文稿为场景

1. 读取 Markdown 口播文稿
2. 按语义段落（不是按段落标记）拆分为 2-15 个场景
3. 每个场景包含：
   - `id`: "scene-01", "scene-02", ...
   - `text`: 口播文字（不是标题，是说出来的话）
   - `estimatedDuration`: 根据字数估算（中文约 4字/秒）
   - `visualBeats`: 数组，标记需要视觉变化的时刻（可以为空）
4. 输出 `scenes.json`

#### 步骤 3：Creative Gate G1 — 场景拆分确认

展示 scenes.json 摘要给用户：
- 场景数量和总时长
- 每个场景的关键词概要
- 预估的视觉节奏

等待用户确认或要求调整。

#### 步骤 4：更新状态文件

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
- Input: existing draft
- Original: {原始文稿路径或描述}
- Scenes: scenes.json
```

#### 步骤 5：Hard Gate — 运行 exit-check.py

```bash
python3 .claude/skills/content/script-writer/exit-check.py
```

退出码 ≠ 0 时，**必须修复后才能进入下一个 Skill**。

---

### 入口 B：只有 topic / 关键词

#### 前置步骤 1：阶段一 — 研究与选题

1. **理解输入**：分析用户真正想表达什么，而不是机械复述输入
2. **执行研究**：读取 `references/research-framework.md`，按深研究标准执行
   - 区分已确认事实、推断、观点、争议点
   - 主动指出限制条件和未知点
   - 不堆砌资料，只为选题判断服务
3. **输出选题方案**：读取 `references/topic-output-format.md`，产出阶段一结果
   - 输入理解（Input understanding）
   - 研究底稿（Research base）
   - 第一层候选池：5-8 个方向
   - 第二层深展开：自动精选 3 个方向
4. **阶段一结束**：必须停下，让用户选择

#### Creative Gate G0a — 选题确认（不可跳过）

展示 3 个深展开方向给用户，要求：
- 选择其中一个方向
- 或要求修改其中一个方向

**不允许**在此阶段直接生成口播稿。用户必须完成方向选择后，才能进入阶段二。

#### 前置步骤 2：阶段二 — 参数推荐与口播稿生成

用户选定方向后：

1. **读取 `references/script-generation-checkpoints.md`**
2. **给出推荐型 checkpoint**：
   - 平台（同时映射到 harness Platform：9:16 / 16:9 / 4:5）
   - 表达风格（Expression Style）
   - 内容力度（Intensity）
   - 成稿规格（Output format）
   - 默认带受众假设，但受众不是强制选择项
3. **说明推荐理由**：每项默认推荐都要解释为什么这样判断

#### Creative Gate G0b — 参数确认（不可跳过）

等待用户回复：
- `use recommended` — 采用全部推荐
- 或调整任意类别

用户确认后，将平台和 Mood 写入 `state/L2-spec.md` 的 Metadata。

#### 前置步骤 3：生成 draft-script.md

1. **读取 `references/writing-style-principles.md`**
2. **生成口播稿**，要求：
   - 可说、可念、像真人在讲
   - 保留观点锋芒，保留活人感
   - 按默认结构组织：Hook → Core claim → Reasoning beats → Turn/Contrast → Closing line
3. **输出 `draft-script.md`**

#### 汇合到入口 A

入口 B 完成后，`draft-script.md` 即为入口 A 的"已有口播文稿"。继续执行【入口 A】的步骤 2-5（解析文稿为场景 → Creative Gate G1 → 更新状态文件 → Hard Gate）。

注意：步骤 1（Creative Gate G0）在入口 B 中已通过 Creative Gate G0b 完成，不需要重复。

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
5. **研究变成资料堆砌**：research 的目标不是写成行业报告，而是帮助选题判断。只保留对内容策略有帮助的研究点。
6. **跳过阶段一 checkpoint**：不要从 topic 直接跳到成稿。用户必须在 3 个深展开方向中做选择。
7. **角度压扁成近义改写**：原观点、延展观点、对立观点必须代表真正不同的内容路径，不能只是换标题。
8. **表达风格与 Mood 混淆**：Mood 决定视觉基调（配色、氛围），表达风格决定口播语言风格。两者都要写入 L2-spec.md，但它们是两个独立维度。

## Exit-Check Criteria

运行 `exit-check.py` 检查：
1. `scenes.json` 存在且是有效 JSON
2. 每个场景有 `id`、`text`、`estimatedDuration`
3. 场景数量在 2-15 之间
4. `visualBeats` 数组存在（可以为空数组）
5. `state/L2-spec.md` 存在且包含 Platform 和 Mood 元数据
6. 如果 `L2-spec.md` 的 Source 标注 `Input: topic`，则 `draft-script.md` 必须存在且非空

## References

- 下游 Skill: `content/visual-designer`
- 状态管理: `.claude/state/L2-spec.md`
- 研究框架: `references/research-framework.md`
- 选题输出格式: `references/topic-output-format.md`
- 参数推荐: `references/script-generation-checkpoints.md`
- 口播稿风格: `references/writing-style-principles.md`
- 脚本解析器: `scripts/parse-script.ts`
- 迁移来源: self-media-video G0 + G1, self-media-research-script
