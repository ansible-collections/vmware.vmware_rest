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
short_description: Retrieves guest operating system identification information for a virtual machine.
description:
  - Returns guest operating system identification information for a virtual machine in vCenter.
  - Includes guest OS identifier, family, full name, hostname, and IP address when available.
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
- name: Get guest identity information for a virtual machine
  vmware.vmware_rest.vcenter_vm_guest_identity_info:
    vm: vm-1001
  register: guest_identity

- name: Display guest hostname
  ansible.builtin.debug:
    msg: "Guest hostname is {{ guest_identity.value.host_name }}"
"""

RETURN = r"""
value:
  description:
    - Guest operating system identification information.
  returned: On success
  type: dict
  sample:
    family: LINUX
    full_name:
      args: []
      default_message: Red Hat Enterprise Linux 9 (64-bit)
      id: vmsg.guestos.rhel9_64Guest.label
    host_name: my-vm.example.com
    name: RHEL_9_64
    ip_address: 192.0.2.10
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.vmware.vmware_rest.plugins.module_utils._argument_spec import (
    connection_params_argument_spec,
)
from ansible_collections.vmware.vmware_rest.plugins.module_utils._module_base import (
    VmwareRestInfoModuleBase,
)

IDENTITY_PATH = "/vcenter/vm/{vm}/guest/identity"


class VmwareRestInfoModule(VmwareRestInfoModuleBase):
    PAYLOAD_FORMAT = {
        "get": {"query": {}, "body": {}, "path": {"vm": "vm"}},
    }

    def get_info(self):
        path = self.build_path(IDENTITY_PATH)
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
