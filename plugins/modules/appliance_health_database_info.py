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
short_description: Get the health status of the vCenter Server Appliance database.
description:
  - Returns the health status of the database used by the vCenter Server Appliance.
  - The response reports an overall status along with any messages describing database issues and their severity.
  - Use this module to detect database corruption or degradation that could impact vCenter Server functionality.

author:
  - Ansible Eco Content Team (@eco-ansible-content)

extends_documentation_fragment:
  - vmware.vmware_rest.connection_params

options: {}

version_added: 5.0.0

requirements: []

notes:
  - Generated from vSphere API spec 9.1.0.
  - Compatible with vSphere API 7.0.3.
  - Compatible with vSphere API 8.0.2.
  - This endpoint is deprecated as of vSphere 9.1.0.
"""

EXAMPLES = r"""
- name: Get the appliance database health status
  vmware.vmware_rest.appliance_health_database_info:
  register: database_health

- name: Display the appliance database health status
  ansible.builtin.debug:
    var: database_health.value
"""

RETURN = r"""
value:
  description: The health status of the appliance database.
  returned: On success
  type: dict
  contains:
    status:
      description:
        - The overall health status of the database.
        - V(HEALTHY) means the database is healthy, V(DEGRADED) means it has issues with low impact on vCenter Server,
          and V(UNHEALTHY) means the database is corrupted and vCenter Server functionality will be impacted.
      returned: On success
      type: str
      sample: HEALTHY
    messages:
      description: Messages describing any issues with the database, along with their severity.
      returned: On success
      type: list
      elements: dict
      contains:
        severity:
          description: The severity of the message, either V(ERROR) or V(WARNING).
          returned: On success
          type: str
          sample: WARNING
        message:
          description: A localizable message describing the issue with the database.
          returned: On success
          type: dict
  sample:
    status: HEALTHY
    messages: []
info:
  description:
    - The same information as RV(value), returned as a list for consistency with other info modules.
    - This endpoint returns a single item, so the list always contains one element.
  returned: On success
  type: list
  elements: dict
  sample:
    - status: HEALTHY
      messages: []
"""


from ansible.module_utils.basic import AnsibleModule
from ansible_collections.vmware.vmware_rest.plugins.module_utils._argument_spec import (
    connection_params_argument_spec,
)
from ansible_collections.vmware.vmware_rest.plugins.module_utils._errors import (
    VmwareModuleError,
)
from ansible_collections.vmware.vmware_rest.plugins.module_utils._info_module import (
    VmwareRestInfoModuleBase,
)
from ansible_collections.vmware.vmware_rest.plugins.module_utils._operation_configs import (
    OperationConfig,
)

MOID_PARAMETER_HINTS = []

LIST_ENDPOINT = ""
ITEM_ENDPOINT = "/appliance/health/database"


GET_OPERATION = OperationConfig(
    name="get",
    uri=ITEM_ENDPOINT,
    http_method="GET",
)


def create_module_argument_spec() -> dict:
    module_args = connection_params_argument_spec()
    return module_args


def main():
    module = AnsibleModule(
        argument_spec=create_module_argument_spec(),
        supports_check_mode=True,
    )

    info_module = VmwareRestInfoModuleBase(
        module=module,
        moid_parameter_hints=MOID_PARAMETER_HINTS,
        get_operation_config=GET_OPERATION,
    )
    try:
        result = info_module.get_resource_info()
    except VmwareModuleError as e:
        module.fail_json(**e.to_module_fail_json_output())
    module.exit_json(**result)


if __name__ == "__main__":
    main()
