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
module: appliance_system_time_info
short_description: Get vCenter appliance system time.
description:
  - Returns the current system time of the vCenter Server appliance.
  - Includes the date, time, time zone, and seconds since the Unix epoch.
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
- name: Get vCenter appliance system time
  vmware.vmware_rest.appliance_system_time_info:
  register: appliance_system_time
"""

RETURN = r"""
value:
  description:
    - System time information for the vCenter Server appliance.
  returned: On success
  type: dict
  contains:
    seconds_since_epoch:
      description:
        - Number of seconds since the Unix epoch.
      type: float
      sample: 1406835512.0
    date:
      description:
        - Date string in the format C(Thu 07-31-2014).
      type: str
      sample: Thu 07-31-2014
    time:
      description:
        - Time string in the format C(18:18:32).
      type: str
      sample: 18:18:32
    timezone:
      description:
        - Configured time zone of the appliance.
      type: str
      sample: UTC
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.vmware.vmware_rest.plugins.module_utils._argument_spec import (
    connection_params_argument_spec,
)
from ansible_collections.vmware.vmware_rest.plugins.module_utils._module_base import (
    VmwareRestInfoModuleBase,
)

SYSTEM_TIME_PATH = "/appliance/system/time"


class VmwareRestInfoModule(VmwareRestInfoModuleBase):
    PAYLOAD_FORMAT = {
        "get": {"query": {}, "body": {}, "path": {}},
    }

    def get_info(self):
        response = self.client.get(SYSTEM_TIME_PATH)
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
