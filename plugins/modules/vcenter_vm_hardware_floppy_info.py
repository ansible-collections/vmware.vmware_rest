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
module: vcenter_vm_hardware_floppy_info
short_description: Retrieves virtual floppy drive information for a virtual machine.
description:
  - Returns information about virtual floppy drives belonging to a virtual machine.
  - When I(floppy) is specified, returns detailed information about that device.
  - When I(floppy) is omitted, lists all virtual floppy drives and returns detailed
    information for each.
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
  floppy:
    description:
      - Identifier of the virtual floppy drive to retrieve.
      - Must be an identifier (MOID) for a
        C(com.vmware.vcenter.vm.hardware.Floppy) resource.
    type: str
version_added: 4.11.0
requirements: []
notes:
  - Generated from vSphere API spec 9.1.0.
  - Has support for vSphere API 7.0.3.
  - Has support for vSphere API 8.0.2.
"""

EXAMPLES = r"""
- name: List virtual floppy drives for a virtual machine
  vmware.vmware_rest.vcenter_vm_hardware_floppy_info:
    vm: vm-1001
  register: vm_floppy_devices

- name: Get information about a specific virtual floppy drive
  vmware.vmware_rest.vcenter_vm_hardware_floppy_info:
    vm: vm-1001
    floppy: "4000"
  register: vm_floppy_info
"""

RETURN = r"""
value:
  description:
    - Virtual floppy drive information.
    - Returns a list of device dictionaries when I(floppy) is omitted.
    - Returns a single device dictionary when I(floppy) is specified.
  returned: On success
  type: raw
  sample:
    floppy: "4000"
    label: Floppy drive 1
    state: NOT_CONNECTED
    start_connected: false
    allow_guest_control: true
    backing:
      type: CLIENT_DEVICE
  contains:
    floppy:
      description:
        - Virtual floppy drive identifier (MOID).
      type: str
      sample: "4000"
    label:
      description:
        - Device label.
      type: str
      sample: Floppy drive 1
    backing:
      description:
        - Physical resource backing for the virtual floppy drive.
      type: dict
    state:
      description:
        - Connection status of the virtual device.
      type: str
      choices:
        - CONNECTED
        - RECOVERABLE_ERROR
        - UNRECOVERABLE_ERROR
        - NOT_CONNECTED
        - UNKNOWN
      sample: NOT_CONNECTED
    start_connected:
      description:
        - Whether the device should be connected when the virtual machine is powered on.
      type: bool
      sample: false
    allow_guest_control:
      description:
        - Whether the guest can connect and disconnect the device.
      type: bool
      sample: true
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.vmware.vmware_rest.plugins.module_utils._argument_spec import (
    connection_params_argument_spec,
)
from ansible_collections.vmware.vmware_rest.plugins.module_utils._module_base import (
    VmwareRestInfoModuleBase,
)

LIST_PATH = "/vcenter/vm/{vm}/hardware/floppy"
ITEM_PATH = "/vcenter/vm/{vm}/hardware/floppy/{floppy}"


class VmwareRestInfoModule(VmwareRestInfoModuleBase):
    PAYLOAD_FORMAT = {
        "list": {"query": {}, "body": {}, "path": {"vm": "vm"}},
        "get": {"query": {}, "body": {}, "path": {"vm": "vm", "floppy": "floppy"}},
    }

    def _get_floppy(self, floppy_id):
        path = self.build_path(ITEM_PATH, {"floppy": floppy_id})
        response = self.client.get(path)
        if response.status == 404:
            return {}
        info = response.json
        if "floppy" not in info:
            info["floppy"] = floppy_id
        return info

    def get_info(self):
        floppy = self.params.get("floppy")
        if floppy:
            return self._get_floppy(floppy)

        list_path = self.build_path(LIST_PATH)
        summaries = self.fetch_list(list_path, self.PAYLOAD_FORMAT["list"])
        result = []
        for summary in summaries:
            floppy_id = summary.get("floppy")
            if floppy_id:
                result.append(self._get_floppy(floppy_id))
        return result


def main():
    module_args = connection_params_argument_spec()
    module_args["vm"] = {"type": "str", "required": True}
    module_args["floppy"] = {"type": "str"}

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
    )

    info_module = VmwareRestInfoModule(module)
    result = info_module.get_info()
    module.exit_json(value=result)


if __name__ == "__main__":
    main()
