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
module: vcenter_vm_hardware_cdrom_info
short_description: Retrieves virtual CD-ROM device information for a virtual machine.
description:
  - Returns information about virtual CD-ROM devices belonging to a virtual machine.
  - When I(cdrom) is specified, returns detailed information about that device.
  - When I(cdrom) is omitted, lists all virtual CD-ROM devices and returns detailed
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
  cdrom:
    description:
      - Identifier of the virtual CD-ROM device to retrieve.
      - Must be an identifier (MOID) for a
        C(com.vmware.vcenter.vm.hardware.Cdrom) resource.
    type: str
version_added: 4.11.0
requirements: []
notes:
  - Generated from vSphere API spec 9.1.0.
  - Has support for vSphere API 7.0.3.
  - Has support for vSphere API 8.0.2.
"""

EXAMPLES = r"""
- name: List virtual CD-ROM devices for a virtual machine
  vmware.vmware_rest.vcenter_vm_hardware_cdrom_info:
    vm: vm-1001
  register: vm_cdrom_devices

- name: Get information about a specific virtual CD-ROM device
  vmware.vmware_rest.vcenter_vm_hardware_cdrom_info:
    vm: vm-1001
    cdrom: "3000"
  register: vm_cdrom_info
"""

RETURN = r"""
value:
  description:
    - Virtual CD-ROM device information.
    - Returns a list of device dictionaries when I(cdrom) is omitted.
    - Returns a single device dictionary when I(cdrom) is specified.
  returned: On success
  type: raw
  sample:
    cdrom: "3000"
    type: SATA
    label: CD/DVD drive 1
    state: NOT_CONNECTED
    start_connected: false
    allow_guest_control: true
    backing:
      type: CLIENT_DEVICE
  contains:
    cdrom:
      description:
        - Virtual CD-ROM device identifier (MOID).
      type: str
      sample: "3000"
    type:
      description:
        - Host bus adapter type to which the device is attached.
      type: str
      choices:
        - IDE
        - SATA
      sample: SATA
    label:
      description:
        - Device label.
      type: str
      sample: CD/DVD drive 1
    ide:
      description:
        - Address of the device on a virtual IDE adapter.
      type: dict
    sata:
      description:
        - Address of the device on a virtual SATA adapter.
      type: dict
    backing:
      description:
        - Physical resource backing for the virtual CD-ROM device.
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

LIST_PATH = "/vcenter/vm/{vm}/hardware/cdrom"
ITEM_PATH = "/vcenter/vm/{vm}/hardware/cdrom/{cdrom}"


class VmwareRestInfoModule(VmwareRestInfoModuleBase):
    PAYLOAD_FORMAT = {
        "list": {"query": {}, "body": {}, "path": {"vm": "vm"}},
        "get": {"query": {}, "body": {}, "path": {"vm": "vm", "cdrom": "cdrom"}},
    }

    def _get_cdrom(self, cdrom_id):
        path = self.build_path(ITEM_PATH, {"cdrom": cdrom_id})
        response = self.client.get(path)
        if response.status == 404:
            return {}
        info = response.json
        if "cdrom" not in info:
            info["cdrom"] = cdrom_id
        return info

    def get_info(self):
        cdrom = self.params.get("cdrom")
        if cdrom:
            return self._get_cdrom(cdrom)

        list_path = self.build_path(LIST_PATH)
        summaries = self.fetch_list(list_path, self.PAYLOAD_FORMAT["list"])
        result = []
        for summary in summaries:
            cdrom_id = summary.get("cdrom")
            if cdrom_id:
                result.append(self._get_cdrom(cdrom_id))
        return result


def main():
    module_args = connection_params_argument_spec()
    module_args["vm"] = {"type": "str", "required": True}
    module_args["cdrom"] = {"type": "str"}

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
    )

    info_module = VmwareRestInfoModule(module)
    result = info_module.get_info()
    module.exit_json(value=result)


if __name__ == "__main__":
    main()
