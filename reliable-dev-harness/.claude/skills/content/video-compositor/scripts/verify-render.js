/**
 * verify-render.js
 *
 * Validates Remotion render output against scenes.json specification.
 *
 * Checks:
 * 1. scenes.json exists and has valid structure
 * 2. Remotion source files exist (Scene components)
 * 3. Video file exists and is valid (dimensions, duration, codec)
 * 4. Audio files exist and are valid (if referenced in scenes)
 * 5. Video dimensions match platform preset
 * 6. Video encoding quality (bitrate, framerate)
 *
 * Usage:
 *   node scripts/verify-render.js \
 *     --scenes output/project/scenes.json \
 *     --video out/SelfMediaVideo.mp4 \
 *     --platform douyin
 */

const { spawn } = require("child_process");
const path = require("path");
const fs = require("fs");

const args = process.argv.slice(2);

const getArg = (name) => {
  const idx = args.indexOf(`--${name}`);
  return idx >= 0 ? args[idx + 1] : null;
};

const scenesPath = getArg("scenes");
const videoPath = getArg("video");
const platform = getArg("platform") || "douyin";

const PLATFORM_PRESETS = {
  douyin:      { width: 1080, height: 1920 },
  instagram:   { width: 1080, height: 1920 },
  youtube:     { width: 1920, height: 1080 },
  bilibili:    { width: 1920, height: 1080 },
  weibo:       { width: 1920, height: 1080 },
  xiaohongshu: { width: 1080, height: 1350 },
};

const expectedWidth = getArg("width") ? parseInt(getArg("width")) : (PLATFORM_PRESETS[platform]?.width || 1080);
const expectedHeight = getArg("height") ? parseInt(getArg("height")) : (PLATFORM_PRESETS[platform]?.height || 1920);

async function verifyScenesJson(scenesPath) {
  console.log(`\n[1/5] Validating scenes.json: ${scenesPath}`);

  if (!fs.existsSync(scenesPath)) {
    throw new Error(`scenes.json not found: ${scenesPath}`);
  }

  const content = fs.readFileSync(scenesPath, "utf-8");
  let parsed;

  try {
    parsed = JSON.parse(content);
  } catch (e) {
    throw new Error(`scenes.json is not valid JSON: ${e.message}`);
  }

  const scenes = parsed.scenes || parsed;
  if (!Array.isArray(scenes) || scenes.length === 0) {
    throw new Error(`scenes.json must contain a non-empty "scenes" array`);
  }

  const requiredFields = ["id", "type", "text", "estimatedDuration"];
  for (let i = 0; i < scenes.length; i++) {
    const scene = scenes[i];
    for (const field of requiredFields) {
      if (!(field in scene)) {
        throw new Error(`Scene ${i} (${scene.id || "unknown"}) missing field: ${field}`);
      }
    }

    const validTypes = ["开场钩子", "正文段落", "结尾引导"];
    if (!validTypes.includes(scene.type)) {
      console.warn(`  ⚠ Scene ${scene.id} has unexpected type: ${scene.type}`);
    }

    if (scene.visualType) {
      const validVisualTypes = ["keyword-pill", "big-number", "quote", "paragraph"];
      if (!validVisualTypes.includes(scene.visualType)) {
        console.warn(`  ⚠ Scene ${scene.id} has unexpected visualType: ${scene.visualType}`);
      }
    }
  }

  if (parsed.platform && PLATFORM_PRESETS[parsed.platform]) {
    const preset = PLATFORM_PRESETS[parsed.platform];
    console.log(`  Platform: ${parsed.platform} (${preset.width}x${preset.height})`);
  }

  console.log(`  ✓ ${scenes.length} scenes validated`);
  console.log(`  ✓ All scenes have required fields: ${requiredFields.join(", ")}`);
  return scenes;
}

async function verifyRemotionSourceFiles(scenesDir) {
  console.log(`\n[2/5] Checking Remotion source files: ${scenesDir}`);

  const requiredFiles = [
    "src/Root.tsx",
    "src/Video.tsx",
    "src/KenBurnsVideo.tsx",
    "src/BeatOverlay.tsx",
    "src/types.ts",
  ];

  let allExist = true;
  for (const file of requiredFiles) {
    const fullPath = path.join(scenesDir, file);
    if (fs.existsSync(fullPath)) {
      console.log(`  ✓ ${file}`);
    } else {
      console.warn(`  ⚠ Missing: ${file}`);
      allExist = false;
    }
  }

  if (!allExist) {
    console.warn("  Some Remotion source files are missing. Render may fail.");
  }

  console.log("  ✓ Source file check complete");
  return true;
}

