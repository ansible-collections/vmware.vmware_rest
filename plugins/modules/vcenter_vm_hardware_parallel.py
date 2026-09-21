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
short_description: Manage virtual parallel ports on a virtual machine.
description:
  - Create, update, and delete virtual parallel ports attached to a VMware virtual machine.
  - A virtual parallel port can be backed by a file on a datastore or by a physical
    parallel port device on the ESXi host where the virtual machine is running.
  - This module also supports connecting and disconnecting an existing virtual parallel
    port at runtime using the C(connect) and C(disconnect) states.
  - Only C(present) and C(absent) states are idempotent.

author:
  - Ansible Eco Content Team (@eco-ansible-content)

extends_documentation_fragment:
  - vmware.vmware_rest.connection_params

options:
  state:
    description:
      - The desired state of the resource.
      - Use C(present) to create or update the resource.
      - Use C(absent) to delete the resource.
      - Use C(connect) to connect the virtual parallel port to its backing.
      - Use C(disconnect) to disconnect the virtual parallel port from its backing.
      - Only C(present) and C(absent) support idempotence.
    type: str
    default: present
    choices:
      - present
      - absent
      - connect
      - disconnect
  port:
    description:
      - Identifier of the virtual parallel port to manage.
      - Must be an identifier (MOID) for a C(ParallelPort) resource, for example C(13000).
      - Required when I(state) is C(absent), C(connect), or C(disconnect).
      - When I(state) is C(present), omit to create a new parallel port or provide to update
        an existing one. If you provide an ID and the parallel port does not exist, a new one
        will be created with a random ID.
    type: str
    required: false
  vm:
    description:
      - Identifier of the virtual machine that owns the parallel port.
      - Must be an identifier (MOID) for a C(Vm) resource.
    type: str
    required: true
  backing:
    description:
      - Physical resource backing for the virtual parallel port.
      - If omitted, defaults to automatic detection of a suitable host device.
    type: dict
    required: false
    suboptions:
      type:
        description:
          - Backing type for the virtual parallel port.
          - C(FILE) - Virtual parallel port is backed by a file on a datastore.
          - C(HOST_DEVICE) - Virtual parallel port is backed by a physical parallel port
            device on the ESXi host where the virtual machine is running.
        type: str
        required: false
        choices:
          - FILE
          - HOST_DEVICE
      file:
        description:
          - Path of the file that should be used as the virtual parallel port backing.
          - Only relevant when I(type) is C(FILE).
        type: str
        required: false
      host_device:
        description:
          - Name of the host device that should be used as the virtual parallel port backing.
          - If omitted, the virtual parallel port will be configured to automatically detect
            a suitable host device.
          - Only relevant when I(type) is C(HOST_DEVICE).
        type: str
        required: false
  start_connected:
    description:
      - Whether the virtual parallel port should be connected whenever the virtual machine
        is powered on.
      - Defaults to C(false) if omitted.
    type: bool
    required: false
  allow_guest_control:
    description:
      - Whether the guest operating system is allowed to connect and disconnect the virtual
        parallel port.
      - Defaults to C(false) if omitted.
    type: bool
    required: false

version_added: 5.0.0

requirements: []

notes:
  - Generated from vSphere API spec 9.1.0.
"""

EXAMPLES = r"""
- name: Add a virtual parallel port backed by a file
  vmware.vmware_rest.vcenter_vm_hardware_parallel:
    vm: vm-1001
    backing:
      type: FILE
      file: "[datastore1] parallel/port1.log"
    start_connected: true
    allow_guest_control: true
    state: present
  register: parallel_result

- name: Add a virtual parallel port backed by a host device
  vmware.vmware_rest.vcenter_vm_hardware_parallel:
    vm: vm-1001
    backing:
      type: HOST_DEVICE
      host_device: /dev/parport0
    state: present

- name: Update an existing virtual parallel port
  vmware.vmware_rest.vcenter_vm_hardware_parallel:
    vm: vm-1001
    port: '{{ parallel_result.id }}'
    allow_guest_control: false
    state: present

- name: Connect a virtual parallel port
  vmware.vmware_rest.vcenter_vm_hardware_parallel:
    vm: vm-1001
    port: '{{ parallel_result.id }}'
    state: connect

- name: Disconnect a virtual parallel port
  vmware.vmware_rest.vcenter_vm_hardware_parallel:
    vm: vm-1001
    port: '{{ parallel_result.id }}'
    state: disconnect

- name: Remove a virtual parallel port
  vmware.vmware_rest.vcenter_vm_hardware_parallel:
    vm: vm-1001
    port: '{{ parallel_result.id }}'
    state: absent
