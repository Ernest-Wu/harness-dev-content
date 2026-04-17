---
name: pm/distribution-planner
description: Plan content distribution across platforms with metadata, UTM tracking, and compliance checks. Use before publishing content.
intent: >-
  Ensure every piece of content has a distribution plan: which platform, when, 
  with what metadata, and how to track performance. This is CG4 in the PM Gate framework.
type: interactive
best_for:
  - "Planning content distribution before publishing"
  - "Setting up UTM tracking and SEO metadata"
  - "Ensuring content meets platform compliance requirements"
scenarios:
  - "视频做好了，怎么分发？"
  - "How do we publish this across platforms?"
  - "Set up distribution tracking for our content"
estimated_time: "10-15 min"
---

## Purpose

Plan content distribution strategy BEFORE publishing. This is **CG4: PM Distribution Gate** — ensuring every content piece has a clear distribution plan with tracking, compliance, and timing.

Without this gate, content gets published without metadata, UTM tracking, or platform optimization — making it impossible to measure CG5 validation results.

## Key Concepts

### Distribution Planning Checklist

Every distribution plan covers 5 areas:

1. **Platform Selection** — Where does this content go? (YouTube, Douyin, Xiaohongshu, Bilibili, WeChat, etc.)
2. **Metadata Strategy** — Title, description, tags, thumbnail per platform
3. **Timing & Scheduling** — Best publishing time per platform and audience
4. **UTM Tracking** — Campaign parameters for measuring traffic and conversion
5. **Compliance & Legal** — Copyright, ad disclosures, platform rules

### Platform Metadata Requirements

Different platforms have different requirements:

| Platform | Title Max | Description | Tags | Thumbnail | Special |
|----------|-----------|-------------|------|-----------|---------|
| YouTube | 100 chars | 5000 chars | 500 chars | 1280×720 min | End screen, cards |
| Douyin | 55 chars | 100 chars | 5 tags | 9:16 vertical | Cover image, hashtag |
| Xiaohongshu | 20 chars | 1000 chars | Topic tags | 3:4 vertical | Emoji style |
| Bilibili | 80 chars | 250 chars | 12 tags | 16:9/9:16 | Partition selection |

### UTM Parameter Framework

Track content performance with UTM parameters:

```
utm_source={platform}        # e.g., youtube, douyin, xiaohongshu
utm_medium={content_type}    # e.g., video, short_video, carousel
utm_campaign={campaign_name}  # e.g., ai_trends_series_2024
utm_content={video_slug}     # e.g., ep01_what_is_ai
utm_term={keyword}            # optional: paid keywords
```

## Application

### Questions

**Q1: Platforms**
"Which platforms will you publish this content on? List each platform and the content format for that platform."

**Q2: Title & Description**
"For each platform, provide: optimized title (within character limits), description/summary, and 3-5 relevant tags."

**Q3: Thumbnail**
"Have you prepared platform-specific thumbnails? (9:16 for short video, 16:9 for YouTube, 3:4 for Xiaohongshu)"

**Q4: Publishing Schedule**
"When is the best time to publish on each platform? Consider your audience's timezone and platform peak hours."

**Q5: UTM Tracking**
"What UTM parameters will you use to track this content? Define source, medium, campaign, and content for each platform."

**Q6: Compliance**
"For each platform, what are the compliance requirements? (Copyright, ad disclosures, content ratings, platform-specific rules)"

### Output Format

Write to `.claude/state/L6-distribution.md`:

```markdown
# Distribution Plan: {Content Title}

## Platform Strategy

### {Platform 1}
- **Format:** {9:16 short / 16:9 landscape / etc.}
- **Title:** {platform-optimized title}
- **Description:** {platform-optimized description}
- **Tags:** {tag1}, {tag2}, {tag3}
- **Thumbnail:** {description or ready}
- **Publish Time:** {optimal time + timezone}
- **UTM:** utm_source={platform}&utm_medium={type}&utm_campaign={campaign}&utm_content={slug}

### {Platform 2}
...

## UTM Tracking Parameters
- **Campaign:** {campaign_name}
- **Source mapping:** {platform → utm_source}
- **Landing URL:** {url with UTM}

## Compliance Checklist
- [ ] Copyright clearance for all assets
- [ ] Ad/sponsor disclosure (if applicable)
- [ ] Content rating appropriate for platform
- [ ] Platform-specific rules compliance

## A/B Test Plan (optional)
- **Variant A thumbnail:** {description}
- **Variant B thumbnail:** {description}
- **Test duration:** {N hours}
```

### After Output
Run `exit-check.py` before claiming completion.

## Common Pitfalls

### Pitfall 1: Publish and Forget
**Symptom:** Content is published with no distribution plan

**Fix:** Platform-specific metadata, timing, and tracking must be defined BEFORE publishing. Use this skill as the gate.

### Pitfall 2: Same Metadata Everywhere
**Symptom:** Copy-pasting the same title, description, and tags across all platforms

**Fix:** Each platform has different character limits, audience expectations, and algorithm preferences. Optimize per platform.

### Pitfall 3: No UTM Tracking
**Symptom:** "We'll just check analytics"

**Fix:** Without UTM parameters, you can't attribute traffic to specific content pieces. CG5 validation (pm/content-validation) depends on this data.

### Pitfall 4: Ignoring Compliance
**Symptom:** "We'll figure out copyright after publishing"

**Fix:** Platforms can take down content retroactively. Ad disclosures are legally required in many jurisdictions. Resolve compliance BEFORE publishing.

### Pitfall 5: No A/B Testing Plan
**Symptom:** Publishing with a single thumbnail and title, hoping for the best

**Fix:** At minimum, plan A/B tests for thumbnails. The best thumbnail often outperforms by 2-3x on CTR.

## References

- Related skills: pm/content-validation (CG5), content/video-compositor (CG3)
- Upstream: L0-strategy.md (business goals and KPIs)
- PM Gate: CG4 — PM Distribution Gate