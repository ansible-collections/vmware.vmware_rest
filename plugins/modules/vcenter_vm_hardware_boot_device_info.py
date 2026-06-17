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
module: vcenter_vm_hardware_boot_device_info
short_description: Retrieves boot device order for a virtual machine.
description:
  - Returns the ordered list of boot devices configured for a virtual machine in vCenter.
  - Each entry describes a bootable virtual device type or a specific bootable device.
author:
  - Ansible Eco Content Team (@eco-ansible-content)
extends_documentation_fragment:
  - vmware.vmware_rest.connection_params
options:
  vm:
    description:
      - Identifier of the virtual machine.
      - Must be an identifier (MOID) for a C(VirtualMachine) resource.
    type: str
    required: true
version_added: 4.11.0
requirements: []
notes:
  - Generated from vSphere API spec 9.1.0.
  - Has support for vSphere API 7.0.3.
  - Has support for vSphere API 8.0.2.
"""

EXAMPLES = r"""
- name: Get boot device order for a virtual machine
  vmware.vmware_rest.vcenter_vm_hardware_boot_device_info:
    vm: vm-1001
  register: boot_devices

- name: Verify CD-ROM is the first boot device
  ansible.builtin.assert:
    that:
      - boot_devices.value | length > 0
      - boot_devices.value[0].type == "CDROM"
"""

RETURN = r"""
value:
  description:
    - Ordered list of boot device entries for the virtual machine.
  returned: On success
  type: list
  elements: dict
  sample:
    - type: CDROM
    - type: DISK
      disks:
        - "2000"
  contains:
    type:
      description:
        - Virtual device type for the boot entry.
      type: str
      choices:
        - CDROM
        - DISK
        - ETHERNET
        - FLOPPY
      sample: CDROM
    nic:
      description:
        - Virtual Ethernet adapter identifier used when I(type=ETHERNET).
        - Must be an identifier (MOID) for a
          C(com.vmware.vcenter.vm.hardware.Ethernet) resource.
      type: str
      sample: "4000"
    disks:
      description:
        - Ordered list of virtual disk identifiers used when I(type=DISK).
        - Each element must be an identifier (MOID) for a
          C(com.vmware.vcenter.vm.hardware.Disk) resource.
      type: list
      elements: str
      sample:
        - "2000"
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.vmware.vmware_rest.plugins.module_utils._argument_spec import (
    connection_params_argument_spec,
)
from ansible_collections.vmware.vmware_rest.plugins.module_utils._module_base import (
    VmwareRestInfoModuleBase,
    normalize_list_response,
)

BOOT_DEVICE_PATH = "/vcenter/vm/{vm}/hardware/boot/device"


class VmwareRestInfoModule(VmwareRestInfoModuleBase):
    PAYLOAD_FORMAT = {
        "get": {"query": {}, "body": {}, "path": {"vm": "vm"}},
    }

    def get_info(self):
        path = self.build_path(BOOT_DEVICE_PATH)
        response = self.client.get(path)
        if response.status == 404:
            return []
        return normalize_list_response(response.json)


def main():
    module_args = connection_params_argument_spec()
    module_args["vm"] = {"type": "str", "required": True}

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
    )

    info_module = VmwareRestInfoModule(module)
    result = info_module.get_info()
    module.exit_json(value=result)


if __name__ == "__main__":
    main()
