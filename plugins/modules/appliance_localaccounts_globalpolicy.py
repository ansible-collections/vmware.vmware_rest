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
module: appliance_localaccounts_globalpolicy
short_description: Set the global password policy.
description:
  - Sets the global password policy for local accounts on the vCenter Server appliance.
  - Only parameters explicitly specified by the user are sent to the API.
  - Use I(state=present) to update the global password policy when it differs from
    the current configuration.
author:
  - Ansible Eco Content Team (@eco-ansible-content)
extends_documentation_fragment:
  - vmware.vmware_rest.connection_params
options:
  state:
    description:
      - The desired state of the global password policy.
      - Use C(present) to update the global password policy.
      - C(absent) is not supported because the API does not provide a delete operation.
    type: str
    choices:
      - present
      - absent
    default: present
  max_days:
    description:
      - Maximum number of days a password may be used.
      - If the password is older than this, a password change will be forced.
      - If unset on the appliance, the restriction is ignored.
    type: int
  min_days:
    description:
      - Minimum number of days allowed between password changes.
      - Password changes attempted sooner than this will be rejected.
      - If unset on the appliance, the restriction is ignored.
    type: int
  warn_days:
    description:
      - Number of days warning given before a password expires.
      - A zero means warning is given only upon the day of expiration.
      - If unset on the appliance, no warning will be provided.
    type: int
  prior_password_remember_count:
    description:
      - Number of prior passwords remembered to assess non-repetition.
    type: int
  failed_attempt_count_before_account_lockout:
    description:
      - Number of consecutive authentication failures before the account is locked out.
    type: int
  length_of_lockout_period_in_seconds:
    description:
      - Number of seconds after lockout before access is re-enabled.
    type: int
  fail_interval_between_attempts:
    description:
      - Interval in seconds during which consecutive authentication failures must
        occur for account lockout.
    type: int
  minimum_length:
    description:
      - Minimum number of characters required in the password.
    type: int
  minimum_uppercase_char_count:
    description:
      - Minimum number of uppercase characters required in the password.
    type: int
  minimum_lowercase_char_count:
    description:
      - Minimum number of lowercase characters required in the password.
    type: int
  minimum_numerics_char_count:
    description:
      - Minimum number of numeric characters required in the password.
    type: int
  minimum_special_char_count:
    description:
      - Minimum number of special characters required in the password.
    type: int
version_added: 4.11.0
requirements: []
notes:
  - Generated from vSphere API spec 9.1.0.
  - Has support for vSphere API 7.0.3.
  - Has support for vSphere API 8.0.2.
"""

EXAMPLES = r"""
- name: Update the global policy of the local accounts
  vmware.vmware_rest.appliance_localaccounts_globalpolicy:
    warn_days: 5

- name: Set minimum and maximum password age
  vmware.vmware_rest.appliance_localaccounts_globalpolicy:
    min_days: 1
    max_days: 90
"""

RETURN = r"""
value:
  description:
    - Global password policy after update, or current policy when no change was made.
  returned: On success when I(state=present)
  type: dict
  sample:
    max_days: 90
    min_days: 1
    warn_days: 5
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.vmware.vmware_rest.plugins.module_utils._argument_spec import (
    connection_params_argument_spec,
)
from ansible_collections.vmware.vmware_rest.plugins.module_utils._errors import (
    UnexpectedAPIResponse,
)
from ansible_collections.vmware.vmware_rest.plugins.module_utils._module_base import (
    VmwareRestCrudModuleBase,
    params_differ,
)

PATH = "/appliance/local-accounts/global-policy"

_UPDATE_BODY = {
    "max_days": "max_days",
    "min_days": "min_days",
    "warn_days": "warn_days",
    "prior_password_remember_count": "prior_password_remember_count",
    "failed_attempt_count_before_account_lockout": (
        "failed_attempt_count_before_account_lockout"
    ),
    "length_of_lockout_period_in_seconds": "length_of_lockout_period_in_seconds",
    "fail_interval_between_attempts": "fail_interval_between_attempts",
    "minimum_length": "minimum_length",
    "minimum_uppercase_char_count": "minimum_uppercase_char_count",
    "minimum_lowercase_char_count": "minimum_lowercase_char_count",
    "minimum_numerics_char_count": "minimum_numerics_char_count",
    "minimum_special_char_count": "minimum_special_char_count",
}


class VmwareRestCrudModule(VmwareRestCrudModuleBase):
    PAYLOAD_FORMAT = {
        "update": {
            "query": {},
            "body": _UPDATE_BODY,
            "path": {},
        },
    }

    UPDATABLE_PARAMS = tuple(_UPDATE_BODY.values())

    def ensure_present(self):
        response = self.client.get(PATH)
        current = response.json

        update_body = self.build_updatable_payload()
        if not update_body:
            return {"changed": False, "value": current}

        if not params_differ(current, update_body):
            return {"changed": False, "value": current}

        if not self.module.check_mode:
            put_response = self.client.request("PUT", PATH, data=update_body)
            if put_response.status not in (200, 204):
                self.client.error_handler.handle_request_error(
                    exception=UnexpectedAPIResponse(
                        put_response.status, put_response.data
                    ),
                    method="PUT",
                    path=PATH,
                    request_kwargs={"data": update_body},
                )

            updated = self.client.get(PATH)
            return {"changed": True, "value": updated.json}

        return {"changed": True, "value": current}

    def ensure_absent(self):
        return {"changed": False}


def main():
    module_args = connection_params_argument_spec()
    module_args["state"] = {
        "type": "str",
        "choices": ["present", "absent"],
        "default": "present",
    }
    for param in _UPDATE_BODY.values():
        module_args[param] = {"type": "int"}

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
    )

    crud_module = VmwareRestCrudModule(module)

    if module.params["state"] == "present":
        result = crud_module.ensure_present()
    elif module.params["state"] == "absent":
        result = crud_module.ensure_absent()
    else:
        module.fail_json(msg="Unsupported state: {0}".format(module.params["state"]))

    module.exit_json(**result)


if __name__ == "__main__":
    main()
