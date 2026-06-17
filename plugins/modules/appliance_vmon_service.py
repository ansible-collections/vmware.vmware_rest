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
module: appliance_vmon_service
short_description: Manage vMon-managed vCenter appliance services.
description:
  - Updates startup type and controls run state of services managed by vMon.
  - Use I(state=present) with I(startup_type) to update service startup configuration.
  - Use I(state=start), I(state=stop), or I(state=restart) to control service run state.
author:
  - Ansible Eco Content Team (@eco-ansible-content)
extends_documentation_fragment:
  - vmware.vmware_rest.connection_params
options:
  state:
    description:
      - The desired service operation.
      - Use C(present) to update I(startup_type).
      - Use C(start), C(stop), or C(restart) to control the service run state.
    type: str
    choices:
      - present
      - start
      - stop
      - restart
    default: present
  service:
    description:
      - Identifier of the vMon-managed service.
      - Must be an identifier for a C(appliance.vmon.Service) resource.
    type: str
    required: true
  startup_type:
    description:
      - Startup type for the service.
      - Required when I(state=present).
    type: str
    choices:
      - AUTOMATIC
      - DISABLED
      - MANUAL
version_added: 4.11.0
requirements: []
notes:
  - Generated from vSphere API spec 8.0.2.
  - Has support for vSphere API 7.0.3.
  - This API endpoint is deprecated in vSphere 8.0.2 and the module will not be compatible with future versions of vSphere.
"""

EXAMPLES = r"""
- name: Set vpxd startup type to automatic
  vmware.vmware_rest.appliance_vmon_service:
    service: vpxd
    startup_type: AUTOMATIC

- name: Start the vpxd service
  vmware.vmware_rest.appliance_vmon_service:
    service: vpxd
    state: start

- name: Stop the vpxd service
  vmware.vmware_rest.appliance_vmon_service:
    service: vpxd
    state: stop
"""

RETURN = r"""
value:
  description:
    - Current service information when no change was required.
  returned: On success when the service was already in the desired state
  type: dict
  sample:
    startup_type: AUTOMATIC
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

SERVICE_PATH = "/rest/appliance/vmon/service/{service}"
START_PATH = "/rest/appliance/vmon/service/{service}/start"
STOP_PATH = "/rest/appliance/vmon/service/{service}/stop"
RESTART_PATH = "/rest/appliance/vmon/service/{service}/restart"


class VmwareRestCrudModule(VmwareRestCrudModuleBase):
    PAYLOAD_FORMAT = {
        "update": {"query": {}, "body": {}, "path": {"service": "service"}},
        "start": {"query": {}, "body": {}, "path": {"service": "service"}},
        "stop": {"query": {}, "body": {}, "path": {"service": "service"}},
        "restart": {"query": {}, "body": {}, "path": {"service": "service"}},
    }

    UPDATABLE_PARAMS = ()

    def _unwrap_service_info(self, payload):
        if isinstance(payload, dict) and "value" in payload:
            return payload["value"]
        return payload

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
        return self._unwrap_service_info(response.json)

    def _post_action(self, action):
        path_map = {
            "start": START_PATH,
            "stop": STOP_PATH,
            "restart": RESTART_PATH,
        }
        path = self.build_path(path_map[action])
        response = self.client.request("POST", path)
        if response.status != 200:
            self.client.error_handler.handle_request_error(
                exception=UnexpectedAPIResponse(response.status, response.data),
                method="POST",
                path=path,
                request_kwargs={},
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
        startup_type = self.params.get("startup_type")
        if startup_type is None:
            self.module.fail_json(
                msg="startup_type is required when state is present."
            )

        current = self._get_service_info()
        if current.get("startup_type") == startup_type:
            return {"changed": False, "value": current}

        path = self.build_path(SERVICE_PATH)
        update_body = {"spec": {"startup_type": startup_type}}
        if not self.module.check_mode:
            patch_response = self.client.patch(path, data=update_body)
            if patch_response.status not in (200, 204):
                self.client.error_handler.handle_request_error(
                    exception=UnexpectedAPIResponse(
                        patch_response.status, patch_response.data
                    ),
                    method="PATCH",
                    path=path,
                    request_kwargs={"data": update_body},
                )

            updated = self._get_service_info()
            return {"changed": True, "value": updated}

        return {"changed": True, "value": current}

    def ensure_absent(self):
        self.module.fail_json(
            msg="Use state present, start, stop, or restart to manage vMon services."
        )


def main():
    module_args = connection_params_argument_spec()
    module_args["state"] = {
        "type": "str",
        "choices": ["present", "start", "stop", "restart"],
        "default": "present",
    }
    module_args["service"] = {"type": "str", "required": True}
    module_args["startup_type"] = {
        "type": "str",
        "choices": ["AUTOMATIC", "DISABLED", "MANUAL"],
    }

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
        required_if=[("state", "present", ["startup_type"])],
    )

    crud_module = VmwareRestCrudModule(module)
    state = module.params["state"]

    if state == "present":
        result = crud_module.ensure_present()
    elif state in ("start", "stop", "restart"):
        result = crud_module.run_action(state)
    else:
        module.fail_json(msg="Unsupported state: {0}".format(state))

    module.exit_json(**result)


if __name__ == "__main__":
    main()
