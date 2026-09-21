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
module: appliance_localaccounts_globalpolicy
short_description: Manage the global password policy for local accounts on the vCenter Server Appliance.
description:
  - Update the global password policy that applies to local accounts on the vCenter Server Appliance.
  - The policy controls password aging (maximum, minimum, and warning days), password complexity requirements, and account lockout behavior.
  - Changes apply to both new and existing local accounts. To change the policy for a single account, use the per-account local-accounts API instead.

author:
  - Ansible Eco Content Team (@eco-ansible-content)

extends_documentation_fragment:
  - vmware.vmware_rest.connection_params

options:
  state:
    description:
      - The desired state of the global password policy.
      - Use C(present) to update the policy with the supplied values.
    type: str
    default: present
    choices:
      - present
  max_days:
    description:
      - Maximum number of days a password may be used. If the password is older than this, a password change will be forced.
      - This property was added in vSphere API 6.7.
    type: int
    required: false
  min_days:
    description:
      - Minimum number of days allowed between password changes. Any password changes attempted sooner than this will be rejected.
      - This property was added in vSphere API 6.7.
    type: int
    required: false
  warn_days:
    description:
      - Number of days warning given before a password expires. A zero means warning is given only upon the day of expiration.
      - This property was added in vSphere API 6.7.
    type: int
    required: false
  prior_password_remember_count:
    description:
      - The number of prior passwords for the user to be remembered by the vCenter appliance in order for the appliance to assess non-repetition.
      - This property was added in vSphere API 9.1.0.0.
    type: int
    required: false
  failed_attempt_count_before_account_lockout:
    description:
      - Threshold Number of consecutive authentication failures for the user during the recent interval before the account is locked out.
      - This property was added in vSphere API 9.1.0.0.
    type: int
    required: false
  length_of_lockout_period_in_seconds:
    description:
      - The access will be reenabled after n seconds after the lock out.
      - This property was added in vSphere API 9.1.0.0.
    type: int
    required: false
  fail_interval_between_attempts:
    description:
      - The length of the interval during which the consecutive authentication failures must happen for the user account lock out
      - This property was added in vSphere API 9.1.0.0.
    type: int
    required: false
  minimum_length:
    description:
      - Minimum number of the characters needed in the password.
      - This property was added in vSphere API 9.1.0.0.
    type: int
    required: false
  minimum_uppercase_char_count:
    description:
      - Minimum number of upper case characters needed in the password.
      - This property was added in vSphere API 9.1.0.0.
    type: int
    required: false
  minimum_lowercase_char_count:
    description:
      - Minimum number of lower case characters needed in the password.
      - This property was added in vSphere API 9.1.0.0.
    type: int
    required: false
  minimum_numerics_char_count:
    description:
      - Minimum number of numeric characters needed in the password.
      - This property was added in vSphere API 9.1.0.0.
    type: int
    required: false
  minimum_special_char_count:
    description:
      - Minimum number of special characters needed in the password.
      - This property was added in vSphere API 9.1.0.0.
    type: int
    required: false
  managed_at_fleet:
    description:
      - Whether the password policy is managed at fleet or not.
      - This property was added in vSphere API 9.1.0.0.
    type: bool
    required: false

version_added: 5.0.0

requirements: []

notes:
  - Generated from vSphere API spec 9.1.0.
  - Not compatible with vSphere API 7.0.3.
  - Not compatible with vSphere API 8.0.2.
"""

EXAMPLES = r"""
- name: Set basic password aging policy
  vmware.vmware_rest.appliance_localaccounts_globalpolicy:
    max_days: 90
    min_days: 1
    warn_days: 7

- name: Enforce password complexity and account lockout policy
  vmware.vmware_rest.appliance_localaccounts_globalpolicy:
    max_days: 60
    min_days: 1
    warn_days: 14
    minimum_length: 12
    minimum_uppercase_char_count: 1
    minimum_lowercase_char_count: 1
    minimum_numerics_char_count: 1
    minimum_special_char_count: 1
    prior_password_remember_count: 5
    failed_attempt_count_before_account_lockout: 3
    fail_interval_between_attempts: 900
    length_of_lockout_period_in_seconds: 1800
