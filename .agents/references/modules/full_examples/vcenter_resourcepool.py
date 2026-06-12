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
short_description: Creates, updates, or deletes a resource pool in vCenter.
description:
  - Manages resource pools in vCenter.
  - Use I(state=present) to create a resource pool or update an existing one.
  - Use I(state=absent) to delete a resource pool.
  - When updating, only parameters that differ from the current configuration are
    sent to the API.
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
  name:
    description:
      - Name of the resource pool.
      - Required when creating a resource pool.
      - When I(state=absent), can be used to locate the resource pool when I(resource_pool)
        is not set.
    type: str
  parent:
    description:
      - Parent of the resource pool.
      - Required when creating a resource pool.
      - Must be an identifier (MOID) for a C(ResourcePool) resource.
    type: str
  resource_pool:
    description:
      - Identifier of the resource pool to update or delete.
      - Must be an identifier (MOID) for a C(ResourcePool) resource.
      - When not set, I(name) is used to locate the resource pool.
    type: str
  cpu_allocation:
    description:
      - Resource allocation for CPU.
    type: dict
    suboptions:
      reservation:
        description:
          - Amount of CPU resource guaranteed to the resource pool, in MHz.
        type: int
      expandable_reservation:
        description:
          - Whether the reservation can grow beyond the specified value.
        type: bool
      limit:
        description:
          - Maximum CPU utilization of the resource pool, in MHz.
          - Use C(-1) for no fixed limit.
        type: int
      shares:
        description:
          - Shares used in case of CPU resource contention.
        type: dict
        suboptions:
          level:
            description:
              - Allocation level for shares.
            type: str
            choices:
              - LOW
              - NORMAL
              - HIGH
              - CUSTOM
          shares:
            description:
              - Number of shares when I(level=CUSTOM).
            type: int
  memory_allocation:
    description:
      - Resource allocation for memory.
    type: dict
    suboptions:
      reservation:
        description:
          - Amount of memory resource guaranteed to the resource pool, in MB.
        type: int
      expandable_reservation:
        description:
          - Whether the reservation can grow beyond the specified value.
        type: bool
      limit:
        description:
          - Maximum memory utilization of the resource pool, in MB.
          - Use C(-1) for no fixed limit.
        type: int
      shares:
        description:
          - Shares used in case of memory resource contention.
        type: dict
        suboptions:
          level:
            description:
              - Allocation level for shares.
            type: str
            choices:
              - LOW
              - NORMAL
              - HIGH
              - CUSTOM
          shares:
            description:
              - Number of shares when I(level=CUSTOM).
            type: int
version_added: 4.11.0
requirements: []
notes:
  - Generated from vSphere API spec 9.1.0.
"""

EXAMPLES = r"""
- name: Create a resource pool
  vmware.vmware_rest.vcenter_resourcepool:
    name: my_resource_pool
    parent: resgroup-8
    cpu_allocation:
      reservation: 1000
      limit: 4000
    memory_allocation:
      reservation: 1024
      limit: 4096

- name: Update a resource pool
  vmware.vmware_rest.vcenter_resourcepool:
    resource_pool: resgroup-1009
    cpu_allocation:
      limit: 8000

- name: Delete a resource pool
  vmware.vmware_rest.vcenter_resourcepool:
    state: absent
    resource_pool: resgroup-1009
"""

RETURN = r"""
value:
  description:
    - The resource pool MOID after create, or resource pool information after update.
  returned: On success when I(state=present)
  type: raw
  sample: resgroup-1009
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

SHARES_OPTIONS = {
    "level": {
        "type": "str",
        "choices": ["LOW", "NORMAL", "HIGH", "CUSTOM"],
    },
    "shares": {"type": "int"},
}

ALLOCATION_OPTIONS = {
    "reservation": {"type": "int"},
    "expandable_reservation": {"type": "bool"},
    "limit": {"type": "int"},
    "shares": {"type": "dict", "options": SHARES_OPTIONS},
}

_RESOURCE_POOL_BODY = {
    "name": "name",
    "parent": "parent",
    "cpu_allocation": "cpu_allocation",
    "memory_allocation": "memory_allocation",
}


class VmwareRestCrudModule(VmwareRestCrudModuleBase):
    PAYLOAD_FORMAT = {
        "create": {
            "query": {},
            "body": _RESOURCE_POOL_BODY,
            "path": {},
        },
        "update": {
            "query": {},
            "body": payload_body_subset(_RESOURCE_POOL_BODY, exclude=("parent",)),
            "path": {},
        },
        "delete": {
            "query": {},
            "body": {},
            "path": {"resource_pool": "resource_pool"},
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
        parent = self.params.get("parent")

        if name and not parent:
            found_id = self._find_by_name(name)
            if found_id:
                return self._ensure_present_by_id(found_id)
            self.module.fail_json(msg="Resource pool not found with name: {0}".format(name))

        if name and parent:
            return self._create()

        self.module.fail_json(msg="name and parent are required when creating a resource pool")

    def ensure_absent(self):
        resource_pool = self.resolve_resource_id(
            "resource_pool",
            "name",
            self._find_by_name,
        )
        if not resource_pool:
            return {"changed": False}

        return self.delete_if_exists(ITEM_PATH, {"resource_pool": resource_pool})

    def _create(self):
        create_body = self.build_payload(self.PAYLOAD_FORMAT["create"])
        response = self.client.post(LIST_PATH, data=create_body)
        return {"changed": True, "value": response.json}

    def _ensure_present_by_id(self, resource_pool):
        path = self.build_path(ITEM_PATH, {"resource_pool": resource_pool})
        response = self.client.get(path)
        if response.status == 404:
            self.module.fail_json(
                msg="Resource pool not found: {0}".format(resource_pool)
            )

        return self.update_if_changed(
            path,
            response.json,
            self.build_updatable_payload(),
        )

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
    module_args["name"] = {"type": "str"}
    module_args["parent"] = {"type": "str"}
    module_args["resource_pool"] = {"type": "str"}
    module_args["cpu_allocation"] = {
        "type": "dict",
        "options": ALLOCATION_OPTIONS,
    }
    module_args["memory_allocation"] = {
        "type": "dict",
        "options": ALLOCATION_OPTIONS,
    }

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False,
    )

    crud_module = VmwareRestCrudModule(module)

    if module.params["state"] == "present":
        result = crud_module.ensure_present()
    elif module.params["state"] == "absent":
        result = crud_module.ensure_absent()
    else:
        module.fail_json(msg="Unsupported state: {0}".format(module.params["state"]))

    module.exit_json(**result)


if __name__ == "__main__":
    main()
