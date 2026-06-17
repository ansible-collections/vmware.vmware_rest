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
module: appliance_networking_interfaces_ipv6
short_description: Set IPv6 network configuration for a vCenter appliance interface.
description:
  - Sets IPv6 network configuration for a specific network interface on the
    vCenter Server appliance.
  - Only parameters explicitly specified by the user are sent to the API.
  - Unspecified parameters retain their current values from the appliance.
  - Use I(state=present) to update IPv6 configuration when it differs from the
    current settings.
author:
  - Ansible Eco Content Team (@eco-ansible-content)
extends_documentation_fragment:
  - vmware.vmware_rest.connection_params
options:
  state:
    description:
      - The desired state of the IPv6 configuration.
      - Use C(present) to update IPv6 network configuration.
      - C(absent) is not supported because the API does not provide a delete operation.
    type: str
    choices:
      - present
      - absent
    default: present
  interface_name:
    description:
      - Network interface to update, for example C(nic0).
      - Must be an identifier (MOID) for a C(appliance.networking.interfaces) resource.
    type: str
    required: true
  dhcp:
    description:
      - Whether an IPv6 address is assigned by a DHCP server.
    type: bool
  autoconf:
    description:
      - Whether an IPv6 address is assigned by Stateless Address Autoconfiguration
        (SLAAC).
    type: bool
  addresses:
    description:
      - Statically assigned IPv6 addresses.
    type: list
    elements: dict
    suboptions:
      address:
        description:
          - The IPv6 address, for example C(fc00:10:20:83:20c:29ff:fe94:bb5a).
        type: str
        required: true
      prefix:
        description:
          - The IPv6 CIDR prefix, for example C(64).
        type: int
        required: true
  default_gateway:
    description:
      - The default gateway for static IPv6 address assignment.
    type: str
version_added: 4.11.0
requirements: []
notes:
  - Generated from vSphere API spec 9.1.0.
  - Has support for vSphere API 7.0.3.
  - Has support for vSphere API 8.0.2.
"""

EXAMPLES = r"""
- name: Enable IPv6 SLAAC on nic0
  vmware.vmware_rest.appliance_networking_interfaces_ipv6:
    interface_name: nic0
    autoconf: true
    dhcp: false
    addresses: []
    default_gateway: ""

- name: Set a static IPv6 address on nic0
  vmware.vmware_rest.appliance_networking_interfaces_ipv6:
    interface_name: nic0
    dhcp: false
    autoconf: false
    addresses:
      - address: fc00:10:20:83:20c:29ff:fe94:bb5a
        prefix: 64
    default_gateway: fc00:10:20:83::1
"""

RETURN = r"""
value:
  description:
    - IPv6 configuration for the network interface after an update, or the current
      configuration when no change was made.
  returned: On success when I(state=present)
  type: dict
  sample:
    dhcp: false
    autoconf: false
    addresses:
      - address: fc00:10:20:83:20c:29ff:fe94:bb5a
        prefix: 64
        origin: MANUAL
        status: PREFERRED
    default_gateway: fc00:10:20:83::1
    configurable: true
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.vmware.vmware_rest.plugins.module_utils._argument_spec import (
    connection_params_argument_spec,
)
from ansible_collections.vmware.vmware_rest.plugins.module_utils._module_base import (
    VmwareRestCrudModuleBase,
    params_differ,
)

PATH = "/appliance/networking/interfaces/{interface_name}/ipv6"

_UPDATE_BODY = {
    "dhcp": "dhcp",
    "autoconf": "autoconf",
    "addresses": "addresses",
    "default_gateway": "default_gateway",
}

ADDRESS_OPTIONS = {
    "address": {"type": "str", "required": True},
    "prefix": {"type": "int", "required": True},
}


class VmwareRestCrudModule(VmwareRestCrudModuleBase):
    PAYLOAD_FORMAT = {
        "update": {
            "query": {},
            "body": _UPDATE_BODY,
            "path": {"interface_name": "interface_name"},
        },
    }

    UPDATABLE_PARAMS = tuple(_UPDATE_BODY.values())

    def ensure_present(self):
        update_params = self.build_updatable_payload()
        if not update_params:
            self.module.fail_json(
                msg=(
                    "At least one of dhcp, autoconf, addresses, or default_gateway "
                    "must be specified when state is present"
                )
            )

        path = self.build_path(PATH)
        response = self.client.get(path)
        if response.status == 404:
            self.module.fail_json(
                msg="Network interface not found: {0}".format(
                    self.params["interface_name"]
                )
            )

        current = response.json
        desired = self._build_desired_config(current)

        if not params_differ(self._config_body(current), desired):
            return {"changed": False, "value": current}

        if not self.module.check_mode:
            self.client.put(path, data=desired)
            updated = self.client.get(path)
            return {"changed": True, "value": updated.json}

        return {"changed": True, "value": current}

    def ensure_absent(self):
        return {"changed": False}

    def _config_body(self, current):
        return {
            "dhcp": current["dhcp"],
            "autoconf": current["autoconf"],
            "addresses": self._put_addresses(current.get("addresses", [])),
            "default_gateway": current["default_gateway"],
        }

    def _build_desired_config(self, current):
        desired = self._config_body(current)
        for param in self.UPDATABLE_PARAMS:
            if self.params.get(param) is not None:
                desired[param] = self.params[param]
        return desired

    @staticmethod
    def _put_addresses(addresses):
        return [
            {"address": entry["address"], "prefix": entry["prefix"]}
            for entry in addresses
        ]


def main():
    module_args = connection_params_argument_spec()
    module_args["state"] = {
        "type": "str",
        "choices": ["present", "absent"],
        "default": "present",
    }
    module_args["interface_name"] = {"type": "str", "required": True}
    module_args["dhcp"] = {"type": "bool"}
    module_args["autoconf"] = {"type": "bool"}
    module_args["addresses"] = {
        "type": "list",
        "elements": "dict",
        "options": ADDRESS_OPTIONS,
    }
    module_args["default_gateway"] = {"type": "str"}

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
    )

    crud_module = VmwareRestCrudModule(module)

    if module.params["state"] == "present":
        result = crud_module.ensure_present()
    elif module.params["state"] == "absent":
        result = crud_module.ensure_absent()
    else:
        module.fail_json(msg="Unsupported state: {0}".format(module.params["state"]))

    module.exit_json(**result)


if __name__ == "__main__":
    main()
