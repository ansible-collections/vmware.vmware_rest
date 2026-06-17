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
module: appliance_services
short_description: Manage vCenter appliance services.
description:
  - Starts, stops, or restarts a vCenter Server appliance service.
  - Use I(state=start) to start a service, I(state=stop) to stop a service, and
    I(state=restart) to restart a service.
  - The module is idempotent for I(state=start) and I(state=stop) when the service
    is already in the requested run state.
author:
  - Ansible Eco Content Team (@eco-ansible-content)
extends_documentation_fragment:
  - vmware.vmware_rest.connection_params
options:
  state:
    description:
      - The desired service action.
      - Use C(start) to start the service.
      - Use C(stop) to stop the service.
      - Use C(restart) to restart the service.
    type: str
    choices:
      - start
      - stop
      - restart
    required: true
  service:
    description:
      - Identifier of the service to manage.
      - Must be an identifier (MOID) for a C(com.vmware.appliance.services) resource.
    type: str
    required: true
version_added: 4.11.0
requirements: []
notes:
  - Generated from vSphere API spec 9.1.0.
  - Has support for vSphere API 7.0.3.
  - Has support for vSphere API 8.0.2.
"""

EXAMPLES = r"""
- name: Stop the ntpd service
  vmware.vmware_rest.appliance_services:
    service: ntpd
    state: stop

- name: Start the ntpd service
  vmware.vmware_rest.appliance_services:
    service: ntpd
    state: start

- name: Restart the ntpd service
  vmware.vmware_rest.appliance_services:
    service: ntpd
    state: restart
"""

RETURN = r"""
value:
  description:
    - Current service information when no change was required.
  returned: On success when the service was already in the desired run state
  type: dict
  sample:
    description: ntpd.service
    state: STARTED
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.vmware.vmware_rest.plugins.module_utils._argument_spec import (
    connection_params_argument_spec,
)
from ansible_collections.vmware.vmware_rest.plugins.module_utils._errors import (
    UnexpectedAPIResponse,
)
from ansible_collections.vmware.vmware_rest.plugins.module_utils._module_base import (
    VmwareRestCrudModuleBase,
)

SERVICE_PATH = "/appliance/services/{service}"

PAYLOAD_FORMAT = {
    "start": {
        "query": {"action": "start"},
        "body": {},
        "path": {"service": "service"},
    },
    "stop": {
        "query": {"action": "stop"},
        "body": {},
        "path": {"service": "service"},
    },
    "restart": {
        "query": {"action": "restart"},
        "body": {},
        "path": {"service": "service"},
    },
}


class VmwareRestCrudModule(VmwareRestCrudModuleBase):
    PAYLOAD_FORMAT = PAYLOAD_FORMAT

    UPDATABLE_PARAMS = ()

    def _get_service_info(self):
        path = self.build_path(SERVICE_PATH)
        response = self.client.get(path)
        if response.status == 404:
            self.client.error_handler.handle_request_error(
                exception=UnexpectedAPIResponse(response.status, response.data),
                method="GET",
                path=path,
                request_kwargs={},
            )
        return response.json

    def _post_action(self, action):
        path = self.build_path(SERVICE_PATH)
        query = {"action": action}
        response = self.client.request("POST", path, query=query)
        if response.status != 204:
            self.client.error_handler.handle_request_error(
                exception=UnexpectedAPIResponse(response.status, response.data),
                method="POST",
                path=path,
                request_kwargs={"query": query},
            )

    def run_action(self, action):
        current = self._get_service_info()
        current_state = current.get("state")

        if action == "start" and current_state == "STARTED":
            return {"changed": False, "value": current}
        if action == "stop" and current_state == "STOPPED":
            return {"changed": False, "value": current}

        if not self.module.check_mode:
            self._post_action(action)
        return {"changed": True}

    def ensure_present(self):
        self.module.fail_json(
            msg="Use state start, stop, or restart to manage appliance services."
        )

    def ensure_absent(self):
        self.module.fail_json(
            msg="Use state start, stop, or restart to manage appliance services."
        )


def main():
    module_args = connection_params_argument_spec()
    module_args["state"] = {
        "type": "str",
        "choices": ["start", "stop", "restart"],
        "required": True,
    }
    module_args["service"] = {"type": "str", "required": True}

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
    )

    crud_module = VmwareRestCrudModule(module)
    result = crud_module.run_action(module.params["state"])
    module.exit_json(**result)


if __name__ == "__main__":
    main()
