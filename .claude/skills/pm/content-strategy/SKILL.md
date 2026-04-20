---
name: pm/content-strategy
description: Define content strategy before production — target audience, business goals, KPIs, and differentiation. Use before script-writer to establish CG0 gate.
intent: >-
  Ensure every piece of content starts with clear strategic intent: who it's for, 
  why we're making it, and how we measure success. This is CG0 in the PM Gate framework.
type: interactive
best_for:
  - "Starting a new content production cycle"
  - "Defining audience, goals, and KPIs before creating content"
  - "Ensuring content aligns with business objectives"
scenarios:
  - "I want to make a short video about AI trends"
  - "帮我把这个口播稿做成短视频"
  - "我们需要一个新的内容系列"
estimated_time: "10-15 min"
---

## Purpose

Define the strategic foundation for content production BEFORE any creative work begins. This is **CG0: PM Content Strategy Gate** — the first gate in the content track.

Without this gate, content teams produce videos that look great but serve no strategic purpose.

## Key Concepts

### Content Strategy Compass

Every content piece starts with 6 strategic decisions:

1. **Target Audience** — Who is this for? (Age, interests, pain points)
2. **Business Goal** — Why are we making this? (Brand awareness / Lead generation / Conversion / Education)
3. **KPI Definition** — How do we measure success? (Views / Completion rate / Engagement rate / Conversion rate)
4. **Core Message Priority** — What is the ONE thing the audience should remember?
5. **Differentiation Strategy** — How does this stand out from similar content?
6. **Compliance Requirements** — Any legal or ethical constraints?

### Discovery Interview Framework (from discovery-interview-prep)

Before defining strategy, gather input through structured discovery:

- **Audience discovery:** Who are they? What platforms do they use? What content do they already consume?
- **Goal alignment:** What business objective does this content serve? Is it top-of-funnel, mid-funnel, or bottom-of-funnel?
- **Competitive scan:** What similar content exists? How do we differentiate?
- **Resource check:** What production capacity do we have? What's the realistic output cadence?

### Positioning Workshop Framework (from positioning-workshop)

For content series (not single videos), run a mini positioning exercise:

**Content Positioning Statement:**
- **For** [target audience segment]
- **that need** [content need — entertainment, education, inspiration]
- **this content series**
- **is a** [content category — tutorial series, documentary, daily brief]
- **that** [unique value — what they get that they can't get elsewhere]
- **Unlike** [competing content / existing alternatives]
- **this series provides** [differentiation — unique angle, format, expertise]

## Application

### Entry Mode (via workshop-facilitation protocol)
Offer three modes:
1. **Guided** — I ask you 6 strategic questions one at a time
2. **Context Dump** — You paste your topic/audience/goals; I fill gaps
3. **Best Guess** — I infer strategy from minimal input and label all assumptions

### Questions

**Q1: Target Audience**
"Who is the primary audience for this content? Describe their age, interests, and pain points."

**Q2: Business Goal**
"What business objective does this content serve? (Brand awareness / Lead generation / Conversion / Education / Community)"

**Q3: Success Metrics**
"How will you measure success? Give at least one number (target views, completion rate, engagement rate, or conversion rate)."

**Q4: Core Message**
"If the audience remembers ONE thing from this content, what should it be?"

**Q5: Differentiation**
"What makes this content different from what already exists on this topic?"

**Q6: Compliance**
"Any legal, ethical, or platform-specific requirements? (Ad disclosures, content ratings, copyright)"

### Output Format

Write to `.claude/state/L0-strategy.md`:

```markdown
# Content Strategy: {Content Title/Topic}

## Target Audience
- **Primary:** {persona description — age, interests, pain points}
- **Secondary (optional):** {persona}

## Business Goal
{Brand awareness / Lead generation / Conversion / Education / Community}

## KPI
- {KPI 1}: move from {baseline} to {target} within {timeframe}
- {KPI 2}: ...

## Core Message Priority
1. {THE one thing audience should remember}
2. {Supporting point 1}
3. {Supporting point 2}

## Differentiation Strategy
- **Unique angle:** {what makes this different}
- **Format advantage:** {how the format serves the message}
- **Expertise lever:** {what expertise or access we bring}

## Compliance Requirements
- {requirement 1}
- {requirement 2}

## Assumptions
- {assumption 1}: {validation status}
```

### After Output
Run `exit-check.py` before claiming completion.

Then proceed to `content/script-writer` (CG1).

## Common Pitfalls

### Pitfall 1: "Make a video about X" Without Strategy
**Symptom:** "I want to make a video about machine learning"

**Fix:** Strategy first. "For junior developers who need practical ML skills, a weekly tutorial series that cuts through theory and shows real implementations — unlike academic courses that take 40 hours before you write code."

### Pitfall 2: Vanity Metrics
**Symptom:** "Our goal is to get 1 million views"

**Fix:** Views without engagement = vanity. Pair views with completion rate and conversion to ensure the right people watch AND act.

### Pitfall 3: No Differentiation
**Symptom:** "There's nothing like this out there" — usually false

**Fix:** Search the topic on the target platform first. If similar content exists, define how yours is different (deeper expertise, unique format, better storytelling, exclusive access).

### Pitfall 4: Audience Too Broad
**Symptom:** "Our audience is anyone interested in tech"

**Fix:** Narrow to a specific segment first. "Junior developers with 1-3 years of experience who want to transition to ML" is actionable. "Anyone interested in tech" is not.

### Pitfall 5: Skipping Compliance
**Symptom:** "Just make it fun, we'll figure out legal later"

**Fix:** Ad disclosures, content ratings, and copyright must be resolved BEFORE production starts. Retroactive compliance is expensive and sometimes impossible.

## References

- Related skills: content/script-writer (CG1), pm/content-validation (CG5)
- Downstream: L0-strategy.md feeds into L2-content-spec.md
- PM Gate: CG0 — PM Content Strategy Gate
- Framework sources: discovery-interview-prep, positioning-workshop (Product-Manager-Skills)