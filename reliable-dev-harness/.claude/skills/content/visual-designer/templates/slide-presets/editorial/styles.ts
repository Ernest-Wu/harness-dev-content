import { StyleSheet } from "remotion";

export const editorialStyles = StyleSheet.create({
  container: {
    backgroundColor: "#FAFAF8",
    flex: 1,
    justifyContent: "flex-start",
    alignItems: "flex-start",
    paddingTop: 80,
    paddingBottom: 80,
    paddingLeft: 48,
    paddingRight: 48,
    borderLeftWidth: 4,
    borderLeftColor: "#0066CC",
  },
  title: {
    fontFamily: "Source Han Sans SC, Noto Sans SC, sans-serif",
    fontSize: 72,
    fontWeight: 600,
    color: "#1A1A1A",
    textAlign: "left",
    lineHeight: 1.3,
    marginBottom: 32,
  },
  body: {
    fontFamily: "Source Han Sans SC, Noto Sans SC, sans-serif",
    fontSize: 42,
    fontWeight: 400,
    color: "#1A1A1A",
    textAlign: "left",
    lineHeight: 1.8,
  },
  secondary: {
    fontFamily: "Source Han Sans SC, Noto Sans SC, sans-serif",
    fontSize: 28,
    fontWeight: 400,
    color: "#666666",
    textAlign: "left",
    lineHeight: 1.6,
  },
  accent: {
    color: "#0066CC",
  },
  gridLine: {
    position: "absolute",
    left: 48,
    top: 0,
    bottom: 0,
    width: 1,
    backgroundColor: "#E0E0E0",
  },
});

export const EDITORIAL_CONFIG = {
  background: "#FAFAF8",
  primaryText: "#1A1A1A",
  secondaryText: "#666666",
  accent: "#0066CC",
  fontFamily: "Source Han Sans SC",
  titleSize: 72,
  bodySize: 42,
  lineHeight: 1.8,
  aspectRatio: "9:16",
  safeArea: { top: 80, bottom: 80, left: 48, right: 48 },
  borderLeft: true,
};
