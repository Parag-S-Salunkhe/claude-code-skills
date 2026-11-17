#!/bin/bash
# Store a secret in the macOS login keychain without it ever touching a file, the shell history, the process list
# or an AI's context. Run it YOURSELF in a terminal:   scripts/add_secret.sh <service> <account>
# macOS's `security` tool asks for the value itself (hidden, typed twice). Read it later with:
#   security find-generic-password -s <service> -a <account> -w
set -euo pipefail
SERVICE="${1:?service name, e.g. my-api}"; ACCOUNT="${2:?account name, e.g. $USER}"
[ -t 0 ] || { echo "Run this in an interactive terminal (it prompts for the value)." >&2; exit 1; }
# -w as the LAST option = security prompts for the password; -U updates an existing item.
security add-generic-password -U -s "$SERVICE" -a "$ACCOUNT" -w
echo "Saved to the login keychain as service '$SERVICE', account '$ACCOUNT'."
