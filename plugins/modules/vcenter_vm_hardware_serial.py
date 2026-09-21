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
module: vcenter_vm_hardware_serial
short_description: Manage virtual serial ports on a virtual machine.
description:
  - Create, update, and delete virtual serial ports attached to a VMware virtual machine.
  - A virtual serial port can be backed by a file on a datastore, a physical serial port
    device on the ESXi host, a named pipe, or a network location.
  - This module also supports connecting and disconnecting an existing virtual serial port
    at runtime using the C(connect) and C(disconnect) states.
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
      - Use C(connect) to connect the virtual serial port to its backing.
      - Use C(disconnect) to disconnect the virtual serial port from its backing.
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
      - Identifier of the virtual serial port to manage.
      - Must be an identifier (MOID) for a C(SerialPort) resource, for example C(9000).
      - Required when I(state) is C(absent), C(connect), or C(disconnect).
      - When I(state) is C(present), omit to create a new serial port or provide to update
        an existing one.
    type: str
    required: false
  vm:
    description:
      - Identifier of the virtual machine that owns the serial port.
      - Must be an identifier (MOID) for a C(Vm) resource.
    type: str
    required: true
  yield_on_poll:
    description:
      - CPU yield behavior. If set to true, the virtual machine will periodically relinquish
        the processor if its sole task is polling the virtual serial port. The amount of time
        it takes to regain the processor depends on the degree of other virtual machine
        activity on the host.
      - Defaults to false if omitted.
    type: bool
    required: false
  backing:
    description:
      - Physical resource backing for the virtual serial port.
      - If omitted, defaults to automatic detection of a suitable host device.
    type: dict
    required: false
    suboptions:
      type:
        description:
          - Backing type for the virtual serial port.
          - C(FILE) - The virtual serial port is backed by a file on a datastore.
          - C(HOST_DEVICE) - The virtual serial port is backed by a physical serial device
            on the ESXi host where the virtual machine is running.
          - C(PIPE_SERVER) - The virtual serial port is backed by a named pipe server. The
            virtual machine accepts a connection from a host application or another virtual
            machine on the same host. This is useful for capturing debugging information sent
            through the virtual serial port.
          - C(PIPE_CLIENT) - The virtual serial port is backed by a named pipe client. The
            virtual machine connects to the named pipe provided by a host application or
            another virtual machine on the same host.
          - C(NETWORK_SERVER) - The virtual serial port is backed by a network server,
            creating a network-accessible serial port that accepts a connection from a
            remote system.
          - C(NETWORK_CLIENT) - The virtual serial port is backed by a network client,
            creating a network-accessible serial port that initiates a connection to a
            remote system.
        type: str
        required: false
        choices:
          - FILE
          - HOST_DEVICE
          - PIPE_SERVER
          - PIPE_CLIENT
          - NETWORK_SERVER
          - NETWORK_CLIENT
      file:
        description:
          - Path of the file that should be used as the virtual serial port backing.
          - Only relevant when I(type) is C(FILE).
        type: str
        required: false
      host_device:
        description:
          - Name of the host device that should be used as the virtual serial port backing.
          - If omitted, the virtual serial port will be configured to automatically detect
            a suitable host device.
          - Only relevant when I(type) is C(HOST_DEVICE).
        type: str
        required: false
      pipe:
        description:
          - Name of the pipe that should be used as the virtual serial port backing.
          - Only relevant when I(type) is C(PIPE_SERVER) or C(PIPE_CLIENT).
        type: str
        required: false
      no_rx_loss:
        description:
          - Flag that enables optimized data transfer over the pipe. When set to true, the
            host buffers data to prevent data overrun, allowing the virtual machine to read
            all of the data transferred over the pipe with no data loss.
          - Defaults to false if omitted.
          - Only relevant when I(type) is C(PIPE_SERVER) or C(PIPE_CLIENT).
        type: bool
        required: false
      network_location:
        description:
          - URI specifying the location of the network service backing the virtual serial port.
          - When I(type) is C(NETWORK_SERVER), this is the location used by clients to connect
            to the server. The hostname part of the URI should either be empty or specify the
            address of the host on which the virtual machine is running.
          - When I(type) is C(NETWORK_CLIENT), this is the location used by the virtual machine
            to connect to the remote server.
          - Only relevant when I(type) is C(NETWORK_SERVER) or C(NETWORK_CLIENT).
        type: str
        required: false
      proxy:
        description:
          - Proxy service that provides network access to the network backing. If set, the
            virtual machine initiates a connection with the proxy service and forwards the
            traffic to the proxy.
          - If omitted, no proxy service is used.
        type: str
        required: false
  start_connected:
    description:
      - Flag indicating whether the virtual device should be connected whenever the virtual
        machine is powered on.
      - Defaults to false if omitted.
    type: bool
    required: false
  allow_guest_control:
    description:
      - Flag indicating whether the guest can connect and disconnect the device.
      - Defaults to false if omitted.
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
- name: Add a virtual serial port backed by a file
  vmware.vmware_rest.vcenter_vm_hardware_serial:
    vm: vm-1001
    backing:
      type: FILE
      file: "[datastore1] serial/port1.log"
    start_connected: true
    allow_guest_control: true
    state: present
  register: serial_result