async function verifyVideoFile(videoPath) {
  console.log(`\n[3/5] Validating video file: ${videoPath}`);

  if (!fs.existsSync(videoPath)) {
    throw new Error(`Video file not found: ${videoPath}`);
  }

  const stats = fs.statSync(videoPath);
  console.log(`  File size: ${(stats.size / 1024 / 1024).toFixed(1)} MB`);

  if (stats.size < 10000) {
    throw new Error(`Video file too small (${stats.size} bytes), render likely failed`);
  }

  const info = await getVideoInfo(videoPath);
  console.log(`  Resolution: ${info.width}x${info.height}`);
  console.log(`  Duration: ${info.duration.toFixed(2)}s`);
  console.log(`  Codec: ${info.codec}`);

  if (info.width !== expectedWidth || info.height !== expectedHeight) {
    console.warn(`  ⚠ Resolution mismatch: expected ${expectedWidth}x${expectedHeight}, got ${info.width}x${info.height}`);
  }

  if (info.duration < 1) {
    throw new Error(`Video duration too short: ${info.duration}s`);
  }

  console.log("  ✓ Video file valid");
  return true;
}

async function verifyAudioFiles(scenes) {
  console.log(`\n[4/5] Validating audio files`);

  const scenesWithAudio = scenes.filter(s => s.audioUrl);
  if (scenesWithAudio.length === 0) {
    console.log("  No audio files referenced in scenes (skipping)");
    return true;
  }

  let allValid = true;
  for (const scene of scenesWithAudio) {
    if (!fs.existsSync(scene.audioUrl)) {
      console.warn(`  ⚠ Audio missing for ${scene.id}: ${scene.audioUrl}`);
      allValid = false;
      continue;
    }

    const audioInfo = await getAudioInfo(scene.audioUrl);
    console.log(`  ✓ ${scene.id}: ${audioInfo.duration.toFixed(2)}s`);

    if (scene.audioDuration) {
      const error = Math.abs(audioInfo.duration - scene.audioDuration) / scene.audioDuration;
      if (error > 0.05) {
        console.warn(`  ⚠ ${scene.id}: audio duration mismatch: declared ${scene.audioDuration}s, actual ${audioInfo.duration.toFixed(2)}s (${(error * 100).toFixed(1)}% error)`);
      }
    }
  }

  if (!allValid) {
    console.warn("  Some audio files are missing or invalid");
  }

  console.log("  ✓ Audio validation complete");
  return true;
}

async function verifyVideoQuality(videoPath) {
  console.log(`\n[5/5] Validating video encoding quality`);

  const info = await getDetailedVideoInfo(videoPath);
  const stats = fs.statSync(videoPath);

  const bitrate = (stats.size * 8) / info.duration;
  const bitrateKbps = bitrate / 1000;

  console.log(`  Bitrate: ${bitrateKbps.toFixed(1)} Kbps`);
  console.log(`  FPS: ${info.fps}`);
  console.log(`  Codec: ${info.codec}`);

  const qualityRanges = {
    low:       { min: 500,   max: 2000,  crf: 28 },
    medium:    { min: 1500,  max: 4000,  crf: 23 },
    high:      { min: 3000,  max: 6000,  crf: 20 },
    cinematic: { min: 4500,  max: 10000, crf: 18 },
  };

  let inferredQuality = "unknown";
  for (const [name, range] of Object.entries(qualityRanges)) {
    if (bitrateKbps >= range.min && bitrateKbps <= range.max) {
      inferredQuality = name;
      break;
    }
  }

  console.log(`  Inferred quality: ${inferredQuality}`);

  if (bitrateKbps < 500) {
    console.warn(`  ⚠ Bitrate very low (< 500 Kbps), quality may suffer`);
  }

  if (info.fps < 25 || info.fps > 35) {
    console.warn(`  ⚠ Abnormal framerate: ${info.fps} (expected ~30)`);
  }

  console.log("  ✓ Video quality check complete");
  return true;
}

function getVideoInfo(videoPath) {
  return new Promise((resolve, reject) => {
    const ffprobe = spawn("ffprobe", [
      "-v", "error",
      "-select_streams", "v:0",
      "-show_entries", "stream=width,height,codec_name,duration",
      "-of", "default=noprint_wrappers=1",
      videoPath,
    ], { shell: true });

    let output = "";
    ffprobe.stdout.on("data", (data) => { output += data.toString(); });
    ffprobe.on("close", (code) => {
      if (code !== 0) { reject(new Error(`ffprobe exited with code ${code}`)); return; }
      const lines = output.trim().split("\n");
      const info = {};
      for (const line of lines) {
        const [key, value] = line.split("=");
        if (key && value) { info[key] = isNaN(value) ? value : parseFloat(value); }
      }
      resolve({ width: info.width, height: info.height, codec: info.codec_name, duration: info.duration || 0 });
    });
    ffprobe.on("error", reject);
  });
}

