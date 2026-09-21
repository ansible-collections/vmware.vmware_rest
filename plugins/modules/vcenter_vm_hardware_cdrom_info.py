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
module: vcenter_vm_hardware_cdrom_info
short_description: Gather information about virtual CD-ROM drives on a virtual machine.
description:
  - Retrieve information about one or more virtual CD-ROM drives attached to a VMware
    virtual machine.
  - Can return a list of all virtual CD-ROM drives on a VM, or detailed information about
    a specific CD-ROM drive identified by its MOID.
  - Use this module to discover CD-ROM configurations such as the backing type (ISO file,
    host device, or client device), the adapter (IDE or SATA) the drive is attached to,
    the connection state, and guest control settings.

author:
  - Ansible Eco Content Team (@eco-ansible-content)

extends_documentation_fragment:
  - vmware.vmware_rest.connection_params

options:
  cdrom:
    description:
      - Identifier of the virtual CD-ROM drive to retrieve details for.
      - Must be an identifier (MOID) for a C(Cdrom) resource, for example C(16000).
      - If omitted, all virtual CD-ROM drives on the VM are returned.
    type: str
    required: false
  vm:
    description:
      - Identifier of the virtual machine to query.
      - Must be an identifier (MOID) for a C(Vm) resource.
    type: str
    required: true

version_added: 5.0.0

requirements: []

notes:
  - Generated from vSphere API spec 9.1.0.
  - Compatible with vSphere API 7.0.3.
  - Compatible with vSphere API 8.0.2.
"""

EXAMPLES = r"""
- name: List all virtual CD-ROM drives on a VM
  vmware.vmware_rest.vcenter_vm_hardware_cdrom_info:
    vm: vm-1001
  register: all_cdroms

- name: Get details about a specific virtual CD-ROM drive
  vmware.vmware_rest.vcenter_vm_hardware_cdrom_info:
    vm: vm-1001
    cdrom: "16000"
  register: cdrom_details
"""

RETURN = r"""
id:
  description: MOID of the queried virtual CD-ROM drive.
  returned: When only one resource, with a MOID, was queried.
  sample: "16000"
  type: str
value:
  description:
    - Raw output from the API response.
    - This output is maintained for consistency with version 4.x and earlier of this collection.
      It is recommended to switch to the info return key for a more consistent and documented output.
  returned: On success.
  sample:
    label: CD/DVD drive 1
    type: SATA
    sata:
      bus: 0
      unit: 0
    backing:
      type: ISO_FILE
      iso_file: "[datastore1] ISOs/installer.iso"
    state: CONNECTED
    start_connected: true
    allow_guest_control: true
  type: raw
info:
  description: A list of virtual CD-ROM drives matching the query.
  returned: On success.
  sample:
    - cdrom: "16000"
  type: list
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

MOID_PARAMETER_HINTS = ["vm", "cdrom"]

LIST_ENDPOINT = "/vcenter/vm/{vm}/hardware/cdrom"
ITEM_ENDPOINT = "/vcenter/vm/{vm}/hardware/cdrom/{cdrom}"


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
    module_args["cdrom"] = {
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
