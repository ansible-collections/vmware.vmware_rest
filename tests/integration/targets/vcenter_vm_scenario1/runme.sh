#!/usr/bin/env bash
set -eux
source ../init.sh
echo $VMWARE_HOST
echo $VMWARE_USER
echo $VMWARE_PASSWORD

exec ansible-playbook -i ../inventory.networking playbook.yaml
