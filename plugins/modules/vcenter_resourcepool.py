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
module: vcenter_resourcepool
short_description: Manage vCenter resource pools
description:
  - Create, update, or delete resource pools in vCenter.
  - Resource pools are used to partition CPU and memory resources for virtual machines.
  - This module ensures a resource pool exists with the specified configuration or is absent.

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
      - Required when I(state=absent) or when updating an existing resource pool.
      - Mutually exclusive with I(name) when I(state=present).
    type: str
    required: false
  name:
    description:
      - Name of the resource pool.
      - Required when creating a new resource pool (I(state=present) without I(resource_pool)).
      - When updating, specifies the new name for the resource pool.
    type: str
    required: false
  parent:
    description:
      - Parent resource pool for the new resource pool.
      - Must be an identifier (MOID) for a C(ResourcePool) resource.
      - Required when creating a new resource pool.
      - Cannot be changed after creation.
    type: str
    required: false
  cpu_allocation:
    description:
      - Resource allocation settings for CPU.
      - If omitted during creation, default CPU allocation is used.
    type: dict
    required: false
    suboptions:
      reservation:
        description:
          - Amount of CPU resource guaranteed available to the resource pool in MHz.
          - Reserved resources can be used by other VMs if not utilized.
          - If omitted, defaults to 0.
        type: int
        required: false
      expandable_reservation:
        description:
          - Whether the reservation can grow beyond the specified value if parent has unreserved resources.
          - If omitted, defaults to true.
        type: bool
        required: false
      limit:
        description:
          - Maximum CPU usage limit in MHz.
          - Set to -1 for no limit (only bounded by available resources and shares).
          - If omitted, defaults to -1.
        type: int
        required: false
      shares:
        description:
          - Shares configuration for resource contention.
          - If omitted, defaults to NORMAL level.
        type: dict
        required: false
        suboptions:
          level:
            description:
              - The allocation level determining share values.
              - C(LOW) maps to 500 shares per vCPU.
              - C(NORMAL) maps to 1000 shares per vCPU.
              - C(HIGH) maps to 2000 shares per vCPU.
              - C(CUSTOM) allows specifying exact share value in I(shares).
            type: str
            required: true
            choices:
              - LOW
              - NORMAL
              - HIGH
              - CUSTOM
          shares:
            description:
              - Number of shares when I(level=CUSTOM).
              - Ignored for other levels.
              - No unit; relative measure compared to other resource pools.
            type: int
            required: false
  memory_allocation:
    description:
      - Resource allocation settings for memory.
      - If omitted during creation, default memory allocation is used.
    type: dict
    required: false
    suboptions:
      reservation:
        description:
          - Amount of memory resource guaranteed available to the resource pool in MB.
          - Reserved resources can be used by other VMs if not utilized.
          - If omitted, defaults to 0.
        type: int
        required: false
      expandable_reservation:
        description:
          - Whether the reservation can grow beyond the specified value if parent has unreserved resources.
          - If omitted, defaults to true.
        type: bool
        required: false
      limit:
        description:
          - Maximum memory usage limit in MB.
          - Set to -1 for no limit (only bounded by available resources and shares).
          - If omitted, defaults to -1.
        type: int
        required: false
      shares:
        description:
          - Shares configuration for resource contention.
          - If omitted, defaults to NORMAL level.
        type: dict
        required: false
        suboptions:
          level:
            description:
              - The allocation level determining share values.
              - C(LOW) maps to 5 shares per MB of memory.
              - C(NORMAL) maps to 10 shares per MB of memory.
              - C(HIGH) maps to 20 shares per MB of memory.
              - C(CUSTOM) allows specifying exact share value in I(shares).
            type: str
            required: true
            choices:
              - LOW
              - NORMAL
              - HIGH
              - CUSTOM
          shares:
            description:
              - Number of shares when I(level=CUSTOM).
              - Ignored for other levels.
              - No unit; relative measure compared to other resource pools.
            type: int
            required: false

version_added: "5.0.0"
requirements: []

notes:
  - Generated from vSphere API spec 9.1.0.
  - Root resource pools cannot be deleted.
"""

EXAMPLES = r"""
- name: Create a resource pool
  vmware.vmware_rest.vcenter_resourcepool:
    vcenter_hostname: "vcenter.example.com"
    vcenter_username: "administrator@vsphere.local"
    vcenter_password: "password"
    state: present
    name: "Production"
    parent: "resgroup-root"
    cpu_allocation:
      reservation: 1000
      limit: 4000
      shares:
        level: "HIGH"
    memory_allocation:
      reservation: 2048
      limit: 8192
      shares:
        level: "HIGH"
  register: new_pool

- name: Update resource pool CPU allocation
  vmware.vmware_rest.vcenter_resourcepool:
    vcenter_hostname: "vcenter.example.com"
    vcenter_username: "administrator@vsphere.local"
    vcenter_password: "password"
    state: present
    resource_pool: "resgroup-123"
    cpu_allocation:
      limit: 6000
      shares:
        level: "CUSTOM"
        shares: 3000
  register: updated_pool

- name: Delete a resource pool
  vmware.vmware_rest.vcenter_resourcepool:
    vcenter_hostname: "vcenter.example.com"
    vcenter_username: "administrator@vsphere.local"
    vcenter_password: "password"
    state: absent
    resource_pool: "resgroup-123"
  register: deleted_pool
"""

RETURN = r"""
id:
  description:
    - The MOID of the resource pool.
    - Returned when creating a new resource pool.
  returned: On create
  sample: "resgroup-123"
  type: str

