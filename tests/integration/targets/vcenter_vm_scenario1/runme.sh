#!/usr/bin/env bash
set -eu
source ../init.sh
set -eux

export ANSIBLE_CALLBACK_WHITELIST=goneri.utils.update_return_section
exec ansible-playbook -i ../inventory.networking playbook.yaml
