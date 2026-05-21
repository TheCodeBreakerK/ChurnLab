#!/bin/bash
set -euo pipefail

PYTHON_VERSION=${PYTHON_VERSION:-3.13}
UV_INIT_BARE=${UV_INIT_BARE:-true}

echo "Initializing Python ${PYTHON_VERSION} environment..."

uv python install "${PYTHON_VERSION}"

if [ ! -f pyproject.toml ]; then
    if [ "${UV_INIT_BARE}" = "true" ]; then
        uv init --bare --python "${PYTHON_VERSION}"
    else
        uv init --python "${PYTHON_VERSION}"
    fi
    echo "  ✅ pyproject.toml created"
else
    echo "  ℹ️  pyproject.toml already exists, skipping init"
fi

echo "✅ Initialization complete"
