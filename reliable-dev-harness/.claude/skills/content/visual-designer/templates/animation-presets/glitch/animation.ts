import {
  AnimationType,
  Easing,
} from "../../../types/animation";

export const GLITCH_PRESET = {
  name: "glitch",
  description: "数字故障效果，适合科技感和赛博朋克内容",
  enter: {
    type: AnimationType.GLITCH_IN,
    duration: 0.3,
    intensity: 0.8,
    easing: Easing.EASE_IN,
  },
  exit: {
    type: AnimationType.GLITCH_OUT,
    duration: 0.25,
    intensity: 0.6,
    easing: Easing.EASE_OUT,
  },
  emphasis: {
    type: AnimationType.GLITCH_PULSE,
    scale: 1.02,
    duration: 0.15,
    intensity: 0.4,
  },
  transition: {
    type: AnimationType.GLITCH_DISSOLVE,
    duration: 20,
  },
};

export const glitchEnter = {
  type: AnimationType.GLITCH_IN,
  duration: 0.3,
  intensity: 0.8,
  easing: Easing.EASE_IN,
};

export const glitchExit = {
  type: AnimationType.GLITCH_OUT,
  duration: 0.25,
  intensity: 0.6,
  easing: Easing.EASE_OUT,
};

export const glitchEmphasis = {
  type: AnimationType.GLITCH_PULSE,
  scale: 1.02,
  duration: 0.15,
  intensity: 0.4,
};
