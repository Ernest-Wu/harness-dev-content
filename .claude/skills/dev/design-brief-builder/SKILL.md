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

### PM Direction Gate (G1)

This skill produces the input for the **PM Direction Gate**. Before proceeding to design mockups, verify:
- [ ] Design direction aligns with business goals from L2-spec
- [ ] Visual style serves the target user (not just aesthetic preference)
- [ ] Accessibility requirements are specified (WCAG level, contrast ratios)
- [ ] Brand guidelines are referenced or defined

### Positioning Statement Framework (from positioning-statement)

Before choosing visual direction, confirm *what you're positioning for* using Geoffrey Moore's framework:

**Value Proposition:**
- **For** [specific target customer/persona]
- **that need** [underserved need — focus on pains and gains]
- [product name]
- **is a** [product category — anchors buyer perception]
- **that** [benefit statement — outcomes, not features]

**Differentiation Statement:**
- **Unlike** [primary competitor or substitute behavior]
- [product name]
- **provides** [unique differentiation — outcomes, not features]

**Quality checks:**
- Target specificity: Could you describe this person to a recruiter?
- Category fit: Does "is a [category]" help or hurt? Sometimes creating a new category is strategic but risky.
- Differentiation honesty: Could a competitor copy this in 6 months? If yes, it's not durable.
- Outcome framing: Are you saying what users *achieve* differently, not just what you *do* differently?

**Anti-patterns:**
- "For everyone" / "For businesses that want to grow" → Pick the *first* customer segment specifically
- Feature list as benefit statement → Lead with outcome: "Reduces churn by 30%" not "provides AI, analytics, and integrations"
- Imaginary competitor ("Unlike outdated legacy systems") → Name the real alternative buyers consider

### User Story Mapping Framework (from user-story-mapping)

Structure design decisions around **user journey narrative**, not feature lists:

```
Backbone (3-5 activities): User's high-level journey left-to-right
  → Steps (3-5 per activity): Observable actions within each activity
    → Tasks (5-7 per step): Specific work items, prioritized top-to-bottom
        Top rows: MVP (must-have)
        Lower rows: Future releases (nice-to-have)
```

**How this informs design:**
- Backbone activities → main navigation / screen categories
- Steps → page-level layouts / user flows
- MVP tasks → what to design first (P0 screens)
- Future tasks → what to defer (P2 screens)

**Anti-patterns:**
- Activities as features, not user behaviors → "Use dashboard" ✗ → "Monitor project progress" ✓
- Too many activities (10+) → Consolidate to 3-5 high-level activities
- Ignoring vertical prioritization → Explicitly draw release lines for MVP vs. future
- Mapping in isolation → Collaborate with PM and engineering

## Application

Ask adaptive questions to pin down:
1. Primary and accent colors (hex values)
2. Surface hierarchy (how many elevation levels)
3. Corner radius philosophy (sharp, soft, pill)
4. Motion language (instant, fade, bounce)
5. Target platform constraints
6. **Positioning alignment** — Does this visual direction serve the value proposition?
7. **User journey coverage** — Do screens cover all backbone activities?

Output to `.claude/state/L3-design.md`.

## Common Pitfalls

### Pitfall 1: Vague Descriptions
**Fix:** Every color must have a hex code. Every spacing decision must reference a token or number.

### Pitfall 2: Ignoring Accessibility
**Fix:** Specify minimum contrast ratios and focus states.

### Pitfall 3: Aesthetic-Only Decisions
**Fix:** Every visual choice should trace back to a positioning statement or user need. "Dark mode looks cool" is insufficient — "Dark mode reduces eye strain for our target users who work 8+ hours daily" is justified.

### Pitfall 4: Designing Without Journey Context
**Fix:** Map screens to user story map activities. If a screen doesn't serve a backbone activity, question whether it's needed.

## References

- Related skills: design-maker, dev-builder, product-spec-builder
- Framework sources: positioning-statement (Geoffrey Moore), user-story-mapping (Jeff Patton)
