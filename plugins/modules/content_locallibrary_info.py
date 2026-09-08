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
module: content_locallibrary_info
short_description: Gather information about vCenter local content libraries.
description:
  - Retrieve information about the local content libraries defined in vCenter.
  - A local library stores its content on this vCenter Server and can optionally be published so that
    other vCenter Servers can subscribe to it.
  - When O(library_id) is provided, return the full details of that single local library, such as its
    name, description, storage backings, and publish settings.
  - When O(library_id) is omitted, list every local content library available in the Content Library.
  - This module is read-only and does not create, modify, or delete any libraries.

author:
  - Ansible Eco Content Team (@eco-ansible-content)

extends_documentation_fragment:
  - vmware.vmware_rest.connection_params

options:
  library_id:
    description:
      - The identifier of the local content library to retrieve detailed information for.
      - When omitted, information about all local content libraries is returned.
      - The value must be the identifier (MOID) of an existing local content library.
    type: str
    required: false

version_added: 5.0.0

requirements: []

notes:
  - Generated from vSphere API spec 9.1.0.
"""

EXAMPLES = r"""
- name: List all local content libraries
  vmware.vmware_rest.content_locallibrary_info:
  register: all_local_libraries

- name: Get information about a single local content library
  vmware.vmware_rest.content_locallibrary_info:
    library_id: e6d5c7a1-5a52-4a3b-9c1e-8f0b2d3a4b5c
  register: my_local_library

- name: Display the name of the queried local library
  ansible.builtin.debug:
    var: my_local_library.value.name
"""

RETURN = r"""
id:
  description: The identifier (MOID) of the local content library that was queried.
  returned: When only one library, identified by O(library_id), was queried
  sample: e6d5c7a1-5a52-4a3b-9c1e-8f0b2d3a4b5c
  type: str
value:
  description: Detailed information about a single local content library.
  returned: When only one library, identified by O(library_id), was queried
  sample:
    id: e6d5c7a1-5a52-4a3b-9c1e-8f0b2d3a4b5c
    name: my_local_library
    description: Automated content library
    type: LOCAL
    creation_time: "2026-01-15T10:22:00.940Z"
    last_modified_time: "2026-01-15T10:22:00.940Z"
    version: "1"
    server_guid: 52fb0b5e-ffc3-465b-bf4f-e4e6d5423cf5
    storage_backings:
      - datastore_id: datastore-1013
        type: DATASTORE
    publish_info:
      published: true
      authentication_method: NONE
      publish_url: https://vcenter.test:443/cls/vcsp/lib/e6d5c7a1-5a52-4a3b-9c1e-8f0b2d3a4b5c/lib.json
  type: dict
info:
  description: A list of detailed information about all local content libraries.
  returned: When O(library_id) is not provided
  elements: dict
  sample:
    - id: e6d5c7a1-5a52-4a3b-9c1e-8f0b2d3a4b5c
      name: my_local_library
      description: Automated content library
      type: LOCAL
      creation_time: "2026-01-15T10:22:00.940Z"
      last_modified_time: "2026-01-15T10:22:00.940Z"
      version: "1"
    - id: 7f2a1b3c-9d4e-4a5b-8c6d-2e3f4a5b6c7d
      name: templates_library
      description: Shared VM templates
      type: LOCAL
      creation_time: "2026-01-16T08:05:11.134Z"
      last_modified_time: "2026-01-16T08:05:11.134Z"
      version: "3"
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

MOID_PARAMETER_HINTS = ["library_id"]

LIST_ENDPOINT = "/content/local-library"
ITEM_ENDPOINT = "/content/local-library/{library_id}"


LIST_OPERATION = OperationConfig(
    name="list",
    uri=LIST_ENDPOINT,
    http_method="GET",
)

GET_OPERATION = OperationConfig(
    name="get",
    uri=ITEM_ENDPOINT,
    http_method="GET",
)


def create_module_argument_spec() -> dict:
    module_args = connection_params_argument_spec()
    module_args["library_id"] = {
        "type": "str",
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
