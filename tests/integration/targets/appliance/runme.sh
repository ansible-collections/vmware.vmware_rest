#!/usr/bin/env bash
set -eux
export INVENTORY_PATH=/tmp/inventory-vmware_rest
source ../init.sh
exec ansible-playbook playbook.yaml
