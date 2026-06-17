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
module: vcenter_vm_guest_operations_info
short_description: Retrieves guest operating system operation status for a virtual machine.
description:
  - Returns information about guest operation readiness for a virtual machine in vCenter.
  - Indicates whether the virtual machine can process guest operations and interactive guest operations.
  - Requires the C(System.Read) privilege on the virtual machine.
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
- name: Get guest operations status for a virtual machine
  vmware.vmware_rest.vcenter_vm_guest_operations_info:
    vm: vm-1001
  register: guest_operations

- name: Check whether guest operations are ready
  ansible.builtin.debug:
    msg: "Guest operations ready: {{ guest_operations.value.guest_operations_ready }}"
  when: guest_operations.value is defined
"""

RETURN = r"""
value:
  description:
    - Guest operating system operation status information.
  returned: On success
  type: dict
  sample:
    guest_operations_ready: true
    interactive_guest_operations_ready: true
  contains:
    guest_operations_ready:
      description:
        - Whether the virtual machine is ready to process guest operations.
      type: bool
      sample: true
    interactive_guest_operations_ready:
      description:
        - Whether the virtual machine is ready to process interactive guest operations.
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

OPERATIONS_PATH = "/vcenter/vm/{vm}/guest/operations"


class VmwareRestInfoModule(VmwareRestInfoModuleBase):
    PAYLOAD_FORMAT = {
        "get": {"query": {}, "body": {}, "path": {"vm": "vm"}},
    }

    def get_info(self):
        path = self.build_path(OPERATIONS_PATH)
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
