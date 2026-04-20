# Self Media Video Template

Remotion 项目模板，用于从自媒体口播稿生成短视频。支持竖屏(9:16)、横屏(16:9)、小红书种草版(4:5)三种平台格式。

## 快速开始

### 1. 安装依赖

```bash
cd project-template
npm install
```

### 2. 预览模板

```bash
npm start
```

在浏览器中打开 Remotion Studio，查看默认示例视频。

### 3. 自定义内容

编辑 `src/scenes.json`，替换为你的场景数据：

```json
{
  "scenes": [
    {
      "id": "scene-1",
      "type": "开场钩子",
      "text": "你的开场钩子文案",
      "estimatedDuration": 90,
      "animationHint": "typewriter",
      "keyWords": ["钩子", "关键词"],
      "visualFocus": "纯文字",
      "visualType": "title"
    }
  ],
  "platform": "douyin"
}
```

## 平台预设

| 平台 | 比例 | 分辨率 |
|------|------|--------|
| `douyin` / `instagram` | 9:16 | 1080x1920 |
| `youtube` / `bilibili` / `weibo` | 16:9 | 1920x1080 |
| `xiaohongshu` | 4:5 | 1080x1350 |

## 渲染视频

### 方式一：两段式渲染（推荐）

```bash
# Step 1: 使用 Playwright 生成 base-video.mp4
npx tsx scripts/render-base-video.ts

# Step 2: 使用 Remotion 合成最终视频
npx remotion render src/index.tsx base-video --output=final-video.mp4
```

### 方式二：直接 Remotion 渲染

```bash
npm run build
```

## 项目结构

```
project-template/
├── src/
│   ├── index.tsx              # Remotion 入口
│   ├── Root.tsx               # 根组件，定义合成
│   ├── Video.tsx              # 主视频合成组件
│   ├── Subtitles.tsx          # 字幕组件
│   ├── KenBurnsVideo.tsx      # Ken Burns 视频效果
│   ├── BeatOverlay.tsx        # 节拍覆盖效果
│   ├── scenes.d.ts            # 场景类型定义
│   ├── scenes.json            # 场景数据（由 script-writer 产出）
│   ├── types.ts               # 全局类型定义（含平台/TTS预设）
│   ├── styles/
│   │   └── globals.css        # 全局样式
│   └── utils/
│       ├── timing.ts          # 时间工具函数
│       └── subtitles.ts       # 字幕工具函数
├── scripts/
│   └── render-base-video.ts   # Playwright 基础视频渲染
├── public/
│   └── template.md            # 本文档
├── package.json
├── tsconfig.json
└── remotion.config.ts
```

## TTS 音频集成

1. 使用 tts-engine 技能生成各场景音频（输出到 `audio/` 目录）
2. 运行 `render-base-video.ts` 时自动读取 `audio/` 和 `scenes.json`
3. 最终视频将包含音频和字幕 overlay

## 与 harness 技能配合

- **上游**：`content/script-writer` → 产出 `scenes.json`
- **上游**：`content/visual-designer` → 产出 `slides-preview.html`
- **本技能**：`content/video-compositor` → 合成 `base-video.mp4` + `final-video.mp4`
