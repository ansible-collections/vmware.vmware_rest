#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = """
module: vcenter_network_info
short_description: Handle resource of type vcenter_network
description: Handle resource of type vcenter_network
options:
  filter_datacenters:
    description:
    - Datacenters that must contain the network for the network to match the filter.
    - If unset or empty, networks in any datacenter match the filter.
    - 'When clients pass a value of this structure as a parameter, the field must
      contain identifiers for the resource type: Datacenter. When operations return
      a value of this structure as a result, the field will contain identifiers for
      the resource type: Datacenter.'
    elements: str
    type: list
  filter_folders:
    description:
    - Folders that must contain the network for the network to match the filter.
    - If unset or empty, networks in any folder match the filter.
    - 'When clients pass a value of this structure as a parameter, the field must
      contain identifiers for the resource type: Folder. When operations return a
      value of this structure as a result, the field will contain identifiers for
      the resource type: Folder.'
    elements: str
    type: list
  filter_names:
    description:
    - Names that networks must have to match the filter (see Network.Summary.name).
    - If unset or empty, networks with any name match the filter.
    elements: str
    type: list
  filter_networks:
    description:
    - Identifiers of networks that can match the filter.
    - If unset or empty, networks with any identifier match the filter.
    - 'When clients pass a value of this structure as a parameter, the field must
      contain identifiers for the resource type: Network. When operations return a
      value of this structure as a result, the field will contain identifiers for
      the resource type: Network.'
    elements: str
    type: list
  filter_types:
    description:
    - Types that networks must have to match the filter (see Network.Summary.type).
    - If unset, networks with any type match the filter.
    elements: str
    type: list
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
author:
- Goneri Le Bouder (@goneri) <goneri@lebouder.net>
version_added: 1.0.0
requirements:
- python >= 3.6
- aiohttp
"""

EXAMPLES = """
- name: Get a list of the networks
  vcenter_network_info:
  register: my_network_value
- name: Get a list of the networks with a filter
  vcenter_network_info:
    filter_types: STANDARD_PORTGROUP
  register: my_standard_portgroup_value
"""

# This structure describes the format of the data expected by the end-points
PAYLOAD_FORMAT = {
    "list": {
        "query": {
            "filter.datacenters": "filter.datacenters",
            "filter.folders": "filter.folders",
            "filter.names": "filter.names",
            "filter.networks": "filter.networks",
            "filter.types": "filter.types",
        },
        "body": {},
        "path": {},
    }
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

    argument_spec["filter_datacenters"] = {"type": "list", "elements": "str"}
    argument_spec["filter_folders"] = {"type": "list", "elements": "str"}
    argument_spec["filter_names"] = {"type": "list", "elements": "str"}
    argument_spec["filter_networks"] = {"type": "list", "elements": "str"}
    argument_spec["filter_types"] = {"type": "list", "elements": "str"}

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

    _in_query_parameters = PAYLOAD_FORMAT["list"]["query"].keys()
    return ("https://{vcenter_hostname}" "/rest/vcenter/network").format(
        **params
    ) + gen_args(params, _in_query_parameters)


async def entry_point(module, session):
    async with session.get(build_url(module.params)) as resp:
        _json = await resp.json()
        if module.params.get("None"):
            _json["id"] = module.params.get("None")
        return await update_changed_flag(_json, resp.status, "get")


if __name__ == "__main__":
    import asyncio

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
