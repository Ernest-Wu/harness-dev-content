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