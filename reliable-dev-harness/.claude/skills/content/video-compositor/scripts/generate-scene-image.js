/**
 * generate-scene-image.js
 *
 * AI image generation script for scene backgrounds and illustrations.
 * Uses DALL-E API to generate style-consistent images.
 *
 * Usage:
 *   node scripts/generate-scene-image.js \
 *     --scene-text "AI模型的发展..." \
 *     --scene-type "开场钩子" \
 *     --style "tech" \
 *     --aspect-ratio "16:9" \
 *     --output "./output/scenes/scene-01-bg.png"
 *
 * Environment:
 *   OPENAI_API_KEY - DALL-E API key
 */

const { spawn } = require("child_process");
const fs = require("fs");
const path = require("path");
const crypto = require("crypto");

// ============ Configuration ============

const SCENE_TYPE_KEYWORDS = {
  "开场钩子": "attention-grabbing, dramatic lighting, bold, surprising, curiosity",
  "正文段落": "analytical, data visualization style, clean, informative, credible",
  "结尾引导": "inspiring, forward-looking, positive energy, motivational, actionable",
  "案例解析": "professional, detailed, charts or diagrams, clean layout",
  "实战建议": "professional, actionable, checklist style, clean",
};

// 场景插图类型映射
const SCENE_ILLUSTRATION_TYPES = {
  "数据类": {
    keywords: "data visualization, growth chart, clean graph, analytics dashboard, statistical",
    promptTemplate: "Professional data visualization illustration showing {subject}. Clean modern style, dark background with purple/blue accents (#6366F1, #a855f7), subtle grid lines, trend indicators. No text, no watermark."
  },
  "案例类": {
    keywords: "professional photo, product shot, realistic, case study, detailed",
    promptTemplate: "Professional case study illustration showing {subject}. Realistic photography style, dramatic lighting, dark background with purple/blue accent lighting. Clean composition, no text, no watermark."
  },
  "概念类": {
    keywords: "abstract visualization, network nodes, connection, futuristic, tech",
    promptTemplate: "Abstract conceptual illustration of {subject}. Futuristic tech style, neural network or connection diagram aesthetic, glowing nodes on dark background, purple/blue color scheme (#6366F1, #a855f7). No text, no watermark."
  },
  "对比类": {
    keywords: "side-by-side comparison, split view, before after, contrasting",
    promptTemplate: "Professional comparison illustration showing {subject}. Split view or side-by-side composition, dark background with purple/blue accents, clean modern style. No text, no watermark."
  },
  "实战类": {
    keywords: "step-by-step, interface mockup, tutorial style, practical, actionable",
    promptTemplate: "Practical tutorial illustration showing {subject}. Interface mockup or step-by-step visual style, clean modern design, dark background with purple/blue accent colors. No text, no watermark."
  }
};

const STYLE_KEYWORDS = {
  tech: "cyberpunk elements, neon glow, geometric patterns, digital matrix",
  minimal: "clean lines, ample whitespace, subtle gradients, minimalist",
  vibrant: "colorful, energetic, saturated tones, dynamic composition",
  cinematic: "film grain, anamorphic, cinematic lighting, dramatic shadows",
};

const MOOD_KEYWORDS = {
  "开场钩子": "surprising, dramatic, mysterious",
  "正文段落": "informative, analytical, credible",
  "结尾引导": "motivational, inspiring, positive",
  "案例解析": "professional, data-driven, authoritative",
  "实战建议": "practical, actionable, clear",
};

// ============ Prompt Building ============

/**
 * 判断场景内容类型
 */
function detectSceneContentType(sceneText, sceneType) {
  const text = sceneText.toLowerCase();

  // 数据类关键词
  if (/增长|数据|统计|图表|曲线|比例|百分比|排名|分数|指标/.test(text)) {
    return "数据类";
  }
  // 对比类关键词
  if (/对比|比较|差异|优劣|不同|区别| vs |versus/.test(text)) {
    return "对比类";
  }
  // 实战类关键词
  if (/步骤|教程|方法|技巧|实战|操作|如何|实现|搭建|创建/.test(text)) {
    return "实战类";
  }
  // 案例类关键词
  if (/案例|实例|例子|故事|人物|产品|公司|企业/.test(text)) {
    return "案例类";
  }
  // 默认概念类
  return "概念类";
}

/**
 * Build the image generation prompt for a scene illustration (scene-image type)
 */
