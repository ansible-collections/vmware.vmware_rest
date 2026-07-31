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
module: vcenter_resourcepool_info
short_description: Gather information about vCenter resource pools.
description:
  - Retrieve information about one or more VMware vCenter resource pools.
  - Can return a list of all resource pools or detailed information about a specific
    resource pool identified by its MOID.
  - Use the filter parameters to narrow results by resource pool name, parent resource pool,
    datacenter, host, or cluster.

author:
  - Ansible Eco Content Team (@eco-ansible-content)

extends_documentation_fragment:
  - vmware.vmware_rest.connection_params

options:
  resource_pool:
    description:
      - Identifier of the resource pool to retrieve details for.
      - Must be an identifier (MOID) for a C(ResourcePool) resource.
    type: str
    required: false
  resource_pools:
    description:
      - A list of resource pool MOIDs to filter the results.
      - Only resource pools whose identifiers appear in this list will be returned.
      - If omitted or empty, resource pools with any identifier are returned.
    type: list
    required: false
    elements: str
  names:
    aliases:
      - filter_names
    description:
      - A list of resource pool names to filter the results.
      - Only resource pools whose names appear in this list will be returned.
      - If omitted or empty, resource pools with any name are returned.
    type: list
    required: false
    elements: str
  parent_resource_pools:
    description:
      - A list of parent resource pool MOIDs to filter the results.
      - Only resource pools that are children of the specified parent pools will be returned.
      - If omitted or empty, resource pools under any parent are returned.
    type: list
    required: false
    elements: str
  datacenters:
    aliases:
      - filter_datacenters
    description:
      - A list of datacenter MOIDs to filter the results.
      - Only resource pools that reside in the specified datacenters will be returned.
      - If omitted or empty, resource pools in any datacenter are returned.
    type: list
    required: false
    elements: str
  hosts:
    description:
      - A list of host MOIDs to filter the results.
      - Only resource pools that belong to the specified hosts will be returned.
      - If omitted or empty, resource pools on any host are returned.
    type: list
    required: false
    elements: str
  clusters:
    description:
      - A list of cluster MOIDs to filter the results.
      - Only resource pools that belong to the specified clusters will be returned.
      - If omitted or empty, resource pools in any cluster are returned.
    type: list
    required: false
    elements: str

version_added: 5.0.0

requirements: []

notes:
  - Generated from vSphere API spec 9.1.0.
"""

EXAMPLES = r"""
- name: List all resource pools
  vmware.vmware_rest.vcenter_resourcepool_info:
  register: all_resource_pools

- name: Get details about a specific resource pool
  vmware.vmware_rest.vcenter_resourcepool_info:
    resource_pool: resgroup-1009
  register: my_resource_pool

- name: Filter resource pools by name
  vmware.vmware_rest.vcenter_resourcepool_info:
    names:
      - my_resource_pool
  register: filtered_pools

- name: Filter resource pools by cluster
  vmware.vmware_rest.vcenter_resourcepool_info:
    clusters:
      - domain-c1007
  register: cluster_pools
"""

RETURN = r"""
id:
  description: MOID of the queried resource pool.
  returned: When only one resource, with a MOID, was queried.
  sample: resgroup-1009
  type: str
value:
  description:
    - Raw output from the API response.
    - This output is maintained for consistency with version 4.x and earlier of this collection.
      It is recommended to switch to the info return key for a more consistent and documented output.
  returned: On success.
  sample:
    name: my_resource_pool
    cpu_allocation:
      reservation: 0
      expandable_reservation: true
      limit: -1
      shares:
        level: NORMAL
        shares: 4000
    memory_allocation:
      reservation: 0
      expandable_reservation: true
      limit: -1
      shares:
        level: NORMAL
        shares: 163840
    resource_pools: []
  type: raw
info:
  description: A list of resource pools matching the query.
  returned: On success.
  sample:
    - resource_pool: resgroup-1009
      name: my_resource_pool
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

MOID_PARAMETER_HINTS = ["resource_pool"]

LIST_ENDPOINT = "/vcenter/resource-pool"
ITEM_ENDPOINT = "/vcenter/resource-pool/{resource_pool}"


LIST_OPERATION = OperationConfig(
    name="list",
    uri=LIST_ENDPOINT,
    http_method="GET",
    query_spec={
        "resource_pools": {
            "required": False,
        },
        "names": {
            "required": False,
        },
        "parent_resource_pools": {
            "required": False,
        },
        "datacenters": {
            "required": False,
        },
        "hosts": {
            "required": False,
        },
        "clusters": {
            "required": False,
        },
    },
)

GET_OPERATION = OperationConfig(
    name="get",
    uri=ITEM_ENDPOINT,
    http_method="GET",
)


def create_module_argument_spec() -> dict:
    module_args = connection_params_argument_spec()
    module_args["clusters"] = {
        "type": "list",
        "elements": "str",
    }
    module_args["datacenters"] = {
        "type": "list",
        "aliases": ["filter_datacenters"],
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
    module_args["parent_resource_pools"] = {
        "type": "list",
        "elements": "str",
    }
    module_args["resource_pool"] = {
        "type": "str",
    }
    module_args["resource_pools"] = {
        "type": "list",
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
        list_operation_config=LIST_OPERATION,
    )
    try:
        result = info_module.get_resource_info()
    except VmwareModuleError as e:
        module.fail_json(**e.to_module_fail_json_output())
    module.exit_json(**result)


if __name__ == "__main__":
    main()
