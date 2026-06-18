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
module: appliance_health_database_info
short_description: Returns the health status of the database.
description:
  - Returns the health status of the vCenter appliance database.
  - Includes an overall status and any health messages reported by the appliance.
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
  - This API endpoint is deprecated in vSphere 9.1.0 and the module will not be compatible with future versions of vSphere.
"""

EXAMPLES = r"""
- name: Get the database health status
  vmware.vmware_rest.appliance_health_database_info:
  register: result
"""

RETURN = r"""
value:
  description:
    - Database health information.
  returned: On success
  type: dict
  contains:
    status:
      description:
        - Database health status.
      type: str
      sample: HEALTHY
    messages:
      description:
        - Messages describing any issues with the database, along with their severity.
      type: list
      elements: dict
      contains:
        severity:
          description:
            - Severity of the message.
          type: str
          sample: WARNING
        message:
          description:
            - Message describing the issue with the database.
          type: dict
          contains:
            id:
              description:
                - Unique identifier of the localizable message.
              type: str
            default_message:
              description:
                - Message text in the C(en_US) locale.
              type: str
            args:
              description:
                - Positional arguments substituted into the message template.
              type: list
              elements: str
  sample:
    status: HEALTHY
    messages: []
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.vmware.vmware_rest.plugins.module_utils._argument_spec import (
    connection_params_argument_spec,
)
from ansible_collections.vmware.vmware_rest.plugins.module_utils._module_base import (
    VmwareRestInfoModuleBase,
)

DATABASE_HEALTH_PATH = "/appliance/health/database"


class VmwareRestInfoModule(VmwareRestInfoModuleBase):
    PAYLOAD_FORMAT = {
        "get": {"query": {}, "body": {}, "path": {}},
    }

    def get_info(self):
        response = self.client.get(DATABASE_HEALTH_PATH)
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
