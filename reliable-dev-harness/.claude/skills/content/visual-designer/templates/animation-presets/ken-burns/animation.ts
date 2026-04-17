import {
  AnimationType,
  Easing,
} from "../../../types/animation";

export const KEN_BURNS_PRESET = {
  name: "ken-burns",
  description: "电影感效果，缓慢的缩放和位移，适合叙事性内容",
  enter: {
    type: AnimationType.KEN_BURNS_IN,
    duration: 1.5,
    easing: Easing.EASE_IN_OUT,
  },
  exit: {
    type: AnimationType.KEN_BURNS_OUT,
    duration: 1.2,
    easing: Easing.EASE_IN,
  },
  emphasis: {
    type: AnimationType.SLOW_ZOOM,
    scale: 1.03,
    duration: 0.8,
  },
  transition: {
    type: AnimationType.CROSSFADE,
    duration: 25,
  },
  kenBurnsEffect: {
    minZoom: 1.0,
    maxZoom: 1.15,
    panAmount: 30,
    duration: 8,
  },
};

export const kenBurnsEnter = {
  type: AnimationType.KEN_BURNS_IN,
  duration: 1.5,
  easing: Easing.EASE_IN_OUT,
};

export const kenBurnsExit = {
  type: AnimationType.KEN_BURNS_OUT,
  duration: 1.2,
  easing: Easing.EASE_IN,
};

export const kenBurnsEmphasis = {
  type: AnimationType.SLOW_ZOOM,
  scale: 1.03,
  duration: 0.8,
};