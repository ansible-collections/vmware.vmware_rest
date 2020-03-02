#!/usr/bin/env bash
pwd
ls ..
set -eux
export ANSIBLE_CONFIG=ansible.cfg
export VMWARE_HOST=$(crudini --get ../../inventory.networking vmware_rest:vars hostname)
export VMWARE_USER=$(crudini --get ../../inventory.networking vmware_rest:vars username)
export VMWARE_PASSWORD=$(crudini --get ../../inventory.networking vmware_rest:vars password)
#ansible-playbook prepare_environment.yml $*
#ansible-inventory --list -i vmware.yaml
exec ansible-playbook -i ../inventory.networking playbook.yaml