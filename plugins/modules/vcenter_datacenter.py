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
short_description: PLACEHOLDER
description:
  - PLACEHOLDER

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
    type: str
    required: false
  folder:
    description:
      - Datacenter folder in which the new datacenter should be created.
      - This property is currently required. In the future, if this property is missing or 'null', the system will attempt to choose a suitable folder for the datacenter; if a folder cannot be chosen, the datacenter creation operation will fail.
      - When clients pass a value of this schema as a parameter, the property must be an identifier (MOID) for the resource type 'Folder'. When operations return a value of this schema as a response, the property will be an identifier (MOID) for the resource type 'Folder'.
    type: str
    required: false
  force:
    description:
      - If true, delete the datacenter even if it is not empty.
      - If missing or 'null' a *Vapi.Std.Errors.ResourceInUse* error will be reported if the datacenter is not empty. This is the equivalent of passing the value false.
    type: bool
    required: false

version_added: 5.0.0

requirements: []

notes:
  - Generated from vSphere API spec 9.1.0.
"""

EXAMPLES = r"""
"""

RETURN = r"""
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
    query_spec={
        "datacenters": {
            "required": False,
            "module_param": "datacenter",
        },
        "names": {
            "required": False,
            "module_param": "name",
        },
        "folders": {
            "required": False,
            "module_param": "folder",
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
        "folder": {
            "required": False,
        },
    },
)

DELETE_OPERATION = OperationConfig(
    name="delete",
    uri=ITEM_ENDPOINT,
    http_method="DELETE",
    query_spec={
        "force": {
            "required": False,
        },
    },
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
        "choices": ['present', 'absent'],
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
