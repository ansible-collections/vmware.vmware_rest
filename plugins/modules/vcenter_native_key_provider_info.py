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
module: vcenter_native_key_provider_info
short_description: Gather information about vCenter key providers.
description:
  - Gather information about Key Providers configured on a vCenter server.
  - Returns details about specific key provider if a key provider identifier is given.
  - Can filter the results by key provider identifiers or health status.

author:
  - Ansible Eco Content Team (@eco-ansible-content)

extends_documentation_fragment:
  - vmware.vmware_rest.connection_params

options:
  provider:
    description:
      - Identifier of the key provider to gather information for.
    type: str
    required: false
  providers:
    description:
      - List of key provider identifiers to filter the results by.
      - If missing or empty, the result will not be filtered by key provider identifiers.
    type: list
    required: false
    elements: str
  health:
    description:
      - List of key provider health statuses to filter the results by.
      - Supported values include C(OK), C(WARNING), C(ERROR).
      - If missing or empty, the result will not be filtered by key provider health statuses.
    type: list
    required: false
    elements: str

version_added: 5.0.0

requirements: []

notes:
  - Generated from vSphere API spec 9.1.0.
"""

EXAMPLES = r"""
- name: List all key providers
  vmware.vmware_rest.vcenter_native_key_provider_info:

- name: Get information about a specific key provider
  vmware.vmware_rest.vcenter_native_key_provider_info:
    provider: "my_key_provider"

- name: List key providers filtered by health statuses
  vmware.vmware_rest.vcenter_native_key_provider_info:
    health:
      - OK
      - WARNING
"""

RETURN = r"""
id:
  description: Identifier of the queried key provider
  returned: When only one key provider, with an identifier, was queried
  sample: my_key_provider
  type: str

value:
  description:
    - Detailed information about key provider.
    - Dict if only one item was found, list otherwise
    - Maintained for backwards compatibility. Use the info return value if possible.
  returned: On success
  sample:
    constraints: {tpm_required: true}
    health: OK
    native_info: {key_id: "1234567890"}
    type: NATIVE
  type: raw

info:
  description: A list of detailed information about key providers
  returned: On success
  sample:
    - constraints: {tpm_required: true}
      health: OK
      native_info: {key_id: "1234567890"}
      type: NATIVE
  type: list
"""


from ansible.module_utils.basic import AnsibleModule
from ansible_collections.vmware.vmware_rest.plugins.module_utils._argument_spec import (
    connection_params_argument_spec,
)
from ansible_collections.vmware.vmware_rest.plugins.module_utils._info_module import (
    VmwareRestInfoModuleBase,
)
from ansible_collections.vmware.vmware_rest.plugins.module_utils._operation_configs import (
    OperationConfig,
)


MOID_PARAMETER_HINTS = ["provider"]

LIST_ENDPOINT = "/vcenter/crypto-manager/kms/providers"
ITEM_ENDPOINT = "/vcenter/crypto-manager/kms/providers/{provider}"

LIST_OPERATION = OperationConfig(
    name="list",
    uri=LIST_ENDPOINT,
    http_method="GET",
    query_spec={
        "providers": {
            "required": False,
        },
        "health": {
            "required": False,
        },
    },
)

GET_OPERATION = OperationConfig(
    name="get",
    uri=ITEM_ENDPOINT,
    http_method="GET",
    query_spec={
        "provider": {
            "required": True,
        },
    },
)

def create_module_argument_spec() -> dict:
    module_args = connection_params_argument_spec()
    module_args["health"] = {
        "type": "list",
        "elements": "str",
        "required": False,
        "choices": ["OK", "WARNING", "ERROR"]
    }
    module_args["providers"] = {
        "type": "list",
        "elements": "str",
        "required": False
    }
    module_args["provider"] = {
        "type": "str",
        "required": False
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
    result = info_module.get_resource_info()
    module.exit_json(**result)


if __name__ == "__main__":
    main()
