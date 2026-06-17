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
module: vcenter_vm_guest_power_info
short_description: Retrieves guest operating system power state information for a virtual machine.
description:
  - Returns information about the guest operating system power state of a virtual machine in vCenter.
  - Includes the guest power state and whether the virtual machine is ready for soft power operations.
  - Requires VMware Tools to be running in the guest operating system.
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
- name: Get guest operating system power state for a virtual machine
  vmware.vmware_rest.vcenter_vm_guest_power_info:
    vm: vm-1001
  register: guest_power_info

- name: Display guest power state
  ansible.builtin.debug:
    msg: "Guest OS state is {{ guest_power_info.value.state }}"
  when:
    - guest_power_info.value is defined
    - guest_power_info.value.state is defined
"""

RETURN = r"""
value:
  description:
    - Guest operating system power state information.
  returned: On success
  type: dict
  sample:
    operations_ready: true
    state: RUNNING
  contains:
    state:
      description:
        - The power state of the guest operating system.
      type: str
      choices:
        - RUNNING
        - SHUTTING_DOWN
        - RESETTING
        - STANDBY
        - NOT_RUNNING
        - UNAVAILABLE
      sample: RUNNING
    operations_ready:
      description:
        - Whether the virtual machine is ready to process soft power operations.
      type: bool
      sample: true
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.vmware.vmware_rest.plugins.module_utils._argument_spec import (
    connection_params_argument_spec,
)
from ansible_collections.vmware.vmware_rest.plugins.module_utils._module_base import (
    VmwareRestInfoModuleBase,
)

GUEST_POWER_PATH = "/vcenter/vm/{vm}/guest/power"


class VmwareRestInfoModule(VmwareRestInfoModuleBase):
    PAYLOAD_FORMAT = {
        "get": {"query": {}, "body": {}, "path": {"vm": "vm"}},
    }

    def get_info(self):
        path = self.build_path(GUEST_POWER_PATH)
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
