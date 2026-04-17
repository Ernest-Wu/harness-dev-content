import {
  AnimationType,
  Easing,
} from "../../../types/animation";

export const KINETIC_TYPOGRAPHY_PRESET = {
  name: "kinetic-typography",
  description: "文字逐字/逐行弹入+轻微旋转，适合标题和强调内容",
  enter: {
    type: AnimationType.SPRING_BOUNCE,
    stagger: 0.05,
    duration: 0.6,
    scale: { from: 0.5, to: 1 },
    rotation: { from: -5, to: 0 },
    easing: Easing.EASE_OUT,
  },
  exit: {
    type: AnimationType.FADE_SCALE_OUT,
    duration: 0.4,
    scale: 0.9,
    easing: Easing.EASE_IN,
  },
  emphasis: {
    type: AnimationType.PULSE,
    scale: 1.05,
    duration: 0.2,
  },
  transition: {
    type: AnimationType.CROSSFADE,
    duration: 25,
  },
};

export const kineticTypographyEnter = {
  type: AnimationType.SPRING_BOUNCE,
  stagger: 0.05,
  duration: 0.6,
  scale: { from: 0.5, to: 1 },
  rotation: { from: -5, to: 0 },
  easing: Easing.EASE_OUT,
};

export const kineticTypographyExit = {
  type: AnimationType.FADE_SCALE_OUT,
  duration: 0.4,
  scale: 0.9,
  easing: Easing.EASE_IN,
};

export const kineticTypographyEmphasis = {
  type: AnimationType.PULSE,
  scale: 1.05,
  duration: 0.2,
};
