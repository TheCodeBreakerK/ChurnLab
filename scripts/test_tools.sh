#!/bin/bash
set -euo

PROJECT_NAME=${PROJECT_NAME:-Python + uv}

echo "=== Testing Installed Tools ==="
echo "Run date: $(date -Is)"
echo

report_tool() {
    local name="$1"; shift
    local cmd="$*"
    if command -v "$name" >/dev/null 2>&1; then
        if [ -n "$cmd" ]; then
            local v
            v=$($cmd 2>/dev/null | head -1)
            echo "  ✅ ${name}: ${v}"
        else
            echo "  ✅ ${name}: available"
        fi
    else
        echo "  ❌ ${name}: not found"
    fi
}

report_tool uv       "uv --version"
report_tool python   "python --version"
report_tool bash     "bash --version"
report_tool zsh      "zsh --version"
report_tool git      "git --version"
report_tool curl     "curl --version"
report_tool wget     "wget --version"
report_tool zip      "zip --version"
report_tool unzip    "unzip -v"
report_tool grep     "grep --version"
report_tool sed      "sed --version"
report_tool awk      "awk --version"
report_tool find     "find --version"
report_tool make     "make --version"

echo
echo "✅ Tool check complete for '${PROJECT_NAME}'"