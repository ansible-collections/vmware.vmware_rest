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
module: vcenter_vm_hardware_serial_info
short_description: Gather information about the virtual serial ports of a virtual machine
description:
  - Retrieve information about the virtual serial ports attached to a virtual machine.
  - When O(port) is provided, detailed information about that single serial port is returned.
  - When O(port) is omitted, a summary list of all serial ports on the virtual machine is returned.
  - Use this module to inspect a virtual machine's serial port configuration, such as its
    backing type, connection state, and guest control settings.

author:
  - Ansible Eco Content Team (@eco-ansible-content)

extends_documentation_fragment:
  - vmware.vmware_rest.connection_params

options:
  port:
    description:
      - Identifier of a specific virtual serial port to query.
      - Must be the MOID (managed object identifier) of a serial C(Port) resource.
      - When omitted, information about all serial ports on the virtual machine is returned.
    type: str
    required: false
  vm:
    description:
      - Identifier of the virtual machine whose serial ports should be queried.
      - Must be the MOID (managed object identifier) of an existing C(Vm) resource.
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
- name: List all serial ports of a virtual machine
  vmware.vmware_rest.vcenter_vm_hardware_serial_info:
    vm: vm-1013

- name: Gather information about a specific serial port
  vmware.vmware_rest.vcenter_vm_hardware_serial_info:
    vm: vm-1013
    port: "9000"
"""

RETURN = r"""
id:
  description: MOID of the queried serial port.
  returned: When only one resource, with a MOID, was queried
  sample: "9000"
  type: str

value:
  description:
    - Raw output from the API response.
    - This output is maintained for consistency with version 4.x and earlier of this collection.
      It is recommended to switch to the info return key for a more consistent and documented output.
  returned: On success
  sample:
    allow_guest_control: false
    backing:
      auto_detect: false
      file: "[datastore1] vm-1013/port1.log"
      type: FILE
    label: "Serial port 1"
    start_connected: true
    state: NOT_CONNECTED
    yield_on_poll: false
  type: raw

info:
  description: A list of detailed information about the virtual serial ports.
  returned: On success
  sample:
    - allow_guest_control: false
      backing:
        auto_detect: false
        file: "[datastore1] vm-1013/port1.log"
        type: FILE
      label: "Serial port 1"
      port: "9000"
      start_connected: true
      state: NOT_CONNECTED
      yield_on_poll: false
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

MOID_PARAMETER_HINTS = ["vm", "port"]

LIST_ENDPOINT = "/vcenter/vm/{vm}/hardware/serial"
ITEM_ENDPOINT = "/vcenter/vm/{vm}/hardware/serial/{port}"


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
    module_args["port"] = {
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
