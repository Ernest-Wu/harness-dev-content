/**
 * layered-text animation
 *
 * Overlapping text layers with 3D transform effect.
 * Three text layers at different depths create a rich, cinematic feel.
 *
 * Usage:
 *   import { LAYERED_TEXT_CSS } from './layered-text/animation';
 *
 * In HTML:
 *   <div class="text-layer-3d">
 *     <div class="layer layer-back">深层文字</div>
 *     <div class="layer layer-mid">中层文字</div>
 *     <div class="layer layer-front">前景文字</div>
 *   </div>
 */

export const LAYERED_TEXT_CSS = `
.text-layer-3d {
  position: relative;
  display: inline-block;
  -webkit-perspective: 500px;
  perspective: 500px;
}

.layer {
  position: absolute;
  top: 0;
  left: 0;
  white-space: nowrap;
}

.layer-back {
  color: #1e1e3f;
  -webkit-transform: translateZ(-20px) rotateX(5deg);
  transform: translateZ(-20px) rotateX(5deg);
  opacity: 0.5;
}

.layer-mid {
  color: #4a4a8f;
  -webkit-transform: translateZ(-10px) rotateX(2deg);
  transform: translateZ(-10px) rotateX(2deg);
  opacity: 0.7;
}

.layer-front {
  color: #ffffff;
  -webkit-transform: translateZ(0);
  transform: translateZ(0);
  text-shadow: 0 0 20px rgba(99, 102, 241, 0.5);
  position: relative;
}

.layer {
  opacity: 0;
  -webkit-animation: layerReveal 0.8s ease-out forwards;
  animation: layerReveal 0.8s ease-out forwards;
}

.layer-front {
  -webkit-animation-delay: 0s;
  animation-delay: 0s;
}

.layer-mid {
  -webkit-animation-delay: 0.15s;
  animation-delay: 0.15s;
}

.layer-back {
  -webkit-animation-delay: 0.3s;
  animation-delay: 0.3s;
}

@keyframes layerReveal {
  0% {
    opacity: 0;
    -webkit-transform: translateY(20px) rotateX(-10deg);
    transform: translateY(20px) rotateX(-10deg);
  }
  100% {
    opacity: 1;
    -webkit-transform: translateY(0) rotateX(0);
    transform: translateY(0) rotateX(0);
  }
}

.layer-back.layerReveal {
  -webkit-animation-delay: 0.3s;
}

.layer-mid.layerReveal {
  -webkit-animation-delay: 0.15s;
}

.layer-front.layerReveal {
  -webkit-animation-delay: 0s;
}
`;

/**
 * Simpler version that works with a single text element
 * Uses CSS pseudo-elements to create the layered effect
 */
export const LAYERED_TEXT_SIMPLE_CSS = `
.text-layered {
  position: relative;
  display: inline-block;
}

.text-layered::before,
.text-layered::after {
  content: attr(data-text);
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

.text-layered::before {
  color: #1e1e3f;
  -webkit-transform: translateZ(-15px) rotateX(3deg);
  transform: translateZ(-15px) rotateX(3deg);
  opacity: 0.5;
  animation: layerBack 0.8s ease-out 0.2s forwards;
}

.text-layered::after {
  color: #4a4a8f;
  -webkit-transform: translateZ(-5px) rotateX(1deg);
  transform: translateZ(-5px) rotateX(1deg);
  opacity: 0.7;
  animation: layerMid 0.8s ease-out 0.1s forwards;
}

.text-layered {
  color: #ffffff;
  text-shadow: 0 0 20px rgba(99, 102, 241, 0.5);
  -webkit-animation: layerFront 0.8s ease-out forwards;
  animation: layerFront 0.8s ease-out forwards;
  position: relative;
  z-index: 1;
}

@keyframes layerBack {
  0% { opacity: 0; -webkit-transform: translateY(20px) rotateX(-10deg); }
  100% { opacity: 0.5; -webkit-transform: translateY(0) rotateX(3deg); }
}

@keyframes layerMid {
  0% { opacity: 0; -webkit-transform: translateY(20px) rotateX(-10deg); }
  100% { opacity: 0.7; -webkit-transform: translateY(0) rotateX(1deg); }
}

@keyframes layerFront {
  0% { opacity: 0; -webkit-transform: translateY(20px); }
  100% { opacity: 1; -webkit-transform: translateY(0); }
}
`;