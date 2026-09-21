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
module: vcenter_vm_hardware_floppy_info
short_description: Gather information about virtual floppy drives on a virtual machine.
description:
  - Retrieve information about one or more virtual floppy drives attached to a VMware
    virtual machine.
  - Can return a list of all virtual floppy drives on a VM, or detailed information about
    a specific floppy drive identified by its MOID.
  - Use this module to discover floppy drive configurations such as backing type, connection
    state, and guest control settings.

author:
  - Ansible Eco Content Team (@eco-ansible-content)

deprecated:
  removed_in: 6.0.0
  why: Floppy drives are legacy hardware no longer commonly used
  alternative: Use modern storage options or M(vmware.vmware.vm) for comprehensive hardware management.

extends_documentation_fragment:
  - vmware.vmware_rest.connection_params

options:
  floppy:
    description:
      - Identifier of the virtual floppy drive to retrieve details for.
      - Must be an identifier (MOID) for a C(Floppy) resource, for example C(8000).
      - If omitted, all virtual floppy drives on the VM are returned.
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
- name: List all virtual floppy drives on a VM
  vmware.vmware_rest.vcenter_vm_hardware_floppy_info:
    vm: vm-1001
  register: all_floppies

- name: Get details about a specific virtual floppy drive
  vmware.vmware_rest.vcenter_vm_hardware_floppy_info:
    vm: vm-1001
    floppy: "8000"
  register: floppy_details
"""

RETURN = r"""
id:
  description: MOID of the queried virtual floppy drive.
  returned: When only one resource, with a MOID, was queried.
  sample: "8000"
  type: str
value:
  description:
    - Raw output from the API response.
    - This output is maintained for consistency with version 4.x and earlier of this collection.
      It is recommended to switch to the info return key for a more consistent and documented output.
  returned: On success.
  sample:
    label: Floppy drive 1
    backing:
      type: IMAGE_FILE
      image_file: "[datastore1] floppies/boot.flp"
    state: CONNECTED
    start_connected: true
    allow_guest_control: true
  type: raw
info:
  description: A list of virtual floppy drives matching the query.
  returned: On success.
  sample:
    - floppy: "8000"
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

MOID_PARAMETER_HINTS = ["vm", "floppy"]

LIST_ENDPOINT = "/vcenter/vm/{vm}/hardware/floppy"
ITEM_ENDPOINT = "/vcenter/vm/{vm}/hardware/floppy/{floppy}"


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
    module_args["floppy"] = {
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
