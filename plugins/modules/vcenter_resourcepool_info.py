#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# template: DEFAULT_MODULE

DOCUMENTATION = """
module: vcenter_resourcepool_info
short_description: Collect the information associated with the vCenter resourcepools
description: Collect the information associated with the vCenter resourcepools
options:
  filter_clusters:
    description:
    - Clusters that must contain the resource pool for the resource pool to match
      the filter.
    - If unset or empty, resource pools in any cluster match the filter.
    - When clients pass a value of this structure as a parameter, the field must contain
      the id of resources returned by M(vcenter_cluster_info).
    elements: str
    type: list
  filter_datacenters:
    description:
    - Datacenters that must contain the resource pool for the resource pool to match
      the filter.
    - If unset or empty, resource pools in any datacenter match the filter.
    - When clients pass a value of this structure as a parameter, the field must contain
      the id of resources returned by M(vcenter_datacenter_info).
    elements: str
    type: list
  filter_hosts:
    description:
    - Hosts that must contain the resource pool for the resource pool to match the
      filter.
    - If unset or empty, resource pools in any host match the filter.
    - When clients pass a value of this structure as a parameter, the field must contain
      the id of resources returned by M(vcenter_host_info).
    elements: str
    type: list
  filter_names:
    description:
    - Names that resource pools must have to match the filter (see I(name)).
    - If unset or empty, resource pools with any name match the filter.
    elements: str
    type: list
  filter_parent_resource_pools:
    description:
    - Resource pools that must contain the resource pool for the resource pool to
      match the filter.
    - If unset or empty, resource pools in any resource pool match the filter.
    - When clients pass a value of this structure as a parameter, the field must contain
      the id of resources returned by M(vcenter_resourcepool_info).
    elements: str
    type: list
  filter_resource_pools:
    description:
    - Identifiers of resource pools that can match the filter.
    - If unset or empty, resource pools with any identifier match the filter.
    - When clients pass a value of this structure as a parameter, the field must contain
      the id of resources returned by M(vcenter_resourcepool_info).
    elements: str
    type: list
  resource_pool:
    description:
    - Identifier of the resource pool for which information should be retrieved.
    - The parameter must be the id of a resource returned by M(vcenter_resourcepool_info).
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
  vcenter_rest_log_file:
    description:
    - 'You can use this optional parameter to set the location of a log file. '
    - 'This file will be used to record the HTTP REST interaction. '
    - 'The file will be stored on the host that run the module. '
    - 'If the value is not specified in the task, the value of '
    - environment variable C(VMWARE_REST_LOG_FILE) will be used instead.
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
- name: Get the existing resource pool
  vmware.vmware_rest.vcenter_resourcepool_info:
    resource_pool: '{{ resource_pools.value[0].resource_pool }}'
  register: my_resource_pool
- name: Get the existing resource pools
  vmware.vmware_rest.vcenter_resourcepool_info:
  register: resource_pools
- name: Get the existing resource pools
  vmware.vmware_rest.vcenter_resourcepool_info:
  register: resource_pools
- name: Read details from a specific resource pool
  vmware.vmware_rest.vcenter_resourcepool_info:
    resource_pool: '{{ my_resource_pool.id }}'
  register: my_resource_pool
"""

RETURN = """
# content generated by the update_return_section callback# task: Read details from a specific resource pool
id:
  description: moid of the resource
  returned: On success
  sample: resgroup-1034
  type: str
value:
  description: Read details from a specific resource pool
  returned: On success
  sample:
    cpu_allocation:
      expandable_reservation: 1
      limit: -1
      reservation: 0
      shares:
        level: NORMAL
    memory_allocation:
      expandable_reservation: 0
      limit: 1000
      reservation: 0
      shares:
        level: NORMAL
    name: my_resource_pool
    resource_pools: []
  type: dict
"""

