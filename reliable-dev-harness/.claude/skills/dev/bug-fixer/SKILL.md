---
name: bug-fixer
description: Systematic four-stage debugging without guesswork. Use when a build fails, test fails, or review finds a defect.
intent: Apply a doctor-like diagnostic process to debugging - collect evidence, compare patterns, form hypotheses, test them one by one, then implement and verify. Prevents trial-and-error coding that introduces new bugs.
type: interactive
---

## Purpose

Debug systematically using the scientific method. No guesswork. No changing five things at once.

## Key Concepts

- Evidence first - read the full error and stack trace
- Compare pattern - find a working similar feature and diff it
- Hypothesis validation - test at most 3 hypotheses, one at a time
- Single change rule - one logical fix per attempt
- Regression check - verify the fix does not break existing tests

## Application

### Stage 1: Collect Evidence
1. Read the complete error message and stack trace
2. Reproduce the bug - is it stable or intermittent?
3. Check recent code changes (git diff)
4. Trace data flow from trigger to crash

### Stage 2: Pattern Analysis
1. Find a similar feature that works correctly
2. Identify differences between working and broken code
3. List suspicious lines or assumptions

### Stage 3: Hypothesis Validation
1. Form at most 3 hypotheses, ranked by likelihood
2. Test the most likely hypothesis with the smallest possible change
3. If hypothesis is wrong, record why and move to the next

### Stage 4: Implement and Verify
1. Make exactly one logical change
2. Compile / build
3. Run the failing test - does it pass now?
4. Run the full test suite - did you break anything else?

## Common Pitfalls

### Pitfall 1: Changing Multiple Things at Once
**Fix:** One change at a time. Otherwise you cannot know what fixed it.

### Pitfall 2: Ignoring the Stack Trace
**Fix:** Read the full trace. The answer is usually in the first few frames.

### Pitfall 3: The Same Bug Repeatedly
**Fix:** If a bug survives 3 fix attempts, stop. Re-examine the architecture or your understanding of the problem.

## References

- Related skills: dev-builder, code-review
