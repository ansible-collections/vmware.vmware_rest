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
module: vcenter_resourcepool
short_description: Manages vCenter resource pools.
description:
  - Creates, updates, or deletes resource pools in vCenter.
  - Use I(state=present) to ensure a resource pool exists and matches the desired
    configuration.
  - Use I(state=absent) to delete a resource pool.
author:
  - Ansible Eco Content Team (@eco-ansible-content)
extends_documentation_fragment:
  - vmware.vmware_rest.connection_params
options:
  state:
    description:
      - The desired state of the resource pool.
      - Use C(present) to create or update the resource pool.
      - Use C(absent) to delete the resource pool.
    type: str
    choices:
      - present
      - absent
    default: present
  resource_pool:
    description:
      - Identifier of the resource pool to update or delete.
      - Must be an identifier (MOID) for a C(ResourcePool) resource.
      - When not set, I(name) is used to locate the resource pool.
    type: str
  name:
    description:
      - Name of the resource pool.
      - Required when creating a resource pool.
      - When I(state=absent), can be used to locate the resource pool when
        I(resource_pool) is not set.
    type: str
  parent:
    description:
      - Parent resource pool in which the new resource pool should be created.
      - Must be an identifier (MOID) for a C(ResourcePool) resource.
      - Required when creating a resource pool.
    type: str
  cpu_allocation:
    description:
      - CPU resource allocation settings for the resource pool.
    type: dict
    suboptions:
      reservation:
        description:
          - Amount of CPU guaranteed available to the resource pool, in MHz.
        type: int
      expandable_reservation:
        description:
          - Whether the reservation can grow beyond the specified value when the
            parent resource pool has unreserved resources.
        type: bool
      limit:
        description:
          - Maximum CPU utilization for the resource pool, in MHz.
          - Use C(-1) for no fixed limit.
        type: int
      shares:
        description:
          - CPU shares used when there is resource contention.
        type: dict
        suboptions:
          level:
            description:
              - Predefined allocation level for shares.
            type: str
            choices:
              - LOW
              - NORMAL
              - HIGH
              - CUSTOM
          shares:
            description:
              - Number of shares when I(level) is C(CUSTOM).
            type: int
  memory_allocation:
    description:
      - Memory resource allocation settings for the resource pool.
    type: dict
    suboptions:
      reservation:
        description:
          - Amount of memory guaranteed available to the resource pool, in MB.
        type: int
      expandable_reservation:
        description:
          - Whether the reservation can grow beyond the specified value when the
            parent resource pool has unreserved resources.
        type: bool
      limit:
        description:
          - Maximum memory utilization for the resource pool, in MB.
          - Use C(-1) for no fixed limit.
        type: int
      shares:
        description:
          - Memory shares used when there is resource contention.
        type: dict
        suboptions:
          level:
            description:
              - Predefined allocation level for shares.
            type: str
            choices:
              - LOW
              - NORMAL
              - HIGH
              - CUSTOM
          shares:
            description:
              - Number of shares when I(level) is C(CUSTOM).
            type: int
version_added: 4.11.0
requirements: []
notes:
  - Generated from vSphere API spec 9.1.0.
  - Has support for vSphere API 7.0.3.
  - Has support for vSphere API 8.0.2.
"""

EXAMPLES = r"""
- name: Create a resource pool
  vmware.vmware_rest.vcenter_resourcepool:
    name: my_resource_pool
    parent: resgroup-47

- name: Create a resource pool with CPU and memory allocation
  vmware.vmware_rest.vcenter_resourcepool:
    name: my_resource_pool
    parent: resgroup-47
    cpu_allocation:
      reservation: 1000
      limit: 4000
      shares:
        level: NORMAL
    memory_allocation:
      reservation: 1024
      expandable_reservation: true

- name: Update a resource pool by MOID
  vmware.vmware_rest.vcenter_resourcepool:
    resource_pool: resgroup-1009
    name: renamed_resource_pool

- name: Delete a resource pool by name
  vmware.vmware_rest.vcenter_resourcepool:
    state: absent
    name: my_resource_pool
"""

RETURN = r"""
id:
  description:
    - The MOID of the resource pool.
  returned: On success when I(state=present)
  type: str
  sample: resgroup-1009

