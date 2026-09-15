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
module: vcenter_vm_storage_policy_compliance
short_description: Check the storage policy compliance of a virtual machine.
description:
  - Run an on-demand storage policy compliance check for a virtual machine.
  - The check compares the storage policies assigned to the virtual machine's home
    directory and virtual disks against the actual storage on which they reside.
  - The compliance results are returned in the response; use
    M(vmware.vmware_rest.vcenter_vm_storage_policy_compliance_info) to read the last
    known compliance status without triggering a new check.

author:
  - Ansible Eco Content Team (@eco-ansible-content)

extends_documentation_fragment:
  - vmware.vmware_rest.connection_params

options:
  state:
    description:
      - The desired state of the resource.
      - Use C(check) to trigger an on-demand storage policy compliance check.
      - This module only supports the C(check) action and is therefore not idempotent;
        every run performs a fresh compliance check.
    type: str
    required: true
    choices:
      - check
  vm:
    description:
      - The identifier of the virtual machine to check for compliance.
      - Must be the MOID (managed object identifier) of a C(Vm) resource.
    type: str
    required: true
  vm_home:
    description:
      - Whether to include the virtual machine's home directory in the compliance check.
      - Set to C(true) to check the home directory, C(false) to skip it.
      - This property was added in vSphere API 6.7.
    type: bool
    required: false
  disks:
    description:
      - The MOIDs (managed object identifiers) of the virtual machine's virtual disks
        to check for compliance.
      - Each identifier must reference a C(com.vmware.vcenter.vm.hardware.Disk) resource.
      - If omitted, null, or empty, the compliance check is invoked on all disks
        associated with the virtual machine.
      - This property was added in vSphere API 6.7.
    type: list
    required: false
    elements: str

version_added: 5.0.0

requirements: []

notes:
  - Generated from vSphere API spec 9.1.0.
"""

EXAMPLES = r"""
- name: Look up the VM called test_vm1 in the inventory
  register: search_result
  vmware.vmware_rest.vcenter_vm_info:
    filter_names:
      - test_vm1

- name: Check storage policy compliance for the whole VM
  vmware.vmware_rest.vcenter_vm_storage_policy_compliance:
    vm: '{{ search_result.value[0].vm }}'
    vm_home: true
    state: check

- name: Check compliance for specific disks only
  vmware.vmware_rest.vcenter_vm_storage_policy_compliance:
    vm: '{{ search_result.value[0].vm }}'
    vm_home: false
    disks:
      - '2000'
      - '2001'
    state: check
"""

RETURN = r"""
id:
  description: MOID of the virtual machine that was checked.
  returned: When state is set to a supported action.
  sample: vm-1009
  type: str
value:
  description: The raw API response body containing the storage policy compliance results.
  returned: On success
  type: raw
  sample:
    overall_compliance: COMPLIANT
    vm_home:
      status: COMPLIANT
      check_time: '2026-09-14T10:30:00.000Z'
      policy: aa6d5a82-1c88-45da-85d3-3d74b91a5bad
      failure_cause: []
    disks:
      '2000':
        status: COMPLIANT
        check_time: '2026-09-14T10:30:00.000Z'
        policy: aa6d5a82-1c88-45da-85d3-3d74b91a5bad
        failure_cause: []
"""


from ansible.module_utils.basic import AnsibleModule
from ansible_collections.vmware.vmware_rest.plugins.module_utils._argument_spec import (
    connection_params_argument_spec,
)
from ansible_collections.vmware.vmware_rest.plugins.module_utils._errors import (
    VmwareModuleError,
)
from ansible_collections.vmware.vmware_rest.plugins.module_utils._crud_module import (
    VmwareRestCrudModuleBase,
)
from ansible_collections.vmware.vmware_rest.plugins.module_utils._operation_configs import (
    OperationConfig,
)

MOID_PARAMETER_HINTS = ["vm"]

LIST_ENDPOINT = ""
ITEM_ENDPOINT = "/vcenter/vm/{vm}/storage/policy/compliance"


GET_OPERATION = OperationConfig(
    name="get",
    uri=ITEM_ENDPOINT,
    http_method="GET",
)


ACTION_OPERATIONS = {
    "check": OperationConfig(
        name="check",
        uri="/vcenter/vm/{vm}/storage/policy/compliance?action=check",
        http_method="POST",
        body_spec={
            "vm_home": {
                "required": True,
            },
            "disks": {
                "required": False,
            },
        },
    ),
}


def create_module_argument_spec() -> dict:
    module_args = connection_params_argument_spec()
    module_args["disks"] = {
        "type": "list",
        "elements": "str",
    }
    module_args["vm"] = {
        "type": "str",
        "required": True,
    }
    module_args["vm_home"] = {
        "type": "bool",
    }
    module_args["state"] = {
        "type": "str",
        "choices": ["check"],
        "required": True,
    }
    return module_args


def main():
    module = AnsibleModule(
        argument_spec=create_module_argument_spec(),
        supports_check_mode=True,
    )

    crud_module = VmwareRestCrudModuleBase(
        module=module,
        moid_parameter_hints=MOID_PARAMETER_HINTS,
        get_operation_config=GET_OPERATION,
        action_operations=ACTION_OPERATIONS,
    )

    try:
        if module.params["state"] in ACTION_OPERATIONS:
            result = crud_module.perform_action()
        else:
            module.fail_json(
                msg="Unsupported state: {0}".format(module.params["state"])
            )
    except VmwareModuleError as e:
        module.fail_json(**e.to_module_fail_json_output())

    module.exit_json(**result)


if __name__ == "__main__":
    main()
