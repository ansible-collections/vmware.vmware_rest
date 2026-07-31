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
short_description: Gather information about vCenter datacenters.
description:
  - Retrieve information about one or more VMware vCenter datacenters.
  - Can return a list of all datacenters or detailed information about a specific datacenter
    identified by its MOID.
  - Use the filter parameters to narrow results by datacenter name, identifier, or parent folder.

author:
  - Ansible Eco Content Team (@eco-ansible-content)

extends_documentation_fragment:
  - vmware.vmware_rest.connection_params

options:
  datacenter:
    description:
      - Identifier of the datacenter to retrieve details for.
      - Must be an identifier (MOID) for a C(Datacenter) resource.
    type: str
    required: false
  datacenters:
    aliases:
      - filter_datacenters
    description:
      - A list of datacenter MOIDs to filter the results.
      - Only datacenters whose identifiers appear in this list will be returned.
      - If omitted or empty, datacenters with any identifier are returned.
    type: list
    required: false
    elements: str
  names:
    aliases:
      - filter_names
    description:
      - A list of datacenter names to filter the results.
      - Only datacenters whose names appear in this list will be returned.
      - If omitted or empty, datacenters with any name are returned.
    type: list
    required: false
    elements: str
  folders:
    aliases:
      - filter_folders
    description:
      - A list of folder MOIDs to filter the results.
      - Only datacenters that reside in the specified folders will be returned.
      - If omitted or empty, datacenters in any folder are returned.
    type: list
    required: false
    elements: str

version_added: 5.0.0

requirements: []

notes:
  - Generated from vSphere API spec 9.1.0.
"""

EXAMPLES = r"""
- name: List all datacenters
  vmware.vmware_rest.vcenter_datacenter_info:
  register: all_datacenters

- name: Get details about a specific datacenter
  vmware.vmware_rest.vcenter_datacenter_info:
    datacenter: datacenter-1001
  register: my_datacenter

- name: Filter datacenters by name
  vmware.vmware_rest.vcenter_datacenter_info:
    names:
      - my_datacenter
  register: filtered_datacenters
"""

RETURN = r"""
id:
  description: MOID of the queried datacenter.
  returned: When only one resource, with a MOID, was queried.
  sample: datacenter-1001
  type: str
value:
  description:
    - Raw output from the API response.
    - This output is maintained for consistency with version 4.x and earlier of this collection.
      It is recommended to switch to the info return key for a more consistent and documented output.
  returned: On success.
  sample:
    name: my_datacenter
    datastore_folder: group-s1002
    host_folder: group-h1003
    network_folder: group-n1004
    vm_folder: group-v1005
  type: raw
info:
  description: A list of datacenters matching the query.
  returned: On success.
  sample:
    - datacenter: datacenter-1001
      name: my_datacenter
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
        "aliases": ["filter_datacenters"],
        "elements": "str",
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
    try:
        result = info_module.get_resource_info()
    except VmwareModuleError as e:
        module.fail_json(**e.to_module_fail_json_output())
    module.exit_json(**result)


if __name__ == "__main__":
    main()
