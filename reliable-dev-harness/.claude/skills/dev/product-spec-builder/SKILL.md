---
name: product-spec-builder
description: Turn vague product ideas into structured AI-readable specs via adaptive questioning. Use when starting a new product or feature.
intent: >-
  Guide users from fuzzy ideas to decision-ready product specifications through multi-turn discovery. The output is not for humans to read—it's a execution baseline for downstream Skills (design-brief-builder, dev-planner, dev-builder, code-review).
type: interactive
best_for:
  - "Starting a new product or major feature"
  - "Clarifying scope before design or development"
  - "Creating a shared execution baseline for AI agents"
scenarios:
  - "I want to build a novel-writing tool for indie authors"
  - "Help me spec out a team inbox feature for our CRM"
  - "I have an idea but don't know where to start"
estimated_time: "15-25 min"
---

## Purpose

Turn vague product ideas into structured, AI-readable product specifications through adaptive questioning. This is not a human-facing PRD—it's an **execution contract** for all downstream Skills.

Use this when:
- Starting a new product or feature
- Scope feels fuzzy and keeps changing
- You need downstream Agents (designer, developer, reviewer) to align on the same baseline

## Key Concepts

### The Spec as Execution Contract
A good Product-Spec is **machine-readable first, human-readable second**. It must contain:
1. **Problem Statement** — Who is blocked, what are they trying to do, why it matters
2. **Target User** — Specific persona, not "general users"
3. **Core Features** — 3-7 bullet points, each with a user outcome
4. **Success Metrics** — Quantified, time-bound, verifiable
5. **Scope Boundaries** — Explicit In-Scope and Out-of-Scope
6. **Key Decisions** — Product-level tradeoffs already made

### Anti-Patterns (What This Is NOT)
- **Not a marketing deck:** No buzzwords, no "revolutionize the industry"
- **Not an engineering spec:** Don't specify tech stack or database schema here
- **Not endless:** 1-2 pages max. If it's longer, the product is too big.

## Application

### Entry Mode (via workshop-facilitation protocol)
Offer three modes:
1. **Guided** — I ask you 8-12 questions one at a time
2. **Context Dump** — You paste everything you know; I fill gaps only
3. **Best Guess** — I infer from minimal input and label all assumptions

### Question Sequence (Adaptive, max 10 questions)

**Q1: Target User**
"Who is the primary user? Describe their situation and what they're trying to accomplish."

**Q2: Core Problem**
"What is the most painful/frustrating part of their current workflow?"

**Q3: Proposed Solution (1 sentence)**
"If you had to describe the product in one sentence, what does it do?"

**Q4: Core Features**
"List the 3-5 most important capabilities. For each, answer: what user outcome does it enable?"

**Q5: Success Metrics**
"How will you know this product is working? Give at least one number (conversion rate, time saved, retention, etc.)."

**Q6: Scope Boundaries**
"What is explicitly NOT included in the first version?"

**Q7: Platform / Format**
"Web app, mobile app, desktop app, browser extension, CLI, or API?"

**Q8: Key Constraints**
"Any hard constraints? (timeline, budget, regulatory, must-use tech, offline requirement)"

**Q9-Q12:** Adaptive follow-ups based on previous answers.

### Output Format

Write the final spec to `.claude/state/L2-spec.md` using this structure:

```markdown
# Product Spec: {Project Name}

## Problem Statement
{Who} struggles with {what} because {root cause}, leading to {consequence}.

## Target User
- **Primary:** {persona + situation}
- **Secondary (optional):** {persona}

## Core Solution (1 sentence)
{A single sentence description}

## Core Features
1. **{Feature name}** — Enables {user outcome}
2. ...

## Success Metrics
- {Metric 1}: move from {baseline} to {target} within {timeframe}
- ...

## Scope
**In Scope:**
- ...

**Out of Scope (v1):**
- ...

## Key Decisions
- {Tradeoff decision 1}
- ...
```

### After Output
Run `exit-check.py` before claiming completion.

## Examples

### Good: AI Novel Writing Tool
**Problem:** Indie authors waste 40% of their creative energy on formatting, continuity tracking, and scene outlining instead of writing.
**Solution:** A web-based novel editor that auto-tracks character continuity and generates scene outlines from plot beats.
**Scope:** In = editor, continuity checker, outline generator. Out = publishing distribution, collaborative editing, mobile app.
**Metrics:** Author weekly word count increases 25% within 30 days of onboarding.

### Bad: "A platform for writers"
**Why bad:** No specific user, no specific problem, no metrics, no scope boundaries. Every downstream Agent will guess differently.

## Common Pitfalls

### Pitfall 1: Solution-First Thinking
**Symptom:** Spec starts with "We'll build an AI app that..." without describing who needs it and why.

**Fix:** Always lead with Problem Statement. If you can't name the user and their pain, stop here.

### Pitfall 2: Scope Creep in the Spec
**Symptom:** Out of Scope is empty or vague ("maybe later").

**Fix:** Out of Scope must be explicit and uncomfortable. If it hurts to leave something out, you're doing it right.

### Pitfall 3: Metrics Theater
**Symptom:** "Improve user experience" or "Make writers more productive."

**Fix:** Every metric must have a number, a baseline, and a timeframe. "25% increase in weekly word count within 30 days" is a metric. "Better UX" is not.

## References

### Related Skills
- `design-brief-builder` — Consumes this spec to define visual standards
- `dev-planner` — Consumes this spec to plan technical phases
- `code-review` — Uses this spec as the functional acceptance baseline

### External Frameworks
- Jobs-to-be-Done (Clayton Christensen)
- Teresa Torres, *Continuous Discovery Habits*
