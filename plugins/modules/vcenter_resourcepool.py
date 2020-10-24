#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# template: DEFAULT_MODULE

DOCUMENTATION = """
module: vcenter_resourcepool
short_description: Manage the resourcepool of a vCenter
description: Manage the resourcepool of a vCenter
options:
  cpu_allocation:
    description:
    - Resource allocation for CPU.
    - if unset or empty, the CPU allocation of the resource pool will not be changed.
    - 'Valide attributes are:'
    - ' - C(expandable_reservation) (bool): In a resource pool with an expandable
      reservation, the reservation can grow beyond the specified value, if the parent
      resource pool has unreserved resources. A non-expandable reservation is called
      a fixed reservation.'
    - If unset or empty, I(expandable_reservation) will be set to true.
    - ' - C(limit) (int): The utilization of a resource pool will not exceed this
      limit, even if there are available resources. This is typically used to ensure
      a consistent performance of resource pools independent of available resources.
      If set to -1, then there is no fixed limit on resource usage (only bounded by
      available resources and shares). Units are MB for memory, and MHz for CPU.'
    - If unset or empty, I(limit) will be set to -1.
    - ' - C(reservation) (int): Amount of resource that is guaranteed available to
      a resource pool. Reserved resources are not wasted if they are not used. If
      the utilization is less than the reservation, the resources can be utilized
      by other running virtual machines. Units are MB fo memory, and MHz for CPU.'
    - If unset or empty, I(reservation) will be set to 0.
    - ' - C(shares) (dict): Shares are used in case of resource contention.'
    - '   - Accepted keys:'
    - '     - level (string): This option defines the possible values for the allocation
      level.'
    - 'Accepted value for this field:'
    - '       - C(LOW)'
    - '       - C(NORMAL)'
    - '       - C(HIGH)'
    - '       - C(CUSTOM)'
    - '     - shares (integer): When I(level) is set to CUSTOM, it is the number of
      shares allocated. Otherwise, this value is ignored. '
    - ' There is no unit for this value. It is a relative measure based on the settings
      for other resource pools.'
    - ''
    - This field is optional and it is only relevant when the value of I(level) is
      CUSTOM.
    type: dict
  memory_allocation:
    description:
    - Resource allocation for CPU.
    - if unset or empty, the CPU allocation of the resource pool will not be changed.
    - 'Valide attributes are:'
    - ' - C(expandable_reservation) (bool): In a resource pool with an expandable
      reservation, the reservation can grow beyond the specified value, if the parent
      resource pool has unreserved resources. A non-expandable reservation is called
      a fixed reservation.'
    - If unset or empty, I(expandable_reservation) will be set to true.
    - ' - C(limit) (int): The utilization of a resource pool will not exceed this
      limit, even if there are available resources. This is typically used to ensure
      a consistent performance of resource pools independent of available resources.
      If set to -1, then there is no fixed limit on resource usage (only bounded by
      available resources and shares). Units are MB for memory, and MHz for CPU.'
    - If unset or empty, I(limit) will be set to -1.
    - ' - C(reservation) (int): Amount of resource that is guaranteed available to
      a resource pool. Reserved resources are not wasted if they are not used. If
      the utilization is less than the reservation, the resources can be utilized
      by other running virtual machines. Units are MB fo memory, and MHz for CPU.'
    - If unset or empty, I(reservation) will be set to 0.
    - ' - C(shares) (dict): Shares are used in case of resource contention.'
    - '   - Accepted keys:'
    - '     - level (string): This option defines the possible values for the allocation
      level.'
    - 'Accepted value for this field:'
    - '       - C(LOW)'
    - '       - C(NORMAL)'
    - '       - C(HIGH)'
    - '       - C(CUSTOM)'
    - '     - shares (integer): When I(level) is set to CUSTOM, it is the number of
      shares allocated. Otherwise, this value is ignored. '
    - ' There is no unit for this value. It is a relative measure based on the settings
      for other resource pools.'
    - ''
    - This field is optional and it is only relevant when the value of I(level) is
      CUSTOM.
    type: dict
  name:
    description:
    - Name of the resource pool.
    - if unset or empty, the name of the resource pool will not be changed. Required
      with I(state=['present'])
    type: str
  parent:
    description:
    - Parent of the created resource pool.
    - When clients pass a value of this structure as a parameter, the field must be
      the id of a resource returned by M(vcenter_resourcepool_info). Required with
      I(state=['present'])
    type: str
  resource_pool:
    description:
    - Identifier of the resource pool to be deleted.
    - The parameter must be the id of a resource returned by M(vcenter_resourcepool_info).
      Required with I(state=['absent'])
    type: str
  state:
    choices:
    - absent
    - present
    default: present
    description: []
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

EXAMPLES = r"""
"""

RETURN = r"""
# content generated by the update_return_section callback# task: Create a generic resource pool
id:
  description: moid of the resource
  returned: On success
  sample: resgroup-1383
  type: str
value:
  description: Create a generic resource pool
  returned: On success
  sample:
    cpu_allocation:
      expandable_reservation: 1
      limit: -1
      reservation: 0
      shares:
        level: NORMAL
    memory_allocation:
      expandable_reservation: 1
      limit: -1
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
}

