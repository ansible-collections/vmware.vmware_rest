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
short_description: Manage virtual floppy drives on a virtual machine.
description:
  - Create, update, and delete virtual floppy drives attached to a VMware virtual machine.
  - A virtual floppy drive can be backed by an image file (e.g. a C(.flp) or C(.img) file on
    a datastore), a physical floppy device on the ESXi host, or a client device connected
    through the virtual machine console.
  - This module also supports connecting and disconnecting an existing virtual floppy drive
    at runtime using the C(connect) and C(disconnect) states.
  - Only C(present) and C(absent) states are idempotent.

deprecated:
  removed_in: 6.0.0
  why: Floppy drives are legacy hardware no longer commonly used
  alternative: Use modern storage options or M(vmware.vmware.vm) for comprehensive hardware management.

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
      - Use C(connect) to connect the virtual floppy drive to its backing.
      - Use C(disconnect) to disconnect the virtual floppy drive from its backing.
      - Only C(present) and C(absent) support idempotence.
    type: str
    default: present
    choices:
      - present
      - absent
      - connect
      - disconnect
  floppy:
    description:
      - Identifier of the virtual floppy drive to manage.
      - Must be an identifier (MOID) for a C(Floppy) resource, for example C(8000).
      - Required when I(state) is C(absent), C(connect), or C(disconnect).
      - When I(state) is C(present), omit to create a new floppy drive or provide to update
        an existing one. If you provide an ID and the floppy does not exist, a new one will be
        created with a random ID.
    type: str
    required: false
  vm:
    description:
      - Identifier of the virtual machine that owns the floppy drive.
      - Must be an identifier (MOID) for a C(Vm) resource.
    type: str
    required: true
  backing:
    description:
      - Physical resource backing for the virtual floppy drive.
      - If omitted, defaults to automatic detection of a suitable host device.
    type: dict
    required: false
    suboptions:
      type:
        description:
          - Backing type for the virtual floppy drive.
          - C(IMAGE_FILE) - Virtual floppy drive is backed by an image file on a datastore.
          - C(HOST_DEVICE) - Virtual floppy drive is backed by a physical floppy device on
            the ESXi host where the virtual machine is running.
          - C(CLIENT_DEVICE) - Virtual floppy drive is backed by a device on the client that
            is connected to the virtual machine console.
        type: str
        required: false
        choices:
          - IMAGE_FILE
          - HOST_DEVICE
          - CLIENT_DEVICE
      image_file:
        description:
          - Path of the image file that should be used as the virtual floppy drive backing.
          - Only relevant when I(type) is C(IMAGE_FILE).
        type: str
        required: false
      host_device:
        description:
          - Name of the host device that should be used as the virtual floppy drive backing.
          - If omitted, the virtual floppy drive will be configured to automatically detect
            a suitable host device.
          - Only relevant when I(type) is C(HOST_DEVICE).
        type: str
        required: false
  start_connected:
    description:
      - Whether the virtual floppy drive should be connected whenever the virtual machine
        is powered on.
      - Defaults to C(false) if omitted.
    type: bool
    required: false
  allow_guest_control:
    description:
      - Whether the guest operating system is allowed to connect and disconnect the virtual
        floppy drive.
      - Defaults to C(false) if omitted.
    type: bool
    required: false

version_added: 5.0.0

requirements: []

notes:
  - Generated from vSphere API spec 9.1.0.
  - Compatible with vSphere API 7.0.3.
  - Compatible with vSphere API 8.0.2.
"""

EXAMPLES = r"""
- name: Add a virtual floppy drive backed by an image file
  vmware.vmware_rest.vcenter_vm_hardware_floppy:
    vm: vm-1001
    backing:
      type: IMAGE_FILE
      image_file: "[datastore1] floppies/boot.flp"
    start_connected: true
    allow_guest_control: true
    state: present
  register: floppy_result

- name: Add a virtual floppy drive backed by a client device
  vmware.vmware_rest.vcenter_vm_hardware_floppy:
    vm: vm-1001
    backing:
      type: CLIENT_DEVICE
    state: present

- name: Update an existing virtual floppy drive
  vmware.vmware_rest.vcenter_vm_hardware_floppy:
    vm: vm-1001
    floppy: '{{ floppy_result.id }}'
    allow_guest_control: false
    state: present

- name: Connect a virtual floppy drive
  vmware.vmware_rest.vcenter_vm_hardware_floppy:
    vm: vm-1001
    floppy: '{{ floppy_result.id }}'
    state: connect

- name: Disconnect a virtual floppy drive
  vmware.vmware_rest.vcenter_vm_hardware_floppy:
    vm: vm-1001
    floppy: '{{ floppy_result.id }}'
    state: disconnect

- name: Remove a virtual floppy drive
  vmware.vmware_rest.vcenter_vm_hardware_floppy:
    vm: vm-1001
    floppy: '{{ floppy_result.id }}'
    state: absent
"""

RETURN = r"""
id:
  description: MOID of the managed virtual floppy drive.
  returned: When state is present, or when a resource is deleted, or when state is set to a supported action.
  sample: "8000"
  type: str
value:
  description: The raw API response body from the vCenter operation.
  returned: On success
  type: raw
  sample:
    label: Floppy drive 1
    backing:
      type: IMAGE_FILE
      image_file: "[datastore1] floppies/boot.flp"
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

MOID_PARAMETER_HINTS = ["vm", "floppy"]

LIST_ENDPOINT = "/vcenter/vm/{vm}/hardware/floppy"
ITEM_ENDPOINT = "/vcenter/vm/{vm}/hardware/floppy/{floppy}"


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
                "image_file": {
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
                "image_file": {
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
        uri="/vcenter/vm/{vm}/hardware/floppy/{floppy}?action=connect",
        http_method="POST",
    ),
    "disconnect": OperationConfig(
        name="disconnect",
        uri="/vcenter/vm/{vm}/hardware/floppy/{floppy}?action=disconnect",
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
                "choices": ["IMAGE_FILE", "HOST_DEVICE", "CLIENT_DEVICE"],
            },
            "image_file": {
                "type": "str",
            },
            "host_device": {
                "type": "str",
            },
        },
    }
    module_args["floppy"] = {
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
