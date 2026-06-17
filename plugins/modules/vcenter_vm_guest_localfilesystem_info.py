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
module: vcenter_vm_guest_localfilesystem_info
short_description: Retrieves guest operating system local file system information.
description:
  - Returns details of local file systems configured in the guest operating system of a virtual machine.
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
- name: Get guest local file system information for a virtual machine
  vmware.vmware_rest.vcenter_vm_guest_localfilesystem_info:
    vm: vm-1001
  register: guest_localfilesystem_info

- name: Display free space on guest file systems
  ansible.builtin.debug:
    msg: "Mount {{ item.key }} has {{ item.value.free_space }} bytes free"
  loop: "{{ guest_localfilesystem_info.value | dict2items }}"
  when: guest_localfilesystem_info.value is defined
"""

RETURN = r"""
value:
  description:
    - Map of local file system mount paths to file system details.
    - Each key is a mount path in the guest operating system.
    - Each value contains capacity, free space, and optional filesystem type and disk mappings.
  returned: On success
  type: dict
  sample:
    /:
      capacity: 107374182400
      free_space: 53687091200
      filesystem: ext4
      mappings:
        - disk: "2000"
    C:\:
      capacity: 536870912000
      free_space: 268435456000
      filesystem: NTFS
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.vmware.vmware_rest.plugins.module_utils._argument_spec import (
    connection_params_argument_spec,
)
from ansible_collections.vmware.vmware_rest.plugins.module_utils._module_base import (
    VmwareRestInfoModuleBase,
)

LOCAL_FILESYSTEM_PATH = "/vcenter/vm/{vm}/guest/local-filesystem"


class VmwareRestInfoModule(VmwareRestInfoModuleBase):
    PAYLOAD_FORMAT = {
        "get": {"query": {}, "body": {}, "path": {"vm": "vm"}},
    }

    def get_info(self):
        path = self.build_path(LOCAL_FILESYSTEM_PATH)
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
