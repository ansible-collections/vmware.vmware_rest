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
short_description: PLACEHOLDER
description:
  - PLACEHOLDER

author:
  - Ansible Eco Content Team (@eco-ansible-content)

extends_documentation_fragment:
  - vmware.vmware_rest.connection_params

options:
  state:
    description:
      - The desired state of the resource.
      - Use C(check) to perform the check action.
      - Only options C(present) and C(absent) support idempotence.
    type: str
    required: true
    choices:
      - check
  vm:
    description:
      - Identifier of the vm to manage.
      - Must be an identifier (MOID) for a C(Vm) resource.
    type: str
    required: true
  vm_home:
    description:
      - Invoke compliance check on the virtual machine home directory if set to true.
      - This property was added in __vSphere API 6.7__.
    type: bool
    required: false
  disks:
    description:
      - Identifiers of the virtual machine's virtual disks for which compliance should be checked.
      - This property was added in __vSphere API 6.7__.
      - If missing or 'null' or empty, compliance check is invoked on all the associated disks.
      - When clients pass a value of this schema as a parameter, the property must contain identifiers (MOIDs) for the resource type 'com.vmware.vcenter.vm.hardware.Disk'. When operations return a value of this schema as a response, the property will contain identifiers (MOIDs) for the resource type 'com.vmware.vcenter.vm.hardware.Disk'.
    type: list
    required: false
    elements: str

version_added: 5.0.0

requirements: []

notes:
  - Generated from vSphere API spec 9.1.0.
"""

EXAMPLES = r"""
"""

RETURN = r"""
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
