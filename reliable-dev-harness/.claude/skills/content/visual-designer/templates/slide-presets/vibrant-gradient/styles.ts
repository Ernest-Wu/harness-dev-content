import { StyleSheet } from "remotion";

export const vibrantGradientStyles = StyleSheet.create({
  container: {
    backgroundColor: "#6366F1",
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    paddingTop: 120,
    paddingBottom: 120,
    paddingLeft: 50,
    paddingRight: 50,
  },
  title: {
    fontFamily: "Noto Sans SC, sans-serif",
    fontSize: 76,
    fontWeight: 700,
    color: "#FFFFFF",
    textAlign: "center",
    lineHeight: 1.3,
    marginBottom: 36,
  },
  body: {
    fontFamily: "Noto Sans SC, sans-serif",
    fontSize: 44,
    fontWeight: 500,
    color: "#FFFFFF",
    textAlign: "center",
    lineHeight: 1.7,
  },
  secondary: {
    fontFamily: "Noto Sans SC, sans-serif",
    fontSize: 36,
    fontWeight: 400,
    color: "#F0F0FF",
    textAlign: "center",
    lineHeight: 1.7,
  },
  accent: {
    color: "#FBBF24",
    fontWeight: 600,
  },
});

export const VIBRANT_GRADIENT_CONFIG = {
  backgroundGradient: { start: "#6366F1", end: "#8B5CF6" },
  primaryText: "#FFFFFF",
  secondaryText: "#F0F0FF",
  accent: "#FBBF24",
  fontFamily: "Noto Sans SC",
  titleSize: 76,
  bodySize: 44,
  lineHeight: 1.7,
  aspectRatio: "9:16",
  safeArea: { top: 120, bottom: 120, left: 50, right: 50 },
};