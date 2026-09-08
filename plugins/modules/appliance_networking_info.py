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
module: appliance_networking_info
short_description: Gather information about the network configuration of the vCenter Server Appliance.
description:
  - Retrieve the network configuration of the vCenter Server Appliance for all configured interfaces.
  - The returned information includes the DNS configuration (mode, hostname, and servers) and, for each
    network interface, its status, MAC address, and IPv4 and IPv6 address settings.
  - This module is read only and does not change any configuration. Use
    M(vmware.vmware_rest.appliance_networking) to modify the appliance network settings.

author:
  - Ansible Eco Content Team (@eco-ansible-content)

extends_documentation_fragment:
  - vmware.vmware_rest.connection_params

options: {}

version_added: 5.0.0

requirements: []

notes:
  - Generated from vSphere API spec 9.1.0.
"""

EXAMPLES = r"""
- name: Gather the appliance network configuration
  vmware.vmware_rest.appliance_networking_info:
  register: networking

- name: Display the appliance hostname
  ansible.builtin.debug:
    var: networking.value.dns.hostname
"""

RETURN = r"""
value:
  description: The network configuration of the appliance, including DNS settings and all interfaces.
  returned: On success
  type: dict
  sample:
    dns:
      mode: STATIC
      hostname: vcenter.example.com
      servers:
        - 10.20.80.1
    interfaces:
      nic0:
        name: nic0
        status: up
        mac: "00:0C:29:94:BB:5A"
        ipv4:
          configurable: true
          mode: STATIC
          address: 10.20.80.191
          prefix: 24
          default_gateway: 10.20.80.1
        ipv6:
          configurable: true
          dhcp: false
          autoconf: false
          default_gateway: "::"
          addresses:
            - address: fc00:10:20:83:20c:29ff:fe94:bb5a
              prefix: 64
              origin: STATIC
              status: PREFERRED
info:
  description: A list containing the appliance network configuration.
  returned: On success
  type: list
  elements: dict
  sample:
    - dns:
        mode: STATIC
        hostname: vcenter.example.com
        servers:
          - 10.20.80.1
      interfaces:
        nic0:
          name: nic0
          status: up
          mac: "00:0C:29:94:BB:5A"
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

MOID_PARAMETER_HINTS = []

LIST_ENDPOINT = ""
ITEM_ENDPOINT = "/appliance/networking"


GET_OPERATION = OperationConfig(
    name="get",
    uri=ITEM_ENDPOINT,
    http_method="GET",
)


def create_module_argument_spec() -> dict:
    module_args = connection_params_argument_spec()
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
    )
    try:
        result = info_module.get_resource_info()
    except VmwareModuleError as e:
        module.fail_json(**e.to_module_fail_json_output())
    module.exit_json(**result)


if __name__ == "__main__":
    main()
