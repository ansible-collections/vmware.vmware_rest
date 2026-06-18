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
module: appliance_health_softwarepackages_info
short_description: Retrieves software update health of the vCenter appliance.
description:
  - Retrieves information about available software updates in the remote vSphere Update Manager repository.
  - V(red) indicates that security updates are available.
  - V(orange) indicates that non-security updates are available.
  - V(green) indicates that there are no updates available.
  - V(gray) indicates that there was an error retrieving information on software updates.
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
- name: Get vCenter appliance software update health
  vmware.vmware_rest.appliance_health_softwarepackages_info:
  register: appliance_softwarepackages_health
"""

RETURN = r"""
value:
  description:
    - Software update health level of the vCenter Server appliance.
    - V(green) indicates there are no updates available.
    - V(orange) indicates non-security updates are available.
    - V(red) indicates security updates are available.
    - V(gray) indicates an error retrieving software update information.
    - V(yellow) indicates the service is healthy but experiencing some level of problems.
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

SOFTWARE_PACKAGES_HEALTH_PATH = "/appliance/health/software-packages"


class VmwareRestInfoModule(VmwareRestInfoModuleBase):
    PAYLOAD_FORMAT = {
        "get": {"query": {}, "body": {}, "path": {}},
    }

    def get_info(self):
        response = self.client.get(SOFTWARE_PACKAGES_HEALTH_PATH)
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
