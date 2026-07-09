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
short_description: Gather information about vCenter datacenters
description:
  - This module retrieves information about datacenters in vCenter Server.
  - You can query information about a specific datacenter by its identifier.
  - You can also list all datacenters or filter by name, folder, or multiple identifiers.
  - Datacenters are organizational containers that group compute resources like hosts and clusters.

author:
  - Ansible Eco Content Team (@eco-ansible-content)

extends_documentation_fragment:
  - vmware.vmware_rest.connection_params

options:
  datacenter:
    description:
      - Identifier of a specific datacenter to query.
      - Must be an identifier (MOID) for a C(Datacenter) resource.
      - When specified, returns detailed information about this single datacenter.
    type: str
    required: false
  datacenters:
    description:
      - List of datacenter identifiers to filter by.
      - Only datacenters matching these MOIDs will be returned.
      - If omitted or empty, all datacenters match this filter criterion.
    type: list
    required: false
    elements: str
  names:
    description:
      - List of datacenter names to filter by.
      - Only datacenters with these names will be returned.
      - If omitted or empty, all datacenters match this filter criterion.
    type: list
    required: false
    elements: str
  folders:
    description:
      - List of folder identifiers to filter by.
      - Only datacenters contained in these folders will be returned.
      - Each value must be a MOID for a Folder resource.
      - If omitted or empty, datacenters in any folder match this filter criterion.
    type: list
    required: false
    elements: str

version_added: 5.0.0

requirements: []

notes:
  - Generated from vSphere API spec 9.1.0.
  - Compatible with vSphere API 8.0.2.
  - Compatible with vSphere API 7.0.3.
"""

EXAMPLES = r"""
- name: Get information about all datacenters
  vmware.vmware_rest.vcenter_datacenter_info:
  register: all_datacenters

- name: Get information about a specific datacenter
  vmware.vmware_rest.vcenter_datacenter_info:
    datacenter: datacenter-1001
  register: datacenter_info

- name: Get datacenters by name
  vmware.vmware_rest.vcenter_datacenter_info:
    names:
      - production-dc
      - development-dc
  register: filtered_datacenters

- name: Get datacenters in specific folders
  vmware.vmware_rest.vcenter_datacenter_info:
    folders:
      - group-d1
      - group-d2
  register: datacenters_in_folders
"""

RETURN = r"""
id:
  description: MOID of the queried resource
  returned: When only one resource, with a MOID, was queried
  sample: datacenter-1001
  type: str

value:
  description: Detailed information about a single datacenter
  returned: When only one resource was queried
  sample:
    datacenter: datacenter-1001
    name: production-dc
  type: dict

info:
  description: A list of detailed information about datacenters
  returned: On success
  sample:
    - datacenter: datacenter-1001
      name: production-dc
    - datacenter: datacenter-1002
      name: development-dc
  type: list
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
