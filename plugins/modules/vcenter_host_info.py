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
module: vcenter_host_info
short_description: Gather information about vCenter ESXi hosts.
description:
  - Retrieve information about one or more VMware vCenter ESXi hosts.
  - Returns the hosts that match the supplied filters, or all hosts when no filter is given.
  - Use the filter parameters to narrow results by host name, identifier, connection state,
    cluster, folder, or datacenter.

deprecated:
  removed_in: 6.0.0
  why: Functionality is duplicated in other supported modules.
  alternative: Use M(vmware.vmware.esxi_info) instead.

author:
  - Ansible Eco Content Team (@eco-ansible-content)

extends_documentation_fragment:
  - vmware.vmware_rest.connection_params

options:
  filter:
    description:
      - A specification used to filter the hosts that are returned.
      - If omitted, all hosts match the filter.
    type: dict
    required: false
    suboptions:
      standalone:
        description:
          - When C(true), only hosts that are not part of a cluster are returned.
          - When C(false), only hosts that are part of a cluster are returned.
          - If omitted, hosts are returned regardless of cluster membership.
          - If set to C(true) while I(clusters) is also specified, no hosts will match the filter.
        type: bool
        required: false
  hosts:
    description:
      - A list of host MOIDs to filter the results.
      - Only hosts whose identifiers appear in this list will be returned.
      - If omitted or empty, hosts with any identifier are returned.
    type: list
    required: false
    elements: str
  names:
    aliases:
      - filter_names
    description:
      - A list of host names to filter the results.
      - Only hosts whose names appear in this list will be returned.
      - If omitted or empty, hosts with any name are returned.
    type: list
    required: false
    elements: str
  folders:
    aliases:
      - filter_folders
    description:
      - A list of folder MOIDs to filter the results.
      - Only hosts that reside in the specified folders will be returned.
      - If omitted or empty, hosts in any folder are returned.
    type: list
    required: false
    elements: str
  datacenters:
    aliases:
      - filter_datacenters
    description:
      - A list of datacenter MOIDs to filter the results.
      - Only hosts that reside in the specified datacenters will be returned.
      - If omitted or empty, hosts in any datacenter are returned.
    type: list
    required: false
    elements: str
  clusters:
    description:
      - A list of cluster MOIDs to filter the results.
      - Only hosts that belong to the specified clusters will be returned.
      - If omitted or empty, hosts in any cluster and hosts that are not in a cluster are returned.
      - If this list is not empty while I(filter.standalone) is C(true), no hosts will match the filter.
    type: list
    required: false
    elements: str
  connection_states:
    description:
      - A list of connection states to filter the results.
      - Only hosts that are in one of the listed connection states will be returned.
      - CONNECTED - Host is connected to the vCenter Server.
      - DISCONNECTED - Host is disconnected from the vCenter Server.
      - NOT_RESPONDING - vCenter Server is not receiving heartbeats from the host. The state
        automatically changes to connected once heartbeats are received again.
      - If omitted or empty, hosts in any connection state are returned.
    type: list
    required: false
    elements: str
  host_uuids:
    description:
      - A list of host UUIDs to filter the results.
      - The UUID maps to "UUID" in SMBIOS System Information (Type 1) at offset 08h.
      - This property was added in vSphere API 9.0.0.0.
      - If omitted or empty, hosts with any UUID are returned.
    type: list
    required: false
    elements: str

version_added: 5.0.0

requirements: []

notes:
  - Generated from vSphere API spec 9.1.0.
"""

EXAMPLES = r"""
- name: List all hosts
  vmware.vmware_rest.vcenter_host_info:
  register: all_hosts

- name: Filter hosts by name
  vmware.vmware_rest.vcenter_host_info:
    names:
      - esxi01.example.com
  register: filtered_hosts

- name: List connected standalone hosts
  vmware.vmware_rest.vcenter_host_info:
    filter:
      standalone: true
    connection_states:
      - CONNECTED
  register: standalone_hosts

- name: List hosts in a specific cluster
  vmware.vmware_rest.vcenter_host_info:
    clusters:
      - domain-c1001
  register: cluster_hosts
"""

RETURN = r"""
id:
  description: MOID of the queried host.
  returned: When only one resource, with a MOID, was queried.
  sample: host-1001
  type: str
value:
  description:
    - Raw output from the API response.
    - This output is maintained for consistency with version 4.x and earlier of this collection.
      It is recommended to switch to the info return key for a more consistent and documented output.
  returned: On success.
  sample:
    host: host-1001
    name: esxi01.example.com
    connection_state: CONNECTED
    power_state: POWERED_ON
  type: raw
info:
  description: A list of hosts matching the query.
  returned: On success.
  sample:
    - host: host-1001
      name: esxi01.example.com
      connection_state: CONNECTED
      power_state: POWERED_ON
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
ITEM_ENDPOINT = "/vcenter/host"


GET_OPERATION = OperationConfig(
    name="get",
    uri=ITEM_ENDPOINT,
    http_method="GET",
    query_spec={
        "filter": {
            "required": False,
            "subspec": {
                "standalone": {
                    "required": False,
                },
            },
        },
        "hosts": {
            "required": False,
        },
        "names": {
            "required": False,
        },
        "folders": {
            "required": False,
        },
        "datacenters": {
            "required": False,
        },
        "clusters": {
            "required": False,
        },
        "connection_states": {
            "required": False,
        },
        "host_uuids": {
            "required": False,
        },
    },
)


def create_module_argument_spec() -> dict:
    module_args = connection_params_argument_spec()
    module_args["clusters"] = {
        "type": "list",
        "elements": "str",
    }
    module_args["connection_states"] = {
        "type": "list",
        "elements": "str",
    }
    module_args["datacenters"] = {
        "type": "list",
        "aliases": ["filter_datacenters"],
        "elements": "str",
    }
    module_args["filter"] = {
        "type": "dict",
        "options": {
            "standalone": {
                "type": "bool",
            },
        },
    }
    module_args["folders"] = {
        "type": "list",
        "aliases": ["filter_folders"],
        "elements": "str",
    }
    module_args["host_uuids"] = {
        "type": "list",
        "elements": "str",
    }
    module_args["hosts"] = {
        "type": "list",
        "elements": "str",
    }
    module_args["names"] = {
        "type": "list",
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
