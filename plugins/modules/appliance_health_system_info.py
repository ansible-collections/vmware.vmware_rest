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
module: appliance_health_system_info
short_description: Get overall health of system.
description:
  - Returns the overall health level of the vCenter Server appliance system.
  - Possible health levels include C(green), C(yellow), C(orange), C(red), and C(gray).
author:
  - Ansible Eco Content Team (@eco-ansible-content)
extends_documentation_fragment:
  - vmware.vmware_rest.connection_params
options: {}
version_added: 4.11.0
requirements: []
notes:
  - Generated from vSphere API spec 9.1.0.
  - Has support for vSphere API 7.0.3.
  - Has support for vSphere API 8.0.2.
"""

EXAMPLES = r"""
- name: Get overall vCenter appliance system health
  vmware.vmware_rest.appliance_health_system_info:
  register: appliance_system_health
"""

RETURN = r"""
value:
  description:
    - Overall system health level of the vCenter Server appliance.
    - C(green) indicates the service is healthy.
    - C(yellow) indicates the service is healthy but experiencing some problems.
    - C(orange) indicates degraded health that might have serious problems.
    - C(red) indicates the service is unavailable or not functioning properly.
    - C(gray) indicates no health data is available for this service.
  returned: On success
  type: str
  sample: green
  choices:
    - orange
    - gray
    - green
    - red
    - yellow
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.vmware.vmware_rest.plugins.module_utils._argument_spec import (
    connection_params_argument_spec,
)
from ansible_collections.vmware.vmware_rest.plugins.module_utils._module_base import (
    VmwareRestInfoModuleBase,
)

SYSTEM_HEALTH_PATH = "/appliance/health/system"


class VmwareRestInfoModule(VmwareRestInfoModuleBase):
    PAYLOAD_FORMAT = {
        "get": {"query": {}, "body": {}, "path": {}},
    }

    def get_info(self):
        response = self.client.get(SYSTEM_HEALTH_PATH)
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
