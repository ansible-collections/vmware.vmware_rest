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
module: vcenter_vm_hardware_adapter_sata_info
short_description: Gather information about the virtual SATA adapters of a virtual machine.
description:
  - Return information about the virtual SATA adapters attached to a virtual machine.
  - When O(adapter) is provided, detailed information about that single SATA adapter is returned, including its type, label, and SATA bus number.
  - When O(adapter) is omitted, a list of all SATA adapters configured on the virtual machine is returned.

author:
  - Ansible Eco Content Team (@eco-ansible-content)

extends_documentation_fragment:
  - vmware.vmware_rest.connection_params

options:
  adapter:
    description:
      - Identifier of the SATA adapter to query.
      - When set, detailed information about only this adapter is returned.
      - When omitted, all SATA adapters on the virtual machine are returned.
      - Must be an identifier (MOID) for a C(SataAdapter) resource.
    type: str
    required: false
  vm:
    description:
      - Identifier of the virtual machine whose SATA adapters should be queried.
      - Must be an identifier (MOID) for a C(Vm) resource.
    type: str
    required: true

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

- name: List all SATA adapters of a virtual machine
  vmware.vmware_rest.vcenter_vm_hardware_adapter_sata_info:
    vm: '{{ search_result.value[0].vm }}'
  register: sata_adapters

- name: Gather detailed information about a single SATA adapter
  vmware.vmware_rest.vcenter_vm_hardware_adapter_sata_info:
    vm: '{{ search_result.value[0].vm }}'
    adapter: '{{ sata_adapters.info[0].adapter }}'
  register: sata_adapter_detail
"""

RETURN = r"""
value:
  description:
    - Raw output from the API response.
    - This output is maintained for consistency with version 4.x and earlier of this collection.
      It is recommended to switch to the info return key for a more consistent and documented output.
  returned: On success.
  sample:
    bus: 0
    label: SATA controller 0
    pci_slot_number: 32
    type: AHCI
  type: raw
info:
  description: A list of detailed information about the virtual SATA adapters.
  returned: On success.
  sample:
    - bus: 0
      label: SATA controller 0
      pci_slot_number: 32
      type: AHCI
  type: list
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

MOID_PARAMETER_HINTS = ["vm", "adapter"]

LIST_ENDPOINT = "/vcenter/vm/{vm}/hardware/adapter/sata"
ITEM_ENDPOINT = "/vcenter/vm/{vm}/hardware/adapter/sata/{adapter}"


LIST_OPERATION = OperationConfig(
    name="list",
    uri=LIST_ENDPOINT,
    http_method="GET",
)

GET_OPERATION = OperationConfig(
    name="get",
    uri=ITEM_ENDPOINT,
    http_method="GET",
)


def create_module_argument_spec() -> dict:
    module_args = connection_params_argument_spec()
    module_args["adapter"] = {
        "type": "str",
    }
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
        list_operation_config=LIST_OPERATION,
    )
    try:
        result = info_module.get_resource_info()
    except VmwareModuleError as e:
        module.fail_json(**e.to_module_fail_json_output())
    module.exit_json(**result)


if __name__ == "__main__":
    main()
