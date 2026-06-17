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
module: vcenter_vm_hardware_adapter_scsi_info
short_description: Retrieves information about virtual SCSI adapters on a virtual machine.
description:
  - Retrieves information about virtual SCSI adapters on a virtual machine.
  - When I(adapter) is set, returns information about that virtual SCSI adapter.
  - When I(adapter) is not set, lists all virtual SCSI adapters on the virtual
    machine and returns detailed information for each.
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
  adapter:
    description:
      - Virtual SCSI adapter identifier.
      - Must be an identifier (MOID) for a C(ScsiAdapter) resource.
    type: str
version_added: 4.11.0
requirements: []
notes:
  - Generated from vSphere API spec 9.1.0.
  - Has support for vSphere API 7.0.3.
  - Has support for vSphere API 8.0.2.
"""

EXAMPLES = r"""
- name: List virtual SCSI adapters on a virtual machine
  vmware.vmware_rest.vcenter_vm_hardware_adapter_scsi_info:
    vm: vm-42
  register: scsi_adapters

- name: Get a specific virtual SCSI adapter
  vmware.vmware_rest.vcenter_vm_hardware_adapter_scsi_info:
    vm: vm-42
    adapter: scsi-2000
  register: scsi_adapter_info
"""

RETURN = r"""
value:
  description:
    - List of virtual SCSI adapter information objects.
  returned: On success
  type: list
  elements: dict
  sample:
    - id: scsi-2000
      label: SCSI controller 0
      type: PVSCSI
      sharing: NONE
      scsi:
        bus: 0
        unit: 7
      pci_slot_number: 16
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.vmware.vmware_rest.plugins.module_utils._argument_spec import (
    connection_params_argument_spec,
)
from ansible_collections.vmware.vmware_rest.plugins.module_utils._module_base import (
    VmwareRestInfoModuleBase,
)

LIST_PATH = "/vcenter/vm/{vm}/hardware/adapter/scsi"
ITEM_PATH = "/vcenter/vm/{vm}/hardware/adapter/scsi/{adapter}"


class VmwareRestInfoModule(VmwareRestInfoModuleBase):
    PAYLOAD_FORMAT = {
        "get": {"query": {}, "body": {}, "path": {"adapter": "adapter"}},
        "list": {"query": {}, "body": {}, "path": {}},
    }

    def get_info(self):
        adapter = self.params.get("adapter")
        if adapter:
            info = self._get_adapter(adapter)
            if not info:
                return []
            return [info]

        summaries = self._list_adapters()
        result = []
        for summary in summaries:
            adapter_id = summary.get("adapter")
            if not adapter_id:
                continue
            info = self._get_adapter(adapter_id)
            if info:
                result.append(info)
        return result

    def _list_adapters(self):
        list_path = self.build_path(LIST_PATH)
        return self.fetch_list(list_path, self.PAYLOAD_FORMAT["list"])

    def _get_adapter(self, adapter_id):
        path = self.build_path(ITEM_PATH, {"adapter": adapter_id})
        response = self.client.get(path)
        if response.status == 404:
            return None

        info = response.json
        if "id" not in info:
            info["id"] = adapter_id
        return info


def main():
    module_args = connection_params_argument_spec()
    module_args["vm"] = {"type": "str", "required": True}
    module_args["adapter"] = {"type": "str"}

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
    )

    info_module = VmwareRestInfoModule(module)
    result = info_module.get_info()
    module.exit_json(value=result)


if __name__ == "__main__":
    main()
