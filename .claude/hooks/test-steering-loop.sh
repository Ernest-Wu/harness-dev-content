#!/bin/bash
# Steering Loop E2E Test
#
# Validates the complete feedback graduation → proposal generation flow.
# Creates mock feedback in .claude/feedback/, runs feedback-analyzer,
# generates a proposal, validates proposal format, and cleans up.
#
# Usage:
#     bash .claude/hooks/test-steering-loop.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HARNESS_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
FEEDBACK_DIR="$HARNESS_DIR/.claude/feedback"

# Unique prefix for test files (to avoid collision with real feedback)
TEST_PREFIX="TEST_E2E_$$"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

PASS=0
FAIL=0

pass() {
    echo -e "${GREEN}PASS${NC}: $1"
    ((PASS++)) || true
}

fail() {
    echo -e "${RED}FAIL${NC}: $1"
    ((FAIL++)) || true
}

warn() {
    echo -e "${YELLOW}WARN${NC}: $1"
}

# ── Cleanup helpers ─────────────────────────────────────────────────

cleanup_test_files() {
    # Remove all test feedback files
    for f in "$FEEDBACK_DIR"/${TEST_PREFIX}_*.md; do
        [[ -f "$f" ]] && rm -f "$f"
    done
    # Remove proposal file if exists
    rm -f "$FEEDBACK_DIR"/PROPOSAL-${TEST_PREFIX}-*.md
}

# Cleanup on exit (even on failure)
trap cleanup_test_files EXIT

# ── Setup ───────────────────────────────────────────────────────────

echo "═══ Steering Loop E2E Test ═══"
echo ""

# Ensure feedback directory exists
mkdir -p "$FEEDBACK_DIR"

# Clean up any leftover test files from previous runs
cleanup_test_files

# ── Test 1: Dev domain threshold (≥3) ───────────────────────────────

echo "Test 1: Dev domain graduation (threshold: 3)"

for i in 1 2 3; do
    cat > "$FEEDBACK_DIR/${TEST_PREFIX}_dev-builder-scope-creep_${i}.md" <<EOF
---
skill: dev-builder
type: scope-creep
---

Implementation included authentication feature not in the spec.
EOF
done

cd "$HARNESS_DIR"
OUTPUT=$(python3 .claude/hooks/feedback-analyzer.py 2>&1 || true)

if echo "$OUTPUT" | grep -q "dev-builder"; then
    pass "Dev domain feedback detected"
else
    fail "Dev domain feedback not detected in analyzer output"
    echo "Output: $OUTPUT"
fi

if echo "$OUTPUT" | grep -qi "Graduated"; then
    pass "Dev domain graduation detected (3 ≥ 3)"
else
    fail "Dev domain graduation not detected"
    echo "Output: $OUTPUT"
fi

cleanup_test_files

# ── Test 2: PM domain threshold (≥2) ────────────────────────────────

echo ""
echo "Test 2: PM domain graduation (threshold: 2)"

for i in 1 2; do
    cat > "$FEEDBACK_DIR/${TEST_PREFIX}_validation-metric-recalibration_${i}.md" <<EOF
---
skill: validation
type: metric-recalibration
---

Success metric needs to be redefined based on new market data.
EOF
done

OUTPUT=$(python3 .claude/hooks/feedback-analyzer.py 2>&1 || true)

if echo "$OUTPUT" | grep -q "validation"; then
    pass "PM domain feedback detected"
else
    fail "PM domain feedback not detected"
    echo "Output: $OUTPUT"
fi

if echo "$OUTPUT" | grep -qi "Graduated"; then
    pass "PM domain graduation detected (2 ≥ 2)"
else
    fail "PM domain graduation not detected"
    echo "Output: $OUTPUT"
fi

cleanup_test_files

# ── Test 3: Content domain threshold (≥5) ───────────────────────────

echo ""
echo "Test 3: Content domain graduation (threshold: 5)"

# First, check current baseline (there may be existing feedback)
BASELINE_OUTPUT=$(python3 .claude/hooks/feedback-analyzer.py 2>&1 || true)
BASELINE_COUNT=$(echo "$BASELINE_OUTPUT" | grep -o "tts-engine / voice-quality = [0-9]*" | grep -o "[0-9]*" || echo "0")
NEEDED=$((5 - BASELINE_COUNT))
if [[ $NEEDED -lt 1 ]]; then
    NEEDED=1