import socket
import json
from ansible.module_utils.basic import env_fallback

try:
    from ansible_collections.cloud.common.plugins.module_utils.turbo.exceptions import (
        EmbeddedModuleFailure,
    )
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

    argument_spec["cpu_allocation"] = {"type": "dict"}
    argument_spec["memory_allocation"] = {"type": "dict"}
    argument_spec["name"] = {"type": "str"}
    argument_spec["parent"] = {"type": "str"}
    argument_spec["resource_pool"] = {"type": "str"}
    argument_spec["state"] = {
        "type": "str",
        "choices": ["absent", "present"],
        "default": "present",
    }

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
        validate_certs=module.params["vcenter_validate_certs"],
        log_file=module.params["vcenter_rest_log_file"],
    )
    result = await entry_point(module, session)
    module.exit_json(**result)


# template: URL
def build_url(params):
    return ("https://{vcenter_hostname}" "/rest/vcenter/resource-pool").format(**params)


# template: main_content
async def entry_point(module, session):
    if module.params["state"] == "present":
        if "_create" in globals():
            operation = "create"
        else:
            operation = "update"
    elif module.params["state"] == "absent":
        operation = "delete"
    else:
        operation = module.params["state"]

    func = globals()["_" + operation]
    return await func(module.params, session)


# FUNC_WITH_DATA_CREATE_TPL
async def _create(params, session):
    if params["resource_pool"]:
        _json = await get_device_info(
            session, build_url(params), params["resource_pool"]
        )
    else:
        _json = await exists(params, session, build_url(params), ["resource_pool"])
    if _json:
        if "_update" in globals():
            params["resource_pool"] = _json["id"]
            return await globals()["_update"](params, session)
        else:
            return await update_changed_flag(_json, 200, "get")

    payload = prepare_payload(params, PAYLOAD_FORMAT["create"])
    _url = ("https://{vcenter_hostname}" "/rest/vcenter/resource-pool").format(**params)
    async with session.post(_url, json=payload) as resp:
        if resp.status == 500:
            raise EmbeddedModuleFailure(
                f"Request has failed: status={resp.status}, {await resp.text()}"
            )
        try:
            if resp.headers["Content-Type"] == "application/json":
                _json = await resp.json()
        except KeyError:
            _json = {}
        # Update the value field with all the details
        if (resp.status in [200, 201]) and "value" in _json:
            if isinstance(_json["value"], dict):
                _id = list(_json["value"].values())[0]
            else:
                _id = _json["value"]
            _json = await get_device_info(session, _url, _id)

        return await update_changed_flag(_json, resp.status, "create")


# template: FUNC_WITH_DATA_DELETE_TPL
async def _delete(params, session):
    _in_query_parameters = PAYLOAD_FORMAT["delete"]["query"].keys()
    payload = payload = prepare_payload(params, PAYLOAD_FORMAT["delete"])
    subdevice_type = get_subdevice_type("/rest/vcenter/resource-pool/{resource_pool}")
    if subdevice_type and not params[subdevice_type]:
        _json = await exists(params, session, build_url(params))
        if _json:
            params[subdevice_type] = _json["id"]
    _url = (
        "https://{vcenter_hostname}" "/rest/vcenter/resource-pool/{resource_pool}"
    ).format(**params) + gen_args(params, _in_query_parameters)
    async with session.delete(_url, json=payload) as resp:
        try:
            if resp.headers["Content-Type"] == "application/json":
                _json = await resp.json()
        except KeyError:
            _json = {}
        return await update_changed_flag(_json, resp.status, "delete")


# FUNC_WITH_DATA_UPDATE_TPL
async def _update(params, session):
    payload = payload = prepare_payload(params, PAYLOAD_FORMAT["update"])
    _url = (
        "https://{vcenter_hostname}" "/rest/vcenter/resource-pool/{resource_pool}"
    ).format(**params)
    async with session.get(_url) as resp:
        _json = await resp.json()
        for k, v in _json["value"].items():
            if k in payload and payload[k] == v:
                del payload[k]
            elif "spec" in payload:
                if k in payload["spec"] and payload["spec"][k] == v:
                    del payload["spec"][k]

        # NOTE: workaround for vcenter_vm_hardware, upgrade_version needs the upgrade_policy
        # option. So we ensure it's here.
        try:
            if (
                payload["spec"]["upgrade_version"]
                and "upgrade_policy" not in payload["spec"]
            ):
                payload["spec"]["upgrade_policy"] = _json["value"]["upgrade_policy"]
        except KeyError:
            pass

        if payload == {} or payload == {"spec": {}}:
            # Nothing has changed
            _json["id"] = params.get("resource_pool")
            return await update_changed_flag(_json, resp.status, "get")
    async with session.patch(_url, json=payload) as resp:
        try:
            if resp.headers["Content-Type"] == "application/json":
                _json = await resp.json()
        except KeyError:
            _json = {}
        _json["id"] = params.get("resource_pool")
        return await update_changed_flag(_json, resp.status, "update")


if __name__ == "__main__":
    import asyncio

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
