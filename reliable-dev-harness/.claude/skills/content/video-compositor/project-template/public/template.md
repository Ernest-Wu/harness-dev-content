# Self Media Video Template

Remotion 项目模板，用于从自媒体口播稿生成竖屏短视频。

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

编辑 `src/Root.tsx` 中的 `defaultScenes` 数组，替换为你的内容：

```typescript
const defaultScenes: VideoProps["scenes"] = [
  {
    id: "scene-1",
    text: "你的开场钩子文案",
    type: "开场钩子",
    animationHint: "typewriter", // typewriter | fade | slide | emphasize
    estimatedDuration: 90,
  },
  {
    id: "scene-2",
    text: "你的正文内容",
    type: "正文段落",
    animationHint: "fade",
    estimatedDuration: 60,
  },
  {
    id: "scene-3",
    text: "你的结尾引导文案",
    type: "结尾引导",
    animationHint: "emphasize",
    estimatedDuration: 60,
  },
];
```

## 场景类型

| 类型 | 用途 | 默认颜色 |
|------|------|----------|
| `开场钩子` | 吸引观众注意力的开场 | 橙色 (#FF6B35) |
| `正文段落` | 主要内容叙述 | 蓝色 (#4A9EFF) |
| `结尾引导` | CTA 引导点赞、关注等 | 绿色 (#50C878) |

## 动画类型

| 动画 | 效果 | 适用场景 |
|------|------|----------|
| `typewriter` | 打字机效果，逐字显示 | 开场钩子、关键信息 |
| `fade` | 淡入淡出 | 正文段落 |
| `slide` | 滑入效果 | 强调重点 |
| `emphasize` | 缩放+光晕强调 | 关键金句、CTA |

## 主题

支持 `dark` (暗色) 和 `light` (亮色) 两种主题：

```typescript
<Video scenes={scenes} theme="dark" />
```

## 输出配置

- **分辨率**: 1080 x 1920 (竖屏 9:16)
- **帧率**: 30 fps
- **格式**: JPEG 序列

## 渲染视频

```bash
# 渲染并输出为 MP4
npm run build

# 或使用 Remotion CLI
npx remotion render SelfMediaVideo out/self-media-video.mp4
```

## TTS 音频集成

配合 TTS 生成音频，参考 `references/tts-guide.md`:

1. 使用 edge-tts 或 MiniMax TTS 生成音频
2. 获取音频时长
3. 根据时长调整 `estimatedDuration`

## 项目结构

```
project-template/
├── src/
│   ├── Root.tsx              # 入口，定义合成
│   ├── Video.tsx             # 主合成组件
│   ├── components/
│   │   ├── Scene.tsx         # 场景组件
│   │   ├── TitleSlide.tsx    # 标题幻灯片
│   │   └── TextAnimations.tsx # 文字动画
│   ├── styles/
│   │   └── globals.css       # 全局样式
│   └── utils/
│       └── timing.ts         # 时间工具函数
├── public/
│   └── template.md           # 本文档
├── package.json
├── tsconfig.json
└── remotion.config.ts
```

## 与 self-media-script 配合

此模板与 `self-media-script` 技能配合使用：

1. 使用 `self-media-script` 生成口播稿
2. 将口播稿解析为场景数组
3. 使用此模板渲染为视频

```typescript
// 口播稿转场景示例
const scriptToScenes = (script: string): VideoProps["scenes"] => {
  const paragraphs = script.split("\n\n");
  return paragraphs.map((text, i) => ({
    id: `scene-${i + 1}`,
    text,
    type: i === 0 ? "开场钩子" : i === paragraphs.length - 1 ? "结尾引导" : "正文段落",
    animationHint: i === 0 ? "typewriter" : i === paragraphs.length - 1 ? "emphasize" : "fade",
    estimatedDuration: Math.ceil(text.length * 3), // 估算每字 3 帧
  }));
};
```
