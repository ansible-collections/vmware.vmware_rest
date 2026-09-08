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
short_description: Gather the disk to partition mapping of the vCenter Server Appliance.
description:
  - Gather information about the storage layout of the vCenter Server Appliance.
  - Returns the mapping between the appliance storage partitions and the hard disk
    numbers that are visible in the vSphere Client.
  - Use this module to discover which disk backs each partition before resizing storage
    with M(vmware.vmware_rest.appliance_system_storage).

author:
  - Ansible Eco Content Team (@eco-ansible-content)

extends_documentation_fragment:
  - vmware.vmware_rest.connection_params

options: {}

version_added: 5.0.0

requirements: []

notes:
  - Generated from vSphere API spec 9.1.0.
"""

EXAMPLES = r"""
- name: Gather the disk to partition mapping of the appliance
  vmware.vmware_rest.appliance_system_storage_info:
  register: storage_mapping

- name: Show the partition backed by each disk
  ansible.builtin.debug:
    msg: "Disk {{ item.disk }} backs partition {{ item.partition }}"
  loop: "{{ storage_mapping.info }}"
"""

RETURN = r"""
value:
  description:
    - Detailed information about the appliance storage partitions.
    - A list of disk to partition mapping entries.
  returned: On success
  type: raw
  sample:
    - disk: "1"
      partition: /
      description:
        default_message: "Root partition"
        id: com.vmware.applmgmt.storage.root
    - disk: "2"
      partition: /storage/log
      description:
        default_message: "Log partition"
        id: com.vmware.applmgmt.storage.log
info:
  description: A list of the disk to partition mapping entries on the appliance.
  returned: On success
  elements: dict
  type: list
  sample:
    - disk: "1"
      partition: /
      description:
        default_message: "Root partition"
        id: com.vmware.applmgmt.storage.root
    - disk: "2"
      partition: /storage/log
      description:
        default_message: "Log partition"
        id: com.vmware.applmgmt.storage.log
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

MOID_PARAMETER_HINTS = []

LIST_ENDPOINT = ""
ITEM_ENDPOINT = "/appliance/system/storage"


GET_OPERATION = OperationConfig(
    name="get",
    uri=ITEM_ENDPOINT,
    http_method="GET",
)


def create_module_argument_spec() -> dict:
    module_args = connection_params_argument_spec()
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
