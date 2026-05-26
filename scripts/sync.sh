#!/bin/bash
set -euo pipefail

echo "Syncing dependencies with uv..."
uv sync
echo "✅ Sync complete"