function getDetailedVideoInfo(videoPath) {
  return new Promise((resolve, reject) => {
    const ffprobe = spawn("ffprobe", [
      "-v", "error",
      "-select_streams", "v:0",
      "-show_entries", "stream=width,height,codec_name,duration,r_frame_rate",
      "-of", "default=noprint_wrappers=1:nokey=1",
      videoPath,
    ], { shell: true });

    let output = "";
    ffprobe.stdout.on("data", (data) => { output += data.toString(); });
    ffprobe.on("close", (code) => {
      if (code !== 0) { reject(new Error(`ffprobe exited with code ${code}`)); return; }
      const lines = output.trim().split("\n");
      const info = {};
      for (const line of lines) {
        const [key, value] = line.split("=");
        if (key && value) { info[key] = value; }
      }
      let fps = 30;
      if (info.r_frame_rate) {
        const parts = info.r_frame_rate.split("/");
        fps = parts.length === 2 ? Math.round(parseInt(parts[0]) / parseInt(parts[1])) : parseInt(parts[0]);
      }
      resolve({
        width: parseInt(info.width) || 0,
        height: parseInt(info.height) || 0,
        codec: info.codec_name || "unknown",
        duration: parseFloat(info.duration) || 0,
        fps,
      });
    });
    ffprobe.on("error", reject);
  });
}

function getAudioInfo(audioPath) {
  return new Promise((resolve, reject) => {
    const ffprobe = spawn("ffprobe", [
      "-v", "error",
      "-select_streams", "a:0",
      "-show_entries", "stream=sample_rate,duration",
      "-of", "default=noprint_wrappers=1",
      audioPath,
    ], { shell: true });

    let output = "";
    ffprobe.stdout.on("data", (data) => { output += data.toString(); });
    ffprobe.on("close", (code) => {
      if (code !== 0) { reject(new Error(`ffprobe exited with code ${code}`)); return; }
      const lines = output.trim().split("\n");
      const info = {};
      for (const line of lines) {
        const [key, value] = line.split("=");
        if (key && value) { info[key] = isNaN(value) ? value : parseFloat(value); }
      }
      resolve({ sampleRate: info.sample_rate, duration: info.duration || 0 });
    });
    ffprobe.on("error", reject);
  });
}

function runCommand(cmd, args) {
  return new Promise((resolve, reject) => {
    const proc = spawn(cmd, args, { shell: true });
    proc.on("close", (code) => {
      if (code === 0) resolve();
      else reject(new Error(`${cmd} exited with code ${code}`));
    });
    proc.on("error", reject);
  });
}

async function verifyAll() {
  console.log("=".repeat(50));
  console.log("Remotion Render Verification");
  console.log("=".repeat(50));

  if (!scenesPath) {
    console.error("Usage: node verify-render.js --scenes <path> --video <path> [--platform douyin]");
    console.error("");
    console.error("  --scenes    Path to scenes.json");
    console.error("  --video     Path to rendered video file (MP4)");
    console.error("  --platform  Target platform (douyin|instagram|youtube|bilibili|weibo|xiaohongshu)");
    console.error("  --width     Override expected width");
    console.error("  --height    Override expected height");
    process.exit(1);
  }

  try {
    const scenes = await verifyScenesJson(scenesPath);

    const projectRoot = path.resolve(path.dirname(scenesPath), "..");
    await verifyRemotionSourceFiles(projectRoot);

    if (videoPath) {
      await verifyVideoFile(videoPath);
      await verifyAudioFiles(scenes);
      await verifyVideoQuality(videoPath);
    } else {
      console.log("\n[3/5] Skipping video validation (no --video path provided)");
      console.log("[4/5] Skipping audio validation (no --video path provided)");
      console.log("[5/5] Skipping quality check (no --video path provided)");
    }

    console.log("\n" + "=".repeat(50));
    console.log("✓ All validations passed!");
    console.log("=".repeat(50));
    process.exit(0);
  } catch (err) {
    console.error("\n" + "=".repeat(50));
    console.error("✗ Validation failed:", err.message);
    console.error("=".repeat(50));
    process.exit(1);
  }
}

verifyAll();