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
module: appliance_shutdown
short_description: Power off or reboot the vCenter Server Appliance.
description:
  - Schedule or cancel a power off or reboot of the vCenter Server Appliance.
  - Use O(state=poweroff) to shut the appliance down, or O(state=reboot) to restart it.
  - A shutdown or reboot can be scheduled to start after a delay, and a previously
    scheduled shutdown can be cancelled with O(state=cancel).
  - Use M(vmware.vmware_rest.appliance_shutdown_info) to view details of a pending
    shutdown or reboot.

author:
  - Ansible Eco Content Team (@eco-ansible-content)

extends_documentation_fragment:
  - vmware.vmware_rest.connection_params

options:
  state:
    description:
      - The shutdown action to perform on the appliance.
      - Use C(poweroff) to power off the appliance.
      - Use C(reboot) to reboot the appliance.
      - Use C(cancel) to cancel a pending shutdown or reboot.
      - None of these actions are idempotent.
    type: str
    required: true
    choices:
      - cancel
      - poweroff
      - reboot
  delay:
    description:
      - The number of minutes to wait before the poweroff or reboot begins.
      - When set to 0, the action starts immediately.
      - Required when O(state=poweroff) or O(state=reboot). Ignored when O(state=cancel).
    type: int
    required: false
  reason:
    description:
      - A message describing why the appliance is being powered off or rebooted.
      - Required when O(state=poweroff) or O(state=reboot). Ignored when O(state=cancel).
    type: str
    required: false

version_added: 5.0.0

requirements: []

notes:
  - Generated from vSphere API spec 9.1.0.
"""

EXAMPLES = r"""
- name: Reboot the appliance immediately
  vmware.vmware_rest.appliance_shutdown:
    state: reboot
    delay: 0
    reason: Applying configuration changes

- name: Schedule a poweroff in 10 minutes
  vmware.vmware_rest.appliance_shutdown:
    state: poweroff
    delay: 10
    reason: Planned maintenance window

- name: Cancel a pending shutdown or reboot
  vmware.vmware_rest.appliance_shutdown:
    state: cancel
"""

RETURN = r"""
value:
  description: The raw API response body from the vCenter operation. Empty when the operation returns no content.
  returned: On success
  type: raw
  sample: {}
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

MOID_PARAMETER_HINTS = []

LIST_ENDPOINT = ""
ITEM_ENDPOINT = "/appliance/shutdown"


GET_OPERATION = OperationConfig(
    name="get",
    uri=ITEM_ENDPOINT,
    http_method="GET",
)


ACTION_OPERATIONS = {
    "cancel": OperationConfig(
        name="cancel",
        uri="/appliance/shutdown?action=cancel",
        http_method="POST",
    ),
    "poweroff": OperationConfig(
        name="poweroff",
        uri="/appliance/shutdown?action=poweroff",
        http_method="POST",
        body_spec={
            "delay": {
                "required": True,
            },
            "reason": {
                "required": True,
            },
        },
    ),
    "reboot": OperationConfig(
        name="reboot",
        uri="/appliance/shutdown?action=reboot",
        http_method="POST",
        body_spec={
            "delay": {
                "required": True,
            },
            "reason": {
                "required": True,
            },
        },
    ),
}


def create_module_argument_spec() -> dict:
    module_args = connection_params_argument_spec()
    module_args["delay"] = {
        "type": "int",
    }
    module_args["reason"] = {
        "type": "str",
    }
    module_args["state"] = {
        "type": "str",
        "choices": ["cancel", "poweroff", "reboot"],
        "required": True,
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
        action_operations=ACTION_OPERATIONS,
    )

    try:
        if module.params["state"] in ACTION_OPERATIONS:
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
