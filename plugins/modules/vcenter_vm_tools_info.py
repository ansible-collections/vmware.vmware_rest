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
module: vcenter_vm_tools_info
short_description: Retrieves VMware Tools information for a virtual machine.
description:
  - Retrieves VMware Tools properties for a virtual machine in vCenter.
  - Returns run state, version status, upgrade policy, and related Tools metadata.
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
- name: Get VMware Tools information for a virtual machine
  vmware.vmware_rest.vcenter_vm_tools_info:
    vm: vm-1001
  register: vm_tools_info

- name: Wait until VMware Tools is running
  vmware.vmware_rest.vcenter_vm_tools_info:
    vm: vm-1001
  register: vm_tools_info
  until:
    - vm_tools_info is not failed
    - vm_tools_info.value.run_state == "RUNNING"
  retries: 10
  delay: 5
"""

RETURN = r"""
value:
  description:
    - VMware Tools properties for the virtual machine.
  returned: On success
  type: dict
  sample:
    auto_update_supported: true
    run_state: RUNNING
    upgrade_policy: MANUAL
    version_status: CURRENT
    version: 12.1.5
    version_number: 12389
    install_type: OPEN_VM_TOOLS
    guest_reboot_status:
      reboot_requested: false
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.vmware.vmware_rest.plugins.module_utils._argument_spec import (
    connection_params_argument_spec,
)
from ansible_collections.vmware.vmware_rest.plugins.module_utils._module_base import (
    VmwareRestInfoModuleBase,
)

TOOLS_PATH = "/vcenter/vm/{vm}/tools"


class VmwareRestInfoModule(VmwareRestInfoModuleBase):
    PAYLOAD_FORMAT = {
        "get": {"query": {}, "body": {}, "path": {"vm": "vm"}},
    }

    def get_info(self):
        path = self.build_path(TOOLS_PATH)
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
