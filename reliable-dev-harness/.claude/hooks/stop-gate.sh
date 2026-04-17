#!/bin/bash
# stop-gate.sh - Prevent session end with unreviewed code changes
set -e

# Check if any code files were modified but not reviewed
if [ -f ".claude/state/review-pending.flag" ]; then
    echo "🚫 STOP-GATE: Unreviewed code changes exist. Run code-review before stopping."
    exit 1
fi

echo "✅ Stop-gate passed. No unreviewed changes."
