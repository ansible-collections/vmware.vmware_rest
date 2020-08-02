INVENTORY_PATH="${INVENTORY_PATH:-../../inventory.networking}"

# The inventory file should have the following format:
# [vmware_rest]
# localhost ansible_connection=local ansible_python_interpreter=python
#
# [vmware_rest:vars]
# hostname=vcenter.test
# username=administrator@vsphere.local
# password=TRQhZ:WdXrhA*w;nqaU0
echo "Reading credentials from ${INVENTORY_PATH}"
export VMWARE_HOST=$(sed 's,^vcenter_hostname=\(.*\),\1,;t;d' ${INVENTORY_PATH})
export VMWARE_USER=$(sed 's,^vcenter_username=\(.*\),\1,;t;d' ${INVENTORY_PATH})
export VMWARE_PASSWORD=$(sed 's,^vcenter_password=\(.*\),\1,;t;d' ${INVENTORY_PATH})
export ESXI1_HOSTNAME=$(sed 's,^esxi1_hostname=\(.*\),\1,;t;d' ${INVENTORY_PATH})
export ESXI1_USERNAME=$(sed 's,^esxi1_username=\(.*\),\1,;t;d' ${INVENTORY_PATH})
export ESXI1_PASSWORD=$(sed 's,^esxi1_password=\(.*\),\1,;t;d' ${INVENTORY_PATH})
export ESXI2_HOSTNAME=$(sed 's,^esxi2_hostname=\(.*\),\1,;t;d' ${INVENTORY_PATH})
export ESXI2_USERNAME=$(sed 's,^esxi2_username=\(.*\),\1,;t;d' ${INVENTORY_PATH})
export ESXI2_PASSWORD=$(sed 's,^esxi2_password=\(.*\),\1,;t;d' ${INVENTORY_PATH})
export VMWARE_VALIDATE_CERTS=no
export ANSIBLE_ROLES_PATH=..
