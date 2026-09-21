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
module: vcenter_vm_hardware_boot_device
short_description: Manage the boot device order of a virtual machine.
description:
  - Set the ordered list of devices that a virtual machine attempts to boot from.
  - The order of the entries determines the sequence in which the virtual machine tries each device during boot.
  - Each entry identifies a device class (such as CD-ROM or floppy) or a specific bootable device such as one or more virtual disks or an Ethernet adapter.
  - This module replaces the entire boot device order with the list provided in O(devices).
  - This module does not support idempotence. The module will always report a change.

author:
  - Ansible Eco Content Team (@eco-ansible-content)

extends_documentation_fragment:
  - vmware.vmware_rest.connection_params

options:
  state:
    description:
      - The desired state of the resource.
      - Use C(present) to create or update the resource.
    type: str
    default: present
    choices:
      - present
  vm:
    description:
      - Identifier of the virtual machine whose boot device order should be managed.
      - Must be an identifier (MOID) for a C(Vm) resource.
    type: str
    required: true
  devices:
    description:
      - The ordered list of devices the virtual machine attempts to boot from.
      - The virtual machine tries each entry in the order it appears in this list.
      - Providing this list replaces the current boot device order in its entirety.
    type: list
    required: false
    elements: dict
    suboptions:
      type:
        description:
          - The kind of device this boot entry represents.
          - C(CDROM) boots from a virtual CD-ROM device.
          - C(DISK) boots from one or more virtual disks listed in O(devices[].disks).
          - C(ETHERNET) boots over the network using the Ethernet adapter given in O(devices[].nic).
          - C(FLOPPY) boots from a virtual floppy drive.
        type: str
        required: true
        choices:
          - CDROM
          - DISK
          - ETHERNET
          - FLOPPY
      nic:
        description:
          - The virtual Ethernet adapter to boot from for this entry.
          - Relevant only when O(devices[].type) is C(ETHERNET).
          - Must be the identifier (MOID) of a virtual Ethernet adapter, as returned by M(vmware.vmware_rest.vcenter_vm_hardware_ethernet_info).
        type: str
        required: false
      disks:
        description:
          - The ordered list of virtual disks to boot from for this entry.
          - Relevant only when O(devices[].type) is C(DISK).
          - Each element must be the identifier (MOID) of a virtual disk, as returned by M(vmware.vmware_rest.vcenter_vm_hardware_disk_info).
        type: list
        required: false
        elements: str

version_added: 5.0.0

requirements: []

notes:
  - Generated from vSphere API spec 9.1.0.
  - Compatible with vSphere API 7.0.3.
  - Compatible with vSphere API 8.0.2.
"""

EXAMPLES = r"""
- name: Look up the virtual machine by name
  register: search_result
  vmware.vmware_rest.vcenter_vm_info:
    filter_names:
      - test_vm1

- name: Boot from the CD-ROM device only
  vmware.vmware_rest.vcenter_vm_hardware_boot_device:
    vm: '{{ search_result.value[0].vm }}'
    devices:
      - type: CDROM
    state: present

- name: Set a boot order that tries the CD-ROM, then a disk, then the network
  vmware.vmware_rest.vcenter_vm_hardware_boot_device:
    vm: '{{ search_result.value[0].vm }}'
    devices:
      - type: CDROM
      - type: DISK
        disks:
          - '16000'
      - type: ETHERNET
        nic: '4000'
    state: present
"""

RETURN = r"""
id:
  description: MOID of the virtual machine whose boot device order was managed.
  returned: When state is present, or when a resource is deleted, or when state is set to a supported action.
  sample: vm-1001
  type: str
value:
  description:
    - The raw API response body from the vCenter operation.
    - The boot device update endpoint returns no content on success, so this value is typically empty.
  returned: On success.
  sample: {}
  type: raw
"""


from ansible.module_utils.basic import AnsibleModule
from ansible_collections.vmware.vmware_rest.plugins.module_utils._argument_spec import (
    connection_params_argument_spec,
)
from ansible_collections.vmware.vmware_rest.plugins.module_utils._errors import (
    VmwareModuleError,
)
from ansible_collections.vmware.vmware_rest.plugins.module_utils._crud_module import (
    VmwareRestCrudModuleBase,
)
from ansible_collections.vmware.vmware_rest.plugins.module_utils._operation_configs import (
    OperationConfig,
)

MOID_PARAMETER_HINTS = ["vm"]

LIST_ENDPOINT = ""
ITEM_ENDPOINT = "/vcenter/vm/{vm}/hardware/boot/device"


GET_OPERATION = OperationConfig(
    name="get",
    uri=ITEM_ENDPOINT,
    http_method="GET",
)

UPDATE_OPERATION = OperationConfig(
    name="update",
    uri=ITEM_ENDPOINT,
    http_method="PUT",
    body_spec={
        "devices": {
            "required": True,
        },
    },
)


def create_module_argument_spec() -> dict:
    module_args = connection_params_argument_spec()
    module_args["devices"] = {
        "type": "list",
        "elements": "dict",
        "options": {
            "type": {
                "type": "str",
                "choices": ["CDROM", "DISK", "ETHERNET", "FLOPPY"],
                "required": True,
            },
            "nic": {
                "type": "str",
            },
            "disks": {
                "type": "list",
                "elements": "str",
            },
        },
    }
    module_args["vm"] = {
        "type": "str",
        "required": True,
    }
    module_args["state"] = {
        "type": "str",
        "choices": ["present"],
        "default": "present",
    }
    return module_args


def main():
    module = AnsibleModule(
        argument_spec=create_module_argument_spec(),
        supports_check_mode=True,
    )

    crud_module = VmwareRestCrudModuleBase(
        module=module,
        moid_parameter_hints=MOID_PARAMETER_HINTS,
        get_operation_config=GET_OPERATION,
        update_operation_config=UPDATE_OPERATION,
    )

    try:
        if module.params["state"] == "present":
            result = crud_module.ensure_present()
        else:
            module.fail_json(
                msg="Unsupported state: {0}".format(module.params["state"])
            )
    except VmwareModuleError as e:
        module.fail_json(**e.to_module_fail_json_output())

    module.exit_json(**result)


if __name__ == "__main__":
    main()