"""

RETURN = r"""
value:
  description: The raw API response body from the vCenter operation.
  returned: On success
  sample: {}
  type: raw
"""


from ansible.module_utils.basic import AnsibleModule
from ansible_collections.vmware.vmware_rest.plugins.module_utils._argument_spec import (
    connection_params_argument_spec,
)
from ansible_collections.vmware.vmware_rest.plugins.module_utils._errors import (
    VmwareModuleError,
)
from ansible_collections.vmware.vmware_rest.plugins.module_utils._crud_module import (
    VmwareRestCrudModuleBase,
)
from ansible_collections.vmware.vmware_rest.plugins.module_utils._operation_configs import (
    OperationConfig,
)

MOID_PARAMETER_HINTS = []

LIST_ENDPOINT = ""
ITEM_ENDPOINT = "/appliance/local-accounts/global-policy"


GET_OPERATION = OperationConfig(
    name="get",
    uri=ITEM_ENDPOINT,
    http_method="GET",
)

UPDATE_OPERATION = OperationConfig(
    name="update",
    uri=ITEM_ENDPOINT,
    http_method="PUT",
    body_spec={
        "max_days": {
            "required": False,
        },
        "min_days": {
            "required": False,
        },
        "warn_days": {
            "required": False,
        },
        "prior_password_remember_count": {
            "required": False,
        },
        "failed_attempt_count_before_account_lockout": {
            "required": False,
        },
        "length_of_lockout_period_in_seconds": {
            "required": False,
        },
        "fail_interval_between_attempts": {
            "required": False,
        },
        "minimum_length": {
            "required": False,
        },
        "minimum_uppercase_char_count": {
            "required": False,
        },
        "minimum_lowercase_char_count": {
            "required": False,
        },
        "minimum_numerics_char_count": {
            "required": False,
        },
        "minimum_special_char_count": {
            "required": False,
        },
        "managed_at_fleet": {
            "required": False,
        },
    },
)


def create_module_argument_spec() -> dict:
    module_args = connection_params_argument_spec()
    module_args["fail_interval_between_attempts"] = {
        "type": "int",
    }
    module_args["failed_attempt_count_before_account_lockout"] = {
        "type": "int",
    }
    module_args["length_of_lockout_period_in_seconds"] = {
        "type": "int",
    }
    module_args["managed_at_fleet"] = {
        "type": "bool",
    }
    module_args["max_days"] = {
        "type": "int",
    }
    module_args["min_days"] = {
        "type": "int",
    }
    module_args["minimum_length"] = {
        "type": "int",
    }
    module_args["minimum_lowercase_char_count"] = {
        "type": "int",
    }
    module_args["minimum_numerics_char_count"] = {
        "type": "int",
    }
    module_args["minimum_special_char_count"] = {
        "type": "int",
    }
    module_args["minimum_uppercase_char_count"] = {
        "type": "int",
    }
    module_args["prior_password_remember_count"] = {
        "type": "int",
    }
    module_args["warn_days"] = {
        "type": "int",
    }
    module_args["state"] = {
        "type": "str",
        "choices": ["present"],
        "default": "present",
    }
    return module_args


def main():
    module = AnsibleModule(
        argument_spec=create_module_argument_spec(),
        supports_check_mode=True,
    )

    crud_module = VmwareRestCrudModuleBase(
        module=module,
        moid_parameter_hints=MOID_PARAMETER_HINTS,
        get_operation_config=GET_OPERATION,
        update_operation_config=UPDATE_OPERATION,
    )

    try:
        if module.params["state"] == "present":
            result = crud_module.ensure_present()
        else:
            module.fail_json(
                msg="Unsupported state: {0}".format(module.params["state"])
            )
    except VmwareModuleError as e:
        module.fail_json(**e.to_module_fail_json_output())

    module.exit_json(**result)


if __name__ == "__main__":
    main()
