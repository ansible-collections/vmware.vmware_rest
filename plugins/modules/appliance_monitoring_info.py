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
module: appliance_monitoring_info
short_description: Gather information about the monitored statistics of the vCenter Server Appliance.
description:
  - Retrieve information about the metrics that the vCenter Server Appliance monitors, such as CPU,
    memory, network, and storage statistics.
  - When O(stat_id) is provided, return the details of that single monitored item, including its
    display name, category, unit of measure, and description.
  - When O(stat_id) is omitted, list every monitored item available on the appliance.
  - This module only reports the metadata that describes each monitored item. Use
    M(vmware.vmware_rest.appliance_monitoring_query) to retrieve the actual data points for a metric.

author:
  - Ansible Eco Content Team (@eco-ansible-content)

extends_documentation_fragment:
  - vmware.vmware_rest.connection_params

options:
  stat_id:
    description:
      - The identifier of the monitored item to retrieve detailed information for.
      - When omitted, information about all monitored items on the appliance is returned.
      - The value must be the ID of a monitored item returned by this module, for example V(cpu.util)
        or V(mem.util).
    type: str
    required: false

version_added: 5.0.0

requirements: []

notes:
  - Generated from vSphere API spec 9.1.0.
"""

EXAMPLES = r"""
- name: List all monitored items on the appliance
  vmware.vmware_rest.appliance_monitoring_info:
  register: all_stats

- name: Get information about a single monitored item
  vmware.vmware_rest.appliance_monitoring_info:
    stat_id: cpu.util
  register: cpu_stat

- name: Display the unit of measure for the monitored item
  ansible.builtin.debug:
    var: cpu_stat.value.units
"""

RETURN = r"""
id:
  description: The identifier of the monitored item that was queried.
  returned: When only one monitored item, identified by O(stat_id), was queried
  sample: cpu.util
  type: str
value:
  description: Detailed information about a single monitored item.
  returned: When only one monitored item, identified by O(stat_id), was queried
  sample:
    id: cpu.util
    name: CPU utilization
    units: "%"
    category: cpu
    instance: ""
    description: com.vmware.applmgmt.mon.descr.cpu.util
  type: dict
info:
  description: A list of detailed information about the monitored items on the appliance.
  returned: When O(stat_id) is not provided
  elements: dict
  sample:
    - id: cpu.util
      name: CPU utilization
      units: "%"
      category: cpu
      instance: ""
      description: com.vmware.applmgmt.mon.descr.cpu.util
    - id: mem.util
      name: Memory utilization
      units: KB
      category: memory
      instance: ""
      description: com.vmware.applmgmt.mon.descr.mem.util
  type: list
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

MOID_PARAMETER_HINTS = ["stat_id"]

LIST_ENDPOINT = "/appliance/monitoring"
ITEM_ENDPOINT = "/appliance/monitoring/{stat_id}"


LIST_OPERATION = OperationConfig(
    name="list",
    uri=LIST_ENDPOINT,
    http_method="GET",
)

GET_OPERATION = OperationConfig(
    name="get",
    uri=ITEM_ENDPOINT,
    http_method="GET",
)


def create_module_argument_spec() -> dict:
    module_args = connection_params_argument_spec()
    module_args["stat_id"] = {
        "type": "str",
    }
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
        list_operation_config=LIST_OPERATION,
    )
    try:
        result = info_module.get_resource_info()
    except VmwareModuleError as e:
        module.fail_json(**e.to_module_fail_json_output())
    module.exit_json(**result)


if __name__ == "__main__":
    main()
