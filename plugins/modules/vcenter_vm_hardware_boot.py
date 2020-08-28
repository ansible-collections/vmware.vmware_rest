#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = """
module: vcenter_vm_hardware_boot
short_description: Handle resource of type vcenter_vm_hardware_boot
description: Handle resource of type vcenter_vm_hardware_boot
options:
  delay:
    description:
    - Delay in milliseconds before beginning the firmware boot process when the virtual
      machine is powered on. This delay may be used to provide a time window for users
      to connect to the virtual machine console and enter BIOS setup mode.
    - If unset, the value is unchanged.
    type: int
  efi_legacy_boot:
    description:
    - Flag indicating whether to use EFI legacy boot mode.
    - If unset, the value is unchanged.
    type: bool
  enter_setup_mode:
    description:
    - Flag indicating whether the firmware boot process should automatically enter
      setup mode the next time the virtual machine boots. Note that this flag will
      automatically be reset to false once the virtual machine enters setup mode.
    - If unset, the value is unchanged.
    type: bool
  network_protocol:
    choices:
    - IPV4
    - IPV6
    description:
    - The Boot.NetworkProtocol enumerated type defines the valid network boot protocols
      supported when booting a virtual machine with EFI firmware over the network.
    type: str
  retry:
    description:
    - Flag indicating whether the virtual machine should automatically retry the boot
      process after a failure.
    - If unset, the value is unchanged.
    type: bool
  retry_delay:
    description:
    - Delay in milliseconds before retrying the boot process after a failure; applicable
      only when Boot.Info.retry is true.
    - If unset, the value is unchanged.
    type: int
  state:
    choices:
    - present
    default: present
    description: []
    type: str
  type:
    choices:
    - BIOS
    - EFI
    description:
    - The Boot.Type enumerated type defines the valid firmware types for a virtual
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
- name: Collect information about a specific VM
  vcenter_vm_info:
    vm: '{{ search_result.value[0].vm }}'
  register: test_vm1_info
- name: Change a VM boot parameters
  vcenter_vm_hardware_boot:
    vm: '{{ test_vm1_info.id }}'
    efi_legacy_boot: true
    type: EFI
- name: Change a VM boot parameters (again)
  vcenter_vm_hardware_boot:
    vm: '{{ test_vm1_info.id }}'
    efi_legacy_boot: true
    type: EFI
"""

IN_QUERY_PARAMETER = []

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

    argument_spec["delay"] = {"type": "int"}
    argument_spec["efi_legacy_boot"] = {"type": "bool"}
    argument_spec["enter_setup_mode"] = {"type": "bool"}
    argument_spec["network_protocol"] = {"type": "str", "choices": ["IPV4", "IPV6"]}
    argument_spec["retry"] = {"type": "bool"}
    argument_spec["retry_delay"] = {"type": "int"}
    argument_spec["state"] = {
        "type": "str",
        "choices": ["present"],
        "default": "present",
    }
    argument_spec["type"] = {"type": "str", "choices": ["BIOS", "EFI"]}
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

    return ("https://{vcenter_hostname}" "/rest/vcenter/vm/{vm}/hardware/boot").format(
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
    func = globals()[("_" + operation)]
    return await func(module.params, session)


async def _update(params, session):
    accepted_fields = [
        "delay",
        "efi_legacy_boot",
        "enter_setup_mode",
        "network_protocol",
        "retry",
        "retry_delay",
        "type",
    ]
    spec = {}
    for i in accepted_fields:
        if params[i]:
            spec[i] = params[i]
    _url = "https://{vcenter_hostname}/rest/vcenter/vm/{vm}/hardware/boot".format(
        **params
    )
    async with session.get(_url) as resp:
        _json = await resp.json()
        for (k, v) in _json["value"].items():
            if (k in spec) and (spec[k] == v):
                del spec[k]
        if not spec:
            _json["id"] = params.get("None")
            return await update_changed_flag(_json, resp.status, "get")
    async with session.patch(_url, json={"spec": spec}) as resp:
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
