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
module: vcenter_datacenter_info
short_description: PLACEHOLDER
description:
  - PLACEHOLDER

author:
  - Ansible Eco Content Team (@eco-ansible-content)

extends_documentation_fragment:
  - vmware.vmware_rest.connection_params

options:
  datacenter:
    description:
      - Identifier of the datacenter to manage.
      - Must be an identifier (MOID) for a C(Datacenter) resource.
    type: str
    required: false
  datacenters:
    description:
      - Identifiers of datacenters that can match the filter.
      - If missing or 'null' or empty, datacenters with any identifier match the filter.
      - When clients pass a value of this schema as a parameter, the property must contain identifiers (MOIDs) for the resource type 'Datacenter'. When operations return a value of this schema as a response, the property will contain identifiers (MOIDs) for the resource type 'Datacenter'.
    type: list
    required: false
    elements: str
  names:
    description:
      - Names that datacenters must have to match the filter (see *Vcenter.Datacenter.Info.name*).
      - If missing or 'null' or empty, datacenters with any name match the filter.
    type: list
    required: false
    elements: str
  folders:
    description:
      - Folders that must contain the datacenters for the datacenter to match the filter.
      - If missing or 'null' or empty, datacenters in any folder match the filter.
      - When clients pass a value of this schema as a parameter, the property must contain identifiers (MOIDs) for the resource type 'Folder'. When operations return a value of this schema as a response, the property will contain identifiers (MOIDs) for the resource type 'Folder'.
    type: list
    required: false
    elements: str

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
from ansible_collections.vmware.vmware_rest.plugins.module_utils._info_module import (
    VmwareRestInfoModuleBase,
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
        },
        "names": {
            "required": False,
        },
        "folders": {
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
    module_args["datacenter"] = {
        "type": "str",
    }
    module_args["datacenters"] = {
        "type": "list",
        "elements": "str",
    }
    module_args["folders"] = {
        "type": "list",
        "elements": "str",
    }
    module_args["names"] = {
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
    result = info_module.get_resource_info()
    module.exit_json(**result)


if __name__ == "__main__":
    main()
