import React from "react";
import { useCurrentFrame, useVideoConfig, interpolate, AbsoluteFill } from "remotion";
import { OffthreadVideo, staticFile } from "remotion";

interface KenBurnsVideoProps {
  src: string;
  beatCount?: number;
}

export const KenBurnsVideo: React.FC<KenBurnsVideoProps> = ({ src, beatCount = 0 }) => {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();

  const intensity = Math.min(1 + beatCount * 0.03, 1.12);
  const progress = frame / Math.max(durationInFrames, 1);

  const scale = interpolate(progress, [0, 1], [1, intensity], {
    extrapolateRight: "clamp",
  });

  const translateX = interpolate(progress, [0, 1], [0, -12 * intensity], {
    extrapolateRight: "clamp",
  });

  const translateY = interpolate(progress, [0, 1], [0, -8 * intensity], {
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill style={{ overflow: "hidden" }}>
      <OffthreadVideo
        src={staticFile(src)}
        style={{
          width: "100%",
          height: "100%",
          objectFit: "cover",
          transform: `scale(${scale}) translate(${translateX}px, ${translateY}px)`,
        }}
      />
    </AbsoluteFill>
  );
};
