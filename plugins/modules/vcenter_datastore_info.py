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
module: vcenter_datastore_info
short_description: Retrieves information about datastores in vCenter.
description:
  - Retrieves information about datastores in vCenter.
  - When I(datastore) is set, returns information about that datastore.
  - When I(datastore) is not set, lists datastores matching the filter options
    and returns detailed information for each match.
author:
  - Ansible Eco Content Team (@eco-ansible-content)
extends_documentation_fragment:
  - vmware.vmware_rest.connection_params
options:
  datastore:
    description:
      - Identifier of the datastore to retrieve.
      - Must be an identifier (MOID) for a C(Datastore) resource.
    type: str
  datastores:
    description:
      - Identifiers of datastores that can match the filter.
      - If not set, datastores with any identifier match the filter.
      - Each element must be an identifier (MOID) for a C(Datastore) resource.
    type: list
    elements: str
    aliases:
      - filter_datastores
  names:
    description:
      - Names that datastores must have to match the filter.
      - If not set, datastores with any name match the filter.
    type: list
    elements: str
    aliases:
      - filter_names
  types:
    description:
      - Types that datastores must have to match the filter.
      - If not set, datastores with any type match the filter.
    type: list
    elements: str
    choices:
      - VMFS
      - NFS
      - NFS41
      - CIFS
      - VSAN
      - VFFS
      - VVOL
    aliases:
      - filter_types
  folders:
    description:
      - Folders that must contain the datastore for it to match the filter.
      - If not set, datastores in any folder match the filter.
      - Each element must be an identifier (MOID) for a C(Folder) resource.
    type: list
    elements: str
    aliases:
      - filter_folders
  datacenters:
    description:
      - Datacenters that must contain the datastore for it to match the filter.
      - If not set, datastores in any datacenter match the filter.
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
- name: List all datastores
  vmware.vmware_rest.vcenter_datastore_info:
  register: datastores

- name: Get a specific datastore
  vmware.vmware_rest.vcenter_datastore_info:
    datastore: datastore-1001
  register: datastore_info

- name: List VMFS datastores
  vmware.vmware_rest.vcenter_datastore_info:
    types:
      - VMFS
  register: vmfs_datastores
"""

RETURN = r"""
value:
  description:
    - List of datastore information objects.
  returned: On success
  type: list
  elements: dict
  sample:
    - id: datastore-1001
      name: shared_vmfs
      type: VMFS
      accessible: true
      free_space: 107374182400
      multiple_host_access: true
      thin_provisioning_supported: true
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.vmware.vmware_rest.plugins.module_utils._argument_spec import (
    connection_params_argument_spec,
)
from ansible_collections.vmware.vmware_rest.plugins.module_utils._module_base import (
    VmwareRestInfoModuleBase,
)

LIST_PATH = "/vcenter/datastore"
ITEM_PATH = "/vcenter/datastore/{datastore}"


class VmwareRestInfoModule(VmwareRestInfoModuleBase):
    PAYLOAD_FORMAT = {
        "get": {"query": {}, "body": {}, "path": {"datastore": "datastore"}},
        "list": {
            "query": {
                "datastores": "datastores",
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
        if self.params.get("datastore"):
            return [self._get_datastore(self.params["datastore"])]

        summaries = self._list_datastores()
        result = []
        for summary in summaries:
            datastore_id = summary["datastore"]
            info = self._get_datastore(datastore_id)
            result.append(info)
        return result

    def _list_datastores(self):
        return self.fetch_list(LIST_PATH, self.PAYLOAD_FORMAT["list"])

    def _get_datastore(self, datastore_id):
        path = self.build_path(ITEM_PATH, {"datastore": datastore_id})
        response = self.client.get(path)
        if response.status == 404:
            return {}

        info = response.json
        if "id" not in info:
            info["id"] = datastore_id
        return info


def main():
    module_args = connection_params_argument_spec()
    module_args["datastore"] = {"type": "str"}
    module_args["datastores"] = {
        "type": "list",
        "elements": "str",
        "aliases": ["filter_datastores"],
    }
    module_args["names"] = {
        "type": "list",
        "elements": "str",
        "aliases": ["filter_names"],
    }
    module_args["types"] = {
        "type": "list",
        "elements": "str",
        "choices": ["VMFS", "NFS", "NFS41", "CIFS", "VSAN", "VFFS", "VVOL"],
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
