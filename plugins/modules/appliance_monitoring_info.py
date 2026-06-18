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
module: appliance_monitoring_info
short_description: Get the list of monitored items on the vCenter appliance.
description:
  - Returns the list of items monitored by the vCenter Server appliance monitoring backend.
  - Each item includes an identifier, display name, units, category, instance, and description.
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
- name: Get the list of monitored items
  vmware.vmware_rest.appliance_monitoring_info:
  register: monitored_items
"""

RETURN = r"""
value:
  description:
    - List of monitored items available from the appliance monitoring backend.
  returned: On success
  type: list
  elements: dict
  contains:
    id:
      description:
        - Monitored item identifier (MOID), for example C(CPU) or C(MEMORY).
      returned: On success
      type: str
      sample: mem.total
    name:
      description:
        - Human-readable monitored item name.
      returned: On success
      type: str
      sample: Memory total
    units:
      description:
        - Y-axis label for the monitored item, for example C(Mbps) or C(%).
      returned: On success
      type: str
      sample: MB
    category:
      description:
        - Monitored item category, for example C(network) or C(storage).
      returned: On success
      type: str
      sample: mem
    instance:
      description:
        - Instance name for the monitored item, for example C(eth0).
      returned: On success
      type: str
      sample: total
    description:
      description:
        - Monitored item description key.
      returned: On success
      type: str
      sample: com.vmware.applmgmt.mon.descr.mem.total
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.vmware.vmware_rest.plugins.module_utils._argument_spec import (
    connection_params_argument_spec,
)
from ansible_collections.vmware.vmware_rest.plugins.module_utils._module_base import (
    VmwareRestInfoModuleBase,
    normalize_list_response,
)

MONITORING_LIST_PATH = "/appliance/monitoring"


class VmwareRestInfoModule(VmwareRestInfoModuleBase):
    PAYLOAD_FORMAT = {
        "get": {"query": {}, "body": {}, "path": {}},
    }

    def get_info(self):
        response = self.client.get(MONITORING_LIST_PATH)
        if response.status == 404:
            return []
        return normalize_list_response(response.json)


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
