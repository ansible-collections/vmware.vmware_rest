#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = """
module: vcenter_datacenter
short_description: Handle resource of type vcenter_datacenter
description: Handle resource of type vcenter_datacenter
options:
  datacenter:
    description:
    - Identifier of the datacenter to be deleted.
    - 'The parameter must be an identifier for the resource type: Datacenter. Required
      with I(state=[''delete''])'
    type: str
  folder:
    description:
    - Datacenter folder in which the new datacenter should be created.
    - This field is currently required. In the future, if this field is unset, the
      system will attempt to choose a suitable folder for the datacenter; if a folder
      cannot be chosen, the datacenter creation operation will fail.
    - 'When clients pass a value of this structure as a parameter, the field must
      be an identifier for the resource type: Folder. When operations return a value
      of this structure as a result, the field will be an identifier for the resource
      type: Folder.'
    type: str
  force:
    description:
    - If true, delete the datacenter even if it is not empty.
    - If unset a ResourceInUse error will be reported if the datacenter is not empty.
      This is the equivalent of passing the value false.
    type: bool
  name:
    description:
    - The name of the datacenter to be created. Required with I(state=['create'])
    type: str
  state:
    choices:
    - absent
    - present
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
- name: Get a list of all the datacenters
  register: existing_datacenters
  vcenter_datacenter_info:
- set_fact:
    my_datacenter_folder: '{{ my_folders.value|selectattr("type", "equalto", "DATACENTER")|first
      }}'
- name: Create datacenter my_dc
  vcenter_datacenter:
    name: my_dc
    folder: '{{ my_datacenter_folder.folder }}'
- name: Create datacenter my_dc (again)
  vcenter_datacenter:
    name: my_dc
    folder: '{{ my_datacenter_folder.folder }}'
- name: Force delete the existing DC
  vcenter_datacenter:
    state: absent
    datacenter: '{{ item.datacenter }}'
    force: true
  with_items: '{{ existing_datacenters.value }}'
"""

IN_QUERY_PARAMETER = ["force"]

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
    get_device_info,
    list_devices,
    exists,
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

    argument_spec["datacenter"] = {"type": "str"}
    argument_spec["folder"] = {"type": "str"}
    argument_spec["force"] = {"type": "bool"}
    argument_spec["name"] = {"type": "str"}
    argument_spec["state"] = {
        "type": "str",
        "choices": ["absent", "present"],
        "default": "present",
    }

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

    return ("https://{vcenter_hostname}" "/rest/vcenter/datacenter").format(**params)


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
    func = globals()[("_" + operation)]
    return await func(module.params, session)


async def _create(params, session):
    accepted_fields = ["folder", "name"]
    _json = await exists(params, session, build_url(params))
    if _json:
        if "_update" in globals():
            params["datacenter"] = _json["id"]
            return await _update(params, session)
        else:
            return await update_changed_flag(_json, 200, "get")
    spec = {}
    for i in accepted_fields:
        if params[i]:
            spec[i] = params[i]
    _url = "https://{vcenter_hostname}/rest/vcenter/datacenter".format(**params)
    async with session.post(_url, json={"spec": spec}) as resp:
        try:
            if resp.headers["Content-Type"] == "application/json":
                _json = await resp.json()
        except KeyError:
            _json = {}
        if (resp.status in [200, 201]) and ("value" in _json):
            if isinstance(_json["value"], dict):
                _id = list(_json["value"].values())[0]
            else:
                _id = _json["value"]
            _json = await get_device_info(params, session, _url, _id)
        return await update_changed_flag(_json, resp.status, "create")


async def _delete(params, session):
    _url = "https://{vcenter_hostname}/rest/vcenter/datacenter/{datacenter}".format(
        **params
    ) + gen_args(params, IN_QUERY_PARAMETER)
    async with session.delete(_url) as resp:
        try:
            if resp.headers["Content-Type"] == "application/json":
                _json = await resp.json()
        except KeyError:
            _json = {}
        return await update_changed_flag(_json, resp.status, "delete")


if __name__ == "__main__":
    import asyncio

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
