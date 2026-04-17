/**
 * char-by-char animation
 *
 * Character-by-character reveal with color gradient sweep.
 * Each character appears sequentially with a gradient color effect.
 *
 * Usage:
 *   import { CHAR_BY_CHAR_CSS, charByCharScript } from './char-by-char/animation';
 *
 * In HTML:
 *   <div class="text-char-reveal">每个字符都会单独动画</div>
 */

export const CHAR_BY_CHAR_CSS = `
.text-char-reveal {
  display: inline-block;
}

.text-char-reveal .char {
  display: inline-block;
  opacity: 0;
  transform: translateY(10px);
  -webkit-transform: translateY(10px);
}

.text-char-reveal .char.revealed {
  opacity: 1;
  transform: translateY(0);
  -webkit-transform: translateY(0);
  background: linear-gradient(90deg, #6366F1, #a855f7, #ec4899);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  background-size: 200% 100%;
  animation: charReveal 0.4s ease-out forwards, gradientSweep 2s ease-in-out 0.4s infinite;
  -webkit-animation: charReveal 0.4s ease-out forwards, gradientSweep 2s ease-in-out 0.4s infinite;
}

.text-char-reveal .char:nth-child(1) { animation-delay: 0.05s, 0.4s; -webkit-animation-delay: 0.05s, 0.4s; }
.text-char-reveal .char:nth-child(2) { animation-delay: 0.1s, 0.45s; -webkit-animation-delay: 0.1s, 0.45s; }
.text-char-reveal .char:nth-child(3) { animation-delay: 0.15s, 0.5s; -webkit-animation-delay: 0.15s, 0.5s; }
.text-char-reveal .char:nth-child(4) { animation-delay: 0.2s, 0.55s; -webkit-animation-delay: 0.2s, 0.55s; }
.text-char-reveal .char:nth-child(5) { animation-delay: 0.25s, 0.6s; -webkit-animation-delay: 0.25s, 0.6s; }
.text-char-reveal .char:nth-child(6) { animation-delay: 0.3s, 0.65s; -webkit-animation-delay: 0.3s, 0.65s; }
.text-char-reveal .char:nth-child(7) { animation-delay: 0.35s, 0.7s; -webkit-animation-delay: 0.35s, 0.7s; }
.text-char-reveal .char:nth-child(8) { animation-delay: 0.4s, 0.75s; -webkit-animation-delay: 0.4s, 0.75s; }
.text-char-reveal .char:nth-child(9) { animation-delay: 0.45s, 0.8s; -webkit-animation-delay: 0.45s, 0.8s; }
.text-char-reveal .char:nth-child(10) { animation-delay: 0.5s, 0.85s; -webkit-animation-delay: 0.5s, 0.85s; }
.text-char-reveal .char:nth-child(n+11) { animation-delay: 0.5s, 0.85s; -webkit-animation-delay: 0.5s, 0.85s; }

@keyframes charReveal {
  0% { opacity: 0; transform: translateY(10px); -webkit-transform: translateY(10px); }
  100% { opacity: 1; transform: translateY(0); -webkit-transform: translateY(0); }
}

@keyframes gradientSweep {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}

@-webkit-keyframes charReveal {
  0% { opacity: 0; -webkit-transform: translateY(10px); }
  100% { opacity: 1; -webkit-transform: translateY(0); }
}

@-webkit-keyframes gradientSweep {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}
`;

/**
 * JavaScript to split text into characters and trigger reveal animation
 */
export const charByCharScript = `
(function() {
  const elements = document.querySelectorAll('.text-char-reveal');
  elements.forEach(el => {
    const text = el.textContent;
    el.innerHTML = '';
    text.split('').forEach((char, i) => {
      const span = document.createElement('span');
      span.className = 'char';
      span.textContent = char === ' ' ? '\\u00A0' : char;
      el.appendChild(span);
    });
    // Trigger animation after a short delay
    setTimeout(() => {
      el.querySelectorAll('.char').forEach((char, i) => {
        setTimeout(() => char.classList.add('revealed'), i * 50);
      });
    }, 300);
  });
})();
`;