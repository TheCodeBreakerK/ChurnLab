#!/bin/bash
set -euo pipefail

OUT="requirements.txt"
echo "# Generated on $(date)" > "$OUT"
uv pip freeze >> "$OUT"
echo "✅ Dependencies frozen → ${OUT}"
