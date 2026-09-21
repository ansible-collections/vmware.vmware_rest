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
module: appliance_infraprofile_configs
short_description: Export, import, or validate infrastructure profile configurations on the vCenter Server Appliance.
description:
  - Export, import, or validate infrastructure profile (infraprofile) configurations on the vCenter Server Appliance.
  - Infrastructure profiles capture the configuration of appliance components (such as Authentication Management or Appliance Management) so they can be backed up and applied to other appliances.
  - Use C(state=export) to retrieve the current configuration of one or more profiles as a JSON specification.
  - Use C(state=import) to apply a previously exported configuration specification to the appliance.
  - Use C(state=validate) to check whether a configuration specification can be applied without actually importing it.
  - These are non-idempotent actions that are executed each time the module runs.

author:
  - Ansible Eco Content Team (@eco-ansible-content)

extends_documentation_fragment:
  - vmware.vmware_rest.connection_params

options:
  state:
    description:
      - The desired state of the resource.
      - Use C(export) to perform the export action.
      - Use C(import) to perform the import action.
      - Use C(validate) to perform the validate action.
      - Only options C(present) and C(absent) support idempotence.
    type: str
    required: true
    choices:
      - export
      - import
      - validate
  encryption_key:
    description:
      - This property is deprecated as of __vSphere API 9.0.0.0__.
      - Encryption Key to encrypt/decrypt profiles.
      - This property was added in __vSphere API 7.0.0.0__.
      - If missing or 'null' encryption will not be used for the profile.
    type: str
    required: false
  description:
    description:
      - This property is deprecated as of __vSphere API 9.0.0.0__.
      - Custom description provided by the user.
      - This property was added in __vSphere API 7.0.0.0__.
      - If missing or 'null' description will be empty.
    type: str
    required: false
  profiles:
    description:
      - This property is deprecated as of __vSphere API 9.0.0.0__.
      - Profiles to be exported/imported.
      - This property was added in __vSphere API 7.0.0.0__.
      - If missing or 'null' or empty, all profiles will be returned.
      - When clients pass a value of this schema as a parameter, the property must contain identifiers (MOIDs) for the resource type 'com.vmware.infraprofile.profile'. When operations return a value of this schema as a response, the property will contain identifiers (MOIDs) for the resource type 'com.vmware.infraprofile.profile'.
    type: list
    required: false
    elements: str
  config_spec:
    description:
      - This property is deprecated as of __vSphere API 9.0.0.0__.
      - The JSON string representing the desired config specification.
      - This property was added in __vSphere API 7.0.0.0__.
    type: str
    required: false
  profile_spec:
    description:
      - This property is deprecated as of __vSphere API 9.0.0.0__.
      - The profile specification, if any
      - This property was added in __vSphere API 7.0.0.0__.
      - Only set if there is a profilespec avaliable for this import profilespec.
    type: dict
    required: false
    suboptions:
      encryption_key:
        description:
          - This property is deprecated as of __vSphere API 9.0.0.0__.
          - Encryption Key to encrypt/decrypt profiles.
          - This property was added in __vSphere API 7.0.0.0__.
          - If missing or 'null' encryption will not be used for the profile.
        type: str
        required: false
      description:
        description:
          - This property is deprecated as of __vSphere API 9.0.0.0__.
          - Custom description provided by the user.
          - This property was added in __vSphere API 7.0.0.0__.
          - If missing or 'null' description will be empty.
        type: str
        required: false
      profiles:
        description:
          - This property is deprecated as of __vSphere API 9.0.0.0__.
          - Profiles to be exported/imported.
          - This property was added in __vSphere API 7.0.0.0__.
          - If missing or 'null' or empty, all profiles will be returned.
          - When clients pass a value of this schema as a parameter, the property must contain identifiers (MOIDs) for the resource type 'com.vmware.infraprofile.profile'. When operations return a value of this schema as a response, the property will contain identifiers (MOIDs) for the resource type 'com.vmware.infraprofile.profile'.
        type: list
        required: false
        elements: str

version_added: 5.0.0

requirements: []

