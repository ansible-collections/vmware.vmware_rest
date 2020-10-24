#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# template: DEFAULT_MODULE

DOCUMENTATION = """
module: vcenter_vm_hardware_disk
short_description: Manage the disk of a VM
description: Manage the disk of a VM
options:
  backing:
    description:
    - Existing physical resource backing for the virtual disk. Exactly one of I(backing)
      or I(new_vmdk) must be specified.
    - If unset, the virtual disk will not be connected to an existing backing.
    - 'Valide attributes are:'
    - ' - C(type) (str): This option defines the valid backing types for a virtual
      disk.'
    - '   - Accepted values:'
    - '     - VMDK_FILE'
    - ' - C(vmdk_file) (str): Path of the VMDK file backing the virtual disk.'
    - This field is optional and it is only relevant when the value of I(type) is
      VMDK_FILE.
    type: dict
  disk:
    description:
    - Virtual disk identifier.
    - The parameter must be the id of a resource returned by M(vcenter_vm_hardware_disk).
      Required with I(state=['absent'])
    type: str
  ide:
    description:
    - Address for attaching the device to a virtual IDE adapter.
    - If unset, the server will choose an available address; if none is available,
      the request will fail.
    - 'Valide attributes are:'
    - ' - C(master) (bool): Flag specifying whether the device should be the master
      or slave device on the IDE adapter.'
    - If unset, the server will choose an available connection type. If no IDE connections
      are available, the request will be rejected.
    - ' - C(primary) (bool): Flag specifying whether the device should be attached
      to the primary or secondary IDE adapter of the virtual machine.'
    - If unset, the server will choose a adapter with an available connection. If
      no IDE connections are available, the request will be rejected.
    type: dict
  label:
    description: []
    type: str
  new_vmdk:
    description:
    - Specification for creating a new VMDK backing for the virtual disk. Exactly
      one of I(backing) or I(new_vmdk) must be specified.
    - If unset, a new VMDK backing will not be created.
    - 'Valide attributes are:'
    - ' - C(capacity) (int): Capacity of the virtual disk backing in bytes.'
    - If unset, defaults to a guest-specific capacity.
    - ' - C(name) (str): Base name of the VMDK file. The name should not include the
      ''.vmdk'' file extension.'
    - If unset, a name (derived from the name of the virtual machine) will be chosen
      by the server.
    - ' - C(storage_policy) (dict): The I(storage_policy_spec) structure contains
      information about the storage policy that is to be associated the with VMDK
      file.'
    - 'If unset the default storage policy of the target datastore (if applicable)
      is applied. Currently a default storage policy is only supported by object based
      datastores : VVol & vSAN. For non- object datastores, if unset then no storage
      policy would be associated with the VMDK file.'
    - '   - Accepted keys:'
    - '     - policy (string): Identifier of the storage policy which should be associated
      with the VMDK file.'
    - 'When clients pass a value of this structure as a parameter, the field must
      be the id of a resource returned by M(vcenter_storage_policies). '
    type: dict
  sata:
    description:
    - Address for attaching the device to a virtual SATA adapter.
    - If unset, the server will choose an available address; if none is available,
      the request will fail.
    - 'Valide attributes are:'
    - ' - C(bus) (int): Bus number of the adapter to which the device should be attached.'
    - ' - C(unit) (int): Unit number of the device.'
    - If unset, the server will choose an available unit number on the specified adapter.
      If there are no available connections on the adapter, the request will be rejected.
    type: dict
  scsi:
    description:
    - Address for attaching the device to a virtual SCSI adapter.
    - If unset, the server will choose an available address; if none is available,
      the request will fail.
    - 'Valide attributes are:'
    - ' - C(bus) (int): Bus number of the adapter to which the device should be attached.'
    - ' - C(unit) (int): Unit number of the device.'
    - If unset, the server will choose an available unit number on the specified adapter.
      If there are no available connections on the adapter, the request will be rejected.
    type: dict
  state:
    choices:
    - absent
    - present
    default: present
    description: []
    type: str
  type:
    choices:
    - IDE
    - SATA
    - SCSI
    description:
    - The I(host_bus_adapter_type) enumerated type defines the valid types of host
      bus adapters that may be used for attaching a virtual storage device to a virtual
      machine.
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
    - The parameter must be the id of a resource returned by M(vcenter_vm_info).
    type: str
author:
- Goneri Le Bouder (@goneri) <goneri@lebouder.net>
version_added: 1.0.0
requirements:
- python >= 3.6
- aiohttp
"""

