#!/bin/bash

# PostToolUse hook: auto-format and validate after every file edit.
# Runs `make format` (auto-fix) then `make check` (format+lint).
# Exits 2 to block the agent if validation fails.

# Only trigger for file-editing tools
INPUT=$(cat)
TOOL=$(echo "$INPUT" | python3 -c "import json,sys; print(json.load(sys.stdin).get('toolName',''))" 2>/dev/null || echo "")

case "$TOOL" in
    replace_string_in_file|multi_replace_string_in_file|create_file|edit_notebook_file)
        ;;
    *)
        exit 0
        ;;
esac

# Auto-format (fixes style issues before validation)
make format >/dev/null 2>&1 || true

# Validate formatting and linting
CHECK_OUTPUT=$(make check 2>&1)
CHECK_EXIT=$?

if [ "$CHECK_EXIT" -ne 0 ]; then
    echo "$CHECK_OUTPUT" | python3 -c "
import json, sys
output = sys.stdin.read().strip()
print(json.dumps({'stopReason': 'make check failed. Fix these issues before proceeding:\n' + output}))
"
    exit 2
fi

exit 0
