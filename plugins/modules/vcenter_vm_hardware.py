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
module: vcenter_vm_hardware
short_description: Manage the virtual hardware settings of a virtual machine.
description:
  - Update the virtual hardware configuration of a virtual machine, such as its virtual
    hardware (compatibility) version and the scheduled hardware upgrade policy.
  - Trigger an on-demand upgrade of the virtual hardware to a newer compatibility version.
  - The virtual machine is identified by its managed object identifier (MOID).
  - This module maps to the vCenter C(/vcenter/vm/{vm}/hardware) REST API.

author:
  - Ansible Eco Content Team (@eco-ansible-content)

extends_documentation_fragment:
  - vmware.vmware_rest.connection_params

options:
  state:
    description:
      - The desired state of the resource.
      - Use C(present) to update the virtual hardware settings.
      - Use C(upgrade) to perform the virtual hardware upgrade action.
      - Only option C(present) supports idempotence.
    type: str
    default: present
    choices:
      - present
      - upgrade
  vm:
    description:
      - Identifier of the virtual machine whose hardware is being managed.
      - Must be the managed object identifier (MOID) of an existing C(Vm) resource.
    type: str
    required: true
  upgrade_policy:
    description:
      - Scheduled upgrade policy that controls when the virtual hardware is automatically upgraded.
      - If set to C(NEVER), the scheduled upgrade version is reset and left unset.
      - C(NEVER) - Do not upgrade the virtual machine when it is powered on.
      - C(AFTER_CLEAN_SHUTDOWN) - Run the scheduled upgrade when the virtual machine is powered on after a clean shutdown of the guest operating system.
      - C(ALWAYS) - Run the scheduled upgrade when the virtual machine is powered on.
      - If not set, the value is left unchanged.
    type: str
    required: false
  upgrade_version:
    description:
      - Target hardware version to be used on the next scheduled virtual hardware upgrade.
      - If specified, this must be a newer virtual hardware version than the virtual machine's current hardware version.
      - C(VMX_03) - Hardware version 3, first supported in ESXi 2.5.
      - C(VMX_04) - Hardware version 4, first supported in ESXi 3.0.
      - C(VMX_06) - Hardware version 6, first supported in WS 6.0.
      - C(VMX_07) - Hardware version 7, first supported in ESXi 4.0.
      - C(VMX_08) - Hardware version 8, first supported in ESXi 5.0.
      - C(VMX_09) - Hardware version 9, first supported in ESXi 5.1.
      - C(VMX_10) - Hardware version 10, first supported in ESXi 5.5.
      - C(VMX_11) - Hardware version 11, first supported in ESXi 6.0.
      - C(VMX_12) - Hardware version 12, first supported in Workstation 12.0.
      - C(VMX_13) - Hardware version 13, first supported in ESXi 6.5.
      - C(VMX_14) - Hardware version 14, first supported in ESXi 6.7. This value was added in vSphere API 6.7.
      - C(VMX_15) - Hardware version 15, first supported in ESXi 6.7 Update 2. This value was added in vSphere API 6.7.2.
      - C(VMX_16) - Hardware version 16, first supported in Workstation 15.0. This value was added in vSphere API 7.0.0.0.
      - C(VMX_17) - Hardware version 17, first supported in ESXi 7.0.0-0. This value was added in vSphere API 7.0.0.0.
      - C(VMX_18) - Hardware version 18, first supported in ESXi 7.0 U1. This value was added in vSphere API 7.0.1.0.
      - C(VMX_19) - Hardware version 19, first supported in ESXi 7.0 U2. This value was added in vSphere API 7.0.2.0.
      - C(VMX_20) - Hardware version 20, first supported in ESXi 8.0.0.1. This value was added in vSphere API 8.0.0.1.
      - C(VMX_21) - Hardware version 21, first supported in ESXi 8.0 U2. This value was added in vSphere API 8.0.2.0.
      - C(VMX_22) - Hardware version 22, first supported in ESXi 9.0. This value was added in vSphere API 9.0.0.0.
      - If O(upgrade_policy=NEVER), this property must not be set. Otherwise, if not set, it defaults to the most
        recent virtual hardware version supported by the server.
    type: str
    required: false
  version:
    description:
      - Target virtual hardware (compatibility) version to upgrade the virtual machine to.
      - Only used when O(state=upgrade).
      - C(VMX_03) - Hardware version 3, first supported in ESXi 2.5.
      - C(VMX_04) - Hardware version 4, first supported in ESXi 3.0.
      - C(VMX_06) - Hardware version 6, first supported in WS 6.0.
      - C(VMX_07) - Hardware version 7, first supported in ESXi 4.0.
      - C(VMX_08) - Hardware version 8, first supported in ESXi 5.0.
      - C(VMX_09) - Hardware version 9, first supported in ESXi 5.1.
      - C(VMX_10) - Hardware version 10, first supported in ESXi 5.5.
      - C(VMX_11) - Hardware version 11, first supported in ESXi 6.0.
      - C(VMX_12) - Hardware version 12, first supported in Workstation 12.0.
      - C(VMX_13) - Hardware version 13, first supported in ESXi 6.5.
      - C(VMX_14) - Hardware version 14, first supported in ESXi 6.7. This value was added in vSphere API 6.7.
      - C(VMX_15) - Hardware version 15, first supported in ESXi 6.7 Update 2. This value was added in vSphere API 6.7.2.
      - C(VMX_16) - Hardware version 16, first supported in Workstation 15.0. This value was added in vSphere API 7.0.0.0.
      - C(VMX_17) - Hardware version 17, first supported in ESXi 7.0.0-0. This value was added in vSphere API 7.0.0.0.
      - C(VMX_18) - Hardware version 18, first supported in ESXi 7.0 U1. This value was added in vSphere API 7.0.1.0.
      - C(VMX_19) - Hardware version 19, first supported in ESXi 7.0 U2. This value was added in vSphere API 7.0.2.0.
      - C(VMX_20) - Hardware version 20, first supported in ESXi 8.0.0.1. This value was added in vSphere API 8.0.0.1.
      - C(VMX_21) - Hardware version 21, first supported in ESXi 8.0 U2. This value was added in vSphere API 8.0.2.0.
      - C(VMX_22) - Hardware version 22, first supported in ESXi 9.0. This value was added in vSphere API 9.0.0.0.
      - If not set, defaults to the most recent virtual hardware version supported by the server.
    type: str
    required: false

