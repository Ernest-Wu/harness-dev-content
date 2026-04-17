/**
 * render-base-video.ts
 *
 * Uses Playwright to screen-record slides-preview.html frame-by-frame,
 * then concatenates all frames into base-video.mp4 using ffmpeg.
 *
 * CLI:
 *   npx tsx scripts/render-base-video.ts [--scenes ../../scenes.json] [--html ./slides-preview.html] [--output ../../base-video.mp4]
 */

import * as fs from "fs";
import * as path from "path";
import { chromium } from "playwright";
import { spawn } from "child_process";
import * as http from "http";

interface Scene {
  id: string;
  audioDuration?: number;
}

interface ProjectData {
  scenes: Scene[];
  platform?: string;
}

const FPS = 30;

const PLATFORM_DIMENSIONS: Record<string, { width: number; height: number }> = {
  douyin: { width: 1080, height: 1920 },
  instagram: { width: 1080, height: 1920 },
  youtube: { width: 1920, height: 1080 },
  bilibili: { width: 1920, height: 1080 },
  weibo: { width: 1920, height: 1080 },
  xiaohongshu: { width: 1080, height: 1350 },
};

function startStaticServer(rootDir: string, port: number): http.Server {
  const server = http.createServer((req, res) => {
    const reqPath = req.url ? decodeURIComponent(req.url.split("?")[0]) : "/";
    const filePath = path.join(rootDir, reqPath === "/" ? "/index.html" : reqPath);

    fs.readFile(filePath, (err, data) => {
      if (err) {
        res.writeHead(404);
        res.end("Not found");
        return;
      }
      const ext = path.extname(filePath).toLowerCase();
      const mime: Record<string, string> = {
        ".html": "text/html",
        ".js": "application/javascript",
        ".css": "text/css",
        ".json": "application/json",
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".gif": "image/gif",
        ".svg": "image/svg+xml",
        ".mp3": "audio/mpeg",
        ".mp4": "video/mp4",
      };
      res.writeHead(200, { "Content-Type": mime[ext] || "application/octet-stream" });
      res.end(data);
    });
  });
  server.listen(port);
  return server;
}

function runFfmpeg(frameDir: string, outputPath: string, fps: number): Promise<void> {
  return new Promise((resolve, reject) => {
    const args = [
      "-y",
      "-framerate", String(fps),
      "-i", path.join(frameDir, "frame_%06d.png"),
      "-c:v", "libx264",
      "-pix_fmt", "yuv420p",
      "-crf", "18",
      "-movflags", "+faststart",
      outputPath,
    ];
    const proc = spawn("ffmpeg", args, { stdio: "inherit" });
    proc.on("close", (code) => {
      if (code === 0) resolve();
      else reject(new Error(`ffmpeg exited with code ${code}`));
    });
    proc.on("error", reject);
  });
}

async function main() {
  const args = process.argv.slice(2);
  const getArg = (name: string): string | undefined => {
    const idx = args.indexOf(`--${name}`);
    return idx >= 0 ? args[idx + 1] : undefined;
  };

  const scenesPath = getArg("scenes") || "../../scenes.json";
  const htmlPath = getArg("html") || "./slides-preview.html";
  const outputPath = getArg("output") || "../../base-video.mp4";

  const resolvedScenesPath = path.resolve(scenesPath);
  const resolvedHtmlPath = path.resolve(htmlPath);
  const resolvedOutputPath = path.resolve(outputPath);

  if (!fs.existsSync(resolvedScenesPath)) {
    console.error(`scenes.json not found: ${resolvedScenesPath}`);
    process.exit(1);
  }
  if (!fs.existsSync(resolvedHtmlPath)) {
    console.error(`HTML file not found: ${resolvedHtmlPath}`);
    process.exit(1);
  }

  const projectData: ProjectData = JSON.parse(fs.readFileSync(resolvedScenesPath, "utf-8"));
  const scenes = projectData.scenes || [];
  const platform = projectData.platform || "bilibili";
  const dims = PLATFORM_DIMENSIONS[platform] || PLATFORM_DIMENSIONS.bilibili;

  const htmlDir = path.dirname(resolvedHtmlPath);
  const port = 9876;
  const server = startStaticServer(htmlDir, port);
  const tempDir = fs.mkdtempSync(path.join(require("os").tmpdir(), "base-video-frames-"));

  console.log(`Serving ${htmlDir} on http://localhost:${port}`);
  console.log(`Viewport: ${dims.width}x${dims.height} @ ${FPS}fps`);
  console.log(`Scenes to record: ${scenes.length}`);

  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    viewport: { width: dims.width, height: dims.height },
    deviceScaleFactor: 1,
  });
  const page = await context.newPage();

  const url = `http://localhost:${port}/${path.basename(resolvedHtmlPath)}`;
  await page.goto(url, { waitUntil: "networkidle" });

  let globalFrameIndex = 0;

  for (let i = 0; i < scenes.length; i++) {
    const scene = scenes[i];
    const durationSec = scene.audioDuration || 5;
    const frameCount = Math.ceil(durationSec * FPS);

    // Scroll to slide i
    await page.evaluate((slideIndex) => {
      const slides = document.querySelectorAll(".slide");
      if (slides[slideIndex]) {
        slides[slideIndex].scrollIntoView({ behavior: "instant", block: "start" });
      }
    }, i);

    // Wait for IntersectionObserver to trigger .visible and CSS animations to start
    await page.waitForTimeout(400);

    console.log(`Recording scene ${i + 1}/${scenes.length} (${frameCount} frames, ${durationSec.toFixed(2)}s)`);

    for (let f = 0; f < frameCount; f++) {
      const sceneTime = f / FPS;
      await page.evaluate((t) => {
        document.documentElement.style.setProperty("--scene-time", String(t));
        document.querySelectorAll("[data-beat-at]").forEach((el) => {
          const beatAt = parseFloat((el as HTMLElement).dataset.beatAt || "0");
          el.classList.toggle("beat-active", t >= beatAt);
        });
      }, sceneTime);

      const framePath = path.join(tempDir, `frame_${String(globalFrameIndex).padStart(6, "0")}.png`);
      await page.screenshot({ path: framePath, type: "png" });
      globalFrameIndex++;
    }
  }

  await browser.close();
  server.close();

  console.log(`Encoding ${globalFrameIndex} frames into ${resolvedOutputPath}...`);
  await runFfmpeg(tempDir, resolvedOutputPath, FPS);

  // Cleanup temp frames
  fs.rmSync(tempDir, { recursive: true, force: true });
  console.log(`base-video.mp4 created successfully: ${resolvedOutputPath}`);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
