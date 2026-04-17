---
name: design-maker
description: Generate design deliverables from spec and design brief. Use when you need mockups, wireframes, or structured design data before development.
intent: Translate Product Spec and Design Brief into concrete design deliverables that serve as the highest authority for downstream development. Outputs can be structured JSON for code generation, Figma files via API, or Pencil-compatible wireframes.
type: interactive
---

## Purpose

Generate concrete design deliverables from the Product Spec and Design Brief. This is the highest authority for all downstream UI development.

Without this step, dev-builder will guess colors, spacing, and layout from pretraining data. The result is usually inconsistent and ugly.

## Key Concepts

### Design Deliverable Types
1. Structured Design JSON - Machine-readable page/component structure with exact tokens
2. Figma File (via API) - Created through Figma REST API using figma-export.py
3. Pencil Wireframe (.epz) - Lightweight mockup for rapid iteration

### Visual Authority Chain
Design deliverable > Design-Brief.md > Product-Spec.md

When UI conflicts arise, the design deliverable wins.

### Anti-Patterns (What This Is NOT)
- Not a vague description - modern and clean is not a design deliverable
- Not a requirements document - do not describe what the UI should do; show what it looks like
- Not optional - skipping this step guarantees UI inconsistency

## Application

### Before You Start
Read:
1. .claude/state/L2-spec.md - what features need screens
2. .claude/state/L3-design.md - colors, spacing, typography tokens
3. List of pages/components required from spec

### Step 1: Identify Required Screens/Components
From the spec, extract every UI surface that needs a design:
- Pages (full screens)
- Components (reusable elements: nav, forms, cards)
- States (empty, loading, error, success)

### Step 2: Generate Structured Design Data
For each screen/component, produce a structured description in YAML format.

### Step 3: Export to Target Format

#### Option A: Figma (requires FIGMA_TOKEN env var)
```bash
python3 .claude/skills/design-maker/scripts/figma-export.py --input design-output.yaml --name "MyApp v1"
```
This creates a new Figma file and returns the URL.

#### Option B: Pencil Wireframe
```bash
python3 .claude/skills/design-maker/scripts/pencil-export.py --input design-output.yaml --output mockup.epz
```

#### Option C: Structured JSON Only
Save design-output.yaml to .claude/state/L5-design-data.yaml.

### Step 4: Record Design Authority
Write the final design file reference to .claude/state/L5-design-data.yaml.

### Step 5: Run Exit Check
```bash
python3 .claude/skills/design-maker/exit-check.py
```

## Examples

### Good: Login Page Design
A structured YAML with exact positions, colors, and typography.

### Bad: A simple login screen with a form
No positions. No colors. No sizes. Every developer will interpret this differently.

## Common Pitfalls

### Pitfall 1: Designing Only the Happy Path
Fix - For every screen, design error states, empty states, and loading states.

### Pitfall 2: Design Data Out of Sync with Spec
Fix - Cross-check every element against the spec In-Scope list.

### Pitfall 3: Vague Measurements
Fix - Every spacing value must be an exact number from the Design Brief.

## References

### Related Skills
- design-brief-builder - Provides design tokens
- product-spec-builder - Defines screens needed
- dev-builder - Consumes design data
- code-review - Verifies UI code against this deliverable

### External Tools
- Figma REST API
- Pencil (Evolus) open-source wireframing tool