notes:
  - Generated from vSphere API spec 9.1.0.
  - Compatible with vSphere API 7.0.3.
  - Compatible with vSphere API 8.0.2.
"""

EXAMPLES = r"""
- name: Export all infrastructure profiles
  vmware.vmware_rest.appliance_infraprofile_configs:
    state: export
  register: exported_profiles

- name: Export a specific profile with a description
  vmware.vmware_rest.appliance_infraprofile_configs:
    state: export
    profiles:
      - ApplianceManagement
    description: Backup taken before upgrade
  register: appliance_mgmt_profile

- name: Validate a configuration specification before importing it
  vmware.vmware_rest.appliance_infraprofile_configs:
    state: validate
    config_spec: "{{ exported_profiles.value }}"

- name: Import a previously exported configuration specification
  vmware.vmware_rest.appliance_infraprofile_configs:
    state: import
    config_spec: "{{ exported_profiles.value }}"
    profile_spec:
      description: Restore appliance configuration
      profiles:
        - ApplianceManagement
"""

RETURN = r"""
id:
  description: Identifier of the infraprofile action performed.
  returned: When state is set to a supported action
  sample: ''
  type: str

value:
  description:
    - The raw API response body from the vCenter operation.
    - For C(export), this is the JSON configuration specification of the requested profiles.
    - For C(import) and C(validate), this contains the result of the operation, including any validation status or messages.
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
ITEM_ENDPOINT = "/appliance/infraprofile/configs"


GET_OPERATION = OperationConfig(
    name="get",
    uri=ITEM_ENDPOINT,
    http_method="GET",
)


ACTION_OPERATIONS = {
    "export": OperationConfig(
        name="export",
        uri="/appliance/infraprofile/configs?action=export",
        http_method="POST",
        body_spec={
            "encryption_key": {
                "required": False,
            },
            "description": {
                "required": False,
            },
            "profiles": {
                "required": False,
            },
        },
    ),
    "import": OperationConfig(
        name="import",
        uri="/appliance/infraprofile/configs?action=import&vmw-task=true",
        http_method="POST",
        body_spec={
            "config_spec": {
                "required": True,
            },
            "profile_spec": {
                "required": False,
                "subspec": {
                    "encryption_key": {
                        "required": False,
                    },
                    "description": {
                        "required": False,
                    },
                    "profiles": {
                        "required": False,
                    },
                },
            },
        },
    ),
    "validate": OperationConfig(
        name="validate",
        uri="/appliance/infraprofile/configs?action=validate&vmw-task=true",
        http_method="POST",
        body_spec={
            "config_spec": {
                "required": True,
            },
            "profile_spec": {
                "required": False,
                "subspec": {
                    "encryption_key": {
                        "required": False,
                    },
                    "description": {
                        "required": False,
                    },
                    "profiles": {
                        "required": False,
                    },
                },
            },
        },
    ),
}


def create_module_argument_spec() -> dict:
    module_args = connection_params_argument_spec()
    module_args["config_spec"] = {
        "type": "str",
    }
    module_args["description"] = {
        "type": "str",
    }
    module_args["encryption_key"] = {
        "type": "str",
        "no_log": True,
    }
    module_args["profile_spec"] = {
        "type": "dict",
        "options": {
            "encryption_key": {
                "type": "str",
                "no_log": True,
            },
            "description": {
                "type": "str",
            },
            "profiles": {
                "type": "list",
                "elements": "str",
            },
        },
    }
    module_args["profiles"] = {
        "type": "list",
        "elements": "str",
    }
    module_args["state"] = {
        "type": "str",
        "choices": ["export", "import", "validate"],
        "required": True,
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
        action_operations=ACTION_OPERATIONS,
    )

    try:
        if module.params["state"] in ACTION_OPERATIONS:
            result = crud_module.perform_action()
        else:
            module.fail_json(
                msg="Unsupported state: {0}".format(module.params["state"])
            )
    except VmwareModuleError as e:
        module.fail_json(**e.to_module_fail_json_output())

    module.exit_json(**result)


if __name__ == "__main__":
    main()
