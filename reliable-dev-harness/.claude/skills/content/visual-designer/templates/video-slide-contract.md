# Video-First Slide Design Contract

This document defines the rules for converting `frontend-slides` presentations into time-driven video slides.

## Core Rule: Time-Driven, Not Click-Driven

Every visual change must be triggered by the passage of time (`--scene-time`), NOT by scroll position, hover, or keyboard events.

## Mandatory Attributes

Any element that animates within a scene MUST have:

```html
<div data-beat-at="2.5" data-beat-type="number-pop">52.8%</div>
```

- `data-beat-at`: time in seconds (relative to scene start)
- `data-beat-type`: one of `hook-reveal`, `keyword-highlight`, `number-pop`, `quote-reveal`, `split-contrast`

## Allowed Animations

Only GPU-safe properties:
- `transform` (scale, translate, rotate)
- `opacity`

**Forbidden:**
- `width`, `height`, `top`, `left` (causes layout thrashing)
- CSS `@keyframes` with complex keyframe curves (prefer transition + class toggle)
- Hover effects
- Scroll-triggered effects (`IntersectionObserver` is only allowed for initial `.visible` on scene enter)

## HTML Structure Template

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>...</title>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=...">
  <style>
    /* === VIEWPORT BASE (full viewport-base.css) === */
    /* === PLATFORM OVERRIDE (inject AFTER viewport-base) === */
    /* === THEME VARIABLES === */
    /* === BEAT ANIMATIONS === */
    /* === SLIDE STYLES === */
  </style>
</head>
<body>
  <section class="slide" id="scene-01" data-scene-duration="12.5">
    <!-- Content with data-beat-at attributes -->
  </section>
  <!-- more sections... -->
  <script>
    // Optional: sync any JS-driven effects to --scene-time
  </script>
</body>
</html>
```

## Platform Override Injection Rule

After pasting the full `viewport-base.css`, immediately append the correct platform override:
- `platform-9-16.css` for `douyin`, `instagram`
- `platform-4-5.css` for `xiaohongshu`
- none needed for `bilibili`, `youtube`, `weibo`

## Per-Slide Creative Freedom

Each scene MUST have a distinct layout. Do NOT copy-paste the same DOM structure across scenes. The layout should be driven by:
1. The scene's `text` content
2. The scene's `imageUrl` (if present)
3. The scene's `visualBeats` (timed reveals)
