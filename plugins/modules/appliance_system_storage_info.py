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
module: appliance_system_storage_info
short_description: Get disk to partition mapping.
description:
  - Returns the mapping of vCenter Server appliance storage disks to partitions.
  - Each entry includes the disk identifier, partition name, and an optional description.
author:
  - Ansible Eco Content Team (@eco-ansible-content)
extends_documentation_fragment:
  - vmware.vmware_rest.connection_params
options: {}
version_added: 4.11.0
requirements: []
notes:
  - Generated from vSphere API spec 9.1.0.
  - Has support for vSphere API 7.0.3.
  - Has support for vSphere API 8.0.2.
"""

EXAMPLES = r"""
- name: Get the appliance storage information
  vmware.vmware_rest.appliance_system_storage_info:
  register: appliance_storage_info
"""

RETURN = r"""
value:
  description:
    - Disk to partition mapping for the vCenter Server appliance.
  returned: On success
  type: list
  elements: dict
  sample:
    - disk: "1"
      partition: lv_root_0
      description:
        default_message: Root partition
        id: storage.partition.lv_root_0
  contains:
    disk:
      description:
        - Disk number in the vSphere Client.
        - Must be an identifier (MOID) for a C(appliance.system.storage) resource.
      type: str
      sample: "1"
    partition:
      description:
        - Storage partition name.
      type: str
      sample: lv_root_0
    description:
      description:
        - Localized description of the partition.
      type: dict
      contains:
        id:
          description:
            - Identifier of the localizable message.
          type: str
        default_message:
          description:
            - Message text in the en_US locale.
          type: str
        args:
          description:
            - Positional arguments for the message template.
          type: list
          elements: str
        params:
          description:
            - Named arguments for the message template.
          type: dict
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.vmware.vmware_rest.plugins.module_utils._argument_spec import (
    connection_params_argument_spec,
)
from ansible_collections.vmware.vmware_rest.plugins.module_utils._module_base import (
    VmwareRestInfoModuleBase,
    normalize_list_response,
)

STORAGE_PATH = "/appliance/system/storage"


class VmwareRestInfoModule(VmwareRestInfoModuleBase):
    PAYLOAD_FORMAT = {
        "list": {"query": {}, "body": {}, "path": {}},
    }

    def get_info(self):
        response = self.client.get(STORAGE_PATH)
        if response.status == 404:
            return []
        return normalize_list_response(response.json)


def main():
    module_args = connection_params_argument_spec()

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
    )

    info_module = VmwareRestInfoModule(module)
    result = info_module.get_info()
    module.exit_json(value=result)


if __name__ == "__main__":
    main()
