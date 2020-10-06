#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = """
module: vcenter_host_info
short_description: Collect the information associated with the vCenter hosts
description: Collect the information associated with the vCenter hosts
options:
  filter_clusters:
    description:
    - Clusters that must contain the hosts for the hosts to match the filter.
    - If unset or empty, hosts in any cluster and hosts that are not in a cluster
      match the filter. If this field is not empty and I(standalone) is true, no hosts
      will match the filter.
    - 'When clients pass a value of this structure as a parameter, the field must
      contain the id of resources returned by M(vcenter_cluster_info). '
    elements: str
    type: list
  filter_connection_states:
    description:
    - Connection states that a host must be in to match the filter (see I()
    - If unset or empty, hosts in any connection state match the filter.
    elements: str
    type: list
  filter_datacenters:
    description:
    - Datacenters that must contain the hosts for the hosts to match the filter.
    - If unset or empty, hosts in any datacenter match the filter.
    - 'When clients pass a value of this structure as a parameter, the field must
      contain the id of resources returned by M(vcenter_datacenter_info). '
    elements: str
    type: list
  filter_folders:
    description:
    - Folders that must contain the hosts for the hosts to match the filter.
    - If unset or empty, hosts in any folder match the filter.
    - 'When clients pass a value of this structure as a parameter, the field must
      contain the id of resources returned by M(vcenter_folder_info). '
    elements: str
    type: list
  filter_hosts:
    description:
    - Identifiers of hosts that can match the filter.
    - If unset or empty, hosts with any identifier match the filter.
    - 'When clients pass a value of this structure as a parameter, the field must
      contain the id of resources returned by M(vcenter_host_info). '
    elements: str
    type: list
  filter_names:
    description:
    - Names that hosts must have to match the filter (see I(name)).
    - If unset or empty, hosts with any name match the filter.
    elements: str
    type: list
  filter_standalone:
    description:
    - If true, only hosts that are not part of a cluster can match the filter, and
      if false, only hosts that are are part of a cluster can match the filter.
    - If unset Hosts can match filter independent of whether they are part of a cluster
      or not. If this field is true and I(clusters) os not empty, no hosts will match
      the filter.
    type: bool
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
- name: Get a list of the hosts
  vcenter_host_info:
  register: my_hosts
"""

RETURN = """
"""

# This structure describes the format of the data expected by the end-points
PAYLOAD_FORMAT = {
    "list": {
        "query": {
            "filter.clusters": "filter.clusters",
            "filter.connection_states": "filter.connection_states",
            "filter.datacenters": "filter.datacenters",
            "filter.folders": "filter.folders",
            "filter.hosts": "filter.hosts",
            "filter.names": "filter.names",
            "filter.standalone": "filter.standalone",
        },
        "body": {},
        "path": {},
    },
    "create": {
        "query": {},
        "body": {
            "folder": "spec/folder",
            "force_add": "spec/force_add",
            "hostname": "spec/hostname",
            "password": "spec/password",
            "port": "spec/port",
            "thumbprint": "spec/thumbprint",
            "thumbprint_verification": "spec/thumbprint_verification",
            "user_name": "spec/user_name",
        },
        "path": {},
    },
    "delete": {"query": {}, "body": {}, "path": {"host": "host"}},
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
    argument_spec["filter_connection_states"] = {"type": "list", "elements": "str"}
    argument_spec["filter_datacenters"] = {"type": "list", "elements": "str"}
    argument_spec["filter_folders"] = {"type": "list", "elements": "str"}
    argument_spec["filter_hosts"] = {"type": "list", "elements": "str"}
    argument_spec["filter_names"] = {"type": "list", "elements": "str"}
    argument_spec["filter_standalone"] = {"type": "bool"}

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
    session = await open_session(
        vcenter_hostname=module.params["vcenter_hostname"],
        vcenter_username=module.params["vcenter_username"],
        vcenter_password=module.params["vcenter_password"],
        log_file=module.params["vcenter_rest_log_file"],
    )
    result = await entry_point(module, session)
    module.exit_json(**result)


def build_url(params):

    _in_query_parameters = PAYLOAD_FORMAT["list"]["query"].keys()
    return ("https://{vcenter_hostname}" "/rest/vcenter/host").format(
        **params
    ) + gen_args(params, _in_query_parameters)


async def entry_point(module, session):
    url = build_url(module.params)
    async with session.get(url) as resp:
        _json = await resp.json()
        if module.params.get("host"):
            _json["id"] = module.params.get("host")
        elif module.params.get("label"):  # TODO extend the list of filter
            _json = await exists(module.params, session, url)
        else:  # list context, retrieve the details of each entry
            try:
                if (
                    isinstance(_json["value"][0]["host"], str)
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
