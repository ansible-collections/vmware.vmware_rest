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
short_description: Get the local user account information.
description:
  - Returns information about local user accounts on the vCenter Server appliance.
  - When I(username) is specified, returns information for that account only.
  - When I(username) is omitted, lists all local accounts with detailed information
    for each account.
author:
  - Ansible Eco Content Team (@eco-ansible-content)
extends_documentation_fragment:
  - vmware.vmware_rest.connection_params
options:
  username:
    description:
      - User login name.
      - Must be an identifier (MOID) for a C(com.vmware.appliance.local_accounts) resource.
      - When specified, only that account is returned.
    type: str
version_added: 4.11.0
requirements: []
notes:
  - Generated from vSphere API spec 9.1.0.
  - Has support for vSphere API 7.0.3.
  - Has support for vSphere API 8.0.2.
"""

EXAMPLES = r"""
- name: List the local accounts
  vmware.vmware_rest.appliance_localaccounts_info:
  register: local_accounts

- name: Get a specific local account
  vmware.vmware_rest.appliance_localaccounts_info:
    username: root
  register: root_account
"""

RETURN = r"""
value:
  description:
    - Local account information.
    - Returns a list of account dictionaries when I(username) is omitted.
    - Returns a single account dictionary when I(username) is specified.
  returned: On success
  type: raw
  sample:
    - enabled: true
      fullname: root
      has_password: true
      roles:
        - superAdmin
      username: root
  contains:
    username:
      description:
        - User login name.
      type: str
      sample: root
    fullname:
      description:
        - Full name of the user.
      type: str
      sample: root
    email:
      description:
        - Email address of the local account.
      type: str
    roles:
      description:
        - User roles.
        - Each element must be an identifier (MOID) for a C(com.vmware.appliance.roles) resource.
      type: list
      elements: str
      sample:
        - superAdmin
    enabled:
      description:
        - Flag indicating if the account is enabled.
      type: bool
      sample: true
    has_password:
      description:
        - Flag indicating whether the user password is set.
      type: bool
      sample: true
    last_password_change:
      description:
        - Date and time the password was changed.
      type: str
      sample: "2022-11-23T00:00:00.000Z"
    password_expires_at:
      description:
        - Date when the account password will expire.
      type: str
      sample: "2023-02-21T00:00:00.000Z"
    inactive_at:
      description:
        - Date and time the account will be locked after password expiration.
      type: str
    min_days_between_password_change:
      description:
        - Minimum number of days between password changes.
      type: int
      sample: 0
    max_days_between_password_change:
      description:
        - Maximum number of days between password changes.
      type: int
      sample: 90
    warn_days_before_password_expiration:
      description:
        - Number of days of warning before the password expires.
      type: int
      sample: 7
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.vmware.vmware_rest.plugins.module_utils._argument_spec import (
    connection_params_argument_spec,
)
from ansible_collections.vmware.vmware_rest.plugins.module_utils._module_base import (
    VmwareRestInfoModuleBase,
)

LIST_PATH = "/appliance/local-accounts"
ACCOUNT_PATH = "/appliance/local-accounts/{username}"


class VmwareRestInfoModule(VmwareRestInfoModuleBase):
    PAYLOAD_FORMAT = {
        "list": {"query": {}, "body": {}, "path": {}},
        "get": {"query": {}, "body": {}, "path": {"username": "username"}},
    }

    def _get_account(self, username):
        response = self.client.get(
            self.build_path(ACCOUNT_PATH, {"username": username})
        )
        if response.status == 404:
            return None
        account = response.json
        account["username"] = username
        return account

    def get_info(self):
        username = self.params.get("username")
        if username:
            account = self._get_account(username)
            if account is None:
                self.module.fail_json(
                    msg="Local account not found: {0}".format(username)
                )
            return account

        usernames = self.fetch_list(LIST_PATH, self.PAYLOAD_FORMAT["list"])
        result = []
        for name in usernames:
            account = self._get_account(name)
            if account is not None:
                result.append(account)
        return result


def main():
    module_args = connection_params_argument_spec()
    module_args["username"] = {"type": "str"}

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
    )

    info_module = VmwareRestInfoModule(module)
    result = info_module.get_info()
    module.exit_json(value=result)


if __name__ == "__main__":
    main()
