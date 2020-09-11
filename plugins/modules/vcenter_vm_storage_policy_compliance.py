#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = """
module: vcenter_vm_storage_policy_compliance
short_description: Handle resource of type vcenter_vm_storage_policy_compliance
description: Handle resource of type vcenter_vm_storage_policy_compliance
options:
  action:
    choices:
    - check
    description:
    - action=check
    type: str
  check_spec:
    description:
    - Parameter specifies the entities on which storage policy compliance check is
      to be invoked. The storage compliance Info Compliance.Info is returned.
    - If unset, the behavior is equivalent to a Compliance.CheckSpec with CheckSpec#vmHome
      set to true and CheckSpec#disks populated with all disks attached to the virtual
      machine.
    - 'Valide attributes are:'
    - ' - C(disks) (list): Identifiers of the virtual machine''s virtual disks for
      which compliance should be checked.'
    - If unset or empty, compliance check is invoked on all the associated disks.
    - 'When clients pass a value of this structure as a parameter, the field must
      contain identifiers for the resource type: vcenter.vm.hardware.Disk. When operations
      return a value of this structure as a result, the field will contain identifiers
      for the resource type: vcenter.vm.hardware.Disk.'
    - ' - C(vm_home) (bool): Invoke compliance check on the virtual machine home directory
      if set to true.'
    type: dict
  state:
    choices:
    - check
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
    "get": {"query": {}, "body": {}, "path": {"vm": "vm"}},
    "check": {
        "query": {"action": "action"},
        "body": {
            "check_spec": {"disks": "check_spec/disks", "vm_home": "check_spec/vm_home"}
        },
        "path": {"vm": "vm"},
    },
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

    argument_spec["action"] = {"type": "str", "choices": ["check"]}
    argument_spec["check_spec"] = {"type": "dict"}
    argument_spec["state"] = {"type": "str", "choices": ["check"]}
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

    return (
        "https://{vcenter_hostname}" "/rest/vcenter/vm/{vm}/storage/policy/compliance"
    ).format(**params)


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


async def _check(params, session):
    _in_query_parameters = PAYLOAD_FORMAT["check"]["query"].keys()
    payload = payload = prepare_payload(params, PAYLOAD_FORMAT["check"])
    subdevice_type = get_subdevice_type(
        "/rest/vcenter/vm/{vm}/storage/policy/compliance"
    )
    if subdevice_type and (not params[subdevice_type]):
        _json = await exists(params, session, build_url(params))
        if _json:
            params[subdevice_type] = _json["id"]
    _url = "https://{vcenter_hostname}/rest/vcenter/vm/{vm}/storage/policy/compliance".format(
        **params
    ) + gen_args(
        params, _in_query_parameters
    )
    async with session.post(_url, json=payload) as resp:
        try:
            if resp.headers["Content-Type"] == "application/json":
                _json = await resp.json()
        except KeyError:
            _json = {}
        return await update_changed_flag(_json, resp.status, "check")


if __name__ == "__main__":
    import asyncio

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
