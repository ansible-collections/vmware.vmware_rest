#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = """
module: vcenter_datastore_info
short_description: Collect the information associated with the vCenter datastores
description: Collect the information associated with the vCenter datastores
options:
  datastore:
    description:
    - Identifier of the datastore for which information should be retrieved.
    - The parameter must be the id of a resource returned by M(vcenter_datastore_info).
    type: str
  filter_datacenters:
    description:
    - Datacenters that must contain the datastore for the datastore to match the filter.
    - If unset or empty, datastores in any datacenter match the filter.
    - 'When clients pass a value of this structure as a parameter, the field must
      contain the id of resources returned by M(vcenter_datacenter_info). '
    elements: str
    type: list
  filter_datastores:
    description:
    - Identifiers of datastores that can match the filter.
    - If unset or empty, datastores with any identifier match the filter.
    - 'When clients pass a value of this structure as a parameter, the field must
      contain the id of resources returned by M(vcenter_datastore_info). '
    elements: str
    type: list
  filter_folders:
    description:
    - Folders that must contain the datastore for the datastore to match the filter.
    - If unset or empty, datastores in any folder match the filter.
    - 'When clients pass a value of this structure as a parameter, the field must
      contain the id of resources returned by M(vcenter_folder_info). '
    elements: str
    type: list
  filter_names:
    description:
    - Names that datastores must have to match the filter (see I(name)).
    - If unset or empty, datastores with any name match the filter.
    elements: str
    type: list
  filter_types:
    description:
    - Types that datastores must have to match the filter (see I(type)).
    - If unset or empty, datastores with any type match the filter.
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
- name: Retrieve a list of all the datastores
  vcenter_datastore_info:
  register: my_datastores
- name: We can also use filter to limit the number of result
  vcenter_datastore_info:
    filter_names:
    - rw_datastore
  register: my_datastores
"""

RETURN = """
"""

# This structure describes the format of the data expected by the end-points
PAYLOAD_FORMAT = {
    "list": {
        "query": {
            "filter.datacenters": "filter.datacenters",
            "filter.datastores": "filter.datastores",
            "filter.folders": "filter.folders",
            "filter.names": "filter.names",
            "filter.types": "filter.types",
        },
        "body": {},
        "path": {},
    },
    "get": {"query": {}, "body": {}, "path": {"datastore": "datastore"}},
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

    argument_spec["datastore"] = {"type": "str"}
    argument_spec["filter_datacenters"] = {"type": "list", "elements": "str"}
    argument_spec["filter_datastores"] = {"type": "list", "elements": "str"}
    argument_spec["filter_folders"] = {"type": "list", "elements": "str"}
    argument_spec["filter_names"] = {"type": "list", "elements": "str"}
    argument_spec["filter_types"] = {"type": "list", "elements": "str"}

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

    if params["datastore"]:
        _in_query_parameters = PAYLOAD_FORMAT["get"]["query"].keys()
        return (
            "https://{vcenter_hostname}" "/rest/vcenter/datastore/{datastore}"
        ).format(**params) + gen_args(params, _in_query_parameters)
    else:
        _in_query_parameters = PAYLOAD_FORMAT["list"]["query"].keys()
        return ("https://{vcenter_hostname}" "/rest/vcenter/datastore").format(
            **params
        ) + gen_args(params, _in_query_parameters)


async def entry_point(module, session):
    url = build_url(module.params)
    async with session.get(url) as resp:
        _json = await resp.json()
        if module.params.get("datastore"):
            _json["id"] = module.params.get("datastore")
        elif module.params.get("label"):  # TODO extend the list of filter
            _json = await exists(module.params, session, url)
        else:  # list context, retrieve the details of each entry
            try:
                if (
                    isinstance(_json["value"][0]["datastore"], str)
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
