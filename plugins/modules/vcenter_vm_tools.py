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
module: vcenter_vm_tools
short_description: Updates VMware Tools properties for a virtual machine.
description:
  - Updates VMware Tools properties for a virtual machine in vCenter.
  - Use I(state=present) to set the Tools upgrade policy when it differs from the
    current configuration.
author:
  - Ansible Eco Content Team (@eco-ansible-content)
extends_documentation_fragment:
  - vmware.vmware_rest.connection_params
options:
  state:
    description:
      - The desired state of VMware Tools configuration.
      - Use C(present) to update Tools properties.
    type: str
    choices:
      - present
    default: present
  vm:
    description:
      - Identifier of the virtual machine.
      - Must be an identifier (MOID) for a C(VirtualMachine) resource.
    type: str
    required: true
  upgrade_policy:
    description:
      - Tools upgrade policy setting for the virtual machine.
      - When C(MANUAL), Tools are not auto-upgraded; upgrade must be initiated manually.
      - When C(UPGRADE_AT_POWER_CYCLE), Tools are upgraded automatically when the
        virtual machine is powered on after a power cycle, if a newer version is available.
    type: str
    choices:
      - MANUAL
      - UPGRADE_AT_POWER_CYCLE
version_added: 4.11.0
requirements: []
notes:
  - Generated from vSphere API spec 9.1.0.
  - Has support for vSphere API 7.0.3.
  - Has support for vSphere API 8.0.2.
"""

EXAMPLES = r"""
- name: Query VMware Tools properties without changing configuration
  vmware.vmware_rest.vcenter_vm_tools:
    vm: vm-1001

- name: Set VMware Tools upgrade policy to manual
  vmware.vmware_rest.vcenter_vm_tools:
    vm: vm-1001
    upgrade_policy: MANUAL

- name: Set VMware Tools to upgrade at power cycle
  vmware.vmware_rest.vcenter_vm_tools:
    vm: vm-1001
    upgrade_policy: UPGRADE_AT_POWER_CYCLE
"""

RETURN = r"""
value:
  description:
    - VMware Tools properties after update, or current properties when no change was made.
  returned: On success when I(state=present)
  type: dict
  sample:
    auto_update_supported: true
    run_state: RUNNING
    upgrade_policy: MANUAL
    version_status: CURRENT
    version: 12.1.5
    install_type: OPEN_VM_TOOLS
    guest_reboot_status:
      reboot_requested: false
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.vmware.vmware_rest.plugins.module_utils._argument_spec import (
    connection_params_argument_spec,
)
from ansible_collections.vmware.vmware_rest.plugins.module_utils._module_base import (
    VmwareRestCrudModuleBase,
)

TOOLS_PATH = "/vcenter/vm/{vm}/tools"


class VmwareRestCrudModule(VmwareRestCrudModuleBase):
    PAYLOAD_FORMAT = {
        "update": {
            "query": {},
            "body": {"upgrade_policy": "upgrade_policy"},
            "path": {"vm": "vm"},
        },
    }

    UPDATABLE_PARAMS = ("upgrade_policy",)

    def ensure_present(self):
        path = self.build_path(TOOLS_PATH)
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
            msg="VMware Tools cannot be removed; absent state is not supported."
        )


def main():
    module_args = connection_params_argument_spec()
    module_args["state"] = {
        "type": "str",
        "choices": ["present"],
        "default": "present",
    }
    module_args["vm"] = {"type": "str", "required": True}
    module_args["upgrade_policy"] = {
        "type": "str",
        "choices": ["MANUAL", "UPGRADE_AT_POWER_CYCLE"],
    }

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
