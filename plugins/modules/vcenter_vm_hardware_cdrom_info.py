#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = """
module: vcenter_vm_hardware_cdrom_info
short_description: Handle resource of type vcenter_vm_hardware_cdrom
description: Handle resource of type vcenter_vm_hardware_cdrom
options:
  cdrom:
    description:
    - Virtual CD-ROM device identifier.
    - 'The parameter must be an identifier for the resource type: vcenter.vm.hardware.Cdrom.
      Required with I(state=[''get''])'
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
  vm:
    description:
    - Virtual machine identifier.
    - 'The parameter must be an identifier for the resource type: VirtualMachine.'
    type: str
author:
- Goneri Le Bouder (@goneri) <goneri@lebouder.net>
version_added: 1.0.0
requirements:
- python >= 3.6
- aiohttp
"""

EXAMPLES = """
"""

# This structure describes the format of the data expected by the end-points
PAYLOAD_FORMAT = {
    "list": {"query": {}, "body": {}, "path": {"vm": "vm"}},
    "create": {
        "query": {},
        "body": {
            "allow_guest_control": "spec/allow_guest_control",
            "backing": {
                "device_access_type": "spec/backing/device_access_type",
                "host_device": "spec/backing/host_device",
                "iso_file": "spec/backing/iso_file",
                "type": "spec/backing/type",
            },
            "ide": {"master": "spec/ide/master", "primary": "spec/ide/primary"},
            "sata": {"bus": "spec/sata/bus", "unit": "spec/sata/unit"},
            "start_connected": "spec/start_connected",
            "type": "spec/type",
        },
        "path": {"vm": "vm"},
    },
    "delete": {"query": {}, "body": {}, "path": {"vm": "vm", "cdrom": "cdrom"}},
    "get": {"query": {}, "body": {}, "path": {"vm": "vm", "cdrom": "cdrom"}},
    "update": {
        "query": {},
        "body": {
            "allow_guest_control": "spec/allow_guest_control",
            "backing": {
                "device_access_type": "spec/backing/device_access_type",
                "host_device": "spec/backing/host_device",
                "iso_file": "spec/backing/iso_file",
                "type": "spec/backing/type",
            },
            "start_connected": "spec/start_connected",
        },
        "path": {"vm": "vm", "cdrom": "cdrom"},
    },
    "connect": {"query": {}, "body": {}, "path": {"vm": "vm", "cdrom": "cdrom"}},
    "disconnect": {"query": {}, "body": {}, "path": {"vm": "vm", "cdrom": "cdrom"}},
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

    argument_spec["cdrom"] = {"type": "str"}
    argument_spec["vm"] = {"type": "str"}

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

    if params["cdrom"]:
        _in_query_parameters = PAYLOAD_FORMAT["get"]["query"].keys()
        return (
            "https://{vcenter_hostname}" "/rest/vcenter/vm/{vm}/hardware/cdrom/{cdrom}"
        ).format(**params) + gen_args(params, _in_query_parameters)
    else:
        _in_query_parameters = PAYLOAD_FORMAT["list"]["query"].keys()
        return (
            "https://{vcenter_hostname}" "/rest/vcenter/vm/{vm}/hardware/cdrom"
        ).format(**params) + gen_args(params, _in_query_parameters)


async def entry_point(module, session):
    async with session.get(build_url(module.params)) as resp:
        _json = await resp.json()
        if module.params.get("cdrom"):
            _json["id"] = module.params.get("cdrom")
        return await update_changed_flag(_json, resp.status, "get")


if __name__ == "__main__":
    import asyncio

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
