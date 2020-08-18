#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = """
module: vcenter_host_info
short_description: Handle resource of type vcenter_host
description: Handle resource of type vcenter_host
options:
  filter.clusters:
    description:
    - Clusters that must contain the hosts for the hosts to match the filter.
    - If unset or empty, hosts in any cluster and hosts that are not in a cluster
      match the filter. If this field is not empty and Host.FilterSpec.standalone
      is true, no hosts will match the filter.
    - 'When clients pass a value of this structure as a parameter, the field must
      contain identifiers for the resource type: ClusterComputeResource. When operations
      return a value of this structure as a result, the field will contain identifiers
      for the resource type: ClusterComputeResource.'
    type: list
  filter.connection_states:
    description:
    - Connection states that a host must be in to match the filter (see Host.Summary.connection-state.
    - If unset or empty, hosts in any connection state match the filter.
    type: list
  filter.datacenters:
    description:
    - Datacenters that must contain the hosts for the hosts to match the filter.
    - If unset or empty, hosts in any datacenter match the filter.
    - 'When clients pass a value of this structure as a parameter, the field must
      contain identifiers for the resource type: Datacenter. When operations return
      a value of this structure as a result, the field will contain identifiers for
      the resource type: Datacenter.'
    type: list
  filter.folders:
    description:
    - Folders that must contain the hosts for the hosts to match the filter.
    - If unset or empty, hosts in any folder match the filter.
    - 'When clients pass a value of this structure as a parameter, the field must
      contain identifiers for the resource type: Folder. When operations return a
      value of this structure as a result, the field will contain identifiers for
      the resource type: Folder.'
    type: list
  filter.hosts:
    description:
    - Identifiers of hosts that can match the filter.
    - If unset or empty, hosts with any identifier match the filter.
    - 'When clients pass a value of this structure as a parameter, the field must
      contain identifiers for the resource type: HostSystem. When operations return
      a value of this structure as a result, the field will contain identifiers for
      the resource type: HostSystem.'
    type: list
  filter.names:
    description:
    - Names that hosts must have to match the filter (see Host.Summary.name).
    - If unset or empty, hosts with any name match the filter.
    type: list
  filter.standalone:
    description:
    - If true, only hosts that are not part of a cluster can match the filter, and
      if false, only hosts that are are part of a cluster can match the filter.
    - If unset Hosts can match filter independent of whether they are part of a cluster
      or not. If this field is true and Host.FilterSpec.clusters os not empty, no
      hosts will match the filter.
    type: bool
author:
- Ansible VMware team
version_added: 1.0.0
requirements:
- python >= 3.6
"""

IN_QUERY_PARAMETER = [
    "filter.clusters",
    "filter.connection_states",
    "filter.datacenters",
    "filter.folders",
    "filter.hosts",
    "filter.names",
    "filter.standalone",
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

    argument_spec["filter.clusters"] = {"type": "list", "operationIds": ["list"]}
    argument_spec["filter.connection_states"] = {
        "type": "list",
        "operationIds": ["list"],
    }
    argument_spec["filter.datacenters"] = {"type": "list", "operationIds": ["list"]}
    argument_spec["filter.folders"] = {"type": "list", "operationIds": ["list"]}
    argument_spec["filter.hosts"] = {"type": "list", "operationIds": ["list"]}
    argument_spec["filter.names"] = {"type": "list", "operationIds": ["list"]}
    argument_spec["filter.standalone"] = {"type": "bool", "operationIds": ["list"]}

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

    return "https://{vcenter_hostname}/rest/vcenter/host".format(**params) + gen_args(
        params, IN_QUERY_PARAMETER
    )


async def entry_point(module, session):
    async with session.get(url(module.params)) as resp:
        _json = await resp.json()
        return await update_changed_flag(_json, resp.status, "get")


if __name__ == "__main__":
    import asyncio

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
