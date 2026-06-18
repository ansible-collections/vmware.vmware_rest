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
module: vcenter_host_info
short_description: Get information about vCenter hosts.
description:
  - Returns information about hosts in vCenter Server.
  - When I(host) is specified, returns information for that host only.
  - When I(host) is omitted, lists hosts matching the optional filters.
author:
  - Ansible Eco Content Team (@eco-ansible-content)
extends_documentation_fragment:
  - vmware.vmware_rest.connection_params
options:
  host:
    description:
      - Identifier of the host to retrieve.
      - Must be an identifier (MOID) for a C(HostSystem) resource.
      - When specified, only that host is returned.
    type: str
  hosts:
    description:
      - Identifiers of hosts that can match the filter.
      - Each element must be an identifier (MOID) for a C(HostSystem) resource.
      - When omitted or empty, hosts with any identifier match the filter.
    type: list
    elements: str
  names:
    description:
      - Names that hosts must have to match the filter.
      - When omitted or empty, hosts with any name match the filter.
    type: list
    elements: str
  folders:
    description:
      - Folders that must contain the hosts for the hosts to match the filter.
      - Each element must be an identifier (MOID) for a C(Folder) resource.
      - When omitted or empty, hosts in any folder match the filter.
    type: list
    elements: str
  datacenters:
    description:
      - Datacenters that must contain the hosts for the hosts to match the filter.
      - Each element must be an identifier (MOID) for a C(Datacenter) resource.
      - When omitted or empty, hosts in any datacenter match the filter.
    type: list
    elements: str
  clusters:
    description:
      - Clusters that must contain the hosts for the hosts to match the filter.
      - Each element must be an identifier (MOID) for a C(ClusterComputeResource) resource.
      - When omitted or empty, hosts in any cluster and hosts that are not in a cluster match the filter.
      - If this option is not empty and I(standalone) is C(true), no hosts match the filter.
    type: list
    elements: str
  connection_states:
    description:
      - Connection states that a host must be in to match the filter.
    type: list
    elements: str
    choices:
      - CONNECTED
      - DISCONNECTED
      - NOT_RESPONDING
  host_uuids:
    description:
      - UUIDs of hosts that can match the filter.
      - Maps to UUID in SMBIOS System Information (Type 1) at offset 08h.
      - When omitted or empty, hosts with any UUID match the filter.
    type: list
    elements: str
  standalone:
    description:
      - When C(true), only hosts that are not part of a cluster can match the filter.
      - When C(false), only hosts that are part of a cluster can match the filter.
      - When omitted, hosts can match the filter independent of cluster membership.
      - If I(clusters) is not empty and this option is C(true), no hosts match the filter.
    type: bool
version_added: 4.11.0
requirements: []
notes:
  - Generated from vSphere API spec 9.1.0.
  - Has support for vSphere API 7.0.3.
  - Has support for vSphere API 8.0.2.
"""

EXAMPLES = r"""
- name: List all hosts
  vmware.vmware_rest.vcenter_host_info:
  register: hosts

- name: Get a host by MOID
  vmware.vmware_rest.vcenter_host_info:
    host: host-42
  register: host_info

- name: List connected standalone hosts
  vmware.vmware_rest.vcenter_host_info:
    standalone: true
    connection_states:
      - CONNECTED
  register: standalone_hosts
"""

RETURN = r"""
value:
  description:
    - Host information.
    - Returns a list of host dictionaries when I(host) is omitted.
    - Returns a single host dictionary when I(host) is specified.
  returned: On success
  type: raw
  sample:
    - host: host-42
      name: esxi01.example.com
      connection_state: CONNECTED
      power_state: POWERED_ON
      host_uuid: 42000000-0000-0000-0000-000000000000
  contains:
    host:
      description:
        - Identifier of the host.
        - Must be an identifier (MOID) for a C(HostSystem) resource.
      type: str
      sample: host-42
    name:
      description:
        - Name of the host.
      type: str
      sample: esxi01.example.com
    connection_state:
      description:
        - Connection status of the host.
      type: str
      sample: CONNECTED
    power_state:
      description:
        - Power state of the host.
        - Present only when I(connection_state) is C(CONNECTED).
      type: str
      sample: POWERED_ON
    host_uuid:
      description:
        - UUID of the host.
      type: str
      sample: 42000000-0000-0000-0000-000000000000
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.vmware.vmware_rest.plugins.module_utils._argument_spec import (
    connection_params_argument_spec,
)
from ansible_collections.vmware.vmware_rest.plugins.module_utils._errors import (
    UnexpectedAPIResponse,
)
from ansible_collections.vmware.vmware_rest.plugins.module_utils._module_base import (
    VmwareRestInfoModuleBase,
    normalize_list_response,
)

LIST_PATH = "/vcenter/host"


class VmwareRestInfoModule(VmwareRestInfoModuleBase):
    PAYLOAD_FORMAT = {
        "list": {
            "query": {
                "hosts": "hosts",
                "names": "names",
                "folders": "folders",
                "datacenters": "datacenters",
                "clusters": "clusters",
                "connection_states": "connection_states",
                "host_uuids": "host_uuids",
                "standalone": "standalone",
            },
            "body": {},
            "path": {},
        },
    }

    def get_info(self):
        host = self.params.get("host")
        query = self.build_query(self.PAYLOAD_FORMAT["list"])
        if host:
            query["hosts"] = [host]

        response = self.client.get(LIST_PATH, query=query or None)
        if response.status == 404:
            if host:
                self.client.error_handler.handle_request_error(
                    exception=UnexpectedAPIResponse(response.status, response.data),
                    method="GET",
                    path=LIST_PATH,
                    request_kwargs={"query": query},
                )
            return []

        result = normalize_list_response(response.json)
        if host:
            for item in result:
                if item.get("host") == host:
                    return item
            self.module.fail_json(msg="Host '{0}' was not found.".format(host))

        return result


def main():
    module_args = connection_params_argument_spec()
    module_args["host"] = {"type": "str"}
    module_args["hosts"] = {"type": "list", "elements": "str"}
    module_args["names"] = {"type": "list", "elements": "str"}
    module_args["folders"] = {"type": "list", "elements": "str"}
    module_args["datacenters"] = {"type": "list", "elements": "str"}
    module_args["clusters"] = {"type": "list", "elements": "str"}
    module_args["connection_states"] = {
        "type": "list",
        "elements": "str",
        "choices": ["CONNECTED", "DISCONNECTED", "NOT_RESPONDING"],
    }
    module_args["host_uuids"] = {"type": "list", "elements": "str"}
    module_args["standalone"] = {"type": "bool"}

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
    )

    info_module = VmwareRestInfoModule(module)
    result = info_module.get_info()
    module.exit_json(value=result)


if __name__ == "__main__":
    main()
