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
module: appliance_update_info
short_description: Get the current status of the vCenter appliance update.
description:
  - Returns the current status of the vCenter Server appliance update.
  - Includes update state, version, optional running task details, and the timestamp of the latest update repository query.
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
- name: Get the current appliance update status
  vmware.vmware_rest.appliance_update_info:
  register: update_status
"""

RETURN = r"""
value:
  description:
    - Appliance update status information.
  returned: On success
  type: dict
  contains:
    state:
      description:
        - State of the appliance update.
      type: str
      sample: UP_TO_DATE
      choices:
        - UP_TO_DATE
        - UPDATES_PENDING
        - STAGE_IN_PROGRESS
        - INSTALL_IN_PROGRESS
        - INSTALL_FAILED
        - ROLLBACK_IN_PROGRESS
    version:
      description:
        - Version of the base appliance when I(state) is C(UP_TO_DATE).
        - Version of the update being staged or installed when I(state) is C(STAGE_IN_PROGRESS) or C(INSTALL_IN_PROGRESS).
        - Version of the staged update when I(state) is C(UPDATES_PENDING).
        - Version of the failed update when I(state) is C(INSTALL_FAILED) or C(ROLLBACK_IN_PROGRESS).
      type: str
      sample: 9.1.0.10000
    task:
      description:
        - The running or completed update task.
      type: dict
    latest_query_time:
      description:
        - Timestamp of the latest query to the update repository.
        - Omitted when the update repository was never queried.
      type: str
      sample: "2026-06-15T12:00:00Z"
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.vmware.vmware_rest.plugins.module_utils._argument_spec import (
    connection_params_argument_spec,
)
from ansible_collections.vmware.vmware_rest.plugins.module_utils._module_base import (
    VmwareRestInfoModuleBase,
)

UPDATE_PATH = "/appliance/update"


class VmwareRestInfoModule(VmwareRestInfoModuleBase):
    PAYLOAD_FORMAT = {
        "get": {"query": {}, "body": {}, "path": {}},
    }

    def get_info(self):
        response = self.client.get(UPDATE_PATH)
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
