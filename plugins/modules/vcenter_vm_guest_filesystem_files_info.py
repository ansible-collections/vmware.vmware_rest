#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2021, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# template: header.j2

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = r"""
module: vcenter_vm_guest_filesystem_files_info
short_description: Returns information about a file or directory in the guest
description: Returns information about a file or directory in the guest. <p>
options:
  credentials:
    description:
    - The guest authentication data.  See {@link Credentials}. This parameter is mandatory.
    - 'Valid attributes are:'
    - ' - C(interactive_session) (bool): If {@term set}, the {@term operation} will
      interact with the logged-in desktop session in the guest. This requires that
      the logged-on user matches the user specified by the {@link Credentials}. This
      is currently only supported for {@link Type#USERNAME_PASSWORD}.'
    - ' - C(type) (str): Types of guest credentials'
    - '   - Accepted values:'
    - '     - USERNAME_PASSWORD'
    - '     - SAML_BEARER_TOKEN'
    - ' - C(user_name) (str): For {@link Type#SAML_BEARER_TOKEN}, this is the guest
      user to be associated with the credentials. For {@link Type#USERNAME_PASSWORD}
      this is the guest username.'
    - ' - C(password) (str): password'
    - ' - C(saml_token) (str): SAML Bearer Token'
    required: true
    type: dict
  filter:
    description:
    - Specification to match files for which information should be returned.
    - 'Valid attributes are:'
    - ' - C(match_pattern) (str): The perl-compatible regular expression used to filter
      the returned files.'
    type: dict
  iteration:
    description:
    - The specification of a page of results to be retrieved.
    - 'Valid attributes are:'
    - ' - C(size) (int): Specifies the maximum number of results to return.'
    - ' - C(index) (int): Which result to start the list with. If this value exceeds
      the number of results, an empty list will be returned.'
    type: dict
  path:
    description:
    - The complete path to the directory or file to query. This parameter is mandatory.
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
  vm:
    description:
    - Virtual Machine to perform the operation on. This parameter is mandatory.
    required: true
    type: str
author:
- Ansible Cloud Team (@ansible-collections)
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
    "delete": {
        "query": {},
        "body": {"credentials": "credentials"},
        "path": {"path": "path", "vm": "vm"},
    },
    "get": {
        "query": {},
        "body": {"credentials": "credentials"},
        "path": {"path": "path", "vm": "vm"},
    },
    "create_temporary": {
        "query": {},
        "body": {
            "credentials": "credentials",
            "parent_path": "parent_path",
            "prefix": "prefix",
            "suffix": "suffix",
        },
        "path": {"vm": "vm"},
    },
    "list": {
        "query": {},
        "body": {
            "credentials": "credentials",
            "filter": "filter",
            "iteration": "iteration",
            "path": "path",
        },
        "path": {"vm": "vm"},
    },
    "move": {
        "query": {},
        "body": {
            "credentials": "credentials",
            "new_path": "new_path",
            "overwrite": "overwrite",
            "path": "path",
        },
        "path": {"vm": "vm"},
    },
    "update": {
        "query": {},
        "body": {
            "credentials": "credentials",
            "file_attributes": "file_attributes",
            "path": "path",
        },
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

    argument_spec["credentials"] = {"required": True, "type": "dict"}
    argument_spec["filter"] = {"type": "dict"}
    argument_spec["iteration"] = {"type": "dict"}
    argument_spec["path"] = {"required": True, "type": "str"}
    argument_spec["vm"] = {"required": True, "type": "str"}

    return argument_spec


async def main():
    required_if = list([])

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


# template: info_list_and_get_module.j2
def build_url(params):
    _in_query_parameters = PAYLOAD_FORMAT["list"]["query"].keys()
    return (
        "https://{vcenter_hostname}"
        "/api/vcenter/vm/{vm}/guest/filesystem/files?action=list"
    ).format(**params) + gen_args(params, _in_query_parameters)


async def entry_point(module, session):
    url = build_url(module.params)
    async with session.get(url) as resp:
        _json = await resp.json()

        if "value" not in _json:  # 7.0.2+
            _json = {"value": _json}

        return await update_changed_flag(_json, resp.status, "get")


if __name__ == "__main__":
    import asyncio

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
