#!/usr/bin/env bash
set -eux

export ANSIBLE_CALLBACK_WHITELIST=goneri.utils.update_return_section
export INVENTORY_PATH=/tmp/inventory-vmware_rest
source ../init.sh
exec ansible-playbook -i ${INVENTORY_PATH} playbook.yaml -e wait_for_vm=1
