#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2021, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# template: header.j2

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = r"""
module: vcenter_vm_storage_policy
short_description: Manage the storage policy of a VM
description: Manage the storage policy of a VM
options:
  disks:
    description:
    - Storage policy or policies to be used when reconfiguring virtual machine diks.
    - if unset the current storage policy is retained.
    - 'When clients pass a value of this structure as a parameter, the key in the
      field map must be the id of a resource returned by M(vcenter_vm_hardware_disk). '
    - 'Valid attributes are:'
    - ' - C(key) (str): '
    - ' - C(value) (dict): '
    - '   - Accepted keys:'
    - '     - policy (string): Storage Policy identification.'
    - This field is optional and it is only relevant when the value of I(type) is
      USE_SPECIFIED_POLICY.
    - 'When clients pass a value of this structure as a parameter, the field must
      be the id of a resource returned by M(vcenter_storage_policies). '
    - '     - type (string): This option defines the choices for how to specify the
      policy to be associated with a virtual disk.'
    - 'Accepted value for this field:'
    - '       - C(USE_SPECIFIED_POLICY)'
    - '       - C(USE_DEFAULT_POLICY)'
    elements: dict
    type: list
  state:
    choices:
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
  vm:
    description:
    - Virtual machine identifier.
    - The parameter must be the id of a resource returned by M(vcenter_vm_info). This
      parameter is mandatory.
    required: true
    type: str
  vm_home:
    description:
    - Storage policy to be used when reconfiguring the virtual machine home.
    - if unset the current storage policy is retained.
    - 'Valid attributes are:'
    - ' - C(policy) (str): Storage Policy identification.'
    - This field is optional and it is only relevant when the value of I(type) is
      USE_SPECIFIED_POLICY.
    - 'When clients pass a value of this structure as a parameter, the field must
      be the id of a resource returned by M(vcenter_storage_policies). '
    - ' - C(type) (str): This option defines the choices for how to specify the policy
      to be associated with the virtual machine home''s directory.'
    - '   - Accepted values:'
    - '     - USE_SPECIFIED_POLICY'
    - '     - USE_DEFAULT_POLICY'
    type: dict
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
    "get": {"query": {}, "body": {}, "path": {"vm": "vm"}},
    "update": {
        "query": {},
        "body": {"disks": "spec/disks", "vm_home": "spec/vm_home"},
        "path": {"vm": "vm"},
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

    argument_spec["disks"] = {"type": "list", "elements": "dict"}
    argument_spec["state"] = {
        "type": "str",
        "choices": ["present"],
        "default": "present",
    }
    argument_spec["vm"] = {"required": True, "type": "str"}
    argument_spec["vm_home"] = {"type": "dict"}

    return argument_spec


async def main():
    required_if = list([["state", None, ["vm"], True],])

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
    return ("https://{vcenter_hostname}" "/rest/vcenter/vm/{vm}/storage/policy").format(
        **params
    )


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


async def _update(params, session):
    payload = prepare_payload(params, PAYLOAD_FORMAT["update"])
    _url = ("https://{vcenter_hostname}" "/rest/vcenter/vm/{vm}/storage/policy").format(
        **params
    )
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
            _json["id"] = params.get("None")
            return await update_changed_flag(_json, resp.status, "get")
    async with session.patch(_url, json=payload) as resp:
        try:
            if resp.headers["Content-Type"] == "application/json":
                _json = await resp.json()
        except KeyError:
            _json = {}
        _json["id"] = params.get("None")
        return await update_changed_flag(_json, resp.status, "update")


if __name__ == "__main__":
    import asyncio

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
