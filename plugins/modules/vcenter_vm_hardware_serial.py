#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = """
module: vcenter_vm_hardware_serial
short_description: Handle resource of type vcenter_vm_hardware_serial
description: Handle resource of type vcenter_vm_hardware_serial
options:
  allow_guest_control:
    description:
    - Flag indicating whether the guest can connect and disconnect the device.
    - If unset, the value is unchanged.
    type: bool
  backing:
    description:
    - 'Physical resource backing for the virtual serial port. '
    - ' This field may only be modified if the virtual machine is not powered on or
      the virtual serial port is not connected.'
    - If unset, the value is unchanged.
    - 'Validate attributes are:'
    - ' - C(file) (str): Path of the file backing the virtual serial port.'
    - This field is optional and it is only relevant when the value of Serial.BackingSpec.type
      is FILE.
    - ' - C(host_device) (str): Name of the device backing the virtual serial port. '
    - If unset, the virtual serial port will be configured to automatically detect
      a suitable host device.
    - ' - C(network_location) (str): URI specifying the location of the network service
      backing the virtual serial port. '
    - '   - If Serial.BackingSpec.type is NETWORK_SERVER, this field is the location
      used by clients to connect to this server. The hostname part of the URI should
      either be empty or should specify the address of the host on which the virtual
      machine is running.'
    - '   - If Serial.BackingSpec.type is NETWORK_CLIENT, this field is the location
      used by the virtual machine to connect to the remote server.'
    - ' '
    - This field is optional and it is only relevant when the value of Serial.BackingSpec.type
      is one of NETWORK_SERVER or NETWORK_CLIENT.
    - ' - C(no_rx_loss) (bool): Flag that enables optimized data transfer over the
      pipe. When the value is true, the host buffers data to prevent data overrun.
      This allows the virtual machine to read all of the data transferred over the
      pipe with no data loss.'
    - If unset, defaults to false.
    - ' - C(pipe) (str): Name of the pipe backing the virtual serial port.'
    - This field is optional and it is only relevant when the value of Serial.BackingSpec.type
      is one of PIPE_SERVER or PIPE_CLIENT.
    - ' - C(proxy) (str): Proxy service that provides network access to the network
      backing. If set, the virtual machine initiates a connection with the proxy service
      and forwards the traffic to the proxy.'
    - If unset, no proxy service should be used.
    - ' - C(type) (str): The Serial.BackingType enumerated type defines the valid
      backing types for a virtual serial port.'
    type: dict
  port:
    description:
    - Virtual serial port identifier.
    - 'The parameter must be an identifier for the resource type: vcenter.vm.hardware.SerialPort.
      Required with I(state=[''delete'', ''update''])'
    type: str
  start_connected:
    description:
    - Flag indicating whether the virtual device should be connected whenever the
      virtual machine is powered on.
    - If unset, the value is unchanged.
    type: bool
  state:
    choices:
    - create
    - delete
    - update
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
    - 'The parameter must be an identifier for the resource type: VirtualMachine.'
    type: str
  yield_on_poll:
    description:
    - 'CPU yield behavior. If set to true, the virtual machine will periodically relinquish
      the processor if its sole task is polling the virtual serial port. The amount
      of time it takes to regain the processor will depend on the degree of other
      virtual machine activity on the host. '
    - ' This field may be modified at any time, and changes applied to a connected
      virtual serial port take effect immediately.'
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
"""

IN_QUERY_PARAMETER = []

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
    gen_args,
    open_session,
    update_changed_flag,
    get_device_info,
    list_devices,
    exists,
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
    }

    argument_spec["allow_guest_control"] = {"type": "bool"}
    argument_spec["backing"] = {"type": "dict"}
    argument_spec["port"] = {"type": "str"}
    argument_spec["start_connected"] = {"type": "bool"}
    argument_spec["state"] = {"type": "str", "choices": ["create", "delete", "update"]}
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
    )
    result = await entry_point(module, session)
    module.exit_json(**result)


def build_url(params):

    return (
        "https://{vcenter_hostname}" "/rest/vcenter/vm/{vm}/hardware/serial"
    ).format(**params)


async def entry_point(module, session):
    func = globals()[("_" + module.params["state"])]
    return await func(module.params, session)


async def _create(params, session):
    accepted_fields = [
        "allow_guest_control",
        "backing",
        "start_connected",
        "yield_on_poll",
    ]
    _json = await exists(params, session, build_url(params))
    if _json:
        if "_update" in globals():
            params["port"] = _json["id"]
            return await _update(params, session)
        else:
            return await update_changed_flag(_json, 200, "get")
    spec = {}
    for i in accepted_fields:
        if params[i]:
            spec[i] = params[i]
    _url = "https://{vcenter_hostname}/rest/vcenter/vm/{vm}/hardware/serial".format(
        **params
    )
    async with session.post(_url, json={"spec": spec}) as resp:
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
            _json = await get_device_info(params, session, _url, _id)
        return await update_changed_flag(_json, resp.status, "create")


async def _delete(params, session):
    _url = "https://{vcenter_hostname}/rest/vcenter/vm/{vm}/hardware/serial/{port}".format(
        **params
    ) + gen_args(
        params, IN_QUERY_PARAMETER
    )
    async with session.delete(_url) as resp:
        try:
            if resp.headers["Content-Type"] == "application/json":
                _json = await resp.json()
        except KeyError:
            _json = {}
        return await update_changed_flag(_json, resp.status, "delete")


async def _update(params, session):
    accepted_fields = [
        "allow_guest_control",
        "backing",
        "start_connected",
        "yield_on_poll",
    ]
    spec = {}
    for i in accepted_fields:
        if params[i]:
            spec[i] = params[i]
    _url = "https://{vcenter_hostname}/rest/vcenter/vm/{vm}/hardware/serial/{port}".format(
        **params
    )
    async with session.get(_url) as resp:
        _json = await resp.json()
        for (k, v) in _json["value"].items():
            if (k in spec) and (spec[k] == v):
                del spec[k]
        if not spec:
            _json["id"] = params.get("port")
            return await update_changed_flag(_json, resp.status, "get")
    async with session.patch(_url, json={"spec": spec}) as resp:
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
