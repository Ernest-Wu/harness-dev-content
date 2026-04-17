/**
 * geometric-lines - SVG line animations
 *
 * Animated SVG geometric lines that draw themselves with gradient colors
 * and have a subtle pulse animation.
 *
 * Usage:
 *   import { GEOMETRIC_LINES_CONFIG, geometricLinesStyles } from './geometric-lines/styles';
 *
 * In HTML:
 *   <div class="visual-geo-lines">
 *     <svg class="geo-svg" viewBox="0 0 1920 1080" preserveAspectRatio="xMidYMid slice">
 *       <defs>
 *         <linearGradient id="lineGrad1" x1="0%" y1="0%" x2="100%" y2="0%">
 *           <stop offset="0%" stop-color="#6366F1" stop-opacity="0"/>
 *           <stop offset="50%" stop-color="#6366F1" stop-opacity="1"/>
 *           <stop offset="100%" stop-color="#a855f7" stop-opacity="0"/>
 *         </linearGradient>
 *       </defs>
 *       <line class="geo-line geo-line-1" x1="0" y1="200" x2="1920" y2="400" stroke="url(#lineGrad1)" stroke-width="1"/>
 *     </svg>
 *   </div>
 */

export const GEOMETRIC_LINES_CONFIG = {
  name: "geometric-lines",
  description: "SVG几何线条动画，渐变色+呼吸效果",
  lineCount: 3,
  animationDuration: 3,  // seconds for draw animation
  pulseDuration: 4,      // seconds for pulse animation
};

export const geometricLinesStyles = {
  container: {
    position: "absolute",
    inset: "0",
    overflow: "hidden",
    pointerEvents: "none" as const,
  },
  svg: {
    width: "100%",
    height: "100%",
    position: "absolute",
    top: "0",
    left: "0",
  },
  line: {
    strokeDasharray: "2000",
    strokeDashoffset: "2000",
    animation: "drawLine 3s ease-out forwards, linePulse 4s ease-in-out infinite",
    strokeWidth: "1",
  },
  line1: {
    animationDelay: "0.5s",
  },
  line2: {
    animationDelay: "1s",
  },
  line3: {
    animationDelay: "1.5s",
  },
};

/**
 * CSS Keyframes for geometric lines
 * These should be included in the HTML <style> block
 */
export const GEOMETRIC_LINES_CSS = `
@keyframes drawLine {
  to { stroke-dashoffset: 0; }
}

@keyframes linePulse {
  0%, 100% { opacity: 0.3; }
  50% { opacity: 0.8; }
}

.geo-line {
  stroke-dasharray: 2000;
  stroke-dashoffset: 2000;
  animation: drawLine 3s ease-out forwards, linePulse 4s ease-in-out infinite;
}

.geo-line-1 { animation-delay: 0.5s; }
.geo-line-2 { animation-delay: 1s; }
.geo-line-3 { animation-delay: 1.5s; }
`;

/**
 * Generates SVG line definitions based on aspect ratio
 */
export function generateSvgLines(aspectRatio: "16:9" | "9:16" | "4:5", accentColor = "#6366F1") {
  const lines = {
    "16:9": [
      { x1: 0, y1: 200, x2: 1920, y2: 400 },
      { x1: 0, y1: 600, x2: 1920, y2: 300 },
      { x1: 0, y1: 800, x2: 1920, y2: 700 },
    ],
    "9:16": [
      { x1: 0, y1: 200, x2: 1080, y2: 400 },
      { x1: 0, y1: 600, x2: 1080, y2: 300 },
      { x1: 0, y1: 1000, x2: 1080, y2: 900 },
    ],
    "4:5": [
      { x1: 0, y1: 200, x2: 1080, y2: 350 },
      { x1: 0, y1: 500, x2: 1080, y2: 300 },
      { x1: 0, y1: 800, x2: 1080, y2: 700 },
    ],
  };

  return lines[aspectRatio] || lines["16:9"];
}