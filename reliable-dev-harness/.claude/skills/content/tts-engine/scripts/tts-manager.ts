/**
 * TTS 统一管理脚本
 * 统一管理 Edge TTS 和 MiniMax TTS，自动降级
 *
 * CLI 用法:
 *   npx tsx scripts/tts-manager.ts --scenes scenes.json --output-dir ./audio
 *   npx tsx scripts/tts-manager.ts --scenes scenes.json --output-dir ./audio --provider edge
 *   npx tsx scripts/tts-manager.ts --scenes scenes.json --output-dir ./audio --provider minimax
 *
 * 模块用法:
 *   import { generateSceneAudio, TTSManager } from "./tts-manager";
 */

import { existsSync, mkdirSync, readFileSync, writeFileSync } from "fs";
import { join, basename, dirname } from "path";
import { fileURLToPath } from "url";
import { generateEdgeTTS } from "./tts-edge.js";
import { generateMiniMaxTTS } from "./tts-minimax.js";
import { parseScript } from "./parse-script.js";

interface Scene {
  id: string;
  type: "开场钩子" | "正文段落" | "结尾引导";
  text: string;
  estimatedDuration: number;
  keyWords: string[];
  animationHint: "typewriter" | "fade" | "slide" | "emphasize";
  visualFocus?: string;
  visualType?: string;
  imageUrl?: string;
  audioUrl?: string;
  audioDuration?: number;
}

interface ParsedScript {
  title: string;
  style: string;
  duration: string;
  wordCount: number;
  scenes: Scene[];
}

function writeAudioResultsToScenes(scenesPath: string, results: SceneAudio[], outputDir: string): void {
  if (!existsSync(scenesPath)) return;

  const raw = readFileSync(scenesPath, "utf-8");
  const data = JSON.parse(raw);
  const scenes: Scene[] = data.scenes || data;

  for (const result of results) {
    if (!result.success) continue;
    const scene = scenes.find(s => s.id === result.sceneId);
    if (scene) {
      scene.audioUrl = result.audioPath.replace(outputDir + "/", "").replace(outputDir + path.sep, "");
      scene.audioDuration = result.duration;
    }
  }

  writeFileSync(scenesPath, JSON.stringify(data, null, 2), "utf-8");
  console.log(`\n音频结果已写回: ${scenesPath}`);
}

export interface TTSManagerOptions {
  outputDir: string;
  provider?: "edge" | "minimax" | "auto";
  voice?: string;
  rate?: string;
}

export interface SceneAudio {
  sceneId: string;
  audioPath: string;
  duration: number;  // 秒
  success: boolean;
  error?: string;
}

/**
 * TTS 管理器
 */
export class TTSManager {
  private options: Required<TTSManagerOptions>;
  private results: SceneAudio[] = [];

  constructor(options: TTSManagerOptions) {
    this.options = {
      outputDir: options.outputDir,
      provider: options.provider || "auto",
      voice: options.voice || "zh-CN-XiaoxiaoNeural",
      rate: options.rate || "+0%",
    };

    // 确保输出目录存在
    if (!existsSync(this.options.outputDir)) {
      mkdirSync(this.options.outputDir, { recursive: true });
    }
  }

  /**
   * 生成场景音频
   */
  async generateSceneAudio(scenes: Scene[]): Promise<SceneAudio[]> {
    this.results = [];
    const total = scenes.length;

    console.log(`\n开始生成 ${total} 个场景的音频...`);
    console.log(`Provider: ${this.options.provider}`);
    console.log(`Output dir: ${this.options.outputDir}`);
    console.log("");

    for (let i = 0; i < scenes.length; i++) {
      const scene = scenes[i];
      const progress = `[${i + 1}/${total}]`;

      console.log(`${progress} 处理场景 ${scene.id} (${scene.type})...`);

      try {
        const result = await this.generateSingleAudio(scene);
        this.results.push(result);
        console.log(`  ✓ 成功 - 时长: ${result.duration}s`);
      } catch (error) {
        const errorMsg = error instanceof Error ? error.message : String(error);
        console.log(`  ✗ 失败 - ${errorMsg}`);
        this.results.push({
          sceneId: scene.id,
          audioPath: "",
          duration: 0,
          success: false,
          error: errorMsg,
        });

        // auto 模式下尝试降级
        if (this.options.provider === "auto") {
          console.log(`  → 尝试降级到 MiniMax TTS...`);
          try {
            const fallbackResult = await this.generateSingleAudioWithMinimax(scene);
            this.results[this.results.length - 1] = fallbackResult;
            console.log(`  ✓ 降级成功 - 时长: ${fallbackResult.duration}s`);
          } catch (fallbackError) {
            const fallbackErrorMsg = fallbackError instanceof Error ? fallbackError.message : String(fallbackError);
            this.results[this.results.length - 1].error = `Edge failed, MiniMax also failed: ${fallbackErrorMsg}`;
            console.log(`  ✗ 降级也失败了 - ${fallbackErrorMsg}`);
          }
        }
      }
    }

    return this.results;
  }

