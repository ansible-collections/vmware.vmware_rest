#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright: (c) 2026, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#
# This module is generated using LLM agents and skills defined in the vmware.vmware_rest repository.
# See: https://github.com/ansible-collections/vmware.vmware_rest
#

DOCUMENTATION = r"""
module: vcenter_vm_hardware_disk_info
short_description: Retrieves virtual disk information for a virtual machine.
description:
  - Returns information about virtual disks belonging to a virtual machine.
  - When I(disk) is specified, returns information for that virtual disk only.
  - When I(label) is specified, returns information for virtual disks with a
    matching device label.
  - When I(disk) and I(label) are omitted, lists all virtual disks and returns
    detailed information for each.
author:
  - Ansible Eco Content Team (@eco-ansible-content)
extends_documentation_fragment:
  - vmware.vmware_rest.connection_params
options:
  vm:
    description:
      - Virtual machine identifier.
      - Must be an identifier (MOID) for a C(VirtualMachine) resource.
    type: str
    required: true
  disk:
    description:
      - Identifier of the virtual disk to retrieve.
      - Must be an identifier (MOID) for a
        C(com.vmware.vcenter.vm.hardware.Disk) resource.
    type: str
  label:
    description:
      - Device label used to filter virtual disks.
      - When a single virtual disk matches, the module also returns its MOID in
        I(id).
    type: str
version_added: 4.11.0
requirements: []
notes:
  - Generated from vSphere API spec 9.1.0.
  - Has support for vSphere API 7.0.3.
  - Has support for vSphere API 8.0.2.
"""

EXAMPLES = r"""
- name: List virtual disks for a virtual machine
  vmware.vmware_rest.vcenter_vm_hardware_disk_info:
    vm: vm-1001
  register: vm_disks

- name: Get information about a specific virtual disk
  vmware.vmware_rest.vcenter_vm_hardware_disk_info:
    vm: vm-1001
    disk: "2000"
  register: vm_disk_info

- name: Get information about a virtual disk by label
  vmware.vmware_rest.vcenter_vm_hardware_disk_info:
    vm: vm-1001
    label: Hard disk 1
  register: vm_disk_by_label
"""

RETURN = r"""
id:
  description:
    - Identifier of the virtual disk.
    - Must be an identifier (MOID) for a
      C(com.vmware.vcenter.vm.hardware.Disk) resource.
    - Returned when I(label) matches exactly one virtual disk.
  returned: When I(label) matches exactly one virtual disk
  type: str
  sample: "2000"

value:
  description:
    - Virtual disk information.
    - Returns a list of disk dictionaries when listing or filtering virtual disks.
    - Returns a list containing a single disk dictionary when I(disk) is specified.
  returned: On success
  type: list
  elements: dict
  sample:
    - disk: "2000"
      label: Hard disk 1
      type: SCSI
      capacity: 10737418240
      backing:
        type: VMDK_FILE
        vmdk_file: "[datastore1] vm-1001/vm-1001.vmdk"
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.vmware.vmware_rest.plugins.module_utils._argument_spec import (
    connection_params_argument_spec,
)
from ansible_collections.vmware.vmware_rest.plugins.module_utils._module_base import (
    VmwareRestInfoModuleBase,
)

LIST_PATH = "/vcenter/vm/{vm}/hardware/disk"
ITEM_PATH = "/vcenter/vm/{vm}/hardware/disk/{disk}"


class VmwareRestInfoModule(VmwareRestInfoModuleBase):
    PAYLOAD_FORMAT = {
        "list": {"query": {}, "body": {}, "path": {"vm": "vm"}},
        "get": {"query": {}, "body": {}, "path": {"vm": "vm", "disk": "disk"}},
    }

    def _get_disk(self, disk_id):
        path = self.build_path(ITEM_PATH, {"disk": disk_id})
        response = self.client.get(path)
        if response.status == 404:
            return None

        info = response.json
        if "disk" not in info:
            info["disk"] = disk_id
        return info

    def get_info(self):
        disk = self.params.get("disk")
        if disk:
            info = self._get_disk(disk)
            if info is None:
                return [], None
            return [info], disk

        list_path = self.build_path(LIST_PATH)
        summaries = self.fetch_list(list_path, self.PAYLOAD_FORMAT["list"])
        result = []
        label = self.params.get("label")

        for summary in summaries:
            disk_id = summary.get("disk")
            if not disk_id:
                continue
            info = self._get_disk(disk_id)
            if info is None:
                continue
            if label is not None and info.get("label") != label:
                continue
            result.append(info)

        matched_id = None
        if label is not None and len(result) == 1:
            matched_id = result[0].get("disk")

        return result, matched_id


def main():
    module_args = connection_params_argument_spec()
    module_args["vm"] = {"type": "str", "required": True}
    module_args["disk"] = {"type": "str"}
    module_args["label"] = {"type": "str"}

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
    )

    info_module = VmwareRestInfoModule(module)
    result, disk_id = info_module.get_info()

    exit_kwargs = {"value": result}
    if disk_id:
        exit_kwargs["id"] = disk_id
    module.exit_json(**exit_kwargs)


if __name__ == "__main__":
    main()
