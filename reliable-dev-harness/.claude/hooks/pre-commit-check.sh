#!/bin/bash
# pre-commit-check.sh - Compile gate before commit
set -e

# Auto-detect build command
if [ -f "package.json" ]; then
    npm run build
elif [ -f "Cargo.toml" ]; then
    cargo build
elif [ -f "go.mod" ]; then
    go build ./...
elif [ -d "src" ]; then
    python3 -m compileall src/
fi

echo "✅ Build passed. Commit allowed."
