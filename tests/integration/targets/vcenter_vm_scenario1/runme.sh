#!/usr/bin/env bash
set -eux
source ../init.sh
export ANSIBLE_CONFIG=ansible.cfg
#export VMWARE_HOST=$(crudini --get ../../inventory.networking vmware_rest:vars hostname)
export VMWARE_HOST="vcenter.test"
#export VMWARE_USER=$(crudini --get ../../inventory.networking vmware_rest:vars username)
export VMWARE_USER="administrator@vsphere.local"
#export VMWARE_PASSWORD=$(crudini --get ../../inventory.networking vmware_rest:vars password)
export VMWARE_PASSWORD="$(cat /tmp/vcenter/tmp/vcenter_password.txt)"
exec ansible-playbook -i ../inventory.networking playbook.yaml
