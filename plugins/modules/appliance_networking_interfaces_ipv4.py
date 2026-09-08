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
module: appliance_networking_interfaces_ipv4
short_description: Manage the IPv4 configuration of a vCenter Server Appliance network interface.
description:
  - Configure the IPv4 settings of a specific network interface on the vCenter Server Appliance.
  - The address can be assigned automatically by a DHCP server, set statically, or left unconfigured.
  - When O(mode=STATIC), provide O(address) and O(prefix), and optionally O(default_gateway).
  - Use M(vmware.vmware_rest.appliance_networking_interfaces_ipv4_info) to view the current IPv4 configuration.

author:
  - Ansible Eco Content Team (@eco-ansible-content)

extends_documentation_fragment:
  - vmware.vmware_rest.connection_params

options:
  state:
    description:
      - The desired state of the interface IPv4 configuration.
      - Use C(present) to apply the given IPv4 settings.
    type: str
    default: present
    choices:
      - present
  interface_name:
    description:
      - The name of the network interface to configure, for example C(nic0).
      - The value is the identifier of an interface returned by M(vmware.vmware_rest.appliance_networking_interfaces_info).
    type: str
    required: true
  mode:
    description:
      - How the IPv4 address is assigned to the interface.
      - Use C(DHCP) to have the address assigned automatically by a DHCP server.
      - Use C(STATIC) to assign a fixed address, which requires O(address) and O(prefix).
      - Use C(UNCONFIGURED) to disable IPv4 on the interface.
      - This property was added in vSphere API 6.7.
    type: str
    required: false
  address:
    description:
      - The IPv4 address to assign to the interface, for example C(10.20.80.191).
      - Only relevant when O(mode=STATIC).
      - This property was added in vSphere API 6.7.
    type: str
    required: false
  prefix:
    description:
      - The IPv4 CIDR prefix length, for example C(24) for a 255.255.255.0 netmask.
      - Only relevant when O(mode=STATIC).
      - This property was added in vSphere API 6.7.
    type: int
    required: false
  default_gateway:
    description:
      - The IPv4 address of the default gateway for the appliance.
      - This sets the global default gateway using the specified gateway address and interface, replacing any
        existing default gateway. A link-local gateway address is added only for this interface. Configuring
        multiple global default gateways through different interfaces is not supported.
      - This property was added in vSphere API 6.7.
    type: str
    required: false

version_added: 5.0.0

requirements: []

notes:
  - Generated from vSphere API spec 9.1.0.
"""

EXAMPLES = r"""
- name: Configure nic0 to obtain an IPv4 address via DHCP
  vmware.vmware_rest.appliance_networking_interfaces_ipv4:
    interface_name: nic0
    mode: DHCP
    state: present

- name: Assign a static IPv4 address to nic0
  vmware.vmware_rest.appliance_networking_interfaces_ipv4:
    interface_name: nic0
    mode: STATIC
    address: 10.20.80.191
    prefix: 24
    default_gateway: 10.20.80.1
    state: present

- name: Disable IPv4 on nic0
  vmware.vmware_rest.appliance_networking_interfaces_ipv4:
    interface_name: nic0
    mode: UNCONFIGURED
    state: present
"""

RETURN = r"""
value:
  description: The raw API response body from the vCenter operation. Empty when the operation returns no content.
  returned: On success
  type: raw
  sample: {}
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

MOID_PARAMETER_HINTS = ["interface_name"]

LIST_ENDPOINT = ""
ITEM_ENDPOINT = "/appliance/networking/interfaces/{interface_name}/ipv4"


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
        "mode": {
            "required": True,
        },
        "address": {
            "required": False,
        },
        "prefix": {
            "required": False,
        },
        "default_gateway": {
            "required": False,
        },
    },
)


def create_module_argument_spec() -> dict:
    module_args = connection_params_argument_spec()
    module_args["address"] = {
        "type": "str",
    }
    module_args["default_gateway"] = {
        "type": "str",
    }
    module_args["interface_name"] = {
        "type": "str",
        "required": True,
    }
    module_args["mode"] = {
        "type": "str",
    }
    module_args["prefix"] = {
        "type": "int",
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
