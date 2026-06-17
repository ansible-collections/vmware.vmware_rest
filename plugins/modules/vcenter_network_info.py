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
module: vcenter_network_info
short_description: List vCenter networks matching filter criteria.
description:
  - Returns information about at most 1000 visible networks in vCenter Server matching
    the filter criteria.
  - Results are subject to permission checks on the vCenter Server.
author:
  - Ansible Eco Content Team (@eco-ansible-content)
extends_documentation_fragment:
  - vmware.vmware_rest.connection_params
options:
  networks:
    description:
      - Identifiers of networks that can match the filter.
      - When omitted or empty, networks with any identifier match the filter.
      - Each element must be an identifier (MOID) for a C(Network) resource.
    type: list
    elements: str
  names:
    description:
      - Names that networks must have to match the filter.
      - When omitted or empty, networks with any name match the filter.
    type: list
    elements: str
    aliases:
      - filter_names
  types:
    description:
      - Types that networks must have to match the filter.
      - When omitted, networks with any type match the filter.
    type: list
    elements: str
    choices:
      - STANDARD_PORTGROUP
      - DISTRIBUTED_PORTGROUP
      - OPAQUE_NETWORK
    aliases:
      - filter_types
  folders:
    description:
      - Folders that must contain the network for the network to match the filter.
      - When omitted or empty, networks in any folder match the filter.
      - Each element must be an identifier (MOID) for a C(Folder) resource.
    type: list
    elements: str
    aliases:
      - filter_folders
  datacenters:
    description:
      - Datacenters that must contain the network for the network to match the filter.
      - When omitted or empty, networks in any datacenter match the filter.
      - Each element must be an identifier (MOID) for a C(Datacenter) resource.
    type: list
    elements: str
    aliases:
      - filter_datacenters
version_added: 4.11.0
requirements: []
notes:
  - Generated from vSphere API spec 9.1.0.
  - Has support for vSphere API 7.0.3.
  - Has support for vSphere API 8.0.2.
"""

EXAMPLES = r"""
- name: List all vCenter networks
  vmware.vmware_rest.vcenter_network_info:
  register: networks

- name: List distributed port groups named my-portgroup
  vmware.vmware_rest.vcenter_network_info:
    types:
      - DISTRIBUTED_PORTGROUP
    names:
      - my-portgroup
  register: my_portgroup
"""

RETURN = r"""
value:
  description:
    - List of network summary objects matching the filter.
  returned: On success
  type: list
  elements: dict
  sample:
    - name: VM Network
      network: network-1016
      type: STANDARD_PORTGROUP
    - name: my-portgroup
      network: dvportgroup-1022
      type: DISTRIBUTED_PORTGROUP
  contains:
    network:
      description:
        - Identifier of the network.
        - Must be an identifier (MOID) for a C(Network) resource.
      type: str
      sample: network-1016
    name:
      description:
        - Name of the network.
      type: str
      sample: VM Network
    type:
      description:
        - Type of the vCenter Server network.
      type: str
      choices:
        - STANDARD_PORTGROUP
        - DISTRIBUTED_PORTGROUP
        - OPAQUE_NETWORK
      sample: STANDARD_PORTGROUP
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.vmware.vmware_rest.plugins.module_utils._argument_spec import (
    connection_params_argument_spec,
)
from ansible_collections.vmware.vmware_rest.plugins.module_utils._module_base import (
    VmwareRestInfoModuleBase,
    normalize_list_response,
)

LIST_PATH = "/vcenter/network"


class VmwareRestInfoModule(VmwareRestInfoModuleBase):
    PAYLOAD_FORMAT = {
        "list": {
            "query": {
                "networks": "networks",
                "names": "names",
                "types": "types",
                "folders": "folders",
                "datacenters": "datacenters",
            },
            "body": {},
            "path": {},
        },
    }

    def get_info(self):
        query = self.build_query(self.PAYLOAD_FORMAT["list"])
        response = self.client.get(LIST_PATH, query=query or None)
        if response.status == 404:
            return []
        return normalize_list_response(response.json)


def main():
    module_args = connection_params_argument_spec()
    module_args["networks"] = {"type": "list", "elements": "str"}
    module_args["names"] = {
        "type": "list",
        "elements": "str",
        "aliases": ["filter_names"],
    }
    module_args["types"] = {
        "type": "list",
        "elements": "str",
        "choices": ["STANDARD_PORTGROUP", "DISTRIBUTED_PORTGROUP", "OPAQUE_NETWORK"],
        "aliases": ["filter_types"],
    }
    module_args["folders"] = {
        "type": "list",
        "elements": "str",
        "aliases": ["filter_folders"],
    }
    module_args["datacenters"] = {
        "type": "list",
        "elements": "str",
        "aliases": ["filter_datacenters"],
    }

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
    )

    info_module = VmwareRestInfoModule(module)
    result = info_module.get_info()
    module.exit_json(value=result)


if __name__ == "__main__":
    main()
