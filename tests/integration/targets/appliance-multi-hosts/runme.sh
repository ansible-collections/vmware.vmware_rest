#!/usr/bin/env bash
source ../init.sh

#export ANSIBLE_ROLES_PATH=..
#export VMWARE_HOST=localhost:8000/vcsa1
#export VMWARE_USER=root
#export VMWARE_PASSWORD=password
export VMWARE_VALIDATE_CERTS=no
export VMWARE_REST_LOG_FILE=/tmp/toto.log

exec ansible-playbook -i inventory playbook.yaml
