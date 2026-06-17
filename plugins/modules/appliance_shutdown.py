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
module: appliance_shutdown
short_description: Manage vCenter appliance shutdown and reboot operations.
description:
  - Schedules or cancels shutdown and reboot operations on the vCenter Server appliance.
  - Use I(state=poweroff) to schedule a power off, I(state=reboot) to schedule a reboot,
    and I(state=cancel) to cancel a pending shutdown or reboot.
author:
  - Ansible Eco Content Team (@eco-ansible-content)
extends_documentation_fragment:
  - vmware.vmware_rest.connection_params
options:
  state:
    description:
      - The shutdown operation to perform.
      - Use C(poweroff) to schedule a power off of the appliance.
      - Use C(reboot) to schedule a reboot of the appliance.
      - Use C(cancel) to cancel a pending shutdown or reboot.
    type: str
    choices:
      - cancel
      - poweroff
      - reboot
    required: true
  delay:
    description:
      - Minutes after which the shutdown or reboot should start.
      - If C(0) is specified, the operation starts immediately.
      - Required when I(state=poweroff) or I(state=reboot).
    type: int
  reason:
    description:
      - Reason for performing the shutdown or reboot.
      - Required when I(state=poweroff) or I(state=reboot).
    type: str
version_added: 4.11.0
requirements: []
notes:
  - Generated from vSphere API spec 9.1.0.
  - Has support for vSphere API 7.0.3.
  - Has support for vSphere API 8.0.2.
"""

EXAMPLES = r"""
- name: Schedule a power off of the appliance
  vmware.vmware_rest.appliance_shutdown:
    state: poweroff
    reason: this is an example
    delay: 10

- name: Cancel a pending shutdown
  vmware.vmware_rest.appliance_shutdown:
    state: cancel

- name: Schedule a reboot of the appliance
  vmware.vmware_rest.appliance_shutdown:
    state: reboot
    reason: this is an example
    delay: 10
"""

RETURN = r"""
value:
  description:
    - Pending shutdown configuration when I(state=cancel) and no shutdown was scheduled.
  returned: On success when I(state=cancel) and no change was required
  type: dict
  sample:
    action: ''
    reason: ''
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.vmware.vmware_rest.plugins.module_utils._argument_spec import (
    connection_params_argument_spec,
)
from ansible_collections.vmware.vmware_rest.plugins.module_utils._errors import (
    UnexpectedAPIResponse,
)
from ansible_collections.vmware.vmware_rest.plugins.module_utils._module_base import (
    VmwareRestModuleBase,
)

SHUTDOWN_PATH = "/appliance/shutdown"

_PAYLOAD_FORMAT = {
    "cancel": {"query": {}, "body": {}, "path": {}},
    "poweroff": {
        "query": {},
        "body": {"delay": "delay", "reason": "reason"},
        "path": {},
    },
    "reboot": {
        "query": {},
        "body": {"delay": "delay", "reason": "reason"},
        "path": {},
    },
}


class VmwareRestModule(VmwareRestModuleBase):
    PAYLOAD_FORMAT = _PAYLOAD_FORMAT

    def _get_pending_shutdown(self):
        response = self.client.get(SHUTDOWN_PATH)
        if response.status == 404:
            return {}
        return response.json

    def _post_action(self, action):
        body = self.build_payload(self.PAYLOAD_FORMAT[action])
        response = self.client.request(
            "POST",
            SHUTDOWN_PATH,
            data=body or None,
            query={"action": action},
        )
        if response.status != 204:
            self.client.error_handler.handle_request_error(
                exception=UnexpectedAPIResponse(response.status, response.data),
                method="POST",
                path=SHUTDOWN_PATH,
                request_kwargs={"data": body, "query": {"action": action}},
            )

    def run_cancel(self):
        pending = self._get_pending_shutdown()
        if not pending.get("action"):
            return {"changed": False, "value": pending}

        if not self.module.check_mode:
            self._post_action("cancel")
        return {"changed": True}

    def run_poweroff(self):
        if not self.module.check_mode:
            self._post_action("poweroff")
        return {"changed": True}

    def run_reboot(self):
        if not self.module.check_mode:
            self._post_action("reboot")
        return {"changed": True}


def main():
    module_args = connection_params_argument_spec()
    module_args["state"] = {
        "type": "str",
        "choices": ["cancel", "poweroff", "reboot"],
        "required": True,
    }
    module_args["delay"] = {"type": "int"}
    module_args["reason"] = {"type": "str"}

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
        required_if=[
            ("state", "poweroff", ["delay", "reason"]),
            ("state", "reboot", ["delay", "reason"]),
        ],
    )

    rest_module = VmwareRestModule(module)
    state = module.params["state"]

    if state == "cancel":
        result = rest_module.run_cancel()
    elif state == "poweroff":
        result = rest_module.run_poweroff()
    elif state == "reboot":
        result = rest_module.run_reboot()
    else:
        module.fail_json(msg="Unsupported state: {0}".format(state))

    module.exit_json(**result)


if __name__ == "__main__":
    main()