  /**
   * 使用指定 provider 生成单个音频
   */
  private async generateSingleAudio(scene: Scene): Promise<SceneAudio> {
    const outputPath = join(this.options.outputDir, `${scene.id}.mp3`);

    if (this.options.provider === "minimax") {
      return this.generateSingleAudioWithMinimax(scene);
    }

    // 默认使用 Edge TTS
    const result = await generateEdgeTTS({
      text: scene.text,
      outputPath,
      voice: this.options.voice as "zh-CN-XiaoxiaoNeural" | "zh-CN-YunxiNeural" | "zh-CN-XiaoyiNeural",
      rate: this.options.rate,
    });

    return {
      sceneId: scene.id,
      audioPath: result.outputPath,
      duration: result.duration,
      success: true,
    };
  }

  /**
   * 使用 MiniMax TTS 生成单个音频
   */
  private async generateSingleAudioWithMinimax(scene: Scene): Promise<SceneAudio> {
    const outputPath = join(this.options.outputDir, `${scene.id}.mp3`);

    const result = await generateMiniMaxTTS({
      text: scene.text,
      outputPath,
      voiceId: "male-qn_qingse",
      speed: 1.0,
    });

    return {
      sceneId: scene.id,
      audioPath: result.outputPath,
      duration: result.duration,
      success: true,
    };
  }

  /**
   * 获取生成结果摘要
   */
  getSummary(): {
    total: number;
    success: number;
    failed: number;
    totalDuration: number;
    results: SceneAudio[];
  } {
    const success = this.results.filter(r => r.success).length;
    const failed = this.results.filter(r => !r.success).length;
    const totalDuration = this.results.reduce((sum, r) => sum + r.duration, 0);

    return {
      total: this.results.length,
      success,
      failed,
      totalDuration: Math.round(totalDuration * 100) / 100,
      results: this.results,
    };
  }

  /**
   * 导出结果为 JSON
   */
  exportResults(outputPath: string): void {
    const summary = this.getSummary();
    writeFileSync(outputPath, JSON.stringify(summary, null, 2));
    console.log(`\n结果已保存到: ${outputPath}`);
  }
}

/**
 * 主函数：批量生成场景音频
 */
export async function generateSceneAudio(
  scenes: Scene[],
  options: TTSManagerOptions
): Promise<SceneAudio[]> {
  const manager = new TTSManager(options);
  const results = await manager.generateSceneAudio(scenes);

  // 打印摘要
  const summary = manager.getSummary();
  console.log(`\n========== 生成摘要 ==========`);
  console.log(`总计: ${summary.total} 个场景`);
  console.log(`成功: ${summary.success} 个`);
  console.log(`失败: ${summary.failed} 个`);
  console.log(`总时长: ${summary.totalDuration} 秒`);

  if (summary.failed > 0) {
    console.log(`\n失败场景:`);
    for (const r of summary.results.filter(r => !r.success)) {
      console.log(`  ${r.sceneId}: ${r.error}`);
    }
  }

  return results;
}

// ============ CLI 入口 ============

interface CLIOptions {
  scenes?: string;
  outputDir?: string;
  provider?: "edge" | "minimax" | "auto";
  voice?: string;
  rate?: string;
  exportJson?: string;
}

function parseArgs(): CLIOptions {
  const args = process.argv.slice(2);
  const opts: CLIOptions = {};

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    switch (arg) {
      case "--scenes":
        opts.scenes = args[++i];
        break;
      case "--output-dir":
        opts.outputDir = args[++i];
        break;
      case "--provider":
        opts.provider = args[++i] as "edge" | "minimax" | "auto";
        break;
      case "--voice":
        opts.voice = args[++i];
        break;
      case "--rate":
        opts.rate = args[++i];
        break;
      case "--export-json":
        opts.exportJson = args[++i];
        break;
    }
  }

  return opts;
}

async function main() {
  const opts = parseArgs();

  if (!opts.scenes) {
    console.error("Error: --scenes is required (path to scenes JSON file or markdown script)");
    console.error("Usage: npx tsx scripts/tts-manager.ts --scenes scenes.json --output-dir ./audio [--provider edge|minimax|auto] [--update-scenes]");
    process.exit(1);
  }

  if (!opts.outputDir) {
    console.error("Error: --output-dir is required");
    process.exit(1);
  }

  let scenes: Scene[] = [];
  const scenesPath = opts.scenes;

  if (!existsSync(scenesPath)) {
    console.error(`Error: File not found: ${scenesPath}`);
    process.exit(1);
  }

  const content = readFileSync(scenesPath, "utf-8");

  if (scenesPath.endsWith(".json")) {
    const parsed = JSON.parse(content);
    scenes = parsed.scenes || parsed;
  } else {
    const parsed = parseScript(content);
    scenes = parsed.scenes;
  }

  console.log(`读取到 ${scenes.length} 个场景`);

  const manager = new TTSManager({
    outputDir: opts.outputDir,
    provider: opts.provider || "auto",
    voice: opts.voice,
    rate: opts.rate,
  });

  await manager.generateSceneAudio(scenes);

  const summary = manager.getSummary();

  if (opts.exportJson) {
    manager.exportResults(opts.exportJson);
  }

  writeAudioResultsToScenes(scenesPath, manager.getSummary().results, opts.outputDir);

  console.log(`\n========== 最终结果 ==========`);
  console.log(`成功: ${summary.success}/${summary.total} 个场景`);
  console.log(`总时长: ${summary.totalDuration} 秒`);

  if (summary.failed > 0) {
    console.log(`\n警告: ${summary.failed} 个场景生成失败`);
    process.exit(1);
  }
}

if (import.meta.url === `file://${process.argv[1]}`) {
  main();
}
