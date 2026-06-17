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
module: appliance_vmon_service_info
short_description: Get vMon-managed vCenter appliance service information.
description:
  - Returns information about services managed by vMon.
  - When I(service) is omitted, returns a list of service entries with C(key) and
    C(value) fields.
  - When I(service) is specified, returns a single service information dictionary.
author:
  - Ansible Eco Content Team (@eco-ansible-content)
extends_documentation_fragment:
  - vmware.vmware_rest.connection_params
options:
  service:
    description:
      - Identifier of the vMon-managed service.
      - Must be an identifier for a C(appliance.vmon.Service) resource.
    type: str
version_added: 4.11.0
requirements: []
notes:
  - Generated from vSphere API spec 8.0.2.
  - Has support for vSphere API 7.0.3.
  - This API endpoint is deprecated in vSphere 8.0.2 and the module will not be compatible with future versions of vSphere.
"""

EXAMPLES = r"""
- name: List all vMon-managed services
  vmware.vmware_rest.appliance_vmon_service_info:
  register: vmon_services

- name: Get information about the vpxd service
  vmware.vmware_rest.appliance_vmon_service_info:
    service: vpxd
  register: vpxd_service
"""

RETURN = r"""
value:
  description:
    - Service information.
    - Returns a list of C(key)/C(value) dictionaries when I(service) is omitted.
    - Returns a single service dictionary when I(service) is specified.
  returned: On success
  type: raw
  sample:
    - key: vpxd
      value:
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
    VmwareRestInfoModuleBase,
)

LIST_PATH = "/rest/appliance/vmon/service"
SERVICE_PATH = "/rest/appliance/vmon/service/{service}"


class VmwareRestInfoModule(VmwareRestInfoModuleBase):
    PAYLOAD_FORMAT = {
        "list": {"query": {}, "body": {}, "path": {}},
        "get": {"query": {}, "body": {}, "path": {"service": "service"}},
    }

    def _get_service(self, service):
        path = self.build_path(SERVICE_PATH, {"service": service})
        response = self.client.get(path)
        if response.status == 404:
            self.client.error_handler.handle_request_error(
                exception=UnexpectedAPIResponse(response.status, response.data),
                method="GET",
                path=path,
                request_kwargs={},
            )
        payload = response.json
        if isinstance(payload, dict) and "value" in payload:
            return payload["value"]
        return payload

    def get_info(self):
        service = self.params.get("service")
        if service:
            return self._get_service(service)

        response = self.client.get(LIST_PATH)
        if response.status == 404:
            return []

        payload = response.json
        if isinstance(payload, dict) and "value" in payload:
            return payload["value"]
        return payload


def main():
    module_args = connection_params_argument_spec()
    module_args["service"] = {"type": "str"}

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
    )

    info_module = VmwareRestInfoModule(module)
    result = info_module.get_info()
    module.exit_json(value=result)


if __name__ == "__main__":
    main()
