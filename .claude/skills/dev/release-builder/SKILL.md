---
name: release-builder
description: Package, verify, and publish the product. Use when all Phases are complete and reviewed.
intent: Perform the final build, verification, and deployment steps to ship the product. Acts as the last physical gate before users see the product.
type: workflow
best_for:
  - Final shipping preparation
  - Production deployment verification
  - Release note generation
scenarios:
  - All development phases are complete and code-reviewed
  - Smoke tests must pass on production bundle
  - Rollback plan is required before deploy
  - Release notes must document what changed
estimated_time: 30-60 minutes
---

## Purpose

Package, verify, and publish the product. This is the final gate before users see it.

A failed release-builder means the product is not ready to ship — even if all individual Tasks passed their exit-checks.

## Key Concepts

### Build Verification
Production build must pass with zero errors. This is not optional.

### Smoke Tests
Critical paths (login, payment, core flow) must be manually verified on the production bundle, not just in dev mode.

### Deployment Checklist
Env vars, domains, SSL, analytics, error tracking — all must be verified before deploy.

### Rollback Plan
You must know how to revert before you push. A deploy without a rollback plan is a gamble.

### Release Notes
Document what changed, why, and any breaking changes. Future-you (and your team) will thank present-you.

## Application

### Step 1: Run Production Build
```bash
# Example for npm projects
npm run build
# or
npm run build:prod
```

Verify:
- [ ] Build completes with zero errors
- [ ] No console warnings in production mode
- [ ] Bundle size is within expected range

### Step 2: Run Smoke Tests
Verify these on the production bundle (not dev server):
- [ ] Login flow works end-to-end
- [ ] Core payment/feature flow works
- [ ] Error pages (404, 500) render correctly
- [ ] Mobile responsiveness is acceptable

### Step 3: Verify Deployment Configuration
Checklist:
- [ ] Environment variables are set in production
- [ ] Domain and SSL certificate are valid
- [ ] Analytics tracking is active
- [ ] Error monitoring (Sentry, etc.) is connected
- [ ] Database migrations are ready (if applicable)

### Step 4: Prepare Rollback Plan
Document:
- Previous stable version/tag
- Rollback command or procedure
- Estimated rollback time
- Data migration considerations (if any)

### Step 5: Deploy
```bash
# Example deploy commands
# Vercel: vercel --prod
# AWS: aws deploy ...
# Docker: docker push && kubectl rollout ...
```

### Step 6: Monitor for 30 Minutes After Deploy
- [ ] No error spikes in monitoring
- [ ] Core metrics are stable
- [ ] No user complaints in support channels

### Output: Release Notes
Write to `.claude/state/RELEASE-NOTES.md`:

```markdown
# Release Notes: {Version}

## Changes
- {Change 1}
- {Change 2}

## Breaking Changes
- {None / List}

## Known Issues
- {None / List}

## Rollback
- Tag: {previous-stable-tag}
- Command: {rollback-command}
```

## Examples

### Good Release Checklist
Build passed. Smoke tests passed. Rollback plan documented. Monitoring green for 30 minutes.

### Bad Release
Deployed without smoke tests. No rollback plan. Release notes missing.

## Common Pitfalls

### Pitfall 1: Deploying Without Smoke Tests
**Fix:** Always verify login, payment, or core flow after deploy.

### Pitfall 2: Missing Rollback Plan
**Fix:** Know how to revert before you push. Document the previous stable tag and rollback command.

### Pitfall 3: Forgetting Release Notes
**Fix:** Write release notes before deploy, not after. Future debugging depends on knowing what changed.

### Pitfall 4: Deploying on Friday Afternoon
**Fix:** If something breaks, you want the team available. Avoid end-of-week or end-of-day deploys unless critical.

## References

- Related skills: dev-builder, code-review
- Related hooks: pre-commit-check.sh
- Output: `.claude/state/RELEASE-NOTES.md`
