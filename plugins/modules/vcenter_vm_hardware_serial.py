#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = """
module: vcenter_vm_hardware_serial
short_description: Manage the serial of a VM
description: Manage the serial of a VM
options:
  allow_guest_control:
    description:
    - Flag indicating whether the guest can connect and disconnect the device.
    - If unset, the value is unchanged.
    type: bool
  backing:
    description:
    - Physical resource backing for the virtual serial port.
    - If unset, defaults to automatic detection of a suitable host device.
    - 'Valide attributes are:'
    - ' - C(file) (str): Path of the file backing the virtual serial port.'
    - This field is optional and it is only relevant when the value of I(type) is
      FILE.
    - ' - C(host_device) (str): Name of the device backing the virtual serial port. '
    - ''
    - ''
    - If unset, the virtual serial port will be configured to automatically detect
      a suitable host device.
    - ' - C(network_location) (str): URI specifying the location of the network service
      backing the virtual serial port. '
    - '   - If I(type) is NETWORK_SERVER, this field is the location used by clients
      to connect to this server. The hostname part of the URI should either be empty
      or should specify the address of the host on which the virtual machine is running.'
    - '   - If I(type) is NETWORK_CLIENT, this field is the location used by the virtual
      machine to connect to the remote server.'
    - ' '
    - This field is optional and it is only relevant when the value of I(type) is
      one of NETWORK_SERVER or NETWORK_CLIENT.
    - ' - C(no_rx_loss) (bool): Flag that enables optimized data transfer over the
      pipe. When the value is true, the host buffers data to prevent data overrun.
      This allows the virtual machine to read all of the data transferred over the
      pipe with no data loss.'
    - If unset, defaults to false.
    - ' - C(pipe) (str): Name of the pipe backing the virtual serial port.'
    - This field is optional and it is only relevant when the value of I(type) is
      one of PIPE_SERVER or PIPE_CLIENT.
    - ' - C(proxy) (str): Proxy service that provides network access to the network
      backing. If set, the virtual machine initiates a connection with the proxy service
      and forwards the traffic to the proxy.'
    - If unset, no proxy service should be used.
    - ' - C(type) (str): This option defines the valid backing types for a virtual
      serial port.'
    - '   - Accepted values:'
    - '     - FILE'
    - '     - HOST_DEVICE'
    - '     - PIPE_SERVER'
    - '     - PIPE_CLIENT'
    - '     - NETWORK_SERVER'
    - '     - NETWORK_CLIENT'
    type: dict
  label:
    description: []
    type: str
  port:
    description:
    - Virtual serial port identifier.
    - The parameter must be the id of a resource returned by M(vcenter_vm_hardware_serial).
      Required with I(state=['absent', 'connect', 'disconnect'])
    type: str
  start_connected:
    description:
    - Flag indicating whether the virtual device should be connected whenever the
      virtual machine is powered on.
    - If unset, the value is unchanged.
    type: bool
  state:
    choices:
    - absent
    - connect
    - disconnect
    - present
    - present
    default: present
    description: []
    type: str
  vcenter_hostname:
    description:
    - The hostname or IP address of the vSphere vCenter
    - If the value is not specified in the task, the value of environment variable
      C(VMWARE_HOST) will be used instead.
    required: true
    type: str
  vcenter_password:
    description:
    - The vSphere vCenter username
    - If the value is not specified in the task, the value of environment variable
      C(VMWARE_PASSWORD) will be used instead.
    required: true
    type: str
  vcenter_rest_log_file:
    description:
    - 'You can use this optional parameter to set the location of a log file. '
    - 'This file will be used to record the HTTP REST interaction. '
    - 'The file will be stored on the host that run the module. '
    type: str
  vcenter_username:
    description:
    - The vSphere vCenter username
    - If the value is not specified in the task, the value of environment variable
      C(VMWARE_USER) will be used instead.
    required: true
    type: str
  vcenter_validate_certs:
    default: true
    description:
    - Allows connection when SSL certificates are not valid. Set to C(false) when
      certificates are not trusted.
    - If the value is not specified in the task, the value of environment variable
      C(VMWARE_VALIDATE_CERTS) will be used instead.
    type: bool
  vm:
    description:
    - Virtual machine identifier.
    - The parameter must be the id of a resource returned by M(vcenter_vm_info).
    type: str
  yield_on_poll:
    description:
    - 'CPU yield behavior. If set to true, the virtual machine will periodically relinquish
      the processor if its sole task is polling the virtual serial port. The amount
      of time it takes to regain the processor will depend on the degree of other
      virtual machine activity on the host. '
    - ' This field may be modified at any time, and changes applied to a connected
      virtual serial port take effect immediately.'
    - ''
    - If unset, the value is unchanged.
    type: bool
