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
module: vcenter_vm_guest_identity_info
short_description: Returns identification information about the guest operating system of a virtual machine.
description:
  - Returns identification details that VMware Tools reports about the guest operating system running inside a virtual machine.
  - The information includes the guest operating system family, its full product name, the configured hostname, and the primary IP address.
  - VMware Tools must be installed and running in the guest for this information to be available.

author:
  - Ansible Eco Content Team (@eco-ansible-content)

extends_documentation_fragment:
  - vmware.vmware_rest.connection_params

options:
  vm:
    description:
      - Identifier of the virtual machine whose guest identity information is returned.
      - Must be the managed object identifier (MOID) of a virtual machine, as returned by M(vmware.vmware_rest.vcenter_vm_info).
    type: str
    required: true

version_added: 5.0.0

requirements: []

notes:
  - Generated from vSphere API spec 9.1.0.
"""

EXAMPLES = r"""
- name: Look up the VM called test_vm1 in the inventory
  vmware.vmware_rest.vcenter_vm_info:
    filter_names:
      - test_vm1
  register: search_result

- name: Get guest identity information for the VM
  vmware.vmware_rest.vcenter_vm_guest_identity_info:
    vm: "{{ search_result.value[0].vm }}"
  register: guest_identity

- name: Display the guest hostname and IP address
  ansible.builtin.debug:
    msg: "{{ guest_identity.value.host_name }} has address {{ guest_identity.value.ip_address }}"
"""

RETURN = r"""
value:
  description:
    - Guest operating system identification details for the virtual machine.
    - Returned as a dictionary because this endpoint always describes a single virtual machine.
  returned: On success
  type: dict
  sample:
    name: RHEL_9_64
    family: LINUX
    full_name:
      id: vmsg.guestos.rhel9_64Guest.label
      default_message: Red Hat Enterprise Linux 9 (64-bit)
      args: []
    host_name: test-vm1.example.com
    ip_address: 10.0.2.15
info:
  description:
    - The same information as RV(value), returned as a list for consistency with other info modules.
    - This endpoint returns a single item, so the list always contains one element.
  returned: On success
  type: list
  elements: dict
  sample:
    - name: RHEL_9_64
      family: LINUX
      full_name:
        id: vmsg.guestos.rhel9_64Guest.label
        default_message: Red Hat Enterprise Linux 9 (64-bit)
        args: []
      host_name: test-vm1.example.com
      ip_address: 10.0.2.15
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
ITEM_ENDPOINT = "/vcenter/vm/{vm}/guest/identity"


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
