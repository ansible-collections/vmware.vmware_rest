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
short_description: Get information about vCenter folders.
description:
  - Returns information about folders in vCenter Server.
  - When I(folder) is specified, returns information for that folder only.
  - When I(folder) is omitted, lists folders matching the optional filters.
author:
  - Ansible Eco Content Team (@eco-ansible-content)
extends_documentation_fragment:
  - vmware.vmware_rest.connection_params
options:
  folder:
    description:
      - Identifier of the folder to retrieve.
      - Must be an identifier (MOID) for a C(Folder) resource.
      - When specified, only that folder is returned.
    type: str
  folders:
    description:
      - Identifiers of folders that can match the filter.
      - Each element must be an identifier (MOID) for a C(Folder) resource.
      - When omitted or empty, folders with any identifier match the filter.
    type: list
    elements: str
  names:
    description:
      - Names that folders must have to match the filter.
      - When omitted or empty, folders with any name match the filter.
    type: list
    elements: str
  parent_folders:
    description:
      - Folders that must contain the folder for the folder to match the filter.
      - Each element must be an identifier (MOID) for a C(Folder) resource.
      - When omitted or empty, folders in any parent folder match the filter.
    type: list
    elements: str
  datacenters:
    description:
      - Datacenters that must contain the folder for the folder to match the filter.
      - Each element must be an identifier (MOID) for a C(Datacenter) resource.
      - When omitted or empty, folders in any datacenter match the filter.
    type: list
    elements: str
  type:
    description:
      - Folder type that folders must have to match the filter.
    type: str
    choices:
      - DATACENTER
      - DATASTORE
      - HOST
      - NETWORK
      - VIRTUAL_MACHINE
version_added: 4.11.0
requirements: []
notes:
  - Generated from vSphere API spec 9.1.0.
  - Has support for vSphere API 7.0.3.
  - Has support for vSphere API 8.0.2.
"""

EXAMPLES = r"""
- name: List all folders
  vmware.vmware_rest.vcenter_folder_info:
  register: folders

- name: Get a folder by MOID
  vmware.vmware_rest.vcenter_folder_info:
    folder: group-v42
  register: folder_info

- name: List virtual machine folders matching a name filter
  vmware.vmware_rest.vcenter_folder_info:
    type: VIRTUAL_MACHINE
    names:
      - vm
  register: vm_folders
"""

RETURN = r"""
value:
  description:
    - Folder information.
    - Returns a list of folder dictionaries when I(folder) is omitted.
    - Returns a single folder dictionary when I(folder) is specified.
  returned: On success
  type: raw
  sample:
    - folder: group-v42
      name: vm
      type: VIRTUAL_MACHINE
  contains:
    folder:
      description:
        - Identifier of the folder.
        - Must be an identifier (MOID) for a C(Folder) resource.
      type: str
      sample: group-v42
    name:
      description:
        - Name of the vCenter Server folder.
      type: str
      sample: vm
    type:
      description:
        - Type of the vCenter Server folder.
      type: str
      sample: VIRTUAL_MACHINE
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

LIST_PATH = "/vcenter/folder"


class VmwareRestInfoModule(VmwareRestInfoModuleBase):
    PAYLOAD_FORMAT = {
        "list": {
            "query": {
                "folders": "folders",
                "names": "names",
                "parent_folders": "parent_folders",
                "datacenters": "datacenters",
                "type": "type",
            },
            "body": {},
            "path": {},
        },
    }

    def get_info(self):
        folder = self.params.get("folder")
        query = self.build_query(self.PAYLOAD_FORMAT["list"])
        if folder:
            query["folders"] = [folder]

        response = self.client.get(LIST_PATH, query=query or None)
        if response.status == 404:
            if folder:
                self.client.error_handler.handle_request_error(
                    exception=UnexpectedAPIResponse(response.status, response.data),
                    method="GET",
                    path=LIST_PATH,
                    request_kwargs={"query": query},
                )
            return []

        result = normalize_list_response(response.json)
        if folder:
            for item in result:
                if item.get("folder") == folder:
                    return item
            self.module.fail_json(msg="Folder '{0}' was not found.".format(folder))

        return result


def main():
    module_args = connection_params_argument_spec()
    module_args["folder"] = {"type": "str"}
    module_args["folders"] = {"type": "list", "elements": "str"}
    module_args["names"] = {"type": "list", "elements": "str"}
    module_args["parent_folders"] = {"type": "list", "elements": "str"}
    module_args["datacenters"] = {"type": "list", "elements": "str"}
    module_args["type"] = {
        "type": "str",
        "choices": [
            "DATACENTER",
            "DATASTORE",
            "HOST",
            "NETWORK",
            "VIRTUAL_MACHINE",
        ],
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
