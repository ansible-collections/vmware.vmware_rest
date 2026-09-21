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
module: vcenter_vm_guest_operations_info
short_description: Returns the guest operation status of a virtual machine.
description:
  - Returns information about whether a virtual machine is ready to process guest operations.
  - Guest operations run commands, transfer files, and manage processes inside the guest, and depend on VMware Tools being available.
  - The status distinguishes between regular guest operations and interactive guest operations that run in a logged-in user's session.

author:
  - Ansible Eco Content Team (@eco-ansible-content)

extends_documentation_fragment:
  - vmware.vmware_rest.connection_params

options:
  vm:
    description:
      - Identifier of the virtual machine whose guest operation status is returned.
      - Must be the managed object identifier (MOID) of a virtual machine, as returned by M(vmware.vmware_rest.vcenter_vm_info).
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
- name: Look up the VM called test_vm1 in the inventory
  vmware.vmware_rest.vcenter_vm_info:
    filter_names:
      - test_vm1
  register: search_result

- name: Get the guest operation status for the VM
  vmware.vmware_rest.vcenter_vm_guest_operations_info:
    vm: "{{ search_result.value[0].vm }}"
  register: guest_operations

- name: Fail if the guest is not ready for guest operations
  ansible.builtin.assert:
    that:
      - guest_operations.value.guest_operations_ready
"""

RETURN = r"""
value:
  description:
    - The guest operation readiness status of the virtual machine.
    - Returned as a dictionary because this endpoint always describes a single virtual machine.
  returned: On success
  type: dict
  sample:
    guest_operations_ready: true
    interactive_guest_operations_ready: false
info:
  description:
    - The same information as RV(value), returned as a list for consistency with other info modules.
    - This endpoint returns a single item, so the list always contains one element.
  returned: On success
  type: list
  elements: dict
  sample:
    - guest_operations_ready: true
      interactive_guest_operations_ready: false
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
ITEM_ENDPOINT = "/vcenter/vm/{vm}/guest/operations"


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
