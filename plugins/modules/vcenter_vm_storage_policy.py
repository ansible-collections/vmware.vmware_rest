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
module: vcenter_vm_storage_policy
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
      - Use C(present) to create or update the resource.
    type: str
    default: present
    choices:
      - present
  vm:
    description:
      - Identifier of the vm to manage.
      - Must be an identifier (MOID) for a C(Vm) resource.
    type: str
    required: true
  vm_home:
    description:
      - Storage policy to be used when reconfiguring the virtual machine home.
      - This property was added in __vSphere API 6.7__.
      - If missing or 'null' the current storage policy is retained.
    type: dict
    required: false
    suboptions:
      type:
        description:
          - Policy type to be used while performing update operation on the virtual machine home's directory.
          - USE_SPECIFIED_POLICY - Use the specified policy (see *Vcenter.Vm.Storage.Policy.VmHomePolicySpec.policy*).
          - USE_DEFAULT_POLICY - Use the default storage policy of the datastore.
          - For more information see *Vcenter.Vm.Storage.Policy.VmHomePolicySpec.PolicyType*.
          - This property was added in __vSphere API 6.7__.
        type: str
        required: true
        choices:
          - USE_SPECIFIED_POLICY
          - USE_DEFAULT_POLICY
      policy:
        description:
          - Storage Policy identification.
          - This property was added in __vSphere API 6.7__.
          - This property is optional and it is only relevant when the value of type is *Vcenter.Vm.Storage.Policy.VmHomePolicySpec.PolicyType.USE_SPECIFIED_POLICY*.
          - When clients pass a value of this schema as a parameter, the property must be an identifier (MOID) for the resource type 'com.vmware.vcenter.StoragePolicy'. When operations return a value of this schema as a response, the property will be an identifier (MOID) for the resource type 'com.vmware.vcenter.StoragePolicy'.
        type: str
        required: false
  disks:
    description:
      - Storage policy or policies to be used when reconfiguring virtual machine disk.
      - This property was added in __vSphere API 6.7__.
      - If missing or 'null' the current storage policy is retained.
      - When clients pass a value of this schema as a parameter, the key in the property map must be an identifier (MOID) for the resource type 'com.vmware.vcenter.vm.hardware.Disk'. When operations return a value of this schema as a response, the key in the property map will be an identifier (MOID) for the resource type 'com.vmware.vcenter.vm.hardware.Disk'.
    type: dict
    required: false

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
ITEM_ENDPOINT = "/vcenter/vm/{vm}/storage/policy"


GET_OPERATION = OperationConfig(
    name="get",
    uri=ITEM_ENDPOINT,
    http_method="GET",
)

UPDATE_OPERATION = OperationConfig(
    name="update",
    uri=ITEM_ENDPOINT,
    http_method="PATCH",
    body_spec={
        "vm_home": {
            "required": False,
            "subspec": {
                "type": {
                    "required": False,
                },
                "policy": {
                    "required": False,
                },
            },
        },
        "disks": {
            "required": False,
        },
    },
)


def create_module_argument_spec() -> dict:
    module_args = connection_params_argument_spec()
    module_args["disks"] = {
        "type": "dict",
    }
    module_args["vm"] = {
        "type": "str",
        "required": True,
    }
    module_args["vm_home"] = {
        "type": "dict",
        "options": {
            "type": {
                "type": "str",
                "choices": ['USE_SPECIFIED_POLICY', 'USE_DEFAULT_POLICY'],
                "required": True,
            },
            "policy": {
                "type": "str",
            },
        },
    }
    module_args["state"] = {
        "type": "str",
        "choices": ['present'],
        "default": "present",
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
        update_operation_config=UPDATE_OPERATION,
    )

    try:
        if module.params["state"] == "present":
            result = crud_module.ensure_present()
        else:
            module.fail_json(msg="Unsupported state: {0}".format(module.params["state"]))
    except VmwareModuleError as e:
        module.fail_json(**e.to_module_fail_json_output())

    module.exit_json(**result)


if __name__ == "__main__":
    main()
