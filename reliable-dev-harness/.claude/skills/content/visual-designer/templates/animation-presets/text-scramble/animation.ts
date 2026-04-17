/**
 * text-scramble animation
 *
 * Random character scramble decode effect - characters rapidly change
 * from random symbols to the final text, creating a "decoding" feel.
 *
 * Usage:
 *   import { TEXT_SCRAMBLE_CSS, textScrambleScript } from './text-scramble/animation';
 *
 * In HTML:
 *   <div class="text-scramble" data-final="最终显示的文字">正在解码...</div>
 */

export const TEXT_SCRAMBLE_CSS = `
.text-scramble {
  opacity: 0;
  animation: scrambleFadeIn 0.5s ease-out forwards;
}

@keyframes scrambleFadeIn {
  0% { opacity: 0; }
  70% { opacity: 0.7; }
  100% { opacity: 1; }
}
`;

/**
 * JavaScript for text scramble effect
 * This creates the actual scramble animation
 */
export const textScrambleScript = `
(function() {
  const CHARS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789#@%&*!§¥€£∆∑';
  const FRAMES = 30;
  const DURATION = 2000; // ms

  class TextScramble {
    constructor(el) {
      this.el = el;
      this.finalText = el.dataset.final || el.textContent;
      this.frame = 0;
      this.frameInterval = DURATION / FRAMES;
      this.startTime = null;
    }

    scramble() {
      if (this.frame < FRAMES) {
        const progress = this.frame / FRAMES;
        const revealedCount = Math.floor(progress * this.finalText.length);

        this.el.textContent = this.finalText.split('').map((char, i) => {
          if (char === ' ' || char === '\\n') return char;
          if (i < revealedCount) return char;
          return CHARS[Math.floor(Math.random() * CHARS.length)];
        }).join('');

        this.frame++;
        setTimeout(() => this.scramble(), this.frameInterval);
      } else {
        this.el.textContent = this.finalText;
      }
    }

    start() {
      this.el.textContent = this.finalText.split('').map(() =>
        CHARS[Math.floor(Math.random() * CHARS.length)]
      ).join('');
      setTimeout(() => this.scramble(), 100);
    }
  }

  // Initialize all scramble elements
  document.querySelectorAll('.text-scramble').forEach(el => {
    const scrambler = new TextScramble(el);
    scrambler.start();
  });
})();
`;