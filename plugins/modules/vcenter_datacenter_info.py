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
module: vcenter_datacenter_info
short_description: Get information about vCenter datacenters.
description:
  - Returns information about datacenters in vCenter Server.
  - When I(datacenter) is specified, returns information for that datacenter only.
  - When I(datacenter) is omitted, lists datacenters matching the optional filters and
    returns detailed information for each match.
author:
  - Ansible Eco Content Team (@eco-ansible-content)
extends_documentation_fragment:
  - vmware.vmware_rest.connection_params
options:
  datacenter:
    description:
      - Identifier of the datacenter to retrieve.
      - Must be an identifier (MOID) for a C(Datacenter) resource.
      - When specified, only that datacenter is returned.
    type: str
  datacenters:
    description:
      - Identifiers of datacenters that can match the filter.
      - Each element must be an identifier (MOID) for a C(Datacenter) resource.
      - When omitted or empty, datacenters with any identifier match the filter.
    type: list
    elements: str
  names:
    description:
      - Names that datacenters must have to match the filter.
      - When omitted or empty, datacenters with any name match the filter.
    type: list
    elements: str
  folders:
    description:
      - Folders that must contain the datacenters for the datacenter to match the filter.
      - Each element must be an identifier (MOID) for a C(Folder) resource.
      - When omitted or empty, datacenters in any folder match the filter.
    type: list
    elements: str
version_added: 4.11.0
requirements: []
notes:
  - Generated from vSphere API spec 9.1.0.
  - Has support for vSphere API 7.0.3.
  - Has support for vSphere API 8.0.2.
"""

EXAMPLES = r"""
- name: List all datacenters
  vmware.vmware_rest.vcenter_datacenter_info:
  register: datacenters

- name: Get a datacenter by MOID
  vmware.vmware_rest.vcenter_datacenter_info:
    datacenter: datacenter-1001
  register: datacenter_info

- name: List datacenters matching a name filter
  vmware.vmware_rest.vcenter_datacenter_info:
    names:
      - Eco-Datacenter
  register: filtered_datacenters
"""

RETURN = r"""
value:
  description:
    - Datacenter information.
    - Returns a list of datacenter dictionaries when I(datacenter) is omitted.
    - Returns a single datacenter dictionary when I(datacenter) is specified.
  returned: On success
  type: raw
  sample:
    - datacenter: datacenter-1001
      name: Eco-Datacenter
      datastore_folder: group-d1
      host_folder: group-h1
      network_folder: group-n1
      vm_folder: group-v1
  contains:
    datacenter:
      description:
        - Identifier of the datacenter.
        - Must be an identifier (MOID) for a C(Datacenter) resource.
      type: str
      sample: datacenter-1001
    name:
      description:
        - Name of the datacenter.
      type: str
      sample: Eco-Datacenter
    datastore_folder:
      description:
        - Root datastore folder associated with the datacenter.
        - Must be an identifier (MOID) for a C(Folder) resource.
      type: str
      sample: group-d1
    host_folder:
      description:
        - Root host and cluster folder associated with the datacenter.
        - Must be an identifier (MOID) for a C(Folder) resource.
      type: str
      sample: group-h1
    network_folder:
      description:
        - Root network folder associated with the datacenter.
        - Must be an identifier (MOID) for a C(Folder) resource.
      type: str
      sample: group-n1
    vm_folder:
      description:
        - Root virtual machine folder associated with the datacenter.
        - Must be an identifier (MOID) for a C(Folder) resource.
      type: str
      sample: group-v1
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

LIST_PATH = "/vcenter/datacenter"
DATACENTER_PATH = "/vcenter/datacenter/{datacenter}"


class VmwareRestInfoModule(VmwareRestInfoModuleBase):
    PAYLOAD_FORMAT = {
        "list": {
            "query": {
                "datacenters": "datacenters",
                "names": "names",
                "folders": "folders",
            },
            "body": {},
            "path": {},
        },
        "get": {
            "query": {},
            "body": {},
            "path": {"datacenter": "datacenter"},
        },
    }

    def _get_datacenter(self, datacenter, fail_if_missing=False):
        path = self.build_path(DATACENTER_PATH, {"datacenter": datacenter})
        response = self.client.get(path)
        if response.status == 404:
            if fail_if_missing:
                self.client.error_handler.handle_request_error(
                    exception=UnexpectedAPIResponse(response.status, response.data),
                    method="GET",
                    path=path,
                    request_kwargs={},
                )
            return None

        info = response.json
        info["datacenter"] = datacenter
        return info

    def get_info(self):
        datacenter = self.params.get("datacenter")
        if datacenter:
            return self._get_datacenter(datacenter, fail_if_missing=True)

        query = self.build_query(self.PAYLOAD_FORMAT["list"])
        response = self.client.get(LIST_PATH, query=query or None)
        if response.status == 404:
            return []

        summaries = normalize_list_response(response.json)
        result = []
        for summary in summaries:
            datacenter_id = summary.get("datacenter")
            if not datacenter_id:
                continue
            info = self._get_datacenter(datacenter_id)
            if info is not None:
                result.append(info)
        return result


def main():
    module_args = connection_params_argument_spec()
    module_args["datacenter"] = {"type": "str"}
    module_args["datacenters"] = {"type": "list", "elements": "str"}
    module_args["names"] = {"type": "list", "elements": "str"}
    module_args["folders"] = {"type": "list", "elements": "str"}

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
    )

    info_module = VmwareRestInfoModule(module)
    result = info_module.get_info()
    module.exit_json(value=result)


if __name__ == "__main__":
    main()
