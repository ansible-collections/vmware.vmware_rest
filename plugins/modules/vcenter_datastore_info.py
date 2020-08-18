#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = """
module: vcenter_datastore_info
short_description: Handle resource of type vcenter_datastore
description: Handle resource of type vcenter_datastore
options:
  datastore:
    description:
    - Identifier of the datastore for which information should be retrieved.
    - 'The parameter must be an identifier for the resource type: Datastore. Required
      with I(state=[''get''])'
    type: str
  filter.datacenters:
    description:
    - Datacenters that must contain the datastore for the datastore to match the filter.
    - If unset or empty, datastores in any datacenter match the filter.
    - 'When clients pass a value of this structure as a parameter, the field must
      contain identifiers for the resource type: Datacenter. When operations return
      a value of this structure as a result, the field will contain identifiers for
      the resource type: Datacenter.'
    type: list
  filter.datastores:
    description:
    - Identifiers of datastores that can match the filter.
    - If unset or empty, datastores with any identifier match the filter.
    - 'When clients pass a value of this structure as a parameter, the field must
      contain identifiers for the resource type: Datastore. When operations return
      a value of this structure as a result, the field will contain identifiers for
      the resource type: Datastore.'
    type: list
  filter.folders:
    description:
    - Folders that must contain the datastore for the datastore to match the filter.
    - If unset or empty, datastores in any folder match the filter.
    - 'When clients pass a value of this structure as a parameter, the field must
      contain identifiers for the resource type: Folder. When operations return a
      value of this structure as a result, the field will contain identifiers for
      the resource type: Folder.'
    type: list
  filter.names:
    description:
    - Names that datastores must have to match the filter (see Datastore.Info.name).
    - If unset or empty, datastores with any name match the filter.
    type: list
  filter.types:
    description:
    - Types that datastores must have to match the filter (see Datastore.Summary.type).
    - If unset or empty, datastores with any type match the filter.
    type: list
author:
- Ansible VMware team
version_added: 1.0.0
requirements:
- python >= 3.6
"""

IN_QUERY_PARAMETER = [
    "filter.datacenters",
    "filter.datastores",
    "filter.folders",
    "filter.names",
    "filter.types",
]

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

    argument_spec["datastore"] = {"type": "str", "operationIds": ["get"]}
    argument_spec["filter.datacenters"] = {"type": "list", "operationIds": ["list"]}
    argument_spec["filter.datastores"] = {"type": "list", "operationIds": ["list"]}
    argument_spec["filter.folders"] = {"type": "list", "operationIds": ["list"]}
    argument_spec["filter.names"] = {"type": "list", "operationIds": ["list"]}
    argument_spec["filter.types"] = {"type": "list", "operationIds": ["list"]}

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

    if params["datastore"]:
        return "https://{vcenter_hostname}/rest/vcenter/datastore/{datastore}".format(
            **params
        ) + gen_args(params, IN_QUERY_PARAMETER)
    else:
        return "https://{vcenter_hostname}/rest/vcenter/datastore".format(
            **params
        ) + gen_args(params, IN_QUERY_PARAMETER)


async def entry_point(module, session):
    async with session.get(url(module.params)) as resp:
        _json = await resp.json()
        return await update_changed_flag(_json, resp.status, "get")


if __name__ == "__main__":
    import asyncio

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
