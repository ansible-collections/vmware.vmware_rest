!/usr/bin/env bash
source ../init-eco.sh

# Generates a string starting with 'test-' followed by 4 random lowercase characters
TINY_PREFIX="test-$(uuidgen | tr -d '-' | cut -c1-4 | tr '[:upper:]' '[:lower:]')"

# Extract the ansible_tags from integration_config.yml
ANSIBLE_TAGS=$(awk '/ansible_tags/ {print $2}' ../../integration_config.yml)

# Check if the ANSIBLE_TAGS variable is set
if [[ -n "$ANSIBLE_TAGS" ]]; then
  echo "ANSIBLE_TAGS is set to: $ANSIBLE_TAGS"
  exec ansible-playbook playbook.yml --tags "$ANSIBLE_TAGS" --extra-vars "tiny_prefix=$TINY_PREFIX"
fi