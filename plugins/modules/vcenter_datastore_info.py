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
short_description: Gather information about vCenter datastores.
description:
  - Retrieve information about one or more VMware vCenter datastores.
  - Can return a list of all datastores or detailed information about a specific datastore
    identified by its MOID.
  - Use the filter parameters to narrow results by datastore name, identifier, type, folder,
    or datacenter.

author:
  - Ansible Eco Content Team (@eco-ansible-content)

extends_documentation_fragment:
  - vmware.vmware_rest.connection_params

options:
  datastore:
    description:
      - Identifier of the datastore to retrieve details for.
      - Must be an identifier (MOID) for a C(Datastore) resource.
    type: str
    required: false
  datastores:
    description:
      - A list of datastore MOIDs to filter the results.
      - Only datastores whose identifiers appear in this list will be returned.
      - If omitted or empty, datastores with any identifier are returned.
    type: list
    required: false
    elements: str
  names:
    aliases:
      - filter_names
    description:
      - A list of datastore names to filter the results.
      - Only datastores whose names appear in this list will be returned.
      - If omitted or empty, datastores with any name are returned.
    type: list
    required: false
    elements: str
  types:
    aliases:
      - filter_types
    description:
      - A list of datastore types to filter the results.
      - Only datastores of one of the listed types will be returned.
      - If omitted or empty, datastores of any type are returned.
      - Valid types are the following.
      - VMFS - VMware File System (ESX Server only).
      - NFS - Network file system v3 (linux & esx servers only).
      - NFS41 - Network file system v4.1 (linux & esx servers only).
      - CIFS - Common Internet File System.
      - VSAN - Virtual SAN (ESX Server only).
      - VFFS - Flash Read Cache (ESX Server only).
      - VVOL - vSphere Virtual Volume (ESX Server only).
    type: list
    required: false
    elements: str
  folders:
    aliases:
      - filter_folders
    description:
      - A list of folder MOIDs to filter the results.
      - Only datastores that reside in the specified folders will be returned.
      - If omitted or empty, datastores in any folder are returned.
    type: list
    required: false
    elements: str
  datacenters:
    aliases:
      - filter_datacenters
    description:
      - A list of datacenter MOIDs to filter the results.
      - Only datastores that reside in the specified datacenters will be returned.
      - If omitted or empty, datastores in any datacenter are returned.
    type: list
    required: false
    elements: str

version_added: 5.0.0

requirements: []

notes:
  - Generated from vSphere API spec 9.1.0.
"""

EXAMPLES = r"""
- name: List all datastores
  vmware.vmware_rest.vcenter_datastore_info:
  register: all_datastores

- name: Get details about a specific datastore
  vmware.vmware_rest.vcenter_datastore_info:
    datastore: datastore-1001
  register: my_datastore

- name: Filter datastores by name
  vmware.vmware_rest.vcenter_datastore_info:
    names:
      - my_datastore
  register: filtered_datastores

- name: Filter VMFS and NFS datastores in a specific datacenter
  vmware.vmware_rest.vcenter_datastore_info:
    types:
      - VMFS
      - NFS
    datacenters:
      - datacenter-1001
  register: filtered_datastores
"""

RETURN = r"""
id:
  description: MOID of the queried datastore.
  returned: When only one resource, with a MOID, was queried.
  sample: datastore-1001
  type: str
value:
  description:
    - Raw output from the API response.
    - This output is maintained for consistency with version 4.x and earlier of this collection.
      It is recommended to switch to the info return key for a more consistent and documented output.
  returned: On success.
  sample:
    name: my_datastore
    type: VMFS
    accessible: true
    free_space: 32204521472
    multiple_host_access: true
    thin_provisioning_supported: true
  type: raw
info:
  description: A list of datastores matching the query.
  returned: On success.
  sample:
    - datastore: datastore-1001
      name: my_datastore
      type: VMFS
      free_space: 32204521472
      capacity: 53687091200
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

MOID_PARAMETER_HINTS = ["datastore"]

LIST_ENDPOINT = "/vcenter/datastore"
ITEM_ENDPOINT = "/vcenter/datastore/{datastore}"


LIST_OPERATION = OperationConfig(
    name="list",
    uri=LIST_ENDPOINT,
    http_method="GET",
    query_spec={
        "datastores": {
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

GET_OPERATION = OperationConfig(
    name="get",
    uri=ITEM_ENDPOINT,
    http_method="GET",
)


def create_module_argument_spec() -> dict:
    module_args = connection_params_argument_spec()
    module_args["datacenters"] = {
        "type": "list",
        "aliases": ["filter_datacenters"],
        "elements": "str",
    }
    module_args["datastore"] = {
        "type": "str",
    }
    module_args["datastores"] = {
        "type": "list",
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
        list_operation_config=LIST_OPERATION,
    )
    try:
        result = info_module.get_resource_info()
    except VmwareModuleError as e:
        module.fail_json(**e.to_module_fail_json_output())
    module.exit_json(**result)


if __name__ == "__main__":
    main()
