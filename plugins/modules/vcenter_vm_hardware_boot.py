#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = """
module: vcenter_vm_hardware_boot
short_description: Handle resource of type vcenter_vm_hardware_boot
description: Handle resource of type vcenter_vm_hardware_boot
options:
  delay:
    description:
    - Delay in milliseconds before beginning the firmware boot process when the virtual
      machine is powered on. This delay may be used to provide a time window for users
      to connect to the virtual machine console and enter BIOS setup mode.
    - If unset, the value is unchanged.
    type: int
  efi_legacy_boot:
    description:
    - Flag indicating whether to use EFI legacy boot mode.
    - If unset, the value is unchanged.
    type: bool
  enter_setup_mode:
    description:
    - Flag indicating whether the firmware boot process should automatically enter
      setup mode the next time the virtual machine boots. Note that this flag will
      automatically be reset to false once the virtual machine enters setup mode.
    - If unset, the value is unchanged.
    type: bool
  network_protocol:
    choices:
    - IPV4
    - IPV6
    description:
    - The Boot.NetworkProtocol enumerated type defines the valid network boot protocols
      supported when booting a virtual machine with EFI firmware over the network.
    type: str
  retry:
    description:
    - Flag indicating whether the virtual machine should automatically retry the boot
      process after a failure.
    - If unset, the value is unchanged.
    type: bool
  retry_delay:
    description:
    - Delay in milliseconds before retrying the boot process after a failure; applicable
      only when Boot.Info.retry is true.
    - If unset, the value is unchanged.
    type: int
  state:
    choices:
    - update
    description: []
    type: str
  type:
    choices:
    - BIOS
    - EFI
    description:
    - The Boot.Type enumerated type defines the valid firmware types for a virtual
      machine.
    type: str
  vm:
    description:
    - Virtual machine identifier.
    - 'The parameter must be an identifier for the resource type: VirtualMachine.'
    type: str
author:
- Ansible VMware team
version_added: 1.0.0
requirements:
- python >= 3.6
"""

IN_QUERY_PARAMETER = []

import socket
import json
from ansible.module_utils.basic import env_fallback

try:
    from ansible_module.turbo.module import AnsibleTurboModule as AnsibleModule
except ImportError:
    from ansible.module_utils.basic import AnsibleModule
from ansible_collections.vmware.vmware_rest.plugins.module_utils.vmware_rest import (
    gen_args,
    open_session,
    update_changed_flag,
)


def prepare_argument_spec():
    argument_spec = {
        "vcenter_hostname": dict(
            type="str", required=False, fallback=(env_fallback, ["VMWARE_HOST"]),
        ),
        "vcenter_username": dict(
            type="str", required=False, fallback=(env_fallback, ["VMWARE_USER"]),
        ),
        "vcenter_password": dict(
            type="str",
            required=False,
            no_log=True,
            fallback=(env_fallback, ["VMWARE_PASSWORD"]),
        ),
        "vcenter_certs": dict(
            type="bool",
            required=False,
            no_log=True,
            fallback=(env_fallback, ["VMWARE_VALIDATE_CERTS"]),
        ),
    }

    argument_spec["delay"] = {"type": "int", "operationIds": ["update"]}
    argument_spec["efi_legacy_boot"] = {"type": "bool", "operationIds": ["update"]}
    argument_spec["enter_setup_mode"] = {"type": "bool", "operationIds": ["update"]}
    argument_spec["network_protocol"] = {
        "type": "str",
        "choices": ["IPV4", "IPV6"],
        "operationIds": ["update"],
    }
    argument_spec["retry"] = {"type": "bool", "operationIds": ["update"]}
    argument_spec["retry_delay"] = {"type": "int", "operationIds": ["update"]}
    argument_spec["state"] = {"type": "str", "choices": ["update"]}
    argument_spec["type"] = {
        "type": "str",
        "choices": ["BIOS", "EFI"],
        "operationIds": ["update"],
    }
    argument_spec["vm"] = {"type": "str", "operationIds": ["update"]}

    return argument_spec


async def get_device_info(params, session, _url, _key):
    async with session.get(_url + "/" + _key) as resp:
        _json = await resp.json()
        entry = _json["value"]
        entry["_key"] = _key
        return entry


async def list_devices(params, session):
    existing_entries = []
    _url = url(params)
    async with session.get(_url) as resp:
        _json = await resp.json()
        devices = _json["value"]
    for device in devices:
        _id = list(device.values())[0]
        existing_entries.append((await get_device_info(params, session, _url, _id)))
    return existing_entries


async def exists(params, session):
    unicity_keys = ["bus", "pci_slot_number"]
    devices = await list_devices(params, session)
    for device in devices:
        for k in unicity_keys:
            if params.get(k) is not None and device.get(k) != params.get(k):
                break
        else:
            return device


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


def url(params):

    return "https://{vcenter_hostname}/rest/vcenter/vm/{vm}/hardware/boot".format(
        **params
    )


async def entry_point(module, session):
    func = globals()[("_" + module.params["state"])]
    return await func(module.params, session)


async def _update(params, session):
    accepted_fields = [
        "delay",
        "efi_legacy_boot",
        "enter_setup_mode",
        "network_protocol",
        "retry",
        "retry_delay",
        "type",
    ]
    if "update" == "create":
        _exists = await exists(params, session)
        if _exists:
            return await update_changed_flag({"value": _exists}, 200, "get")
    spec = {}
    for i in accepted_fields:
        if params[i]:
            spec[i] = params[i]
    _url = "https://{vcenter_hostname}/rest/vcenter/vm/{vm}/hardware/boot".format(
        **params
    )
    async with session.patch(_url, json={"spec": spec}) as resp:
        try:
            if resp.headers["Content-Type"] == "application/json":
                _json = await resp.json()
        except KeyError:
            _json = {}
        if (
            ("update" == "create")
            and (resp.status in [200, 201])
            and ("value" in _json)
        ):
            if isinstance(_json["value"], dict):
                _id = list(_json["value"].values())[0]
            else:
                _id = _json["value"]
            _json = {"value": (await get_device_info(params, session, _url, _id))}
        return await update_changed_flag(_json, resp.status, "update")


if __name__ == "__main__":
    import asyncio

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
