#!/bin/bash
# mark-review-needed.sh - Flag that code changes require review

touch .claude/state/review-pending.flag
echo "Review flag set."
