#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = """
module: vcenter_vmtemplate_libraryitems
short_description: Handle resource of type vcenter_vmtemplate_libraryitems
description: Handle resource of type vcenter_vmtemplate_libraryitems
options:
  action:
    choices:
    - deploy
    description:
    - action=deploy Required with I(state=['deploy'])
    type: str
  description:
    description:
    - Description of the deployed virtual machine.
    type: str
  disk_storage:
    description:
    - Storage specification for the virtual machine template's disks.
    - 'Validate attributes are:'
    - ' - C(datastore) (str): Identifier for the datastore associated with a virtual
      machine template''s disk.'
    - ' - C(storage_policy) (dict): Storage policy for a virtual machine template''s
      disk.'
    type: dict
  disk_storage_overrides:
    description:
    - Storage specification for individual disks in the deployed virtual machine.
      This is specified as a mapping between disk identifiers in the source virtual
      machine template contained in the library item and their storage specifications.
    type: list
  guest_customization:
    description:
    - Guest customization spec to apply to the deployed virtual machine.
    - 'Validate attributes are:'
    - ' - C(name) (str): Name of the customization specification.'
    type: dict
  hardware_customization:
    description:
    - Hardware customization spec which specifies updates to the deployed virtual
      machine.
    - 'Validate attributes are:'
    - ' - C(cpu_update) (dict): CPU update specification for the deployed virtual
      machine.'
    - ' - C(disks_to_remove) (list): Idenfiers of disks to remove from the deployed
      virtual machine.'
    - ' - C(disks_to_update) (list): Disk update specification for individual disks
      in the deployed virtual machine.'
    - ' - C(memory_update) (dict): Memory update specification for the deployed virtual
      machine.'
    - ' - C(nics) (list): Map of Ethernet network adapters to update.'
    type: dict
  library:
    description:
    - Identifier of the library in which the new library item should be created. Required
      with I(state=['create'])
    type: str
  name:
    description:
    - Name of the deployed virtual machine.
    type: str
  placement:
    description:
    - Information used to place the virtual machine template.
    - 'Validate attributes are:'
    - ' - C(cluster) (str): Cluster onto which the virtual machine template should
      be placed. If {@name #cluster} and {@name #resourcePool} are both specified,
      {@name #resourcePool} must belong to {@name #cluster}. If {@name #cluster} and
      {@name #host} are both specified, {@name #host} must be a member of {@name #cluster}.'
    - ' - C(folder) (str): Virtual machine folder into which the virtual machine template
      should be placed.'
    - ' - C(host) (str): Host onto which the virtual machine template should be placed.
      If {@name #host} and {@name #resourcePool} are both specified, {@name #resourcePool}
      must belong to {@name #host}. If {@name #host} and {@name #cluster} are both
      specified, {@name #host} must be a member of {@name #cluster}.'
    - ' - C(resource_pool) (str): Resource pool into which the virtual machine template
      should be placed.'
    type: dict
  powered_on:
    description:
    - Specifies whether the deployed virtual machine should be powered on after deployment.
    type: bool
  source_vm:
    description:
    - Identifier of the source virtual machine to create the library item from. Required
      with I(state=['create'])
    type: str
  state:
    choices:
    - create
    - deploy
    description: []
    type: str
  template_library_item:
    description:
    - identifier of the content library item containing the source virtual machine
      template to be deployed. Required with I(state=['deploy'])
    type: str
  vm_home_storage:
    description:
    - Storage location for the virtual machine template's configuration and log files.
    - 'Validate attributes are:'
    - ' - C(datastore) (str): Identifier of the datastore for the virtual machine
      template''s configuration and log files.'
    - ' - C(storage_policy) (dict): Storage policy for the virtual machine template''s
      configuration and log files.'
    type: dict
author:
- Ansible VMware team
version_added: 1.0.0
requirements:
- python >= 3.6
"""

IN_QUERY_PARAMETER = ["action"]

import socket
import json
from ansible.module_utils.basic import env_fallback

try:
    from ansible_module.turbo.module import AnsibleTurboModule as AnsibleModule
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

    argument_spec["action"] = {
        "type": "str",
        "choices": ["deploy"],
        "operationIds": ["deploy"],
    }
    argument_spec["description"] = {"type": "str", "operationIds": ["create", "deploy"]}
    argument_spec["disk_storage"] = {
        "type": "dict",
        "operationIds": ["create", "deploy"],
    }
    argument_spec["disk_storage_overrides"] = {
        "type": "list",
        "operationIds": ["create", "deploy"],
    }
    argument_spec["guest_customization"] = {"type": "dict", "operationIds": ["deploy"]}
    argument_spec["hardware_customization"] = {
        "type": "dict",
        "operationIds": ["deploy"],
    }
    argument_spec["library"] = {"type": "str", "operationIds": ["create"]}
    argument_spec["name"] = {"type": "str", "operationIds": ["create", "deploy"]}
    argument_spec["placement"] = {"type": "dict", "operationIds": ["create", "deploy"]}
    argument_spec["powered_on"] = {"type": "bool", "operationIds": ["deploy"]}
    argument_spec["source_vm"] = {"type": "str", "operationIds": ["create"]}
    argument_spec["state"] = {"type": "str", "choices": ["create", "deploy"]}
    argument_spec["template_library_item"] = {"type": "str", "operationIds": ["deploy"]}
    argument_spec["vm_home_storage"] = {
        "type": "dict",
        "operationIds": ["create", "deploy"],
    }

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

    return "https://{vcenter_hostname}/rest/vcenter/vm-template/library-items".format(
        **params
    )


async def entry_point(module, session):
    func = globals()[("_" + module.params["state"])]
    return await func(module.params, session)


async def _create(params, session):
    accepted_fields = [
        "description",
        "disk_storage",
        "disk_storage_overrides",
        "library",
        "name",
        "placement",
        "source_vm",
        "vm_home_storage",
    ]
    if "create" == "create":
        _exists = await exists(params, session)
        if _exists:
            return await update_changed_flag({"value": _exists}, 200, "get")
    spec = {}
    for i in accepted_fields:
        if params[i]:
            spec[i] = params[i]
    _url = "https://{vcenter_hostname}/rest/vcenter/vm-template/library-items".format(
        **params
    )
    async with session.post(_url, json={"spec": spec}) as resp:
        try:
            if resp.headers["Content-Type"] == "application/json":
                _json = await resp.json()
        except KeyError:
            _json = {}
        if (
            ("create" == "create")
            and (resp.status in [200, 201])
            and ("value" in _json)
        ):
            if isinstance(_json["value"], dict):
                _id = list(_json["value"].values())[0]
            else:
                _id = _json["value"]
            _json = {"value": (await get_device_info(params, session, _url, _id))}
        return await update_changed_flag(_json, resp.status, "create")


async def _deploy(params, session):
    accepted_fields = [
        "description",
        "disk_storage",
        "disk_storage_overrides",
        "guest_customization",
        "hardware_customization",
        "name",
        "placement",
        "powered_on",
        "vm_home_storage",
    ]
    if "deploy" == "create":
        _exists = await exists(params, session)
        if _exists:
            return await update_changed_flag({"value": _exists}, 200, "get")
    spec = {}
    for i in accepted_fields:
        if params[i]:
            spec[i] = params[i]
    _url = "https://{vcenter_hostname}/rest/vcenter/vm-template/library-items/{template_library_item}".format(
        **params
    )
    async with session.post(_url, json={"spec": spec}) as resp:
        try:
            if resp.headers["Content-Type"] == "application/json":
                _json = await resp.json()
        except KeyError:
            _json = {}
        if (
            ("deploy" == "create")
            and (resp.status in [200, 201])
            and ("value" in _json)
        ):
            if isinstance(_json["value"], dict):
                _id = list(_json["value"].values())[0]
            else:
                _id = _json["value"]
            _json = {"value": (await get_device_info(params, session, _url, _id))}
        return await update_changed_flag(_json, resp.status, "deploy")


if __name__ == "__main__":
    import asyncio

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
