#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2021, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# template: header.j2

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = r"""
module: appliance_localaccounts
short_description: Update selected fields in local user account properties.
description: Update selected fields in local user account properties.
options:
  config:
    description:
    - User configuration Required with I(state=['present'])
    - 'Valid attributes are:'
    - ' - C(password) (str): Password'
    - ' - C(old_password) (str): Old password of the user (required in case of the
      password change, not required if superAdmin user changes the password of the
      other user)'
    - ' - C(full_name) (str): Full name of the user'
    - ' - C(email) (str): Email address of the local account'
    - ' - C(roles) (list): User roles'
    - ' - C(enabled) (bool): Flag indicating if the account is enabled'
    - ' - C(password_expires) (bool): Flag indicating if the account password expires'
    - ' - C(password_expires_at) (str): Date when the account''s password will expire'
    - ' - C(inactive_after_password_expiration) (bool): Flag indicating if the account
      will be locked after password expiration'
    - ' - C(days_after_password_expiration) (int): Number of days after password expiration
      before the account will be locked'
    - ' - C(min_days_between_password_change) (int): Minimum number of days between
      password change'
    - ' - C(max_days_between_password_change) (int): Maximum number of days between
      password change'
    - ' - C(warn_days_before_password_expiration) (int): Number of days of warning
      before password expires'
    type: dict
  days_after_password_expiration:
    description:
    - Number of days after password expiration before the account will be locked
    type: int
  email:
    description:
    - Email address of the local account
    type: str
  enabled:
    description:
    - Flag indicating if the account is enabled
    type: bool
  full_name:
    description:
    - Full name of the user
    type: str
  inactive_after_password_expiration:
    description:
    - Flag indicating if the account will be locked after password expiration
    type: bool
  max_days_between_password_change:
    description:
    - Maximum number of days between password change
    type: int
  min_days_between_password_change:
    description:
    - Minimum number of days between password change
    type: int
  old_password:
    description:
    - Old password of the user (required in case of the password change, not required
      if superAdmin user changes the password of the other user)
    type: str
  password:
    description:
    - Password Required with I(state=['present', 'set'])
    type: str
  password_expires:
    description:
    - Flag indicating if the account password expires
    type: bool
  password_expires_at:
    description:
    - Date when the account's password will expire
    type: str
  roles:
    description:
    - User roles Required with I(state=['present', 'set'])
    elements: str
    type: list
  state:
    choices:
    - absent
    - present
    - set
    default: present
    description: []
    type: str
  username:
    description:
    - User login name This parameter is mandatory.
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
  warn_days_before_password_expiration:
    description:
    - Number of days of warning before password expires
    type: int
author:
- Ansible Cloud Team (@ansible-collections)
version_added: 1.0.0
requirements:
- python >= 3.6
- aiohttp
"""

EXAMPLES = r"""
- name: Add a local accounts
  vmware.vmware_rest.appliance_localaccounts:
    username: foobar
    config:
      full_name: Foobar
      email: foobar@vsphere.local
      password: Foobar56^$7
      roles:
      - operator
      - admin
      - superAdmin
    state: present
  register: result
- name: Add a local accounts (idempotency)
  vmware.vmware_rest.appliance_localaccounts:
    username: foobar
    config:
      full_name: Foobar
      email: foobar@vsphere.local
      # password: foobar
      roles:
      - operator
      - admin
      - superAdmin
    state: present
  register: result
- name: Change account email address
  vmware.vmware_rest.appliance_localaccounts:
    username: foobar
    config:
      full_name: Foobar
      email: foobar2@vsphere.local
      roles:
      - operator
      - admin
      - superAdmin
    state: present
  register: result
- name: Delete a local accounts
  vmware.vmware_rest.appliance_localaccounts:
    username: foobar
    state: absent
  register: result
"""

RETURN = r"""
# content generated by the update_return_section callback# task: Change account email address
id:
  description: moid of the resource
  returned: On success
  sample: VALUE_SPECIFIED_IN_NO_LOG_PARAMETER
  type: str
value:
  description: Change account email address
  returned: On success
  sample:
    email: '********@vsphere.local'
    enabled: 1
    fullname: Foobar
    has_password: 1
    last_password_change: '2021-04-27T00:00:00.000Z'
    max_days_between_password_change: -1
    min_days_between_password_change: -1
    roles:
    - operator
    warn_days_before_password_expiration: 5
  type: dict
"""

