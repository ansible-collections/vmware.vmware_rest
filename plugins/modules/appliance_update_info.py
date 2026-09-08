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
module: appliance_update_info
short_description: Gather information about the current appliance update status.
description:
  - Retrieve the current status of the vCenter Server Appliance update.
  - Reports whether the appliance is up to date, has updates pending, or is
    currently staging or installing an update.
  - Returns the relevant version string and, when available, details about the
    running or completed update task and the time of the last query to the
    update repository.
  - Use this module to check for available appliance updates or to monitor the
    progress of an ongoing update.

author:
  - Ansible Eco Content Team (@eco-ansible-content)

extends_documentation_fragment:
  - vmware.vmware_rest.connection_params

options: {}

version_added: 5.0.0

requirements: []

notes:
  - Generated from vSphere API spec 9.1.0.
"""

EXAMPLES = r"""
- name: Gather the current appliance update status
  vmware.vmware_rest.appliance_update_info:
  register: appliance_update

- name: Show the appliance update state and version
  ansible.builtin.debug:
    msg: "Update state is {{ appliance_update.value.state }} for version {{ appliance_update.value.version }}"
"""

RETURN = r"""
value:
  description: Detailed information about the current appliance update status.
  returned: On success
  type: dict
  sample:
    state: "UP_TO_DATE"
    version: "9.1.0.10000"
    latest_query_time: "2024-07-31T18:18:32.000Z"
info:
  description: A list containing the current appliance update status.
  returned: On success
  elements: dict
  type: list
  sample:
    - state: "UP_TO_DATE"
      version: "9.1.0.10000"
      latest_query_time: "2024-07-31T18:18:32.000Z"
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
ITEM_ENDPOINT = "/appliance/update"


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
