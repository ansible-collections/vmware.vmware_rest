#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = """
module: stats_rsrcaddrs_info
short_description: Handle resource of type stats_rsrcaddrs
description: Handle resource of type stats_rsrcaddrs
options:
  id:
    description:
    - Resource Address ID.
    - 'The parameter must be an identifier for the resource type: vstats.model.RsrcAddr.
      Required with I(state=[''get''])'
    type: str
  page:
    description:
    - 'The ResourceAddresses.FilterSpec.page field is used to retrieve paged data
      for large result sets. It is an opaque paging token obtained from a prior call
      to the ResourceAddresses.list API. Warning: This attribute is available as Technology
      Preview. These are early access APIs provided to test, automate and provide
      feedback on the feature. Since this can change based on feedback, VMware does
      not guarantee backwards compatibility and recommends against using them in production
      environments. Some Technology Preview APIs might only be applicable to specific
      environments.'
    - when set a follow up page in a paged result set will be delivered.
    type: str
  resources:
    description:
    - 'Resources to include in the query. Each resource is specified through a composite
      string that follows the following format. '
    - ' type.<resource type>[.<scheme>]=<resource id> '
    - ' resource type specifies the type of resource for example VM, VCPU etc. '
    - ' scheme is an optional element to disambiguate the resource as needed for example
      to differentiate managed object id from uuid. '
    - ' resource id is the unique resource identifier value for example: vm-41 '
    - ' Example values include: type.VM=vm-41, type.VCPU=1, type.VM.moid=vm-41'
    - '. Warning: This attribute is available as Technology Preview. These are early
      access APIs provided to test, automate and provide feedback on the feature.
      Since this can change based on feedback, VMware does not guarantee backwards
      compatibility and recommends against using them in production environments.
      Some Technology Preview APIs might only be applicable to specific environments.'
    - When left unset the result will not be filtered for specific resources.
    type: list
  types:
    description:
    - 'List of Resource types. Warning: This attribute is available as Technology
      Preview. These are early access APIs provided to test, automate and provide
      feedback on the feature. Since this can change based on feedback, VMware does
      not guarantee backwards compatibility and recommends against using them in production
      environments. Some Technology Preview APIs might only be applicable to specific
      environments.'
    - When unset the result will not be filtered by resource types.
    - 'When clients pass a value of this structure as a parameter, the field must
      contain identifiers for the resource type: vstats.model.RsrcType. When operations
      return a value of this structure as a result, the field will contain identifiers
      for the resource type: vstats.model.RsrcType.'
    type: list
author:
- Ansible VMware team
version_added: 1.0.0
requirements:
- python >= 3.6
"""

IN_QUERY_PARAMETER = ["page", "resources", "types"]

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

    argument_spec["id"] = {"type": "str", "operationIds": ["get"]}
    argument_spec["page"] = {"type": "str", "operationIds": ["list"]}
    argument_spec["resources"] = {"type": "list", "operationIds": ["list"]}
    argument_spec["types"] = {"type": "list", "operationIds": ["list"]}

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

    if params["id"]:
        return "https://{vcenter_hostname}/rest/api/stats/rsrc-addrs/{id}".format(
            **params
        ) + gen_args(params, IN_QUERY_PARAMETER)
    else:
        return "https://{vcenter_hostname}/rest/api/stats/rsrc-addrs".format(
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
