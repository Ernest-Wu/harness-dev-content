# Writing Style Principles

本文件在 script-writer 的**入口 B（topic 研究模式）**的阶段二使用，用于生成最终口播稿。

## 核心要求

最终稿必须满足三件事：

- 能说出口
- 有明确态度
- 像真人在讲

不要写成"模板在念字"，也不要写成"公众号长文硬改口播"。

## 口播语言规则

- Prefer sentence rhythms that can be spoken aloud comfortably.
- Allow occasional repetition when it helps emphasis or realism.
- Use transitions that feel like a person thinking through an idea, not a report template.
- Avoid over-polished, bureaucratic, or empty motivational phrasing.
- Keep one main idea per sentence.
- Avoid multi-layer subordinate clauses.
- Break long sentences into shorter spoken beats.
- Leave natural pauses where a speaker would breathe.
- Allow short spoken phrases and rhetorical questions.
- If a sentence feels like it needs more than one breath, split it.

## 活人感指导

当用户希望更强的"活人感"时：

- increase conversational phrasing
- keep a clear point of view
- allow emotional temperature where appropriate
- keep the language grounded instead of abstract
- use concrete scenes instead of abstract judgments
- keep a firm attitude without turning it into a slogan
- allow thinking traces like "I used to think..." or "At first I thought..."
- use human reaction lines to carry the point forward
- avoid stacking adjectives back to back

可以允许一点"人在边想边说"的痕迹，但不要因此失去结构感。

## 默认结构

默认按这个顺序组织：

1. Hook
2. Core claim
3. 2-3 spoken reasoning beats, with examples or consequences where useful
4. Turn, contrast, or response to an opposing view
5. Closing line
6. Optional title or cover line

## 节奏提醒

- 开场前两三句要尽快让人知道"这条内容为什么值得继续听"
- 论证部分不要连续堆三四层抽象判断，能落到场景就落到场景
- 如果要反驳对立面，先承认它为什么有吸引力，再给出你的拆解
- 结尾不要像总结报告；更像"话说到这，给你一个能记住的收束"

如果用户要的是提纲，就给结构和关键句；如果要的是完整稿，就写成可直接口播的自然语言。

## 输出格式

生成的口播稿写入 `draft-script.md`，格式为纯 Markdown：

```markdown
# {标题}

## 开场钩子
{Hook 内容，自然语言}

## 正文
### 段落1
{内容}

### 段落2
{内容}

## 结尾引导
{收束 + CTA（如有）}
```

段落之间用空行分隔，不要使用复杂的 Markdown 嵌套格式。
