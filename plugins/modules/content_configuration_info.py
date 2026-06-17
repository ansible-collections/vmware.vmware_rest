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
module: content_configuration_info
short_description: Get Content Library Service configuration.
description:
  - Retrieves the current global configuration values of the Content Library Service.
  - Includes automatic synchronization settings, transfer throttling limits, and
    related metadata for each configuration property.
  - Requires the C(ContentLibrary.GetConfiguration) privilege.
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
- name: Get Content Library Service configuration
  vmware.vmware_rest.content_configuration_info:
  register: content_configuration
"""

RETURN = r"""
value:
  description:
    - Content Library Service global configuration.
  returned: On success
  type: dict
  sample:
    automatic_sync_enabled: true
    automatic_sync_start_hour: 20
    automatic_sync_stop_hour: 7
    maximum_concurrent_item_syncs: 5
  contains:
    automatic_sync_enabled:
      description:
        - Whether automatic synchronization is enabled for subscribed libraries.
      type: bool
      sample: true
    automatic_sync_enabled_setting:
      description:
        - Setting metadata for I(automatic_sync_enabled).
      type: dict
    automatic_sync_start_hour:
      description:
        - Hour at which automatic synchronization starts, between 0 and 23 inclusive.
      type: int
      sample: 20
    automatic_sync_start_hour_setting:
      description:
        - Setting metadata for I(automatic_sync_start_hour).
      type: dict
    automatic_sync_stop_hour:
      description:
        - Hour at which automatic synchronization stops, between 0 and 23 inclusive.
      type: int
      sample: 7
    automatic_sync_stop_hour_setting:
      description:
        - Setting metadata for I(automatic_sync_stop_hour).
      type: dict
    maximum_concurrent_item_syncs:
      description:
        - Maximum number of library items allowed to synchronize concurrently from remote libraries.
      type: int
      sample: 5
    maximum_concurrent_item_syncs_setting:
      description:
        - Setting metadata for I(maximum_concurrent_item_syncs).
      type: dict
    automatic_sync_refresh_interval:
      description:
        - Interval in minutes between automatic synchronizations within the sync window.
      type: int
      sample: 240
    automatic_sync_refresh_interval_setting:
      description:
        - Setting metadata for I(automatic_sync_refresh_interval).
      type: dict
    automatic_sync_setting_refresh_interval:
      description:
        - Interval in seconds before changed automatic sync settings are applied.
      type: int
      sample: 600
    automatic_sync_setting_refresh_interval_setting:
      description:
        - Setting metadata for I(automatic_sync_setting_refresh_interval).
      type: dict
    transfer_throttling_bandwidth_total:
      description:
        - Maximum bandwidth usage threshold in Mbps across all transfers.
      type: int
      sample: 0
    transfer_throttling_bandwidth_total_setting:
      description:
        - Setting metadata for I(transfer_throttling_bandwidth_total).
      type: dict
    transfer_nfc_max_concurrent_transfers_per_host:
      description:
        - Maximum concurrent NFC transfers allowed per ESXi host.
      type: int
      sample: 8
    transfer_nfc_max_concurrent_transfers_per_host_setting:
      description:
        - Setting metadata for I(transfer_nfc_max_concurrent_transfers_per_host).
      type: dict
    priority_transfer_threads_pool_size:
      description:
        - Maximum number of concurrent priority file transfers.
      type: int
      sample: 5
    priority_transfer_threads_pool_size_setting:
      description:
        - Setting metadata for I(priority_transfer_threads_pool_size).
      type: dict
    transfer_threads_pool_size:
      description:
        - Maximum number of concurrent non-priority file transfers.
      type: int
      sample: 20
    transfer_threads_pool_size_setting:
      description:
        - Setting metadata for I(transfer_threads_pool_size).
      type: dict
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.vmware.vmware_rest.plugins.module_utils._argument_spec import (
    connection_params_argument_spec,
)
from ansible_collections.vmware.vmware_rest.plugins.module_utils._module_base import (
    VmwareRestInfoModuleBase,
)

CONFIGURATION_PATH = "/content/configuration"


class VmwareRestInfoModule(VmwareRestInfoModuleBase):
    PAYLOAD_FORMAT = {
        "get": {"query": {}, "body": {}, "path": {}},
    }

    def get_info(self):
        response = self.client.get(CONFIGURATION_PATH)
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
