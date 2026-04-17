#!/bin/bash
# Content Validator Hook
# Runs exit-checks for content domain skills
# Called by Orchestrator at content pipeline gate points

set -e

SKILLS_DIR="$(dirname "$0")/../skills/content"

echo "🔍 Content Validator Hook"

# Determine which content skill to validate based on argument
SKILL="${1:-}"

if [ -z "$SKILL" ]; then
    echo "Usage: $0 <script-writer|visual-designer|tts-engine|video-compositor>"
    exit 1
fi

EXIT_CHECK="$SKILLS_DIR/$SKILL/exit-check.py"

if [ ! -f "$EXIT_CHECK" ]; then
    echo "❌ Exit check not found: $EXIT_CHECK"
    exit 1
fi

echo "Running exit check for: content/$SKILL"
python3 "$EXIT_CHECK"
EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    echo "✅ content/$SKILL passed exit check"
else
    echo "❌ content/$SKILL failed exit check (exit code: $EXIT_CODE)"
    echo "   Fix the issues above before proceeding."
fi

exit $EXIT_CODE
