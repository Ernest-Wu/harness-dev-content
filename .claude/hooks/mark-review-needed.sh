#!/bin/bash
# mark-review-needed.sh - Flag that code changes require review

mkdir -p "$(dirname "$0")/../state"
touch "$(dirname "$0")/../state/review-pending.flag"
echo "Review flag set."