value:
  description:
    - Resource pool information after update, or the MOID after create.
  returned: On success when I(state=present) and the resource pool was created or updated
  type: raw
  sample:
    name: my_resource_pool
    resource_pools: []
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.vmware.vmware_rest.plugins.module_utils._argument_spec import (
    connection_params_argument_spec,
)
from ansible_collections.vmware.vmware_rest.plugins.module_utils._module_base import (
    VmwareRestCrudModuleBase,
    find_summary_id,
    payload_body_subset,
)

LIST_PATH = "/vcenter/resource-pool"
ITEM_PATH = "/vcenter/resource-pool/{resource_pool}"

_CREATE_BODY = {
    "name": "name",
    "parent": "parent",
    "cpu_allocation": "cpu_allocation",
    "memory_allocation": "memory_allocation",
}

_ALLOCATION_ARG_SPEC = {
    "type": "dict",
    "options": {
        "reservation": {"type": "int"},
        "expandable_reservation": {"type": "bool"},
        "limit": {"type": "int"},
        "shares": {
            "type": "dict",
            "options": {
                "level": {
                    "type": "str",
                    "choices": ["LOW", "NORMAL", "HIGH", "CUSTOM"],
                },
                "shares": {"type": "int"},
            },
        },
    },
}


class VmwareRestCrudModule(VmwareRestCrudModuleBase):
    PAYLOAD_FORMAT = {
        "create": {
            "query": {},
            "body": _CREATE_BODY,
            "path": {},
        },
        "update": {
            "query": {},
            "body": payload_body_subset(_CREATE_BODY, exclude=("parent",)),
            "path": {},
        },
        "list": {
            "query": {"names": "name"},
            "body": {},
            "path": {},
        },
    }

    UPDATABLE_PARAMS = ("name", "cpu_allocation", "memory_allocation")

    def ensure_present(self):
        resource_pool = self.params.get("resource_pool")
        if resource_pool:
            return self._ensure_present_by_id(resource_pool)

        name = self.params.get("name")
        if not name:
            self.module.fail_json(
                msg="name is required when creating a resource pool"
            )

        found_id = self._find_by_name(name)
        if found_id:
            return self._ensure_present_by_id(found_id)

        return self._create()

    def ensure_absent(self):
        resource_pool = self.resolve_resource_id(
            "resource_pool",
            "name",
            self._find_by_name,
        )
        if not resource_pool:
            return {"changed": False}

        return self.delete_if_exists(
            ITEM_PATH,
            {"resource_pool": resource_pool},
        )

    def _create(self):
        parent = self.params.get("parent")
        if not parent:
            self.module.fail_json(
                msg="parent is required when creating a resource pool"
            )

        create_body = self.build_payload(self.PAYLOAD_FORMAT["create"])
        if not self.module.check_mode:
            response = self.client.post(LIST_PATH, data=create_body)
            resource_pool_id = response.json
        else:
            resource_pool_id = None
        return {
            "changed": True,
            "value": resource_pool_id,
            "id": resource_pool_id,
        }

    def _ensure_present_by_id(self, resource_pool):
        path = self.build_path(ITEM_PATH, {"resource_pool": resource_pool})
        response = self.client.get(path)
        if response.status == 404:
            self.module.fail_json(
                msg="Resource pool not found: {0}".format(resource_pool)
            )

        update_body = self.build_updatable_payload()
        if not update_body:
            return {"changed": False, "id": resource_pool}

        result = self.update_if_changed(path, response.json, update_body)
        result["id"] = resource_pool
        return result

    def _find_by_name(self, name):
        summaries = self.fetch_list(LIST_PATH, self.PAYLOAD_FORMAT["list"])
        return find_summary_id(summaries, name, id_key="resource_pool")


def main():
    module_args = connection_params_argument_spec()
    module_args["state"] = {
        "type": "str",
        "choices": ["present", "absent"],
        "default": "present",
    }
    module_args["resource_pool"] = {"type": "str"}
    module_args["name"] = {"type": "str"}
    module_args["parent"] = {"type": "str"}
    module_args["cpu_allocation"] = _ALLOCATION_ARG_SPEC
    module_args["memory_allocation"] = _ALLOCATION_ARG_SPEC

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
    )

    crud_module = VmwareRestCrudModule(module)

    if module.params["state"] == "present":
        result = crud_module.ensure_present()
    elif module.params["state"] == "absent":
        result = crud_module.ensure_absent()
    else:
        module.fail_json(
            msg="Unsupported state: {0}".format(module.params["state"])
        )

    module.exit_json(**result)


if __name__ == "__main__":
    main()
