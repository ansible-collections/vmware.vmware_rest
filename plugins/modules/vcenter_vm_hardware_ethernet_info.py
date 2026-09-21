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
module: vcenter_vm_hardware_ethernet_info
short_description: Gather information about the virtual Ethernet adapters of a virtual machine.
description:
  - Gather information about the virtual Ethernet (network) adapters attached to a virtual machine.
  - When O(nic) is provided, returns the detailed configuration of that single adapter.
  - When O(nic) is omitted, returns a list of all Ethernet adapters configured on the virtual machine.
  - Reported details include the adapter emulation type, MAC address, connection state, and network backing.

author:
  - Ansible Eco Content Team (@eco-ansible-content)

extends_documentation_fragment:
  - vmware.vmware_rest.connection_params

options:
  nic:
    description:
      - Identifier of the virtual Ethernet adapter to gather information about.
      - Must be the MOID (managed object identifier) of a C(Nic) resource on the virtual machine.
      - When omitted, information about all Ethernet adapters on the virtual machine is returned.
    type: str
    required: false
  vm:
    description:
      - Identifier of the virtual machine whose Ethernet adapters are queried.
      - Must be the MOID (managed object identifier) of a C(Vm) resource.
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
- name: List all Ethernet adapters on a virtual machine
  vmware.vmware_rest.vcenter_vm_hardware_ethernet_info:
    vm: vm-1001
  register: all_nics

- name: Get details about a specific Ethernet adapter
  vmware.vmware_rest.vcenter_vm_hardware_ethernet_info:
    vm: vm-1001
    nic: "4000"
  register: my_nic
"""

RETURN = r"""
id:
  description: MOID of the queried Ethernet adapter.
  returned: When only one resource, with a MOID, was queried.
  sample: "4000"
  type: str
value:
  description:
    - Raw output from the API response.
    - This output is maintained for consistency with version 4.x and earlier of this collection.
      It is recommended to switch to the info return key for a more consistent and documented output.
  returned: On success.
  sample:
    label: Network adapter 1
    type: VMXNET3
    mac_type: ASSIGNED
    mac_address: "00:50:56:8a:1b:2c"
    pci_slot_number: 160
    state: CONNECTED
    start_connected: true
    allow_guest_control: true
    wake_on_lan_enabled: false
    backing:
      type: STANDARD_PORTGROUP
      network: network-1002
  type: raw
info:
  description: A list of Ethernet adapters configured on the virtual machine.
  returned: On success.
  sample:
    - nic: "4000"
      label: Network adapter 1
      type: VMXNET3
      mac_address: "00:50:56:8a:1b:2c"
      state: CONNECTED
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

MOID_PARAMETER_HINTS = ["vm", "nic"]

LIST_ENDPOINT = "/vcenter/vm/{vm}/hardware/ethernet"
ITEM_ENDPOINT = "/vcenter/vm/{vm}/hardware/ethernet/{nic}"


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
    module_args["nic"] = {
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
