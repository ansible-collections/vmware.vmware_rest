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
module: appliance_networking_interfaces_ipv6_info
short_description: Retrieve the IPv6 configuration of a vCenter Server Appliance network interface.
description:
  - Gather the current IPv6 settings of a specific network interface on the vCenter Server Appliance.
  - The returned information includes the DHCP and autoconfiguration status, the statically assigned
    addresses, and the default gateway.
  - Use M(vmware.vmware_rest.appliance_networking_interfaces_ipv6) to change the IPv6 configuration.

author:
  - Ansible Eco Content Team (@eco-ansible-content)

extends_documentation_fragment:
  - vmware.vmware_rest.connection_params

options:
  interface_name:
    description:
      - The name of the network interface to query, for example C(nic0).
      - The value is the identifier of an interface returned by M(vmware.vmware_rest.appliance_networking_interfaces_info).
    type: str
    required: true

version_added: 5.0.0

requirements: []

notes:
  - Generated from vSphere API spec 9.1.0.
"""

EXAMPLES = r"""
- name: Get the IPv6 configuration of nic0
  vmware.vmware_rest.appliance_networking_interfaces_ipv6_info:
    interface_name: nic0
  register: result
"""

RETURN = r"""
id:
  description: The name of the queried network interface.
  returned: On success
  sample: nic0
  type: str
value:
  description: The IPv6 configuration of the network interface.
  returned: On success
  sample:
    autoconf: false
    dhcp: false
    addresses:
      - address: fc00:10:20:83:20c:29ff:fe94:bb5a
        origin: STATIC
        prefix: 64
        status: PREFERRED
    default_gateway: fc00:10:20:83::1
  type: dict
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

LIST_ENDPOINT = ""
ITEM_ENDPOINT = "/appliance/networking/interfaces/{interface_name}/ipv6"


GET_OPERATION = OperationConfig(
    name="get",
    uri=ITEM_ENDPOINT,
    http_method="GET",
)


def create_module_argument_spec() -> dict:
    module_args = connection_params_argument_spec()
    module_args["interface_name"] = {
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
    )
    try:
        result = info_module.get_resource_info()
    except VmwareModuleError as e:
        module.fail_json(**e.to_module_fail_json_output())
    module.exit_json(**result)


if __name__ == "__main__":
    main()