# This structure describes the format of the data expected by the end-points
PAYLOAD_FORMAT = {
    "list": {
        "query": {
            "filter.clusters": "filter.clusters",
            "filter.datacenters": "filter.datacenters",
            "filter.hosts": "filter.hosts",
            "filter.names": "filter.names",
            "filter.parent_resource_pools": "filter.parent_resource_pools",
            "filter.resource_pools": "filter.resource_pools",
        },
        "body": {},
        "path": {},
    },
    "create": {
        "query": {},
        "body": {
            "cpu_allocation": "spec/cpu_allocation",
            "memory_allocation": "spec/memory_allocation",
            "name": "spec/name",
            "parent": "spec/parent",
        },
        "path": {},
    },
    "delete": {"query": {}, "body": {}, "path": {"resource_pool": "resource_pool"}},
    "get": {"query": {}, "body": {}, "path": {"resource_pool": "resource_pool"}},
    "update": {
        "query": {},
        "body": {
            "cpu_allocation": "spec/cpu_allocation",
            "memory_allocation": "spec/memory_allocation",
            "name": "spec/name",
        },
        "path": {"resource_pool": "resource_pool"},
    },
}  # pylint: disable=line-too-long

import json
import socket
from ansible.module_utils.basic import env_fallback

try:
    from ansible_collections.cloud.common.plugins.module_utils.turbo.exceptions import (
        EmbeddedModuleFailure,
    )
    from ansible_collections.cloud.common.plugins.module_utils.turbo.module import (
        AnsibleTurboModule as AnsibleModule,
    )

    AnsibleModule.collection_name = "vmware.vmware_rest"
except ImportError:
    from ansible.module_utils.basic import AnsibleModule
from ansible_collections.vmware.vmware_rest.plugins.module_utils.vmware_rest import (
    build_full_device_list,
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
        "vcenter_rest_log_file": dict(
            type="str",
            required=False,
            fallback=(env_fallback, ["VMWARE_REST_LOG_FILE"]),
        ),
    }

    argument_spec["filter_clusters"] = {"type": "list", "elements": "str"}
    argument_spec["filter_datacenters"] = {"type": "list", "elements": "str"}
    argument_spec["filter_hosts"] = {"type": "list", "elements": "str"}
    argument_spec["filter_names"] = {"type": "list", "elements": "str"}
    argument_spec["filter_parent_resource_pools"] = {"type": "list", "elements": "str"}
    argument_spec["filter_resource_pools"] = {"type": "list", "elements": "str"}
    argument_spec["resource_pool"] = {"type": "str"}

    return argument_spec


async def main():
    module_args = prepare_argument_spec()
    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)
    if not module.params["vcenter_hostname"]:
        module.fail_json("vcenter_hostname cannot be empty")
    if not module.params["vcenter_username"]:
        module.fail_json("vcenter_username cannot be empty")
    if not module.params["vcenter_password"]:
        module.fail_json("vcenter_password cannot be empty")
    try:
        session = await open_session(
            vcenter_hostname=module.params["vcenter_hostname"],
            vcenter_username=module.params["vcenter_username"],
            vcenter_password=module.params["vcenter_password"],
            validate_certs=module.params["vcenter_validate_certs"],
            log_file=module.params["vcenter_rest_log_file"],
        )
    except EmbeddedModuleFailure as err:
        module.fail_json(err.get_message())
    result = await entry_point(module, session)
    module.exit_json(**result)


# template: URL_WITH_LIST
def build_url(params):
    if params["resource_pool"]:
        _in_query_parameters = PAYLOAD_FORMAT["get"]["query"].keys()
        return (
            "https://{vcenter_hostname}" "/rest/vcenter/resource-pool/{resource_pool}"
        ).format(**params) + gen_args(params, _in_query_parameters)
    _in_query_parameters = PAYLOAD_FORMAT["list"]["query"].keys()
    return ("https://{vcenter_hostname}" "/rest/vcenter/resource-pool").format(
        **params
    ) + gen_args(params, _in_query_parameters)


# template: FUNC
async def entry_point(module, session):
    url = build_url(module.params)
    async with session.get(url) as resp:
        _json = await resp.json()
        if module.params.get("resource_pool"):
            _json["id"] = module.params.get("resource_pool")
        elif module.params.get("label"):  # TODO extend the list of filter
            _json = await exists(module.params, session, url)
        else:  # list context, retrieve the details of each entry
            try:
                if (
                    isinstance(_json["value"][0]["resource_pool"], str)
                    and len(list(_json["value"][0].values())) == 1
                ):
                    # this is a list of id, we fetch the details
                    full_device_list = await build_full_device_list(session, url, _json)
                    _json = {"value": [i["value"] for i in full_device_list]}
            except (TypeError, KeyError, IndexError):
                pass

        return await update_changed_flag(_json, resp.status, "get")


if __name__ == "__main__":
    import asyncio

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
