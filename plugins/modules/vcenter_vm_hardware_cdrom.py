#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# template: DEFAULT_MODULE

DOCUMENTATION = """
module: vcenter_vm_hardware_cdrom
short_description: Manage the cdrom of a VM
description: Manage the cdrom of a VM
options:
  allow_guest_control:
    description:
    - Flag indicating whether the guest can connect and disconnect the device.
    - If unset, the value is unchanged.
    type: bool
  backing:
    description:
    - Physical resource backing for the virtual CD-ROM device.
    - If unset, defaults to automatic detection of a suitable host device.
    - 'Valide attributes are:'
    - ' - C(device_access_type) (str): This option defines the valid device access
      types for a physical device packing of a virtual CD-ROM device.'
    - '   - Accepted values:'
    - '     - EMULATION'
    - '     - PASSTHRU'
    - '     - PASSTHRU_EXCLUSIVE'
    - ' - C(host_device) (str): Name of the device that should be used as the virtual
      CD-ROM device backing.'
    - If unset, the virtual CD-ROM device will be configured to automatically detect
      a suitable host device.
    - ' - C(iso_file) (str): Path of the image file that should be used as the virtual
      CD-ROM device backing.'
    - This field is optional and it is only relevant when the value of I(type) is
      ISO_FILE.
    - ' - C(type) (str): This option defines the valid backing types for a virtual
      CD-ROM device.'
    - '   - Accepted values:'
    - '     - ISO_FILE'
    - '     - HOST_DEVICE'
    - '     - CLIENT_DEVICE'
    type: dict
  cdrom:
    description:
    - Virtual CD-ROM device identifier.
    - The parameter must be the id of a resource returned by M(vcenter_vm_hardware_cdrom).
      Required with I(state=['absent', 'connect', 'disconnect'])
    type: str
  ide:
    description:
    - Address for attaching the device to a virtual IDE adapter.
    - If unset, the server will choose an available address; if none is available,
      the request will fail.
    - 'Valide attributes are:'
    - ' - C(master) (bool): Flag specifying whether the device should be the master
      or slave device on the IDE adapter.'
    - If unset, the server will choose an available connection type. If no IDE connections
      are available, the request will be rejected.
    - ' - C(primary) (bool): Flag specifying whether the device should be attached
      to the primary or secondary IDE adapter of the virtual machine.'
    - If unset, the server will choose a adapter with an available connection. If
      no IDE connections are available, the request will be rejected.
    type: dict
  label:
    description: []
    type: str
  sata:
    description:
    - Address for attaching the device to a virtual SATA adapter.
    - If unset, the server will choose an available address; if none is available,
      the request will fail.
    - 'Valide attributes are:'
    - ' - C(bus) (int): Bus number of the adapter to which the device should be attached.'
    - ' - C(unit) (int): Unit number of the device.'
    - If unset, the server will choose an available unit number on the specified adapter.
      If there are no available connections on the adapter, the request will be rejected.
    type: dict
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
    default: present
    description: []
    type: str
  type:
    choices:
    - IDE
    - SATA
    description:
    - The I(host_bus_adapter_type) enumerated type defines the valid types of host
      bus adapters that may be used for attaching a Cdrom to a virtual machine.
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
    - 'If the value is not specified in the task, the value of '
    - environment variable C(VMWARE_REST_LOG_FILE) will be used instead.
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

EXAMPLES = r"""
"""

RETURN = r"""
# content generated by the update_return_section callback# task: Attach an ISO image to a guest VM
id:
  description: moid of the resource
  returned: On success
  sample: '16002'
  type: str
