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
module: vcenter_vm_guest_networking_routes_info
short_description: Returns information about the network routing in the guest operating system of a virtual machine.
description:
  - Returns the network routing table reported by VMware Tools for a virtual machine's guest operating system.
  - Each route describes a destination network, its prefix length, the gateway used to reach it, and the guest network interface it is associated with.
  - VMware Tools must be installed and running in the guest for this information to be available.

author:
  - Ansible Eco Content Team (@eco-ansible-content)

extends_documentation_fragment:
  - vmware.vmware_rest.connection_params

options:
  vm:
    description:
      - Identifier of the virtual machine whose guest network routing information is returned.
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

- name: Get guest network routing information for the VM
  vmware.vmware_rest.vcenter_vm_guest_networking_routes_info:
    vm: "{{ search_result.value[0].vm }}"
  register: guest_routes

- name: Display the guest network routes
  ansible.builtin.debug:
    var: guest_routes.info
"""

RETURN = r"""
value:
  description:
    - Information about the network routes configured in the guest operating system.
    - Returned as a single route dictionary when the guest reports exactly one route, or as a list of route dictionaries when it reports more than one.
  returned: On success
  type: raw
  sample:
    - network: 0.0.0.0
      prefix_length: 0
      gateway_address: 10.0.2.2
      interface_index: 0
    - network: 10.0.2.0
      prefix_length: 24
      interface_index: 0
info:
  description:
    - A list of all network routes reported by the guest operating system.
    - This is always a list, regardless of how many routes the guest reports.
  returned: On success
  type: list
  elements: dict
  sample:
    - network: 0.0.0.0
      prefix_length: 0
      gateway_address: 10.0.2.2
      interface_index: 0
    - network: 10.0.2.0
      prefix_length: 24
      interface_index: 0
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
ITEM_ENDPOINT = "/vcenter/vm/{vm}/guest/networking/routes"


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
