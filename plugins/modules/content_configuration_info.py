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
module: content_configuration_info
short_description: Gather information about the global configuration of the vCenter Content Library Service.
description:
  - Retrieve the service-wide settings that control how the vCenter Content Library Service behaves.
  - These settings include the automatic synchronization schedule for subscribed libraries, the
    number of concurrent item and file transfers, and the bandwidth used when transferring content.
  - The configuration is a single, global object, so this module always returns one result and takes
    no selection parameters.
  - Use M(vmware.vmware_rest.content_configuration) to change these settings.

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
- name: Gather the Content Library Service configuration
  vmware.vmware_rest.content_configuration_info:
  register: content_config

- name: Show whether automatic synchronization is enabled
  ansible.builtin.debug:
    var: content_config.value.automatic_sync_enabled
"""

RETURN = r"""
value:
  description: The current global configuration of the Content Library Service.
  returned: On success
  sample:
    automatic_sync_enabled: true
    automatic_sync_start_hour: 20
    automatic_sync_stop_hour: 7
    automatic_sync_refresh_interval: 240
    automatic_sync_setting_refresh_interval: 600
    maximum_concurrent_item_syncs: 5
    transfer_throttling_bandwidth_total: 0
    transfer_nfc_max_concurrent_transfers_per_host: 8
    priority_transfer_threads_pool_size: 5
    transfer_threads_pool_size: 20
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

MOID_PARAMETER_HINTS = []

LIST_ENDPOINT = ""
ITEM_ENDPOINT = "/content/configuration"


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
