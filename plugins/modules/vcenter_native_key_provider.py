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
module: vcenter_native_key_provider
short_description: Manage vCenter native key providers.
description:
  - Create, update, or delete Native Key Providers on a vCenter server.
  - Can also be used to export or import Native Key Provider configurations.

author:
  - Ansible Eco Content Team (@eco-ansible-content)

extends_documentation_fragment:
  - vmware.vmware_rest.connection_params

options:
  state:
    description:
      - The desired action to perform on the native key provider.
      - Use C(present) to create or update the native key provider.
      - Use C(absent) to delete the native key provider.
      - Use C(export) to perform the export action.
      - Use C(import) to perform the import action.
      - Only options C(present) and C(absent) support idempotence.
    type: str
    default: present
    choices:
      - present
      - absent
      - export
      - import
  provider:
    description:
      - Identifier (name) of the native key provider.
      - This must be a unique string provided by the user when creating a new key provider.
    type: str
    required: false
  constraints:
    description:
      - The constraints on the key provider.
      - If missing, there are no constraints on the key provider.
    type: dict
    required: false
    suboptions:
      tpm_required:
        description:
          - Determines if the key provider is restricted to hosts with TPM 2.0 capability.
        type: bool
        required: false
  native_spec:
    description:
      - Specifications for creating a native key provider with C(state=present).
    type: dict
    required: false
    suboptions:
      key_id:
        description:
          - Key identifier for the key provider.
          - The key identifier must be a 128-bit UUID represented as a hexadecimal string in "12345678-abcd-1234-cdef-123456789abc" format.
          - If missing, the key identifier will be generated automatically.
        type: str
        required: false
      key_derivation_key:
        description:
          - Key used to derive data encryption keys. Must be Base64 encoded.
          - If missing, the key derivation key will be generated automatically.
        type: str
        required: false
  password:
    description:
      - Password used to encrypt the exported key provider configuration or decrypt an imported key provider configuration.
      - If missing or empty, the key provider configuration will not be encrypted when exporting.
      - This property is required when C(state=import) to decrypt an encrypted key provider configuration.
    type: str
    required: false
  config:
    description:
      - Native key provider configuration file to import with C(state=import).
      - This property is required when C(state=import) to import a key provider configuration.
    type: str
    required: false
  dry_run:
    description:
      - Whether to perform a trial import without actually creating a key provider.
      - Used in conjunction with C(state=import) to validate the key provider configuration.
    type: bool
    required: false

version_added: 5.0.0

requirements: []

notes:
  - Generated from vSphere API spec 9.1.0.
"""

EXAMPLES = r"""
- name: Create a new native key provider
  vmware.vmware_rest.vcenter_native_key_provider:
    provider: "my_native_key_provider"
    state: present

- name: Create a native key provider with TPM required
  vmware.vmware_rest.vcenter_native_key_provider:
    provider: "secure_native_key_provider"
    state: present
    constraints:
      tpm_required: true

- name: Export a native key provider configuration
  vmware.vmware_rest.vcenter_native_key_provider:
    provider: "my_native_key_provider"
    state: export
    password: "SuperSecretPassword123!"

- name: Delete a native key provider
  vmware.vmware_rest.vcenter_native_key_provider:
    provider: "my_native_key_provider"
    state: absent
"""

RETURN = r"""
id:
  description: MOID of the managed resource
  returned: When state is present, or when a resource is deleted, or when state is set to a supported action
  sample: my_native_provider
  type: str
"""


from ansible.module_utils.basic import AnsibleModule
from ansible_collections.vmware.vmware_rest.plugins.module_utils._argument_spec import (
    connection_params_argument_spec,
)
from ansible_collections.vmware.vmware_rest.plugins.module_utils._crud_module import (
    VmwareRestCrudModuleBase,
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
            "module_param": "provider",
        },
    },
)

GET_OPERATION = OperationConfig(
    name="get",
    uri=ITEM_ENDPOINT,
    http_method="GET",
)

CREATE_OPERATION = OperationConfig(
    name="create",
    uri=LIST_ENDPOINT,
    http_method="POST",
    body_spec={
        "provider": {
            "required": True,
        },
        "constraints": {
            "required": False,
            "subspec": {
                "tpm_required": {
                    "required": False,
                },
            },
        },
        "native_spec": {
            "required": False,
            "subspec": {
                "key_id": {
                    "required": False,
                },
                "key_derivation_key": {
                    "required": False,
                },
            },
        },
    },
)

UPDATE_OPERATION = OperationConfig(
    name="update",
    uri=ITEM_ENDPOINT,
    http_method="PATCH",
    body_spec={
        "native_spec": {
            "required": False,
            "subspec": {
                "key_id": {
                    "required": False,
                },
                "key_derivation_key": {
                    "required": False,
                },
            },
        },
    },
)

DELETE_OPERATION = OperationConfig(
    name="delete",
    uri=ITEM_ENDPOINT,
    http_method="DELETE",
)


ACTION_OPERATIONS = {
    "export": OperationConfig(
        name="export",
        uri="/vcenter/crypto-manager/kms/providers?action=export",
        http_method="POST",
        body_spec={
            "provider": {
                "required": True,
            },
            "password": {
                "required": False,
            },
        },
    ),
    "import": OperationConfig(
        name="import",
        uri="/vcenter/crypto-manager/kms/providers?action=import",
        http_method="POST",
        body_spec={
            "config": {
                "required": False,
            },
            "password": {
                "required": False,
            },
            "constraints": {
                "required": False,
                "subspec": {
                    "tpm_required": {
                        "required": False,
                    },
                },
            },
            "dry_run": {
                "required": False,
            },
        },
    ),
}


def create_module_argument_spec() -> dict:
    module_args = connection_params_argument_spec()
    module_args["config"] = {
        "type": "str",
    }
    module_args["constraints"] = {
        "type": "dict",
        "options": {
            "tpm_required": {
                "type": "bool",
            },
        },
    }
    module_args["dry_run"] = {
        "type": "bool",
    }
    module_args["native_spec"] = {
        "type": "dict",
        "options": {
            "key_id": {
                "type": "str",
            },
            "key_derivation_key": {
                "type": "str",
            },
        },
    }
    module_args["password"] = {
        "type": "str",
    }
    module_args["provider"] = {
        "type": "str",
    }
    module_args["state"] = {
        "type": "str",
        "choices": ['present', 'absent', 'export', 'import'],
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
        list_operation_config=LIST_OPERATION,
        create_operation_config=CREATE_OPERATION,
        update_operation_config=UPDATE_OPERATION,
        delete_operation_config=DELETE_OPERATION,
        action_operations=ACTION_OPERATIONS,
    )

    if module.params["state"] == "present":
        result = crud_module.ensure_present()
    elif module.params["state"] == "absent":
        result = crud_module.ensure_absent()
    elif module.params["state"] in ACTION_OPERATIONS:
        result = crud_module.perform_action()
    else:
        module.fail_json(msg="Unsupported state: {0}".format(module.params["state"]))

    module.exit_json(**result)


if __name__ == "__main__":
    main()