EXAMPLES = r"""
- name: Collect information about a specific VM
  vmware.vmware_rest.vcenter_vm_info:
    vm: '{{ search_result.value[0].vm }}'
  register: test_vm1_info
- name: Create a new disk
  vmware.vmware_rest.vcenter_vm_hardware_disk:
    vm: '{{ test_vm1_info.id }}'
    type: SATA
    new_vmdk:
      capacity: 320000
  register: my_new_disk
- name: Delete the disk
  vmware.vmware_rest.vcenter_vm_hardware_disk:
    vm: '{{ test_vm1_info.id }}'
    disk: '{{ my_new_disk.id }}'
    state: absent
"""

RETURN = r"""
# content generated by the update_return_section callback# task: Create a new disk
id:
  description: moid of the resource
  returned: On success
  sample: '16000'
  type: str
value:
  description: Create a new disk
  returned: On success
  sample:
    backing:
      type: VMDK_FILE
      vmdk_file: '[rw_datastore] test_vm1/test_vm1_1.vmdk'
    capacity: 320000
    label: Hard disk 2
    sata:
      bus: 0
      unit: 0
    type: SATA
  type: dict
"""

# This structure describes the format of the data expected by the end-points
PAYLOAD_FORMAT = {
    "list": {"query": {}, "body": {}, "path": {"vm": "vm"}},
    "create": {
        "query": {},
        "body": {
            "backing": "spec/backing",
            "ide": "spec/ide",
            "new_vmdk": "spec/new_vmdk",
            "sata": "spec/sata",
            "scsi": "spec/scsi",
            "type": "spec/type",
        },
        "path": {"vm": "vm"},
    },
    "delete": {"query": {}, "body": {}, "path": {"disk": "disk", "vm": "vm"}},
    "get": {"query": {}, "body": {}, "path": {"disk": "disk", "vm": "vm"}},
    "update": {
        "query": {},
        "body": {"backing": "spec/backing"},
        "path": {"disk": "disk", "vm": "vm"},
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

    argument_spec["backing"] = {"type": "dict"}
    argument_spec["disk"] = {"type": "str"}
    argument_spec["ide"] = {"type": "dict"}
    argument_spec["label"] = {"type": "str"}
    argument_spec["new_vmdk"] = {"type": "dict"}
    argument_spec["sata"] = {"type": "dict"}
    argument_spec["scsi"] = {"type": "dict"}
    argument_spec["state"] = {
        "type": "str",
        "choices": ["absent", "present"],
        "default": "present",
    }
    argument_spec["type"] = {"type": "str", "choices": ["IDE", "SATA", "SCSI"]}
    argument_spec["vm"] = {"type": "str"}

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
    return ("https://{vcenter_hostname}" "/rest/vcenter/vm/{vm}/hardware/disk").format(
        **params
    )


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
    if params["disk"]:
        _json = await get_device_info(session, build_url(params), params["disk"])
    else:
        _json = await exists(params, session, build_url(params), ["disk"])
    if _json:
        if "_update" in globals():
            params["disk"] = _json["id"]
            return await globals()["_update"](params, session)
        else:
            return await update_changed_flag(_json, 200, "get")

    payload = prepare_payload(params, PAYLOAD_FORMAT["create"])
    _url = ("https://{vcenter_hostname}" "/rest/vcenter/vm/{vm}/hardware/disk").format(
        **params
    )
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
    subdevice_type = get_subdevice_type("/rest/vcenter/vm/{vm}/hardware/disk/{disk}")
    if subdevice_type and not params[subdevice_type]:
        _json = await exists(params, session, build_url(params))
        if _json:
            params[subdevice_type] = _json["id"]
    _url = (
        "https://{vcenter_hostname}" "/rest/vcenter/vm/{vm}/hardware/disk/{disk}"
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
        "https://{vcenter_hostname}" "/rest/vcenter/vm/{vm}/hardware/disk/{disk}"
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
            _json["id"] = params.get("disk")
            return await update_changed_flag(_json, resp.status, "get")
    async with session.patch(_url, json=payload) as resp:
        try:
            if resp.headers["Content-Type"] == "application/json":
                _json = await resp.json()
        except KeyError:
            _json = {}
        _json["id"] = params.get("disk")
        return await update_changed_flag(_json, resp.status, "update")


if __name__ == "__main__":
    import asyncio

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
