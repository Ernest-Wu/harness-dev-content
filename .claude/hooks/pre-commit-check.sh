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
elif [ -f "pyproject.toml" ] || [ -f "setup.py" ] || [ -f "setup.cfg" ]; then
    python3 -m compileall .
elif [ -d "src" ] && find src -name "*.py" | grep -q .; then
    python3 -m compileall src/
elif find . -maxdepth 1 -name "*.py" | grep -q .; then
    python3 -m compileall .
else
    echo "⚠️ No build system detected (no package.json, Cargo.toml, go.mod, pyproject.toml, setup.py, or Python source). Pre-commit check cannot verify build safety."
    exit 1
fi

echo "✅ Build passed. Commit allowed."
