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