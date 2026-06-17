#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright: (c) 2026, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#
# This module is generated using LLM agents and skills defined in the vmware.vmware_rest repository.
# See: https://github.com/ansible-collections/vmware.vmware_rest
#

DOCUMENTATION = r"""
module: vcenter_vm_hardware_boot
short_description: Updates boot-related settings for a virtual machine.
description:
  - Updates boot-related settings for a virtual machine in vCenter.
  - Use I(state=present) to set firmware type, boot delay, retry behavior, and
    related options when they differ from the current configuration.
author:
  - Ansible Eco Content Team (@eco-ansible-content)
extends_documentation_fragment:
  - vmware.vmware_rest.connection_params
options:
  state:
    description:
      - The desired state of the virtual machine boot configuration.
      - Use C(present) to update boot-related settings.
    type: str
    choices:
      - present
    default: present
  vm:
    description:
      - Virtual machine identifier.
      - Must be an identifier (MOID) for a C(VirtualMachine) resource.
    type: str
    required: true
  type:
    description:
      - Firmware type used by the virtual machine.
      - When C(BIOS), Basic Input/Output System firmware is used.
      - When C(EFI), Extensible Firmware Interface firmware is used.
    type: str
    choices:
      - BIOS
      - EFI
  efi_legacy_boot:
    description:
      - Whether to use EFI legacy boot mode.
      - Relevant only when I(type) is C(EFI).
    type: bool
  network_protocol:
    description:
      - Protocol used when booting the virtual machine over the network.
      - Relevant only when I(type) is C(EFI).
    type: str
    choices:
      - IPV4
      - IPV6
  delay:
    description:
      - Delay in milliseconds before beginning the firmware boot process when the
        virtual machine is powered on.
    type: int
  retry:
    description:
      - Whether the virtual machine should automatically retry the boot process
        after a failure.
    type: bool
  retry_delay:
    description:
      - Delay in milliseconds before retrying the boot process after a failure.
      - Applicable only when I(retry) is C(true).
    type: int
  enter_setup_mode:
    description:
      - Whether the firmware boot process should automatically enter setup mode
        the next time the virtual machine boots.
      - This flag is reset to C(false) once the virtual machine enters setup mode.
    type: bool
version_added: 4.11.0
requirements: []
notes:
  - Generated from vSphere API spec 9.1.0.
  - Has support for vSphere API 7.0.3.
  - Has support for vSphere API 8.0.2.
"""

EXAMPLES = r"""
- name: Query boot settings without changing configuration
  vmware.vmware_rest.vcenter_vm_hardware_boot:
    vm: vm-1001

- name: Set firmware type to EFI
  vmware.vmware_rest.vcenter_vm_hardware_boot:
    vm: vm-1001
    type: EFI

- name: Configure boot delay and retry behavior
  vmware.vmware_rest.vcenter_vm_hardware_boot:
    vm: vm-1001
    delay: 5000
    retry: true
    retry_delay: 10000
"""

RETURN = r"""
value:
  description:
    - Boot-related settings after update, or current settings when no change was made.
  returned: On success when I(state=present)
  type: dict
  sample:
    type: EFI
    efi_legacy_boot: false
    network_protocol: IPV4
    delay: 0
    retry: false
    retry_delay: 10000
    enter_setup_mode: false
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.vmware.vmware_rest.plugins.module_utils._argument_spec import (
    connection_params_argument_spec,
)
from ansible_collections.vmware.vmware_rest.plugins.module_utils._module_base import (
    VmwareRestCrudModuleBase,
)

BOOT_PATH = "/vcenter/vm/{vm}/hardware/boot"


class VmwareRestCrudModule(VmwareRestCrudModuleBase):
    PAYLOAD_FORMAT = {
        "update": {
            "query": {},
            "body": {
                "type": "type",
                "efi_legacy_boot": "efi_legacy_boot",
                "network_protocol": "network_protocol",
                "delay": "delay",
                "retry": "retry",
                "retry_delay": "retry_delay",
                "enter_setup_mode": "enter_setup_mode",
            },
            "path": {"vm": "vm"},
        },
    }

    UPDATABLE_PARAMS = (
        "type",
        "efi_legacy_boot",
        "network_protocol",
        "delay",
        "retry",
        "retry_delay",
        "enter_setup_mode",
    )

    def ensure_present(self):
        path = self.build_path(BOOT_PATH)
        response = self.client.get(path)
        if response.status == 404:
            self.module.fail_json(
                msg="Virtual machine not found: {0}".format(self.params["vm"])
            )
        return self.update_if_changed(
            path,
            response.json,
            self.build_updatable_payload(),
        )

    def ensure_absent(self):
        self.module.fail_json(
            msg="Boot settings cannot be removed; absent state is not supported."
        )


def main():
    module_args = connection_params_argument_spec()
    module_args["state"] = {
        "type": "str",
        "choices": ["present"],
        "default": "present",
    }
    module_args["vm"] = {"type": "str", "required": True}
    module_args["type"] = {
        "type": "str",
        "choices": ["BIOS", "EFI"],
    }
    module_args["efi_legacy_boot"] = {"type": "bool"}
    module_args["network_protocol"] = {
        "type": "str",
        "choices": ["IPV4", "IPV6"],
    }
    module_args["delay"] = {"type": "int"}
    module_args["retry"] = {"type": "bool"}
    module_args["retry_delay"] = {"type": "int"}
    module_args["enter_setup_mode"] = {"type": "bool"}

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
    )

    crud_module = VmwareRestCrudModule(module)

    if module.params["state"] == "present":
        result = crud_module.ensure_present()
    else:
        module.fail_json(msg="Unsupported state: {0}".format(module.params["state"]))

    module.exit_json(**result)


if __name__ == "__main__":
    main()
