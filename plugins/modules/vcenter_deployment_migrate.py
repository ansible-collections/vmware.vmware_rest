#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = """
module: vcenter_deployment_migrate
short_description: Handle resource of type vcenter_deployment_migrate
description: Handle resource of type vcenter_deployment_migrate
options:
  action:
    choices:
    - cancel
    description:
    - action=cancel Required with I(state=['cancel'])
    type: str
  active_directory:
    description:
    - Information specific to the Active Directory server to which the source windows
      vCenter Server is joined.
    - 'Validate attributes are:'
    - ' - C(domain) (str): The domain name of the Active Directory server to which
      the migrated vCenter Server appliance should be joined.'
    - ' - C(password) (str): Active Directory user password that has permission to
      join the Active Directory after the vCenter Server is migrated to appliance.'
    - ' - C(username) (str): Active Directory user that has permission to join the
      Active Directory after the vCenter Server is migrated to appliance.'
    type: dict
  auto_answer:
    description:
    - Use the default option for any questions that may come up during appliance configuration.
    type: bool
  existing_migration_assistant:
    description:
    - Information specific to the Migration Assistant that is running on the Windows
      vCenter Server. Required with I(state=['check', 'start'])
    - 'Validate attributes are:'
    - ' - C(https_port) (int): The HTTPS port being used by Migration Assistant.'
    - ' - C(ssl_thumbprint) (str): SHA1 thumbprint of the Migration Assistant SSL
      certificate that will be used for verification.'
    type: dict
  history:
    description:
    - 'Determines how vCenter history will be migrated during the migration process.
      vCenter history consists of: <ul> <li>Statistics</li> <li>Events</li> <li>Tasks</li>
      </ul> By default only core data will be migrated. Use this spec to define which
      part of vCenter history data will be migrated and when.'
    - 'Validate attributes are:'
    - ' - C(data_set) (str): The {@name HistoryMigrationOption} defines the vCenter
      history migration option choices.'
    - ' - C(defer_import) (bool): Defines how vCenter history will be migrated. If
      set to true, vCenter history will be migrated separately after successful upgrade
      or migration, otherwise it will be migrated along with core data during the
      upgrade or migration process.'
    type: dict
  psc:
    description:
    - Information specific to a Platform Services Controller.
    - 'Validate attributes are:'
    - ' - C(ceip_enabled) (bool): Customer experience improvement program should be
      enabled or disabled for this Platform Services Controller migration.'
    type: dict
  source_vc_windows:
    description:
    - Information specific to the Windows vCenter Server. Required with I(state=['check',
      'start'])
    - 'Validate attributes are:'
    - ' - C(hostname) (str): The IP address or DNS resolvable name of the source Windows
      machine.'
    - ' - C(password) (str): The SSO administrator account password.'
    - ' - C(username) (str): The SSO account with administrative privilege to perform
      the migration operation.'
    type: dict
  state:
    choices:
    - cancel
    - check
    - start
    description: []
    type: str
  vcsa_embedded:
    description:
    - Information specific to an embedded vCenter Server.
    - 'Validate attributes are:'
    - ' - C(ceip_enabled) (bool): Customer experience improvement program should be
      enabled or disabled for this embedded vCenter Server migration.'
    type: dict
author:
- Ansible VMware team
version_added: 1.0.0
requirements:
- python >= 3.6
"""

IN_QUERY_PARAMETER = ["action"]

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

    argument_spec["action"] = {
        "type": "str",
        "choices": ["cancel"],
        "operationIds": ["cancel"],
    }
    argument_spec["active_directory"] = {
        "type": "dict",
        "operationIds": ["check", "start"],
    }
    argument_spec["auto_answer"] = {"type": "bool", "operationIds": ["check", "start"]}
    argument_spec["existing_migration_assistant"] = {
        "type": "dict",
        "operationIds": ["check", "start"],
    }
    argument_spec["history"] = {"type": "dict", "operationIds": ["check", "start"]}
    argument_spec["psc"] = {"type": "dict", "operationIds": ["check", "start"]}
    argument_spec["source_vc_windows"] = {
        "type": "dict",
        "operationIds": ["check", "start"],
    }
    argument_spec["state"] = {"type": "str", "choices": ["cancel", "check", "start"]}
    argument_spec["vcsa_embedded"] = {
        "type": "dict",
        "operationIds": ["check", "start"],
    }

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

    return "https://{vcenter_hostname}/rest/vcenter/deployment/migrate".format(**params)


async def entry_point(module, session):
    func = globals()[("_" + module.params["state"])]
    return await func(module.params, session)


async def _cancel(params, session):
    _url = "https://{vcenter_hostname}/rest/vcenter/deployment/migrate".format(
        **params
    ) + gen_args(params, IN_QUERY_PARAMETER)
    async with session.post(_url) as resp:
        try:
            if resp.headers["Content-Type"] == "application/json":
                _json = await resp.json()
        except KeyError:
            _json = {}
        return await update_changed_flag(_json, resp.status, "cancel")


async def _check(params, session):
    accepted_fields = [
        "active_directory",
        "auto_answer",
        "existing_migration_assistant",
        "history",
        "psc",
        "source_vc_windows",
        "vcsa_embedded",
    ]
    if "check" == "create":
        _exists = await exists(params, session)
        if _exists:
            return await update_changed_flag({"value": _exists}, 200, "get")
    spec = {}
    for i in accepted_fields:
        if params[i]:
            spec[i] = params[i]
    _url = "https://{vcenter_hostname}/rest/vcenter/deployment/migrate?action=check".format(
        **params
    )
    async with session.post(_url, json={"spec": spec}) as resp:
        try:
            if resp.headers["Content-Type"] == "application/json":
                _json = await resp.json()
        except KeyError:
            _json = {}
        if ("check" == "create") and (resp.status in [200, 201]) and ("value" in _json):
            if isinstance(_json["value"], dict):
                _id = list(_json["value"].values())[0]
            else:
                _id = _json["value"]
            _json = {"value": (await get_device_info(params, session, _url, _id))}
        return await update_changed_flag(_json, resp.status, "check")


async def _start(params, session):
    accepted_fields = [
        "active_directory",
        "auto_answer",
        "existing_migration_assistant",
        "history",
        "psc",
        "source_vc_windows",
        "vcsa_embedded",
    ]
    if "start" == "create":
        _exists = await exists(params, session)
        if _exists:
            return await update_changed_flag({"value": _exists}, 200, "get")
    spec = {}
    for i in accepted_fields:
        if params[i]:
            spec[i] = params[i]
    _url = "https://{vcenter_hostname}/rest/vcenter/deployment/migrate?action=start".format(
        **params
    )
    async with session.post(_url, json={"spec": spec}) as resp:
        try:
            if resp.headers["Content-Type"] == "application/json":
                _json = await resp.json()
        except KeyError:
            _json = {}
        if ("start" == "create") and (resp.status in [200, 201]) and ("value" in _json):
            if isinstance(_json["value"], dict):
                _id = list(_json["value"].values())[0]
            else:
                _id = _json["value"]
            _json = {"value": (await get_device_info(params, session, _url, _id))}
        return await update_changed_flag(_json, resp.status, "start")


if __name__ == "__main__":
    import asyncio

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
