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
module: content_library_subscriptions_info
short_description: Gather information about the subscriptions of a published content library.
description:
  - Retrieve information about the subscriptions of a published content library, that is, the
    subscribed libraries that receive content from a given published library.
  - When O(subscription) is provided, return the details of that single subscription, including the
    subscribed library and the vCenter Server instance and placement where it resides.
  - When O(subscription) is omitted, list every subscription of the published library identified by
    O(library).
  - This module is read-only and does not create, modify, or delete any subscriptions.

author:
  - Ansible Eco Content Team (@eco-ansible-content)

extends_documentation_fragment:
  - vmware.vmware_rest.connection_params

options:
  library:
    description:
      - The identifier of the published content library whose subscriptions you want to query.
      - The value must be the identifier (MOID) of an existing published content library.
    type: str
    required: true
  subscription:
    description:
      - The identifier of a single subscription to retrieve detailed information for.
      - When omitted, information about all subscriptions of the library is returned.
      - The value must be the identifier (MOID) of an existing subscription.
    type: str
    required: false

version_added: 5.0.0

requirements: []

notes:
  - Generated from vSphere API spec 9.1.0.
"""

EXAMPLES = r"""
- name: List all subscriptions of a published library
  vmware.vmware_rest.content_library_subscriptions_info:
    library: e6d5c7a1-5a52-4a3b-9c1e-8f0b2d3a4b5c
  register: all_subscriptions

- name: Get information about a single subscription
  vmware.vmware_rest.content_library_subscriptions_info:
    library: e6d5c7a1-5a52-4a3b-9c1e-8f0b2d3a4b5c
    subscription: 8b1f0a3d-2c4e-4f6a-9b8c-1d2e3f4a5b6c
  register: my_subscription

- name: Display the subscribed library name
  ansible.builtin.debug:
    var: my_subscription.value.subscribed_library_name
"""

RETURN = r"""
id:
  description: The identifier (MOID) of the subscription that was queried.
  returned: When only one subscription, identified by O(subscription), was queried
  sample: 8b1f0a3d-2c4e-4f6a-9b8c-1d2e3f4a5b6c
  type: str
value:
  description: Detailed information about a single subscription.
  returned: When only one subscription, identified by O(subscription), was queried
  sample:
    subscribed_library: 3393956a-43ed-4e7f-bd96-eb39bd604445
    subscribed_library_name: my_subscribed_library
    subscribed_library_location: LOCAL
    subscribed_library_vcenter:
      hostname: vcenter.test
      https_port: 443
      server_guid: 52fb0b5e-ffc3-465b-bf4f-e4e6d5423cf5
  type: dict
info:
  description: A list of detailed information about all subscriptions of the published library.
  returned: When O(subscription) is not provided
  elements: dict
  sample:
    - subscription: 8b1f0a3d-2c4e-4f6a-9b8c-1d2e3f4a5b6c
      subscribed_library: 3393956a-43ed-4e7f-bd96-eb39bd604445
      subscribed_library_name: my_subscribed_library
      subscribed_library_vcenter_hostname: vcenter.test
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

MOID_PARAMETER_HINTS = ["library", "subscription"]

LIST_ENDPOINT = "/content/library/{library}/subscriptions"
ITEM_ENDPOINT = "/content/library/{library}/subscriptions/{subscription}"


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
    module_args["library"] = {
        "type": "str",
        "required": True,
    }
    module_args["subscription"] = {
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
