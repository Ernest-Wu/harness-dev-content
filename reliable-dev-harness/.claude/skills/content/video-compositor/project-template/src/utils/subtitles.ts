/**
 * Subtitle utilities for self-media-video
 * Generates TikTok-style caption data from scene text and audio duration.
 */

import type { SubtitleLine } from "../types";

/**
 * Split Chinese text into sentences by common punctuation.
 */
export function splitIntoSentences(text: string): string[] {
  // Split by Chinese and English sentence terminators, keeping delimiters
  const parts = text.split(/([。！？.!?；;])/);
  const sentences: string[] = [];
  let current = "";

  for (let i = 0; i < parts.length; i++) {
    current += parts[i];
    if (/[。！？.!?；;]$/.test(parts[i]) && current.trim()) {
      sentences.push(current.trim());
      current = "";
    }
  }

  if (current.trim()) {
    sentences.push(current.trim());
  }

  return sentences.filter((s) => s.length > 0);
}

/**
 * Generate subtitle lines distributed evenly across audioDuration (in seconds).
 */
export function generateSubtitles(text: string, audioDuration: number): SubtitleLine[] {
  const sentences = splitIntoSentences(text);
  if (sentences.length === 0) return [];

  const totalMs = audioDuration * 1000;
  const avgDuration = totalMs / sentences.length;

  // Ensure each subtitle gets at least 800ms to be readable
  const minDuration = 800;
  const effectiveDuration = Math.max(avgDuration, minDuration);

  const subtitles: SubtitleLine[] = [];
  let currentMs = 0;

  for (let i = 0; i < sentences.length; i++) {
    const sentence = sentences[i];
    const endMs = Math.min(currentMs + effectiveDuration, totalMs);

    subtitles.push({
      text: sentence,
      startMs: Math.round(currentMs),
      endMs: Math.round(endMs),
    });

    currentMs = endMs;
    if (currentMs >= totalMs) break;
  }

  // Adjust last subtitle to end exactly at audio end
  if (subtitles.length > 0) {
    subtitles[subtitles.length - 1].endMs = Math.round(totalMs);
  }

  return subtitles;
}

/**
 * Export subtitles to a Caption-compatible JSON format for Remotion.
 */
export function exportRemotionCaptions(subtitles: SubtitleLine[]) {
  return subtitles.map((sub) => ({
    text: sub.text,
    startMs: sub.startMs,
    endMs: sub.endMs,
    timestampMs: sub.startMs,
    confidence: 1,
    tokens: sub.text.split("").map((char, i) => {
      const charDuration = (sub.endMs - sub.startMs) / sub.text.length;
      return {
        text: char,
        fromMs: sub.startMs + i * charDuration,
        toMs: sub.startMs + (i + 1) * charDuration,
      };
    }),
  }));
}
