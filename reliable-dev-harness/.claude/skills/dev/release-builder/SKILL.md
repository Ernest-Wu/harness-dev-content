---
name: release-builder
description: Package and publish the product. Use when all Phases are complete and reviewed.
intent: Perform the final build, verification, and deployment steps to ship the product.
type: workflow
---

## Purpose

Package, verify, and publish the product. This is the final gate before users see it.

## Key Concepts

- Build verification = production build passes
- Smoke tests = critical paths still work
- Deployment checklist = env vars, domains, SSL, analytics

## Application

1. Run the production build
2. Run smoke tests on the production bundle
3. Verify deployment configuration
4. Deploy
5. Monitor for 30 minutes after deploy

## Common Pitfalls

### Pitfall 1: Deploying Without Smoke Tests
**Fix:** Always verify login, payment, or core flow after deploy.

### Pitfall 2: Missing Rollback Plan
**Fix:** Know how to revert before you push.

## References

- Related skills: dev-builder, code-review
