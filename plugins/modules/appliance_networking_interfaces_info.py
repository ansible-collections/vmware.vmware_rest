#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright: (c) 2026, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#
# This module is generated using LLM agents and skills defined in the vmware.vmware_rest repository.
# See: https://github.com/ansible-collections/vmware.vmware_rest
#

DOCUMENTATION = r"""
module: appliance_networking_interfaces_info
short_description: Get information about vCenter appliance network interfaces.
description:
  - Returns information about network interfaces on the vCenter Server appliance.
  - When I(interface_name) is specified, returns information for that interface only.
  - When I(interface_name) is omitted, lists all available network interfaces, including
    those that are not yet configured.
author:
  - Ansible Eco Content Team (@eco-ansible-content)
extends_documentation_fragment:
  - vmware.vmware_rest.connection_params
options:
  interface_name:
    description:
      - Network interface name, for example C(nic0).
      - Must be an identifier (MOID) for a C(com.vmware.appliance.networking.interfaces) resource.
      - When specified, only that interface is returned.
    type: str
version_added: 4.11.0
requirements: []
notes:
  - Generated from vSphere API spec 9.1.0.
  - Has support for vSphere API 7.0.3.
  - Has support for vSphere API 8.0.2.
"""

EXAMPLES = r"""
- name: List all network interfaces
  vmware.vmware_rest.appliance_networking_interfaces_info:
  register: network_interfaces

- name: Get a specific network interface
  vmware.vmware_rest.appliance_networking_interfaces_info:
    interface_name: nic0
  register: nic0_interface
"""

RETURN = r"""
value:
  description:
    - Network interface information.
    - Returns a list of interface dictionaries when I(interface_name) is omitted.
    - Returns a single interface dictionary when I(interface_name) is specified.
  returned: On success
  type: raw
  sample:
    - mac: "00:0C:29:94:BB:5A"
      name: nic0
      status: up
  contains:
    name:
      description:
        - Interface name, for example C(nic0) or C(nic1).
      type: str
      sample: nic0
    status:
      description:
        - Interface status.
        - C(down) indicates the interface is down.
        - C(up) indicates the interface is up.
      type: str
      choices:
        - down
        - up
      sample: up
    mac:
      description:
        - MAC address.
      type: str
      sample: "00:0C:29:94:BB:5A"
    ipv4:
      description:
        - IPv4 address information.
        - This property is absent when IPv4 is not enabled.
      type: dict
      contains:
        configurable:
          description:
            - Whether the network interface IPv4 configuration is configurable.
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
            - IPv4 address.
          type: str
          sample: 10.20.80.191
        prefix:
          description:
            - IPv4 CIDR prefix.
          type: int
          sample: 24
        default_gateway:
          description:
            - IPv4 default gateway address.
          type: str
    ipv6:
      description:
        - IPv6 address information.
        - This property is absent when IPv6 is not enabled.
      type: dict
      contains:
        dhcp:
          description:
            - Whether DHCP is enabled for IPv6.
          type: bool
        autoconf:
          description:
            - Whether Stateless Address Autoconfiguration (SLAAC) is enabled.
          type: bool
        configurable:
          description:
            - Whether the network interface IPv6 configuration is configurable.
          type: bool
        default_gateway:
          description:
            - IPv6 default gateway address.
          type: str
        addresses:
          description:
            - IPv6 addresses with their origins and statuses.
          type: list
          elements: dict
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.vmware.vmware_rest.plugins.module_utils._argument_spec import (
    connection_params_argument_spec,
)
from ansible_collections.vmware.vmware_rest.plugins.module_utils._module_base import (
    VmwareRestInfoModuleBase,
)

LIST_PATH = "/appliance/networking/interfaces"
INTERFACE_PATH = "/appliance/networking/interfaces/{interface_name}"


class VmwareRestInfoModule(VmwareRestInfoModuleBase):
    PAYLOAD_FORMAT = {
        "list": {"query": {}, "body": {}, "path": {}},
        "get": {"query": {}, "body": {}, "path": {"interface_name": "interface_name"}},
    }

    def _get_interface(self, interface_name):
        response = self.client.get(
            self.build_path(INTERFACE_PATH, {"interface_name": interface_name})
        )
        if response.status == 404:
            return None
        return response.json

    def get_info(self):
        interface_name = self.params.get("interface_name")
        if interface_name:
            interface = self._get_interface(interface_name)
            if interface is None:
                self.module.fail_json(
                    msg="Network interface not found: {0}".format(interface_name)
                )
            return interface

        return self.fetch_list(LIST_PATH, self.PAYLOAD_FORMAT["list"])


def main():
    module_args = connection_params_argument_spec()
    module_args["interface_name"] = {"type": "str"}

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
    )

    info_module = VmwareRestInfoModule(module)
    result = info_module.get_info()
    module.exit_json(value=result)


if __name__ == "__main__":
    main()
