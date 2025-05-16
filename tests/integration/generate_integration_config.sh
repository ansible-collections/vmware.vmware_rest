#!/usr/bin/env bash
# shellcheck disable=SC2155,SC2086

# Resolve the script's directory reliably
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"
cd "$SCRIPT_DIR" || exit 1

# Truncate the output file
truncate -s 0 "${SCRIPT_DIR}/integration_config.yml"

# Read the template and substitute environment variables
while read -r line; do
    eval 'echo "'"$line"'"' >> "${SCRIPT_DIR}/integration_config.yml"
done < "${SCRIPT_DIR}/integration_config.yml.tpl"
