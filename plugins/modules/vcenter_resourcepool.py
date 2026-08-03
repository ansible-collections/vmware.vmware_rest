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
short_description: Manage vCenter resource pools.
description:
  - Create, update, and delete VMware vCenter resource pools.
  - A resource pool is a logical abstraction for flexible management of CPU and memory
    resources within a cluster or host. Resource pools can be nested to create a hierarchy
    for fine-grained resource allocation.
  - Use this module to provision new resource pools, adjust CPU and memory allocations,
    or remove existing resource pools from the vCenter inventory.

author:
  - Ansible Eco Content Team (@eco-ansible-content)

extends_documentation_fragment:
  - vmware.vmware_rest.connection_params

options:
  state:
    description:
      - The desired state of the resource.
      - Use C(present) to create or update the resource.
      - Use C(absent) to delete the resource.
    type: str
    default: present
    choices:
      - present
      - absent
  resource_pool:
    description:
      - Identifier of the resource pool to manage.
      - Must be an identifier (MOID) for a C(ResourcePool) resource.
    type: str
    required: false
  name:
    description:
      - Name of the resource pool.
      - This property was added in __vSphere API 7.0.0.0__.
    type: str
    required: false
  parent:
    description:
      - The parent resource pool under which to create this resource pool.
      - Must be the MOID (managed object identifier) of an existing C(ResourcePool).
      - This property was added in __vSphere API 7.0.0.0__.
    type: str
    required: false
  cpu_allocation:
    description:
      - Resource allocation for CPU.
      - This property was added in __vSphere API 7.0.0.0__.
      - If missing or 'null' or empty, use the default CPU allocation specification.
    type: dict
    required: false
    suboptions:
      reservation:
        description:
          - Amount of resource that is guaranteed available to a resource pool. Reserved resources are not
            wasted if they are not used. If the utilization is less than the reservation, the resources can be
            utilized by other running virtual machines. Units are MB for memory, and MHz for CPU.
          - This property was added in __vSphere API 7.0.0.0__.
          - If missing or 'null' or empty, *Vcenter.ResourcePool.ResourceAllocationCreateSpec.reservation* will be set to 0.
        type: int
        required: false
      expandable_reservation:
        description:
          - In a resource pool with an expandable reservation, the reservation can grow beyond the specified
            value, if the parent resource pool has unreserved resources. A non-expandable reservation is called
            a fixed reservation.
          - This property was added in __vSphere API 7.0.0.0__.
          - If missing or 'null' or empty, *Vcenter.ResourcePool.ResourceAllocationCreateSpec.expandable_reservation* will be set to true.
        type: bool
        required: false
      limit:
        description:
          - The utilization of a resource pool will not exceed this limit, even if there are available
            resources. This is typically used to ensure a consistent performance of resource pools independent
            of available resources. If set to -1, then there is no fixed limit on resource usage (only bounded
            by available resources and shares). Units are MB for memory, and MHz for CPU.
          - This property was added in __vSphere API 7.0.0.0__.
          - If missing or 'null' or empty, *Vcenter.ResourcePool.ResourceAllocationCreateSpec.limit* will be set to -1.
        type: int
        required: false
      shares:
        description:
          - Shares are used in case of resource contention.
          - This property was added in __vSphere API 7.0.0.0__.
          - If missing or 'null' or empty,
            *Vcenter.ResourcePool.ResourceAllocationCreateSpec.shares* will be set to
            '*Vcenter.ResourcePool.SharesInfo.Level.NORMAL*'.
        type: dict
        required: false
        suboptions:
          level:
            description:
              - The allocation level. It maps to a pre-determined set of numeric values for shares. If the
                shares value does not map to a predefined size, then the level is set as CUSTOM.
              - LOW - For CPU Shares = 500 * number of virtual CPUs. For Memory Shares = 5 * virtual machine memory size in MB.
              - NORMAL - For CPU Shares = 1000 * number of virtual CPUs. For Memory Shares = 10 * virtual machine memory size in MB.
              - HIGH - For CPU Shares = 2000 * number of virtual CPUs. For Memory Shares = 20 * virtual machine memory size in MB.
              - CUSTOM - If set, in case there is resource contention the server uses the shares value to determine the resource allocation.
              - For more information see *Vcenter.ResourcePool.SharesInfo.Level*.
              - This property was added in __vSphere API 7.0.0.0__.
            type: str
            required: true
            choices:
              - LOW
              - NORMAL
              - HIGH
              - CUSTOM
          shares:
            description:
              - When *Vcenter.ResourcePool.SharesInfo.level* is set to CUSTOM, it is the number of shares allocated. Otherwise, this value is ignored.
              - There is no unit for this value. It is a relative measure based on the settings for other resource pools.
              - This property was added in __vSphere API 7.0.0.0__.
              - This property is optional and it is only relevant when the value of level is *Vcenter.ResourcePool.SharesInfo.Level.CUSTOM*.
            type: int
            required: false
  memory_allocation:
    description:
      - Resource allocation for memory.
      - This property was added in __vSphere API 7.0.0.0__.
      - If missing or 'null' or empty, use the default memory allocation specification.
    type: dict
    required: false
    suboptions:
      reservation:
        description:
          - Amount of resource that is guaranteed available to a resource pool. Reserved resources are not
            wasted if they are not used. If the utilization is less than the reservation, the resources can be
            utilized by other running virtual machines. Units are MB for memory, and MHz for CPU.
          - This property was added in __vSphere API 7.0.0.0__.
          - If missing or 'null' or empty, *Vcenter.ResourcePool.ResourceAllocationCreateSpec.reservation* will be set to 0.
        type: int
        required: false
      expandable_reservation:
        description:
          - In a resource pool with an expandable reservation, the reservation can grow beyond the specified
            value, if the parent resource pool has unreserved resources. A non-expandable reservation is called
            a fixed reservation.
          - This property was added in __vSphere API 7.0.0.0__.
          - If missing or 'null' or empty, *Vcenter.ResourcePool.ResourceAllocationCreateSpec.expandable_reservation* will be set to true.
        type: bool
        required: false
      limit:
        description:
          - The utilization of a resource pool will not exceed this limit, even if there are available
            resources. This is typically used to ensure a consistent performance of resource pools independent
            of available resources. If set to -1, then there is no fixed limit on resource usage (only bounded
            by available resources and shares). Units are MB for memory, and MHz for CPU.
          - This property was added in __vSphere API 7.0.0.0__.
          - If missing or 'null' or empty, *Vcenter.ResourcePool.ResourceAllocationCreateSpec.limit* will be set to -1.
        type: int
        required: false
      shares:
        description:
          - Shares are used in case of resource contention.
          - This property was added in __vSphere API 7.0.0.0__.
          - If missing or 'null' or empty,
            *Vcenter.ResourcePool.ResourceAllocationCreateSpec.shares* will be set to
            '*Vcenter.ResourcePool.SharesInfo.Level.NORMAL*'.
        type: dict
        required: false
        suboptions:
          level:
            description:
              - The allocation level. It maps to a pre-determined set of numeric values for shares. If the
                shares value does not map to a predefined size, then the level is set as CUSTOM.
              - LOW - For CPU Shares = 500 * number of virtual CPUs. For Memory Shares = 5 * virtual machine memory size in MB.
              - NORMAL - For CPU Shares = 1000 * number of virtual CPUs. For Memory Shares = 10 * virtual machine memory size in MB.
              - HIGH - For CPU Shares = 2000 * number of virtual CPUs. For Memory Shares = 20 * virtual machine memory size in MB.
              - CUSTOM - If set, in case there is resource contention the server uses the shares value to determine the resource allocation.
              - For more information see *Vcenter.ResourcePool.SharesInfo.Level*.
              - This property was added in __vSphere API 7.0.0.0__.
            type: str
            required: true
            choices:
              - LOW
              - NORMAL
              - HIGH
              - CUSTOM
          shares:
            description:
              - When *Vcenter.ResourcePool.SharesInfo.level* is set to CUSTOM, it is the number of shares allocated. Otherwise, this value is ignored.
              - There is no unit for this value. It is a relative measure based on the settings for other resource pools.
              - This property was added in __vSphere API 7.0.0.0__.
              - This property is optional and it is only relevant when the value of level is *Vcenter.ResourcePool.SharesInfo.Level.CUSTOM*.
            type: int
            required: false

