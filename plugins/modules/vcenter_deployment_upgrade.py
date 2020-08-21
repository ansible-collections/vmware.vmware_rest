#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = """
module: vcenter_deployment_upgrade
short_description: Handle resource of type vcenter_deployment_upgrade
description: Handle resource of type vcenter_deployment_upgrade
options:
  action:
    choices:
    - cancel
    description:
    - action=cancel Required with I(state=['cancel'])
    type: str
  auto_answer:
    description:
    - Use the default option for any questions that may come up during appliance configuration.
    type: bool
  history:
    description:
    - 'Determines how vCenter history will be migrated during the upgrade process.
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
    - Information that are specific to this Platform Services Controller.
    - 'Validate attributes are:'
    - ' - C(ceip_enabled) (bool): Customer experience improvement program should be
      enabled or disabled for this Platform Services Controller upgrade.'
    type: dict
  source_appliance:
    description:
    - Source appliance spec. Required with I(state=['check', 'start'])
    - 'Validate attributes are:'
    - ' - C(hostname) (str): The IP address or DNS resolvable name of the source appliance.'
    - ' - C(https_port) (int): The HTTPS port of the source appliance.'
    - ' - C(root_password) (str): The password of the root user on the source appliance.'
    - ' - C(ssh_thumbprint) (str): MD5 thumbprint of the server SSH key will be used
      for verification.'
    - ' - C(ssh_verify) (bool): Appliance SSH verification should be enabled or disabled.
      By default it is disabled and will not use any verification. If thumbprint is
      provided, thumbprint verification will be performed.'
    - ' - C(ssl_thumbprint) (str): SHA1 thumbprint of the server SSL certificate will
      be used for verification.'
    - ' - C(ssl_verify) (bool): SSL verification should be enabled or disabled for
      the source appliance validations. By default it is enabled and will use SSL
      certificate for verification. If thumbprint is provided, will use thumbprint
      for the verification.'
    - ' - C(sso_admin_password) (str): The SSO administrator account password.'
    - ' - C(sso_admin_username) (str): The SSO administrator account on the source
      appliance.'
    type: dict
  source_location:
    description:
    - Source location spec. Required with I(state=['check', 'start'])
    - 'Validate attributes are:'
    - ' - C(hostname) (str): The IP address or DNS resolvable name of the container.'
    - ' - C(https_port) (int): The HTTPS port of the container.'
    - ' - C(password) (str): The administrator account password.'
    - ' - C(ssl_thumbprint) (str): SHA1 thumbprint of the server SSL certificate will
      be used for verification.'
    - ' - C(ssl_verify) (bool): SSL verification should be enabled or disabled. If
      {@name #sslVerify} is true and and {@name #sslThumbprint} is {@term unset},
      the CA certificate will be used for verification. If {@name #sslVerify} is true
      and {@name #sslThumbprint} is set then the thumbprint will be used for verification.
      No verification will be performed if {@name #sslVerify} value is set to false.'
    - ' - C(username) (str): The administrator account on the host.'
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
    - Information that are specific to this embedded vCenter Server.
    - 'Validate attributes are:'
    - ' - C(ceip_enabled) (bool): Customer experience improvement program should be
      enabled or disabled for this embedded vCenter Server upgrade.'
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
    from ansible_collections.cloud.common.plugins.module_utils.turbo.module import (
        AnsibleTurboModule as AnsibleModule,
    )
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
    argument_spec["auto_answer"] = {"type": "bool", "operationIds": ["check", "start"]}
    argument_spec["history"] = {"type": "dict", "operationIds": ["check", "start"]}
    argument_spec["psc"] = {"type": "dict", "operationIds": ["check", "start"]}
    argument_spec["source_appliance"] = {
        "type": "dict",
        "operationIds": ["check", "start"],
    }
    argument_spec["source_location"] = {
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

    return "https://{vcenter_hostname}/rest/vcenter/deployment/upgrade".format(**params)


async def entry_point(module, session):
    func = globals()[("_" + module.params["state"])]
    return await func(module.params, session)


async def _cancel(params, session):
    _url = "https://{vcenter_hostname}/rest/vcenter/deployment/upgrade".format(
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
        "auto_answer",
        "history",
        "psc",
        "source_appliance",
        "source_location",
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
    _url = "https://{vcenter_hostname}/rest/vcenter/deployment/upgrade?action=check".format(
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
        "auto_answer",
        "history",
        "psc",
        "source_appliance",
        "source_location",
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
    _url = "https://{vcenter_hostname}/rest/vcenter/deployment/upgrade?action=start".format(
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
