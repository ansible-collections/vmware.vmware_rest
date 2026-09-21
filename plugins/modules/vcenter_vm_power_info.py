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
module: vcenter_vm_power_info
short_description: Gather information about the power state of a virtual machine.
description:
  - Retrieve the current power state of a virtual machine.
  - The returned details indicate whether the virtual machine is powered on, powered off, or suspended.
  - When the virtual machine is powered off, the result also reports whether it was shut down cleanly,
    which can be used to detect an unexpected crash.
  - Use this module to check a virtual machine's power state before performing operations that require
    it to be in a specific state.

author:
  - Ansible Eco Content Team (@eco-ansible-content)

deprecated:
  removed_in: 6.0.0
  why: This functionality has been moved to vmware.vmware.vm_info.
  alternative: Use M(vmware.vmware.vm_info) instead.

extends_documentation_fragment:
  - vmware.vmware_rest.connection_params

options:
  vm:
    description:
      - Identifier of the virtual machine whose power state information should be gathered.
      - Must be an identifier (MOID) for a C(Vm) resource.
    type: str
    required: true

version_added: 5.0.0

requirements: []

notes:
  - Generated from vSphere API spec 9.1.0.
  - Compatible with vSphere API 7.0.3.
  - Compatible with vSphere API 8.0.2.
"""

EXAMPLES = r"""
- name: Gather power state information for a virtual machine
  vmware.vmware_rest.vcenter_vm_power_info:
    vm: vm-1013
  register: power_info

- name: Fail if the virtual machine is not powered on
  ansible.builtin.assert:
    that:
      - power_info.value.state == "POWERED_ON"
"""

RETURN = r"""
value:
  description: Detailed information about the power state of the virtual machine.
  returned: On success
  type: dict
  sample:
    clean_power_off: true
    state: POWERED_OFF
info:
  description: A list containing the detailed power state information for the queried virtual machine.
  returned: On success
  type: list
  sample:
    - clean_power_off: true
      state: POWERED_OFF
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
ITEM_ENDPOINT = "/vcenter/vm/{vm}/power"


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
