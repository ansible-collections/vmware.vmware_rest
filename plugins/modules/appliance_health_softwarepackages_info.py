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
short_description: Get the health status of available software updates for the vCenter Server Appliance.
description:
  - Returns information about software updates available in the remote vSphere Update Manager repository.
  - The status is reported as a color code where V(red) means security updates are available, V(orange) means non-security
    updates are available, V(green) means no updates are available, and V(gray) means the update information could not be retrieved.
  - Use this module to detect whether the appliance has pending software or security updates.

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
"""

EXAMPLES = r"""
- name: Get the appliance software packages health status
  vmware.vmware_rest.appliance_health_softwarepackages_info:
  register: softwarepackages_health

- name: Display the appliance software packages health status
  ansible.builtin.debug:
    var: softwarepackages_health.value
"""

RETURN = r"""
value:
  description:
    - The health status of available software updates for the appliance.
    - V(red) indicates security updates are available, V(orange) indicates non-security updates are available,
      V(green) indicates no updates are available, and V(gray) indicates the update information could not be retrieved.
  returned: On success
  sample: green
  type: str
info:
  description:
    - The same information as RV(value), returned as a list for consistency with other info modules.
    - This endpoint returns a single item, so the list always contains one element.
  returned: On success
  sample:
    - green
  type: list
  elements: str
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
ITEM_ENDPOINT = "/appliance/health/software-packages"


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
