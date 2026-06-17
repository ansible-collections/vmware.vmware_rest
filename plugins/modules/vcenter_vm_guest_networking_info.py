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
module: vcenter_vm_guest_networking_info
short_description: Retrieves guest operating system network configuration information.
description:
  - Returns information about the network configuration in the guest operating system of a virtual machine.
  - Includes DNS configuration and DNS-assigned values when reported by VMware Tools.
  - Requires VMware Tools to be running in the guest.
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
- name: Get guest networking information for a virtual machine
  vmware.vmware_rest.vcenter_vm_guest_networking_info:
    vm: vm-1001
  register: guest_networking_info

- name: Display guest DNS servers
  ansible.builtin.debug:
    var: guest_networking_info.value.dns.ip_addresses
  when:
    - guest_networking_info.value is defined
    - guest_networking_info.value.dns is defined
"""

RETURN = r"""
value:
  description:
    - Guest operating system networking configuration.
  returned: On success
  type: dict
  contains:
    dns_values:
      description:
        - Client DNS values assigned by a Domain Name Server.
      returned: success
      type: dict
      sample:
        host_name: esx01
        domain_name: example.com
    dns:
      description:
        - Client DNS configuration describing how DNS queries are resolved.
      returned: success
      type: dict
      sample:
        ip_addresses:
          - 192.0.2.1
          - 2001:db8::1
        search_domains:
          - example.com
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.vmware.vmware_rest.plugins.module_utils._argument_spec import (
    connection_params_argument_spec,
)
from ansible_collections.vmware.vmware_rest.plugins.module_utils._module_base import (
    VmwareRestInfoModuleBase,
)

NETWORKING_PATH = "/vcenter/vm/{vm}/guest/networking"


class VmwareRestInfoModule(VmwareRestInfoModuleBase):
    PAYLOAD_FORMAT = {
        "get": {"query": {}, "body": {}, "path": {"vm": "vm"}},
    }

    def get_info(self):
        path = self.build_path(NETWORKING_PATH)
        response = self.client.get(path)
        if response.status == 404:
            return {}
        return response.json


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