"""

RETURN = r"""
id:
  description: MOID of the managed virtual parallel port.
  returned: When state is present, or when a resource is deleted, or when state is set to a supported action.
  sample: "13000"
  type: str
value:
  description: The raw API response body from the vCenter operation.
  returned: On success
  type: raw
  sample:
    label: Parallel port 1
    backing:
      type: FILE
      file: "[datastore1] parallel/port1.log"
    state: CONNECTED
    start_connected: true
    allow_guest_control: true
"""


from ansible.module_utils.basic import AnsibleModule
from ansible_collections.vmware.vmware_rest.plugins.module_utils._argument_spec import (
    connection_params_argument_spec,
)
from ansible_collections.vmware.vmware_rest.plugins.module_utils._errors import (
    VmwareModuleError,
)
from ansible_collections.vmware.vmware_rest.plugins.module_utils._crud_module import (
    VmwareRestCrudModuleBase,
)
from ansible_collections.vmware.vmware_rest.plugins.module_utils._operation_configs import (
    OperationConfig,
)

MOID_PARAMETER_HINTS = ["vm", "port"]

LIST_ENDPOINT = "/vcenter/vm/{vm}/hardware/parallel"
ITEM_ENDPOINT = "/vcenter/vm/{vm}/hardware/parallel/{port}"


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

CREATE_OPERATION = OperationConfig(
    name="create",
    uri=LIST_ENDPOINT,
    http_method="POST",
    body_spec={
        "backing": {
            "required": False,
            "subspec": {
                "type": {
                    "required": False,
                },
                "file": {
                    "required": False,
                },
                "host_device": {
                    "required": False,
                },
            },
        },
        "start_connected": {
            "required": False,
        },
        "allow_guest_control": {
            "required": False,
        },
    },
)

UPDATE_OPERATION = OperationConfig(
    name="update",
    uri=ITEM_ENDPOINT,
    http_method="PATCH",
    body_spec={
        "backing": {
            "required": False,
            "subspec": {
                "type": {
                    "required": False,
                },
                "file": {
                    "required": False,
                },
                "host_device": {
                    "required": False,
                },
            },
        },
        "start_connected": {
            "required": False,
        },
        "allow_guest_control": {
            "required": False,
        },
    },
)

DELETE_OPERATION = OperationConfig(
    name="delete",
    uri=ITEM_ENDPOINT,
    http_method="DELETE",
)


ACTION_OPERATIONS = {
    "connect": OperationConfig(
        name="connect",
        uri="/vcenter/vm/{vm}/hardware/parallel/{port}?action=connect",
        http_method="POST",
    ),
    "disconnect": OperationConfig(
        name="disconnect",
        uri="/vcenter/vm/{vm}/hardware/parallel/{port}?action=disconnect",
        http_method="POST",
    ),
}


def create_module_argument_spec() -> dict:
    module_args = connection_params_argument_spec()
    module_args["allow_guest_control"] = {
        "type": "bool",
    }
    module_args["backing"] = {
        "type": "dict",
        "options": {
            "type": {
                "type": "str",
                "choices": ["FILE", "HOST_DEVICE"],
            },
            "file": {
                "type": "str",
            },
            "host_device": {
                "type": "str",
            },
        },
    }
    module_args["port"] = {
        "type": "str",
    }
    module_args["start_connected"] = {
        "type": "bool",
    }
    module_args["vm"] = {
        "type": "str",
        "required": True,
    }
    module_args["state"] = {
        "type": "str",
        "choices": ["present", "absent", "connect", "disconnect"],
        "default": "present",
    }
    return module_args


def main():
    module = AnsibleModule(
        argument_spec=create_module_argument_spec(),
        supports_check_mode=True,
    )

    crud_module = VmwareRestCrudModuleBase(
        module=module,
        moid_parameter_hints=MOID_PARAMETER_HINTS,
        get_operation_config=GET_OPERATION,
        list_operation_config=LIST_OPERATION,
        create_operation_config=CREATE_OPERATION,
        update_operation_config=UPDATE_OPERATION,
        delete_operation_config=DELETE_OPERATION,
        action_operations=ACTION_OPERATIONS,
    )

    try:
        if module.params["state"] == "present":
            result = crud_module.ensure_present()
        elif module.params["state"] == "absent":
            result = crud_module.ensure_absent()
        elif module.params["state"] in ACTION_OPERATIONS:
            result = crud_module.perform_action()
        else:
            module.fail_json(
                msg="Unsupported state: {0}".format(module.params["state"])
            )
    except VmwareModuleError as e:
        module.fail_json(**e.to_module_fail_json_output())

    module.exit_json(**result)


if __name__ == "__main__":
    main()
