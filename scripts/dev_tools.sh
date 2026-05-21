#!/bin/bash
set -euo pipefail

echo "Installing dev tools (ruff, mypy)..."
uv add --dev ruff mypy
echo "✅ Dev tools installed"
