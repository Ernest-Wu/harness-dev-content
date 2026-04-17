import React from "react";
import { Sequence, interpolate, useCurrentFrame } from "remotion";
import type { VisualBeat } from "./types";
import { VIDEO_FPS } from "./types";

interface BeatOverlayProps {
  beats?: VisualBeat[];
}

const FocusRing: React.FC = () => {
  const frame = useCurrentFrame();
  const opacity = interpolate(frame, [0, 8, 16], [0, 0.25, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <div
      style={{
        position: "absolute",
        inset: 0,
        border: "6px solid rgba(255,255,255,0.4)",
        opacity,
        pointerEvents: "none",
        zIndex: 50,
      }}
    />
  );
};

export const BeatOverlay: React.FC<BeatOverlayProps> = ({ beats = [] }) => {
  if (beats.length === 0) return null;

  return (
    <>
      {beats.map((beat, i) => {
        const fromFrame = Math.round(beat.at * VIDEO_FPS);
        return (
          <Sequence
            key={`${i}-${beat.at}`}
            from={fromFrame}
            durationInFrames={20}
            layout="none"
          >
            <FocusRing />
          </Sequence>
        );
      })}
    </>
  );
};
