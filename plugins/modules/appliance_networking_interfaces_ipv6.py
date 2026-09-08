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
module: appliance_networking_interfaces_ipv6
short_description: Manage the IPv6 configuration of a vCenter Server Appliance network interface.
description:
  - Configure the IPv6 settings of a specific network interface on the vCenter Server Appliance.
  - Addresses can be assigned automatically by a DHCP server, by Stateless Address Autoconfiguration (SLAAC),
    or set statically, and an optional default gateway can be configured.
  - Use M(vmware.vmware_rest.appliance_networking_interfaces_ipv6_info) to view the current IPv6 configuration.

author:
  - Ansible Eco Content Team (@eco-ansible-content)

extends_documentation_fragment:
  - vmware.vmware_rest.connection_params

options:
  state:
    description:
      - The desired state of the interface IPv6 configuration.
      - Use C(present) to apply the given IPv6 settings.
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
  dhcp:
    description:
      - Whether the interface obtains an IPv6 address automatically from a DHCP server.
      - This property was added in vSphere API 6.7.
    type: bool
    required: false
  autoconf:
    description:
      - Whether the interface obtains an IPv6 address through Stateless Address Autoconfiguration (SLAAC).
      - This property was added in vSphere API 6.7.
    type: bool
    required: false
  addresses:
    description:
      - The list of IPv6 addresses to assign statically to the interface.
      - This property was added in vSphere API 6.7.
    type: list
    required: false
    elements: dict
    suboptions:
      address:
        description:
          - The IPv6 address, for example C(fc00:10:20:83:20c:29ff:fe94:bb5a).
          - This property was added in vSphere API 6.7.
        type: str
        required: true
      prefix:
        description:
          - The IPv6 CIDR prefix length, for example C(64).
          - This property was added in vSphere API 6.7.
        type: int
        required: true
  default_gateway:
    description:
      - The IPv6 address of the default gateway for static address assignment.
      - This sets the global IPv6 default gateway using the specified gateway address and interface, replacing any
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
- name: Configure nic0 to obtain an IPv6 address via DHCP
  vmware.vmware_rest.appliance_networking_interfaces_ipv6:
    interface_name: nic0
    dhcp: true
    autoconf: false
    addresses: []
    default_gateway: ""
    state: present

- name: Enable SLAAC autoconfiguration on nic0
  vmware.vmware_rest.appliance_networking_interfaces_ipv6:
    interface_name: nic0
    dhcp: false
    autoconf: true
    addresses: []
    default_gateway: ""
    state: present

- name: Assign a static IPv6 address to nic0
  vmware.vmware_rest.appliance_networking_interfaces_ipv6:
    interface_name: nic0
    dhcp: false
    autoconf: false
    addresses:
      - address: fc00:10:20:83:20c:29ff:fe94:bb5a
        prefix: 64
    default_gateway: fc00:10:20:83::1
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
ITEM_ENDPOINT = "/appliance/networking/interfaces/{interface_name}/ipv6"


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
        "dhcp": {
            "required": True,
        },
        "autoconf": {
            "required": True,
        },
        "addresses": {
            "required": True,
        },
        "default_gateway": {
            "required": True,
        },
    },
)


def create_module_argument_spec() -> dict:
    module_args = connection_params_argument_spec()
    module_args["addresses"] = {
        "type": "list",
        "elements": "dict",
        "options": {
            "address": {
                "type": "str",
                "required": True,
            },
            "prefix": {
                "type": "int",
                "required": True,
            },
        },
    }
    module_args["autoconf"] = {
        "type": "bool",
    }
    module_args["default_gateway"] = {
        "type": "str",
    }
    module_args["dhcp"] = {
        "type": "bool",
    }
    module_args["interface_name"] = {
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
