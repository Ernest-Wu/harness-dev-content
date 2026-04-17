/**
 * Video.tsx - Main video composition component
 * Uses TransitionSeries for scene management.
 * Base video is rendered via Playwright; Remotion adds overlays + motion enhancement.
 */
import React from "react";
import {
  TransitionSeries,
  linearTiming,
  springTiming,
} from "@remotion/transitions";
import { fade } from "@remotion/transitions/fade";
import { slide } from "@remotion/transitions/slide";
import { wipe } from "@remotion/transitions/wipe";
import { flip } from "@remotion/transitions/flip";
import { Audio, staticFile, AbsoluteFill } from "remotion";
import { Subtitles } from "./Subtitles";
import { KenBurnsVideo } from "./KenBurnsVideo";
import { BeatOverlay } from "./BeatOverlay";
import { TRANSITION_FRAMES } from "./types";
import type { Scene as SceneType, PlatformKey } from "./types";
import { getSceneDurationInFrames } from "./utils/timing";

export interface VideoProps {
  scenes: SceneType[];
  platform?: PlatformKey;
}

function getTransitionForScenes(fromScene: SceneType, toScene: SceneType) {
  if (fromScene.type === "开场钩子" && toScene.type === "正文段落") {
    return {
      presentation: wipe(),
      timing: springTiming({ config: { damping: 200 }, durationInFrames: TRANSITION_FRAMES }),
    };
  }
  if (fromScene.type === "正文段落" && toScene.type === "开场钩子") {
    return {
      presentation: slide({ direction: "from-bottom" }),
      timing: linearTiming({ durationInFrames: TRANSITION_FRAMES }),
    };
  }
  if (fromScene.type === "正文段落" && toScene.type === "正文段落") {
    return {
      presentation: slide({ direction: "from-right" }),
      timing: linearTiming({ durationInFrames: TRANSITION_FRAMES }),
    };
  }
  if (fromScene.type === "正文段落" && toScene.type === "结尾引导") {
    return {
      presentation: flip(),
      timing: springTiming({ config: { damping: 15 }, durationInFrames: TRANSITION_FRAMES }),
    };
  }
  return {
    presentation: fade(),
    timing: linearTiming({ durationInFrames: TRANSITION_FRAMES }),
  };
}

export const Video: React.FC<VideoProps> = ({ scenes, platform = "bilibili" }) => {
  return (
    <AbsoluteFill style={{ width: "100%", height: "100%", overflow: "hidden", backgroundColor: "#0f0f0f" }}>
      <TransitionSeries>
        {scenes.map((scene, index) => {
          const duration = getSceneDurationInFrames(scene);
          const videoFile = `scene-${String(index).padStart(2, "0")}.mp4`;

          return (
            <React.Fragment key={scene.id}>
              <TransitionSeries.Sequence durationInFrames={duration}>
                <AbsoluteFill>
                  <KenBurnsVideo src={videoFile} beatCount={scene.visualBeats?.length ?? 0} />
                </AbsoluteFill>
                {scene.subtitles && <Subtitles subtitles={scene.subtitles} />}
                <BeatOverlay beats={scene.visualBeats} />
                {scene.audioUrl && (
                  <Audio src={staticFile(scene.audioUrl)} volume={1} />
                )}
              </TransitionSeries.Sequence>

              {index < scenes.length - 1 && (
                <TransitionSeries.Transition
                  {...(getTransitionForScenes(scene, scenes[index + 1]) as any)}
                />
              )}
            </React.Fragment>
          );
        })}
      </TransitionSeries>
    </AbsoluteFill>
  );
};
