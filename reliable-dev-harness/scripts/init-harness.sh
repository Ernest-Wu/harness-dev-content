#!/bin/bash
# init-harness.sh - Initialize Reliable Dev Harness in a new or existing project
set -e

PROJECT_ROOT="${1:-.}"
HARNESS_DIR="$PROJECT_ROOT/.claude"

echo "Initializing Reliable Dev Harness in $PROJECT_ROOT..."

# Create directory structure
mkdir -p "$HARNESS_DIR"/{skills,hooks,agents,state,feedback,docs}
mkdir -p "$PROJECT_ROOT/scripts"

# Copy harness files if not already present
if [ ! -f "$HARNESS_DIR/CLAUDE.md" ]; then
    echo "  -> Copying CLAUDE.md"
    cp "$(dirname "$0")/../.claude/CLAUDE.md" "$HARNESS_DIR/CLAUDE.md"
fi

if [ ! -f "$HARNESS_DIR/check-harness.py" ]; then
    echo "  -> Copying check-harness.py"
    cp "$(dirname "$0")/../.claude/check-harness.py" "$HARNESS_DIR/check-harness.py"
fi

# Create empty state files if missing
touch "$HARNESS_DIR/state/L2-spec.md"
touch "$HARNESS_DIR/state/L3-design.md"
touch "$HARNESS_DIR/state/L4-plan.md"
touch "$HARNESS_DIR/state/task-history.yaml"
touch "$HARNESS_DIR/feedback/FEEDBACK-INDEX.md"

# Create review flag for stop-gate
touch "$HARNESS_DIR/state/review-pending.flag"

echo "✅ Harness initialized. Run 'python3 $HARNESS_DIR/check-harness.py' to verify."