author:
- Goneri Le Bouder (@goneri) <goneri@lebouder.net>
version_added: 1.0.0
requirements:
- python >= 3.6
- aiohttp
"""

EXAMPLES = """
- name: Get an existing serial port (label)
  vcenter_vm_hardware_serial_info:
    vm: '{{ test_vm1_info.id }}'
    label: Serial port 1
  register: serial_port_1
- name: Collect information about a specific VM
  vcenter_vm_info:
    vm: '{{ search_result.value[0].vm }}'
  register: test_vm1_info
- name: Create a new serial port
  vcenter_vm_hardware_serial:
    vm: '{{ test_vm1_info.id }}'
    label: Serial port 2
    allow_guest_control: true
- name: Create an existing serial port (label)
  vcenter_vm_hardware_serial:
    vm: '{{ test_vm1_info.id }}'
    label: Serial port 1
    allow_guest_control: true
- name: Create another serial port with a label
  vcenter_vm_hardware_serial:
    vm: '{{ test_vm1_info.id }}'
    label: Serial port 2
    allow_guest_control: true
- name: Delete an existing serial port (label)
  vcenter_vm_hardware_serial:
    vm: '{{ test_vm1_info.id }}'
    label: Serial port 2
    state: absent
- name: Delete an existing serial port (port id)
  vcenter_vm_hardware_serial:
    vm: '{{ test_vm1_info.id }}'
    port: '{{ serial_port_1.id }}'
    state: absent
"""

RETURN = """
# content generated by the update_return_section callback# task: Create an existing serial port (label)
id:
  description: moid of the resource
  returned: On success
  sample: '9000'
  type: str
value:
  description: Create an existing serial port (label)
  returned: On success
  sample:
    allow_guest_control: 1
    backing:
      auto_detect: 1
      host_device: ''
      type: HOST_DEVICE
    label: Serial port 1
    start_connected: 0
    state: NOT_CONNECTED
    yield_on_poll: 0
  type: dict
