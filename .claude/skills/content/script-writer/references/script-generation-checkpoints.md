# Script Generation Checkpoints

本文件在 script-writer 的**入口 B（topic 研究模式）**的阶段二使用。

用户从阶段一选定方向后，再使用这个文件。

## 核心原则

在真正写稿之前，先做"推荐型 checkpoint"，而不是直接让用户从零填写配置。

你需要先判断这个方向最适合怎么讲，再把推荐项给用户确认。

## 必选 checkpoint 类别

在写稿前，先分析已选方向，并对以下类别给出默认推荐：

1. Platform
2. Expression style
3. Intensity
4. Output format

然后请用户确认或调整。除非用户主动要求完全自定义，否则不要让用户每一项都从头选。

## 推荐优先流程

按这个结构输出：

1. State the selected topic in one sentence.
2. State the inferred audience assumption.
3. Give a recommended configuration with brief reasons:
   - Recommended platform
   - Recommended expression style
   - Recommended intensity
   - Recommended output format
4. Offer 2-3 useful alternatives only where they meaningfully change the result.
5. Ask the user to reply with `use recommended` or adjust any category.

推荐要有判断，不要含糊。这个 checkpoint 的目标是降低决策负担，同时保留人工介入。

## 平台选项

平台选择同时决定 harness 的 Platform 规格：

| 平台 | 典型场景 | harness Platform |
|------|---------|-----------------|
| Douyin / 抖音 | 短视频口播 | 9:16 |
| WeChat Channels / 视频号 | 私域传播 | 9:16 |
| Xiaohongshu video / 小红书视频 | 种草/经验分享 | 9:16 或 4:5 |
| Bilibili | 知识/深度内容 | 16:9 |
| Generic version | 通用横屏演示 | 16:9 |
| 社交媒体图片视频 | 朋友圈/信息流 | 4:5 |

## 表达风格选项

- rational analysis
- sharp commentary
- story-driven
- companion-style conversation
- knowledge-creator tone
- strong human feel

允许混搭，例如 `rational analysis + strong human feel`。

如果用户没有特别指定，而话题又偏观点表达或经验判断，优先考虑带一点"活人感"的组合，而不是纯知识播报腔。

**注意**：表达风格与 harness 的 Mood 是两个独立维度。Mood 决定视觉基调（配色、氛围），表达风格决定口播语言风格。两者都需写入 L2-content-spec.md。

## 内容力度选项

- conservative
- balanced
- strong point of view
- higher conflict

## 成稿规格选项

- short spoken outline
- 1-minute script
- 3-minute script
- 5-minute script
- partial draft
- full draft

## 受众处理

受众不是强制 checkpoint。你要主动推断最可能的受众，然后把这个假设说出来，让用户有机会修正。

## 可选高级控制项

只有在话题复杂、平台差异大、或者用户想更细控时，才引入这些额外选项：

- Opening structure: strong hook, story opening, question opening, conclusion first, contrast opening
- Persona tone: calm expert, friend-like conversation, sharp but not abusive, experienced observer, research creator, plain-spoken ordinary person
- Ending action: invite comments, leave an open question, closing line, soft follow, no call to action
- Risk boundary: safer wording, sharp but evidence-based, controversial but not personal, avoid attacking specific people or groups

如果启用高级控制项，也要先给默认推荐，不要甩给用户一大堆裸选项。

## 状态文件写入

用户确认配置后，将结果写入 `state/L2-content-spec.md`：

```markdown
## Metadata
- Platform: {9:16 | 16:9 | 4:5}
- Mood: {Impressed | Excited | Calm | Inspired}
- Expression Style: {rational analysis | sharp commentary | story-driven | ...}
- Intensity: {conservative | balanced | strong point of view | higher conflict}
- Target Duration: {N}s

## Source
- Input: topic (auto-generated draft)
- Draft: draft-script.md
- Scenes: scenes.json
```