function buildIllustrationPrompt(sceneText, sceneType, style, aspectRatio) {
  const contentType = detectSceneContentType(sceneText, sceneType);
  const illustrationConfig = SCENE_ILLUSTRATION_TYPES[contentType] || SCENE_ILLUSTRATION_TYPES["概念类"];

  const aspectRatioMap = {
    "16:9": "16:9 horizontal",
    "9:16": "9:16 vertical",
    "4:5": "4:5 portrait",
  };

  // 提取场景核心内容作为 subject
  const subject = sceneText.substring(0, 100).replace(/[^\w\u4e00-\u9fa5]/g, ' ').trim();

  // 填充 prompt 模板
  let prompt = illustrationConfig.promptTemplate.replace("{subject}", subject || "AI technology concept");

  prompt += `\n\nAspect ratio: ${aspectRatioMap[aspectRatio] || aspectRatioMap["16:9"]}`;

  return prompt;
}

/**
 * Build the image generation prompt for a scene
 */
function buildPrompt(sceneText, sceneType, style, aspectRatio, imageType = "background") {
  const typeKeywords = SCENE_TYPE_KEYWORDS[sceneType] || SCENE_TYPE_KEYWORDS["正文段落"];
  const styleKeywords = STYLE_KEYWORDS[style] || STYLE_KEYWORDS.tech;
  const moodKeywords = MOOD_KEYWORDS[sceneType] || MOOD_KEYWORDS["正文段落"];

  const aspectRatioMap = {
    "16:9": "16:9 horizontal",
    "9:16": "9:16 vertical",
    "4:5": "4:5 portrait",
  };

  const prompt = `
High-contrast abstract visual for ${sceneType}.

Style: ${styleKeywords}
Mood: ${moodKeywords}
Aspect ratio: ${aspectRatioMap[aspectRatio] || aspectRatioMap["16:9"]}

Requirements:
- Professional video thumbnail style
- Dark background with purple/blue accents (#6366F1, #a855f7)
- Minimal or no text space
- No watermark, signature, or low quality elements
- Dramatic lighting, cinematic feel
- Suitable for ${sceneType} content

Scene context: ${sceneText.substring(0, 200)}
`.trim();

  return prompt;
}

/**
 * Build negative prompt to ensure style consistency
 */
function buildNegativePrompt() {
  return "text, watermark, signature, low quality, blurry, deformed, ugly, bad anatomy";
}

// ============ Image Generation ============

/**
 * Generate image using DALL-E 3 via OpenAI API
 */
async function generateWithDalle(prompt, negativePrompt, outputPath, apiKey) {
  const { OpenAI } = require("/Users/wuzhijing/.nvm/versions/node/v22.22.0/lib/node_modules/openai");

  const client = new OpenAI({ apiKey });

  console.log("Generating image with DALL-E 3...");
  console.log("Prompt:", prompt.substring(0, 100), "...");

  const response = await client.images.generate({
    model: "dall-e-3",
    prompt,
    negative_prompt: negativePrompt,
    size: "1024x1024",
    quality: "standard",
    n: 1,
  });

  const imageUrl = response.data[0].url;
  console.log("Generated image URL:", imageUrl);

  // Download the image
  await downloadImage(imageUrl, outputPath);

  return { imagePath: outputPath, prompt };
}

/**
 * Download image from URL to local path
 */
async function downloadImage(url, outputPath) {
  return new Promise((resolve, reject) => {
    const wget = spawn("curl", ["-L", "-o", outputPath, url], { shell: true });

    wget.on("close", (code) => {
      if (code === 0) {
        console.log("Image saved to:", outputPath);
        resolve();
      } else {
        reject(new Error(`curl exited with code ${code}`));
      }
    });

    wget.on("error", reject);
  });
}

/**
 * Generate a unique hash for caching
 */
function generateCacheKey(sceneText, sceneType, style, aspectRatio, imageType = "background") {
  const data = `${sceneText}:${sceneType}:${style}:${aspectRatio}:${imageType}`;
  return crypto.createHash("md5").update(data).digest("hex");
}

// ============ Main ============

