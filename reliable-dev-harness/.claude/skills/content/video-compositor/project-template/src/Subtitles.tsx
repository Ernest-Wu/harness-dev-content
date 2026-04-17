import React from "react";
import { useCurrentFrame, useVideoConfig, spring } from "remotion";
import type { SubtitleLine } from "./types";

interface SubtitlesProps {
  subtitles: SubtitleLine[];
}

export const Subtitles: React.FC<SubtitlesProps> = ({ subtitles }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const currentMs = (frame / fps) * 1000;

  const activeIndex = subtitles.findIndex(
    (s) => s.startMs <= currentMs && s.endMs > currentMs
  );
  if (activeIndex === -1) return null;

  const active = subtitles[activeIndex];
  const lineDurationMs = active.endMs - active.startMs;
  const elapsedMs = currentMs - active.startMs;
  const minTypewriterMs = 800;
  const typewriterDurationMs = Math.max(lineDurationMs * 0.7, minTypewriterMs);

  const progress = Math.min(elapsedMs / typewriterDurationMs, 1);
  const visibleChars = Math.max(1, Math.floor(progress * active.text.length));
  const displayText = active.text.slice(0, visibleChars);

  // Spring entrance when a new subtitle line appears
  const lineStartFrame = Math.round((active.startMs / 1000) * fps);
  const localFrame = frame - lineStartFrame;
  const scale = spring({
    frame: localFrame,
    fps,
    config: { damping: 200, mass: 0.5, stiffness: 200 },
    from: 0.92,
    to: 1,
  });
  const opacity = spring({
    frame: localFrame,
    fps,
    config: { damping: 200, mass: 0.5, stiffness: 200 },
    from: 0,
    to: 1,
  });

  return (
    <div
      style={{
        position: "absolute",
        bottom: "clamp(3rem, 8vh, 5rem)",
        left: "50%",
        transform: `translateX(-50%) scale(${scale})`,
        opacity,
        maxWidth: "min(90vw, 900px)",
        width: "100%",
        textAlign: "center",
        zIndex: 100,
        padding: "0 clamp(1rem, 4vw, 2rem)",
        boxSizing: "border-box",
        pointerEvents: "none",
      }}
    >
      <div
        style={{
          display: "inline-block",
          backgroundColor: "rgba(0,0,0,0.6)",
          color: "#ffffff",
          fontSize: "clamp(1rem, 3vw, 1.6rem)",
          fontWeight: 600,
          padding: "clamp(0.4rem, 1vw, 0.8rem) clamp(0.8rem, 2vw, 1.5rem)",
          borderRadius: "9999px",
          lineHeight: 1.4,
          fontFamily: '"IBM Plex Sans", sans-serif',
          whiteSpace: "pre-wrap",
        }}
      >
        {displayText}
        <span
          style={{
            display: "inline-block",
            width: "2px",
            height: "1em",
            backgroundColor: "rgba(255,255,255,0.8)",
            marginLeft: "2px",
            verticalAlign: "middle",
            animation: "subtitle-cursor 0.6s steps(1) infinite",
          }}
        />
      </div>
      <style>{`
        @keyframes subtitle-cursor {
          0%, 100% { opacity: 1; }
          50% { opacity: 0; }
        }
      `}</style>
    </div>
  );
};
