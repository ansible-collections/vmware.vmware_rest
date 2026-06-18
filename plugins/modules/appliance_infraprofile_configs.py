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
module: appliance_infraprofile_configs
short_description: Exports the desired profile specification.
description:
  - Exports infrastructure profile configuration specifications from the vCenter appliance.
  - Use I(state=export) to export one or more registered profiles.
author:
  - Ansible Eco Content Team (@eco-ansible-content)
extends_documentation_fragment:
  - vmware.vmware_rest.connection_params
options:
  state:
    description:
      - The operation to perform on infrastructure profile configurations.
      - Use C(export) to export the desired profile specification.
    type: str
    choices:
      - export
    required: true
  description:
    description:
      - Custom description provided by the user.
      - If unset, the description will be empty.
    type: str
  encryption_key:
    description:
      - Encryption key to encrypt or decrypt profiles.
      - If unset, encryption will not be used for the profile.
    type: str
  profiles:
    description:
      - Profiles to export.
      - If unset or empty, all profiles are returned.
      - Each element must be an identifier (MOID) for a C(com.vmware.infraprofile.profile) resource.
    type: list
    elements: str
version_added: 4.11.0
requirements: []
notes:
  - Generated from vSphere API spec 9.1.0.
  - Has support for vSphere API 7.0.3.
  - Has support for vSphere API 8.0.2.
  - This API endpoint is deprecated in vSphere 9.0.0.0 and the module will not be compatible with future versions of vSphere.
"""

EXAMPLES = r"""
- name: Export the ApplianceManagement profile
  vmware.vmware_rest.appliance_infraprofile_configs:
    state: export
    profiles:
      - ApplianceManagement
  register: exported_profile
"""

RETURN = r"""
value:
  description:
    - Exported profile configuration specification.
    - The API returns a JSON string; the module parses it when possible.
  returned: On success when I(state=export)
  type: raw
  sample:
    action: RESTART_SERVICE
    productName: VMware vCenter Server
    profiles:
      ApplianceManagement:
        name: ApplianceManagement
"""

import json

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.vmware.vmware_rest.plugins.module_utils._argument_spec import (
    connection_params_argument_spec,
)
from ansible_collections.vmware.vmware_rest.plugins.module_utils._module_base import (
    VmwareRestModuleBase,
)

PATH = "/appliance/infraprofile/configs"

_EXPORT_BODY = {
    "description": "description",
    "encryption_key": "encryption_key",
    "profiles": "profiles",
}


class VmwareRestModule(VmwareRestModuleBase):
    PAYLOAD_FORMAT = {
        "export": {
            "query": {},
            "body": _EXPORT_BODY,
            "path": {},
        },
    }

    def export_profiles(self):
        body = self.build_payload(self.PAYLOAD_FORMAT["export"])
        response = self.client.post(
            PATH,
            data=body,
            query={"action": "export"},
        )
        return {"changed": True, "value": _normalize_export_value(response.json)}


def _normalize_export_value(data):
    if isinstance(data, str):
        stripped = data.strip()
        if stripped.startswith(("{", "[")):
            try:
                return json.loads(data)
            except ValueError:
                pass
    return data


def main():
    module_args = connection_params_argument_spec()
    module_args["state"] = {
        "type": "str",
        "choices": ["export"],
        "required": True,
    }
    module_args["description"] = {"type": "str"}
    module_args["encryption_key"] = {"type": "str", "no_log": True}
    module_args["profiles"] = {"type": "list", "elements": "str"}

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False,
    )

    rest_module = VmwareRestModule(module)

    if module.params["state"] == "export":
        result = rest_module.export_profiles()
    else:
        module.fail_json(msg="Unsupported state: {0}".format(module.params["state"]))

    module.exit_json(**result)


if __name__ == "__main__":
    main()
