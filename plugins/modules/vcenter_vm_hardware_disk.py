#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = """
module: vcenter_vm_hardware_disk
short_description: Handle resource of type vcenter_vm_hardware_disk
description: Handle resource of type vcenter_vm_hardware_disk
options:
  backing:
    description:
    - Existing physical resource backing for the virtual disk. Exactly one of Disk.CreateSpec.backing
      or Disk.CreateSpec.new-vmdk must be specified.
    - If unset, the virtual disk will not be connected to an existing backing.
    - 'Valide attributes are:'
    - ' - C(type) (str): The Disk.BackingType enumerated type defines the valid backing
      types for a virtual disk.'
    - '   - Accepted values:'
    - '     - VMDK_FILE'
    - ' - C(vmdk_file) (str): Path of the VMDK file backing the virtual disk.'
    - This field is optional and it is only relevant when the value of Disk.BackingSpec.type
      is VMDK_FILE.
    elements: dict
    type: dict
  disk:
    description:
    - Virtual disk identifier.
    - 'The parameter must be an identifier for the resource type: vcenter.vm.hardware.Disk.
      Required with I(state=[''delete'', ''update''])'
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
    elements: dict
    type: dict
  new_vmdk:
    description:
    - Specification for creating a new VMDK backing for the virtual disk. Exactly
      one of Disk.CreateSpec.backing or Disk.CreateSpec.new-vmdk must be specified.
    - If unset, a new VMDK backing will not be created.
    - 'Valide attributes are:'
    - ' - C(capacity) (int): Capacity of the virtual disk backing in bytes.'
    - If unset, defaults to a guest-specific capacity.
    - ' - C(name) (str): Base name of the VMDK file. The name should not include the
      ''.vmdk'' file extension.'
    - If unset, a name (derived from the name of the virtual machine) will be chosen
      by the server.
    - ' - C(storage_policy) (dict): The Disk.StoragePolicySpec structure contains
      information about the storage policy that is to be associated the with VMDK
      file.'
    - 'If unset the default storage policy of the target datastore (if applicable)
      is applied. Currently a default storage policy is only supported by object based
      datastores : VVol & vSAN. For non- object datastores, if unset then no storage
      policy would be associated with the VMDK file.'
    - '   - Accepted keys:'
    - '     - policy (string): Identifier of the storage policy which should be associated
      with the VMDK file.'
    - 'When clients pass a value of this structure as a parameter, the field must
      be an identifier for the resource type: vcenter.StoragePolicy. When operations
      return a value of this structure as a result, the field will be an identifier
      for the resource type: vcenter.StoragePolicy.'
    elements: dict
    type: dict
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
    elements: dict
    type: dict
  scsi:
    description:
    - Address for attaching the device to a virtual SCSI adapter.
    - If unset, the server will choose an available address; if none is available,
      the request will fail.
    - 'Valide attributes are:'
    - ' - C(bus) (int): Bus number of the adapter to which the device should be attached.'
    - ' - C(unit) (int): Unit number of the device.'
    - If unset, the server will choose an available unit number on the specified adapter.
      If there are no available connections on the adapter, the request will be rejected.
    elements: dict
    type: dict
  state:
    choices:
    - absent
    - present
    - present
    default: present
    description: []
    type: str
  type:
    choices:
    - IDE
    - SATA
    - SCSI
    description:
    - The Disk.HostBusAdapterType enumerated type defines the valid types of host
      bus adapters that may be used for attaching a virtual storage device to a virtual
      machine.
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
author:
- Goneri Le Bouder (@goneri) <goneri@lebouder.net>
version_added: 1.0.0
requirements:
- python >= 3.6
- aiohttp
"""

EXAMPLES = """
"""

# This structure describes the format of the data expected by the end-points
PAYLOAD_FORMAT = {
    "list": {"query": {}, "body": {}, "path": {"vm": "vm"}},
    "create": {
        "query": {},
        "body": {
            "backing": "spec/backing",
            "ide": "spec/ide",
            "new_vmdk": "spec/new_vmdk",
            "sata": "spec/sata",
            "scsi": "spec/scsi",
            "type": "spec/type",
        },
        "path": {"vm": "vm"},
    },
    "delete": {"query": {}, "body": {}, "path": {"disk": "disk", "vm": "vm"}},
    "get": {"query": {}, "body": {}, "path": {"disk": "disk", "vm": "vm"}},
    "update": {
        "query": {},
        "body": {"backing": "spec/backing"},
        "path": {"disk": "disk", "vm": "vm"},
    },
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
    }

    argument_spec["backing"] = {"type": "dict"}
    argument_spec["disk"] = {"type": "str"}
    argument_spec["ide"] = {"type": "dict"}
    argument_spec["new_vmdk"] = {"type": "dict"}
    argument_spec["sata"] = {"type": "dict"}
    argument_spec["scsi"] = {"type": "dict"}
    argument_spec["state"] = {
        "type": "str",
        "choices": ["absent", "present", "present"],
        "default": "present",
    }
    argument_spec["type"] = {"type": "str", "choices": ["IDE", "SATA", "SCSI"]}
    argument_spec["vm"] = {"type": "str"}

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

    return ("https://{vcenter_hostname}" "/rest/vcenter/vm/{vm}/hardware/disk").format(
        **params
    )


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


async def _create(params, session):
    if params["disk"]:
        _json = await get_device_info(
            params, session, build_url(params), params["disk"]
        )
    else:
        _json = await exists(params, session, build_url(params), ["disk"])
    if _json:
        if "_update" in globals():
            params["disk"] = _json["id"]
            return await globals()["_update"](params, session)
        else:
            return await update_changed_flag(_json, 200, "get")
    payload = prepare_payload(params, PAYLOAD_FORMAT["create"])
    _url = "https://{vcenter_hostname}/rest/vcenter/vm/{vm}/hardware/disk".format(
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
            _json = await get_device_info(params, session, _url, _id)
        return await update_changed_flag(_json, resp.status, "create")


async def _delete(params, session):
    _in_query_parameters = PAYLOAD_FORMAT["delete"]["query"].keys()
    payload = payload = prepare_payload(params, PAYLOAD_FORMAT["delete"])
    subdevice_type = get_subdevice_type("/rest/vcenter/vm/{vm}/hardware/disk/{disk}")
    if subdevice_type and (not params[subdevice_type]):
        _json = await exists(params, session, build_url(params))
        if _json:
            params[subdevice_type] = _json["id"]
    _url = "https://{vcenter_hostname}/rest/vcenter/vm/{vm}/hardware/disk/{disk}".format(
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


async def _update(params, session):
    payload = payload = prepare_payload(params, PAYLOAD_FORMAT["update"])
    _url = "https://{vcenter_hostname}/rest/vcenter/vm/{vm}/hardware/disk/{disk}".format(
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
            _json["id"] = params.get("disk")
            return await update_changed_flag(_json, resp.status, "get")
    async with session.patch(_url, json=payload) as resp:
        try:
            if resp.headers["Content-Type"] == "application/json":
                _json = await resp.json()
        except KeyError:
            _json = {}
        _json["id"] = params.get("disk")
        return await update_changed_flag(_json, resp.status, "update")


if __name__ == "__main__":
    import asyncio

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
