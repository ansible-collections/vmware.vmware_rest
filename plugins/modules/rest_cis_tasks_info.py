#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = """
module: rest_cis_tasks_info
short_description: Handle resource of type rest_cis_tasks
description: Handle resource of type rest_cis_tasks
options:
  filter_spec.operations:
    description:
    - 'Identifiers of operations. Tasks created by these operations match the filter
      (see CommonInfo.operation). '
    - ' Note that an operation identifier by itself is not globally unique. To filter
      on an operation, the identifier of the service interface containing the operation
      should also be specified in Tasks.FilterSpec.services.'
    - If unset or empty, tasks associated with any operation will match the filter.
    - 'When clients pass a value of this structure as a parameter, the field must
      contain identifiers for the resource type: vapi.operation. When operations return
      a value of this structure as a result, the field will contain identifiers for
      the resource type: vapi.operation.'
    type: list
  filter_spec.services:
    description:
    - Identifiers of services. Tasks created by operations in these services match
      the filter (see CommonInfo.service).
    - This field may be unset if Tasks.FilterSpec.tasks is specified. Currently all
      services must be from the same provider. If this field is unset or empty, tasks
      for any service will match the filter.
    - 'When clients pass a value of this structure as a parameter, the field must
      contain identifiers for the resource type: vapi.service. When operations return
      a value of this structure as a result, the field will contain identifiers for
      the resource type: vapi.service.'
    type: list
  filter_spec.status:
    description:
    - Status that a task must have to match the filter (see CommonInfo.status).
    - If unset or empty, tasks with any status match the filter.
    type: list
  filter_spec.targets:
    description:
    - Identifiers of the targets the operation for the associated task created or
      was performed on (see CommonInfo.target).
    - If unset or empty, tasks associated with operations on any target match the
      filter.
    type: list
  filter_spec.tasks:
    description:
    - Identifiers of tasks that can match the filter.
    - This field may be unset if Tasks.FilterSpec.services is specified. Currently
      all tasks must be from the same provider. If unset or empty, tasks with any
      identifier will match the filter.
    - 'When clients pass a value of this structure as a parameter, the field must
      contain identifiers for the resource type: cis.task. When operations return
      a value of this structure as a result, the field will contain identifiers for
      the resource type: cis.task.'
    type: list
  filter_spec.users:
    description:
    - Users who must have initiated the operation for the associated task to match
      the filter (see CommonInfo.user).
    - If unset or empty, tasks associated with operations initiated by any user match
      the filter.
    type: list
  result_spec.exclude_result:
    description:
    - If true, the result will not be included in the task information, otherwise
      it will be included.
    - If unset, the result of the operation will be included in the task information.
    type: bool
  result_spec.return_all:
    description:
    - If true, all data, including operation-specific data, will be returned, otherwise
      only the data described in Info will be returned.
    - If unset, only the data described in Info will be returned.
    type: bool
  spec.exclude_result:
    description:
    - If true, the result will not be included in the task information, otherwise
      it will be included.
    - If unset, the result of the operation will be included in the task information.
    type: bool
  spec.return_all:
    description:
    - If true, all data, including operation-specific data, will be returned, otherwise
      only the data described in Info will be returned.
    - If unset, only the data described in Info will be returned.
    type: bool
  task:
    description:
    - Task identifier.
    - 'The parameter must be an identifier for the resource type: cis.task. Required
      with I(state=[''get''])'
    type: str
author:
- Ansible VMware team
version_added: 1.0.0
requirements:
- python >= 3.6
"""

IN_QUERY_PARAMETER = [
    "filter_spec.operations",
    "filter_spec.services",
    "filter_spec.status",
    "filter_spec.targets",
    "filter_spec.tasks",
    "filter_spec.users",
    "result_spec.exclude_result",
    "result_spec.return_all",
    "spec.exclude_result",
    "spec.return_all",
]

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

    argument_spec["filter_spec.operations"] = {"type": "list", "operationIds": ["list"]}
    argument_spec["filter_spec.services"] = {"type": "list", "operationIds": ["list"]}
    argument_spec["filter_spec.status"] = {"type": "list", "operationIds": ["list"]}
    argument_spec["filter_spec.targets"] = {"type": "list", "operationIds": ["list"]}
    argument_spec["filter_spec.tasks"] = {"type": "list", "operationIds": ["list"]}
    argument_spec["filter_spec.users"] = {"type": "list", "operationIds": ["list"]}
    argument_spec["result_spec.exclude_result"] = {
        "type": "bool",
        "operationIds": ["list"],
    }
    argument_spec["result_spec.return_all"] = {"type": "bool", "operationIds": ["list"]}
    argument_spec["spec.exclude_result"] = {"type": "bool", "operationIds": ["get"]}
    argument_spec["spec.return_all"] = {"type": "bool", "operationIds": ["get"]}
    argument_spec["task"] = {"type": "str", "operationIds": ["get"]}

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

    if params["task"]:
        return "https://{vcenter_hostname}/rest/cis/tasks/{task}".format(
            **params
        ) + gen_args(params, IN_QUERY_PARAMETER)
    else:
        return "https://{vcenter_hostname}/rest/cis/tasks".format(**params) + gen_args(
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