value:
  description:
    - Updated resource pool configuration.
    - Only returned when updating an existing resource pool.
  returned: On update
  sample:
    name: "Production-Updated"
    cpu_allocation:
      reservation: 2000
      limit: 8000
      expandable_reservation: true
      shares:
        level: "HIGH"
  type: dict
"""


from ansible.module_utils.basic import AnsibleModule
from ansible_collections.vmware.vmware_rest.plugins.module_utils._argument_spec import (
    connection_params_argument_spec,
)
from ansible_collections.vmware.vmware_rest.plugins.module_utils._module_base import (
    VmwareRestCrudModuleBase,
    params_differ,
    payload_body_subset,
)


class VmwareRestCrudModule(VmwareRestCrudModuleBase):
    _CREATE_BODY = {
        "name": "name",
        "parent": "parent",
        "cpu_allocation": "cpu_allocation",
        "memory_allocation": "memory_allocation",
    }

    PAYLOAD_FORMAT = {
        "create": {
            "query": {},
            "body": _CREATE_BODY,
            "path": {},
        },
        "update": {
            "query": {},
            "body": payload_body_subset(_CREATE_BODY, exclude=("parent",)),
            "path": {"resourcePool": "resource_pool"},
        },
        "delete": {
            "query": {},
            "body": {},
            "path": {"resourcePool": "resource_pool"},
        },
    }

    UPDATABLE_PARAMS = ("name", "cpu_allocation", "memory_allocation")

    def ensure_present(self, path_template: str) -> dict:
        """
        Ensure a resource pool exists with the desired configuration.

        Creates the resource pool if it does not exist, or updates it if configuration differs.
        Returns changed=True only when the resource pool was created or modified.
        """
        resource_pool_id = self.params.get("resource_pool")

        if not resource_pool_id:
            if not self.params.get("name"):
                self.module.fail_json(msg="'name' is required when creating a new resource pool")
            if not self.params.get("parent"):
                self.module.fail_json(msg="'parent' is required when creating a new resource pool")

            create_body = self.build_payload(self.PAYLOAD_FORMAT["create"])
            if not self.module.check_mode:
                response = self.client.post("/vcenter/resource-pool", data=create_body)
                resource_pool_id = response.json
                result = {"changed": True, "id": resource_pool_id}
            else:
                result = {"changed": True}
            return result

        path = self.build_path(path_template)
        response = self.client.get(path)
        if response.status == 404:
            self.module.fail_json(msg=f"Resource pool '{resource_pool_id}' not found")

        current = response.json
        desired = self.build_payload(self.PAYLOAD_FORMAT["update"])

        if not desired:
            return {"changed": False, "value": current}

        if not params_differ(current, desired):
            return {"changed": False, "value": current}

        if not self.module.check_mode:
            self.client.patch(path, data=desired)
            updated_response = self.client.get(path)
            result = {"changed": True, "value": updated_response.json}
        else:
            result = {"changed": True}

        return result

    def ensure_absent(self, path_template: str) -> dict:
        """
        Ensure a resource pool is deleted.

        Returns changed=False if the resource pool does not exist.
        Returns changed=True if the resource pool was deleted.
        """
        if not self.params.get("resource_pool"):
            self.module.fail_json(msg="'resource_pool' is required when state=absent")

        path = self.build_path(path_template)
        response = self.client.get(path)

        if response.status == 404:
            return {"changed": False}

        if not self.module.check_mode:
            self.client.delete(path)

        return {"changed": True}


def main():
    module_args = connection_params_argument_spec()

    module_args["state"] = {
        "type": "str",
        "choices": ["present", "absent"],
        "default": "present",
    }
    module_args["resource_pool"] = {
        "type": "str",
        "required": False,
    }
    module_args["name"] = {
        "type": "str",
        "required": False,
    }
    module_args["parent"] = {
        "type": "str",
        "required": False,
    }
    module_args["cpu_allocation"] = {
        "type": "dict",
        "required": False,
        "options": {
            "reservation": {"type": "int", "required": False},
            "expandable_reservation": {"type": "bool", "required": False},
            "limit": {"type": "int", "required": False},
            "shares": {
                "type": "dict",
                "required": False,
                "options": {
                    "level": {
                        "type": "str",
                        "required": True,
                        "choices": ["LOW", "NORMAL", "HIGH", "CUSTOM"],
                    },
                    "shares": {"type": "int", "required": False},
                },
            },
        },
    }
    module_args["memory_allocation"] = {
        "type": "dict",
        "required": False,
        "options": {
            "reservation": {"type": "int", "required": False},
            "expandable_reservation": {"type": "bool", "required": False},
            "limit": {"type": "int", "required": False},
            "shares": {
                "type": "dict",
                "required": False,
                "options": {
                    "level": {
                        "type": "str",
                        "required": True,
                        "choices": ["LOW", "NORMAL", "HIGH", "CUSTOM"],
                    },
                    "shares": {"type": "int", "required": False},
                },
            },
        },
    }

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
    )

    crud_module = VmwareRestCrudModule(module)

    path_template = "/vcenter/resource-pool/{resource_pool}"
    if module.params["state"] == "present":
        result = crud_module.ensure_present(path_template)
    elif module.params["state"] == "absent":
        result = crud_module.ensure_absent(path_template)
    else:
        module.fail_json(msg="Unsupported state: {0}".format(module.params["state"]))

    module.exit_json(**result)


if __name__ == "__main__":
    main()
