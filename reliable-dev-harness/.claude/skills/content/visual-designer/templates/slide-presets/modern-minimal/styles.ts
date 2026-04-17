import { StyleSheet } from "remotion";

export const modernMinimalStyles = StyleSheet.create({
  container: {
    backgroundColor: "#0A0A0A",
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    paddingTop: 100,
    paddingBottom: 100,
    paddingLeft: 60,
    paddingRight: 60,
  },
  title: {
    fontFamily: "Noto Sans SC, sans-serif",
    fontSize: 72,
    fontWeight: 700,
    color: "#FFFFFF",
    textAlign: "center",
    lineHeight: 1.2,
    marginBottom: 32,
  },
  body: {
    fontFamily: "Noto Sans SC, sans-serif",
    fontSize: 48,
    fontWeight: 400,
    color: "#FFFFFF",
    textAlign: "center",
    lineHeight: 1.6,
  },
  secondary: {
    fontFamily: "Noto Sans SC, sans-serif",
    fontSize: 36,
    fontWeight: 300,
    color: "#A0A0A0",
    textAlign: "center",
    lineHeight: 1.6,
  },
  accent: {
    color: "#6366F1",
  },
});

export const MODERN_MINIMAL_CONFIG = {
  background: "#0A0A0A",
  primaryText: "#FFFFFF",
  secondaryText: "#A0A0A0",
  accent: "#6366F1",
  fontFamily: "Noto Sans SC",
  titleSize: 72,
  bodySize: 48,
  lineHeight: 1.6,
  aspectRatio: "9:16",
  safeArea: { top: 100, bottom: 100, left: 60, right: 60 },
};