- name: Add a virtual serial port backed by a host device
  vmware.vmware_rest.vcenter_vm_hardware_serial:
    vm: vm-1001
    backing:
      type: HOST_DEVICE
      host_device: /dev/ttyS0
    state: present

- name: Add a network-backed virtual serial port acting as a server
  vmware.vmware_rest.vcenter_vm_hardware_serial:
    vm: vm-1001
    backing:
      type: NETWORK_SERVER
      network_location: telnet://:12345
    yield_on_poll: true
    state: present

- name: Update an existing virtual serial port
  vmware.vmware_rest.vcenter_vm_hardware_serial:
    vm: vm-1001
    port: '{{ serial_result.id }}'
    allow_guest_control: false
    state: present

- name: Connect a virtual serial port
  vmware.vmware_rest.vcenter_vm_hardware_serial:
    vm: vm-1001
    port: '{{ serial_result.id }}'
    state: connect

- name: Disconnect a virtual serial port
  vmware.vmware_rest.vcenter_vm_hardware_serial:
    vm: vm-1001
    port: '{{ serial_result.id }}'
    state: disconnect

- name: Remove a virtual serial port
  vmware.vmware_rest.vcenter_vm_hardware_serial:
    vm: vm-1001
    port: '{{ serial_result.id }}'
    state: absent
"""

RETURN = r"""
id:
  description: MOID of the managed virtual serial port.
  returned: When state is present, or when a resource is deleted, or when state is set to a supported action.
  sample: "9000"
  type: str
value:
  description: The raw API response body from the vCenter operation.
  returned: On success
  type: raw
  sample:
    label: Serial port 1
    backing:
      type: FILE
      file: "[datastore1] serial/port1.log"
    state: CONNECTED
    yield_on_poll: false
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

LIST_ENDPOINT = "/vcenter/vm/{vm}/hardware/serial"
ITEM_ENDPOINT = "/vcenter/vm/{vm}/hardware/serial/{port}"


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
        "yield_on_poll": {
            "required": False,
        },
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
                "pipe": {
                    "required": False,
                },
                "no_rx_loss": {
                    "required": False,
                },
                "network_location": {
                    "required": False,
                },
                "proxy": {
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
        "yield_on_poll": {
            "required": False,
        },
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
                "pipe": {
                    "required": False,
                },
                "no_rx_loss": {
                    "required": False,
                },
                "network_location": {
                    "required": False,
                },
                "proxy": {
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
        uri="/vcenter/vm/{vm}/hardware/serial/{port}?action=connect",
        http_method="POST",
    ),
    "disconnect": OperationConfig(
        name="disconnect",
        uri="/vcenter/vm/{vm}/hardware/serial/{port}?action=disconnect",
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
                "choices": [
                    "FILE",
                    "HOST_DEVICE",
                    "PIPE_SERVER",
                    "PIPE_CLIENT",
                    "NETWORK_SERVER",
                    "NETWORK_CLIENT",
                ],
            },
            "file": {
                "type": "str",
            },
            "host_device": {
                "type": "str",
            },
            "pipe": {
                "type": "str",
            },
            "no_rx_loss": {
                "type": "bool",
            },
            "network_location": {
                "type": "str",
            },
            "proxy": {
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
    module_args["yield_on_poll"] = {
        "type": "bool",
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
