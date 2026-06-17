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
module: vcenter_vm_hardware_boot_device
short_description: Configures the boot device order for a virtual machine.
description:
  - Sets the ordered list of virtual devices used when booting a virtual machine.
  - The virtual machine checks devices in order until boot succeeds.
  - When the device list is empty, the virtual machine uses its default boot sequence.
  - Only one entry per device type is allowed, except for C(ETHERNET) adapters.
author:
  - Ansible Eco Content Team (@eco-ansible-content)
extends_documentation_fragment:
  - vmware.vmware_rest.connection_params
options:
  state:
    description:
      - The desired boot device configuration.
      - Use C(present) to set the boot device order.
      - Use C(absent) to reset the boot device order to the default sequence.
    type: str
    choices:
      - present
      - absent
    default: present
  vm:
    description:
      - Virtual machine identifier.
      - Must be an identifier (MOID) for a C(VirtualMachine) resource.
    type: str
    required: true
  devices:
    description:
      - Ordered list of boot devices.
      - Required when I(state=present).
    type: list
    elements: dict
    suboptions:
      type:
        description:
          - Virtual device type for this boot entry.
        type: str
        required: true
        choices:
          - CDROM
          - DISK
          - ETHERNET
          - FLOPPY
      nic:
        description:
          - Virtual Ethernet adapter to use for this boot entry.
          - Relevant only when I(type=ETHERNET).
          - Must be an identifier (MOID) for a
            C(com.vmware.vcenter.vm.hardware.Ethernet) resource.
        type: str
      disks:
        description:
          - Ordered list of virtual disks for this boot entry.
          - Relevant only when I(type=DISK).
          - Each element must be an identifier (MOID) for a
            C(com.vmware.vcenter.vm.hardware.Disk) resource.
        type: list
        elements: str
version_added: 4.11.0
requirements: []
notes:
  - Generated from vSphere API spec 9.1.0.
  - Has support for vSphere API 7.0.3.
  - Has support for vSphere API 8.0.2.
"""

EXAMPLES = r"""
- name: Set boot order to disk then CD-ROM
  vmware.vmware_rest.vcenter_vm_hardware_boot_device:
    vm: vm-1001
    devices:
      - type: DISK
        disks:
          - "2000"
      - type: CDROM

- name: Boot from a specific Ethernet adapter
  vmware.vmware_rest.vcenter_vm_hardware_boot_device:
    vm: vm-1001
    devices:
      - type: ETHERNET
        nic: "4000"
      - type: DISK
        disks:
          - "2000"

- name: Reset boot device order to the default sequence
  vmware.vmware_rest.vcenter_vm_hardware_boot_device:
    vm: vm-1001
    state: absent
"""

RETURN = r"""
value:
  description:
    - Ordered list of configured boot devices after the operation, or the current
      configuration when no change was made.
  returned: On success
  type: list
  elements: dict
  sample:
    - type: DISK
      disks:
        - "2000"
    - type: CDROM
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.vmware.vmware_rest.plugins.module_utils._argument_spec import (
    connection_params_argument_spec,
)
from ansible_collections.vmware.vmware_rest.plugins.module_utils._errors import (
    UnexpectedAPIResponse,
)
from ansible_collections.vmware.vmware_rest.plugins.module_utils._module_base import (
    VmwareRestCrudModuleBase,
    normalize_list_response,
    values_equal,
)

BOOT_DEVICE_PATH = "/vcenter/vm/{vm}/hardware/boot/device"

DEVICE_ENTRY_OPTIONS = {
    "type": {
        "type": "str",
        "required": True,
        "choices": ["CDROM", "DISK", "ETHERNET", "FLOPPY"],
    },
    "nic": {"type": "str"},
    "disks": {"type": "list", "elements": "str"},
}

_UPDATE_BODY = {"devices": "devices"}


class VmwareRestCrudModule(VmwareRestCrudModuleBase):
    PAYLOAD_FORMAT = {
        "update": {
            "query": {},
            "body": _UPDATE_BODY,
            "path": {"vm": "vm"},
        },
    }

    def _fetch_boot_devices(self):
        path = self.build_path(BOOT_DEVICE_PATH)
        response = self.client.get(path)
        if response.status == 404:
            self.module.fail_json(
                msg="Virtual machine not found: {0}".format(self.params["vm"])
            )
        return normalize_list_response(response.json)

    def _put_boot_devices(self, path, devices):
        body = {"devices": devices}
        response = self.client.request("PUT", path, data=body)
        if response.status in (200, 204):
            return response
        self.client.error_handler.handle_request_error(
            exception=UnexpectedAPIResponse(response.status, response.data),
            method="PUT",
            path=path,
            request_kwargs={"data": body},
        )

    def _devices_match(self, current, desired):
        if len(current) != len(desired):
            return False
        for current_entry, desired_entry in zip(current, desired):
            if not values_equal(current_entry, desired_entry):
                return False
        return True

    def ensure_present(self):
        if self.params.get("devices") is None:
            self.module.fail_json(
                msg="devices must be specified when state is present"
            )

        desired = self.params["devices"]
        path = self.build_path(BOOT_DEVICE_PATH)
        current = self._fetch_boot_devices()

        if self._devices_match(current, desired):
            return {"changed": False, "value": current}

        if not self.module.check_mode:
            self._put_boot_devices(path, desired)
            updated = self._fetch_boot_devices()
        else:
            updated = desired
        return {"changed": True, "value": updated}

    def ensure_absent(self):
        path = self.build_path(BOOT_DEVICE_PATH)
        current = self._fetch_boot_devices()

        if not current:
            return {"changed": False, "value": current}

        if not self.module.check_mode:
            self._put_boot_devices(path, [])
            updated = self._fetch_boot_devices()
        else:
            updated = []
        return {"changed": True, "value": updated}


def main():
    module_args = connection_params_argument_spec()
    module_args["state"] = {
        "type": "str",
        "choices": ["present", "absent"],
        "default": "present",
    }
    module_args["vm"] = {"type": "str", "required": True}
    module_args["devices"] = {
        "type": "list",
        "elements": "dict",
        "options": DEVICE_ENTRY_OPTIONS,
    }

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
    )

    crud_module = VmwareRestCrudModule(module)

    if module.params["state"] == "present":
        result = crud_module.ensure_present()
    elif module.params["state"] == "absent":
        result = crud_module.ensure_absent()
    else:
        module.fail_json(msg="Unsupported state: {0}".format(module.params["state"]))

    module.exit_json(**result)


if __name__ == "__main__":
    main()
