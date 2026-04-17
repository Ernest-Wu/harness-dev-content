---
name: dev-planner
description: Research tech stack and split the project into Phases with clear deliverables. Use after spec and design are ready.
intent: Create a structured DEV-PLAN that breaks a project into executable Phases. This file serves as the anchor for cross-session development continuity.
type: interactive
---

## Purpose

Create a structured DEV-PLAN that breaks the project into executable Phases. This is the cross-session anchor.

## Key Concepts

- Phase = a coherent milestone with a clear deliverable
- Dependency graph = what must be done before what
- Tech research = what components or libraries can be reused
- Risk flag = which Phase is most likely to fail

### PM Scope Gate (G2)

This skill produces the input for the **PM Scope Gate**. Before proceeding to implementation, verify:
- [ ] Phase mapping aligns with business priority (P0 → MVP first)
- [ ] Business goal from L2-spec is present in each Phase's objective
- [ ] Each Phase has clear success metrics linked to spec
- [ ] Risk flags are identified and mitigation strategies exist
- [ ] MVP boundary is explicitly defined vs. future phases

### Roadmap Planning Framework (from roadmap-planning)

Structure phases using **strategic roadmap types** based on project context:

| Roadmap Type | When to Use | Structure |
|-------------|-------------|-----------|
| Now/Next/Later | Agile teams, high uncertainty | Current quarter (committed) → Next (high confidence) → Later (exploration) |
| Theme-Based | Communicating to execs/stakeholders | Organize by strategic themes (Retention, Expansion, etc.) |
| Timeline (Quarters) | Resource planning, stakeholder comm | Q1: Epics A,B → Q2: Epics C,D → Q3: Epics E,F |

**Key principles:**
- Roadmaps are strategic plans, not commitments — they evolve with learning
- Tie every phase/epic to a business outcome (not just "build feature X")
- Reassess when product stage changes, team reorganizes, or the framework feels broken

**Anti-patterns:**
- Feature-based roadmap (lists features without context) → Use outcome-driven or theme-based
- Roadmap as contract → Roadmaps state intent, not promises
- Never reassess → Revisit quarterly or when stage changes

### Epic Hypothesis Framework (from epic-hypothesis)

Each Phase should be expressed as a **testable hypothesis**, not a feature list:

```
We believe that [building X] for [persona Y]
will achieve [outcome Z]
because [assumption W].
```

**Required fields per Phase:**
- **Hypothesis:** The testable belief statement above
- **Success Metric:** Quantified, time-bound measure
- **Target:** Baseline → Goal (e.g., "Activation 40% → 60%")
- **Effort Estimate:** T-shirt sizing (S/M/L/XL)
- **Business Outcome Mapping:** Which OKR/goal does this Phase serve?

**Anti-patterns:**
- Feature without hypothesis → "Build onboarding" is a feature; "Adding step-by-step onboarding for new users will increase activation from 40% to 60%" is a hypothesis
- Metric without baseline → "Improve activation" ✗ → "Activation 40% → 60%" ✓
- Epic too large → If effort is XL, decompose into smaller hypotheses

### Lean UX Canvas (from lean-ux-canvas)

Validate Phase hypotheses before committing resources using the 7-box canvas:

| Box | Question | Connects To |
|-----|----------|-------------|
| 1. Business Problem | What problem are we solving? | L2-spec Problem Statement |
| 2. Business Outcome | How do we know we've succeeded? | Success Metrics in L2-spec |
| 3. Users | Who are the users? | Proto-persona from spec |
| 4. User Benefit | What do users get? | L2-spec Core Features |
| 5. Hypothesis | What we believe will happen? | Epic hypothesis per Phase |
| 6. Experiment | What's the smallest thing we can do to test? | MVP scope definition |
| 7. Learnings | What did we learn? | Feeds back into next Phase |

**How to use in planning:**
- Fill boxes 1-5 from L2-spec content
- Box 6 determines MVP scope for each Phase
- Box 7 is filled post-release (feeds G5 Validation Gate)

## Application

1. Read L2-spec.md and L3-design.md
2. Research available libraries, APIs, or components
3. Define 3-7 Phases, each with:
   - Phase name
   - **Epic hypothesis** (testable belief statement)
   - Deliverable
   - Dependencies
   - **Success metric** (quantified, time-bound)
   - **Risk flag**
   - Estimated Tasks
4. **Map each Phase to business outcome** from L2-spec
5. **Define MVP boundary** explicitly (P0 items in Phase 1)
6. Write to `.claude/state/L4-plan.md`

## Common Pitfalls

### Pitfall 1: Phases That Are Too Big
**Fix:** A Phase should be completable in one or a few sessions. If it feels like XL, decompose.

### Pitfall 2: Ignoring Dependencies
**Fix:** Explicitly state what must be done first. Use dependency graph.

### Pitfall 3: Feature Lists Instead of Hypotheses
**Fix:** Every Phase should pass the "We believe that...will achieve...because..." test. If it's just "build feature X," you don't know if it's worth building.

### Pitfall 4: No Business Outcome Mapping
**Fix:** Each Phase must trace back to a business goal in L2-spec. If you can't answer "why does this matter to the business?", the Phase doesn't belong in the plan.

## References

- Related skills: product-spec-builder, design-brief-builder, dev-builder, code-review
- Framework sources: roadmap-planning, epic-hypothesis, lean-ux-canvas (Product-Manager-Skills)
