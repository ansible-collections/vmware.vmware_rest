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
short_description: Retrieves virtual SATA adapter information for a virtual machine.
description:
  - Returns information about virtual SATA adapters belonging to a virtual machine in vCenter.
  - When I(adapter) is specified, returns detailed information for that adapter only.
  - When I(adapter) is omitted, returns a summary list of all virtual SATA adapters on the virtual machine.
author:
  - Ansible Eco Content Team (@eco-ansible-content)
extends_documentation_fragment:
  - vmware.vmware_rest.connection_params
options:
  vm:
    description:
      - Identifier of the virtual machine.
      - Must be an identifier (MOID) for a C(VirtualMachine) resource.
    type: str
    required: true
  adapter:
    description:
      - Identifier of the virtual SATA adapter to retrieve.
      - Must be an identifier (MOID) for a C(com.vmware.vcenter.vm.hardware.SataAdapter) resource.
      - When specified, only that adapter is returned.
    type: str
version_added: 4.11.0
requirements: []
notes:
  - Generated from vSphere API spec 9.1.0.
  - Has support for vSphere API 7.0.3.
  - Has support for vSphere API 8.0.2.
"""

EXAMPLES = r"""
- name: List virtual SATA adapters for a virtual machine
  vmware.vmware_rest.vcenter_vm_hardware_adapter_sata_info:
    vm: vm-1001
  register: sata_adapters

- name: Get a specific virtual SATA adapter
  vmware.vmware_rest.vcenter_vm_hardware_adapter_sata_info:
    vm: vm-1001
    adapter: sata-15000
  register: sata_adapter_info
"""

RETURN = r"""
id:
  description:
    - Identifier of the virtual SATA adapter.
    - Must be an identifier (MOID) for a C(com.vmware.vcenter.vm.hardware.SataAdapter) resource.
    - Returned when I(adapter) is specified.
  returned: When I(adapter) is specified
  type: str
  sample: sata-15000
value:
  description:
    - Virtual SATA adapter information.
    - Returns a list of adapter summary dictionaries when I(adapter) is omitted.
    - Returns a single adapter dictionary when I(adapter) is specified.
  returned: On success
  type: raw
  sample:
    - adapter: sata-15000
  contains:
    adapter:
      description:
        - Identifier of the virtual SATA adapter.
        - Must be an identifier (MOID) for a C(com.vmware.vcenter.vm.hardware.SataAdapter) resource.
      type: str
      sample: sata-15000
    label:
      description:
        - Device label.
      type: str
      sample: SATA controller 0
    type:
      description:
        - Adapter type.
      type: str
      choices:
        - AHCI
      sample: AHCI
    bus:
      description:
        - SATA bus number.
      type: int
      sample: 0
    pci_slot_number:
      description:
        - Address of the SATA adapter on the PCI bus.
        - May be omitted when the virtual machine has never been powered on since the adapter was created.
      type: int
      sample: 34
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.vmware.vmware_rest.plugins.module_utils._argument_spec import (
    connection_params_argument_spec,
)
from ansible_collections.vmware.vmware_rest.plugins.module_utils._errors import (
    UnexpectedAPIResponse,
)
from ansible_collections.vmware.vmware_rest.plugins.module_utils._module_base import (
    VmwareRestInfoModuleBase,
    normalize_list_response,
)

LIST_PATH = "/vcenter/vm/{vm}/hardware/adapter/sata"
ADAPTER_PATH = "/vcenter/vm/{vm}/hardware/adapter/sata/{adapter}"


class VmwareRestInfoModule(VmwareRestInfoModuleBase):
    PAYLOAD_FORMAT = {
        "list": {"query": {}, "body": {}, "path": {"vm": "vm"}},
        "get": {"query": {}, "body": {}, "path": {"vm": "vm", "adapter": "adapter"}},
    }

    def _get_adapter(self, adapter, fail_if_missing=False):
        path = self.build_path(ADAPTER_PATH, {"adapter": adapter})
        response = self.client.get(path)
        if response.status == 404:
            if fail_if_missing:
                self.client.error_handler.handle_request_error(
                    exception=UnexpectedAPIResponse(response.status, response.data),
                    method="GET",
                    path=path,
                    request_kwargs={},
                )
            return None
        return response.json

    def get_info(self):
        adapter = self.params.get("adapter")
        if adapter:
            return self._get_adapter(adapter, fail_if_missing=True)

        path = self.build_path(LIST_PATH)
        response = self.client.get(path)
        if response.status == 404:
            return []
        return normalize_list_response(response.json)


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
    exit_kwargs = {"value": result}
    if module.params.get("adapter"):
        exit_kwargs["id"] = module.params["adapter"]
    module.exit_json(**exit_kwargs)


if __name__ == "__main__":
    main()
