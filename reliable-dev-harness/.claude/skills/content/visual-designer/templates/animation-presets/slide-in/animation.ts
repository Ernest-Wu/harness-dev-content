import {
  AnimationType,
  Easing,
} from "../../../types/animation";

export const SLIDE_IN_PRESET = {
  name: "slide-in",
  description: "文字从侧边滑入",
  enter: {
    type: AnimationType.SLIDE_FROM_LEFT,
    duration: 0.4,
    easing: Easing.EASE_OUT,
  },
  exit: {
    type: AnimationType.SLIDE_TO_RIGHT,
    duration: 0.3,
    easing: Easing.EASE_IN,
  },
  emphasis: {
    type: AnimationType.BOUNCE,
    scale: 1.08,
    duration: 0.3,
  },
  transition: {
    type: AnimationType.SLIDE,
    duration: 20,
  },
};

export const slideInEnter = {
  type: AnimationType.SLIDE_FROM_LEFT,
  duration: 0.4,
  easing: Easing.EASE_OUT,
};

export const slideInExit = {
  type: AnimationType.SLIDE_TO_RIGHT,
  duration: 0.3,
  easing: Easing.EASE_IN,
};

export const slideInEmphasis = {
  type: AnimationType.BOUNCE,
  scale: 1.08,
  duration: 0.3,
};