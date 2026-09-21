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
module: appliance_localaccounts_info
short_description: Gather information about local accounts on the vCenter Server Appliance.
description:
  - Retrieve information about local user accounts on the vCenter Server Appliance.
  - When O(username) is provided, return the detailed properties of that single account, such as its
    full name, email, assigned roles, and password aging settings.
  - When O(username) is omitted, list all local accounts on the appliance.

author:
  - Ansible Eco Content Team (@eco-ansible-content)

extends_documentation_fragment:
  - vmware.vmware_rest.connection_params

options:
  username:
    description:
      - The name of the local account to retrieve detailed information for.
      - When omitted, information about all local accounts on the appliance is returned.
    type: str
    required: false

version_added: 5.0.0

requirements: []

notes:
  - Generated from vSphere API spec 9.1.0.
  - Compatible with vSphere API 7.0.3.
  - Compatible with vSphere API 8.0.2.
"""

EXAMPLES = r"""
- name: List all local accounts on the appliance
  vmware.vmware_rest.appliance_localaccounts_info:
  register: all_accounts

- name: Get information about a single local account
  vmware.vmware_rest.appliance_localaccounts_info:
    username: root
  register: root_account

- name: Display the roles assigned to the account
  ansible.builtin.debug:
    var: root_account.value.roles
"""

RETURN = r"""
id:
  description: The name of the queried local account.
  returned: When only one account, identified by O(username), was queried
  sample: root
  type: str
value:
  description: Detailed information about a single local account.
  returned: When only one account, identified by O(username), was queried
  sample:
    enabled: true
    has_password: true
    fullname: root
    email: admin@example.com
    roles:
      - superAdmin
    last_password_change: "2026-06-01T00:00:00.000Z"
    max_days_between_password_change: 90
    min_days_between_password_change: 1
    warn_days_before_password_expiration: 7
  type: dict
info:
  description: A list of detailed information about local accounts on the appliance.
  returned: When O(username) is not provided
  elements: dict
  sample:
    - enabled: true
      has_password: true
      fullname: root
      roles:
        - superAdmin
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

MOID_PARAMETER_HINTS = ["username"]

LIST_ENDPOINT = "/appliance/local-accounts"
ITEM_ENDPOINT = "/appliance/local-accounts/{username}"


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
    module_args["username"] = {
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
