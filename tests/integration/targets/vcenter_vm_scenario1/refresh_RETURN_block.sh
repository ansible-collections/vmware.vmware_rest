#!/usr/bin/env bash
# shellcheck disable=SC2155
set -eux

export ANSIBLE_CALLBACK_WHITELIST=goneri.utils.collect_task_outputs
export COLLECT_TASK_OUTPUTS_COLLECTION=vmware.vmware_rest
export COLLECT_TASK_OUTPUTS_TARGET_DIR=$(realpath ../../../../manual/source/vmware_rest_scenarios/task_outputs/)
export INVENTORY_PATH=/tmp/inventory-vmware_rest
source ../init.sh
ansible-playbook prepare.yml
exec ansible-playbook run.yml -e wait_for_vm=1
