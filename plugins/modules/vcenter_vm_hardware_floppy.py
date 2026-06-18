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
module: vcenter_vm_hardware_floppy
short_description: Manages virtual floppy drives on a virtual machine.
description:
  - Creates, updates, or removes virtual floppy drives for a virtual machine in vCenter.
  - Use I(state=present) to add a floppy drive or update an existing floppy drive.
  - Use I(state=absent) to remove a floppy drive.
  - When I(floppy) is not specified with I(state=present), a new floppy drive is created.
author:
  - Ansible Eco Content Team (@eco-ansible-content)
extends_documentation_fragment:
  - vmware.vmware_rest.connection_params
options:
  state:
    description:
      - The desired state of the virtual floppy drive.
      - Use C(present) to create or update the floppy drive.
      - Use C(absent) to delete the floppy drive.
    type: str
    choices:
      - present
      - absent
    default: present
  vm:
    description:
      - Identifier of the virtual machine.
      - Must be an identifier (MOID) for a C(VirtualMachine) resource.
    type: str
    required: true
  floppy:
    description:
      - Identifier of the virtual floppy drive.
      - Must be an identifier (MOID) for a
        C(com.vmware.vcenter.vm.hardware.Floppy) resource.
      - Required when I(state=absent).
      - When set with I(state=present), updates the existing floppy drive.
      - When omitted with I(state=present), a new floppy drive is created.
    type: str
  backing:
    description:
      - Physical resource backing for the virtual floppy drive.
    type: dict
    suboptions:
      type:
        description:
          - Backing type for the virtual floppy drive.
        type: str
        choices:
          - IMAGE_FILE
          - HOST_DEVICE
          - CLIENT_DEVICE
      image_file:
        description:
          - Path of the image file backing the virtual floppy drive.
          - Relevant when I(backing.type=IMAGE_FILE).
        type: str
      host_device:
        description:
          - Name of the host device backing the virtual floppy drive.
          - Relevant when I(backing.type=HOST_DEVICE).
          - When not set, the server auto-detects a suitable host device.
        type: str
  start_connected:
    description:
      - Whether the virtual floppy drive is connected when the virtual machine
        is powered on.
    type: bool
  allow_guest_control:
    description:
      - Whether the guest operating system can connect and disconnect the device.
    type: bool
version_added: 4.11.0
requirements: []
notes:
  - Generated from vSphere API spec 9.1.0.
  - Has support for vSphere API 7.0.3.
  - Has support for vSphere API 8.0.2.
"""

EXAMPLES = r"""
- name: Add a client-backed virtual floppy drive
  vmware.vmware_rest.vcenter_vm_hardware_floppy:
    vm: vm-1001
    start_connected: true
    backing:
      type: CLIENT_DEVICE

- name: Attach a floppy image to a virtual machine
  vmware.vmware_rest.vcenter_vm_hardware_floppy:
    vm: vm-1001
    backing:
      type: IMAGE_FILE
      image_file: "[datastore1] images/boot.flp"

- name: Update a floppy drive by MOID
  vmware.vmware_rest.vcenter_vm_hardware_floppy:
    vm: vm-1001
    floppy: "4000"
    start_connected: false

- name: Remove a virtual floppy drive
  vmware.vmware_rest.vcenter_vm_hardware_floppy:
    vm: vm-1001
    floppy: "4000"
    state: absent
"""

RETURN = r"""
id:
  description:
    - Identifier of the virtual floppy drive.
    - Must be an identifier (MOID) for a
      C(com.vmware.vcenter.vm.hardware.Floppy) resource.
  returned: On success when I(state=present)
  type: str
  sample: "4000"

value:
  description:
    - Floppy drive information after create or update, or the current configuration
      when no change was made.
  returned: On success when I(state=present)
  type: dict
  sample:
    label: Floppy drive 1
    start_connected: true
    backing:
      type: IMAGE_FILE
      image_file: "[datastore1] images/boot.flp"
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.vmware.vmware_rest.plugins.module_utils._argument_spec import (
    connection_params_argument_spec,
)
from ansible_collections.vmware.vmware_rest.plugins.module_utils._module_base import (
    VmwareRestCrudModuleBase,
)

LIST_PATH = "/vcenter/vm/{vm}/hardware/floppy"
ITEM_PATH = "/vcenter/vm/{vm}/hardware/floppy/{floppy}"

_CREATE_BODY = {
    "backing": "backing",
    "start_connected": "start_connected",
    "allow_guest_control": "allow_guest_control",
}

_BACKING_ARG_SPEC = {
    "type": "dict",
    "options": {
        "type": {
            "type": "str",
            "choices": ["IMAGE_FILE", "HOST_DEVICE", "CLIENT_DEVICE"],
        },
        "image_file": {"type": "str"},
        "host_device": {"type": "str"},
    },
}


class VmwareRestCrudModule(VmwareRestCrudModuleBase):
    PAYLOAD_FORMAT = {
        "create": {
            "query": {},
            "body": _CREATE_BODY,
            "path": {},
        },
        "update": {
            "query": {},
            "body": _CREATE_BODY,
            "path": {"floppy": "floppy"},
        },
    }

    UPDATABLE_PARAMS = ("backing", "start_connected", "allow_guest_control")

    def ensure_present(self):
        floppy = self.params.get("floppy")
        if floppy:
            return self._ensure_present_by_id(floppy)

        return self._create()

    def ensure_absent(self):
        floppy = self.params.get("floppy")
        if not floppy:
            self.module.fail_json(
                msg="floppy is required when removing a virtual floppy drive"
            )

        return self.delete_if_exists(ITEM_PATH, {"floppy": floppy})

    def _create(self):
        list_path = self.build_path(LIST_PATH)
        create_body = self.build_payload(self.PAYLOAD_FORMAT["create"])
        if not self.module.check_mode:
            response = self.client.post(list_path, data=create_body or None)
            floppy_id = response.json
            info = self._get_floppy_info(floppy_id)
        else:
            floppy_id = None
            info = {}
        return {
            "changed": True,
            "id": floppy_id,
            "value": info,
        }

    def _ensure_present_by_id(self, floppy):
        path = self.build_path(ITEM_PATH, {"floppy": floppy})
        response = self.client.get(path)
        if response.status == 404:
            self.module.fail_json(
                msg="Virtual floppy drive not found: {0}".format(floppy)
            )

        update_body = self.build_updatable_payload()
        result = self.update_if_changed(path, response.json, update_body)
        result["id"] = floppy
        return result

    def _get_floppy_info(self, floppy_id):
        path = self.build_path(ITEM_PATH, {"floppy": floppy_id})
        response = self.client.get(path)
        if response.status == 404:
            return {}
        return response.json


def main():
    module_args = connection_params_argument_spec()
    module_args["state"] = {
        "type": "str",
        "choices": ["present", "absent"],
        "default": "present",
    }
    module_args["vm"] = {"type": "str", "required": True}
    module_args["floppy"] = {"type": "str"}
    module_args["backing"] = _BACKING_ARG_SPEC
    module_args["start_connected"] = {"type": "bool"}
    module_args["allow_guest_control"] = {"type": "bool"}

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
