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
module: vcenter_vm_hardware
short_description: Update or upgrade virtual hardware settings for a virtual machine.
description:
  - Updates virtual hardware upgrade policy and version for a virtual machine.
  - Use I(state=present) to update I(upgrade_policy) and I(upgrade_version) when they
    differ from the current configuration.
  - Use I(state=upgrade) to upgrade the virtual machine hardware version.
  - Use I(state=absent) to make no changes.
author:
  - Ansible Eco Content Team (@eco-ansible-content)
extends_documentation_fragment:
  - vmware.vmware_rest.connection_params
options:
  state:
    description:
      - The desired virtual hardware operation.
      - Use C(present) to update upgrade policy or target version.
      - Use C(upgrade) to upgrade the virtual machine hardware version.
      - Use C(absent) to make no changes.
    type: str
    choices:
      - present
      - upgrade
      - absent
    default: present
  vm:
    description:
      - Identifier of the virtual machine.
      - Must be an identifier (MOID) for a C(VirtualMachine) resource.
    type: str
    required: true
  upgrade_policy:
    description:
      - Policy for upgrading virtual hardware when a newer version is available.
    type: str
    choices:
      - NEVER
      - AFTER_CLEAN_SHUTDOWN
      - ALWAYS
  upgrade_version:
    description:
      - Target virtual hardware version.
    type: str
    choices:
      - VMX_03
      - VMX_04
      - VMX_06
      - VMX_07
      - VMX_08
      - VMX_09
      - VMX_10
      - VMX_11
      - VMX_12
      - VMX_13
      - VMX_14
      - VMX_15
      - VMX_16
      - VMX_17
      - VMX_18
      - VMX_19
      - VMX_20
      - VMX_21
      - VMX_22
version_added: 4.11.0
requirements: []
notes:
  - Generated from vSphere API spec 9.1.0.
  - Has support for vSphere API 7.0.3.
  - Has support for vSphere API 8.0.2.
"""

EXAMPLES = r"""
- name: Set virtual hardware upgrade policy
  vmware.vmware_rest.vcenter_vm_hardware:
    vm: vm-1001
    upgrade_policy: AFTER_CLEAN_SHUTDOWN

- name: Upgrade virtual machine hardware
  vmware.vmware_rest.vcenter_vm_hardware:
    vm: vm-1001
    state: upgrade
"""

RETURN = r"""
value:
  description:
    - Virtual hardware settings after update, or current settings when no change was made.
  returned: On success when I(state=present)
  type: dict
  sample:
    version: VMX_19
    upgrade_policy: AFTER_CLEAN_SHUTDOWN
    upgrade_status: NONE
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.vmware.vmware_rest.plugins.module_utils._argument_spec import (
    connection_params_argument_spec,
)
from ansible_collections.vmware.vmware_rest.plugins.module_utils._module_base import (
    VmwareRestCrudModuleBase,
)

HARDWARE_PATH = "/vcenter/vm/{vm}/hardware"
UPGRADE_PATH = "/vcenter/vm/{vm}/hardware"


class VmwareRestCrudModule(VmwareRestCrudModuleBase):
    PAYLOAD_FORMAT = {
        "update": {
            "query": {},
            "body": {
                "upgrade_policy": "upgrade_policy",
                "upgrade_version": "upgrade_version",
            },
            "path": {},
        },
        "upgrade": {
            "query": {"action": "upgrade"},
            "body": {},
            "path": {},
        },
    }

    UPDATABLE_PARAMS = ("upgrade_policy", "upgrade_version")

    def ensure_present(self):
        update_body = self.build_updatable_payload()
        path = self.build_path(HARDWARE_PATH)
        response = self.client.get(path)
        if response.status == 404:
            self.module.fail_json(
                msg="Virtual machine not found: {0}".format(self.params["vm"])
            )
        if not update_body:
            return {"changed": False, "value": response.json}
        return self.update_if_changed(path, response.json, update_body)

    def ensure_upgrade(self):
        path = self.build_path(UPGRADE_PATH)
        query = self.build_query(self.PAYLOAD_FORMAT["upgrade"])
        if not self.module.check_mode:
            response = self.client.post(path, data={}, query=query)
            vm_id = response.json
            if isinstance(vm_id, dict):
                vm_id = vm_id.get("value", vm_id)
        else:
            vm_id = self.params["vm"]
        return {"changed": True, "id": vm_id, "value": vm_id}

    def ensure_absent(self):
        return {"changed": False}


def main():
    module_args = connection_params_argument_spec()
    module_args["state"] = {
        "type": "str",
        "choices": ["present", "upgrade", "absent"],
        "default": "present",
    }
    module_args["vm"] = {"type": "str", "required": True}
    module_args["upgrade_policy"] = {
        "type": "str",
        "choices": ["NEVER", "AFTER_CLEAN_SHUTDOWN", "ALWAYS"],
    }
    module_args["upgrade_version"] = {
        "type": "str",
        "choices": [
            "VMX_03",
            "VMX_04",
            "VMX_06",
            "VMX_07",
            "VMX_08",
            "VMX_09",
            "VMX_10",
            "VMX_11",
            "VMX_12",
            "VMX_13",
            "VMX_14",
            "VMX_15",
            "VMX_16",
            "VMX_17",
            "VMX_18",
            "VMX_19",
            "VMX_20",
            "VMX_21",
            "VMX_22",
        ],
    }

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
    )

    crud_module = VmwareRestCrudModule(module)
    state = module.params["state"]
    if state == "present":
        result = crud_module.ensure_present()
    elif state == "upgrade":
        result = crud_module.ensure_upgrade()
    elif state == "absent":
        result = crud_module.ensure_absent()
    else:
        module.fail_json(msg="Unsupported state: {0}".format(state))

    module.exit_json(**result)


if __name__ == "__main__":
    main()
