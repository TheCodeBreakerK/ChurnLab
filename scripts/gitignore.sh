#!/bin/bash
set -euo pipefail

if [ -f .gitignore ]; then
    echo "⚠️  .gitignore already exists, skipping"
    exit 0
fi

echo "Downloading Python .gitignore from GitHub..."
curl -fsSL https://raw.githubusercontent.com/github/gitignore/main/Python.gitignore -o .gitignore
echo "✅ .gitignore created"