version_added: 5.0.0

requirements: []

notes:
  - Generated from vSphere API spec 9.1.0.
"""

EXAMPLES = r"""
- name: Create a basic resource pool
  vmware.vmware_rest.vcenter_resourcepool:
    name: my_resource_pool
    parent: resgroup-1001
    state: present
  register: my_resource_pool

- name: Create a resource pool with CPU and memory limits
  vmware.vmware_rest.vcenter_resourcepool:
    name: limited_pool
    parent: resgroup-1001
    cpu_allocation:
      reservation: 2000
      limit: 8000
      expandable_reservation: false
      shares:
        level: CUSTOM
        shares: 4000
    memory_allocation:
      reservation: 1024
      limit: 4096
      expandable_reservation: true
      shares:
        level: HIGH
    state: present

- name: Update an existing resource pool
  vmware.vmware_rest.vcenter_resourcepool:
    resource_pool: '{{ my_resource_pool.id }}'
    name: renamed_pool
    cpu_allocation:
      limit: 16000
    state: present

- name: Delete a resource pool
  vmware.vmware_rest.vcenter_resourcepool:
    resource_pool: '{{ my_resource_pool.id }}'
    state: absent
"""

RETURN = r"""
id:
  description: MOID of the managed resource pool.
  returned: When state is present, or when a resource is deleted, or when state is set to a supported action.
  sample: resgroup-1009
  type: str
value:
  description: The raw API response body from the vCenter operation.
  returned: On success
  type: raw
  sample:
    name: my-resource-pool