# This structure describes the format of the data expected by the end-points
PAYLOAD_FORMAT = {
    "create": {
        "query": {},
        "body": {"config": "config", "username": "username"},
        "path": {},
    },
    "list": {"query": {}, "body": {}, "path": {}},
    "set": {
        "query": {},
        "body": {
            "days_after_password_expiration": "days_after_password_expiration",
            "email": "email",
            "enabled": "enabled",
            "full_name": "full_name",
            "inactive_after_password_expiration": "inactive_after_password_expiration",
            "max_days_between_password_change": "max_days_between_password_change",
            "min_days_between_password_change": "min_days_between_password_change",
            "old_password": "old_password",
            "password": "password",
            "password_expires": "password_expires",
            "password_expires_at": "password_expires_at",
            "roles": "roles",
            "warn_days_before_password_expiration": "warn_days_before_password_expiration",
        },
        "path": {"username": "username"},
    },
    "get": {"query": {}, "body": {}, "path": {"username": "username"}},
    "update": {
        "query": {},
        "body": {
            "days_after_password_expiration": "days_after_password_expiration",
            "email": "email",
            "enabled": "enabled",
            "full_name": "full_name",
            "inactive_after_password_expiration": "inactive_after_password_expiration",
            "max_days_between_password_change": "max_days_between_password_change",
            "min_days_between_password_change": "min_days_between_password_change",
            "old_password": "old_password",
            "password": "password",
            "password_expires": "password_expires",
            "password_expires_at": "password_expires_at",
            "roles": "roles",
            "warn_days_before_password_expiration": "warn_days_before_password_expiration",
        },
        "path": {"username": "username"},
    },
    "delete": {"query": {}, "body": {}, "path": {"username": "username"}},
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

    argument_spec["config"] = {"type": "dict"}
    argument_spec["days_after_password_expiration"] = {"no_log": True, "type": "int"}
    argument_spec["email"] = {"type": "str"}
    argument_spec["enabled"] = {"type": "bool"}
    argument_spec["full_name"] = {"type": "str"}
    argument_spec["inactive_after_password_expiration"] = {
        "no_log": True,
        "type": "bool",
    }
    argument_spec["max_days_between_password_change"] = {"no_log": True, "type": "int"}
    argument_spec["min_days_between_password_change"] = {"no_log": True, "type": "int"}
    argument_spec["old_password"] = {"no_log": True, "type": "str"}
    argument_spec["password"] = {"no_log": True, "type": "str"}
    argument_spec["password_expires"] = {"no_log": True, "type": "bool"}
    argument_spec["password_expires_at"] = {"no_log": True, "type": "str"}
    argument_spec["roles"] = {"type": "list", "elements": "str"}
    argument_spec["state"] = {
        "type": "str",
        "choices": ["absent", "present", "set"],
        "default": "present",
    }
    argument_spec["username"] = {"no_log": True, "required": True, "type": "str"}
    argument_spec["warn_days_before_password_expiration"] = {
        "no_log": True,
        "type": "int",
    }

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


# template: default_module.j2
def build_url(params):
    return ("https://{vcenter_hostname}" "/api/appliance/local-accounts").format(
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


async def _create(params, session):

    if params["username"]:
        _json = await get_device_info(session, build_url(params), params["username"])
    else:
        _json = await exists(params, session, build_url(params), ["username"])
    if _json:
        if "value" not in _json:  # 7.0.2+
            _json = {"value": _json}
        if "_update" in globals():
            params["username"] = _json["id"]
            return await globals()["_update"](params, session)
        return await update_changed_flag(_json, 200, "get")

    payload = prepare_payload(params, PAYLOAD_FORMAT["create"])
    _url = ("https://{vcenter_hostname}" "/api/appliance/local-accounts").format(
        **params
    )
    async with session.post(_url, json=payload) as resp:
        if resp.status == 500:
            text = await resp.text()
            raise EmbeddedModuleFailure(
                f"Request has failed: status={resp.status}, {text}"
            )
        try:
            if resp.headers["Content-Type"] == "application/json":
                _json = await resp.json()
        except KeyError:
            _json = {}

        if resp.status in [200, 201]:
            if isinstance(_json, str):  # 7.0.2 and greater
                _id = _json  # TODO: fetch the object
            elif isinstance(_json, dict) and "value" not in _json:
                _id = list(_json["value"].values())[0]
            elif isinstance(_json, dict) and "value" in _json:
                _id = _json["value"]
            _json_device_info = await get_device_info(session, _url, _id)
            if _json_device_info:
                _json = _json_device_info

        return await update_changed_flag(_json, resp.status, "create")


async def _delete(params, session):
    _in_query_parameters = PAYLOAD_FORMAT["delete"]["query"].keys()
    payload = prepare_payload(params, PAYLOAD_FORMAT["delete"])
    subdevice_type = get_subdevice_type("/api/appliance/local-accounts/{username}")
    if subdevice_type and not params[subdevice_type]:
        _json = await exists(params, session, build_url(params))
        if _json:
            params[subdevice_type] = _json["id"]
    _url = (
        "https://{vcenter_hostname}" "/api/appliance/local-accounts/{username}"
    ).format(**params) + gen_args(params, _in_query_parameters)
    async with session.delete(_url, json=payload) as resp:
        try:
            if resp.headers["Content-Type"] == "application/json":
                _json = await resp.json()
        except KeyError:
            _json = {}
        return await update_changed_flag(_json, resp.status, "delete")


async def _set(params, session):
    _in_query_parameters = PAYLOAD_FORMAT["set"]["query"].keys()
    payload = prepare_payload(params, PAYLOAD_FORMAT["set"])
    subdevice_type = get_subdevice_type("/api/appliance/local-accounts/{username}")
    if subdevice_type and not params[subdevice_type]:
        _json = await exists(params, session, build_url(params))
        if _json:
            params[subdevice_type] = _json["id"]
    _url = (
        "https://{vcenter_hostname}" "/api/appliance/local-accounts/{username}"
    ).format(**params) + gen_args(params, _in_query_parameters)
    async with session.get(_url, json=payload) as resp:
        before = await resp.json()

    async with session.put(_url, json=payload) as resp:
        try:
            if resp.headers["Content-Type"] == "application/json":
                _json = await resp.json()
        except KeyError:
            _json = {}
        if "value" not in _json:  # 7.0.2
            _json = {"value": _json}
        # The PUT answer does not let us know if the resource has actually been
        # modified
        async with session.get(_url, json=payload) as resp_get:
            after = await resp_get.json()
            if before == after:
                return await update_changed_flag(after, resp_get.status, "get")
        return await update_changed_flag(_json, resp.status, "set")


async def _update(params, session):
    payload = prepare_payload(params, PAYLOAD_FORMAT["update"])
    _url = (
        "https://{vcenter_hostname}" "/api/appliance/local-accounts/{username}"
    ).format(**params)
    async with session.get(_url) as resp:
        _json = await resp.json()
        if "value" in _json:
            value = _json["value"]
        else:  # 7.0.2 and greater
            value = _json
        for k, v in value.items():
            if k in payload and payload[k] == v:
                del payload[k]
            elif "spec" in payload:
                if k in payload["spec"] and payload["spec"][k] == v:
                    del payload["spec"][k]

        if payload == {} or payload == {"spec": {}}:
            # Nothing has changed
            if "value" not in _json:  # 7.0.2
                _json = {"value": _json}
            _json["id"] = params.get("username")
            return await update_changed_flag(_json, resp.status, "get")
    async with session.patch(_url, json=payload) as resp:
        try:
            if resp.headers["Content-Type"] == "application/json":
                _json = await resp.json()
        except KeyError:
            _json = {}
        if "value" not in _json:  # 7.0.2
            _json = {"value": _json}
        _json["id"] = params.get("username")
        return await update_changed_flag(_json, resp.status, "update")


if __name__ == "__main__":
    import asyncio

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
