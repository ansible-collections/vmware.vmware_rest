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
module: appliance_monitoring_query
short_description: Get monitoring data from the vCenter appliance.
description:
  - Queries the vCenter Server appliance monitoring backend for aggregated metric data.
  - Returns time-series values for one or more monitored items within the specified UTC time range.
author:
  - Ansible Eco Content Team (@eco-ansible-content)
extends_documentation_fragment:
  - vmware.vmware_rest.connection_params
options:
  names:
    description:
      - Monitored item identifiers to query, for example C(CPU) or C(MEMORY).
      - Each element must be an identifier (MOID) for a C(com.vmware.appliance.monitoring) resource.
    type: list
    elements: str
    required: true
  interval:
    description:
      - Aggregation interval between returned values.
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
      - Aggregation function applied to values within each interval.
    type: str
    required: true
    choices:
      - COUNT
      - MAX
      - AVG
      - MIN
  start_time:
    description:
      - Start of the query range in UTC.
    type: str
    required: true
  end_time:
    description:
      - End of the query range in UTC.
    type: str
    required: true
version_added: 4.11.0
requirements: []
notes:
  - Generated from vSphere API spec 9.1.0.
  - Has support for vSphere API 7.0.3.
  - Has support for vSphere API 8.0.2.
"""

EXAMPLES = r"""
- name: Query the monitoring backend for memory usage
  vmware.vmware_rest.appliance_monitoring_query:
    end_time: "2024-10-31T00:00:00.000Z"
    start_time: "2024-10-30T00:00:00.000Z"
    names:
      - mem.total
    interval: MINUTES5
    function: AVG
  register: monitoring_query_result
"""

RETURN = r"""
value:
  description:
    - List of monitored item data matching the query parameters.
  returned: On success
  type: list
  elements: dict
  contains:
    name:
      description:
        - Monitored item identifier (MOID) for the returned data series.
      returned: On success
      type: str
      sample: mem.total
    interval:
      description:
        - Aggregation interval used for the returned data.
      returned: On success
      type: str
      sample: MINUTES5
    function:
      description:
        - Aggregation function used for the returned data.
      returned: On success
      type: str
      sample: AVG
    start_time:
      description:
        - Start time of the query range in UTC.
      returned: On success
      type: str
      sample: "2024-10-30T00:00:00.000Z"
    end_time:
      description:
        - End time of the query range in UTC.
      returned: On success
      type: str
      sample: "2024-10-31T00:00:00.000Z"
    data:
      description:
        - Aggregated values for each interval in the requested time range.
      returned: On success
      type: list
      elements: str
      sample:
        - "1024"
        - "2048"
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.vmware.vmware_rest.plugins.module_utils._argument_spec import (
    connection_params_argument_spec,
)
from ansible_collections.vmware.vmware_rest.plugins.module_utils._module_base import (
    VmwareRestModuleBase,
    normalize_list_response,
)

MONITORING_QUERY_PATH = "/appliance/monitoring/query"


class VmwareRestQueryModule(VmwareRestModuleBase):
    PAYLOAD_FORMAT = {
        "get": {
            "query": {
                "names": "names",
                "interval": "interval",
                "function": "function",
                "start_time": "start_time",
                "end_time": "end_time",
            },
            "body": {},
            "path": {},
        },
    }

    def query(self):
        query = self.build_query(self.PAYLOAD_FORMAT["get"])
        response = self.client.get(MONITORING_QUERY_PATH, query=query)
        if response.status == 404:
            return []
        return normalize_list_response(response.json)


def main():
    module_args = connection_params_argument_spec()
    module_args["names"] = {
        "type": "list",
        "elements": "str",
        "required": True,
    }
    module_args["interval"] = {
        "type": "str",
        "required": True,
        "choices": ["MINUTES30", "HOURS2", "MINUTES5", "DAY1", "HOURS6"],
    }
    module_args["function"] = {
        "type": "str",
        "required": True,
        "choices": ["COUNT", "MAX", "AVG", "MIN"],
    }
    module_args["start_time"] = {"type": "str", "required": True}
    module_args["end_time"] = {"type": "str", "required": True}

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
    )

    query_module = VmwareRestQueryModule(module)
    result = query_module.query()
    module.exit_json(value=result)


if __name__ == "__main__":
    main()
