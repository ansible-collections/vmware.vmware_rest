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
module: appliance_shutdown_info
short_description: Get details about the pending shutdown action.
description:
  - Returns configuration of a pending vCenter Server appliance shutdown or reboot.
  - When no shutdown is scheduled, the C(action) field is an empty string.
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
- name: Check if there is a shutdown scheduled
  vmware.vmware_rest.appliance_shutdown_info:
  register: pending_shutdown

- name: Display pending shutdown details
  ansible.builtin.debug:
    var: pending_shutdown.value
"""

RETURN = r"""
value:
  description:
    - Pending shutdown configuration.
  returned: On success
  type: dict
  sample:
    action: reboot
    reason: this is an example
    shutdown_time: '2022-11-24T06:12:16.000Z'
  contains:
    action:
      description:
        - Pending shutdown operation.
        - C(poweroff) indicates a power off is scheduled.
        - C(reboot) indicates a reboot is scheduled.
        - An empty string indicates no shutdown is scheduled.
      type: str
      sample: reboot
    reason:
      description:
        - Reason for the pending shutdown action.
      type: str
      sample: this is an example
    shutdown_time:
      description:
        - Scheduled shutdown time in ISO-8601 format.
      type: str
      sample: '2022-11-24T06:12:16.000Z'
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.vmware.vmware_rest.plugins.module_utils._argument_spec import (
    connection_params_argument_spec,
)
from ansible_collections.vmware.vmware_rest.plugins.module_utils._module_base import (
    VmwareRestInfoModuleBase,
)

SHUTDOWN_PATH = "/appliance/shutdown"


class VmwareRestInfoModule(VmwareRestInfoModuleBase):
    PAYLOAD_FORMAT = {
        "get": {"query": {}, "body": {}, "path": {}},
    }

    def get_info(self):
        response = self.client.get(SHUTDOWN_PATH)
        if response.status == 404:
            return {}
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
