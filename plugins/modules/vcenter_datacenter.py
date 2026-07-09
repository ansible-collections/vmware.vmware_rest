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
module: vcenter_datacenter
short_description: Manage vCenter datacenters
description:
  - This module allows you to create and delete datacenters in vCenter Server.
  - Datacenters are organizational containers that group compute resources like hosts and clusters.
  - A datacenter must be created in a specific folder within the vCenter inventory.
  - You can force deletion of a datacenter even if it contains resources.

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
  datacenter:
    description:
      - Identifier of the datacenter to manage.
      - Must be an identifier (MOID) for a C(Datacenter) resource.
    type: str
    required: false
  name:
    description:
      - The name of the datacenter to be created.
      - Required when creating a new datacenter (state is present).
    type: str
    required: false
  folder:
    description:
      - The folder in which the datacenter should be created.
      - Must be the MOID (managed object identifier) of an existing Folder.
      - This is required when creating a datacenter.
    type: str
    required: false
  force:
    description:
      - Whether to force deletion of a non-empty datacenter.
      - If true, the datacenter will be deleted even if it contains resources.
      - If false or omitted, deletion will fail if the datacenter is not empty.
    type: bool
    required: false

version_added: 5.0.0

requirements: []

notes:
  - Generated from vSphere API spec 9.1.0.
  - Compatible with vSphere API 8.0.2.
  - Compatible with vSphere API 7.0.3.
"""

EXAMPLES = r"""
- name: Create a datacenter
  vmware.vmware_rest.vcenter_datacenter:
    name: my-datacenter
    folder: group-d1
    state: present

- name: Delete an empty datacenter
  vmware.vmware_rest.vcenter_datacenter:
    datacenter: datacenter-1001
    state: absent

- name: Force delete a datacenter with resources
  vmware.vmware_rest.vcenter_datacenter:
    datacenter: datacenter-1001
    force: true
    state: absent
"""

RETURN = r"""
id:
  description: MOID of the managed datacenter
  returned: When state is present, or when a resource is deleted, or when state is set to a supported action
  sample: datacenter-1001
  type: str
"""


from ansible.module_utils.basic import AnsibleModule
from ansible_collections.vmware.vmware_rest.plugins.module_utils._argument_spec import (
    connection_params_argument_spec,
)
from ansible_collections.vmware.vmware_rest.plugins.module_utils._crud_module import (
    VmwareRestCrudModuleBase,
)
from ansible_collections.vmware.vmware_rest.plugins.module_utils._operation_configs import (
    OperationConfig,
)

MOID_PARAMETER_HINTS = ["datacenter"]

LIST_ENDPOINT = "/vcenter/datacenter"
ITEM_ENDPOINT = "/vcenter/datacenter/{datacenter}"


LIST_OPERATION = OperationConfig(
    name="list",
    uri=LIST_ENDPOINT,
    http_method="GET",
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
        "folder": {
            "required": False,
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
    module_args["datacenter"] = {
        "type": "str",
    }
    module_args["folder"] = {
        "type": "str",
    }
    module_args["force"] = {
        "type": "bool",
    }
    module_args["name"] = {
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
        delete_operation_config=DELETE_OPERATION,
    )

    if module.params["state"] == "present":
        result = crud_module.ensure_present()
    elif module.params["state"] == "absent":
        result = crud_module.ensure_absent()

    else:
        module.fail_json(msg="Unsupported state: {0}".format(module.params["state"]))

    module.exit_json(**result)


if __name__ == "__main__":
    main()
