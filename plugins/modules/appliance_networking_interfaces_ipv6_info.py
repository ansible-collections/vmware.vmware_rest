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
module: appliance_networking_interfaces_ipv6_info
short_description: Get IPv6 network configuration for a vCenter appliance interface.
description:
  - Returns IPv6 network configuration for a specific network interface on the
    vCenter Server appliance.
author:
  - Ansible Eco Content Team (@eco-ansible-content)
extends_documentation_fragment:
  - vmware.vmware_rest.connection_params
options:
  interface_name:
    description:
      - Network interface to query, for example C(nic0).
      - Must be an identifier (MOID) for a C(appliance.networking.interfaces) resource.
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
- name: Get IPv6 configuration for nic0
  vmware.vmware_rest.appliance_networking_interfaces_ipv6_info:
    interface_name: nic0
  register: ipv6_info
"""

RETURN = r"""
value:
  description:
    - IPv6 configuration for the queried network interface.
  returned: On success
  type: dict
  sample:
    dhcp: false
    autoconf: true
    addresses:
      - address: fc00:10:20:83:20c:29ff:fe94:bb5a
        prefix: 64
        origin: MANUAL
        status: PREFERRED
    default_gateway: fc00:10:20:83::1
    configurable: true
  contains:
    dhcp:
      description:
        - Whether DHCP is enabled for IPv6 on the interface.
      returned: On success
      type: bool
      sample: false
    autoconf:
      description:
        - Whether Stateless Address Autoconfiguration (SLAAC) is enabled.
      returned: On success
      type: bool
      sample: true
    addresses:
      description:
        - List of IPv6 addresses with their origins and statuses.
      returned: On success
      type: list
      elements: dict
      contains:
        address:
          description:
            - The IPv6 address.
          returned: On success
          type: str
          sample: fc00:10:20:83:20c:29ff:fe94:bb5a
        prefix:
          description:
            - The IPv6 CIDR prefix.
          returned: On success
          type: int
          sample: 64
        origin:
          description:
            - Origin of the IPv6 address.
          returned: On success
          type: str
          sample: MANUAL
          choices:
            - DHCP
            - RANDOM
            - MANUAL
            - LINKLAYER
            - OTHER
        status:
          description:
            - Status of the IPv6 address.
          returned: On success
          type: str
          sample: PREFERRED
          choices:
            - TENTATIVE
            - UNKNOWN
            - INACCESSIBLE
            - INVALID
            - DUPLICATE
            - PREFERRED
            - DEPRECATED
            - OPTIMISTIC
    default_gateway:
      description:
        - The default gateway for static IPv6 address assignment.
      returned: On success
      type: str
      sample: fc00:10:20:83::1
    configurable:
      description:
        - Whether the network interface IPv6 configuration can be changed.
      returned: On success
      type: bool
      sample: true
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.vmware.vmware_rest.plugins.module_utils._argument_spec import (
    connection_params_argument_spec,
)
from ansible_collections.vmware.vmware_rest.plugins.module_utils._module_base import (
    VmwareRestInfoModuleBase,
)

PATH = "/appliance/networking/interfaces/{interface_name}/ipv6"


class VmwareRestInfoModule(VmwareRestInfoModuleBase):
    PAYLOAD_FORMAT = {
        "get": {
            "query": {},
            "body": {},
            "path": {"interface_name": "interface_name"},
        },
    }

    def get_info(self):
        path = self.build_path(PATH)
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
