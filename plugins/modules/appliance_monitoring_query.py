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
module: appliance_monitoring_query
short_description: Query the monitored statistics data of the vCenter Server Appliance.
description:
  - Retrieve the recorded data points for one or more monitored items on the vCenter Server Appliance,
    such as CPU, memory, network, or storage usage over a period of time.
  - The data is returned as a time series aggregated over a chosen interval using a chosen aggregation
    function (for example, the average CPU utilization sampled every five minutes).
  - Use M(vmware.vmware_rest.appliance_monitoring_info) to discover which monitored item IDs are
    available before querying their data with this module.

author:
  - Ansible Eco Content Team (@eco-ansible-content)

extends_documentation_fragment:
  - vmware.vmware_rest.connection_params

options:
  item:
    description:
      - The parameters that define the time range and shape of the data to return.
      - Describes the sampling interval, the aggregation function, and the start and end of the
        period to query.
    type: dict
    required: true
    suboptions:
      interval:
        description:
          - The time between each returned data point.
          - V(MINUTES30) - Thirty minutes between values. One week is 336 values.
          - V(HOURS2) - Two hours between values. One month has 360 values.
          - V(MINUTES5) - Five minutes between values (the finest interval). One day has 288 values,
            one week is 2016.
          - V(DAY1) - 24 hours between values. One year has 365 values.
          - V(HOURS6) - Six hours between values. One quarter is 360 values.
        type: str
        required: true
        choices:
          - MINUTES30
          - HOURS2
          - MINUTES5
          - DAY1
          - HOURS6
      function:
        description:
          - How the raw samples are aggregated into each returned data point.
          - V(COUNT) - Uses the count (sum) per period.
          - V(MAX) - Uses the maximum per period.
          - V(AVG) - Uses the average per period.
          - V(MIN) - Uses the minimum per period.
        type: str
        required: true
        choices:
          - COUNT
          - MAX
          - AVG
          - MIN
      start_time:
        description:
          - The start of the time range to query, as an ISO 8601 timestamp in UTC,
            for example V(2026-01-01T00:00:00.000Z).
        type: str
        required: true
      end_time:
        description:
          - The end of the time range to query, as an ISO 8601 timestamp in UTC,
            for example V(2026-01-01T12:00:00.000Z).
        type: str
        required: true
  names:
    aliases:
      - filter_names
    description:
      - The IDs of the monitored items to query data for, for example V(cpu.util) or V(mem.util).
      - The available IDs can be listed with M(vmware.vmware_rest.appliance_monitoring_info).
    type: list
    required: true
    elements: str

version_added: 5.0.0

requirements: []

notes:
  - Generated from vSphere API spec 9.1.0.
  - Compatible with vSphere API 7.0.3.
  - Compatible with vSphere API 8.0.2.
"""

EXAMPLES = r"""
- name: Query average CPU utilization over the last day at five minute intervals
  vmware.vmware_rest.appliance_monitoring_query:
    item:
      interval: MINUTES5
      function: AVG
      start_time: "2026-01-01T00:00:00.000Z"
      end_time: "2026-01-02T00:00:00.000Z"
    names:
      - cpu.util
  register: cpu_data

- name: Query maximum CPU and memory usage over a week at thirty minute intervals
  vmware.vmware_rest.appliance_monitoring_query:
    item:
      interval: MINUTES30
      function: MAX
      start_time: "2026-01-01T00:00:00.000Z"
      end_time: "2026-01-08T00:00:00.000Z"
    names:
      - cpu.util
      - mem.util
  register: usage_data

- name: Display the data points returned for the first monitored item
  ansible.builtin.debug:
    var: usage_data.info[0].data
"""

RETURN = r"""
value:
  description:
    - The queried monitoring data.
    - A single monitored item's data as a dictionary when only one item was returned, otherwise a
      list of monitored item data dictionaries.
  returned: On success
  sample:
    name: cpu.util
    interval: MINUTES5
    function: AVG
    start_time: "2026-01-01T00:00:00.000Z"
    end_time: "2026-01-02T00:00:00.000Z"
    data:
      - "3.5"
      - "4.1"
      - "2.9"
  type: raw
info:
  description: A list of the monitored item data returned by the query.
  returned: On success
  elements: dict
  sample:
    - name: cpu.util
      interval: MINUTES5
      function: AVG
      start_time: "2026-01-01T00:00:00.000Z"
      end_time: "2026-01-02T00:00:00.000Z"
      data:
        - "3.5"
        - "4.1"
        - "2.9"
    - name: mem.util
      interval: MINUTES5
      function: AVG
      start_time: "2026-01-01T00:00:00.000Z"
      end_time: "2026-01-02T00:00:00.000Z"
      data:
        - "512000"
        - "524288"
        - "530012"
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

MOID_PARAMETER_HINTS = []

LIST_ENDPOINT = ""
ITEM_ENDPOINT = "/appliance/monitoring/query"


GET_OPERATION = OperationConfig(
    name="get",
    uri=ITEM_ENDPOINT,
    http_method="GET",
    query_spec={
        "item": {
            "required": True,
            "subspec": {
                "interval": {
                    "required": False,
                },
                "function": {
                    "required": False,
                },
                "start_time": {
                    "required": False,
                },
                "end_time": {
                    "required": False,
                },
            },
        },
        "names": {
            "required": True,
        },
    },
)


def create_module_argument_spec() -> dict:
    module_args = connection_params_argument_spec()
    module_args["item"] = {
        "type": "dict",
        "required": True,
        "options": {
            "interval": {
                "type": "str",
                "choices": ["MINUTES30", "HOURS2", "MINUTES5", "DAY1", "HOURS6"],
                "required": True,
            },
            "function": {
                "type": "str",
                "choices": ["COUNT", "MAX", "AVG", "MIN"],
                "required": True,
            },
            "start_time": {
                "type": "str",
                "required": True,
            },
            "end_time": {
                "type": "str",
                "required": True,
            },
        },
    }
    module_args["names"] = {
        "type": "list",
        "required": True,
        "aliases": ["filter_names"],
        "elements": "str",
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
    )
    try:
        result = info_module.get_resource_info()
    except VmwareModuleError as e:
        module.fail_json(**e.to_module_fail_json_output())
    module.exit_json(**result)


if __name__ == "__main__":
    main()
