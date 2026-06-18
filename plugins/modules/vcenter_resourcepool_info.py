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
short_description: Get information about vCenter resource pools.
description:
  - Returns information about resource pools in vCenter Server.
  - When I(resource_pool) is specified, returns information for that resource pool only.
  - When I(resource_pool) is omitted, lists resource pools matching the optional filters and
    returns detailed information for each match.
author:
  - Ansible Eco Content Team (@eco-ansible-content)
extends_documentation_fragment:
  - vmware.vmware_rest.connection_params
options:
  resource_pool:
    description:
      - Identifier of the resource pool to retrieve.
      - Must be an identifier (MOID) for a C(ResourcePool) resource.
      - When specified, only that resource pool is returned.
    type: str
  resource_pools:
    description:
      - Identifiers of resource pools that can match the filter.
      - Each element must be an identifier (MOID) for a C(ResourcePool) resource.
      - When omitted or empty, resource pools with any identifier match the filter.
    type: list
    elements: str
  names:
    description:
      - Names that resource pools must have to match the filter.
      - When omitted or empty, resource pools with any name match the filter.
    type: list
    elements: str
  parent_resource_pools:
    description:
      - Resource pools that must contain the resource pool for it to match the filter.
      - Each element must be an identifier (MOID) for a C(ResourcePool) resource.
      - When omitted or empty, resource pools in any parent resource pool match the filter.
    type: list
    elements: str
  datacenters:
    description:
      - Datacenters that must contain the resource pool for it to match the filter.
      - Each element must be an identifier (MOID) for a C(Datacenter) resource.
      - When omitted or empty, resource pools in any datacenter match the filter.
    type: list
    elements: str
  hosts:
    description:
      - Hosts that must contain the resource pool for it to match the filter.
      - Each element must be an identifier (MOID) for a C(HostSystem) resource.
      - When omitted or empty, resource pools on any host match the filter.
    type: list
    elements: str
  clusters:
    description:
      - Clusters that must contain the resource pool for it to match the filter.
      - Each element must be an identifier (MOID) for a C(ClusterComputeResource) resource.
      - When omitted or empty, resource pools in any cluster match the filter.
    type: list
    elements: str
version_added: 4.11.0
requirements: []
notes:
  - Generated from vSphere API spec 9.1.0.
  - Has support for vSphere API 7.0.3.
  - Has support for vSphere API 8.0.2.
"""

EXAMPLES = r"""
- name: List all resource pools
  vmware.vmware_rest.vcenter_resourcepool_info:
  register: resource_pools

- name: Get a resource pool by MOID
  vmware.vmware_rest.vcenter_resourcepool_info:
    resource_pool: resgroup-1009
  register: resource_pool_info

- name: List resource pools matching a name filter
  vmware.vmware_rest.vcenter_resourcepool_info:
    names:
      - my_resource_pool
  register: filtered_resource_pools
