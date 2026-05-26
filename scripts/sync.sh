#!/bin/bash
set -euo pipefail

echo "Syncing dependencies with uv..."
uv sync --active
echo "✅ Sync complete"
