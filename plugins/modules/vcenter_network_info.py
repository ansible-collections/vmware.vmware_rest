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
module: vcenter_network_info
short_description: Gather information about vCenter networks.
description:
  - Retrieve information about one or more VMware vCenter networks.
  - Returns the networks that match the supplied filters, or all networks when no filter is given.
  - Use the filter parameters to narrow results by network name, identifier, type, folder,
    or datacenter.

author:
  - Ansible Eco Content Team (@eco-ansible-content)

extends_documentation_fragment:
  - vmware.vmware_rest.connection_params

options:
  networks:
    description:
      - A list of network MOIDs to filter the results.
      - Only networks whose identifiers appear in this list will be returned.
      - If omitted or empty, networks with any identifier are returned.
    type: list
    required: false
    elements: str
  names:
    aliases:
      - filter_names
    description:
      - A list of network names to filter the results.
      - Only networks whose names appear in this list will be returned.
      - If omitted or empty, networks with any name are returned.
    type: list
    required: false
    elements: str
  types:
    aliases:
      - filter_types
    description:
      - A list of network types to filter the results.
      - Only networks of one of the listed types will be returned.
      - STANDARD_PORTGROUP - vSphere standard portgroup (created and managed on ESX).
      - DISTRIBUTED_PORTGROUP - Distributed virtual portgroup (created and managed through vCenter).
      - OPAQUE_NETWORK - A network whose configuration is managed outside of vSphere. The identifier
        and name of the network is made available through vSphere so that host and virtual machine
        virtual ethernet devices can connect to them.
      - If omitted or empty, networks of any type are returned.
    type: list
    required: false
    elements: str
  folders:
    aliases:
      - filter_folders
    description:
      - A list of folder MOIDs to filter the results.
      - Only networks that reside in the specified folders will be returned.
      - If omitted or empty, networks in any folder are returned.
    type: list
    required: false
    elements: str
  datacenters:
    aliases:
      - filter_datacenters
    description:
      - A list of datacenter MOIDs to filter the results.
      - Only networks that reside in the specified datacenters will be returned.
      - If omitted or empty, networks in any datacenter are returned.
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
- name: List all networks
  vmware.vmware_rest.vcenter_network_info:
  register: all_networks

- name: Filter networks by name
  vmware.vmware_rest.vcenter_network_info:
    names:
      - VM Network
  register: filtered_networks

- name: List distributed portgroups
  vmware.vmware_rest.vcenter_network_info:
    types:
      - DISTRIBUTED_PORTGROUP
  register: dvpg_networks

- name: List standard portgroups in a specific datacenter
  vmware.vmware_rest.vcenter_network_info:
    types:
      - STANDARD_PORTGROUP
    datacenters:
      - datacenter-1001
  register: dc_networks
"""

RETURN = r"""
value:
  description:
    - Raw output from the API response.
    - This output is maintained for consistency with version 4.x and earlier of this collection.
      It is recommended to switch to the info return key for a more consistent and documented output.
  returned: On success.
  sample:
    network: network-1001
    name: VM Network
    type: STANDARD_PORTGROUP
  type: raw
info:
  description: A list of networks matching the query.
  returned: On success.
  sample:
    - network: network-1001
      name: VM Network
      type: STANDARD_PORTGROUP
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
ITEM_ENDPOINT = "/vcenter/network"


GET_OPERATION = OperationConfig(
    name="get",
    uri=ITEM_ENDPOINT,
    http_method="GET",
    query_spec={
        "networks": {
            "required": False,
        },
        "names": {
            "required": False,
        },
        "types": {
            "required": False,
        },
        "folders": {
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
    module_args["networks"] = {
        "type": "list",
        "elements": "str",
    }
    module_args["types"] = {
        "type": "list",
        "aliases": ["filter_types"],
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