"""

RETURN = r"""
value:
  description:
    - Resource pool information.
    - Returns a list of resource pool dictionaries when I(resource_pool) is omitted.
    - Returns a single resource pool dictionary when I(resource_pool) is specified.
  returned: On success
  type: raw
  sample:
    - name: my_resource_pool
      resource_pool: resgroup-1009
      resource_pools: []
      cpu_allocation:
        expandable_reservation: true
        limit: -1
        reservation: 0
        shares:
          level: NORMAL
      memory_allocation:
        expandable_reservation: true
        limit: -1
        reservation: 0
        shares:
          level: NORMAL
  contains:
    resource_pool:
      description:
        - Identifier of the resource pool.
        - Must be an identifier (MOID) for a C(ResourcePool) resource.
      type: str
      sample: resgroup-1009
    name:
      description:
        - Name of the resource pool.
      type: str
      sample: my_resource_pool
    resource_pools:
      description:
        - Identifiers of child resource pools contained in this resource pool.
        - Each element must be an identifier (MOID) for a C(ResourcePool) resource.
      type: list
      elements: str
    cpu_allocation:
      description:
        - Resource allocation information for CPU.
      type: dict
      contains:
        reservation:
          description:
            - Guaranteed CPU reservation in MHz.
          type: int
        expandable_reservation:
          description:
            - Whether the reservation can grow beyond the specified value.
          type: bool
        limit:
          description:
            - Maximum CPU utilization limit in MHz, or C(-1) for no fixed limit.
          type: int
        shares:
          description:
            - CPU share allocation settings.
          type: dict
          contains:
            level:
              description:
                - Share allocation level.
              type: str
              choices:
                - LOW
                - NORMAL
                - HIGH
                - CUSTOM
            shares:
              description:
                - Custom share value when I(level=CUSTOM).
              type: int
    memory_allocation:
      description:
        - Resource allocation information for memory.
      type: dict
      contains:
        reservation:
          description:
            - Guaranteed memory reservation in MB.
          type: int
        expandable_reservation:
          description:
            - Whether the reservation can grow beyond the specified value.
          type: bool
        limit:
          description:
            - Maximum memory utilization limit in MB, or C(-1) for no fixed limit.
          type: int
        shares:
          description:
            - Memory share allocation settings.
          type: dict
          contains:
            level:
              description:
                - Share allocation level.
              type: str
              choices:
                - LOW
                - NORMAL
                - HIGH
                - CUSTOM
            shares:
              description:
                - Custom share value when I(level=CUSTOM).
              type: int
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.vmware.vmware_rest.plugins.module_utils._argument_spec import (
    connection_params_argument_spec,
)
from ansible_collections.vmware.vmware_rest.plugins.module_utils._errors import (
    UnexpectedAPIResponse,
)
from ansible_collections.vmware.vmware_rest.plugins.module_utils._module_base import (
    VmwareRestInfoModuleBase,
    normalize_list_response,
)

LIST_PATH = "/vcenter/resource-pool"
RESOURCE_POOL_PATH = "/vcenter/resource-pool/{resource_pool}"


class VmwareRestInfoModule(VmwareRestInfoModuleBase):
    PAYLOAD_FORMAT = {
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
        "get": {
            "query": {},
            "body": {},
            "path": {"resourcePool": "resource_pool"},
        },
    }

    def _get_resource_pool(self, resource_pool, fail_if_missing=False):
        path = self.build_path(RESOURCE_POOL_PATH, {"resource_pool": resource_pool})
        response = self.client.get(path)
        if response.status == 404:
            if fail_if_missing:
                self.client.error_handler.handle_request_error(
                    exception=UnexpectedAPIResponse(response.status, response.data),
                    method="GET",
                    path=path,
                    request_kwargs={},
                )
            return None

        info = response.json
        info["resource_pool"] = resource_pool
        return info

    def get_info(self):
        resource_pool = self.params.get("resource_pool")
        if resource_pool:
            return self._get_resource_pool(resource_pool, fail_if_missing=True)

        query = self.build_query(self.PAYLOAD_FORMAT["list"])
        response = self.client.get(LIST_PATH, query=query or None)
        if response.status == 404:
            return []

        summaries = normalize_list_response(response.json)
        result = []
        for summary in summaries:
            resource_pool_id = summary.get("resource_pool")
            if not resource_pool_id:
                continue
            info = self._get_resource_pool(resource_pool_id)
            if info is not None:
                result.append(info)
        return result


def main():
    module_args = connection_params_argument_spec()
    module_args["resource_pool"] = {"type": "str"}
    module_args["resource_pools"] = {"type": "list", "elements": "str"}
    module_args["names"] = {"type": "list", "elements": "str"}
    module_args["parent_resource_pools"] = {"type": "list", "elements": "str"}
    module_args["datacenters"] = {"type": "list", "elements": "str"}
    module_args["hosts"] = {"type": "list", "elements": "str"}
    module_args["clusters"] = {"type": "list", "elements": "str"}

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
    )

    info_module = VmwareRestInfoModule(module)
    result = info_module.get_info()
    module.exit_json(value=result)


if __name__ == "__main__":
    main()
