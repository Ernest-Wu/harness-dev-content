/**
 * 口播稿解析器
 * 将 Markdown 口播稿解析为结构化 Scene JSON
 * 输出是所有阶段的单一数据源（HTML 预览 + Remotion 渲染）
 */

const CHINESE_STOP_WORDS = new Set([
  "年的", "月的", "日的", "时的", "分的", "秒的",
  "是的", "有的", "没有", "不是", "这是", "那是",
  "什么", "怎么", "怎样", "这个", "那个", "哪个",
  "他们", "她们", "我们", "你们", "它的", "他的",
  "她的", "可以", "可能", "已经", "正在", "还是",
  "但是", "因为", "所以", "如果", "虽然", "然后",
  "而且", "并且", "或者", "以及", "对于", "关于",
  "通过", "使用", "进行", "一个", "一些", "一般",
  "一起", "一直", "一样", "一点", "感觉", "觉得",
  "知道", "看到", "听到", "说到", "出来", "起来",
  "下来", "过来", "回来", "的事", "的人", "的话",
  "了的", "是在", "有的", "要的", "去的", "来的",
  "做的", "说的", "想的", "看的", "听的", "用的",
  "句话", "个人", "时候", "地方", "东西", "事情",
  "问题", "方法", "原因", "结果", "目的", "条件",
  "其实", "那里", "这里", "这些", "那些", "只有",
  "而且", "不过", "同时", "之后", "之前", "之间",
]);

const TRAILING_PARTICLES = /[的了的在和与或但所以而且]/;

type VisualBeatType = "hook-reveal" | "keyword-highlight" | "number-pop" | "quote-reveal" | "split-contrast";

interface VisualBeat {
  at: number;
  type: VisualBeatType;
  target?: string;
}

interface Scene {
  id: string;
  type: "开场钩子" | "正文段落" | "结尾引导";
  text: string;
  estimatedDuration: number;
  keyWords: string[];
  animationHint: "typewriter" | "fade" | "slide" | "emphasize";
  visualFocus: "数据展示" | "概念解释" | "案例呈现" | "纯文字";
  visualType: "keyword-pill" | "big-number" | "quote" | "paragraph";
  imageUrl?: string;
  audioUrl?: string;
  audioDuration?: number;
  stylePreset?: string;
  visualBeats?: VisualBeat[];
}

interface ParsedScript {
  title: string;
  style: string;
  duration: string;
  wordCount: number;
  platform: string;
  scenes: Scene[];
}

function inferVisualFocus(text: string, type: Scene["type"]): Scene["visualFocus"] {
  const hasNumbers = /\d+[%万亿千百十倍]/.test(text);
  const hasComparison = /[比对比增长下降提升超过]/.test(text);
  const hasConceptTerms = /[叫做称定义为概念原理机制逻辑]/.test(text);
  const hasCaseTerms = /[比如例如案例故事实例公司人名]/.test(text);

  if (hasNumbers && hasComparison) return "数据展示";
  if (hasConceptTerms) return "概念解释";
  if (hasCaseTerms) return "案例呈现";
  if (type === "结尾引导") return "纯文字";
  return "纯文字";
}

function inferVisualType(
  text: string,
  visualFocus: Scene["visualFocus"],
  type: Scene["type"],
): Scene["visualType"] {
  if (type === "结尾引导") return "paragraph";
  if (visualFocus === "数据展示") return "big-number";
  const hasQuoteLike = /「[^」]+」|"[^"]+"|"[^"]+"/.test(text);
  if (hasQuoteLike) return "quote";
  if (text.length <= 30) return "keyword-pill";
  return "paragraph";
}

function extractKeyWords(text: string): string[] {
  const segments: string[] = [];
  const chineseChars = text.match(/[\u4e00-\u9fa5]+/g) || [];

  for (const segment of chineseChars) {
    for (let len = 4; len >= 2; len--) {
      for (let i = 0; i <= segment.length - len; i++) {
        const word = segment.substring(i, i + len);
        if (!CHINESE_STOP_WORDS.has(word) && !TRAILING_PARTICLES.test(word.slice(-1))) {
          segments.push(word);
        }
      }
    }
  }

  const englishWords = text.match(/[a-zA-Z]{2,}/gi) || [];
  const allCandidates = [...segments, ...englishWords];

  const freq: Record<string, number> = {};
  for (const w of allCandidates) {
    freq[w] = (freq[w] || 0) + 1;
  }

  return Object.entries(freq)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 5)
    .map(([word]) => word);
}

function inferVisualBeats(text: string, type: Scene["type"], estimatedDuration: number): VisualBeat[] {
  const beats: VisualBeat[] = [];

  if (type === "开场钩子") {
    beats.push({ at: 0, type: "hook-reveal" });
  }

  const numberMatches = Array.from(text.matchAll(/(\d+(?:\.\d+)?)\s*(%|倍|万|亿|千|百|十)/g));
  for (const match of numberMatches) {
    const target = match[1] + match[2];
    const index = match.index ?? 0;
    const at = Math.min(estimatedDuration * 0.3 + (index / text.length) * estimatedDuration * 0.5, estimatedDuration - 2);
    beats.push({ at: Math.round(at * 10) / 10, type: "number-pop", target });
  }

  const quoteMatch = text.match(/「([^」]+)」|"([^"]+)"|"([^"]+)"/);
  if (quoteMatch) {
    const target = quoteMatch[1] || quoteMatch[2] || quoteMatch[3];
    const at = Math.min(estimatedDuration * 0.4, estimatedDuration - 2);
    beats.push({ at: Math.round(at * 10) / 10, type: "quote-reveal", target });
  }

  const comparisonMatch = text.match(/([比从].*?到.*?[倍%万])/);
  if (comparisonMatch) {
    const at = Math.min(estimatedDuration * 0.5, estimatedDuration - 2);
    beats.push({ at: Math.round(at * 10) / 10, type: "split-contrast" });
  }

  const keyTerms = ["关键", "核心", "本质", "秘密", "真相", "重点"];
  for (const term of keyTerms) {
    const idx = text.indexOf(term);
    if (idx >= 0) {
      const at = Math.min(estimatedDuration * (idx / text.length) + 1, estimatedDuration - 1);
      beats.push({ at: Math.round(at * 10) / 10, type: "keyword-highlight", target: term });
      break;
    }
  }

  beats.sort((a, b) => a.at - b.at);

  const deduped: VisualBeat[] = [];
  for (const beat of beats) {
    if (deduped.length === 0 || beat.at - deduped[deduped.length - 1].at >= 1.5) {
      deduped.push(beat);
    }
  }

  return deduped.slice(0, 4);
}

