import {
  AnimationType,
  Easing,
} from "../../../types/animation";

export const SMOOTH_FADE_PRESET = {
  name: "smooth-fade",
  description: "专业级平滑淡入淡出，适合高端品牌内容和电影感视频",
  enter: {
    type: AnimationType.FADE_IN,
    duration: 1.2,
    easing: Easing.EASE_OUT_CUBIC,
  },
  exit: {
    type: AnimationType.FADE_OUT,
    duration: 1.0,
    easing: Easing.EASE_IN_CUBIC,
  },
  emphasis: {
    type: AnimationType.SUBTLE_FLOAT,
    scale: 1.02,
    duration: 0.5,
    easing: Easing.EASE_IN_OUT,
  },
  transition: {
    type: AnimationType.SMOOTH_DISSOLVE,
    duration: 30,
  },
};

export const smoothFadeEnter = {
  type: AnimationType.FADE_IN,
  duration: 1.2,
  easing: Easing.EASE_OUT_CUBIC,
};

export const smoothFadeExit = {
  type: AnimationType.FADE_OUT,
  duration: 1.0,
  easing: Easing.EASE_IN_CUBIC,
};

export const smoothFadeEmphasis = {
  type: AnimationType.SUBTLE_FLOAT,
  scale: 1.02,
  duration: 0.5,
  easing: Easing.EASE_IN_OUT,
};
