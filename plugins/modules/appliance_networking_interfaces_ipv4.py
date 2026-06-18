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
short_description: Set IPv4 network configuration for a vCenter appliance interface
description:
  - Sets the IPv4 network configuration for a specific network interface on the
    vCenter Server appliance.
  - Only parameters explicitly specified by the user are compared and sent to the API.
  - When I(mode) is not specified, the current mode from the appliance is used for
    the update request because the API requires I(mode) in the request body.
  - Use I(state=present) to update IPv4 settings when they differ from the current
    configuration.
author:
  - Ansible Eco Content Team (@eco-ansible-content)
extends_documentation_fragment:
  - vmware.vmware_rest.connection_params
options:
  state:
    description:
      - The desired state of the IPv4 configuration.
      - Use C(present) to update IPv4 settings for the network interface.
      - C(absent) is not supported because the API does not provide a delete operation.
    type: str
    choices:
      - present
      - absent
    default: present
  interface_name:
    description:
      - Network interface to update, for example C(nic0).
      - Must be an identifier (MOID) for a C(com.vmware.appliance.networking.interfaces)
        resource.
    type: str
    required: true
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
      - IPv4 address, for example C(10.20.80.191).
      - Relevant when I(mode) is C(STATIC).
    type: str
  prefix:
    description:
      - IPv4 CIDR prefix, for example C(24).
      - Relevant when I(mode) is C(STATIC).
    type: int
  default_gateway:
    description:
      - IPv4 address of the default gateway for the appliance.
      - Relevant when I(mode) is C(STATIC) or C(DHCP).
    type: str
version_added: 4.11.0
requirements: []
notes:
  - Generated from vSphere API spec 9.1.0.
  - Has support for vSphere API 7.0.3.
  - Has support for vSphere API 8.0.2.
"""

EXAMPLES = r"""
- name: Set static IPv4 configuration for nic0
  vmware.vmware_rest.appliance_networking_interfaces_ipv4:
    interface_name: nic0
    mode: STATIC
    address: 10.20.80.191
    prefix: 24
    default_gateway: 10.20.80.1

- name: Configure nic0 to use DHCP
  vmware.vmware_rest.appliance_networking_interfaces_ipv4:
    interface_name: nic0
    mode: DHCP
"""

RETURN = r"""
value:
  description:
    - IPv4 configuration after update, or current configuration when no change was made.
  returned: On success when I(state=present)
  type: dict
  sample:
    configurable: true
    mode: STATIC
    address: 10.20.80.191
    prefix: 24
    default_gateway: 10.20.80.1
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.vmware.vmware_rest.plugins.module_utils._argument_spec import (
    connection_params_argument_spec,
)
from ansible_collections.vmware.vmware_rest.plugins.module_utils._errors import (
    UnexpectedAPIResponse,
)
from ansible_collections.vmware.vmware_rest.plugins.module_utils._module_base import (
    VmwareRestCrudModuleBase,
    params_differ,
)

IPV4_PATH = "/appliance/networking/interfaces/{interface_name}/ipv4"

_UPDATE_BODY = {
    "mode": "mode",
    "address": "address",
    "prefix": "prefix",
    "default_gateway": "default_gateway",
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

    def _build_put_body(self, current):
        update_body = self.build_updatable_payload()
        if not update_body:
            return None

        put_body = dict(update_body)
        if "mode" not in put_body:
            put_body["mode"] = current["mode"]
        return put_body

    def ensure_present(self):
        path = self.build_path(IPV4_PATH)
        response = self.client.get(path)
        if response.status == 404:
            self.module.fail_json(
                msg="Network interface not found: {0}".format(
                    self.params["interface_name"]
                )
            )

        current = response.json
        put_body = self._build_put_body(current)
        if put_body is None:
            return {"changed": False, "value": current}

        if not params_differ(current, put_body):
            return {"changed": False, "value": current}

        if not self.module.check_mode:
            put_response = self.client.request("PUT", path, data=put_body)
            if put_response.status not in (200, 204):
                self.client.error_handler.handle_request_error(
                    exception=UnexpectedAPIResponse(
                        put_response.status, put_response.data
                    ),
                    method="PUT",
                    path=path,
                    request_kwargs={"data": put_body},
                )

            updated = self.client.get(path)
            return {"changed": True, "value": updated.json}

        return {"changed": True, "value": current}

    def ensure_absent(self):
        return {"changed": False}


def main():
    module_args = connection_params_argument_spec()
    module_args["state"] = {
        "type": "str",
        "choices": ["present", "absent"],
        "default": "present",
    }
    module_args["interface_name"] = {"type": "str", "required": True}
    module_args["mode"] = {
        "type": "str",
        "choices": ["DHCP", "STATIC", "UNCONFIGURED"],
    }
    module_args["address"] = {"type": "str"}
    module_args["prefix"] = {"type": "int"}
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
