/**
 * render-slides-to-video.js
 *
 * Renders HTML slides to video using Puppeteer + ffmpeg
 *
 * Usage:
 * node scripts/render-slides-to-video.js --html scenes/scene-01.html --audio audio/scene-01.mp3 --output out/scene-01.mp4
 *
 * Platform presets (sets width/height automatically):
 *   --platform douyin      (9:16, 1080x1920)
 *   --platform youtube     (16:9, 1920x1080)
 *   --platform xiaohongshu (4:5, 1080x1350)
 *
 * Or specify dimensions manually:
 *   --width 1920 --height 1080
 *
 * Quality presets (default: high):
 *   --quality low      (crf=28, fast, 128k AAC, JPEG 85%)
 *   --quality medium   (crf=23, medium, 160k AAC, JPEG 92%)
 *   --quality high     (crf=20, slow, 192k AAC, JPEG 95%)
 *   --quality cinematic (crf=18, slow, 256k AAC, PNG lossless)
 */

const puppeteer = require("/Users/wuzhijing/.nvm/versions/node/v22.22.0/lib/node_modules/puppeteer");
const chromium = puppeteer;
const { spawn } = require("child_process");
const path = require("path");
const fs = require("fs");

const args = process.argv.slice(2);

const getArg = (name) => {
  const idx = args.indexOf(`--${name}`);
  return idx >= 0 ? args[idx + 1] : null;
};

const htmlPath = getArg("html");
const audioPath = getArg("audio");
const outputPath = getArg("output");

if (!htmlPath || !audioPath || !outputPath) {
  console.error("Usage: node scripts/render-slides-to-video.js --html <path> --audio <path> --output <path>");
  console.error("Platform presets: --platform douyin|youtube|xiaohongshu");
  console.error("Or manual: --width <px> --height <px>");
  console.error("Quality presets: --quality low|medium|high|cinematic (default: high)");
  process.exit(1);
}

const fps = parseInt(getArg("fps") || "30");

// Video quality presets (higher = better quality, larger file)
const qualityPresets = {
  low:      { crf: 28, preset: "fast", aacBitrate: "128k", jpegQuality: 85 },
  medium:   { crf: 23, preset: "medium", aacBitrate: "160k", jpegQuality: 92 },
  high:     { crf: 20, preset: "slow", aacBitrate: "192k", jpegQuality: 95 },
  cinematic: { crf: 18, preset: "slow", aacBitrate: "256k", jpegQuality: 98 },
};

// Default to high quality
const quality = getArg("quality") || "high";
const qualityConfig = qualityPresets[quality] || qualityPresets.high;

// Platform presets
const platformPresets = {
  douyin:      { width: 1080, height: 1920 },  // 9:16 竖版
  instagram:   { width: 1080, height: 1920 },  // 9:16 竖版
  youtube:     { width: 1920, height: 1080 },  // 16:9 横版
  bilibili:    { width: 1920, height: 1080 },  // 16:9 横版
  weibo:       { width: 1920, height: 1080 },  // 16:9 横版
  xiaohongshu: { width: 1080, height: 1350 },  // 4:5 种草版
};

const platform = getArg("platform");
let width, height;

if (platform && platformPresets[platform]) {
  width = platformPresets[platform].width;
  height = platformPresets[platform].height;
  console.log(`Platform preset: ${platform} (${width}x${height})`);
} else {
  width = parseInt(getArg("width") || "1080");
  height = parseInt(getArg("height") || "1920");
}

/**
 * Get audio duration using ffprobe
 */
function getAudioDuration(audioPath) {
  return new Promise((resolve, reject) => {
    const ffprobe = spawn("ffprobe", [
      "-v", "error",
      "-show_entries", "format=duration",
      "-of", "default=noprint_wrappers=1:nokey=1",
      audioPath
    ], { shell: true });

    let output = "";
    ffprobe.stdout.on("data", (data) => { output += data.toString(); });
    ffprobe.on("close", (code) => {
      if (code === 0) resolve(parseFloat(output.trim()));
      else reject(new Error(`ffprobe exited with code ${code}`));
    });
    ffprobe.on("error", reject);
  });
}

