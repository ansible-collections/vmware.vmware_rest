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
module: vcenter_folder_info
short_description: Gather information about vCenter folders.
description:
  - Retrieve information about one or more VMware vCenter folders.
  - Returns the folders that match the supplied filters, or all folders when no filter is given.
  - Use the filter parameters to narrow results by folder name, identifier, type, parent folder,
    or datacenter.

deprecated:
  removed_in: 6.0.0
  why: This functionality has been moved to vmware.vmware.folder_info.
  alternative: Use M(vmware.vmware.folder_info) instead.

author:
  - Ansible Eco Content Team (@eco-ansible-content)

extends_documentation_fragment:
  - vmware.vmware_rest.connection_params

options:
  filter:
    description:
      - A specification used to filter the folders that are returned.
      - If omitted, all folders match the filter.
    type: dict
    required: false
    suboptions:
      type:
        description:
          - Return only folders of this type.
          - DATACENTER - A folder that can contain datacenters.
          - DATASTORE - A folder that can contain datastores.
          - HOST - A folder that can contain compute resources (hosts and clusters).
          - NETWORK - A folder that can contain networks.
          - VIRTUAL_MACHINE - A folder that can contain virtual machines.
          - If omitted, folders of any type are returned.
        type: str
        required: false
        choices:
          - DATACENTER
          - DATASTORE
          - HOST
          - NETWORK
          - VIRTUAL_MACHINE
  folders:
    aliases:
      - filter_folders
    description:
      - A list of folder MOIDs to filter the results.
      - Only folders whose identifiers appear in this list will be returned.
      - If omitted or empty, folders with any identifier are returned.
    type: list
    required: false
    elements: str
  names:
    aliases:
      - filter_names
    description:
      - A list of folder names to filter the results.
      - Only folders whose names appear in this list will be returned.
      - If omitted or empty, folders with any name are returned.
    type: list
    required: false
    elements: str
  parent_folders:
    description:
      - A list of parent folder MOIDs to filter the results.
      - Only folders that reside directly within the specified parent folders will be returned.
      - If omitted or empty, folders in any parent folder are returned.
    type: list
    required: false
    elements: str
  datacenters:
    aliases:
      - filter_datacenters
    description:
      - A list of datacenter MOIDs to filter the results.
      - Only folders that reside in the specified datacenters will be returned.
      - If omitted or empty, folders in any datacenter are returned.
    type: list
    required: false
    elements: str

version_added: 5.0.0

requirements: []

notes:
  - Generated from vSphere API spec 9.1.0.
  - Compatible with vSphere API 7.0.3.
  - Compatible with vSphere API 8.0.2.
"""

EXAMPLES = r"""
- name: List all folders
  vmware.vmware_rest.vcenter_folder_info:
  register: all_folders

- name: List only virtual machine folders
  vmware.vmware_rest.vcenter_folder_info:
    filter:
      type: VIRTUAL_MACHINE
  register: vm_folders

- name: Filter folders by name
  vmware.vmware_rest.vcenter_folder_info:
    names:
      - my_folder
  register: filtered_folders

- name: List virtual machine folders within a specific datacenter
  vmware.vmware_rest.vcenter_folder_info:
    filter:
      type: VIRTUAL_MACHINE
    datacenters:
      - datacenter-1001
  register: dc_vm_folders
"""

RETURN = r"""
value:
  description:
    - Raw output from the API response.
    - This output is maintained for consistency with version 4.x and earlier of this collection.
      It is recommended to switch to the info return key for a more consistent and documented output.
  returned: On success.
  sample:
    folder: group-v1005
    name: my_folder
    type: VIRTUAL_MACHINE
  type: raw
info:
  description: A list of folders matching the query.
  returned: On success.
  sample:
    - folder: group-v1005
      name: my_folder
      type: VIRTUAL_MACHINE
  type: list
"""


from ansible.module_utils.basic import AnsibleModule
from ansible_collections.vmware.vmware_rest.plugins.module_utils._argument_spec import (
    connection_params_argument_spec,
)
from ansible_collections.vmware.vmware_rest.plugins.module_utils._errors import (
    VmwareModuleError,
)
from ansible_collections.vmware.vmware_rest.plugins.module_utils._info_module import (
    VmwareRestInfoModuleBase,
)
from ansible_collections.vmware.vmware_rest.plugins.module_utils._operation_configs import (
    OperationConfig,
)

MOID_PARAMETER_HINTS = []

LIST_ENDPOINT = ""
ITEM_ENDPOINT = "/vcenter/folder"


GET_OPERATION = OperationConfig(
    name="get",
    uri=ITEM_ENDPOINT,
    http_method="GET",
    query_spec={
        "filter": {
            "required": False,
            "subspec": {
                "type": {
                    "required": False,
                },
            },
        },
        "folders": {
            "required": False,
        },
        "names": {
            "required": False,
        },
        "parent_folders": {
            "required": False,
        },
        "datacenters": {
            "required": False,
        },
    },
)


def create_module_argument_spec() -> dict:
    module_args = connection_params_argument_spec()
    module_args["datacenters"] = {
        "type": "list",
        "aliases": ["filter_datacenters"],
        "elements": "str",
    }
    module_args["filter"] = {
        "type": "dict",
        "options": {
            "type": {
                "type": "str",
                "choices": [
                    "DATACENTER",
                    "DATASTORE",
                    "HOST",
                    "NETWORK",
                    "VIRTUAL_MACHINE",
                ],
            },
        },
    }
    module_args["folders"] = {
        "type": "list",
        "aliases": ["filter_folders"],
        "elements": "str",
    }
    module_args["names"] = {
        "type": "list",
        "aliases": ["filter_names"],
        "elements": "str",
    }
    module_args["parent_folders"] = {
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
    )
    try:
        result = info_module.get_resource_info()
    except VmwareModuleError as e:
        module.fail_json(**e.to_module_fail_json_output())
    module.exit_json(**result)


if __name__ == "__main__":
    main()
