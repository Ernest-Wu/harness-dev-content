/**
 * glow-effects - Animated gradient glow orbs
 *
 * Provides floating gradient orb effects behind content.
 * Multiple orbs with different sizes, positions, and animation delays
 * create a rich, dynamic background atmosphere.
 *
 * Usage:
 *   import { GLOW_EFFECTS_CONFIG, glowEffectsStyles } from './glow-effects/styles';
 *
 * In HTML:
 *   <div class="visual-glow-effects">
 *     <div class="glow-orb glow-orb-1"></div>
 *     <div class="glow-orb glow-orb-2"></div>
 *     <div class="glow-orb glow-orb-3"></div>
 *   </div>
 */

export const GLOW_EFFECTS_CONFIG = {
  name: "glow-effects",
  description: "渐变光晕动画，科技感光球漂浮效果",
  orbCount: 3,
  animationDuration: 8,  // seconds per cycle
};

export const glowEffectsStyles = {
  container: {
    position: "absolute",
    inset: "0",
    overflow: "hidden",
    pointerEvents: "none" as const,
  },
  orb: {
    position: "absolute",
    borderRadius: "50%",
    filter: "blur(80px)",
    opacity: "0.4",
    mixBlendMode: "screen",
    pointerEvents: "none" as const,
  },
  orb1: {
    width: "40%",
    height: "60%",
    background: "radial-gradient(circle, #7c3aed 0%, transparent 70%)",
    top: "-10%",
    right: "-5%",
    animation: "orbFloat1 8s ease-in-out infinite",
  },
  orb2: {
    width: "35%",
    height: "50%",
    background: "radial-gradient(circle, #6366F1 0%, transparent 70%)",
    bottom: "-10%",
    left: "10%",
    animation: "orbFloat2 10s ease-in-out infinite",
    animationDelay: "2s",
  },
  orb3: {
    width: "25%",
    height: "40%",
    background: "radial-gradient(circle, #EC4899 0%, transparent 70%)",
    top: "30%",
    left: "60%",
    animation: "orbFloat3 12s ease-in-out infinite",
    animationDelay: "4s",
  },
};

/**
 * CSS Keyframes for glow orb animations
 */
export const GLOW_EFFECTS_CSS = `
@keyframes orbFloat1 {
  0%, 100% {
    transform: translate(0, 0) scale(1);
    opacity: 0.4;
  }
  33% {
    transform: translate(-30px, 20px) scale(1.05);
    opacity: 0.5;
  }
  66% {
    transform: translate(20px, -10px) scale(0.95);
    opacity: 0.35;
  }
}

@keyframes orbFloat2 {
  0%, 100% {
    transform: translate(0, 0) scale(1);
    opacity: 0.35;
  }
  50% {
    transform: translate(40px, -30px) scale(1.1);
    opacity: 0.45;
  }
}

@keyframes orbFloat3 {
  0%, 100% {
    transform: translate(0, 0) scale(1);
    opacity: 0.3;
  }
  25% {
    transform: translate(-20px, 15px) scale(1.08);
    opacity: 0.4;
  }
  75% {
    transform: translate(15px, -25px) scale(0.92);
    opacity: 0.25;
  }
}

.glow-orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  -webkit-filter: blur(80px);
  opacity: 0.4;
  mix-blend-mode: screen;
  -webkit-mix-blend-mode: screen;
  pointer-events: none;
}

.glow-orb-1 {
  width: 40%;
  height: 60%;
  background: radial-gradient(circle, #7c3aed 0%, transparent 70%);
  top: -10%;
  right: -5%;
  animation: orbFloat1 8s ease-in-out infinite;
}

.glow-orb-2 {
  width: 35%;
  height: 50%;
  background: radial-gradient(circle, #6366F1 0%, transparent 70%);
  bottom: -10%;
  left: 10%;
  animation: orbFloat2 10s ease-in-out infinite;
  animation-delay: 2s;
}

.glow-orb-3 {
  width: 25%;
  height: 40%;
  background: radial-gradient(circle, #EC4899 0%, transparent 70%);
  top: 30%;
  left: 60%;
  animation: orbFloat3 12s ease-in-out infinite;
  animation-delay: 4s;
}
`;