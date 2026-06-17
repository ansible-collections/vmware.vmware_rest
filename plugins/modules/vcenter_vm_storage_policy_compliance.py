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
module: vcenter_vm_storage_policy_compliance
short_description: Re-computes and returns storage policy compliance for a virtual machine
description:
  - Returns storage policy compliance information for a virtual machine after explicitly
    re-computing the compliance check.
  - Use I(state=check) to invoke the compliance check on the virtual machine home
    directory and/or selected virtual disks.
author:
  - Ansible Eco Content Team (@eco-ansible-content)
extends_documentation_fragment:
  - vmware.vmware_rest.connection_params
options:
  state:
    description:
      - The operation to perform.
      - Use C(check) to re-compute storage policy compliance for the virtual machine.
    type: str
    choices:
      - check
    required: true
  vm:
    description:
      - Identifier of the virtual machine.
      - Must be an identifier (MOID) for a C(VirtualMachine) resource.
    type: str
    required: true
  vm_home:
    description:
      - Invoke compliance check on the virtual machine home directory when set to C(true).
      - If not set, the API defaults to checking the virtual machine home directory.
    type: bool
  disks:
    description:
      - Identifiers of virtual disks for which compliance should be checked.
      - Each element must be an identifier (MOID) for a C(Disk) resource.
      - If not set or empty, compliance check is invoked on all associated disks.
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
- name: Re-compute storage policy compliance for a virtual machine
  vmware.vmware_rest.vcenter_vm_storage_policy_compliance:
    state: check
    vm: vm-1009
  register: vm_compliance

- name: Re-compute compliance for VM home and specific disks
  vmware.vmware_rest.vcenter_vm_storage_policy_compliance:
    state: check
    vm: vm-1009
    vm_home: true
    disks:
      - "2000"
      - "2001"
  register: vm_compliance
"""

RETURN = r"""
value:
  description:
    - Storage policy compliance information for the virtual machine after the check.
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
    VmwareRestModuleBase,
)

COMPLIANCE_CHECK_PATH = "/vcenter/vm/{vm}/storage/policy/compliance"


class VmwareRestComplianceModule(VmwareRestModuleBase):
    PAYLOAD_FORMAT = {
        "check": {
            "query": {},
            "body": {"vm_home": "vm_home", "disks": "disks"},
            "path": {"vm": "vm"},
        },
    }

    def check_compliance(self):
        path = self.build_path(COMPLIANCE_CHECK_PATH)
        body = self.build_payload(self.PAYLOAD_FORMAT["check"])
        response = self.client.post(
            path,
            data=body if body else None,
            query={"action": "check"},
        )
        return {
            "changed": True,
            "value": response.json or {},
        }


def main():
    module_args = connection_params_argument_spec()
    module_args["state"] = {
        "type": "str",
        "choices": ["check"],
        "required": True,
    }
    module_args["vm"] = {"type": "str", "required": True}
    module_args["vm_home"] = {"type": "bool"}
    module_args["disks"] = {"type": "list", "elements": "str"}

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False,
    )

    compliance_module = VmwareRestComplianceModule(module)

    if module.params["state"] == "check":
        result = compliance_module.check_compliance()
    else:
        module.fail_json(msg="Unsupported state: {0}".format(module.params["state"]))

    module.exit_json(**result)


if __name__ == "__main__":
    main()
