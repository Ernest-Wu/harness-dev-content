---
name: pm/content-validation
description: Validate content performance against KPIs at 7-day checkpoint after publishing. Use to measure content effectiveness and decide iterate/refresh/retire.
intent: >-
  Close the content feedback loop by measuring whether content met the KPIs defined 
  in L0-strategy.md. This is CG5 in the PM Gate framework.
type: interactive
best_for:
  - "7-day post-publish content performance review"
  - "Deciding whether to iterate, refresh, or retire content"
  - "Checking if content KPIs from strategy were met"
scenarios:
  - "视频发了7天了，看看数据怎么样"
  - "Check our content performance metrics"
  - "Should we keep making this series?"
estimated_time: "15-20 min"
---

## Purpose

Validate that published content achieved the strategic goals defined in L0-strategy.md. This is **CG5: PM Content Validation Gate** — the content track's feedback closure point.

Without this gate, you keep producing content without knowing what works, wasting resources on formats or topics that don't resonate.

## Key Concepts

### Content Validation Framework

Content validation measures three dimensions:

1. **Reach Metrics** — Did the content get in front of the right audience?
   - Views, impressions, subscriber growth
   - Platform-specific: completion rate (video), scroll depth (article)

2. **Engagement Metrics** — Did the audience interact meaningfully?
   - Likes, comments, shares, saves
   - Engagement rate = (likes + comments + shares) / views

3. **Conversion Metrics** — Did the content drive the intended business action?
   - Click-through rate (CTM links)
   - Lead generation, sign-ups, purchases
   - Attribution from UTM parameters (defined in L6-distribution.md)

### Business Health Diagnostic (from business-health-diagnostic)

For content series, assess overall channel health alongside per-video metrics:

| Health Dimension | Good Signal | Warning Signal | Critical Signal |
|-----------------|-------------|---------------|-----------------|
| Reach | Growing views per video | Flat views | Declining views |
| Engagement | >5% engagement rate | 2-5% rate | <2% rate |
| Conversion | Meeting KPI targets | 50-80% of target | <50% of target |
| Audience Growth | Net positive subscribers | Flat | Net negative |
| Content Cadence | Publishing on schedule | Missed 1 release | Missed 2+ releases |

### Iterate / Refresh / Retire Decision

| Scenario | Decision | Action |
|----------|----------|--------|
| Metrics meet KPI targets | **Iterate** | Continue producing, optimize format |
| Partial success (50-80%) | **Refresh** | Adjust topic, format, or distribution |
| Metrics clearly miss (<50%) | **Retire** | Stop this content type/series |
| Content fatiguing over time | **Refresh** | New angle, format, or audience segment |

### Steering Loop Connection

Validation findings that repeat 5+ times should feed back into the Steering Loop:
- Same content format consistently underperforms → Propose format change
- Same topic type consistently overperforms → Propose topic expansion
- Same platform consistently underperforms → Propose platform shift

## Application

### 7-Day Checkpoint

1. **Read L0-strategy.md** — Find the KPI definitions
2. **Read L6-distribution.md** — Get UTM parameters and platform list
3. **Collect data** — Pull platform analytics for each KPI
4. **Assess each KPI:**
   - ✅ On target (≥80% of goal)
   - ⚠️ At risk (50-80% of goal)
   - ❌ Off target (<50% of goal)
5. **Make Iterate/Refresh/Retire decision**
6. **Document findings** and feed into Steering Loop if patterns emerge

### Output Format

Write to `.claude/state/L5-validation.md` (appended or overwritten):

```markdown
# Content Validation Report: {Content Title}

## Checkpoint
- **Type:** 7-day content validation
- **Date:** {date}
- **Content:** {title / slug}

## KPI Performance

| KPI | Baseline | Current | Target | Status |
|-----|----------|---------|--------|--------|
| {kpi1} | {baseline} | {current} | {target} | ✅/⚠️/❌ |
| ... | ... | ... | ... | ... |

## Platform Breakdown (if multi-platform)

| Platform | Views | Engagement Rate | CTR | Top Performer? |
|----------|-------|-----------------|-----|---------------|
| {platform1} | {n} | {%} | {%} | Yes/No |
| ... | ... | ... | ... | ... |

## Decision
**Recommendation:** ITERATE / REFRESH / RETIRE
**Rationale:** {one paragraph}

## Next Steps (if ITERATE or REFRESH)
- {Specific action 1}
- {Specific action 2}

## Steering Loop Signals (if recurring pattern)
- {Pattern observed}
- {Proposed rule change, if applicable}

## Learnings
- {Learning 1}
- {Learning 2}
```

### After Output
Run `exit-check.py` before claiming completion.

## Common Pitfalls

### Pitfall 1: Vanity Metrics Only
**Symptom:** "We got 10K views!" but no engagement or conversion data

**Fix:** Views without engagement = reach without impact. Always pair reach metrics with engagement and conversion.

### Pitfall 2: No Baseline Comparison
**Symptom:** "Engagement rate is 3%" without knowing if that's good or bad

**Fix:** Every KPI needs a baseline and target from L0-strategy.md. "3% engagement vs. 2% baseline toward 5% target" is actionable. Just "3%" is not.

### Pitfall 3: Ignoring Platform Differences
**Symptom:** Averaging metrics across platforms

**Fix:** Different platforms have different norms. 2% engagement on YouTube might be great, while 5% on Xiaohongshu might be below average. Assess per-platform.

### Pitfall 4: No Steering Loop Feedback
**Symptom:** Same content format underperforms 5+ times with no rule change

**Fix:** When the same pattern occurs 5+ times, propose a Steering Loop rule change. The harness adjusts when feedback shows systemic issues.

### Pitfall 5: Premature RETIRE
**Symptom:** Killing content after 7 days because numbers are low

**Fix:** 7 days is a signal checkpoint, not a final verdict. Consider algorithm learning period, audience building, and platform-specific growth curves before retiring.

## References

- Related skills: pm/content-strategy (CG0 — defines KPIs), pm/distribution-planner (CG4 — defines tracking)
- Upstream: L0-strategy.md (KPIs), L6-distribution.md (UTM tracking)
- PM Gate: CG5 — PM Content Validation Gate
- Framework sources: business-health-diagnostic (Product-Manager-Skills)