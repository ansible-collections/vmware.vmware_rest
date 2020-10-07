#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = """
module: vcenter_vm_power
short_description: Manage the power of a VM
description: Manage the power of a VM
options:
  state:
    choices:
    - reset
    - start
    - stop
    - suspend
    description: []
    required: true
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
author:
- Goneri Le Bouder (@goneri) <goneri@lebouder.net>
version_added: 1.0.0
requirements:
- python >= 3.6
- aiohttp
"""

EXAMPLES = """
- name: Collect the list of the existing VM
  vcenter_vm_info:
  register: existing_vms
  until: existing_vms is not failed
- name: Collect information about a specific VM
  vcenter_vm_info:
    vm: '{{ search_result.value[0].vm }}'
  register: test_vm1_info
- name: Turn off the VM
  vcenter_vm_power:
    state: stop
    vm: '{{ item.vm }}'
  with_items: '{{ existing_vms.value }}'
  ignore_errors: yes
- name: Turn the power of the VM on
  vcenter_vm_power:
    state: start
    vm: '{{ test_vm1_info.id }}'
"""

RETURN = """
"""

# This structure describes the format of the data expected by the end-points
PAYLOAD_FORMAT = {
    "get": {"query": {}, "body": {}, "path": {"vm": "vm"}},
    "reset": {"query": {}, "body": {}, "path": {"vm": "vm"}},
    "start": {"query": {}, "body": {}, "path": {"vm": "vm"}},
    "stop": {"query": {}, "body": {}, "path": {"vm": "vm"}},
    "suspend": {"query": {}, "body": {}, "path": {"vm": "vm"}},
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

    argument_spec["state"] = {
        "required": True,
        "type": "str",
        "choices": ["reset", "start", "stop", "suspend"],
    }
    argument_spec["vm"] = {"type": "str"}

    return argument_spec


async def main():
    module_args = prepare_argument_spec()
    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)
    if not module.params["vcenter_hostname"]:
        module.fail_json("vcenter_hostname cannot be empty")
    if not module.params["vcenter_username"]:
        module.fail_json("vcenter_username cannot be empty")
    if not module.params["vcenter_password"]:
        module.fail_json("vcenter_password cannot be empty")
    session = await open_session(
        vcenter_hostname=module.params["vcenter_hostname"],
        vcenter_username=module.params["vcenter_username"],
        vcenter_password=module.params["vcenter_password"],
        log_file=module.params["vcenter_rest_log_file"],
    )
    result = await entry_point(module, session)
    module.exit_json(**result)


def build_url(params):

    return ("https://{vcenter_hostname}" "/rest/vcenter/vm/{vm}/power").format(**params)


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


async def _reset(params, session):
    _in_query_parameters = PAYLOAD_FORMAT["reset"]["query"].keys()
    payload = payload = prepare_payload(params, PAYLOAD_FORMAT["reset"])
    subdevice_type = get_subdevice_type("/rest/vcenter/vm/{vm}/power/reset")
    if subdevice_type and (not params[subdevice_type]):
        _json = await exists(params, session, build_url(params))
        if _json:
            params[subdevice_type] = _json["id"]
    _url = "https://{vcenter_hostname}/rest/vcenter/vm/{vm}/power/reset".format(
        **params
    ) + gen_args(params, _in_query_parameters)
    async with session.post(_url, json=payload) as resp:
        try:
            if resp.headers["Content-Type"] == "application/json":
                _json = await resp.json()
        except KeyError:
            _json = {}
        return await update_changed_flag(_json, resp.status, "reset")


async def _start(params, session):
    _in_query_parameters = PAYLOAD_FORMAT["start"]["query"].keys()
    payload = payload = prepare_payload(params, PAYLOAD_FORMAT["start"])
    subdevice_type = get_subdevice_type("/rest/vcenter/vm/{vm}/power/start")
    if subdevice_type and (not params[subdevice_type]):
        _json = await exists(params, session, build_url(params))
        if _json:
            params[subdevice_type] = _json["id"]
    _url = "https://{vcenter_hostname}/rest/vcenter/vm/{vm}/power/start".format(
        **params
    ) + gen_args(params, _in_query_parameters)
    async with session.post(_url, json=payload) as resp:
        try:
            if resp.headers["Content-Type"] == "application/json":
                _json = await resp.json()
        except KeyError:
            _json = {}
        return await update_changed_flag(_json, resp.status, "start")


async def _stop(params, session):
    _in_query_parameters = PAYLOAD_FORMAT["stop"]["query"].keys()
    payload = payload = prepare_payload(params, PAYLOAD_FORMAT["stop"])
    subdevice_type = get_subdevice_type("/rest/vcenter/vm/{vm}/power/stop")
    if subdevice_type and (not params[subdevice_type]):
        _json = await exists(params, session, build_url(params))
        if _json:
            params[subdevice_type] = _json["id"]
    _url = "https://{vcenter_hostname}/rest/vcenter/vm/{vm}/power/stop".format(
        **params
    ) + gen_args(params, _in_query_parameters)
    async with session.post(_url, json=payload) as resp:
        try:
            if resp.headers["Content-Type"] == "application/json":
                _json = await resp.json()
        except KeyError:
            _json = {}
        return await update_changed_flag(_json, resp.status, "stop")


async def _suspend(params, session):
    _in_query_parameters = PAYLOAD_FORMAT["suspend"]["query"].keys()
    payload = payload = prepare_payload(params, PAYLOAD_FORMAT["suspend"])
    subdevice_type = get_subdevice_type("/rest/vcenter/vm/{vm}/power/suspend")
    if subdevice_type and (not params[subdevice_type]):
        _json = await exists(params, session, build_url(params))
        if _json:
            params[subdevice_type] = _json["id"]
    _url = "https://{vcenter_hostname}/rest/vcenter/vm/{vm}/power/suspend".format(
        **params
    ) + gen_args(params, _in_query_parameters)
    async with session.post(_url, json=payload) as resp:
        try:
            if resp.headers["Content-Type"] == "application/json":
                _json = await resp.json()
        except KeyError:
            _json = {}
        return await update_changed_flag(_json, resp.status, "suspend")


if __name__ == "__main__":
    import asyncio

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