"""

# This structure describes the format of the data expected by the end-points
PAYLOAD_FORMAT = {
    "list": {"query": {}, "body": {}, "path": {"vm": "vm"}},
    "create": {
        "query": {},
        "body": {
            "allow_guest_control": "spec/allow_guest_control",
            "backing": "spec/backing",
            "start_connected": "spec/start_connected",
            "yield_on_poll": "spec/yield_on_poll",
        },
        "path": {"vm": "vm"},
    },
    "delete": {"query": {}, "body": {}, "path": {"port": "port", "vm": "vm"}},
    "get": {"query": {}, "body": {}, "path": {"port": "port", "vm": "vm"}},
    "update": {
        "query": {},
        "body": {
            "allow_guest_control": "spec/allow_guest_control",
            "backing": "spec/backing",
            "start_connected": "spec/start_connected",
            "yield_on_poll": "spec/yield_on_poll",
        },
        "path": {"port": "port", "vm": "vm"},
    },
    "connect": {"query": {}, "body": {}, "path": {"port": "port", "vm": "vm"}},
    "disconnect": {"query": {}, "body": {}, "path": {"port": "port", "vm": "vm"}},
}

import socket
import json
from ansible.module_utils.basic import env_fallback

try:
    from ansible_collections.cloud.common.plugins.module_utils.turbo.module import (
        AnsibleTurboModule as AnsibleModule,
    )
except ImportError:
    from ansible.module_utils.basic import AnsibleModule
from ansible_collections.vmware.vmware_rest.plugins.module_utils.vmware_rest import (
    build_full_device_list,
    exists,
    gen_args,
    get_device_info,
    get_subdevice_type,
    list_devices,
    open_session,
    prepare_payload,
    update_changed_flag,
)


def prepare_argument_spec():
    argument_spec = {
        "vcenter_hostname": dict(
            type="str", required=True, fallback=(env_fallback, ["VMWARE_HOST"]),
        ),
        "vcenter_username": dict(
            type="str", required=True, fallback=(env_fallback, ["VMWARE_USER"]),
        ),
        "vcenter_password": dict(
            type="str",
            required=True,
            no_log=True,
            fallback=(env_fallback, ["VMWARE_PASSWORD"]),
        ),
        "vcenter_validate_certs": dict(
            type="bool",
            required=False,
            default=True,
            fallback=(env_fallback, ["VMWARE_VALIDATE_CERTS"]),
        ),
        "vcenter_rest_log_file": dict(
            type="str",
            required=False,
            fallback=(env_fallback, ["VMWARE_REST_LOG_FILE"]),
        ),
    }

    argument_spec["allow_guest_control"] = {"type": "bool"}
    argument_spec["backing"] = {"type": "dict"}
    argument_spec["label"] = {"type": "str"}
    argument_spec["port"] = {"type": "str"}
    argument_spec["start_connected"] = {"type": "bool"}
    argument_spec["state"] = {
        "type": "str",
        "choices": ["absent", "connect", "disconnect", "present", "present"],
        "default": "present",
    }
    argument_spec["vm"] = {"type": "str"}
    argument_spec["yield_on_poll"] = {"type": "bool"}

    return argument_spec


async def main():
    module_args = prepare_argument_spec()
    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)
    session = await open_session(
        vcenter_hostname=module.params["vcenter_hostname"],
        vcenter_username=module.params["vcenter_username"],
        vcenter_password=module.params["vcenter_password"],
        log_file=module.params["vcenter_rest_log_file"],
    )
    result = await entry_point(module, session)
    module.exit_json(**result)


def build_url(params):

    return (
        "https://{vcenter_hostname}" "/rest/vcenter/vm/{vm}/hardware/serial"
    ).format(**params)


async def entry_point(module, session):
    if module.params["state"] == "present":
        if "_create" in globals():
            operation = "create"
        else:
            operation = "update"
    elif module.params["state"] == "absent":
        operation = "delete"
    else:
        operation = module.params["state"]
    func = globals()[("_" + operation)]
    return await func(module.params, session)


async def _connect(params, session):
    _in_query_parameters = PAYLOAD_FORMAT["connect"]["query"].keys()
    payload = payload = prepare_payload(params, PAYLOAD_FORMAT["connect"])
    subdevice_type = get_subdevice_type(
        "/rest/vcenter/vm/{vm}/hardware/serial/{port}/connect"
    )
    if subdevice_type and (not params[subdevice_type]):
        _json = await exists(params, session, build_url(params))
        if _json:
            params[subdevice_type] = _json["id"]
    _url = "https://{vcenter_hostname}/rest/vcenter/vm/{vm}/hardware/serial/{port}/connect".format(
        **params
    ) + gen_args(
        params, _in_query_parameters
    )
    async with session.post(_url, json=payload) as resp:
        try:
            if resp.headers["Content-Type"] == "application/json":
                _json = await resp.json()
        except KeyError:
            _json = {}
        return await update_changed_flag(_json, resp.status, "connect")


async def _create(params, session):
    if params["port"]:
        _json = await get_device_info(session, build_url(params), params["port"])
    else:
        _json = await exists(params, session, build_url(params), ["port"])
    if _json:
        if "_update" in globals():
            params["port"] = _json["id"]
            return await globals()["_update"](params, session)
        else:
            return await update_changed_flag(_json, 200, "get")
    payload = prepare_payload(params, PAYLOAD_FORMAT["create"])
    _url = "https://{vcenter_hostname}/rest/vcenter/vm/{vm}/hardware/serial".format(
        **params
    )
    async with session.post(_url, json=payload) as resp:
        try:
            if resp.headers["Content-Type"] == "application/json":
                _json = await resp.json()
        except KeyError:
            _json = {}
        if (resp.status in [200, 201]) and ("value" in _json):
            if isinstance(_json["value"], dict):
                _id = list(_json["value"].values())[0]
            else:
                _id = _json["value"]
            _json = await get_device_info(session, _url, _id)
        return await update_changed_flag(_json, resp.status, "create")


async def _delete(params, session):
    _in_query_parameters = PAYLOAD_FORMAT["delete"]["query"].keys()
    payload = payload = prepare_payload(params, PAYLOAD_FORMAT["delete"])
    subdevice_type = get_subdevice_type("/rest/vcenter/vm/{vm}/hardware/serial/{port}")
    if subdevice_type and (not params[subdevice_type]):
        _json = await exists(params, session, build_url(params))
        if _json:
            params[subdevice_type] = _json["id"]
    _url = "https://{vcenter_hostname}/rest/vcenter/vm/{vm}/hardware/serial/{port}".format(
        **params
    ) + gen_args(
        params, _in_query_parameters
    )
    async with session.delete(_url, json=payload) as resp:
        try:
            if resp.headers["Content-Type"] == "application/json":
                _json = await resp.json()
        except KeyError:
            _json = {}
        return await update_changed_flag(_json, resp.status, "delete")


async def _disconnect(params, session):
    _in_query_parameters = PAYLOAD_FORMAT["disconnect"]["query"].keys()
    payload = payload = prepare_payload(params, PAYLOAD_FORMAT["disconnect"])
    subdevice_type = get_subdevice_type(
        "/rest/vcenter/vm/{vm}/hardware/serial/{port}/disconnect"
    )
    if subdevice_type and (not params[subdevice_type]):
        _json = await exists(params, session, build_url(params))
        if _json:
            params[subdevice_type] = _json["id"]
    _url = "https://{vcenter_hostname}/rest/vcenter/vm/{vm}/hardware/serial/{port}/disconnect".format(
        **params
    ) + gen_args(
        params, _in_query_parameters
    )
    async with session.post(_url, json=payload) as resp:
        try:
            if resp.headers["Content-Type"] == "application/json":
                _json = await resp.json()
        except KeyError:
            _json = {}
        return await update_changed_flag(_json, resp.status, "disconnect")


async def _update(params, session):
    payload = payload = prepare_payload(params, PAYLOAD_FORMAT["update"])
    _url = "https://{vcenter_hostname}/rest/vcenter/vm/{vm}/hardware/serial/{port}".format(
        **params
    )
    async with session.get(_url) as resp:
        _json = await resp.json()
        for (k, v) in _json["value"].items():
            if (k in payload) and (payload[k] == v):
                del payload[k]
            elif "spec" in payload:
                if (k in payload["spec"]) and (payload["spec"][k] == v):
                    del payload["spec"][k]
        try:
            if payload["spec"]["upgrade_version"] and (
                "upgrade_policy" not in payload["spec"]
            ):
                payload["spec"]["upgrade_policy"] = _json["value"]["upgrade_policy"]
        except KeyError:
            pass
        if (payload == {}) or (payload == {"spec": {}}):
            _json["id"] = params.get("port")
            return await update_changed_flag(_json, resp.status, "get")
    async with session.patch(_url, json=payload) as resp:
        try:
            if resp.headers["Content-Type"] == "application/json":
                _json = await resp.json()
        except KeyError:
            _json = {}
        _json["id"] = params.get("port")
        return await update_changed_flag(_json, resp.status, "update")


if __name__ == "__main__":
    import asyncio

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
