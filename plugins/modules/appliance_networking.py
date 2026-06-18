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
module: appliance_networking
short_description: Manage vCenter appliance networking settings.
description:
  - Enables or disables IPv6 on all vCenter Server appliance interfaces.
  - Use I(state=reset) to reset and restart network configuration on all interfaces
    and renew DHCP leases.
author:
  - Ansible Eco Content Team (@eco-ansible-content)
extends_documentation_fragment:
  - vmware.vmware_rest.connection_params
options:
  state:
    description:
      - The desired networking operation.
      - Use C(present) to enable or disable IPv6 on all interfaces.
      - Use C(reset) to reset and restart network configuration on all interfaces.
    type: str
    choices:
      - present
      - reset
    default: present
  ipv6_enabled:
    description:
      - Whether IPv6 is enabled on all interfaces.
      - Required when I(state=present).
    type: bool
version_added: 4.11.0
requirements: []
notes:
  - Generated from vSphere API spec 9.1.0.
  - Has support for vSphere API 7.0.3.
  - Has support for vSphere API 8.0.2.
"""

EXAMPLES = r"""
- name: Disable IPv6 on all appliance interfaces
  vmware.vmware_rest.appliance_networking:
    ipv6_enabled: false

- name: Reset appliance networking configuration
  vmware.vmware_rest.appliance_networking:
    state: reset
"""

RETURN = r"""
value:
  description:
    - Networking configuration after update when I(state=present).
  returned: On success when I(state=present)
  type: dict
  sample:
    dns:
      mode: STATIC
      hostname: vcenter.example.com
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
    params_differ,
)

NETWORKING_PATH = "/appliance/networking"

_PAYLOAD_FORMAT = {
    "update": {
        "query": {},
        "body": {"ipv6_enabled": "ipv6_enabled"},
        "path": {},
    },
    "reset": {"query": {}, "body": {}, "path": {}},
}


class VmwareRestModule(VmwareRestModuleBase):
    PAYLOAD_FORMAT = _PAYLOAD_FORMAT

    def _post_reset(self):
        response = self.client.request(
            "POST",
            NETWORKING_PATH,
            query={"action": "reset"},
        )
        if response.status != 204:
            self.client.error_handler.handle_request_error(
                exception=UnexpectedAPIResponse(response.status, response.data),
                method="POST",
                path=NETWORKING_PATH,
                request_kwargs={"query": {"action": "reset"}},
            )

    def run_reset(self):
        if not self.module.check_mode:
            self._post_reset()
        return {"changed": True}

    def ensure_present(self):
        if self.params.get("ipv6_enabled") is None:
            self.module.fail_json(msg="ipv6_enabled is required when state is present.")

        current_response = self.client.get(NETWORKING_PATH)
        current = current_response.json
        update_body = self.build_payload(self.PAYLOAD_FORMAT["update"])
        if not params_differ(current, update_body):
            return {"changed": False, "value": current}

        if not self.module.check_mode:
            patch_response = self.client.patch(NETWORKING_PATH, data=update_body)
            if patch_response.status not in (200, 204):
                self.client.error_handler.handle_request_error(
                    exception=UnexpectedAPIResponse(
                        patch_response.status, patch_response.data
                    ),
                    method="PATCH",
                    path=NETWORKING_PATH,
                    request_kwargs={"data": update_body},
                )

            updated = self.client.get(NETWORKING_PATH)
            return {"changed": True, "value": updated.json}

        return {"changed": True, "value": current}


def main():
    module_args = connection_params_argument_spec()
    module_args["state"] = {
        "type": "str",
        "choices": ["present", "reset"],
        "default": "present",
    }
    module_args["ipv6_enabled"] = {"type": "bool"}

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
        required_if=[("state", "present", ["ipv6_enabled"])],
    )

    rest_module = VmwareRestModule(module)

    if module.params["state"] == "present":
        result = rest_module.ensure_present()
    elif module.params["state"] == "reset":
        result = rest_module.run_reset()
    else:
        module.fail_json(msg="Unsupported state: {0}".format(module.params["state"]))

    module.exit_json(**result)


if __name__ == "__main__":
    main()
