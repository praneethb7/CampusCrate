#!/bin/bash
# Open in Terminal, or run from an existing Terminal window.
cd -- "$(dirname -- "$0")/.." || exit 1
exec python3 scripts/native_evidence.py "$@"
