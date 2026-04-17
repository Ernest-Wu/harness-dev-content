import { StyleSheet } from "remotion";

export const cinematicDarkStyles = StyleSheet.create({
  container: {
    backgroundColor: "#0D0D0D",
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    paddingTop: 120,
    paddingBottom: 120,
    paddingLeft: 60,
    paddingRight: 60,
    position: "relative",
  },
  vignette: {
    position: "absolute",
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    background: "radial-gradient(ellipse at center, transparent 40%, rgba(0,0,0,0.7) 100%)",
    pointerEvents: "none",
  },
  title: {
    fontFamily: "Noto Sans SC, sans-serif",
    fontSize: 80,
    fontWeight: 700,
    color: "#F5F5F5",
    textAlign: "center",
    lineHeight: 1.2,
    marginBottom: 40,
    letterSpacing: 2,
  },
  body: {
    fontFamily: "Noto Sans SC, sans-serif",
    fontSize: 44,
    fontWeight: 400,
    color: "#F5F5F5",
    textAlign: "center",
    lineHeight: 1.7,
  },
  secondary: {
    fontFamily: "Noto Sans SC, sans-serif",
    fontSize: 32,
    fontWeight: 300,
    color: "#8A8A8A",
    textAlign: "center",
    lineHeight: 1.6,
  },
  accent: {
    color: "#E50914",
  },
});

export const CINEMATIC_DARK_CONFIG = {
  background: "#0D0D0D",
  primaryText: "#F5F5F5",
  secondaryText: "#8A8A8A",
  accent: "#E50914",
  fontFamily: "Noto Sans SC",
  titleSize: 80,
  bodySize: 44,
  lineHeight: 1.7,
  letterSpacing: 2,
  aspectRatio: "9:16",
  safeArea: { top: 120, bottom: 120, left: 60, right: 60 },
  vignette: true,
};
