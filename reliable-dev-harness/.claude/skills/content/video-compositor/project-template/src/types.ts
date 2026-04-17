/**
 * Unified Scene Schema - Single source of truth for all stages
 * Data flow: scenes.json → HTML Slides (design source) → base-video.mp4 → Remotion overlay composition
 */

export const PLATFORM_PRESETS = {
  douyin:      { width: 1080, height: 1920, label: "抖音/小红书竖版 (9:16)" },
  instagram:   { width: 1080, height: 1920, label: "Instagram Reels (9:16)" },
  youtube:     { width: 1920, height: 1080, label: "YouTube/B站横版 (16:9)" },
  bilibili:    { width: 1920, height: 1080, label: "B站横版 (16:9)" },
  weibo:       { width: 1920, height: 1080, label: "微博 (16:9)" },
  xiaohongshu: { width: 1080, height: 1350, label: "小红书种草版 (4:5)" },
} as const;

export type PlatformKey = keyof typeof PLATFORM_PRESETS;
export type VisualFocus = "数据展示" | "概念解释" | "案例呈现" | "纯文字";
export type VisualType = "keyword-pill" | "big-number" | "quote" | "paragraph" | "title";
export type SceneType = "开场钩子" | "正文段落" | "结尾引导";
export type AnimationHint = "typewriter" | "fade" | "slide" | "emphasize";
export type ImageStyle =
  | "stardew-valley"
  | "watercolor"
  | "sketch"
  | "anime"
  | "photorealistic"
  | "abstract-geometric"
  | "vintage-illustration"
  | "minimal-line-art"
  | "pixel-art";

export type TTSPreset =
  | "专业科普-女"
  | "专业科普-男"
  | "轻松闲聊-女"
  | "轻松闲聊-男"
  | "激情带货-女"
  | "激情带货-男"
  | "温柔种草-女"
  | "深度讲解-男"
  | "快节奏资讯-男";

export type StylePreset =
  | "bold-signal"
  | "electric-studio"
  | "creative-voltage"
  | "dark-botanical"
  | "notebook-tabs"
  | "pastel-geometry"
  | "split-pastel"
  | "vintage-editorial"
  | "neon-cyber"
  | "terminal-green"
  | "swiss-modern"
  | "paper-ink";

export const TTS_VOICE_MAP: Record<TTSPreset, { voice: string; rate: string; provider: "edge" | "minimax" }> = {
  "专业科普-女":   { voice: "zh-CN-YunyangNeural",  rate: "+0%",  provider: "edge" },
  "专业科普-男":   { voice: "zh-CN-YunhaoNeural",   rate: "-5%",  provider: "edge" },
  "轻松闲聊-女":   { voice: "zh-CN-XiaoshuangNeural", rate: "+5%", provider: "edge" },
  "轻松闲聊-男":   { voice: "zh-CN-YunxiNeural",    rate: "+0%",  provider: "edge" },
  "激情带货-女":   { voice: "zh-CN-XiaoyiNeural",    rate: "+10%", provider: "edge" },
  "激情带货-男":   { voice: "zh-CN-YunxiNeural",    rate: "+15%", provider: "edge" },
  "温柔种草-女":   { voice: "zh-CN-XiaoshuangNeural", rate: "+0%", provider: "edge" },
  "深度讲解-男":   { voice: "zh-CN-YunhaoNeural",   rate: "-5%",  provider: "edge" },
  "快节奏资讯-男": { voice: "zh-CN-YunjianNeural",   rate: "+15%", provider: "edge" },
};

export interface SubtitleLine {
  text: string;
  startMs: number;
  endMs: number;
}

export interface VisualBeat {
  at: number;
  type: "hook-reveal" | "keyword-highlight" | "number-pop" | "quote-reveal" | "split-contrast";
  target?: string;
}

export interface Scene {
  id: string;
  type: SceneType;
  text: string;
  estimatedDuration: number;
  keyWords: string[];
  animationHint: AnimationHint;
  visualFocus: VisualFocus;
  visualType: VisualType;
  headline?: string;
  bullets?: string[];
  supportingText?: string;
  imageUrl?: string;
  imagePlacement?: "background" | "right" | "left" | "bottom" | "none";
  audioUrl?: string;
  audioDuration?: number;
  stylePreset?: StylePreset;
  subtitles?: SubtitleLine[];
  visualBeats?: VisualBeat[];
}

export interface ProjectConfig {
  title: string;
  style: string;
  duration: string;
  wordCount: number;
  platform: PlatformKey;
  imageStyle?: ImageStyle;
  ttsPreset?: TTSPreset;
  stylePreset?: StylePreset;
  scenes: Scene[];
}

export interface VideoProps {
  scenes: Scene[];
  platform?: PlatformKey;
}

export const VIDEO_FPS = 30;
export const TRANSITION_FRAMES = 15;
