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
module: vcenter_vm_guest_networking_routes_info
short_description: Retrieves guest operating system network routing information for a virtual machine.
description:
  - Returns information about network routing in the guest operating system of a virtual machine.
  - Each route describes a host, network, or default destination reachable through a gateway.
  - Requires VMware Tools to be running in the guest operating system.
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
- name: Get guest network routes for a virtual machine
  vmware.vmware_rest.vcenter_vm_guest_networking_routes_info:
    vm: vm-1001
  register: guest_routes

- name: Display guest default gateway routes
  ansible.builtin.debug:
    var: guest_routes.value
  when: guest_routes.value is defined
"""

RETURN = r"""
value:
  description:
    - Guest operating system network routing information.
  returned: On success
  type: list
  elements: dict
  sample:
    - network: 0.0.0.0
      prefix_length: 0
      gateway_address: 192.0.2.1
      interface_index: 0
  contains:
    network:
      description:
        - IP address of the destination IP network.
      type: str
      sample: 0.0.0.0
    prefix_length:
      description:
        - The prefix length of the destination network.
        - For IPv4 the value range is 0-32. For IPv6 the value range is 0-128.
      type: int
      sample: 0
    gateway_address:
      description:
        - Unicast IP address of the next hop router for this route.
      type: str
      sample: 192.0.2.1
    interface_index:
      description:
        - Index of the network interface associated with this route.
        - Refers to the relative position of an element in the list returned by
          M(vmware.vmware_rest.vcenter_vm_guest_networking_interfaces_info).
      type: int
      sample: 0
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.vmware.vmware_rest.plugins.module_utils._argument_spec import (
    connection_params_argument_spec,
)
from ansible_collections.vmware.vmware_rest.plugins.module_utils._module_base import (
    VmwareRestInfoModuleBase,
)

ROUTES_PATH = "/vcenter/vm/{vm}/guest/networking/routes"


class VmwareRestInfoModule(VmwareRestInfoModuleBase):
    PAYLOAD_FORMAT = {
        "get": {"query": {}, "body": {}, "path": {"vm": "vm"}},
    }

    def get_info(self):
        path = self.build_path(ROUTES_PATH)
        return self.fetch_list(path, self.PAYLOAD_FORMAT["get"])


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
