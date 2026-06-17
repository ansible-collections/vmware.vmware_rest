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
module: vcenter_vm_hardware_boot_info
short_description: Retrieves boot-related settings for a virtual machine.
description:
  - Returns boot-related settings of a virtual machine, including firmware type,
    boot delay, retry behavior, and setup mode flags.
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
version_added: 4.11.0
requirements: []
notes:
  - Generated from vSphere API spec 9.1.0.
  - Has support for vSphere API 7.0.3.
  - Has support for vSphere API 8.0.2.
"""

EXAMPLES = r"""
- name: Get boot settings for a virtual machine
  vmware.vmware_rest.vcenter_vm_hardware_boot_info:
    vm: vm-1001
  register: vm_boot_info

- name: Display firmware type
  ansible.builtin.debug:
    msg: "Firmware type is {{ vm_boot_info.value.type }}"
"""

RETURN = r"""
value:
  description:
    - Boot-related settings of the virtual machine.
  returned: On success
  type: dict
  contains:
    type:
      description:
        - Firmware type used by the virtual machine.
      type: str
      sample: EFI
    efi_legacy_boot:
      description:
        - Whether EFI legacy boot mode is enabled.
        - Present only when I(type=EFI).
      type: bool
      sample: false
    network_protocol:
      description:
        - Protocol used when booting over the network.
        - Present only when I(type=EFI).
      type: str
      sample: IPV4
    delay:
      description:
        - Delay in milliseconds before beginning the firmware boot process.
      type: int
      sample: 0
    retry:
      description:
        - Whether the virtual machine automatically retries boot after a failure.
      type: bool
      sample: false
    retry_delay:
      description:
        - Delay in milliseconds before retrying boot after a failure.
      type: int
      sample: 10000
    enter_setup_mode:
      description:
        - Whether the firmware boot process enters setup mode on the next boot.
      type: bool
      sample: false
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.vmware.vmware_rest.plugins.module_utils._argument_spec import (
    connection_params_argument_spec,
)
from ansible_collections.vmware.vmware_rest.plugins.module_utils._module_base import (
    VmwareRestInfoModuleBase,
)

BOOT_PATH = "/vcenter/vm/{vm}/hardware/boot"


class VmwareRestInfoModule(VmwareRestInfoModuleBase):
    PAYLOAD_FORMAT = {
        "get": {"query": {}, "body": {}, "path": {"vm": "vm"}},
    }

    def get_info(self):
        path = self.build_path(BOOT_PATH)
        response = self.client.get(path)
        if response.status == 404:
            return {}
        return response.json


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
