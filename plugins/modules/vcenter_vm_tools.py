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
module: vcenter_vm_tools
short_description: Manage the VMware Tools configuration of a virtual machine.
description:
  - Configure the VMware Tools settings of a virtual machine, such as the automatic upgrade policy.
  - Trigger an upgrade of the VMware Tools installed in the guest operating system.
  - This module does not install VMware Tools; the guest must already have a supported Tools package
    present for an upgrade to succeed.

author:
  - Ansible Eco Content Team (@eco-ansible-content)

extends_documentation_fragment:
  - vmware.vmware_rest.connection_params

options:
  state:
    description:
      - The desired state of the resource.
      - Use C(present) to create or update the resource.
      - Use C(upgrade) to perform the upgrade action.
      - Only options C(present) support idempotence.
    type: str
    default: present
    choices:
      - present
      - upgrade
  vm:
    description:
      - Identifier of the virtual machine whose VMware Tools configuration should be managed.
      - Must be an identifier (MOID) for a C(Vm) resource.
    type: str
    required: true
  upgrade_policy:
    description:
      - Controls when VMware Tools are automatically upgraded on the virtual machine.
      - C(MANUAL) - No automatic upgrades are performed. Tools must be upgraded on demand by running this
        module with C(state=upgrade).
      - C(UPGRADE_AT_POWER_CYCLE) - When the virtual machine is power-cycled, the system checks for a newer
        version of Tools on power on. If one is available, Tools are upgraded automatically and the guest is
        rebooted if necessary.
      - Applied when I(state=present).
      - This property was added in vSphere API 7.0.0.0.
      - If not set, the upgrade policy is left unchanged.
    type: str
    required: false
  command_line_options:
    description:
      - Command line options passed to the Tools installer to customize the upgrade procedure.
      - Only used when I(state=upgrade). Leave unset to run the upgrade with default options.
    type: str
    required: false

version_added: 5.0.0

requirements: []

notes:
  - Generated from vSphere API spec 9.1.0.
  - Compatible with vSphere API 7.0.3.
  - Compatible with vSphere API 8.0.2.
"""

EXAMPLES = r"""
- name: Set the VMware Tools upgrade policy to upgrade at power cycle
  vmware.vmware_rest.vcenter_vm_tools:
    vm: vm-1013
    upgrade_policy: UPGRADE_AT_POWER_CYCLE
    state: present

- name: Revert the VMware Tools upgrade policy to manual
  vmware.vmware_rest.vcenter_vm_tools:
    vm: vm-1013
    upgrade_policy: MANUAL
    state: present

- name: Upgrade VMware Tools now
  vmware.vmware_rest.vcenter_vm_tools:
    vm: vm-1013
    state: upgrade

- name: Upgrade VMware Tools with custom installer options
  vmware.vmware_rest.vcenter_vm_tools:
    vm: vm-1013
    command_line_options: /S /v"/qn REBOOT=R"
    state: upgrade
"""

RETURN = r"""
id:
  description: MOID of the managed virtual machine.
  returned: When state is present, or when state is set to a supported action.
  sample: vm-1013
  type: str
value:
  description: The raw API response body from the vCenter operation.
  returned: On success
  type: raw
  sample:
    upgrade_policy: UPGRADE_AT_POWER_CYCLE
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
ITEM_ENDPOINT = "/vcenter/vm/{vm}/tools"


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
    },
)


ACTION_OPERATIONS = {
    "upgrade": OperationConfig(
        name="upgrade",
        uri="/vcenter/vm/{vm}/tools?action=upgrade",
        http_method="POST",
        body_spec={
            "command_line_options": {
                "required": False,
            },
        },
    ),
}


def create_module_argument_spec() -> dict:
    module_args = connection_params_argument_spec()
    module_args["command_line_options"] = {
        "type": "str",
    }
    module_args["upgrade_policy"] = {
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
