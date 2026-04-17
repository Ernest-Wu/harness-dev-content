/**
 * Edge TTS 集成脚本
 * 使用 Python edge-tts CLI 生成中文语音
 *
 * CLI 用法:
 *   npx tsx scripts/tts-edge.ts --text "你好" --output audio.mp3
 *   npx tsx scripts/tts-edge.ts --text "你好" --voice zh-CN-YunxiNeural --output audio.mp3
 *   npx tsx scripts/tts-edge.ts --text "你好" --rate "+10%" --pitch "+5Hz" --output audio.mp3
 *   npx tsx scripts/tts-edge.ts --list-voices
 *
 * 依赖: pip install edge-tts
 */

import { execSync } from "child_process";
import { existsSync, mkdirSync } from "fs";
import { dirname } from "path";

export interface EdgeTTSOptions {
  text: string;
  outputPath: string;
  voice?:
    | "zh-CN-XiaoxiaoNeural"
    | "zh-CN-YunxiNeural"
    | "zh-CN-XiaoyiNeural"
    | "zh-CN-YunyangNeural"
    | "zh-CN-XiaoshuangNeural"
    | "zh-CN-YunjianNeural"
    | "zh-CN-YunhaoNeural";
  rate?: string;   // e.g., "+10%", "-5%"
  pitch?: string; // e.g., "+5Hz"
  volume?: string; // e.g., "+5%"
}

/**
 * 生成 Edge TTS 音频
 */
export async function generateEdgeTTS(options: EdgeTTSOptions): Promise<{ outputPath: string; duration: number }> {
  const {
    text,
    outputPath,
    voice = "zh-CN-XiaoxiaoNeural",
    rate = "+0%",
    pitch = "+0Hz",
    volume = "+0%",
  } = options;

  // 确保输出目录存在
  const dir = dirname(outputPath);
  if (!existsSync(dir)) {
    mkdirSync(dir, { recursive: true });
  }

  // edge-tts CLI 参数构建
  const args = [
    "--text", text,
    "--voice", voice,
    "--rate", rate,
    "--pitch", pitch,
    "--volume", volume,
    "--write-media", outputPath,
  ];

  try {
    // 执行 edge-tts CLI (Python 版本)
    execSync(`edge-tts ${args.join(" ")}`, {
      stdio: "pipe",
      encoding: "utf-8",
    });

    // 测量音频时长
    const duration = await measureAudioDuration(outputPath);

    return { outputPath, duration };
  } catch (error) {
    throw new Error(`Edge TTS failed: ${error instanceof Error ? error.message : String(error)}`);
  }
}

/**
 * 测量音频文件时长（秒）
 */
export async function measureAudioDuration(audioPath: string): Promise<number> {
  try {
    // 使用 ffprobe 测量时长
    const output = execSync(
      `ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "${audioPath}"`,
      { encoding: "utf-8" }
    );
    const duration = parseFloat(output.trim());
    return isNaN(duration) ? 0 : Math.round(duration * 100) / 100;
  } catch {
    // ffprobe 不可用时返回估算值（中文约 5 字/秒）
    return 0;
  }
}

/**
 * 列出所有可用的中文语音
 */
export async function listChineseVoices(): Promise<string[]> {
  try {
    // 使用 Python edge-tts CLI
    const output = execSync(`edge-tts --list-voices`, {
      encoding: "utf-8",
    });
    const lines = output.split("\n");
    const chineseVoices: string[] = [];
    for (const line of lines) {
      if (line.includes("zh-CN")) {
        chineseVoices.push(line.trim());
      }
    }
    return chineseVoices;
  } catch (error) {
    throw new Error(`Failed to list voices: ${error instanceof Error ? error.message : String(error)}`);
  }
}

// ============ CLI 入口 ============

interface CLIOptions {
  text?: string;
  output?: string;
  voice?: string;
  rate?: string;
  pitch?: string;
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
      case "--rate":
        opts.rate = args[++i];
        break;
      case "--pitch":
        opts.pitch = args[++i];
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
    console.log("Available Chinese voices:");
    const voices = await listChineseVoices();
    voices.forEach(v => console.log(`  ${v}`));
    return;
  }

  if (!opts.text) {
    console.error("Error: --text is required");
    console.error("Usage: npx tsx scripts/tts-edge.ts --text \"你好\" --output audio.mp3 [--voice zh-CN-XiaoxiaoNeural] [--rate \"+10%\"] [--pitch \"+5Hz\"]");
    process.exit(1);
  }

  if (!opts.output) {
    console.error("Error: --output is required");
    process.exit(1);
  }

  console.log(`Generating audio...`);
  console.log(`  Text: ${opts.text.slice(0, 50)}${opts.text.length > 50 ? "..." : ""}`);
  console.log(`  Voice: ${opts.voice || "zh-CN-XiaoxiaoNeural"}`);
  console.log(`  Rate: ${opts.rate || "+0%"}`);
  console.log(`  Pitch: ${opts.pitch || "+0Hz"}`);
  console.log(`  Output: ${opts.output}`);

  try {
    const result = await generateEdgeTTS({
      text: opts.text,
      outputPath: opts.output,
      voice: opts.voice as EdgeTTSOptions["voice"],
      rate: opts.rate,
      pitch: opts.pitch,
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
