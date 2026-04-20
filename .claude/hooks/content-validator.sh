#!/bin/bash
# Content Validator Hook
# Runs exit-checks for content domain skills
# Called by Orchestrator at content pipeline gate points

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
if python3 "$EXIT_CHECK"; then
    echo "✅ content/$SKILL passed exit check"
    exit 0
else
    EXIT_CODE=$?
    echo "❌ content/$SKILL failed exit check (exit code: $EXIT_CODE)"
    echo "   Fix the issues above before proceeding."
    exit $EXIT_CODE
fi
