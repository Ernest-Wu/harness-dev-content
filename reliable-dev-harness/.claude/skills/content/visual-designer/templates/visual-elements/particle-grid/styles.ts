/**
 * particle-grid - Animated particle field with grid overlay
 *
 * Provides a dynamic tech-inspired background with floating particles
 * and a subtle grid overlay.
 *
 * Usage:
 *   import { PARTICLE_GRID_CONFIG, particleGridStyles } from './particle-grid/styles';
 *
 * In HTML:
 *   <div class="visual-particle-grid">
 *     <canvas class="particle-canvas" data-particle-config='{"count":50,"color":"#a855f7"}'></canvas>
 *     <div class="grid-overlay"></div>
 *     <!-- slide content -->
 *   </div>
 */

export const PARTICLE_GRID_CONFIG = {
  name: "particle-grid",
  description: "动态粒子场+网格背景，科技感",
  defaultConfig: {
    count: 50,           // number of particles
    color: "#a855f7",    // primary particle color (purple)
    minSize: 1,
    maxSize: 3,
    speed: { x: 0.2, y: 0.1 },
    opacity: { min: 0.3, max: 0.8 },
  }
};

export const particleGridStyles = {
  container: {
    position: "relative",
    width: "100%",
    height: "100%",
    overflow: "hidden",
    background: "#0a0a12",
  },
  canvas: {
    position: "absolute",
    inset: "0",
    width: "100%",
    height: "100%",
    opacity: "0.6",
  },
  gridOverlay: {
    position: "absolute",
    inset: "0",
    backgroundImage: `
      linear-gradient(rgba(99, 102, 241, 0.03) 1px, transparent 1px),
      linear-gradient(90deg, rgba(99, 102, 241, 0.03) 1px, transparent 1px)
    `,
    backgroundSize: "40px 40px",
    pointerEvents: "none" as const,
  },
  content: {
    position: "relative",
    zIndex: 5,
  }
};

/**
 * JavaScript for initializing particle animation
 * This should be inlined as a <script> tag in the HTML
 */
export const PARTICLE_INIT_SCRIPT = `
(function() {
  const canvas = document.querySelector('.particle-canvas');
  if (!canvas) return;

  const config = JSON.parse(canvas.dataset.particleConfig || '{}');
  const count = config.count || 50;
  const color = config.color || '#a855f7';
  const minSize = config.minSize || 1;
  const maxSize = config.maxSize || 3;
  const speedX = config.speedX || 0.2;
  const speedY = config.speedY || 0.1;

  const ctx = canvas.getContext('2d');
  let width, height;
  let particles = [];

  function resize() {
    width = canvas.width = canvas.offsetWidth;
    height = canvas.height = canvas.offsetHeight;
  }

  function createParticle() {
    return {
      x: Math.random() * width,
      y: Math.random() * height,
      size: minSize + Math.random() * (maxSize - minSize),
      speedX: (Math.random() - 0.5) * speedX,
      speedY: (Math.random() - 0.5) * speedY,
      opacity: 0.3 + Math.random() * 0.5,
    };
  }

  function initParticles() {
    particles = [];
    for (let i = 0; i < count; i++) {
      particles.push(createParticle());
    }
  }

  function drawParticle(p) {
    ctx.beginPath();
    ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
    ctx.fillStyle = color;
    ctx.globalAlpha = p.opacity;
    ctx.fill();
  }

  function updateParticle(p) {
    p.x += p.speedX;
    p.y += p.speedY;

    // Wrap around edges
    if (p.x < 0) p.x = width;
    if (p.x > width) p.x = 0;
    if (p.y < 0) p.y = height;
    if (p.y > height) p.y = 0;
  }

  function animate() {
    ctx.clearRect(0, 0, width, height);
    particles.forEach(p => {
      updateParticle(p);
      drawParticle(p);
    });
    ctx.globalAlpha = 1;
    requestAnimationFrame(animate);
  }

  // Initialize
  resize();
  initParticles();
  window.addEventListener('resize', () => {
    resize();
    initParticles();
  });

  // Start animation
  animate();
})();
`;