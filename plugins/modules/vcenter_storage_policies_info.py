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
module: vcenter_storage_policies_info
short_description: Gather information about vCenter storage policies.
description:
  - Retrieve information about VMware vSphere storage policies.
  - Storage policies define storage requirements and capabilities for virtual machines and virtual disks through Storage Policy-Based Management (SPBM).
  - Use this module to list all available storage policies or to get details about specific policies by their identifiers.
  - Storage policies help ensure that VM storage is provisioned on datastores that meet defined service levels and capabilities.

author:
  - Ansible Eco Content Team (@eco-ansible-content)

extends_documentation_fragment:
  - vmware.vmware_rest.connection_params

options:
  policies:
    description:
      - A list of storage policy MOIDs to filter the results.
      - Only storage policies whose identifiers appear in this list will be returned.
      - If omitted or empty, all storage policies are returned.
      - This parameter was added in vSphere API 6.7.
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
- name: List all storage policies
  vmware.vmware_rest.vcenter_storage_policies_info:
  register: all_storage_policies

- name: Get details about specific storage policies
  vmware.vmware_rest.vcenter_storage_policies_info:
    policies:
      - aa6d5a82-1c88-45da-85d3-3d74b91a5bad
      - 9b0e68e6-54cf-4b59-9e53-8a8e0b45c4d2
  register: filtered_policies
"""

RETURN = r"""
id:
  description: Identifier of the queried storage policy.
  returned: When only one storage policy, with an identifier, was queried.
  sample: aa6d5a82-1c88-45da-85d3-3d74b91a5bad
  type: str
value:
  description:
    - Raw output from the API response.
    - This output is maintained for consistency with version 4.x and earlier of this collection.
      It is recommended to switch to the info return key for a more consistent and documented output.
  returned: On success.
  sample:
    policy: aa6d5a82-1c88-45da-85d3-3d74b91a5bad
    name: VM Storage Policy
    description: Storage policy for virtual machine workloads
  type: raw
info:
  description: A list of storage policies matching the query.
  returned: On success.
  sample:
    - policy: aa6d5a82-1c88-45da-85d3-3d74b91a5bad
      name: VM Storage Policy
      description: Storage policy for virtual machine workloads
    - policy: 9b0e68e6-54cf-4b59-9e53-8a8e0b45c4d2
      name: High Performance Policy
      description: Storage policy for high-performance applications
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

MOID_PARAMETER_HINTS = []

LIST_ENDPOINT = ""
ITEM_ENDPOINT = "/vcenter/storage/policies"


GET_OPERATION = OperationConfig(
    name="get",
    uri=ITEM_ENDPOINT,
    http_method="GET",
)


def create_module_argument_spec() -> dict:
    module_args = connection_params_argument_spec()
    module_args["policies"] = {
        "type": "list",
        "elements": "str",
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
    )
    try:
        result = info_module.get_resource_info()
    except VmwareModuleError as e:
        module.fail_json(**e.to_module_fail_json_output())
    module.exit_json(**result)


if __name__ == "__main__":
    main()
