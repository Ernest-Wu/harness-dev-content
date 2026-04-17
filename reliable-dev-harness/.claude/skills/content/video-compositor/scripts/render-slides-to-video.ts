/**
 * render-slides-to-video.ts
 *
 * Renders HTML slides to video using Puppeteer + ffmpeg
 *
 * Workflow:
 * 1. For each scene, use Puppeteer to capture frames from the HTML slide
 * 2. Use ffmpeg to combine frames with audio into final video
 *
 * Usage:
 * npx ts-node scripts/render-slides-to-video.ts --scene scene-01 --html scenes/scene-01.html --audio audio/scene-01.mp3 --output out/scene-01.mp4
 */

import { chromium, Browser, Page } from "puppeteer";
import { spawn, SpawnOptions } from "child_process";
import * as path from "path";
import * as fs from "fs";

interface RenderOptions {
  htmlPath: string;
  audioPath: string;
  outputPath: string;
  fps?: number;
  width?: number;
  height?: number;
}

/**
 * Get audio duration using ffprobe
 */
async function getAudioDuration(audioPath: string): Promise<number> {
  return new Promise((resolve, reject) => {
    const ffprobe = spawn(
      "ffprobe",
      [
        "-v",
        "error",
        "-show_entries",
        "format=duration",
        "-of",
        "default=noprint_wrappers=1:nokey=1",
        audioPath,
      ],
      { shell: true }
    );

    let output = "";
    ffprobe.stdout.on("data", (data) => {
      output += data.toString();
    });
    ffprobe.on("close", (code) => {
      if (code === 0) {
        resolve(parseFloat(output.trim()));
      } else {
        reject(new Error(`ffprobe exited with code ${code}`));
      }
    });
    ffprobe.on("error", reject);
  });
}

/**
 * Render HTML slide to frames using Puppeteer
 */
async function renderHtmlToFrames(
  htmlPath: string,
  outputDir: string,
  duration: number,
  fps: number = 30
): Promise<void> {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();

  const width = 1080;
  const height = 1920;

  await page.setViewport({ width, height, deviceScaleFactor: 1 });

  const htmlUrl = `file://${path.resolve(htmlPath)}`;
  await page.goto(htmlUrl, { waitUntil: "networkidle0" });

  // Wait for fonts to load
  await page.evaluate(() => document.fonts.ready);

  const totalFrames = Math.ceil(duration * fps);
  const frameDelay = 1000 / fps; // ms between frames

  console.log(`Rendering ${totalFrames} frames at ${fps}fps...`);

  for (let frame = 0; frame < totalFrames; frame++) {
    const time = frame / fps;
    const progress = frame / totalFrames;

    // Set current time as CSS variable for animations
    await page.evaluate(
      (t) => {
        document.documentElement.style.setProperty("--current-time", `${t}s`);
        document.documentElement.style.setProperty("--progress", String(progress));
      },
      time
    );

    // Capture screenshot
    const outputPath = path.join(outputDir, `frame-${String(frame).padStart(6, "0")}.jpg`);
    await page.screenshot({
      path: outputPath,
      type: "jpeg",
      quality: 90,
      omitBackground: false,
    });

    if (frame % 30 === 0) {
      console.log(`  Frame ${frame}/${totalFrames} (${(progress * 100).toFixed(1)}%)`);
    }
  }

  await browser.close();
  console.log(`Frames saved to ${outputDir}`);
}

/**
 * Combine frames with audio using ffmpeg
 */
async function combineFramesWithAudio(
  framesDir: string,
  audioPath: string,
  outputPath: string,
  fps: number = 30
): Promise<void> {
  return new Promise((resolve, reject) => {
    const ffmpeg = spawn(
      "ffmpeg",
      [
        "-y",
        "-framerate",
        String(fps),
        "-i",
        `${framesDir}/frame-%06d.jpg`,
        "-i",
        audioPath,
        "-c:v",
        "libx264",
        "-pix_fmt",
        "yuv420p",
        "-c:a",
        "aac",
        "-shortest",
        "-strict",
        "experimental",
        outputPath,
      ],
      { shell: true }
    );

    let stderr = "";
    ffmpeg.stderr.on("data", (data) => {
      stderr += data.toString();
    });
    ffmpeg.on("close", (code) => {
      if (code === 0) {
        console.log(`Video saved to ${outputPath}`);
        resolve();
      } else {
        console.error("ffmpeg error:", stderr);
        reject(new Error(`ffmpeg exited with code ${code}`));
      }
    });
    ffmpeg.on("error", reject);
  });
}

/**
 * Main render function for a single scene
 */
export async function renderScene(options: RenderOptions): Promise<void> {
  const {
    htmlPath,
    audioPath,
    outputPath,
    fps = 30,
    width = 1080,
    height = 1920,
  } = options;

  console.log(`\n=== Rendering Scene ===`);
  console.log(`HTML: ${htmlPath}`);
  console.log(`Audio: ${audioPath}`);
  console.log(`Output: ${outputPath}`);

  // Create temp directory for frames
  const framesDir = path.join(path.dirname(outputPath), `.frames-${Date.now()}`);
  fs.mkdirSync(framesDir, { recursive: true });

  try {
    // Get audio duration
    console.log("Getting audio duration...");
    const duration = await getAudioDuration(audioPath);
    console.log(`Audio duration: ${duration.toFixed(2)}s`);

    // Render HTML to frames
    await renderHtmlToFrames(htmlPath, framesDir, duration, fps);

    // Combine with audio
    await combineFramesWithAudio(framesDir, audioPath, outputPath, fps);
  } finally {
    // Cleanup frames
    console.log("Cleaning up temporary frames...");
    const files = fs.readdirSync(framesDir);
    for (const file of files) {
      fs.unlinkSync(path.join(framesDir, file));
    }
    fs.rmdirSync(framesDir);
  }
}

// CLI entry point
if (require.main === module) {
  const args = process.argv.slice(2);

  const getArg = (name: string): string | undefined => {
    const idx = args.indexOf(`--${name}`);
    return idx >= 0 ? args[idx + 1] : undefined;
  };

  const htmlPath = getArg("html");
  const audioPath = getArg("audio");
  const outputPath = getArg("output");

  if (!htmlPath || !audioPath || !outputPath) {
    console.error("Usage: npx ts-node render-slides-to-video.ts --html <path> --audio <path> --output <path>");
    process.exit(1);
  }

  renderScene({
    htmlPath,
    audioPath,
    outputPath,
    fps: parseInt(getArg("fps") || "30"),
  })
    .then(() => {
      console.log("\n=== Render Complete ===");
      process.exit(0);
    })
    .catch((err) => {
      console.error("Render failed:", err);
      process.exit(1);
    });
}