value:
  description: Attach an ISO image to a guest VM
  returned: On success
  sample:
    allow_guest_control: 0
    backing:
      iso_file: '[ro_datastore] fedora.iso'
      type: ISO_FILE
    label: CD/DVD drive 1
    sata:
      bus: 0
      unit: 2
    start_connected: 1
    state: NOT_CONNECTED
    type: SATA
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
            "ide": "spec/ide",
            "sata": "spec/sata",
            "start_connected": "spec/start_connected",
            "type": "spec/type",
        },
        "path": {"vm": "vm"},
    },
    "delete": {"query": {}, "body": {}, "path": {"cdrom": "cdrom", "vm": "vm"}},
    "get": {"query": {}, "body": {}, "path": {"cdrom": "cdrom", "vm": "vm"}},
    "update": {
        "query": {},
        "body": {
            "allow_guest_control": "spec/allow_guest_control",
            "backing": "spec/backing",
            "start_connected": "spec/start_connected",
        },
        "path": {"cdrom": "cdrom", "vm": "vm"},
    },
    "connect": {"query": {}, "body": {}, "path": {"cdrom": "cdrom", "vm": "vm"}},
    "disconnect": {"query": {}, "body": {}, "path": {"cdrom": "cdrom", "vm": "vm"}},
}

import socket
import json
from ansible.module_utils.basic import env_fallback

try:
    from ansible_collections.cloud.common.plugins.module_utils.turbo.exceptions import (
        EmbeddedModuleFailure,
    )
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
    argument_spec["cdrom"] = {"type": "str"}
    argument_spec["ide"] = {"type": "dict"}
    argument_spec["label"] = {"type": "str"}
    argument_spec["sata"] = {"type": "dict"}
    argument_spec["start_connected"] = {"type": "bool"}
    argument_spec["state"] = {
        "type": "str",
        "choices": ["absent", "connect", "disconnect", "present"],
        "default": "present",
    }
    argument_spec["type"] = {"type": "str", "choices": ["IDE", "SATA"]}
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
        validate_certs=module.params["vcenter_validate_certs"],
        log_file=module.params["vcenter_rest_log_file"],
    )
    result = await entry_point(module, session)
    module.exit_json(**result)


# template: URL
def build_url(params):
    return ("https://{vcenter_hostname}" "/rest/vcenter/vm/{vm}/hardware/cdrom").format(
        **params
    )


# template: main_content
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

    func = globals()["_" + operation]
    return await func(module.params, session)


# template: FUNC_WITH_DATA_TPL
async def _connect(params, session):
    _in_query_parameters = PAYLOAD_FORMAT["connect"]["query"].keys()
    payload = payload = prepare_payload(params, PAYLOAD_FORMAT["connect"])
    subdevice_type = get_subdevice_type(
        "/rest/vcenter/vm/{vm}/hardware/cdrom/{cdrom}/connect"
    )
    if subdevice_type and not params[subdevice_type]:
        _json = await exists(params, session, build_url(params))
        if _json:
            params[subdevice_type] = _json["id"]
    _url = (
        "https://{vcenter_hostname}"
        "/rest/vcenter/vm/{vm}/hardware/cdrom/{cdrom}/connect"
    ).format(**params) + gen_args(params, _in_query_parameters)
    async with session.post(_url, json=payload) as resp:
        try:
            if resp.headers["Content-Type"] == "application/json":
                _json = await resp.json()
        except KeyError:
            _json = {}
        return await update_changed_flag(_json, resp.status, "connect")


# FUNC_WITH_DATA_CREATE_TPL
async def _create(params, session):
    if params["cdrom"]:
        _json = await get_device_info(session, build_url(params), params["cdrom"])
    else:
        _json = await exists(params, session, build_url(params), ["cdrom"])
    if _json:
        if "_update" in globals():
            params["cdrom"] = _json["id"]
            return await globals()["_update"](params, session)
        else:
            return await update_changed_flag(_json, 200, "get")

    payload = prepare_payload(params, PAYLOAD_FORMAT["create"])
    _url = ("https://{vcenter_hostname}" "/rest/vcenter/vm/{vm}/hardware/cdrom").format(
        **params
    )
    async with session.post(_url, json=payload) as resp:
        if resp.status == 500:
            raise EmbeddedModuleFailure(
                f"Request has failed: status={resp.status}, {await resp.text()}"
            )
        try:
            if resp.headers["Content-Type"] == "application/json":
                _json = await resp.json()
        except KeyError:
            _json = {}
        # Update the value field with all the details
        if (resp.status in [200, 201]) and "value" in _json:
            if isinstance(_json["value"], dict):
                _id = list(_json["value"].values())[0]
            else:
                _id = _json["value"]
            _json = await get_device_info(session, _url, _id)

        return await update_changed_flag(_json, resp.status, "create")


