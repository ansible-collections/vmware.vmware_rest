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
module: appliance_networking
short_description: Manage the network configuration of the vCenter Server Appliance.
description:
  - Manage the network configuration of the vCenter Server Appliance across all of its interfaces.
  - Use O(state=reset) to reset and restart the network configuration on all interfaces. This also
    renews the DHCP lease for any interface using a DHCP-assigned address.
  - IPv6 can be enabled or disabled on all interfaces with O(ipv6_enabled).
  - Use M(vmware.vmware_rest.appliance_networking_info) to view the current network configuration.

author:
  - Ansible Eco Content Team (@eco-ansible-content)

extends_documentation_fragment:
  - vmware.vmware_rest.connection_params

options:
  state:
    description:
      - The desired state of the appliance network configuration.
      - Use C(present) to apply the IPv6 enablement given in I(ipv6_enabled).
      - Use C(reset) to reset and restart the network configuration on all interfaces.
    type: str
    default: present
    choices:
      - present
      - reset
  ipv6_enabled:
    description:
      - Whether IPv6 is enabled on all interfaces.
      - If not specified, the current state of IPv6 is left unchanged.
      - Due to the limitations of the vSphere API, this parameter does not support idempotency.
        If this parameter is specified, a change will always be reported.
      - This property was added in vSphere API 6.7.
    type: bool
    required: false

version_added: 5.0.0

requirements: []

notes:
  - Generated from vSphere API spec 9.1.0.
"""

EXAMPLES = r"""
- name: Enable IPv6 on all appliance interfaces
  vmware.vmware_rest.appliance_networking:
    ipv6_enabled: true
    state: present

- name: Disable IPv6 on all appliance interfaces
  vmware.vmware_rest.appliance_networking:
    ipv6_enabled: false
    state: present

- name: Reset and restart the appliance network configuration
  vmware.vmware_rest.appliance_networking:
    state: reset
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

MOID_PARAMETER_HINTS = []

LIST_ENDPOINT = ""
ITEM_ENDPOINT = "/appliance/networking"


GET_OPERATION = OperationConfig(
    name="get",
    uri=ITEM_ENDPOINT,
    http_method="GET",
)

UPDATE_OPERATION = OperationConfig(
    name="update",
    uri=ITEM_ENDPOINT,
    http_method="PATCH",
    body_spec={
        "ipv6_enabled": {
            "required": False,
        },
    },
)


ACTION_OPERATIONS = {
    "reset": OperationConfig(
        name="reset",
        uri="/appliance/networking?action=reset",
        http_method="POST",
    ),
}


def create_module_argument_spec() -> dict:
    module_args = connection_params_argument_spec()
    module_args["ipv6_enabled"] = {
        "type": "bool",
    }
    module_args["state"] = {
        "type": "str",
        "choices": ["present", "reset"],
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
        action_operations=ACTION_OPERATIONS,
    )

    try:
        if module.params["state"] == "present":
            result = crud_module.ensure_present()
        elif module.params["state"] in ACTION_OPERATIONS:
            result = crud_module.perform_action()
        else:
            module.fail_json(
                msg="Unsupported state: {0}".format(module.params["state"])
            )
    except VmwareModuleError as e:
        module.fail_json(**e.to_module_fail_json_output())

    module.exit_json(**result)


if __name__ == "__main__":
    main()
