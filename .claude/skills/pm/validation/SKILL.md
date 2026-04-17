---
name: pm/validation
description: Validate product outcomes against spec metrics at 7-day and 30-day checkpoints. Use after release to measure success and decide GO/PIVOT/KILL.
intent: >-
  Ensure that what we shipped actually achieved the business goals defined in L2-spec.
  This is G5 in the PM Gate framework — the final validation loop that closes the feedback cycle.
type: interactive
best_for:
  - "Product validation after launch (7-day and 30-day checkpoints)"
  - "Deciding whether to continue, pivot, or kill a feature"
  - "Closing the loop between spec metrics and real-world outcomes"
scenarios:
  - "It's been 7 days since launch, let's check metrics"
  - "Our activation rate didn't hit target, should we pivot?"
  - "30-day post-launch review"
estimated_time: "20-30 min"
---

## Purpose

Validate that what we built actually delivers the outcomes we promised in the Product Spec. This skill closes the feedback loop:
**Spec → Build → Release → Validate → Decide → (Spec update or Pivot)**

This is **G5: PM Validation Gate** — the moment of truth where data replaces assumptions.

## Key Concepts

### The Validation Loop

Product development is a hypothesis-testing cycle:
1. **Hypothesis** (L2-spec): "We believe building X for persona Y will achieve outcome Z"
2. **Build** (L3→L4): Design and implement
3. **Release** (G4): Ship to users
4. **Validate** (G5): Did Z happen? ← **You are here**
5. **Decide**: GO (continue) / PIVOT (change direction) / KILL (stop)

### Lean UX Validation Experiment (from lean-ux-canvas)

Before validating, confirm the experiment:

| Box | Question | G5 Source |
|-----|----------|-----------|
| Hypothesis | What did we believe would happen? | Epic hypothesis from L4-plan |
| Success Metric | How do we measure success? | Metrics from L2-spec |
| Baseline | What was the starting point? | Pre-launch measurement |
| Target | What number proves success? | Target from L2-spec |
| Timeframe | When do we measure? | 7 days (initial) / 30 days (final) |

### GO / PIVOT / KILL Decision Framework

| Result | Decision | Next Action |
|--------|----------|-------------|
| Metrics meet or exceed targets | **GO** | Continue current plan, scale up |
| Metrics show partial success (50-80% of target) | **PIVOT** | Identify bottleneck, adjust spec or design, re-validate |
| Metrics clearly miss targets (<50% of target) | **KILL** | Stop investment, document learnings, update L2-spec if core hypothesis is wrong |

### Pol-Probe Framework (from pol-probe)

When metrics are ambiguous, use structured probing:

1. **Surface-level**: Are the numbers telling a clear story?
2. **Root cause**: If metrics are off, WHY? (Not just "users didn't use it" — dig deeper)
3. **System-level**: Are there external factors? (Seasonality, market shifts, onboarding bugs)
4. **User-level**: Talk to 5 users who completed the flow and 5 who didn't

## Application

### 7-Day Checkpoint

**Goal:** Early signal detection. Not final judgment.

1. **Read L2-spec.md** — Find the Success Metrics section
2. **Collect data** — Pull analytics for each metric (baseline → current)
3. **Assess each metric:**
   - ✅ On track (≥80% of target trajectory)
   - ⚠️ At risk (50-80% of target trajectory)
   - ❌ Off track (<50% of target trajectory)
4. **Document findings** in `.claude/state/L5-validation.md`

### 30-Day Checkpoint

**Goal:** Final validation and decision.

1. **Read L5-validation.md** — Review 7-day findings
2. **Collect full data** — Pull comprehensive analytics
3. **Evaluate each metric:**
   - ✅ Target met → **GO**
   - ⚠️ Partially met → **PIVOT** (identify what to change)
   - ❌ Target missed → **KILL** or **MAJOR PIVOT**
4. **Make GO/PIVOT/KILL decision** — Document with rationale
5. **Update L2-spec.md** if scope or priorities change
6. **Feed findings into Steering Loop** — If pattern is recurring, propose rule changes

### Output Format

Write to `.claude/state/L5-validation.md`:

```markdown
# Validation Report: {Project Name}

## Checkpoint
- **Type:** 7-day / 30-day
- **Date:** {date}
- **Product Version:** {version}

## Metrics

| Metric | Baseline | Current | Target | Status |
|--------|----------|---------|--------|--------|
| {metric1} | {baseline} | {current} | {target} | ✅/⚠️/❌ |
| ... | ... | ... | ... | ... |

## Decision
**Recommendation:** GO / PIVOT / KILL
**Rationale:** {one paragraph explaining why}

## PIVOT Plan (if applicable)
- **What to change:** {specific adjustment}
- **Hypothesis:** {new hypothesis if pivoting}
- **Next validation date:** {date}

## Learnings
- {Learning 1}
- {Learning 2}

## Spec Updates (if any)
- {Updates to L2-spec based on validation}
```

### After Output
Run `exit-check.py` before claiming completion.

## Common Pitfalls

### Pitfall 1: Metrics Theater
**Symptom:** "We'll know it when we see it" or "Let's check if users are happy"

**Fix:** Every metric must have a number, baseline, and target. "25% increase in weekly active users within 30 days" is a metric. "Users seem engaged" is not.

### Pitfall 2: Survivor Bias
**Symptom:** Only counting users who completed the flow, ignoring drop-offs

**Fix:** Measure conversion at every step, not just the end. A 90% completion rate of 10% start rate = 9% overall, not 90%.

### Pitfall 3: Premature KILL
**Symptom:** Killing a feature after 7 days because numbers are low

**Fix:** 7-day checkpoint is for **signal detection**, not final judgment. Only KILL at 30 days unless data is catastrophically bad.

### Pitfall 4: No Root Cause Analysis
**Symptom:** "Metrics missed target, so the feature failed"

**Fix:** Always ask WHY. Missed targets could be due to onboarding bugs, wrong audience, poor distribution, or genuinely wrong hypothesis — each requires a different response.

### Pitfall 5: Validation Without Spec
**Symptom:** Checking arbitrary metrics that weren't defined upfront

**Fix:** Validation must reference the exact Success Metrics from L2-spec. If L2-spec didn't define clear metrics, that's a G0 failure — the spec was incomplete.

## References

- Related skills: product-spec-builder (produces L2-spec with metrics), release-builder (G4 pre-release gate)
- Upstream: dev/code-review (G3), dev/release-builder (G4)
- Framework sources: lean-ux-canvas, pol-probe (Product-Manager-Skills)
- PM Gate: G5 — PM Validation Gate