/**
 * Render HTML slide to frames using Puppeteer
 */
async function renderHtmlToFrames(htmlPath, outputDir, duration, fps, usePng = false) {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();

  await page.setViewport({ width, height, deviceScaleFactor: 1 });

  const htmlUrl = `file://${path.resolve(htmlPath)}`;
  console.log(`Loading: ${htmlUrl}`);
  await page.goto(htmlUrl, { waitUntil: "networkidle0" });
  await page.evaluate(() => document.fonts.ready);

  const totalFrames = Math.ceil(duration * fps);
  const jpegQuality = qualityConfig.jpegQuality;

  console.log(`Rendering ${totalFrames} frames at ${fps}fps (quality: ${jpegQuality})...`);

  for (let frame = 0; frame < totalFrames; frame++) {
    const time = frame / fps;
    const progress = frame / totalFrames;

    await page.evaluate(
      (t, p) => {
        document.documentElement.style.setProperty("--current-time", `${t}s`);
        document.documentElement.style.setProperty("--progress", String(p));
      },
      time, progress
    );

    const framePath = path.join(outputDir, `frame-${String(frame).padStart(6, "0")}.${usePng ? 'png' : 'jpg'}`);
    if (usePng) {
      await page.screenshot({
        path: framePath,
        type: "png",
        omitBackground: false,
      });
    } else {
      await page.screenshot({
        path: framePath,
        type: "jpeg",
        quality: jpegQuality,
        omitBackground: false,
      });
    }

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
function combineFramesWithAudio(framesDir, audioPath, outputPath, fps) {
  const { crf, preset, aacBitrate } = qualityConfig;
  // Use PNG for cinematic quality (lossless), JPEG for others
  const usePng = quality === "cinematic";
  const inputExt = usePng ? "png" : "jpg";

  return new Promise((resolve, reject) => {
    const ffmpeg = spawn("ffmpeg", [
      "-y",
      "-framerate", String(fps),
      "-i", `${framesDir}/frame-%06d.${inputExt}`,
      "-i", audioPath,
      "-c:v", "libx264",
      "-preset", preset,
      "-crf", String(crf),
      "-pix_fmt", "yuv420p",
      "-c:a", "aac",
      "-b:a", aacBitrate,
      "-shortest",
      "-strict", "experimental",
      outputPath
    ], { shell: true });

    let stderr = "";
    ffmpeg.stderr.on("data", (data) => { stderr += data.toString(); });
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
 * Main render function
 */
async function renderScene() {
  const usePng = quality === "cinematic";
  console.log(`\n=== Rendering Scene ===`);
  console.log(`HTML: ${htmlPath}`);
  console.log(`Audio: ${audioPath}`);
  console.log(`Output: ${outputPath}`);
  console.log(`Quality: ${quality} (${usePng ? "PNG lossless" : "JPEG lossy"})`);

  // Create temp directory for frames
  const framesDir = path.join(path.dirname(outputPath), `.frames-${Date.now()}`);
  fs.mkdirSync(framesDir, { recursive: true });

  try {
    // Get audio duration
    console.log("Getting audio duration...");
    const duration = await getAudioDuration(audioPath);
    console.log(`Audio duration: ${duration.toFixed(2)}s`);

    // Render HTML to frames
    await renderHtmlToFrames(htmlPath, framesDir, duration, fps, usePng);

    // Combine with audio
    await combineFramesWithAudio(framesDir, audioPath, outputPath, fps);
  } finally {
    // Cleanup frames
    console.log("Cleaning up temporary frames...");
    try {
      const files = fs.readdirSync(framesDir);
      for (const file of files) {
        fs.unlinkSync(path.join(framesDir, file));
      }
      fs.rmdirSync(framesDir);
    } catch (e) {
      console.log("Cleanup skipped:", e.message);
    }
  }
}

renderScene()
  .then(() => {
    console.log("\n=== Render Complete ===");
    process.exit(0);
  })
  .catch((err) => {
    console.error("Render failed:", err);
    process.exit(1);
  });
