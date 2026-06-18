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
short_description: Retrieves information about vCenter storage policies.
description:
  - Returns information about storage policies available in vCenter Server.
  - Storage policies can be used when provisioning virtual machines or disks.
  - When I(policies) is omitted, returns all visible storage policies matching the filter.
author:
  - Ansible Eco Content Team (@eco-ansible-content)
extends_documentation_fragment:
  - vmware.vmware_rest.connection_params
options:
  policies:
    description:
      - Identifiers of storage policies that can match the filter.
      - Each element must be an identifier (MOID) for a
        C(com.vmware.vcenter.StoragePolicy) resource.
      - When omitted or empty, storage policies with any identifier match the filter.
    type: list
    elements: str
version_added: 4.11.0
requirements: []
notes:
  - Generated from vSphere API spec 9.1.0.
  - Has support for vSphere API 7.0.3.
  - Has support for vSphere API 8.0.2.
"""

EXAMPLES = r"""
- name: List all storage policies
  vmware.vmware_rest.vcenter_storage_policies_info:
  register: storage_policies

- name: List specific storage policies
  vmware.vmware_rest.vcenter_storage_policies_info:
    policies:
      - 08d5e973-1d60-48e0-877b-66f5e0c3d88b
  register: filtered_storage_policies
"""

RETURN = r"""
value:
  description:
    - Storage policy information.
  returned: On success
  type: list
  elements: dict
  sample:
    - policy: 08d5e973-1d60-48e0-877b-66f5e0c3d88b
      name: vSAN Default Storage Policy
      description: Storage policy used by default for vSAN datastores
  contains:
    policy:
      description:
        - Identifier of the storage policy.
        - Must be an identifier (MOID) for a C(com.vmware.vcenter.StoragePolicy) resource.
      type: str
      sample: 08d5e973-1d60-48e0-877b-66f5e0c3d88b
    name:
      description:
        - Name of the storage policy.
      type: str
      sample: vSAN Default Storage Policy
    description:
      description:
        - Description of the storage policy.
      type: str
      sample: Storage policy used by default for vSAN datastores
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.vmware.vmware_rest.plugins.module_utils._argument_spec import (
    connection_params_argument_spec,
)
from ansible_collections.vmware.vmware_rest.plugins.module_utils._module_base import (
    VmwareRestInfoModuleBase,
    normalize_list_response,
)

LIST_PATH = "/vcenter/storage/policies"


class VmwareRestInfoModule(VmwareRestInfoModuleBase):
    PAYLOAD_FORMAT = {
        "list": {
            "query": {"policies": "policies"},
            "body": {},
            "path": {},
        },
    }

    def get_info(self):
        query = self.build_query(self.PAYLOAD_FORMAT["list"])
        response = self.client.get(LIST_PATH, query=query or None)
        if response.status == 404:
            return []

        return normalize_list_response(response.json)


def main():
    module_args = connection_params_argument_spec()
    module_args["policies"] = {"type": "list", "elements": "str"}

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
    )

    info_module = VmwareRestInfoModule(module)
    result = info_module.get_info()
    module.exit_json(value=result)


if __name__ == "__main__":
    main()
