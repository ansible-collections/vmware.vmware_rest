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
module: appliance_networking_info
short_description: Get networking information for all configured interfaces.
description:
  - Returns networking information for all configured interfaces on the vCenter Server appliance.
  - Includes DNS configuration and per-interface network settings.
author:
  - Ansible Eco Content Team (@eco-ansible-content)
extends_documentation_fragment:
  - vmware.vmware_rest.connection_params
options: {}
version_added: 4.11.0
requirements: []
notes:
  - Generated from vSphere API spec 9.1.0.
  - Has support for vSphere API 7.0.3.
  - Has support for vSphere API 8.0.2.
"""

EXAMPLES = r"""
- name: Get vCenter appliance networking information
  vmware.vmware_rest.appliance_networking_info:
  register: appliance_networking
"""

RETURN = r"""
value:
  description:
    - Networking configuration for the vCenter Server appliance.
  returned: On success
  type: dict
  contains:
    dns:
      description:
        - DNS configuration.
      type: dict
      contains:
        mode:
          description:
            - DNS mode.
            - C(DHCP) indicates DNS server addresses are obtained from a DHCP server.
            - C(STATIC) indicates DNS server addresses are specified explicitly.
          type: str
          choices:
            - DHCP
            - STATIC
          sample: STATIC
        hostname:
          description:
            - Hostname.
          type: str
          sample: vcenter.example.com
        servers:
          description:
            - DNS servers.
          type: list
          elements: str
          sample:
            - 192.168.1.1
    interfaces:
      description:
        - Interface configuration as a key-value map where the key is a network interface name, for example C(nic0).
        - Each key must be an identifier (MOID) for a C(com.vmware.appliance.networking.interfaces) resource.
      type: dict
      sample:
        nic0:
          mac: "00:0C:29:94:BB:5A"
          name: nic0
          status: up
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.vmware.vmware_rest.plugins.module_utils._argument_spec import (
    connection_params_argument_spec,
)
from ansible_collections.vmware.vmware_rest.plugins.module_utils._module_base import (
    VmwareRestInfoModuleBase,
)

NETWORKING_PATH = "/appliance/networking"


class VmwareRestInfoModule(VmwareRestInfoModuleBase):
    PAYLOAD_FORMAT = {
        "get": {"query": {}, "body": {}, "path": {}},
    }

    def get_info(self):
        response = self.client.get(NETWORKING_PATH)
        if response.status == 404:
            return None
        return response.json


def main():
    module_args = connection_params_argument_spec()

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
    )

    info_module = VmwareRestInfoModule(module)
    result = info_module.get_info()
    module.exit_json(value=result)


if __name__ == "__main__":
    main()
