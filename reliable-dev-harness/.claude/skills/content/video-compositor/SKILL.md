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