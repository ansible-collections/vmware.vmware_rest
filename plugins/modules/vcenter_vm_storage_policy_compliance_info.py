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
module: vcenter_vm_storage_policy_compliance_info
short_description: Returns cached VM storage policy compliance information
description:
  - Returns the cached storage policy compliance information of a virtual machine.
  - The response includes overall compliance status and per-entity compliance for the
    virtual machine home directory and associated virtual disks.
author:
  - Ansible Eco Content Team (@eco-ansible-content)
extends_documentation_fragment:
  - vmware.vmware_rest.connection_params
options:
  vm:
    description:
      - Identifier of the virtual machine.
      - Must be an identifier (MOID) for a C(VirtualMachine) resource.
    type: str
    required: true
version_added: 4.11.0
requirements: []
notes:
  - Generated from vSphere API spec 9.1.0.
  - Has support for vSphere API 7.0.3.
  - Has support for vSphere API 8.0.2.
"""

EXAMPLES = r"""
- name: Get cached VM storage policy compliance information
  vmware.vmware_rest.vcenter_vm_storage_policy_compliance_info:
    vm: vm-1009
  register: vm_compliance
"""

RETURN = r"""
value:
  description:
    - Storage policy compliance information for the virtual machine.
    - May be empty when neither the virtual machine home directory nor any virtual disks
      are associated with a storage policy.
  returned: On success
  type: dict
  sample:
    overall_compliance: COMPLIANT
    vm_home:
      status: COMPLIANT
      check_time: "2026-01-15T10:30:00Z"
      policy: policy-123
      failure_cause: []
    disks:
      "2000":
        status: COMPLIANT
        check_time: "2026-01-15T10:30:00Z"
        policy: policy-123
        failure_cause: []
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.vmware.vmware_rest.plugins.module_utils._argument_spec import (
    connection_params_argument_spec,
)
from ansible_collections.vmware.vmware_rest.plugins.module_utils._module_base import (
    VmwareRestInfoModuleBase,
)

COMPLIANCE_PATH = "/vcenter/vm/{vm}/storage/policy/compliance"


class VmwareRestInfoModule(VmwareRestInfoModuleBase):
    PAYLOAD_FORMAT = {
        "get": {"query": {}, "body": {}, "path": {"vm": "vm"}},
    }

    def get_info(self):
        path = self.build_path(COMPLIANCE_PATH)
        response = self.client.get(path)
        if response.status == 404:
            return {}
        return response.json or {}


def main():
    module_args = connection_params_argument_spec()
    module_args["vm"] = {"type": "str", "required": True}

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
    )

    info_module = VmwareRestInfoModule(module)
    result = info_module.get_info()
    module.exit_json(value=result)


if __name__ == "__main__":
    main()
