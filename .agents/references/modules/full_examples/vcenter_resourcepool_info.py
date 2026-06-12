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
module: vcenter_resourcepool_info
short_description: Retrieves information about resource pools in vCenter.
description:
  - Retrieves information about resource pools in vCenter.
  - When I(resource_pool) is set, returns information about that resource pool.
  - When I(resource_pool) is not set, lists resource pools matching the filter options
    and returns detailed information for each match.
author:
  - Ansible Eco Content Team (@eco-ansible-content)
extends_documentation_fragment:
  - vmware.vmware_rest.connection_params
options:
  resource_pool:
    description:
      - Identifier of the resource pool to retrieve.
      - Must be an identifier (MOID) for a C(ResourcePool) resource.
    type: str
  resource_pools:
    description:
      - Identifiers of resource pools that can match the filter.
      - If not set, resource pools with any identifier match the filter.
      - Each element must be an identifier (MOID) for a C(ResourcePool) resource.
    type: list
    elements: str
    aliases:
      - filter_resource_pools
  names:
    description:
      - Names that resource pools must have to match the filter.
      - If not set, resource pools with any name match the filter.
    type: list
    elements: str
    aliases:
      - filter_names
  parent_resource_pools:
    description:
      - Resource pools that must contain the resource pool for it to match the filter.
      - If not set, resource pools in any parent resource pool match the filter.
      - Each element must be an identifier (MOID) for a C(ResourcePool) resource.
    type: list
    elements: str
    aliases:
      - filter_parent_resource_pools
  datacenters:
    description:
      - Datacenters that must contain the resource pool for it to match the filter.
      - If not set, resource pools in any datacenter match the filter.
      - Each element must be an identifier (MOID) for a C(Datacenter) resource.
    type: list
    elements: str
    aliases:
      - filter_datacenters
  hosts:
    description:
      - Hosts that must contain the resource pool for it to match the filter.
      - If not set, resource pools on any host match the filter.
      - Each element must be an identifier (MOID) for a C(HostSystem) resource.
    type: list
    elements: str
    aliases:
      - filter_hosts
  clusters:
    description:
      - Clusters that must contain the resource pool for it to match the filter.
      - If not set, resource pools in any cluster match the filter.
      - Each element must be an identifier (MOID) for a C(ClusterComputeResource) resource.
    type: list
    elements: str
    aliases:
      - filter_clusters
version_added: 4.11.0
requirements: []
notes:
  - Generated from vSphere API spec 9.1.0.
"""

EXAMPLES = r"""
- name: List all resource pools
  vmware.vmware_rest.vcenter_resourcepool_info:
  register: resource_pools

- name: Get a specific resource pool
  vmware.vmware_rest.vcenter_resourcepool_info:
    resource_pool: resgroup-1009
  register: resource_pool_info

- name: List resource pools by name
  vmware.vmware_rest.vcenter_resourcepool_info:
    names:
      - my_resource_pool
  register: named_pools
"""

RETURN = r"""
value:
  description:
    - List of resource pool information objects.
  returned: On success
  type: list
  elements: dict
  sample:
    - id: resgroup-1009
      name: my_resource_pool
      resource_pools: []
      cpu_allocation:
        reservation: 1000
        expandable_reservation: true
        limit: 4000
        shares:
          level: NORMAL
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.vmware.vmware_rest.plugins.module_utils._argument_spec import (
    connection_params_argument_spec,
)
from ansible_collections.vmware.vmware_rest.plugins.module_utils._module_base import (
    VmwareRestInfoModuleBase,
)

LIST_PATH = "/vcenter/resource-pool"
ITEM_PATH = "/vcenter/resource-pool/{resource_pool}"


class VmwareRestInfoModule(VmwareRestInfoModuleBase):
    PAYLOAD_FORMAT = {
        "get": {"query": {}, "body": {}, "path": {"resource_pool": "resource_pool"}},
        "list": {
            "query": {
                "resource_pools": "resource_pools",
                "names": "names",
                "parent_resource_pools": "parent_resource_pools",
                "datacenters": "datacenters",
                "hosts": "hosts",
                "clusters": "clusters",
            },
            "body": {},
            "path": {},
        },
    }

    def get_info(self):
        if self.params.get("resource_pool"):
            return [self._get_resource_pool(self.params["resource_pool"])]

        summaries = self._list_resource_pools()
        result = []
        for summary in summaries:
            resource_pool_id = summary["resource_pool"]
            info = self._get_resource_pool(resource_pool_id)
            result.append(info)
        return result

    def _list_resource_pools(self):
        return self.fetch_list(LIST_PATH, self.PAYLOAD_FORMAT["list"])

    def _get_resource_pool(self, resource_pool_id):
        path = self.build_path(ITEM_PATH, {"resource_pool": resource_pool_id})
        response = self.client.get(path)
        if response.status == 404:
            return {}

        info = response.json
        if "id" not in info:
            info["id"] = resource_pool_id
        return info


def main():
    module_args = connection_params_argument_spec()
    module_args["resource_pool"] = {"type": "str"}
    module_args["resource_pools"] = {
        "type": "list",
        "elements": "str",
        "aliases": ["filter_resource_pools"],
    }
    module_args["names"] = {
        "type": "list",
        "elements": "str",
        "aliases": ["filter_names"],
    }
    module_args["parent_resource_pools"] = {
        "type": "list",
        "elements": "str",
        "aliases": ["filter_parent_resource_pools"],
    }
    module_args["datacenters"] = {
        "type": "list",
        "elements": "str",
        "aliases": ["filter_datacenters"],
    }
    module_args["hosts"] = {
        "type": "list",
        "elements": "str",
        "aliases": ["filter_hosts"],
    }
    module_args["clusters"] = {
        "type": "list",
        "elements": "str",
        "aliases": ["filter_clusters"],
    }

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
    )

    info_module = VmwareRestInfoModule(module)
    result = info_module.get_info()
    module.exit_json(value=result)


if __name__ == "__main__":
    main()
