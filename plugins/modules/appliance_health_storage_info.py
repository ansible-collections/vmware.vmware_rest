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
module: appliance_health_storage_info
short_description: Retrieves storage health for the vCenter Server Appliance.
description:
  - Returns the storage health level of the vCenter Server Appliance.
  - Uses the vSphere REST API endpoint C(GET /appliance/health/storage).
author:
  - Ansible Eco Content Team (@eco-ansible-content)
extends_documentation_fragment:
  - vmware.vmware_rest.connection_params
version_added: 4.11.0
requirements: []
notes:
  - Generated from vSphere API spec 9.1.0.
  - Has support for vSphere API 7.0.3.
  - Has support for vSphere API 8.0.2.
"""

EXAMPLES = r"""
- name: Get the health of the storage system
  vmware.vmware_rest.appliance_health_storage_info:
  register: storage_health

- name: Assert storage health is green
  ansible.builtin.assert:
    that:
      - storage_health.value == "green"
"""

RETURN = r"""
value:
  description:
    - Storage health level for the vCenter Server Appliance.
    - C(green) indicates the service is healthy.
    - C(yellow) indicates the service is healthy but experiencing problems.
    - C(orange) indicates degraded health with serious problems.
    - C(red) indicates the service is unavailable or not functioning properly.
    - C(gray) indicates no health data is available.
  returned: On success
  type: str
  sample: green
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.vmware.vmware_rest.plugins.module_utils._argument_spec import (
    connection_params_argument_spec,
)
from ansible_collections.vmware.vmware_rest.plugins.module_utils._module_base import (
    VmwareRestInfoModuleBase,
)

STORAGE_HEALTH_PATH = "/appliance/health/storage"


class VmwareRestInfoModule(VmwareRestInfoModuleBase):
    PAYLOAD_FORMAT = {
        "get": {"query": {}, "body": {}, "path": {}},
    }

    def get_info(self):
        response = self.client.get(STORAGE_HEALTH_PATH)
        if response.status == 404:
            return None
        return response.json


def main():
    module_args = connection_params_argument_spec()

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
    )

    info_module = VmwareRestInfoModule(module)
    result = info_module.get_info()
    module.exit_json(value=result)


if __name__ == "__main__":
    main()
