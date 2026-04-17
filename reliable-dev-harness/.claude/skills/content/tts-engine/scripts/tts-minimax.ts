/**
 * MiniMax TTS 集成脚本
 * 使用 MiniMax TTS API 生成语音
 *
 * CLI 用法:
 *   MINIMAX_API_KEY=your-key npx tsx scripts/tts-minimax.ts --text "你好" --output audio.mp3
 *   MINIMAX_API_KEY=your-key npx tsx scripts/tts-minimax.ts --text "你好" --voice male-qn_qingse --speed 1.0 --output audio.mp3
 *
 * 环境变量:
 *   MINIMAX_API_KEY - MiniMax API 密钥
 */

import { existsSync, mkdirSync, writeFileSync } from "fs";
import { dirname, join } from "path";
import { fileURLToPath } from "url";

export interface MiniMaxTTSOptions {
  text: string;
  outputPath: string;
  voiceId?: string;  // e.g., "male-qn_qingse", "female-qb_xiaomeng"
  speed?: number;     // 0.5 - 2.0, default 1.0
  pitch?: number;     // -500 - 500, default 0
  volume?: number;    // -500 - 500, default 0
}

const DEFAULT_VOICE_ID = "male-qn_qingse";
const API_BASE = "https://api.minimaxi.com/v1/t2a_v2";

/**
 * 使用 MiniMax TTS API 生成音频
 */
export async function generateMiniMaxTTS(options: MiniMaxTTSOptions): Promise<{ outputPath: string; duration: number }> {
  const {
    text,
    outputPath,
    voiceId = DEFAULT_VOICE_ID,
    speed = 1.0,
    pitch = 0,
    volume = 0,
  } = options;

  const apiKey = process.env.MINIMAX_API_KEY;
  if (!apiKey) {
    throw new Error("MINIMAX_API_KEY environment variable is required");
  }

  // 确保输出目录存在
  const dir = dirname(outputPath);
  if (!existsSync(dir)) {
    mkdirSync(dir, { recursive: true });
  }

  console.log(`Calling MiniMax TTS API...`);
  console.log(`  Text: ${text.slice(0, 50)}${text.length > 50 ? "..." : ""}`);
  console.log(`  Voice: ${voiceId}, Speed: ${speed}`);

  const response = await fetch(API_BASE, {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${apiKey}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      model: "speech-02",
      text,
      stream: false,
      voice_setting: {
        voice_id: voiceId,
        speed,
        pitch,
        volume,
      },
      audio_setting: {
        audio_format: "mp3",
        sample_rate: 32000,
        bitrate: 128000,
      },
    }),
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(`MiniMax API error ${response.status}: ${errorText}`);
  }

  // MiniMax API 直接返回音频二进制数据
  const audioBuffer = await response.arrayBuffer();
  const buffer = Buffer.from(audioBuffer);

  writeFileSync(outputPath, buffer);
  console.log(`Audio saved to ${outputPath}`);

  // 测量音频时长
  const duration = await measureAudioDuration(outputPath);

  return { outputPath, duration };
}

/**
 * 测量音频文件时长（秒）
 */
export async function measureAudioDuration(audioPath: string): Promise<number> {
  try {
    const { execSync } = await import("child_process");
    const output = execSync(
      `ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "${audioPath}"`,
      { encoding: "utf-8" }
    );
    const duration = parseFloat(output.trim());
    return isNaN(duration) ? 0 : Math.round(duration * 100) / 100;
  } catch {
    // ffprobe 不可用时返回估算值
    return 0;
  }
}

/**
 * 列出 MiniMax 可用的语音 ID（需要实际调用 API 获取）
 */
export async function listMiniMaxVoices(): Promise<string[]> {
  // MiniMax 文档中列出的语音
  return [
    "male-qn_qingse",
    "female-qb_xiaomeng",
    "female-qb_xiaoyuan",
    "male-qn_xiaobai",
    "male-qn_yunxi",
  ];
}

// ============ CLI 入口 ============

interface CLIOptions {
  text?: string;
  output?: string;
  voice?: string;
  speed?: string;
  listVoices?: boolean;
}

function parseArgs(): CLIOptions {
  const args = process.argv.slice(2);
  const opts: CLIOptions = {};

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    switch (arg) {
      case "--text":
        opts.text = args[++i];
        break;
      case "--output":
        opts.output = args[++i];
        break;
      case "--voice":
        opts.voice = args[++i];
        break;
      case "--speed":
        opts.speed = args[++i];
        break;
      case "--list-voices":
        opts.listVoices = true;
        break;
    }
  }

  return opts;
}

async function main() {
  const opts = parseArgs();

  if (opts.listVoices) {
    console.log("Available MiniMax voices:");
    const voices = await listMiniMaxVoices();
    voices.forEach(v => console.log(`  ${v}`));
    return;
  }

  if (!opts.text) {
    console.error("Error: --text is required");
    console.error("Usage: MINIMAX_API_KEY=xxx npx tsx scripts/tts-minimax.ts --text \"你好\" --output audio.mp3 [--voice male-qn_qingse] [--speed 1.0]");
    process.exit(1);
  }

  if (!opts.output) {
    console.error("Error: --output is required");
    process.exit(1);
  }

  if (!process.env.MINIMAX_API_KEY) {
    console.error("Error: MINIMAX_API_KEY environment variable is required");
    process.exit(1);
  }

  try {
    const result = await generateMiniMaxTTS({
      text: opts.text,
      outputPath: opts.output,
      voiceId: opts.voice,
      speed: opts.speed ? parseFloat(opts.speed) : undefined,
    });

    console.log(`\nAudio generated successfully!`);
    console.log(`  Duration: ${result.duration} seconds`);
    console.log(`  File: ${result.outputPath}`);
  } catch (error) {
    console.error(`\nError: ${error instanceof Error ? error.message : String(error)}`);
    process.exit(1);
  }
}

if (import.meta.url === `file://${process.argv[1]}`) {
  main();
}
