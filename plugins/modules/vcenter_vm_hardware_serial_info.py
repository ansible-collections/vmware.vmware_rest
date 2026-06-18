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
module: vcenter_vm_hardware_serial_info
short_description: Get virtual serial port information for a virtual machine.
description:
  - Returns information about virtual serial ports belonging to a virtual machine.
  - When I(port) is specified, returns detailed information about that serial port.
  - When I(label) is specified, returns information for serial ports with a matching
    device label.
  - When I(port) and I(label) are omitted, lists all serial ports and returns detailed
    information for each.
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
  port:
    description:
      - Identifier of the virtual serial port to retrieve.
      - Must be an identifier (MOID) for a
        C(com.vmware.vcenter.vm.hardware.SerialPort) resource.
    type: str
  label:
    description:
      - Device label used to filter serial ports.
      - When a single serial port matches, the module also returns its MOID in I(id).
    type: str
version_added: 4.11.0
requirements: []
notes:
  - Generated from vSphere API spec 9.1.0.
  - Has support for vSphere API 7.0.3.
  - Has support for vSphere API 8.0.2.
"""

EXAMPLES = r"""
- name: List serial ports for a virtual machine
  vmware.vmware_rest.vcenter_vm_hardware_serial_info:
    vm: vm-1001
  register: vm_serial_ports

- name: Get information about a specific serial port
  vmware.vmware_rest.vcenter_vm_hardware_serial_info:
    vm: vm-1001
    port: "5000"
  register: vm_serial_port_info

- name: Get information about a serial port by label
  vmware.vmware_rest.vcenter_vm_hardware_serial_info:
    vm: vm-1001
    label: Serial port 1
  register: vm_serial_port_by_label
"""

RETURN = r"""
id:
  description:
    - Identifier of the virtual serial port.
    - Must be an identifier (MOID) for a
      C(com.vmware.vcenter.vm.hardware.SerialPort) resource.
    - Returned when I(label) matches exactly one serial port.
  returned: When I(label) matches exactly one serial port
  type: str
  sample: "5000"

value:
  description:
    - Virtual serial port information.
    - Returns a list of serial port dictionaries when listing or filtering serial ports.
    - Returns a list containing a single serial port dictionary when I(port) is
      specified.
  returned: On success
  type: list
  elements: dict
  sample:
    - port: "5000"
      label: Serial port 1
      state: NOT_CONNECTED
      start_connected: false
      allow_guest_control: true
      yield_on_poll: false
      backing:
        type: HOST_DEVICE
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.vmware.vmware_rest.plugins.module_utils._argument_spec import (
    connection_params_argument_spec,
)
from ansible_collections.vmware.vmware_rest.plugins.module_utils._module_base import (
    VmwareRestInfoModuleBase,
)

LIST_PATH = "/vcenter/vm/{vm}/hardware/serial"
ITEM_PATH = "/vcenter/vm/{vm}/hardware/serial/{port}"


class VmwareRestInfoModule(VmwareRestInfoModuleBase):
    PAYLOAD_FORMAT = {
        "list": {"query": {}, "body": {}, "path": {"vm": "vm"}},
        "get": {"query": {}, "body": {}, "path": {"vm": "vm", "port": "port"}},
    }

    def _get_port(self, port_id):
        path = self.build_path(ITEM_PATH, {"port": port_id})
        response = self.client.get(path)
        if response.status == 404:
            return None

        info = response.json
        if "port" not in info:
            info["port"] = port_id
        return info

    def get_info(self):
        port = self.params.get("port")
        if port:
            info = self._get_port(port)
            if info is None:
                return [], None
            return [info], port

        list_path = self.build_path(LIST_PATH)
        summaries = self.fetch_list(list_path, self.PAYLOAD_FORMAT["list"])
        result = []
        label = self.params.get("label")

        for summary in summaries:
            port_id = summary.get("port")
            if not port_id:
                continue
            info = self._get_port(port_id)
            if info is None:
                continue
            if label is not None and info.get("label") != label:
                continue
            result.append(info)

        matched_id = None
        if label is not None and len(result) == 1:
            matched_id = result[0].get("port")

        return result, matched_id


def main():
    module_args = connection_params_argument_spec()
    module_args["vm"] = {"type": "str", "required": True}
    module_args["port"] = {"type": "str"}
    module_args["label"] = {"type": "str"}

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
    )

    info_module = VmwareRestInfoModule(module)
    result, port_id = info_module.get_info()

    exit_kwargs = {"value": result}
    if port_id:
        exit_kwargs["id"] = port_id
    module.exit_json(**exit_kwargs)


if __name__ == "__main__":
    main()
