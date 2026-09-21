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
module: vcenter_vm_hardware_disk_info
short_description: Gather information about the virtual disks of a virtual machine.
description:
  - Retrieve information about the virtual disks attached to a virtual machine.
  - When O(disk) is provided, detailed information about that single virtual disk is returned,
    including its label, adapter type and address, backing, and capacity.
  - When O(disk) is omitted, a list summarizing every virtual disk attached to the virtual machine is returned.
  - Use this module to inspect a virtual machine's disk layout, capacity, or backing files.

author:
  - Ansible Eco Content Team (@eco-ansible-content)

extends_documentation_fragment:
  - vmware.vmware_rest.connection_params

options:
  disk:
    description:
      - Identifier of a specific virtual disk to gather detailed information about.
      - When omitted, a summary of all virtual disks attached to the virtual machine is returned.
      - Must be an identifier (MOID) for a C(Disk) resource.
    type: str
    required: false
  vm:
    description:
      - Identifier of the virtual machine whose virtual disks should be gathered.
      - Must be an identifier (MOID) for a C(Vm) resource.
    type: str
    required: true

version_added: 5.0.0

requirements: []

notes:
  - Generated from vSphere API spec 9.1.0.
"""

EXAMPLES = r"""
- name: Gather information about all virtual disks on a virtual machine
  vmware.vmware_rest.vcenter_vm_hardware_disk_info:
    vm: vm-1013
  register: all_disks

- name: Gather information about a single virtual disk
  vmware.vmware_rest.vcenter_vm_hardware_disk_info:
    vm: vm-1013
    disk: "2000"
  register: disk_details
"""

RETURN = r"""
id:
  description: Identifier of the virtual disk that was queried.
  returned: When a single disk, with an identifier, was queried
  type: str
  sample: "2000"
value:
  description: Detailed information about a single virtual disk.
  returned: When a single disk was queried
  type: dict
  sample:
    label: Hard disk 1
    type: SCSI
    scsi:
      bus: 0
      unit: 0
    backing:
      type: VMDK_FILE
      vmdk_file: "[datastore1] my_vm/my_vm.vmdk"
    capacity: 17179869184
info:
  description: A list summarizing the virtual disks attached to the virtual machine.
  returned: When no specific disk was queried
  type: list
  sample:
    - disk: "2000"
    - disk: "2001"
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

MOID_PARAMETER_HINTS = ["vm", "disk"]

LIST_ENDPOINT = "/vcenter/vm/{vm}/hardware/disk"
ITEM_ENDPOINT = "/vcenter/vm/{vm}/hardware/disk/{disk}"


LIST_OPERATION = OperationConfig(
    name="list",
    uri=LIST_ENDPOINT,
    http_method="GET",
)

GET_OPERATION = OperationConfig(
    name="get",
    uri=ITEM_ENDPOINT,
    http_method="GET",
)


def create_module_argument_spec() -> dict:
    module_args = connection_params_argument_spec()
    module_args["disk"] = {
        "type": "str",
    }
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
        list_operation_config=LIST_OPERATION,
    )
    try:
        result = info_module.get_resource_info()
    except VmwareModuleError as e:
        module.fail_json(**e.to_module_fail_json_output())
    module.exit_json(**result)


if __name__ == "__main__":
    main()
