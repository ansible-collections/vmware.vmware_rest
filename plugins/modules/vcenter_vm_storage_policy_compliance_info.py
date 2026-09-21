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
module: vcenter_vm_storage_policy_compliance_info
short_description: Retrieve the storage policy compliance status of a virtual machine.
description:
  - Gather the last known storage policy compliance information for a virtual machine.
  - Reports the overall compliance status along with per-entity compliance details for
    the virtual machine's home directory and its virtual disks.
  - This module reads cached compliance results and does not trigger a new check. Use
    M(vmware.vmware_rest.vcenter_vm_storage_policy_compliance) to run an on-demand check.

author:
  - Ansible Eco Content Team (@eco-ansible-content)

extends_documentation_fragment:
  - vmware.vmware_rest.connection_params

options:
  vm:
    description:
      - The identifier of the virtual machine to query.
      - Must be the MOID (managed object identifier) of a C(Vm) resource.
    type: str
    required: true

version_added: 5.0.0

requirements: []

notes:
  - Generated from vSphere API spec 9.1.0.
  - Compatible with vSphere API 7.0.3.
  - Compatible with vSphere API 8.0.2.
"""

EXAMPLES = r"""
- name: Look up the VM called test_vm1 in the inventory
  register: search_result
  vmware.vmware_rest.vcenter_vm_info:
    filter_names:
      - test_vm1

- name: Gather the storage policy compliance status of a VM
  vmware.vmware_rest.vcenter_vm_storage_policy_compliance_info:
    vm: '{{ search_result.value[0].vm }}'
  register: compliance_info
"""

RETURN = r"""
id:
  description: MOID of the queried virtual machine.
  returned: When only one resource, with a MOID, was queried.
  sample: vm-1009
  type: str
value:
  description:
    - Raw output from the API response.
    - This output is maintained for consistency with version 4.x and earlier of this collection.
      It is recommended to switch to the info return key for a more consistent and documented output.
  returned: On success.
  sample:
    overall_compliance: COMPLIANT
    vm_home:
      status: COMPLIANT
      check_time: '2026-09-14T10:30:00.000Z'
      policy: aa6d5a82-1c88-45da-85d3-3d74b91a5bad
      failure_cause: []
    disks:
      '2000':
        status: COMPLIANT
        check_time: '2026-09-14T10:30:00.000Z'
        policy: aa6d5a82-1c88-45da-85d3-3d74b91a5bad
        failure_cause: []
  type: raw
info:
  description: A list of detailed storage policy compliance information for the virtual machine.
  returned: On success.
  sample:
    - overall_compliance: COMPLIANT
      vm_home:
        status: COMPLIANT
        check_time: '2026-09-14T10:30:00.000Z'
        policy: aa6d5a82-1c88-45da-85d3-3d74b91a5bad
        failure_cause: []
      disks:
        '2000':
          status: COMPLIANT
          check_time: '2026-09-14T10:30:00.000Z'
          policy: aa6d5a82-1c88-45da-85d3-3d74b91a5bad
          failure_cause: []
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

MOID_PARAMETER_HINTS = ["vm"]

LIST_ENDPOINT = ""
ITEM_ENDPOINT = "/vcenter/vm/{vm}/storage/policy/compliance"


GET_OPERATION = OperationConfig(
    name="get",
    uri=ITEM_ENDPOINT,
    http_method="GET",
)


def create_module_argument_spec() -> dict:
    module_args = connection_params_argument_spec()
    module_args["vm"] = {
        "type": "str",
        "required": True,
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
