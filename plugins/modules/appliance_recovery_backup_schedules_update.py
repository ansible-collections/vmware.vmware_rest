#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2021, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# template: header.j2

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = r"""
module: appliance_recovery_backup_schedules_update
short_description: Handle resource of type appliance_recovery_backup_schedules_update
description: Handle resource of type appliance_recovery_backup_schedules_update
options:
  backup_password:
    description:
    - 'Password for a backup piece. The backupPassword must adhere to the following
      password requirements: At least 8 characters, cannot be more than 20 characters
      in length. At least 1 uppercase letter. At least 1 lowercase letter. At least
      1 numeric digit. At least 1 special character (i.e. any character not in [0-9,a-z,A-Z]).
      Only visible ASCII characters (for example, no space).'
    type: str
  enable:
    description:
    - Enable or disable a schedule.
    type: bool
  location:
    description:
    - URL of the backup location.
    type: str
  location_password:
    description:
    - Password for the given location.
    type: str
  location_user:
    description:
    - Username for the given location.
    type: str
  parts:
    description:
    - List of optional parts. Use the {@link appliance.recovery.backup.Parts#list}
      {@term operation} to get information about the supported parts.
    elements: str
    type: list
  recurrence_info:
    description:
    - Recurrence information for the schedule.
    - 'Valid attributes are:'
    - ' - C(days) (list): Day of week when the backup should be run. Days can be specified
      as list of days.'
    - ' - C(hour) (int): Hour when backup should run. The hour should be specified
      in 24-hour clock format.'
    - ' - C(minute) (int): Minute when backup should run.'
    type: dict
  retention_info:
    description:
    - Retention information for the schedule.
    - 'Valid attributes are:'
    - ' - C(max_count) (int): Number of backups which should be retained. If retention
      is not set, all the backups will be retained forever.'
    type: dict
  schedule:
    description:
    - Identifier of the schedule This parameter is mandatory.
    required: true
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
"""

# This structure describes the format of the data expected by the end-points
PAYLOAD_FORMAT = {
    "update": {
        "query": {},
        "body": {
            "backup_password": "spec/backup_password",
            "enable": "spec/enable",
            "location": "spec/location",
            "location_password": "spec/location_password",
            "location_user": "spec/location_user",
            "parts": "spec/parts",
            "recurrence_info": "spec/recurrence_info",
            "retention_info": "spec/retention_info",
        },
        "path": {"schedule": "schedule"},
    }
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

    argument_spec["backup_password"] = {"type": "str"}
    argument_spec["enable"] = {"type": "bool"}
    argument_spec["location"] = {"type": "str"}
    argument_spec["location_password"] = {"type": "str"}
    argument_spec["location_user"] = {"type": "str"}
    argument_spec["parts"] = {"type": "list", "elements": "str"}
    argument_spec["recurrence_info"] = {"type": "dict"}
    argument_spec["retention_info"] = {"type": "dict"}
    argument_spec["schedule"] = {"type": "str"}

    return argument_spec


async def main():
    required_if = list([["state", None, ["schedule"], True],])

    module_args = prepare_argument_spec()
    module = AnsibleModule(
        argument_spec=module_args, required_if=required_if, supports_check_mode=True
    )
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


# template: default_module.j2
def build_url(params):
    return (
        "https://{vcenter_hostname}"
        "/rest/appliance/recovery/backup/schedules/update/{schedule}"
    ).format(**params)


async def entry_point(module, session):

    func = globals()["_update"]

    return await func(module.params, session)


async def _update(params, session):
    payload = prepare_payload(params, PAYLOAD_FORMAT["update"])
    _url = (
        "https://{vcenter_hostname}"
        "/rest/appliance/recovery/backup/schedules/update/{schedule}"
    ).format(**params)
    async with session.get(_url) as resp:
        _json = await resp.json()
        for k, v in _json["value"].items():
            if k in payload and payload[k] == v:
                del payload[k]
            elif "spec" in payload:
                if k in payload["spec"] and payload["spec"][k] == v:
                    del payload["spec"][k]

        if payload == {} or payload == {"spec": {}}:
            # Nothing has changed
            _json["id"] = params.get("schedule")
            return await update_changed_flag(_json, resp.status, "get")
    async with session.put(_url, json=payload) as resp:
        try:
            if resp.headers["Content-Type"] == "application/json":
                _json = await resp.json()
        except KeyError:
            _json = {}
        _json["id"] = params.get("schedule")
        return await update_changed_flag(_json, resp.status, "update")


if __name__ == "__main__":
    import asyncio

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
