#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright: (c) 2026, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#
# This module is generated using LLM agents and skills defined in the vmware.vmware_rest repository.
# See: https://github.com/ansible-collections/vmware.vmware_rest
#

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = r"""
module: vcenter_vm_hardware_boot
short_description: Manage the boot configuration of a virtual machine.
description:
  - Update the boot-related settings of a virtual machine.
  - Controls the firmware type (BIOS or EFI), the boot delay, the network boot protocol, and how the
    virtual machine behaves when a boot attempt fails.
  - Only the settings you provide are changed; any option left unset keeps its current value.

author:
  - Ansible Eco Content Team (@eco-ansible-content)

extends_documentation_fragment:
  - vmware.vmware_rest.connection_params

options:
  state:
    description:
      - The desired state of the resource.
      - Use C(present) to create or update the resource.
    type: str
    default: present
    choices:
      - present
  vm:
    description:
      - Identifier of the virtual machine whose boot configuration should be managed.
      - Must be an identifier (MOID) for a C(Vm) resource.
    type: str
    required: true
  type:
    description:
      - The firmware type used by the virtual machine when it boots.
      - C(BIOS) uses Basic Input/Output System (BIOS) firmware.
      - C(EFI) uses Extensible Firmware Interface (EFI) firmware.
      - If not set, the current value is left unchanged.
    type: str
    required: false
  efi_legacy_boot:
    description:
      - Whether to use EFI legacy boot mode.
      - Only relevant when O(type=EFI).
      - If not set, the current value is left unchanged.
    type: bool
    required: false
  network_protocol:
    description:
      - Protocol to use when the virtual machine attempts to boot over the network.
      - C(IPV4) uses PXE or Apple NetBoot over IPv4.
      - C(IPV6) uses PXE over IPv6.
      - Only relevant when O(type=EFI).
      - If not set, the current value is left unchanged.
    type: str
    required: false
  delay:
    description:
      - Delay in milliseconds before the firmware boot process begins when the virtual machine is powered on.
      - This delay gives users a time window to connect to the virtual machine console and enter BIOS setup mode.
      - If not set, the current value is left unchanged.
    type: int
    required: false
  retry:
    description:
      - Whether the virtual machine should automatically retry the boot process after a failure.
      - If not set, the current value is left unchanged.
    type: bool
    required: false
  retry_delay:
    description:
      - Delay in milliseconds before retrying the boot process after a failure.
      - Only applied when O(retry=true).
      - If not set, the current value is left unchanged.
    type: int
    required: false
  enter_setup_mode:
    description:
      - Whether the firmware boot process should automatically enter setup mode the next time the virtual machine boots.
      - This flag is automatically reset to C(false) once the virtual machine enters setup mode.
      - If not set, the current value is left unchanged.
    type: bool
    required: false

version_added: 5.0.0

requirements: []

notes:
  - Generated from vSphere API spec 9.1.0.
"""

EXAMPLES = r"""
- name: Look up the virtual machine by name
  register: search_result
  vmware.vmware_rest.vcenter_vm_info:
    filter_names:
      - test_vm1

- name: Set a boot delay so the console can be opened before boot
  vmware.vmware_rest.vcenter_vm_hardware_boot:
    vm: '{{ search_result.value[0].vm }}'
    delay: 10000
    state: present

- name: Configure EFI firmware with network boot and automatic retry
  vmware.vmware_rest.vcenter_vm_hardware_boot:
    vm: '{{ search_result.value[0].vm }}'
    type: EFI
    network_protocol: IPV4
    retry: true
    retry_delay: 15000
    state: present
"""

RETURN = r"""
id:
  description: MOID of the virtual machine whose boot configuration was managed.
  returned: When state is present, or when a resource is deleted, or when state is set to a supported action.
  sample: vm-1001
  type: str
value:
  description:
    - The raw API response body from the vCenter operation.
    - The boot update endpoint returns no content on success, so this value is typically empty.
  returned: On success.
  sample: {}
  type: raw
"""


from ansible.module_utils.basic import AnsibleModule
from ansible_collections.vmware.vmware_rest.plugins.module_utils._argument_spec import (
    connection_params_argument_spec,
)
from ansible_collections.vmware.vmware_rest.plugins.module_utils._errors import (
    VmwareModuleError,
)
from ansible_collections.vmware.vmware_rest.plugins.module_utils._crud_module import (
    VmwareRestCrudModuleBase,
)
from ansible_collections.vmware.vmware_rest.plugins.module_utils._operation_configs import (
    OperationConfig,
)

MOID_PARAMETER_HINTS = ["vm"]

LIST_ENDPOINT = ""
ITEM_ENDPOINT = "/vcenter/vm/{vm}/hardware/boot"


GET_OPERATION = OperationConfig(
    name="get",
    uri=ITEM_ENDPOINT,
    http_method="GET",
)

UPDATE_OPERATION = OperationConfig(
    name="update",
    uri=ITEM_ENDPOINT,
    http_method="PATCH",
    body_spec={
        "type": {
            "required": False,
        },
        "efi_legacy_boot": {
            "required": False,
        },
        "network_protocol": {
            "required": False,
        },
        "delay": {
            "required": False,
        },
        "retry": {
            "required": False,
        },
        "retry_delay": {
            "required": False,
        },
        "enter_setup_mode": {
            "required": False,
        },
    },
)


def create_module_argument_spec() -> dict:
    module_args = connection_params_argument_spec()
    module_args["delay"] = {
        "type": "int",
    }
    module_args["efi_legacy_boot"] = {
        "type": "bool",
    }
    module_args["enter_setup_mode"] = {
        "type": "bool",
    }
    module_args["network_protocol"] = {
        "type": "str",
    }
    module_args["retry"] = {
        "type": "bool",
    }
    module_args["retry_delay"] = {
        "type": "int",
    }
    module_args["type"] = {
        "type": "str",
    }
    module_args["vm"] = {
        "type": "str",
        "required": True,
    }
    module_args["state"] = {
        "type": "str",
        "choices": ["present"],
        "default": "present",
    }
    return module_args


def main():
    module = AnsibleModule(
        argument_spec=create_module_argument_spec(),
        supports_check_mode=True,
    )

    crud_module = VmwareRestCrudModuleBase(
        module=module,
        moid_parameter_hints=MOID_PARAMETER_HINTS,
        get_operation_config=GET_OPERATION,
        update_operation_config=UPDATE_OPERATION,
    )

    try:
        if module.params["state"] == "present":
            result = crud_module.ensure_present()
        else:
            module.fail_json(
                msg="Unsupported state: {0}".format(module.params["state"])
            )
    except VmwareModuleError as e:
        module.fail_json(**e.to_module_fail_json_output())

    module.exit_json(**result)


if __name__ == "__main__":
    main()
