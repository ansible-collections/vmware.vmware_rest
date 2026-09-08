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
module: content_subscribedlibrary_info
short_description: Gather information about vCenter subscribed content libraries.
description:
  - Retrieve information about the subscribed content libraries defined in vCenter.
  - A subscribed library synchronizes its content from a published library, which may reside on the
    same or a different vCenter Server.
  - When O(library_id) is provided, return the full details of that single subscribed library, such as
    its name, description, storage backings, and subscription settings.
  - When O(library_id) is omitted, list every subscribed content library available in the Content Library.
  - This module is read-only and does not create, modify, or delete any libraries.

author:
  - Ansible Eco Content Team (@eco-ansible-content)

extends_documentation_fragment:
  - vmware.vmware_rest.connection_params

options:
  library_id:
    description:
      - The identifier of the subscribed content library to retrieve detailed information for.
      - When omitted, information about all subscribed content libraries is returned.
      - The value must be the identifier (MOID) of an existing subscribed content library.
    type: str
    required: false

version_added: 5.0.0

requirements: []

notes:
  - Generated from vSphere API spec 9.1.0.
"""

EXAMPLES = r"""
- name: List all subscribed content libraries
  vmware.vmware_rest.content_subscribedlibrary_info:
  register: all_subscribed_libraries

- name: Get information about a single subscribed content library
  vmware.vmware_rest.content_subscribedlibrary_info:
    library_id: 3393956a-43ed-4e7f-bd96-eb39bd604445
  register: my_subscribed_library

- name: Display the subscription URL of the queried library
  ansible.builtin.debug:
    var: my_subscribed_library.value.subscription_info.subscription_url
"""

RETURN = r"""
id:
  description: The identifier (MOID) of the subscribed content library that was queried.
  returned: When only one library, identified by O(library_id), was queried
  sample: 3393956a-43ed-4e7f-bd96-eb39bd604445
  type: str
value:
  description: Detailed information about a single subscribed content library.
  returned: When only one library, identified by O(library_id), was queried
  sample:
    id: 3393956a-43ed-4e7f-bd96-eb39bd604445
    name: my_subscribed_library
    description: Mirror of the published library
    type: SUBSCRIBED
    creation_time: "2026-01-16T08:05:11.134Z"
    last_modified_time: "2026-01-16T08:05:11.134Z"
    last_sync_time: "2026-01-16T09:10:42.512Z"
    version: "2"
    server_guid: 52fb0b5e-ffc3-465b-bf4f-e4e6d5423cf5
    storage_backings:
      - datastore_id: datastore-1013
        type: DATASTORE
    subscription_info:
      authentication_method: NONE
      automatic_sync_enabled: true
      on_demand: false
      subscription_url: https://vcenter.test:443/cls/vcsp/lib/e6d5c7a1-5a52-4a3b-9c1e-8f0b2d3a4b5c/lib.json
  type: dict
info:
  description: A list of detailed information about all subscribed content libraries.
  returned: When O(library_id) is not provided
  elements: dict
  sample:
    - id: 3393956a-43ed-4e7f-bd96-eb39bd604445
      name: my_subscribed_library
      description: Mirror of the published library
      type: SUBSCRIBED
      creation_time: "2026-01-16T08:05:11.134Z"
      last_modified_time: "2026-01-16T08:05:11.134Z"
      last_sync_time: "2026-01-16T09:10:42.512Z"
      version: "2"
    - id: b4c5d6e7-8f90-4a1b-9c2d-3e4f5a6b7c8d
      name: remote_templates
      description: Templates synced from the datacenter library
      type: SUBSCRIBED
      creation_time: "2026-01-17T11:30:00.000Z"
      last_modified_time: "2026-01-17T11:30:00.000Z"
      version: "5"
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

LIST_ENDPOINT = "/content/subscribed-library"
ITEM_ENDPOINT = "/content/subscribed-library/{library_id}"


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
