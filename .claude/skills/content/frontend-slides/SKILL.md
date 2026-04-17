---
name: frontend-slides
description: Generate visually stunning HTML slides with Mood Selection, 3 Style Previews, and free-form layout. Called by visual-designer as the HTML execution layer.
intent: Provide the visual design execution capability for content production — transform slide data into polished HTML presentations with mood-driven styling, multiple style previews for user selection, and responsive layouts optimized for video output.
type: interactive
---

## Purpose

Generate HTML slide presentations with professional visual design quality. This skill is the **execution layer** called by `visual-designer` (the orchestrator). visual-designer handles video-specific logic (scene mapping, platform CSS, beat attributes), while frontend-slides handles pure visual design.

## Key Concepts

### Mood Selection
Before generating slides, present the user with mood options that set the overall visual direction:
- **Energetic**: Bold colors, dynamic layouts, strong contrast
- **Calm**: Soft palettes, generous whitespace, gentle transitions
- **Professional**: Clean lines, muted tones, structured grids
- **Playful**: Bright accents, asymmetric layouts, rounded elements

### 3 Style Previews
After mood selection, generate exactly 3 distinct style previews for the user to choose from:
1. Each preview must be a complete HTML page with different visual treatment
2. Previews must differ in: color palette, typography, layout density
3. User selects one style — this becomes the final design direction

### Slide Data Format
Input is a JSON structure from visual-designer containing:
- `slides`: Array of slide objects with `title`, `content`, `notes`
- `platform`: Target aspect ratio (9:16, 16:9, or 4:5)
- `mood`: Selected mood direction
- `style`: Selected style name (after user choice)

### Anti-Patterns
- ❌ Do not add video-specific attributes (data-beat-at, platform CSS) — that is visual-designer's job
- ❌ Do not modify slide content or structure — only apply visual styling
- ❌ Do not skip the Mood Selection + Style Preview flow — user must choose
- ❌ Do not generate slides without scenes.json input

## Application

### Step 1: Receive Slide Data from visual-designer

Read the slide data provided by visual-designer (transformed from scenes.json):
- Slide titles and content
- Platform target (9:16, 16:9, 4:5)
- Any image references

### Step 2: Mood Selection (Creative Gate)

Present mood options to the user:
1. Show 4 mood directions with brief descriptions
2. Wait for user selection
3. Record selected mood to `state/L3-design.md`

### Step 3: Generate 3 Style Previews (Creative Gate)

Based on the selected mood, generate 3 distinct style previews:
1. Each preview is a complete HTML page showing 2-3 sample slides
2. Previews must differ in: color palette, font pairing, layout density, visual weight
3. Wait for user to select one style
4. Record selected style to `state/L3-design.md`

### Step 4: Generate Full HTML Slides

Using the selected mood and style:
1. Apply the chosen style to all slides
2. Generate responsive HTML with proper typography and spacing
3. Ensure text readability at video resolution
4. Include proper CSS for the target platform aspect ratio
5. Output: `slides-preview.html`

### Step 5: Hard Gate — Run exit-check.py

```bash
python3 .claude/skills/content/frontend-slides/exit-check.py
```

Exit code ≠ 0 means the output does not meet quality standards. Fix before returning to visual-designer.

## Examples

### ✅ Good Style Preview Structure

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Style Preview A — Energetic</title>
  <style>
    :root { --primary: #FF6B35; --bg: #1A1A2E; --text: #EAEAEA; }
    /* ... full styling ... */
  </style>
</head>
<body>
  <section class="slide">
    <h2>为什么短视频没人看？</h2>
    <p>3个你没想到的原因</p>
  </section>
</body>
</html>
```

### ❌ Bad Practice — Skipping Mood/Style Selection

Directly generating slides without user input violates the Creative Gate requirement. The user must participate in visual direction decisions.

## Common Pitfalls

1. **Skipping Mood Selection**: Generating slides without user input on visual direction. Always present mood options first.
2. **Skipping Style Preview**: Only showing one style. Must present exactly 3 distinct options.
3. **Adding video attributes**: Do not add `data-beat-at` or platform CSS — visual-designer handles post-processing.
4. **Poor readability**: Text too small or low contrast for video. Always test at target resolution.
5. **Inconsistent styling**: Slides within the same presentation must share consistent typography, spacing, and color usage.

## Exit-Check Criteria

Run `exit-check.py` to verify:
1. `slides-preview.html` exists and is valid HTML
2. HTML contains proper slide structure (sections with content)
3. HTML includes CSS styling (not bare/unstyled content)
4. All referenced images exist
5. `state/L3-design.md` contains Mood and Style selection records

## References

- Caller Skill: `content/visual-designer` (orchestrator)
- Downstream: visual-designer post-processes the output (adds data-beat-at, platform CSS)
- State files: `.claude/state/L3-design.md`