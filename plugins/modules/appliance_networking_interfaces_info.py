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
module: appliance_networking_interfaces_info
short_description: Retrieve information about the network interfaces of a vCenter Server Appliance.
description:
  - Gather details about the network interfaces present on the vCenter Server Appliance.
  - When O(interface_name) is provided, only that interface is returned; otherwise all interfaces are listed.
  - The returned information includes the interface name, link status, MAC address, and the IPv4 and IPv6
    address configuration when enabled.

author:
  - Ansible Eco Content Team (@eco-ansible-content)

extends_documentation_fragment:
  - vmware.vmware_rest.connection_params

options:
  interface_name:
    description:
      - The name of a specific network interface to query, for example C(nic0).
      - When omitted, information about all network interfaces on the appliance is returned.
    type: str
    required: false

version_added: 5.0.0

requirements: []

notes:
  - Generated from vSphere API spec 9.1.0.
"""

EXAMPLES = r"""
- name: List all network interfaces on the appliance
  vmware.vmware_rest.appliance_networking_interfaces_info:
  register: result

- name: Get information about a specific network interface
  vmware.vmware_rest.appliance_networking_interfaces_info:
    interface_name: nic0
  register: result
"""

RETURN = r"""
value:
  description:
    - Detailed information about the queried network interface(s).
    - A single interface as a dictionary when O(interface_name) is set, otherwise a list of interfaces.
  returned: On success
  sample:
    mac: "00:0c:29:94:bb:5a"
    name: nic0
    status: up
    ipv4:
      address: 192.168.123.8
      configurable: true
      default_gateway: 192.168.123.1
      mode: STATIC
      prefix: 24
  type: raw
info:
  description: A list of detailed information about the appliance network interfaces.
  returned: On success
  sample:
    - mac: "00:0c:29:94:bb:5a"
      name: nic0
      status: up
      ipv4:
        address: 192.168.123.8
        configurable: true
        default_gateway: 192.168.123.1
        mode: STATIC
        prefix: 24
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

MOID_PARAMETER_HINTS = ["interface_name"]

LIST_ENDPOINT = "/appliance/networking/interfaces"
ITEM_ENDPOINT = "/appliance/networking/interfaces/{interface_name}"


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
    module_args["interface_name"] = {
        "type": "str",
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
