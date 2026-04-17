/**
 * Timing utility functions for Remotion animations
 * Based on remotion-best-practices timing rules
 */
import { interpolate, spring, Easing } from "remotion";
import type { Scene } from "../types";
import { VIDEO_FPS, TRANSITION_FRAMES } from "../types";

/**
 * Standard spring configurations for different animation styles
 */
export const SPRING_PRESETS = {
  /** Smooth, no bounce (subtle reveals) */
  smooth: { damping: 200 },
  /** Snappy, minimal bounce (UI elements) */
  snappy: { damping: 20, stiffness: 200 },
  /** Bouncy entrance (playful animations) */
  bouncy: { damping: 8 },
  /** Heavy, slow, small bounce */
  heavy: { damping: 15, stiffness: 80, mass: 2 },
} as const;

/**
 * Calculate opacity fade animation
 */
export const fadeIn = (
  frame: number,
  startFrame: number,
  durationFrames: number
): number => {
  return interpolate(frame, [startFrame, startFrame + durationFrames], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
};

/**
 * Calculate fade out animation
 */
export const fadeOut = (
  frame: number,
  startFrame: number,
  durationFrames: number
): number => {
  return interpolate(frame, [startFrame, startFrame + durationFrames], [1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
};

/**
 * Calculate slide-in animation from left
 */
export const slideInFromLeft = (
  frame: number,
  startFrame: number,
  durationFrames: number
): number => {
  return interpolate(
    frame,
    [startFrame, startFrame + durationFrames],
    [-100, 0],
    {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
      easing: Easing.out(Easing.quad),
    }
  );
};

/**
 * Calculate typewriter progress (0 to 1)
 */
export const typewriterProgress = (
  frame: number,
  startFrame: number,
  totalFrames: number,
  textLength: number
): number => {
  const progress = interpolate(frame, [startFrame, startFrame + totalFrames], [
    0,
    textLength,
  ]);
  return Math.min(Math.floor(progress), textLength);
};

/**
 * Spring animation helper
 */
export const springValue = (
  frame: number,
  fps: number,
  config?: { damping?: number; stiffness?: number; mass?: number }
): number => {
  return spring({ frame, fps, config });
};

/**
 * Calculate scale entrance animation
 */
export const scaleIn = (
  frame: number,
  startFrame: number,
  durationFrames: number,
  fromScale: number = 0.8,
  toScale: number = 1.0
): number => {
  return interpolate(frame, [startFrame, startFrame + durationFrames], [fromScale, toScale], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.out(Easing.back(1.5)),
  });
};

/**
 * Calculate emphasize animation (scale up slightly)
 */
export const emphasize = (
  frame: number,
  peakFrame: number,
  durationFrames: number
): number => {
  const halfDuration = durationFrames / 2;
  return interpolate(
    frame,
    [peakFrame - halfDuration, peakFrame, peakFrame + halfDuration],
    [1.0, 1.05, 1.0],
    {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
      easing: Easing.inOut(Easing.quad),
    }
  );
};

/**
 * Calculate the duration in frames for a single scene.
 * Uses audioDuration if available, otherwise estimates from animation/length.
 */
export function getSceneDurationInFrames(scene: Scene): number {
  // If audio duration is available, always use it (most accurate)
  if (scene.audioDuration) {
    return Math.ceil(scene.audioDuration * VIDEO_FPS);
  }

  const estimatedFrames = Math.ceil(scene.estimatedDuration * VIDEO_FPS);
  const minFrames = 30;

  switch (scene.animationHint) {
    case "typewriter":
      // Typewriter should span most of the scene duration so text finishes near the end
      return Math.max(estimatedFrames, minFrames);
    case "fade":
      return Math.max(estimatedFrames, 45);
    case "slide":
      return Math.max(estimatedFrames, 40);
    case "emphasize":
      return Math.max(estimatedFrames, 60);
    default:
      return Math.max(estimatedFrames, 45);
  }
}

/**
 * Calculate total frames for all scenes, accounting for transitions.
 * TransitionSeries overlaps frames between consecutive scenes.
 */
export function calculateTotalFrames(scenes: Scene[]): number {
  let total = 0;
  for (let i = 0; i < scenes.length; i++) {
    total += getSceneDurationInFrames(scenes[i]);
    if (i < scenes.length - 1) {
      total -= TRANSITION_FRAMES;
    }
  }
  return Math.max(total, 1);
}
