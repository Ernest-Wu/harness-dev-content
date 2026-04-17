import { StyleSheet } from "remotion";

export const boldHighContrastStyles = StyleSheet.create({
  container: {
    backgroundColor: "#1A1A1A",
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    paddingTop: 80,
    paddingBottom: 80,
    paddingLeft: 50,
    paddingRight: 50,
  },
  title: {
    fontFamily: "Noto Sans SC, sans-serif",
    fontSize: 88,
    fontWeight: 900,
    color: "#FFFFFF",
    textAlign: "center",
    lineHeight: 1.2,
    marginBottom: 40,
    letterSpacing: -2,
  },
  body: {
    fontFamily: "Noto Sans SC, sans-serif",
    fontSize: 52,
    fontWeight: 600,
    color: "#FFFFFF",
    textAlign: "center",
    lineHeight: 1.5,
  },
  secondary: {
    fontFamily: "Noto Sans SC, sans-serif",
    fontSize: 40,
    fontWeight: 500,
    color: "#B0B0B0",
    textAlign: "center",
    lineHeight: 1.5,
  },
  accent: {
    color: "#FF6B35",
    fontWeight: 700,
  },
});

export const BOLD_HIGH_CONTRAST_CONFIG = {
  background: "#1A1A1A",
  primaryText: "#FFFFFF",
  secondaryText: "#B0B0B0",
  accent: "#FF6B35",
  fontFamily: "Noto Sans SC",
  titleSize: 88,
  bodySize: 52,
  lineHeight: 1.5,
  titleWeight: 900,
  bodyWeight: 600,
  aspectRatio: "9:16",
  safeArea: { top: 80, bottom: 80, left: 50, right: 50 },
};