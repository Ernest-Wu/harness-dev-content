import {
  AnimationType,
  Easing,
} from "../../../types/animation";

export const TYPEWRITER_FADE_PRESET = {
  name: "typewriter-fade",
  description: "打字机效果配合淡入淡出",
  enter: {
    type: AnimationType.TYPEWRITER,
    speed: 0.1,
    easing: Easing.EASE_OUT,
  },
  exit: {
    type: AnimationType.FADE,
    duration: 0.3,
  },
  emphasis: {
    type: AnimationType.SCALE_PULSE,
    scale: 1.05,
    duration: 0.2,
  },
  transition: {
    type: AnimationType.FADE,
    duration: 15,
  },
};

export const typewriterFadeEnter = {
  type: AnimationType.TYPEWRITER,
  speed: 0.1,
  easing: Easing.EASE_OUT,
};

export const typewriterFadeExit = {
  type: AnimationType.FADE,
  duration: 0.3,
};

export const typewriterFadeEmphasis = {
  type: AnimationType.SCALE_PULSE,
  scale: 1.05,
  duration: 0.2,
};