/**
 * Main function to generate scene image
 * @param {Object} options - Generation options
 * @param {string} options.sceneText - Scene text content
 * @param {string} options.sceneType - Scene type (开场钩子/正文段落/结尾引导/案例解析/实战建议)
 * @param {string} options.style - Visual style (tech/minimal/vibrant/cinematic)
 * @param {string} options.aspectRatio - Aspect ratio (16:9/9:16/4:5)
 * @param {string} options.outputPath - Output file path
 * @param {string} options.apiKey - OpenAI API key
 * @param {boolean} options.useCache - Whether to use cached images
 * @param {string} options.imageType - Image type: "background" or "scene-image"
 */
async function generateSceneImage(options) {
  const {
    sceneText,
    sceneType = "正文段落",
    style = "tech",
    aspectRatio = "16:9",
    outputPath,
    apiKey,
    useCache = true,
    imageType = "background",
  } = options;

  // Check for cached image (cache key includes imageType)
  const cacheDir = path.join(path.dirname(outputPath), ".image-cache");
  const cacheKey = generateCacheKey(sceneText, sceneType, style, aspectRatio, imageType);
  const cachedPath = path.join(cacheDir, `${cacheKey}.png`);

  if (useCache && fs.existsSync(cachedPath)) {
    console.log("Using cached image:", cachedPath);
    // Copy cached image to output path
    fs.copyFileSync(cachedPath, outputPath);
    return { imagePath: outputPath, prompt: "(cached)", cached: true, imageType };
  }

  // Ensure output directory exists
  const outputDir = path.dirname(outputPath);
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }

  // Build prompts based on image type
  let prompt;
  if (imageType === "scene-image") {
    prompt = buildIllustrationPrompt(sceneText, sceneType, style, aspectRatio);
    console.log("Generating scene illustration...");
  } else {
    prompt = buildPrompt(sceneText, sceneType, style, aspectRatio, imageType);
    console.log("Generating background image...");
  }
  const negativePrompt = buildNegativePrompt();

  // Generate image
  const result = await generateWithDalle(prompt, negativePrompt, outputPath, apiKey);
  result.imageType = imageType;

  // Save to cache
  if (useCache) {
    if (!fs.existsSync(cacheDir)) {
      fs.mkdirSync(cacheDir, { recursive: true });
    }
    fs.copyFileSync(outputPath, cachedPath);
    console.log("Cached at:", cachedPath);
  }

  return result;
}

/**
 * Write generated image URL back into scenes.json
 * Finds the scene by id and sets its imageUrl field
 */
function writeImageUrlToScenes(scenesPath, sceneId, imageUrl) {
  if (!fs.existsSync(scenesPath)) return;

  const raw = fs.readFileSync(scenesPath, "utf-8");
  const data = JSON.parse(raw);
  const scenes = data.scenes || data;

  const scene = scenes.find(s => s.id === sceneId);
  if (scene) {
    scene.imageUrl = imageUrl;
    fs.writeFileSync(scenesPath, JSON.stringify(data, null, 2), "utf-8");
    console.log(`Updated scenes.json: scene "${sceneId}" imageUrl = ${imageUrl}`);
  }
}

// CLI interface
if (require.main === module) {
  const args = process.argv.slice(2);

  const getArg = (name) => {
    const idx = args.indexOf(`--${name}`);
    return idx >= 0 ? args[idx + 1] : null;
  };

  const sceneText = getArg("scene-text") || "AI technology abstract visualization";
  const sceneType = getArg("scene-type") || "正文段落";
  const style = getArg("style") || "tech";
  const aspectRatio = getArg("aspect-ratio") || "16:9";
  const outputPath = getArg("output") || "./output/scene-image.png";
  const apiKey = process.env.OPENAI_API_KEY || getArg("api-key");
  const scenesPath = getArg("scenes");
  const sceneId = getArg("scene-id");

  if (!apiKey) {
    console.error("Error: OPENAI_API_KEY environment variable or --api-key is required");
    process.exit(1);
  }

  generateSceneImage({
    sceneText,
    sceneType,
    style,
    aspectRatio,
    outputPath,
    apiKey,
  })
    .then((result) => {
      console.log("\n=== Generation Complete ===");
      console.log("Output:", result.imagePath);
      console.log("Cached:", result.cached || false);

      if (scenesPath && sceneId) {
        const imageUrl = `scene-images/${sceneId}.png`;
        writeImageUrlToScenes(scenesPath, sceneId, imageUrl);
      }

      process.exit(0);
    })
    .catch((err) => {
      console.error("Generation failed:", err);
      process.exit(1);
    });
}

module.exports = { generateSceneImage, buildPrompt };