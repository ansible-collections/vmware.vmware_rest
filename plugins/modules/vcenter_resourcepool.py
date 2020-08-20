#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = """
module: vcenter_resourcepool
short_description: Handle resource of type vcenter_resourcepool
description: Handle resource of type vcenter_resourcepool
options:
  cpu_allocation:
    description:
    - Resource allocation for CPU.
    - if unset or empty, the CPU allocation of the resource pool will not be changed.
    - 'Validate attributes are:'
    - ' - C(expandable_reservation) (bool): In a resource pool with an expandable
      reservation, the reservation can grow beyond the specified value, if the parent
      resource pool has unreserved resources. A non-expandable reservation is called
      a fixed reservation.'
    - If unset or empty, ResourcePool.ResourceAllocationUpdateSpec.expandable-reservation
      will be set to true.
    - ' - C(limit) (int): The utilization of a resource pool will not exceed this
      limit, even if there are available resources. This is typically used to ensure
      a consistent performance of resource pools independent of available resources.
      If set to -1, then there is no fixed limit on resource usage (only bounded by
      available resources and shares). Units are MB for memory, and MHz for CPU.'
    - If unset or empty, ResourcePool.ResourceAllocationUpdateSpec.limit will be set
      to -1.
    - ' - C(reservation) (int): Amount of resource that is guaranteed available to
      a resource pool. Reserved resources are not wasted if they are not used. If
      the utilization is less than the reservation, the resources can be utilized
      by other running virtual machines. Units are MB fo memory, and MHz for CPU.'
    - If unset or empty, ResourcePool.ResourceAllocationUpdateSpec.reservation will
      be set to 0.
    - ' - C(shares) (dict): Shares are used in case of resource contention.'
    - If unset or empty, ResourcePool.ResourceAllocationUpdateSpec.shares will be
      set to 'NORMAL'.
    type: dict
  memory_allocation:
    description:
    - Resource allocation for memory.
    - if unset or empty, the memory allocation of the resource pool will not be changed.
    - 'Validate attributes are:'
    - ' - C(expandable_reservation) (bool): In a resource pool with an expandable
      reservation, the reservation can grow beyond the specified value, if the parent
      resource pool has unreserved resources. A non-expandable reservation is called
      a fixed reservation.'
    - If unset or empty, ResourcePool.ResourceAllocationUpdateSpec.expandable-reservation
      will be set to true.
    - ' - C(limit) (int): The utilization of a resource pool will not exceed this
      limit, even if there are available resources. This is typically used to ensure
      a consistent performance of resource pools independent of available resources.
      If set to -1, then there is no fixed limit on resource usage (only bounded by
      available resources and shares). Units are MB for memory, and MHz for CPU.'
    - If unset or empty, ResourcePool.ResourceAllocationUpdateSpec.limit will be set
      to -1.
    - ' - C(reservation) (int): Amount of resource that is guaranteed available to
      a resource pool. Reserved resources are not wasted if they are not used. If
      the utilization is less than the reservation, the resources can be utilized
      by other running virtual machines. Units are MB fo memory, and MHz for CPU.'
    - If unset or empty, ResourcePool.ResourceAllocationUpdateSpec.reservation will
      be set to 0.
    - ' - C(shares) (dict): Shares are used in case of resource contention.'
    - If unset or empty, ResourcePool.ResourceAllocationUpdateSpec.shares will be
      set to 'NORMAL'.
    type: dict
  name:
    description:
    - Name of the resource pool.
    - if unset or empty, the name of the resource pool will not be changed.
    type: str
  parent:
    description:
    - Parent of the created resource pool.
    - 'When clients pass a value of this structure as a parameter, the field must
      be an identifier for the resource type: ResourcePool. When operations return
      a value of this structure as a result, the field will be an identifier for the
      resource type: ResourcePool. Required with I(state=[''create''])'
    type: str
  resource_pool:
    description:
    - Identifier of the resource pool to be deleted.
    - 'The parameter must be an identifier for the resource type: ResourcePool. Required
      with I(state=[''delete'', ''update''])'
    type: str
  state:
    choices:
    - create
    - delete
    - update
    description: []
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

    argument_spec["cpu_allocation"] = {
        "type": "dict",
        "operationIds": ["create", "update"],
    }
    argument_spec["memory_allocation"] = {
        "type": "dict",
        "operationIds": ["create", "update"],
    }
    argument_spec["name"] = {"type": "str", "operationIds": ["create", "update"]}
    argument_spec["parent"] = {"type": "str", "operationIds": ["create"]}
    argument_spec["resource_pool"] = {
        "type": "str",
        "operationIds": ["delete", "update"],
    }
    argument_spec["state"] = {"type": "str", "choices": ["create", "delete", "update"]}

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

    return "https://{vcenter_hostname}/rest/vcenter/resource-pool".format(**params)


async def entry_point(module, session):
    func = globals()[("_" + module.params["state"])]
    return await func(module.params, session)


async def _create(params, session):
    accepted_fields = ["cpu_allocation", "memory_allocation", "name", "parent"]
    if "create" == "create":
        _exists = await exists(params, session)
        if _exists:
            return await update_changed_flag({"value": _exists}, 200, "get")
    spec = {}
    for i in accepted_fields:
        if params[i]:
            spec[i] = params[i]
    _url = "https://{vcenter_hostname}/rest/vcenter/resource-pool".format(**params)
    async with session.post(_url, json={"spec": spec}) as resp:
        try:
            if resp.headers["Content-Type"] == "application/json":
                _json = await resp.json()
        except KeyError:
            _json = {}
        if (
            ("create" == "create")
            and (resp.status in [200, 201])
            and ("value" in _json)
        ):
            if isinstance(_json["value"], dict):
                _id = list(_json["value"].values())[0]
            else:
                _id = _json["value"]
            _json = {"value": (await get_device_info(params, session, _url, _id))}
        return await update_changed_flag(_json, resp.status, "create")


async def _delete(params, session):
    _url = "https://{vcenter_hostname}/rest/vcenter/resource-pool/{resource_pool}".format(
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
    accepted_fields = ["cpu_allocation", "memory_allocation", "name"]
    if "update" == "create":
        _exists = await exists(params, session)
        if _exists:
            return await update_changed_flag({"value": _exists}, 200, "get")
    spec = {}
    for i in accepted_fields:
        if params[i]:
            spec[i] = params[i]
    _url = "https://{vcenter_hostname}/rest/vcenter/resource-pool/{resource_pool}".format(
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
