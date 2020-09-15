#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = """
module: vcenter_host
short_description: Handle resource of type vcenter_host
description: Handle resource of type vcenter_host
options:
  folder:
    description:
    - Host and cluster folder in which the new standalone host should be created.
    - This field is currently required. In the future, if this field is unset, the
      system will attempt to choose a suitable folder for the host; if a folder cannot
      be chosen, the host creation operation will fail.
    - 'When clients pass a value of this structure as a parameter, the field must
      be an identifier for the resource type: Folder. When operations return a value
      of this structure as a result, the field will be an identifier for the resource
      type: Folder.'
    type: str
  force_add:
    description:
    - Whether host should be added to the vCenter Server even if it is being managed
      by another vCenter Server. The original vCenterServer loses connection to the
      host.
    - If unset, forceAdd is default to false.
    type: bool
  host:
    description:
    - Identifier of the host to be deleted.
    - 'The parameter must be an identifier for the resource type: HostSystem. Required
      with I(state=[''absent''])'
    type: str
  hostname:
    description:
    - The IP address or DNS resolvable name of the host. Required with I(state=['present'])
    type: str
  password:
    description:
    - The password for the administrator account on the host. Required with I(state=['present'])
    type: str
  port:
    description:
    - The port of the host.
    - If unset, port 443 will be used.
    type: int
  state:
    choices:
    - absent
    - present
    default: present
    description: []
    type: str
  thumbprint:
    description:
    - 'The thumbprint of the SSL certificate, which the host is expected to have.
      The thumbprint is always computed using the SHA1 hash and is the string representation
      of that hash in the format: xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx
      where, ''x'' represents a hexadecimal digit.'
    - This field is optional and it is only relevant when the value of Host.CreateSpec.thumbprint-verification
      is THUMBPRINT.
    type: str
  thumbprint_verification:
    choices:
    - NONE
    - THUMBPRINT
    description:
    - The Host.CreateSpec.ThumbprintVerification enumerated type defines the thumbprint
      verification schemes for a host's SSL certificate. Required with I(state=['present'])
    type: str
  user_name:
    description:
    - The administrator account on the host. Required with I(state=['present'])
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
- name: define ESXi list
  set_fact:
    my_esxis:
    - hostname: "{{ lookup('env', 'ESXI1_HOSTNAME') }}"
      username: "{{ lookup('env', 'ESXI1_USERNAME') }}"
      password: "{{ lookup('env', 'ESXI1_PASSWORD') }}"
- name: Look up the different folders
  set_fact:
    my_virtual_machine_folder: '{{ my_folders.value|selectattr("type", "equalto",
      "VIRTUAL_MACHINE")|first }}'
    my_datastore_folder: '{{ my_folders.value|selectattr("type", "equalto", "DATASTORE")|first
      }}'
    my_host_folder: '{{ my_folders.value|selectattr("type", "equalto", "HOST")|first
      }}'
- name: Connect the host(s)
  vcenter_host:
    hostname: '{{ item.hostname }}'
    password: '{{ item.password }}'
    user_name: '{{ item.username }}'
    thumbprint_verification: NONE
    folder: '{{ my_host_folder.folder }}'
  no_log: true
  with_items: '{{ my_esxis}}'
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

    argument_spec["folder"] = {"type": "str"}
    argument_spec["force_add"] = {"type": "bool"}
    argument_spec["host"] = {"type": "str"}
    argument_spec["hostname"] = {"type": "str"}
    argument_spec["password"] = {"no_log": True, "type": "str"}
    argument_spec["port"] = {"type": "int"}
    argument_spec["state"] = {
        "type": "str",
        "choices": ["absent", "present"],
        "default": "present",
    }
    argument_spec["thumbprint"] = {"type": "str"}
    argument_spec["thumbprint_verification"] = {
        "type": "str",
        "choices": ["NONE", "THUMBPRINT"],
    }
    argument_spec["user_name"] = {"no_log": True, "type": "str"}

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

    return ("https://{vcenter_hostname}" "/rest/vcenter/host").format(**params)


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
    if params["host"]:
        _json = await get_device_info(
            params, session, build_url(params), params["host"]
        )
    else:
        _json = await exists(params, session, build_url(params), ["host"])
    if _json:
        if "_update" in globals():
            params["host"] = _json["id"]
            return await globals()["_update"](params, session)
        else:
            return await update_changed_flag(_json, 200, "get")
    payload = prepare_payload(params, PAYLOAD_FORMAT["create"])
    _url = "https://{vcenter_hostname}/rest/vcenter/host".format(**params)
    async with session.post(_url, json=payload) as resp:
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
    _in_query_parameters = PAYLOAD_FORMAT["delete"]["query"].keys()
    payload = payload = prepare_payload(params, PAYLOAD_FORMAT["delete"])
    subdevice_type = get_subdevice_type("/rest/vcenter/host/{host}")
    if subdevice_type and (not params[subdevice_type]):
        _json = await exists(params, session, build_url(params))
        if _json:
            params[subdevice_type] = _json["id"]
    _url = "https://{vcenter_hostname}/rest/vcenter/host/{host}".format(
        **params
    ) + gen_args(params, _in_query_parameters)
    async with session.delete(_url, json=payload) as resp:
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
