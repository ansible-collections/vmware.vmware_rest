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
module: vcenter_vm_hardware_parallel
short_description: Manages virtual parallel ports on a virtual machine.
description:
  - Creates, updates, or removes virtual parallel ports for a virtual machine in vCenter.
  - Use I(state=present) to ensure a parallel port exists and matches the desired
    configuration.
  - Use I(state=absent) to remove a parallel port.
  - When I(port) is not specified, I(label) is used to locate an existing parallel
    port. If I(label) is also omitted and the virtual machine has exactly one parallel
    port, that port is managed.
author:
  - Ansible Eco Content Team (@eco-ansible-content)
extends_documentation_fragment:
  - vmware.vmware_rest.connection_params
options:
  state:
    description:
      - The desired state of the virtual parallel port.
      - Use C(present) to create or update the parallel port.
      - Use C(absent) to delete the parallel port.
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
  port:
    description:
      - Identifier of the virtual parallel port.
      - Must be an identifier (MOID) for a
        C(com.vmware.vcenter.vm.hardware.ParallelPort) resource.
      - When not set, I(label) or the sole existing parallel port is used to locate
        the device.
    type: str
  label:
    description:
      - Device label used to locate an existing parallel port when I(port) is not set.
    type: str
  backing:
    description:
      - Physical resource backing for the virtual parallel port.
    type: dict
    suboptions:
      type:
        description:
          - Backing type for the virtual parallel port.
        type: str
        choices:
          - FILE
          - HOST_DEVICE
      file:
        description:
          - Path of the file backing the virtual parallel port.
          - Relevant when I(backing.type=FILE).
        type: str
      host_device:
        description:
          - Name of the host device backing the virtual parallel port.
          - Relevant when I(backing.type=HOST_DEVICE).
          - When not set, the server auto-detects a suitable host device.
        type: str
  start_connected:
    description:
      - Whether the virtual parallel port is connected when the virtual machine is
        powered on.
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
- name: Enable guest control on the parallel port
  vmware.vmware_rest.vcenter_vm_hardware_parallel:
    vm: vm-1001
    allow_guest_control: true

- name: Create a parallel port backed by a file
  vmware.vmware_rest.vcenter_vm_hardware_parallel:
    vm: vm-1001
    backing:
      type: FILE
      file: /tmp/parallel.out
    start_connected: true

- name: Update a parallel port by MOID
  vmware.vmware_rest.vcenter_vm_hardware_parallel:
    vm: vm-1001
    port: "4000"
    allow_guest_control: true

- name: Remove a parallel port by label
  vmware.vmware_rest.vcenter_vm_hardware_parallel:
    vm: vm-1001
    label: Parallel port 1
    state: absent
"""

RETURN = r"""
id:
  description:
    - Identifier of the virtual parallel port.
    - Must be an identifier (MOID) for a
      C(com.vmware.vcenter.vm.hardware.ParallelPort) resource.
  returned: On success when I(state=present)
  type: str
  sample: "4000"

value:
  description:
    - Parallel port information after create or update, or the current configuration
      when no change was made.
  returned: On success when I(state=present)
  type: dict
  sample:
    label: Parallel port 1
    start_connected: true
    allow_guest_control: true
    backing:
      type: HOST_DEVICE
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.vmware.vmware_rest.plugins.module_utils._argument_spec import (
    connection_params_argument_spec,
)
from ansible_collections.vmware.vmware_rest.plugins.module_utils._module_base import (
    VmwareRestCrudModuleBase,
    payload_body_subset,
)

LIST_PATH = "/vcenter/vm/{vm}/hardware/parallel"
ITEM_PATH = "/vcenter/vm/{vm}/hardware/parallel/{port}"

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
            "choices": ["FILE", "HOST_DEVICE"],
        },
        "file": {"type": "str"},
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
            "body": payload_body_subset(_CREATE_BODY),
            "path": {"port": "port"},
        },
    }

    UPDATABLE_PARAMS = ("backing", "start_connected", "allow_guest_control")

    def ensure_present(self):
        port = self.params.get("port")
        if port:
            return self._ensure_present_by_id(port)

        found_id = self._resolve_port_id()
        if found_id:
            return self._ensure_present_by_id(found_id)

        return self._create()

    def ensure_absent(self):
        port = self.params.get("port")
        if not port:
            port = self._resolve_port_id(fail_if_ambiguous=True)
            if port is None:
                return {"changed": False}

        return self.delete_if_exists(ITEM_PATH, {"port": port})

    def _create(self):
        list_path = self.build_path(LIST_PATH)
        create_body = self.build_payload(self.PAYLOAD_FORMAT["create"])
        if not self.module.check_mode:
            response = self.client.post(list_path, data=create_body or None)
            port_id = response.json
            info = self._get_port_info(port_id)
        else:
            port_id = None
            info = {}
        return {
            "changed": True,
            "id": port_id,
            "value": info,
        }

    def _ensure_present_by_id(self, port):
        path = self.build_path(ITEM_PATH, {"port": port})
        response = self.client.get(path)
        if response.status == 404:
            self.module.fail_json(
                msg="Virtual parallel port not found: {0}".format(port)
            )

        update_body = self.build_updatable_payload()
        result = self.update_if_changed(path, response.json, update_body)
        result["id"] = port
        return result

    def _get_port_info(self, port_id):
        path = self.build_path(ITEM_PATH, {"port": port_id})
        response = self.client.get(path)
        if response.status == 404:
            return {}
        return response.json

    def _list_port_ids(self):
        list_path = self.build_path(LIST_PATH)
        summaries = self.fetch_list(list_path, self.PAYLOAD_FORMAT["create"])
        port_ids = []
        for summary in summaries:
            port_id = summary.get("port")
            if port_id:
                port_ids.append(port_id)
        return port_ids

    def _resolve_port_id(self, fail_if_ambiguous=False):
        label = self.params.get("label")
        if label:
            for port_id in self._list_port_ids():
                info = self._get_port_info(port_id)
                if info and info.get("label") == label:
                    return port_id
            if fail_if_ambiguous:
                self.module.fail_json(
                    msg="No parallel port found with label: {0}".format(label)
                )
            return None

        port_ids = self._list_port_ids()
        if len(port_ids) == 1:
            return port_ids[0]
        if fail_if_ambiguous and len(port_ids) > 1:
            self.module.fail_json(
                msg="port or label is required when multiple parallel ports exist"
            )
        return None


def main():
    module_args = connection_params_argument_spec()
    module_args["state"] = {
        "type": "str",
        "choices": ["present", "absent"],
        "default": "present",
    }
    module_args["vm"] = {"type": "str", "required": True}
    module_args["port"] = {"type": "str"}
    module_args["label"] = {"type": "str"}
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
