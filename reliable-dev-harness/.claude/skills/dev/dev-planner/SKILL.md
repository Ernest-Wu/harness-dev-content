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

## Application

1. Read L2-spec.md and L3-design.md
2. Research available libraries, APIs, or components
3. Define 3-7 Phases, each with:
   - Phase name
   - Deliverable
   - Dependencies
   - Estimated Tasks
4. Write to `.claude/state/L4-plan.md`

## Common Pitfalls

### Pitfall 1: Phases That Are Too Big
**Fix:** A Phase should be completable in one or a few sessions.

### Pitfall 2: Ignoring Dependencies
**Fix:** Explicitly state what must be done first.

## References

- Related skills: product-spec-builder, design-brief-builder, dev-builder
