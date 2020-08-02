from __future__ import absolute_import, division, print_function

__metaclass__ = type
import socket
import json

DOCUMENTATION = """
module: vcenter_namespacemanagement_stats_timeseries_info
short_description: Handle resource of type vcenter_namespacemanagement_stats_timeseries
description: Handle resource of type vcenter_namespacemanagement_stats_timeseries
options:
  cluster:
    description:
    - Cluster identifier for queries for a cluster.
    - This field is optional and it is only relevant when the value of TimeSeries.Spec.obj-type
      is CLUSTER.
    - 'When clients pass a value of this structure as a parameter, the field must
      be an identifier for the resource type: ClusterComputeResource. When operations
      return a value of this structure as a result, the field will be an identifier
      for the resource type: ClusterComputeResource.'
    type: str
  end:
    description:
    - UNIX timestamp value indicating when the requested series of statistical samples
      should end. https://en.wikipedia.org/wiki/Unix_time Required with I(state=['get'])
    type: int
  namespace:
    description:
    - Namespace name for queries for a namespace.
    - This field is optional and it is only relevant when the value of TimeSeries.Spec.obj-type
      is NAMESPACE.
    - 'When clients pass a value of this structure as a parameter, the field must
      be an identifier for the resource type: vcenter.namespaces.Instance. When operations
      return a value of this structure as a result, the field will be an identifier
      for the resource type: vcenter.namespaces.Instance.'
    type: str
  obj_type:
    choices:
    - CLUSTER
    - NAMESPACE
    - POD
    description:
    - Type of statistics object that this request is operating on. Required with I(state=['get'])
    type: str
  pod:
    description: []
    type: str
  start:
    description:
    - UNIX timestamp value indicating when the requested series of statistical samples
      should begin. https://en.wikipedia.org/wiki/Unix_time Required with I(state=['get'])
    type: int
author:
- Ansible VMware team
version_added: 1.0.0
requirements:
- python >= 3.6
"""
IN_QUERY_PARAMETER = ["cluster", "end", "namespace", "obj_type", "pod", "start"]
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
            type="str", required=False, fallback=(env_fallback, ["VMWARE_HOST"])
        ),
        "vcenter_username": dict(
            type="str", required=False, fallback=(env_fallback, ["VMWARE_USER"])
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
    argument_spec["start"] = {"type": "int", "operationIds": ["get"]}
    argument_spec["pod"] = {"type": "str", "operationIds": ["get"]}
    argument_spec["obj_type"] = {
        "type": "str",
        "choices": ["CLUSTER", "NAMESPACE", "POD"],
        "operationIds": ["get"],
    }
    argument_spec["namespace"] = {"type": "str", "operationIds": ["get"]}
    argument_spec["end"] = {"type": "int", "operationIds": ["get"]}
    argument_spec["cluster"] = {"type": "str", "operationIds": ["get"]}
    return argument_spec


async def get_device_info(params, session, _url, _key):
    async with session.get(((_url + "/") + _key)) as resp:
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
            if (params.get(k) is not None) and (device.get(k) != params.get(k)):
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
    return "https://{vcenter_hostname}/rest/api/vcenter/namespace-management/stats/time-series".format(
        **params
    ) + gen_args(
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
