#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright: (c) 2026, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#
# This module is generated using LLM agents and skills defined in the vmware.vmware_rest repository.
# See: https://github.com/ansible-collections/vmware.vmware_rest
#

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = r"""
module: vcenter_vm_tools_info
short_description: Gather information about the VMware Tools running in a virtual machine.
description:
  - Retrieve the current state of VMware Tools installed in the guest operating system of a virtual machine.
  - Returned details include the installed Tools version, its run state and version status, the installation
    type, and the configured Tools upgrade policy.
  - Use this module to check whether Tools are running and up to date before performing guest operations
    that depend on VMware Tools.

author:
  - Ansible Eco Content Team (@eco-ansible-content)

extends_documentation_fragment:
  - vmware.vmware_rest.connection_params

options:
  vm:
    description:
      - Identifier of the virtual machine whose VMware Tools information should be gathered.
      - Must be an identifier (MOID) for a C(Vm) resource.
    type: str
    required: true

version_added: 5.0.0

requirements: []

notes:
  - Generated from vSphere API spec 9.1.0.
"""

EXAMPLES = r"""
- name: Gather VMware Tools information for a virtual machine
  vmware.vmware_rest.vcenter_vm_tools_info:
    vm: vm-1013
  register: tools_info

- name: Fail if VMware Tools are not running
  ansible.builtin.assert:
    that:
      - tools_info.value.run_state == "RUNNING"
"""

RETURN = r"""
value:
  description: Detailed information about the VMware Tools installed in the virtual machine.
  returned: On success
  type: dict
  sample:
    auto_update_supported: false
    install_attempt_count: 0
    install_type: OPEN_VM_TOOLS
    run_state: RUNNING
    upgrade_policy: MANUAL
    version: "12325"
    version_number: 12325
    version_status: CURRENT
info:
  description: A list containing the detailed VMware Tools information for the queried virtual machine.
  returned: On success
  type: list
  sample:
    - auto_update_supported: false
      install_attempt_count: 0
      install_type: OPEN_VM_TOOLS
      run_state: RUNNING
      upgrade_policy: MANUAL
      version: "12325"
      version_number: 12325
      version_status: CURRENT
"""


from ansible.module_utils.basic import AnsibleModule
from ansible_collections.vmware.vmware_rest.plugins.module_utils._argument_spec import (
    connection_params_argument_spec,
)
from ansible_collections.vmware.vmware_rest.plugins.module_utils._errors import (
    VmwareModuleError,
)
from ansible_collections.vmware.vmware_rest.plugins.module_utils._info_module import (
    VmwareRestInfoModuleBase,
)
from ansible_collections.vmware.vmware_rest.plugins.module_utils._operation_configs import (
    OperationConfig,
)

MOID_PARAMETER_HINTS = ["vm"]

LIST_ENDPOINT = ""
ITEM_ENDPOINT = "/vcenter/vm/{vm}/tools"


GET_OPERATION = OperationConfig(
    name="get",
    uri=ITEM_ENDPOINT,
    http_method="GET",
)


def create_module_argument_spec() -> dict:
    module_args = connection_params_argument_spec()
    module_args["vm"] = {
        "type": "str",
        "required": True,
    }
    return module_args


def main():
    module = AnsibleModule(
        argument_spec=create_module_argument_spec(),
        supports_check_mode=True,
    )

    info_module = VmwareRestInfoModuleBase(
        module=module,
        moid_parameter_hints=MOID_PARAMETER_HINTS,
        get_operation_config=GET_OPERATION,
    )
    try:
        result = info_module.get_resource_info()
    except VmwareModuleError as e:
        module.fail_json(**e.to_module_fail_json_output())
    module.exit_json(**result)


if __name__ == "__main__":
    main()
