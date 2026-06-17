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
module: appliance_infraprofile_configs_info
short_description: List all the profiles which are registered.
description:
  - Lists all infrastructure profiles registered on the vCenter Server appliance.
  - Each profile includes a name and description.
  - Requires the C(Infraprofile.Read) privilege.
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
  - This API endpoint is deprecated in vSphere 9.0.0.0 and the module will not be compatible with future versions of vSphere.
"""

EXAMPLES = r"""
- name: List registered infrastructure profiles
  vmware.vmware_rest.appliance_infraprofile_configs_info:
  register: infraprofile_configs
"""

RETURN = r"""
value:
  description:
    - List of registered infrastructure profiles.
  returned: On success
  type: list
  elements: dict
  sample:
    - name: default
      info: Default profile
  contains:
    name:
      description:
        - Name of the profile, which is also a profile identifier (MOID) for a C(com.vmware.infraprofile.profile) resource.
      type: str
      sample: default
    info:
      description:
        - Description of the profile.
      type: str
      sample: Default profile
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.vmware.vmware_rest.plugins.module_utils._argument_spec import (
    connection_params_argument_spec,
)
from ansible_collections.vmware.vmware_rest.plugins.module_utils._module_base import (
    VmwareRestInfoModuleBase,
)

INFRAPROFILE_CONFIGS_PATH = "/appliance/infraprofile/configs"


class VmwareRestInfoModule(VmwareRestInfoModuleBase):
    PAYLOAD_FORMAT = {
        "get": {"query": {}, "body": {}, "path": {}},
    }

    def get_info(self):
        return self.fetch_list(
            INFRAPROFILE_CONFIGS_PATH,
            self.PAYLOAD_FORMAT["get"],
        )


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