# template: FUNC_WITH_DATA_DELETE_TPL
async def _delete(params, session):
    _in_query_parameters = PAYLOAD_FORMAT["delete"]["query"].keys()
    payload = payload = prepare_payload(params, PAYLOAD_FORMAT["delete"])
    subdevice_type = get_subdevice_type("/rest/vcenter/vm/{vm}/hardware/cdrom/{cdrom}")
    if subdevice_type and not params[subdevice_type]:
        _json = await exists(params, session, build_url(params))
        if _json:
            params[subdevice_type] = _json["id"]
    _url = (
        "https://{vcenter_hostname}" "/rest/vcenter/vm/{vm}/hardware/cdrom/{cdrom}"
    ).format(**params) + gen_args(params, _in_query_parameters)
    async with session.delete(_url, json=payload) as resp:
        try:
            if resp.headers["Content-Type"] == "application/json":
                _json = await resp.json()
        except KeyError:
            _json = {}
        return await update_changed_flag(_json, resp.status, "delete")


# template: FUNC_WITH_DATA_TPL
async def _disconnect(params, session):
    _in_query_parameters = PAYLOAD_FORMAT["disconnect"]["query"].keys()
    payload = payload = prepare_payload(params, PAYLOAD_FORMAT["disconnect"])
    subdevice_type = get_subdevice_type(
        "/rest/vcenter/vm/{vm}/hardware/cdrom/{cdrom}/disconnect"
    )
    if subdevice_type and not params[subdevice_type]:
        _json = await exists(params, session, build_url(params))
        if _json:
            params[subdevice_type] = _json["id"]
    _url = (
        "https://{vcenter_hostname}"
        "/rest/vcenter/vm/{vm}/hardware/cdrom/{cdrom}/disconnect"
    ).format(**params) + gen_args(params, _in_query_parameters)
    async with session.post(_url, json=payload) as resp:
        try:
            if resp.headers["Content-Type"] == "application/json":
                _json = await resp.json()
        except KeyError:
            _json = {}
        return await update_changed_flag(_json, resp.status, "disconnect")


# FUNC_WITH_DATA_UPDATE_TPL
async def _update(params, session):
    payload = payload = prepare_payload(params, PAYLOAD_FORMAT["update"])
    _url = (
        "https://{vcenter_hostname}" "/rest/vcenter/vm/{vm}/hardware/cdrom/{cdrom}"
    ).format(**params)
    async with session.get(_url) as resp:
        _json = await resp.json()
        for k, v in _json["value"].items():
            if k in payload and payload[k] == v:
                del payload[k]
            elif "spec" in payload:
                if k in payload["spec"] and payload["spec"][k] == v:
                    del payload["spec"][k]

        # NOTE: workaround for vcenter_vm_hardware, upgrade_version needs the upgrade_policy
        # option. So we ensure it's here.
        try:
            if (
                payload["spec"]["upgrade_version"]
                and "upgrade_policy" not in payload["spec"]
            ):
                payload["spec"]["upgrade_policy"] = _json["value"]["upgrade_policy"]
        except KeyError:
            pass

        if payload == {} or payload == {"spec": {}}:
            # Nothing has changed
            _json["id"] = params.get("cdrom")
            return await update_changed_flag(_json, resp.status, "get")
    async with session.patch(_url, json=payload) as resp:
        try:
            if resp.headers["Content-Type"] == "application/json":
                _json = await resp.json()
        except KeyError:
            _json = {}
        _json["id"] = params.get("cdrom")
        return await update_changed_flag(_json, resp.status, "update")


if __name__ == "__main__":
    import asyncio

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
