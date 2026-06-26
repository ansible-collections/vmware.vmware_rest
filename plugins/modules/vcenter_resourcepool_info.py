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
short_description: Retrieve information about vCenter resource pools
description:
  - Returns information about resource pools in vCenter.
  - Returns at most 1000 visible resource pools matching the filter criteria.

author:
  - Ansible Eco Content Team (@eco-ansible-content)

extends_documentation_fragment:
  - vmware.vmware_rest.connection_params

options:
  resource_pools:
    description:
      - Identifiers of resource pools that can match the filter.
      - Each element must be an identifier (MOID) for a C(ResourcePool) resource.
      - If omitted, resource pools with any identifier match the filter.
    type: list
    elements: str
    required: false
  names:
    description:
      - Names that resource pools must have to match the filter.
      - If omitted, resource pools with any name match the filter.
    type: list
    elements: str
    required: false
  parent_resource_pools:
    description:
      - Resource pools that must contain the resource pool for it to match the filter.
      - Each element must be an identifier (MOID) for a C(ResourcePool) resource.
      - If omitted, resource pools in any parent resource pool match the filter.
    type: list
    elements: str
    required: false
  datacenters:
    description:
      - Datacenters that must contain the resource pool for it to match the filter.
      - Each element must be an identifier (MOID) for a C(Datacenter) resource.
      - If omitted, resource pools in any datacenter match the filter.
    type: list
    elements: str
    required: false
  hosts:
    description:
      - Hosts that must contain the resource pool for it to match the filter.
      - Each element must be an identifier (MOID) for a C(HostSystem) resource.
      - If omitted, resource pools in any host match the filter.
    type: list
    elements: str
    required: false
  clusters:
    description:
      - Clusters that must contain the resource pool for it to match the filter.
      - Each element must be an identifier (MOID) for a C(ClusterComputeResource) resource.
      - If omitted, resource pools in any cluster match the filter.
    type: list
    elements: str
    required: false

version_added: "5.0.0"
requirements: []

notes:
  - Generated from vSphere API spec 9.1.0.
"""

EXAMPLES = r"""
- name: Get all resource pools
  vmware.vmware_rest.vcenter_resourcepool_info:
    vcenter_hostname: "vcenter.example.com"
    vcenter_username: "administrator@vsphere.local"
    vcenter_password: "password"
  register: all_resource_pools

- name: Get resource pools by name
  vmware.vmware_rest.vcenter_resourcepool_info:
    vcenter_hostname: "vcenter.example.com"
    vcenter_username: "administrator@vsphere.local"
    vcenter_password: "password"
    names:
      - "Production"
      - "Development"
  register: named_resource_pools

- name: Get resource pools in specific cluster
  vmware.vmware_rest.vcenter_resourcepool_info:
    vcenter_hostname: "vcenter.example.com"
    vcenter_username: "administrator@vsphere.local"
    vcenter_password: "password"
    clusters:
      - "domain-c1234"
  register: cluster_resource_pools
"""

RETURN = r"""
value:
  description:
    - List of resource pools matching the filter criteria.
    - Each entry contains summary and detailed information about a resource pool.
  returned: On success
  type: list
  elements: dict
  sample:
    - resource_pool: "resgroup-123"
      name: "Production"
      cpu_allocation:
        reservation: 0
        expandable_reservation: true
        limit: -1
        shares:
          level: "NORMAL"
      memory_allocation:
        reservation: 0
        expandable_reservation: true
        limit: -1
        shares:
          level: "NORMAL"
      resource_pools: []
"""


from ansible.module_utils.basic import AnsibleModule
from ansible_collections.vmware.vmware_rest.plugins.module_utils._argument_spec import (
    connection_params_argument_spec,
)
from ansible_collections.vmware.vmware_rest.plugins.module_utils._module_base import (
    VmwareRestInfoModuleBase,
)


class VmwareRestInfoModule(VmwareRestInfoModuleBase):
    PAYLOAD_FORMAT = {
        "get": {
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
        }
    }

    def get_info(self):
        """
        Get information about resource pools matching the filter criteria.

        Returns a list of resource pools with their detailed information.
        """
        result = []
        query = self.build_query(self.PAYLOAD_FORMAT["get"])

        list_response = self.client.get(
            path="/vcenter/resource-pool",
            query=query,
        )

        if list_response.status == 404:
            return {"value": result}

        summaries = list_response.json if isinstance(list_response.json, list) else list_response.json.get("value", [])

        for summary in summaries:
            resource_pool_id = summary.get("resource_pool")
            if not resource_pool_id:
                continue

            detail_response = self.client.get(
                path=f"/vcenter/resource-pool/{resource_pool_id}",
            )

            if detail_response.status == 200:
                resource_json = detail_response.json
                resource_json["resource_pool"] = resource_pool_id
                result.append(resource_json)

        return {"value": result}


def main():
    module_args = connection_params_argument_spec()

    module_args["resource_pools"] = {
        "type": "list",
        "elements": "str",
        "required": False,
    }
    module_args["names"] = {
        "type": "list",
        "elements": "str",
        "required": False,
    }
    module_args["parent_resource_pools"] = {
        "type": "list",
        "elements": "str",
        "required": False,
    }
    module_args["datacenters"] = {
        "type": "list",
        "elements": "str",
        "required": False,
    }
    module_args["hosts"] = {
        "type": "list",
        "elements": "str",
        "required": False,
    }
    module_args["clusters"] = {
        "type": "list",
        "elements": "str",
        "required": False,
    }

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
    )

    info_module = VmwareRestInfoModule(module)
    result = info_module.get_info()
    module.exit_json(**result)


if __name__ == "__main__":
    main()
