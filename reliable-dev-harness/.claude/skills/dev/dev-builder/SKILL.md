---
name: dev-builder
description: Implement one Task at a time with compile validation and regression checks. Use when translating a DEV-PLAN task into working code.
intent: >-
  Break a Phase into discrete Tasks and implement them one by one. Each Task must compile and pass basic validation before proceeding. Prevents "big bang" commits where a single change introduces multiple intertwined bugs.
type: workflow
best_for:
  - "Implementing a specific task from a DEV-PLAN"
  - "Adding a feature or fixing a bug with minimal blast radius"
  - "Ensuring each incremental change is independently valid"
scenarios:
  - "Implement the login page according to the design mockup"
  - "Add the API endpoint for saving user preferences"
  - "Refactor the state management to use Zustand"
estimated_time: "10-30 min per Task"
---

## Purpose

Implement one discrete Task at a time. Each Task must:
1. Be small enough to reason about in isolation
2. Compile / build without errors
3. Pass any existing tests (regression check)
4. Be documented in `task-history.yaml`

This prevents the "big bang" anti-pattern where 500 lines of mixed changes land at once and nobody knows which part broke what.

## Key Concepts

### Task Definition
A Task is the **smallest coherent unit of work** that can be built and reviewed independently. Examples:
- ✅ Add the `LoginForm` component with validation
- ✅ Create the `POST /api/preferences` endpoint
- ❌ "Build the entire auth system" (too big)

### Compile-First Discipline
Code that does not compile is not "almost done" — it's **not done**. The build must pass before the Task is declared complete.

### Regression Check
Before claiming a Task is done, run the existing test suite (or at least the tests related to the changed files). A Task that breaks existing functionality is a failed Task.

### Anti-Patterns
- **Not a Phase:** Don't try to implement an entire Phase in one go
- **Not a sketch:** Don't submit "work in progress" that doesn't compile
- **Not a refactor festival:** Don't mix unrelated cleanups with feature work

## Application

### Before You Start
Read:
1. `.claude/state/L1-summary.md` — project context
2. `.claude/state/L4-plan.md` — current Phase and active Task
3. `.claude/state/L2-spec.md` — functional requirements for this Task
4. `.claude/state/L3-design.md` — visual standards (if UI Task)
5. Design mockup / Figma link (if available) — **highest authority for UI**

### Step 1: Plan the Task (Mental or Written)
- What files will be created, modified, or deleted?
- What is the public interface (API, component props, function signature)?
- What is the smallest test that proves this works?

### Step 2: Implement
- Write the code
- Write or update tests for the new behavior
- Keep changes focused; if you find yourself refactoring unrelated code, stop and note it for a future Task

### Step 3: Compile / Build
Run the project's build command:
```bash
# Examples — use whatever the project actually uses
npm run build
pnpm build
python -m compileall src/
 cargo build
```

**If it fails:** Fix it. Do not proceed.

### Step 4: Regression Check
Run the relevant tests:
```bash
npm test -- --related
pytest src/path/to/test_file.py
cargo test
```

**If tests fail:** Fix them. Do not proceed.

### Step 5: Run Exit Check
```bash
python3 .claude/skills/dev-builder/exit-check.py
```

**If it fails:** Fix the issues. Do not proceed.

### Step 6: Update Task History
Append to `.claude/state/task-history.yaml`:
```yaml
- task_id: T-042
  phase: "Phase 2: Auth"
  description: "Implement login form UI"
  files_changed:
    - src/components/LoginForm.tsx
    - src/components/LoginForm.test.tsx
  status: completed
  build_passed: true
  tests_passed: true
```

### Step 7: Hand Off
The Task is now ready for `code-review`.

## Examples

### Good Task
**Scope:** Add a password visibility toggle to the login form.
**Changes:** 1 component file + 1 test file.
**Validation:** Component renders, toggle works, existing auth tests still pass.

### Bad Task
**Scope:** "Build auth."
**Changes:** 12 files, 800 lines, mixed UI + API + state management.
**Result:** Impossible to review, impossible to debug, high regression risk.

## Common Pitfalls

### Pitfall 1: Mixing Refactors with Features
**Symptom:** A "add login button" Task also renames 15 variables and reformats 8 files.

**Consequence:** Reviewer can't see the forest for the trees. Bugs hide in noise.

**Fix:** Refactors go in their own Tasks.

### Pitfall 2: "I'll Add Tests Later"
**Symptom:** Feature code is written, tests are skipped because "we're in a hurry."

**Consequence:** "Later" never comes. The next refactor breaks the feature silently.

**Fix:** Tests are part of the Task. No tests = Task not done.

### Pitfall 3: Ignoring Design Mockups
**Symptom:** Developer guesses spacing, colors, and interactions because checking Figma is "too much work."

**Consequence:** UI looks like a different product on every page.

**Fix:** Design mockup is the highest authority. When in doubt, match the mockup exactly.

### Pitfall 4: Not Running the Build
**Symptom:** "It compiles in my head."

**Consequence:** Type errors, missing imports, and broken pipelines discovered during review or deployment.

**Fix:** Build must pass before the Task leaves your hands. No exceptions.

## References

### Related Skills
- `dev-planner` — Produces the DEV-PLAN this Skill consumes
- `code-review` — Receives the output of this Skill
- `bug-fixer` — Called when this Skill or its review finds defects
- `release-builder` — Packages the accumulated completed Tasks

### Related Hooks
- `pre-commit-check.sh` — Runs after this Skill, before commit
- `mark-review-needed.sh` — Flags the changed files for review
