---
name: design-brief-builder
description: Quantify visual direction into a design brief with colors, structure, and interaction style. Use before creating mockups.
intent: Turn fuzzy visual directions like dark theme or minimal style into concrete, measurable design standards that developers and design tools can align on.
type: interactive
---

## Purpose

Turn fuzzy visual directions into a concrete Design Brief. This prevents the common problem where AI generates ten different interpretations of minimal style.

## Key Concepts

- Color palette with exact hex values
- Typography scale and hierarchy
- Spacing system and grid
- Interaction style (flat, skeuomorphic, glassmorphism)
- Motion level (none, subtle, expressive)

## Application

Ask adaptive questions to pin down:
1. Primary and accent colors (hex values)
2. Surface hierarchy (how many elevation levels)
3. Corner radius philosophy (sharp, soft, pill)
4. Motion language (instant, fade, bounce)
5. Target platform constraints

Output to `.claude/state/L3-design.md`.

## Common Pitfalls

### Pitfall 1: Vague Descriptions
**Fix:** Every color must have a hex code. Every spacing decision must reference a token or number.

### Pitfall 2: Ignoring Accessibility
**Fix:** Specify minimum contrast ratios and focus states.

## References

- Related skills: design-maker, dev-builder