"""


from ansible.module_utils.basic import AnsibleModule
from ansible_collections.vmware.vmware_rest.plugins.module_utils._argument_spec import (
    connection_params_argument_spec,
)
from ansible_collections.vmware.vmware_rest.plugins.module_utils._errors import (
    VmwareModuleError,
)
from ansible_collections.vmware.vmware_rest.plugins.module_utils._crud_module import (
    VmwareRestCrudModuleBase,
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
            "module_param": "resource_pool",
        },
        "names": {
            "required": False,
            "module_param": "name",
        },
    },
)

GET_OPERATION = OperationConfig(
    name="get",
    uri=ITEM_ENDPOINT,
    http_method="GET",
)

CREATE_OPERATION = OperationConfig(
    name="create",
    uri=LIST_ENDPOINT,
    http_method="POST",
    body_spec={
        "name": {
            "required": True,
        },
        "parent": {
            "required": True,
        },
        "cpu_allocation": {
            "required": False,
            "subspec": {
                "reservation": {
                    "required": False,
                },
                "expandable_reservation": {
                    "required": False,
                },
                "limit": {
                    "required": False,
                },
                "shares": {
                    "required": False,
                    "subspec": {
                        "level": {
                            "required": False,
                        },
                        "shares": {
                            "required": False,
                        },
                    },
                },
            },
        },
        "memory_allocation": {
            "required": False,
            "subspec": {
                "reservation": {
                    "required": False,
                },
                "expandable_reservation": {
                    "required": False,
                },
                "limit": {
                    "required": False,
                },
                "shares": {
                    "required": False,
                    "subspec": {
                        "level": {
                            "required": False,
                        },
                        "shares": {
                            "required": False,
                        },
                    },
                },
            },
        },
    },
)

UPDATE_OPERATION = OperationConfig(
    name="update",
    uri=ITEM_ENDPOINT,
    http_method="PATCH",
    body_spec={
        "name": {
            "required": False,
        },
        "cpu_allocation": {
            "required": False,
            "subspec": {
                "reservation": {
                    "required": False,
                },
                "expandable_reservation": {
                    "required": False,
                },
                "limit": {
                    "required": False,
                },
                "shares": {
                    "required": False,
                    "subspec": {
                        "level": {
                            "required": False,
                        },
                        "shares": {
                            "required": False,
                        },
                    },
                },
            },
        },
        "memory_allocation": {
            "required": False,
            "subspec": {
                "reservation": {
                    "required": False,
                },
                "expandable_reservation": {
                    "required": False,
                },
                "limit": {
                    "required": False,
                },
                "shares": {
                    "required": False,
                    "subspec": {
                        "level": {
                            "required": False,
                        },
                        "shares": {
                            "required": False,
                        },
                    },
                },
            },
        },
    },
)

DELETE_OPERATION = OperationConfig(
    name="delete",
    uri=ITEM_ENDPOINT,
    http_method="DELETE",
)


def create_module_argument_spec() -> dict:
    module_args = connection_params_argument_spec()
    module_args["cpu_allocation"] = {
        "type": "dict",
        "options": {
            "reservation": {
                "type": "int",
            },
            "expandable_reservation": {
                "type": "bool",
            },
            "limit": {
                "type": "int",
            },
            "shares": {
                "type": "dict",
                "options": {
                    "level": {
                        "type": "str",
                        "choices": ["LOW", "NORMAL", "HIGH", "CUSTOM"],
                        "required": True,
                    },
                    "shares": {
                        "type": "int",
                    },
                },
            },
        },
    }
    module_args["memory_allocation"] = {
        "type": "dict",
        "options": {
            "reservation": {
                "type": "int",
            },
            "expandable_reservation": {
                "type": "bool",
            },
            "limit": {
                "type": "int",
            },
            "shares": {
                "type": "dict",
                "options": {
                    "level": {
                        "type": "str",
                        "choices": ["LOW", "NORMAL", "HIGH", "CUSTOM"],
                        "required": True,
                    },
                    "shares": {
                        "type": "int",
                    },
                },
            },
        },
    }
    module_args["name"] = {
        "type": "str",
    }
    module_args["parent"] = {
        "type": "str",
    }
    module_args["resource_pool"] = {
        "type": "str",
    }
    module_args["state"] = {
        "type": "str",
        "choices": ["present", "absent"],
        "default": "present",
    }
    return module_args


def main():
    module = AnsibleModule(
        argument_spec=create_module_argument_spec(),
        supports_check_mode=True,
    )

    crud_module = VmwareRestCrudModuleBase(
        module=module,
        moid_parameter_hints=MOID_PARAMETER_HINTS,
        get_operation_config=GET_OPERATION,
        list_operation_config=LIST_OPERATION,
        create_operation_config=CREATE_OPERATION,
        update_operation_config=UPDATE_OPERATION,
        delete_operation_config=DELETE_OPERATION,
    )

    try:
        if module.params["state"] == "present":
            result = crud_module.ensure_present()
        elif module.params["state"] == "absent":
            result = crud_module.ensure_absent()

        else:
            module.fail_json(
                msg="Unsupported state: {0}".format(module.params["state"])
            )
    except VmwareModuleError as e:
        module.fail_json(**e.to_module_fail_json_output())

    module.exit_json(**result)


if __name__ == "__main__":
    main()
