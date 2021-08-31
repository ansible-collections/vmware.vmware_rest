set INVENTORY_PATH /tmp/inventory-vmware_rest

# The inventory file should have the following format:
# [vmware_rest]
# localhost ansible_connection=local ansible_python_interpreter=python
#
# [vmware_rest:vars]
# hostname=vcenter.test
# username=administrator@vsphere.local
# password=TRQhZ:WdXrhA*w;nqaU0
echo "Reading credentials from $INVENTORY_PATH"
set -x VMWARE_HOST (sed 's,^vcenter_hostname=\(.*\),\1,;t;d' $INVENTORY_PATH)
set -x VMWARE_USER (sed 's,^vcenter_username=\(.*\),\1,;t;d' $INVENTORY_PATH)
set -x VMWARE_PASSWORD (sed 's,^vcenter_password=\(.*\),\1,;t;d' $INVENTORY_PATH)
set -x ESXI1_HOSTNAME (sed 's,^esxi1_hostname=\(.*\),\1,;t;d' $INVENTORY_PATH)
set -x ESXI1_USERNAME (sed 's,^esxi1_username=\(.*\),\1,;t;d' $INVENTORY_PATH)
set -x ESXI1_PASSWORD (sed 's,^esxi1_password=\(.*\),\1,;t;d' $INVENTORY_PATH)
set -x ESXI2_HOSTNAME (sed 's,^esxi2_hostname=\(.*\),\1,;t;d' $INVENTORY_PATH)
set -x ESXI2_USERNAME (sed 's,^esxi2_username=\(.*\),\1,;t;d' $INVENTORY_PATH)
set -x ESXI2_PASSWORD (sed 's,^esxi2_password=\(.*\),\1,;t;d' $INVENTORY_PATH)
set -x VMWARE_VALIDATE_CERTS no
set -x ANSIBLE_ROLES_PATH (realpath (status dirname))
set -x GOVC_PASSWORD $VMWARE_PASSWORD
set -x GOVC_HOST $VMWARE_HOST
set -x GOVC_USERNAME $VMWARE_USER
set -x GOVC_URL https://$VMWARE_HOST/sdk
set -x GOVC_INSECURE 1
