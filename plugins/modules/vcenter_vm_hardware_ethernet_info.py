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
module: vcenter_vm_hardware_ethernet_info
short_description: Retrieves virtual Ethernet adapter information for a virtual machine.
description:
  - Returns information about virtual Ethernet adapters belonging to a virtual machine.
  - When I(nic) is specified, returns information for that virtual Ethernet adapter only.
  - When I(label) is specified, returns information for virtual Ethernet adapters with a
    matching device label.
  - When I(nic) and I(label) are omitted, lists all virtual Ethernet adapters and returns
    detailed information for each.
author:
  - Ansible Eco Content Team (@eco-ansible-content)
extends_documentation_fragment:
  - vmware.vmware_rest.connection_params
options:
  vm:
    description:
      - Virtual machine identifier.
      - Must be an identifier (MOID) for a C(VirtualMachine) resource.
    type: str
    required: true
  nic:
    description:
      - Identifier of the virtual Ethernet adapter to retrieve.
      - Must be an identifier (MOID) for a
        C(com.vmware.vcenter.vm.hardware.Ethernet) resource.
    type: str
  label:
    description:
      - Device label used to filter virtual Ethernet adapters.
      - When a single virtual Ethernet adapter matches, the module also returns its MOID in
        I(id).
    type: str
version_added: 4.11.0
requirements: []
notes:
  - Generated from vSphere API spec 9.1.0.
  - Has support for vSphere API 7.0.3.
  - Has support for vSphere API 8.0.2.
"""

EXAMPLES = r"""
- name: List virtual Ethernet adapters for a virtual machine
  vmware.vmware_rest.vcenter_vm_hardware_ethernet_info:
    vm: vm-1001
  register: vm_nics

- name: Get information about a specific virtual Ethernet adapter
  vmware.vmware_rest.vcenter_vm_hardware_ethernet_info:
    vm: vm-1001
    nic: "4000"
  register: vm_nic_info

- name: Get information about a virtual Ethernet adapter by label
  vmware.vmware_rest.vcenter_vm_hardware_ethernet_info:
    vm: vm-1001
    label: Network adapter 1
  register: vm_nic_by_label
"""

RETURN = r"""
id:
  description:
    - Identifier of the virtual Ethernet adapter.
    - Must be an identifier (MOID) for a
      C(com.vmware.vcenter.vm.hardware.Ethernet) resource.
    - Returned when I(label) matches exactly one virtual Ethernet adapter.
  returned: When I(label) matches exactly one virtual Ethernet adapter
  type: str
  sample: "4000"

value:
  description:
    - Virtual Ethernet adapter information.
    - Returns a list of adapter dictionaries when listing or filtering virtual Ethernet
      adapters.
    - Returns a list containing a single adapter dictionary when I(nic) is specified.
  returned: On success
  type: list
  elements: dict
  sample:
    - nic: "4000"
      label: Network adapter 1
      type: VMXNET3
      mac_type: GENERATED
      start_connected: true
      state: NOT_CONNECTED
      backing:
        type: DISTRIBUTED_PORTGROUP
        network: network-1001
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.vmware.vmware_rest.plugins.module_utils._argument_spec import (
    connection_params_argument_spec,
)
from ansible_collections.vmware.vmware_rest.plugins.module_utils._module_base import (
    VmwareRestInfoModuleBase,
)

LIST_PATH = "/vcenter/vm/{vm}/hardware/ethernet"
ITEM_PATH = "/vcenter/vm/{vm}/hardware/ethernet/{nic}"


class VmwareRestInfoModule(VmwareRestInfoModuleBase):
    PAYLOAD_FORMAT = {
        "list": {"query": {}, "body": {}, "path": {"vm": "vm"}},
        "get": {"query": {}, "body": {}, "path": {"vm": "vm", "nic": "nic"}},
    }

    def _get_nic(self, nic_id):
        path = self.build_path(ITEM_PATH, {"nic": nic_id})
        response = self.client.get(path)
        if response.status == 404:
            return None

        info = response.json
        if "nic" not in info:
            info["nic"] = nic_id
        return info

    def get_info(self):
        nic = self.params.get("nic")
        if nic:
            info = self._get_nic(nic)
            if info is None:
                return [], None
            return [info], nic

        list_path = self.build_path(LIST_PATH)
        summaries = self.fetch_list(list_path, self.PAYLOAD_FORMAT["list"])
        result = []
        label = self.params.get("label")

        for summary in summaries:
            nic_id = summary.get("nic")
            if not nic_id:
                continue
            info = self._get_nic(nic_id)
            if info is None:
                continue
            if label is not None and info.get("label") != label:
                continue
            result.append(info)

        matched_id = None
        if label is not None and len(result) == 1:
            matched_id = result[0].get("nic")

        return result, matched_id


def main():
    module_args = connection_params_argument_spec()
    module_args["vm"] = {"type": "str", "required": True}
    module_args["nic"] = {"type": "str"}
    module_args["label"] = {"type": "str"}

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
    )

    info_module = VmwareRestInfoModule(module)
    result, nic_id = info_module.get_info()

    exit_kwargs = {"value": result}
    if nic_id:
        exit_kwargs["id"] = nic_id
    module.exit_json(**exit_kwargs)


if __name__ == "__main__":
    main()