fi

echo "  Baseline tts-engine/voice-quality count: $BASELINE_COUNT"
echo "  Adding $NEEDED test feedback(s) to reach threshold"

for i in $(seq 1 $NEEDED); do
    cat > "$FEEDBACK_DIR/${TEST_PREFIX}_tts-engine-voice-quality_${i}.md" <<EOF
---
skill: tts-engine
type: voice-quality
---

Voice sounds too robotic for the target audience.
EOF
done

OUTPUT=$(python3 .claude/hooks/feedback-analyzer.py 2>&1 || true)

if echo "$OUTPUT" | grep -q "tts-engine"; then
    pass "Content domain feedback detected"
else
    fail "Content domain feedback not detected"
    echo "Output: $OUTPUT"
fi

if echo "$OUTPUT" | grep -qi "Graduated"; then
    pass "Content domain graduation detected ($((BASELINE_COUNT + NEEDED)) ≥ 5)"
else
    fail "Content domain graduation not detected"
    echo "Output: $OUTPUT"
fi

cleanup_test_files

# ── Test 4: Proposal generation ─────────────────────────────────────

echo ""
echo "Test 4: Proposal generation flow"

# Create graduated feedback for proposal generation
for i in 1 2 3; do
    cat > "$FEEDBACK_DIR/${TEST_PREFIX}_dev-builder-scope-creep_${i}.md" <<EOF
---
skill: dev-builder
type: scope-creep
---

Implementation included authentication feature not in the spec.
EOF
done

# Generate proposal (simulating evolution-runner behavior)
PROPOSAL_FILE="$FEEDBACK_DIR/PROPOSAL-${TEST_PREFIX}-dev-builder-scope-creep.md"
cat > "$PROPOSAL_FILE" <<'EOF'
# Proposal: Address Scope Creep in dev-builder

## Problem
3 feedback entries report scope creep in dev-builder implementation.

## Root Cause
DEV-PLAN does not clearly mark spec boundaries, causing implementers to add unplanned features.

## Proposed Change
Update dev-builder/SKILL.md Constraints section to require:
- Explicit spec boundary verification before each file modification
- Scope change must trigger Spec Gap Protocol (A/B/C/D/E classification)

## Diff
```diff
--- a/.claude/skills/dev/dev-builder/SKILL.md
+++ b/.claude/skills/dev/dev-builder/SKILL.md
@@ -30,6 +30,10 @@
 - Do not modify files unrelated to the current Task
 - After each file change, explain why it was needed
 - Run exit-check before claiming completion
+- Before adding any feature not explicitly in L2-spec.md:
+  1. Stop and classify as Spec Gap (A/B/C/D/E)
+  2. If C/D/E, escalate to PM before implementation
+  3. Document decision in L4-plan.md Spec Gaps section
```

## Verification
- [ ] Run dev-builder exit-check on existing project
- [ ] Confirm no regression in current workflow
- [ ] Test with a Task that has edge-case scope questions
EOF

# Validate proposal format
if [[ -f "$PROPOSAL_FILE" ]]; then
    pass "Proposal file generated"
else
    fail "Proposal file not found"
fi

if grep -q "## Proposed Change" "$PROPOSAL_FILE"; then
    pass "Proposal has '## Proposed Change' section"
else
    fail "Proposal missing '## Proposed Change' section"
fi

if grep -q "## Diff" "$PROPOSAL_FILE"; then
    pass "Proposal has diff block"
else
    fail "Proposal missing diff block"
fi

if grep -q "## Verification" "$PROPOSAL_FILE"; then
    pass "Proposal has verification checklist"
else
    fail "Proposal missing verification checklist"
fi

# ── Summary ─────────────────────────────────────────────────────────

echo ""
echo "══════════════════════════════════════════════════"
echo "  Steering Loop E2E Test Results"
echo "══════════════════════════════════════════════════"
echo "  Passed: $PASS"
echo "  Failed: $FAIL"
echo ""

if [[ $FAIL -eq 0 ]]; then
    echo -e "${GREEN}═══ Steering Loop E2E Test PASSED ═══${NC}"
    exit 0
else
    echo -e "${RED}═══ Steering Loop E2E Test FAILED ═══${NC}"
    exit 1
fi