version_added: 5.0.0

requirements: []

notes:
  - Generated from vSphere API spec 9.1.0.
"""

EXAMPLES = r"""
- name: Schedule a hardware upgrade after a clean guest shutdown
  vmware.vmware_rest.vcenter_vm_hardware:
    vm: vm-1001
    upgrade_policy: AFTER_CLEAN_SHUTDOWN
    upgrade_version: VMX_21
    state: present

- name: Disable scheduled hardware upgrades
  vmware.vmware_rest.vcenter_vm_hardware:
    vm: vm-1001
    upgrade_policy: NEVER
    state: present

- name: Upgrade the virtual hardware to the latest version supported by the host
  vmware.vmware_rest.vcenter_vm_hardware:
    vm: vm-1001
    state: upgrade

- name: Upgrade the virtual hardware to a specific version
  vmware.vmware_rest.vcenter_vm_hardware:
    vm: vm-1001
    version: VMX_22
    state: upgrade
"""

RETURN = r"""
id:
  description: MOID of the managed virtual machine.
  returned: When state is present, or when a resource is deleted, or when state is set to a supported action.
  sample: vm-1001
  type: str
value:
  description: The raw API response body from the vCenter operation.
  returned: On success
  type: raw
  sample:
    version: VMX_19
    upgrade_policy: NEVER
    upgrade_status: READY
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
ITEM_ENDPOINT = "/vcenter/vm/{vm}/hardware"


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
        "upgrade_policy": {
            "required": False,
        },
        "upgrade_version": {
            "required": False,
        },
    },
)


ACTION_OPERATIONS = {
    "upgrade": OperationConfig(
        name="upgrade",
        uri="/vcenter/vm/{vm}/hardware?action=upgrade",
        http_method="POST",
        body_spec={
            "version": {
                "required": False,
            },
        },
    ),
}


def create_module_argument_spec() -> dict:
    module_args = connection_params_argument_spec()
    module_args["upgrade_policy"] = {
        "type": "str",
    }
    module_args["upgrade_version"] = {
        "type": "str",
    }
    module_args["version"] = {
        "type": "str",
    }
    module_args["vm"] = {
        "type": "str",
        "required": True,
    }
    module_args["state"] = {
        "type": "str",
        "choices": ["present", "upgrade"],
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
        action_operations=ACTION_OPERATIONS,
    )

    try:
        if module.params["state"] == "present":
            result = crud_module.ensure_present()
        elif module.params["state"] in ACTION_OPERATIONS:
            result = crud_module.perform_action()
        else:
            module.fail_json(
                msg="Unsupported state: {0}".format(module.params["state"])
            )
    except VmwareModuleError as e:
        module.fail_json(**e.to_module_fail_json_output())

    module.exit_json(**result)


if __name__ == "__main__":
    main()
