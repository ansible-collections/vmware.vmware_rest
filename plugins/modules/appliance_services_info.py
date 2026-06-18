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
module: appliance_services_info
short_description: Get information about vCenter appliance services.
description:
  - Returns information about vCenter Server appliance services.
  - When I(service) is specified, returns the state and description of that service.
  - When I(service) is omitted, lists all services with their state and description.
author:
  - Ansible Eco Content Team (@eco-ansible-content)
extends_documentation_fragment:
  - vmware.vmware_rest.connection_params
options:
  service:
    description:
      - Identifier of the service whose state is being queried.
      - Must be an identifier (MOID) for a C(com.vmware.appliance.services) resource.
      - When specified, only that service is returned.
    type: str
version_added: 4.11.0
requirements: []
notes:
  - Generated from vSphere API spec 9.1.0.
  - Has support for vSphere API 7.0.3.
  - Has support for vSphere API 8.0.2.
"""

EXAMPLES = r"""
- name: List all appliance services
  vmware.vmware_rest.appliance_services_info:
  register: services

- name: Get information about the ntpd service
  vmware.vmware_rest.appliance_services_info:
    service: ntpd
  register: ntpd_info
"""

RETURN = r"""
value:
  description:
    - Service information.
    - Returns a list of service dictionaries when I(service) is omitted.
    - Returns a single service dictionary when I(service) is specified.
  returned: On success
  type: raw
  sample:
    description: ntpd.service
    id: ntpd
    state: STARTED
  contains:
    id:
      description:
        - Service identifier (MOID).
      type: str
      sample: ntpd
    description:
      description:
        - Service description.
      type: str
      sample: ntpd.service
    state:
      description:
        - Running state of the service.
      type: str
      sample: STARTED
      choices:
        - STARTING
        - STOPPING
        - STARTED
        - STOPPED
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

LIST_PATH = "/appliance/services"
SERVICE_PATH = "/appliance/services/{service}"


class VmwareRestInfoModule(VmwareRestInfoModuleBase):
    PAYLOAD_FORMAT = {
        "list": {"query": {}, "body": {}, "path": {}},
        "get": {"query": {}, "body": {}, "path": {"service": "service"}},
    }

    def _get_service(self, service):
        response = self.client.get(self.build_path(SERVICE_PATH, {"service": service}))
        if response.status == 404:
            self.client.error_handler.handle_request_error(
                exception=UnexpectedAPIResponse(response.status, response.data),
                method="GET",
                path=self.build_path(SERVICE_PATH, {"service": service}),
                request_kwargs={},
            )
        info = response.json
        info["id"] = service
        return info

    def get_info(self):
        service = self.params.get("service")
        if service:
            return self._get_service(service)

        response = self.client.get(LIST_PATH)
        if response.status == 404:
            return []

        services_map = response.json
        if not isinstance(services_map, dict):
            return []

        result = []
        for service_id, info in services_map.items():
            entry = dict(info)
            entry["id"] = service_id
            result.append(entry)
        return result


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
