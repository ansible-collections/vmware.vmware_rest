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
short_description: Manage the storage policies associated with a virtual machine.
description:
  - Update the storage policy configuration of a virtual machine's home directory and/or its virtual hard disks.
  - Assign a specific storage policy, or fall back to the default storage policy of the datastore.
  - Only entities that are supplied are reconfigured; entities left unset retain their current storage policy.

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
      - The storage policy to apply to the virtual machine's home directory.
      - If omitted, the current storage policy of the VM home directory is retained.
      - When this option is specified, the module can never be idempotent. A change will
        always be reported.
    type: dict
    required: false
    suboptions:
      type:
        description:
          - How to select the storage policy for the VM home directory.
          - Use C(USE_SPECIFIED_POLICY) to assign the storage policy given in I(vm_home.policy).
          - Use C(USE_DEFAULT_POLICY) to assign the default storage policy of the datastore.
        type: str
        required: true
        choices:
          - USE_SPECIFIED_POLICY
          - USE_DEFAULT_POLICY
      policy:
        description:
          - The storage policy to assign to the VM home directory.
          - Only used, and required, when I(vm_home.type) is C(USE_SPECIFIED_POLICY).
          - Must be an identifier (MOID) for the resource type C(com.vmware.vcenter.StoragePolicy).
        type: str
        required: false
  disks:
    description:
      - The storage policies to apply to the virtual machine's virtual disks.
      - A map keyed by the disk MOID, where each value is a storage policy specification for that disk.
      - Each key must be an identifier (MOID) for the resource type C(com.vmware.vcenter.vm.hardware.Disk).
      - Any disk that is not listed retains its current storage policy.
      - When this option is specified, the module can never be idempotent. A change will
        always be reported.
    type: dict
    required: false

version_added: 5.0.0

requirements: []

notes:
  - Generated from vSphere API spec 9.1.0.
  - Compatible with vSphere API 7.0.3.
  - Compatible with vSphere API 8.0.2.
"""

EXAMPLES = r"""
- name: Look up the VM called test_vm1 in the inventory
  register: search_result
  vmware.vmware_rest.vcenter_vm_info:
    filter_names:
      - test_vm1

- name: Assign a specific storage policy to the VM home directory
  vmware.vmware_rest.vcenter_vm_storage_policy:
    vm: '{{ search_result.value[0].vm }}'
    vm_home:
      type: USE_SPECIFIED_POLICY
      policy: aa6d5a82-1c88-45da-85d3-3d74b91a5bad
    state: present

- name: Assign storage policies to the VM home directory and a virtual disk
  vmware.vmware_rest.vcenter_vm_storage_policy:
    vm: '{{ search_result.value[0].vm }}'
    vm_home:
      type: USE_DEFAULT_POLICY
    disks:
      '2000':
        type: USE_SPECIFIED_POLICY
        policy: aa6d5a82-1c88-45da-85d3-3d74b91a5bad
    state: present
"""

RETURN = r"""
id:
  description: MOID of the managed virtual machine.
  returned: When state is present, or when state is set to a supported action.
  sample: vm-1009
  type: str
value:
  description: The raw API response body from the vCenter storage policy update operation.
  returned: On success
  type: raw
  sample:
    vm_home: aa6d5a82-1c88-45da-85d3-3d74b91a5bad
    disks:
      '2000': aa6d5a82-1c88-45da-85d3-3d74b91a5bad
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
                "choices": ["USE_SPECIFIED_POLICY", "USE_DEFAULT_POLICY"],
                "required": True,
            },
            "policy": {
                "type": "str",
            },
        },
    }
    module_args["state"] = {
        "type": "str",
        "choices": ["present"],
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
            module.fail_json(
                msg="Unsupported state: {0}".format(module.params["state"])
            )
    except VmwareModuleError as e:
        module.fail_json(**e.to_module_fail_json_output())

    module.exit_json(**result)


if __name__ == "__main__":
    main()
