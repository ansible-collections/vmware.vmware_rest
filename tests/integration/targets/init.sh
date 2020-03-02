export ANSIBLE_CONFIG=ansible.cfg
if [ -f ../../inventory.networking ]; then
    echo "Reading credentials from inventory.networking"
    export VMWARE_HOST=$(crudini --get ../../inventory.networking vmware_rest:vars hostname)
    VMWARE_USER=$(crudini --get ../../inventory.networking vmware_rest:vars username)
    VMWARE_PASSWORD=$(crudini --get ../../inventory.networking vmware_rest:vars password)
fi
if [ -f /tmp/vcenter/tmp/vcenter_password.txt ]; then
    echo "Reading credentials from /tmp/vcenter/tmp/vcenter_password.txt"
    VMWARE_HOST="vcenter.test"
    VMWARE_USER="administrator@vsphere.local"
    VMWARE_PASSWORD="$(cat /tmp/vcenter/tmp/vcenter_password.txt)"
fi

export VMWARE_HOST
export VMWARE_USER
export VMWARE_PASSWORD

