#!/usr/bin/env bash
set -eux

export ANSIBLE_CALLBACK_WHITELIST=goneri.utils.collect_task_outputs
export COLLECT_TASK_OUTPUTS_COLLECTION=vmware.vmware_rest
export COLLECT_TASK_OUTPUTS_TARGET_DIR=$(realpath ../../../../docs/source/vmware_rest_scenarios/task_outputs/)
export INVENTORY_PATH=/tmp/inventory-vmware_rest
source ../init.sh
exec ansible-playbook -i ${INVENTORY_PATH} playbook.yaml -e wait_for_vm=1
