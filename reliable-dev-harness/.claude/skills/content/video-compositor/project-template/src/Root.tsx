import React, { useEffect, useState } from "react";
import { Composition, CalculateMetadataFunction, delayRender, continueRender } from "remotion";
import { Video, VideoProps } from "./Video";
import { PLATFORM_PRESETS, VIDEO_FPS } from "./types";
import type { Scene, PlatformKey } from "./types";
import { calculateTotalFrames } from "./utils/timing";
import projectData from "./scenes.json";

const PRESET_FONT_MAP: Record<string, { display: string; body: string }> = {
  "dark-botanical": { display: "Cormorant", body: "IBM Plex Sans" },
  "bold-signal": { display: "Archivo Black", body: "Space Grotesk" },
  "electric-studio": { display: "Manrope", body: "Manrope" },
  "creative-voltage": { display: "Syne", body: "Space Mono" },
  "notebook-tabs": { display: "Bodoni Moda", body: "DM Sans" },
  "pastel-geometry": { display: "Plus Jakarta Sans", body: "Plus Jakarta Sans" },
  "split-pastel": { display: "Outfit", body: "Outfit" },
  "vintage-editorial": { display: "Fraunces", body: "Work Sans" },
  "neon-cyber": { display: "Clash Display", body: "Satoshi" },
  "terminal-green": { display: "JetBrains Mono", body: "JetBrains Mono" },
  "swiss-modern": { display: "Archivo", body: "Nunito" },
  "paper-ink": { display: "Cormorant Garamond", body: "Source Serif 4" },
};

const FontLoader: React.FC<{ stylePreset?: string }> = ({ stylePreset }) => {
  const [handle] = useState(() => delayRender("Loading fonts"));

  useEffect(() => {
    const preset = stylePreset ? PRESET_FONT_MAP[stylePreset] : null;

    if (!preset) {
      continueRender(handle);
      return;
    }

    const families = [preset.display, preset.body].filter(Boolean);
    const uniqueFamilies = Array.from(new Set(families));

    Promise.all(
      uniqueFamilies.map((family) =>
        document.fonts.load(`1em "${family}"`).catch(() => undefined)
      )
    ).finally(() => {
      continueRender(handle);
    });
  }, [handle, stylePreset]);

  return null;
};

const calculateMetadata: CalculateMetadataFunction<Record<string, unknown>> = async ({
  props,
}: { props: Record<string, unknown> }) => {
  const typedProps = props as unknown as VideoProps;
  const platform: PlatformKey = typedProps.platform || "bilibili";
  const preset = PLATFORM_PRESETS[platform];
  const totalFrames = calculateTotalFrames(typedProps.scenes);

  return {
    durationInFrames: totalFrames,
    fps: VIDEO_FPS,
    width: preset.width,
    height: preset.height,
  };
};

export const Root: React.FC = () => {
  const scenes = (projectData as any).scenes || [];
  const platform = (projectData as any).platform || "bilibili";
  const firstPreset = scenes[0]?.stylePreset;

  return (
    <>
      <FontLoader stylePreset={firstPreset} />
      <Composition
        id="SelfMediaVideo"
        component={Video as any}
        durationInFrames={150}
        fps={VIDEO_FPS}
        width={PLATFORM_PRESETS[platform as PlatformKey].width}
        height={PLATFORM_PRESETS[platform as PlatformKey].height}
        defaultProps={{
          scenes,
          platform,
        }}
        calculateMetadata={calculateMetadata}
      />
    </>
  );
};
