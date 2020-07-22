INVENTORY_PATH="${INVENTORY_PATH:-../../inventory.networking}"

# The inventory file should have the following format:
# [vmware_rest]
# localhost ansible_connection=local ansible_python_interpreter=python
#
# [vmware_rest:vars]
# hostname=vcenter.test
# username=administrator@vsphere.local
# password=TRQhZ:WdXrhA*w;nqaU0

if [ -f ${INVENTORY_PATH} ]; then
    echo "Reading credentials from inventory.networking"
    export VMWARE_HOST=$(sed 's,^hostname=\(.*\),\1,;t;d' ${INVENTORY_PATH})
    VMWARE_USER=$(sed 's,^username=\(.*\),\1,;t;d' ${INVENTORY_PATH})
    VMWARE_PASSWORD=$(sed 's,^password=\(.*\),\1,;t;d' ${INVENTORY_PATH})
elif [ -f /tmp/vcenter/tmp/vcenter_password.txt ]; then
    echo "Reading credentials from /tmp/vcenter/tmp/vcenter_password.txt"
    VMWARE_HOST="vcenter.test"
    VMWARE_USER="administrator@vsphere.local"
    VMWARE_PASSWORD="$(cat /tmp/vcenter/tmp/vcenter_password.txt)"
fi

export ANSIBLE_CONFIG=ansible.cfg
export VMWARE_HOST
export VMWARE_USER
export VMWARE_PASSWORD
