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
module: appliance_infraprofile_configs_info
short_description: List the registered infrastructure profiles on the vCenter Server Appliance.
description:
  - List the infrastructure profiles (infraprofiles) that are registered on the vCenter Server Appliance.
  - Infrastructure profiles capture the configuration of appliance components so they can be exported, validated, and imported.
  - Use this module to discover which profiles are available before exporting or importing a
    configuration with M(vmware.vmware_rest.appliance_infraprofile_configs).

author:
  - Ansible Eco Content Team (@eco-ansible-content)

extends_documentation_fragment:
  - vmware.vmware_rest.connection_params

options: {}

version_added: 5.0.0

requirements: []

notes:
  - Generated from vSphere API spec 9.1.0.
  - Compatible with vSphere API 7.0.3.
  - Compatible with vSphere API 8.0.2.
"""

EXAMPLES = r"""
- name: List all registered infrastructure profiles
  vmware.vmware_rest.appliance_infraprofile_configs_info:
  register: infraprofiles

- name: Display the names of the registered infrastructure profiles
  ansible.builtin.debug:
    var: infraprofiles.value
"""

RETURN = r"""
value:
  description:
    - The list of registered infrastructure profiles.
    - Each entry describes a single profile that can be exported, validated, or imported.
  returned: On success
  sample:
    - name: ApplianceManagement
    - name: ApplianceNetwork
  type: list
  elements: dict

info:
  description:
    - The same information as RV(value), returned as a list for consistency with other info modules.
  returned: On success
  sample:
    - name: ApplianceManagement
    - name: ApplianceNetwork
  type: list
  elements: dict
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

MOID_PARAMETER_HINTS = []

LIST_ENDPOINT = ""
ITEM_ENDPOINT = "/appliance/infraprofile/configs"


GET_OPERATION = OperationConfig(
    name="get",
    uri=ITEM_ENDPOINT,
    http_method="GET",
)


def create_module_argument_spec() -> dict:
    module_args = connection_params_argument_spec()
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
    )
    try:
        result = info_module.get_resource_info()
    except VmwareModuleError as e:
        module.fail_json(**e.to_module_fail_json_output())
    module.exit_json(**result)


if __name__ == "__main__":
    main()