function createScene(
  text: string,
  type: "开场钩子" | "正文段落" | "结尾引导",
  index: number,
): Scene {
  const cleanText = text.replace(/\n+/g, " ").replace(/\s+/g, " ").trim();
  const wordCount = cleanText.length;
  const estimatedDuration = Math.max(5, Math.round(wordCount / 5));
  const keyWords = extractKeyWords(cleanText);
  const visualFocus = inferVisualFocus(cleanText, type);
  const visualType = inferVisualType(cleanText, visualFocus, type);
  const visualBeats = inferVisualBeats(cleanText, type, estimatedDuration);

  let animationHint: Scene["animationHint"] = "fade";
  if (type === "开场钩子") {
    animationHint = "emphasize";
  } else if (estimatedDuration > 20) {
    animationHint = "typewriter";
  } else if (type === "结尾引导") {
    animationHint = "slide";
  }

  return {
    id: `scene-${String(index + 1).padStart(2, "0")}`,
    type,
    text: cleanText,
    estimatedDuration,
    keyWords,
    animationHint,
    visualFocus,
    visualType,
    visualBeats,
  };
}

export function parseScript(markdown: string): ParsedScript {
  const lines = markdown.split("\n");

  let title = "";
  let style = "";
  let duration = "";
  let currentSection = "";
  let currentText: string[] = [];

  const scenes: Scene[] = [];
  let sceneCount = 0;

  for (const line of lines) {
    if (line.startsWith("# ") && !title) {
      title = line.slice(2).trim();
      continue;
    }

    const styleMatch = line.match(/\*\*风格\*\*[：:]([^|]+)/);
    if (styleMatch) style = styleMatch[1].replace(/\*\*/g, "").trim();

    const durationMatch = line.match(/\*\*时长\*\*[：:]([^|]+)/);
    if (durationMatch) duration = durationMatch[1].replace(/\*\*/g, "").trim();

    if (line.startsWith("## 开场钩子")) {
      currentSection = "开场钩子";
      continue;
    }
    if (line.startsWith("## 正文")) {
      if (currentText.length > 0) {
        scenes.push(createScene(currentText.join("\n"), currentSection as Scene["type"], sceneCount++));
        currentText = [];
      }
      currentSection = "正文段落";
      continue;
    }
    if (line.startsWith("## 结尾引导")) {
      if (currentText.length > 0) {
        scenes.push(createScene(currentText.join("\n"), currentSection as Scene["type"], sceneCount++));
        currentText = [];
      }
      currentSection = "结尾引导";
      continue;
    }

    if (line.startsWith("---") || !line.trim()) continue;

    if (currentSection && !line.startsWith("### 段落")) {
      currentText.push(line);
    }

    const paragraphMatch = line.match(/^### 段落\d+ \[约(\d+)秒\]/);
    if (paragraphMatch) {
      if (currentText.length > 0) {
        scenes.push(createScene(currentText.join("\n"), currentSection as Scene["type"], sceneCount++));
        currentText = [];
      }
    }
  }

  if (currentText.length > 0) {
    scenes.push(createScene(currentText.join("\n"), currentSection as Scene["type"], sceneCount++));
  }

  return {
    title,
    style,
    duration,
    wordCount: markdown.replace(/[#*\n]/g, "").length,
    platform: "douyin",
    scenes,
  };
}

export function generateSceneSummary(parsed: ParsedScript): string {
  let summary = `# 场景划分方案\n\n`;
  summary += `**视频标题**: ${parsed.title}\n`;
  summary += `**风格**: ${parsed.style} | **时长**: ${parsed.duration} | **平台**: ${parsed.platform}\n\n`;

  for (const scene of parsed.scenes) {
    summary += `## ${scene.id} - ${scene.type} (约 ${scene.estimatedDuration} 秒)\n`;
    summary += `- 关键词: ${scene.keyWords.join(", ")}\n`;
    summary += `- 动画: ${scene.animationHint}\n`;
    summary += `- 视觉焦点: ${scene.visualFocus}\n`;
    summary += `- 视觉类型: ${scene.visualType}\n`;
    if (scene.visualBeats && scene.visualBeats.length > 0) {
      summary += `- 视觉节拍: ${scene.visualBeats.map(b => `[${b.at}s] ${b.type}${b.target ? `(${b.target})` : ""}`).join(" → ")}\n`;
    }
    summary += `- 内容: "${scene.text.slice(0, 50)}${scene.text.length > 50 ? "..." : ""}"\n\n`;
  }

  const totalSeconds = parsed.scenes.reduce((sum, s) => sum + s.estimatedDuration, 0);
  summary += `**总预估时长**: ${totalSeconds} 秒 (${Math.floor(totalSeconds / 60)}分${totalSeconds % 60}秒)\n`;

  return summary;
}
