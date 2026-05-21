#!/bin/bash
set -euo pipefail

INSTALL_IPYKERNEL=${INSTALL_IPYKERNEL:-true}

if [ "${INSTALL_IPYKERNEL}" != "true" ]; then
    echo "ℹ️  Skipping ipykernel (INSTALL_IPYKERNEL != true)"
    exit 0
fi

if uv run python -c "import ipykernel" >/dev/null 2>&1; then
    echo "ℹ️  ipykernel already present, skipping"
else
    echo "Installing ipykernel..."
    uv add --dev ipykernel
    echo "✅ ipykernel installed"
fi
