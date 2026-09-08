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
short_description: Gather the current system time of the vCenter Server Appliance.
description:
  - Retrieve the current system time reported by the vCenter Server Appliance.
  - Returns the date, the time, the configured timezone, and the number of seconds
    since the epoch as seen by the appliance.
  - Use this module to verify that the appliance clock and timezone are set correctly,
    which is important for certificate validation, logging, and authentication.

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
- name: Gather the current system time of the appliance
  vmware.vmware_rest.appliance_system_time_info:
  register: system_time

- name: Show the appliance date, time, and timezone
  ansible.builtin.debug:
    msg: "The appliance time is {{ system_time.value.date }} {{ system_time.value.time }} ({{ system_time.value.timezone }})"
"""

RETURN = r"""
value:
  description: Detailed information about the current system time of the appliance.
  returned: On success
  type: dict
  sample:
    date: "Thu 07-31-2014"
    time: "18:18:32"
    timezone: "UTC"
    seconds_since_epoch: 1406830712.0
info:
  description: A list containing the current system time of the appliance.
  returned: On success
  elements: dict
  type: list
  sample:
    - date: "Thu 07-31-2014"
      time: "18:18:32"
      timezone: "UTC"
      seconds_since_epoch: 1406830712.0
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
ITEM_ENDPOINT = "/appliance/system/time"


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
