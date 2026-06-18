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
module: appliance_networking_interfaces_ipv4_info
short_description: Get IPv4 network configuration for a vCenter appliance interface
description:
  - Returns the IPv4 network configuration for a specific network interface on the
    vCenter Server appliance.
  - The response includes address assignment mode, optional address and prefix, and
    whether the interface IPv4 settings are configurable.
author:
  - Ansible Eco Content Team (@eco-ansible-content)
extends_documentation_fragment:
  - vmware.vmware_rest.connection_params
options:
  interface_name:
    description:
      - Network interface to query, for example C(nic0).
      - Must be an identifier (MOID) for a C(com.vmware.appliance.networking.interfaces)
        resource.
    type: str
    required: true
version_added: 4.11.0
requirements: []
notes:
  - Generated from vSphere API spec 9.1.0.
  - Has support for vSphere API 7.0.3.
  - Has support for vSphere API 8.0.2.
"""

EXAMPLES = r"""
- name: Get IPv4 configuration for nic0
  vmware.vmware_rest.appliance_networking_interfaces_ipv4_info:
    interface_name: nic0
  register: nic0_ipv4
"""

RETURN = r"""
value:
  description:
    - IPv4 configuration for the queried network interface.
  returned: On success
  type: dict
  sample:
    configurable: true
    mode: STATIC
    address: 10.20.80.191
    prefix: 24
    default_gateway: 10.20.80.1
  contains:
    configurable:
      description:
        - Whether the specified network interface IPv4 settings are configurable.
      type: bool
    mode:
      description:
        - IPv4 address assignment mode.
      type: str
      choices:
        - DHCP
        - STATIC
        - UNCONFIGURED
    address:
      description:
        - IPv4 address when I(mode) is C(STATIC) or C(DHCP).
      type: str
    prefix:
      description:
        - IPv4 CIDR prefix when I(mode) is C(STATIC) or C(DHCP).
      type: int
    default_gateway:
      description:
        - IPv4 default gateway when I(mode) is C(STATIC) or C(DHCP).
      type: str
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.vmware.vmware_rest.plugins.module_utils._argument_spec import (
    connection_params_argument_spec,
)
from ansible_collections.vmware.vmware_rest.plugins.module_utils._module_base import (
    VmwareRestInfoModuleBase,
)

IPV4_PATH = "/appliance/networking/interfaces/{interface_name}/ipv4"


class VmwareRestInfoModule(VmwareRestInfoModuleBase):
    PAYLOAD_FORMAT = {
        "get": {
            "query": {},
            "body": {},
            "path": {"interface_name": "interface_name"},
        },
    }

    def get_info(self):
        path = self.build_path(IPV4_PATH)
        response = self.client.get(path)
        if response.status == 404:
            return None
        return response.json


def main():
    module_args = connection_params_argument_spec()
    module_args["interface_name"] = {"type": "str", "required": True}

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
    )

    info_module = VmwareRestInfoModule(module)
    result = info_module.get_info()
    module.exit_json(value=result)


if __name__ == "__main__":
    main()
