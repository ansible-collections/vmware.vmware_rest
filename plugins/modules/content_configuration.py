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
module: content_configuration
short_description: Manage global Content Library Service configuration.
description:
  - Updates global settings of the Content Library Service on vCenter Server.
  - Only parameters explicitly specified by the user are sent to the API.
  - Use I(state=present) to update the configuration when it differs from the
    current settings.
author:
  - Ansible Eco Content Team (@eco-ansible-content)
extends_documentation_fragment:
  - vmware.vmware_rest.connection_params
options:
  state:
    description:
      - The desired state of the Content Library Service configuration.
      - Use C(present) to update the global configuration.
      - C(absent) is not supported because the API does not provide a delete operation.
    type: str
    choices:
      - present
      - absent
    default: present
  automatic_sync_enabled:
    description:
      - Whether automatic synchronization is enabled for subscribed content libraries.
      - When enabled, subscribed libraries are synchronized on a daily basis.
    type: bool
  automatic_sync_start_hour:
    description:
      - Hour at which automatic synchronization starts.
      - Valid values are between C(0) (midnight) and C(23) inclusive.
    type: int
  automatic_sync_stop_hour:
    description:
      - Hour at which automatic synchronization stops.
      - Active synchronization operations continue, but no new operations are triggered
        after this hour.
      - Valid values are between C(0) (midnight) and C(23) inclusive.
    type: int
  maximum_concurrent_item_syncs:
    description:
      - Maximum number of library items that may be synchronized concurrently from
        remote libraries.
      - Must be a positive number.
    type: int
  automatic_sync_refresh_interval:
    description:
      - Interval in minutes between automatic synchronizations of all subscribed content
        libraries within the automatic synchronization window.
    type: int
  automatic_sync_setting_refresh_interval:
    description:
      - Interval in seconds after automatic synchronization settings change before the
        Content Library Service applies the settings.
      - Changing this value requires a restart of the Content Library Service.
    type: int
  transfer_throttling_bandwidth_total:
    description:
      - Maximum bandwidth usage threshold in Mbps across all transfers handled by the
        Content Library Service.
      - A value of C(0) means unlimited bandwidth.
    type: int
  transfer_nfc_max_concurrent_transfers_per_host:
    description:
      - Maximum concurrent NFC transfers allowed per ESXi host during content library
        transfers.
    type: int
  priority_transfer_threads_pool_size:
    description:
      - Maximum number of concurrent transfers allowed for priority files such as OVF
        descriptors.
      - Changing this value requires a restart of the Content Library Service.
    type: int
  transfer_threads_pool_size:
    description:
      - Maximum number of concurrent transfers allowed for non-priority files.
      - Changing this value requires a restart of the Content Library Service.
    type: int
version_added: 4.11.0
requirements: []
notes:
  - Generated from vSphere API spec 9.1.0.
  - Has support for vSphere API 7.0.3.
  - Has support for vSphere API 8.0.2.
"""

EXAMPLES = r"""
- name: Enable automatic synchronization for subscribed libraries
  vmware.vmware_rest.content_configuration:
    automatic_sync_enabled: true

- name: Configure automatic synchronization window and concurrency
  vmware.vmware_rest.content_configuration:
    automatic_sync_start_hour: 20
    automatic_sync_stop_hour: 7
    maximum_concurrent_item_syncs: 5
"""

RETURN = r"""
value:
  description:
    - Content Library Service configuration after update, or current configuration when
      no change was made.
  returned: On success when I(state=present)
  type: dict
  sample:
    automatic_sync_enabled: true
    automatic_sync_start_hour: 20
    automatic_sync_stop_hour: 7
    maximum_concurrent_item_syncs: 5
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

PATH = "/content/configuration"

_UPDATE_BODY = {
    "automatic_sync_enabled": "automatic_sync_enabled",
    "automatic_sync_start_hour": "automatic_sync_start_hour",
    "automatic_sync_stop_hour": "automatic_sync_stop_hour",
    "maximum_concurrent_item_syncs": "maximum_concurrent_item_syncs",
    "automatic_sync_refresh_interval": "automatic_sync_refresh_interval",
    "automatic_sync_setting_refresh_interval": (
        "automatic_sync_setting_refresh_interval"
    ),
    "transfer_throttling_bandwidth_total": "transfer_throttling_bandwidth_total",
    "transfer_nfc_max_concurrent_transfers_per_host": (
        "transfer_nfc_max_concurrent_transfers_per_host"
    ),
    "priority_transfer_threads_pool_size": "priority_transfer_threads_pool_size",
    "transfer_threads_pool_size": "transfer_threads_pool_size",
}


class VmwareRestCrudModule(VmwareRestCrudModuleBase):
    PAYLOAD_FORMAT = {
        "update": {
            "query": {},
            "body": _UPDATE_BODY,
            "path": {},
        },
    }

    UPDATABLE_PARAMS = tuple(_UPDATE_BODY.values())

    def ensure_present(self):
        response = self.client.get(PATH)
        current = response.json

        update_body = self.build_updatable_payload()
        if not update_body:
            return {"changed": False, "value": current}

        if not params_differ(current, update_body):
            return {"changed": False, "value": current}

        if not self.module.check_mode:
            patch_response = self.client.patch(PATH, data=update_body)
            if patch_response.status not in (200, 204):
                self.client.error_handler.handle_request_error(
                    exception=UnexpectedAPIResponse(
                        patch_response.status, patch_response.data
                    ),
                    method="PATCH",
                    path=PATH,
                    request_kwargs={"data": update_body},
                )

            updated = self.client.get(PATH)
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
    module_args["automatic_sync_enabled"] = {"type": "bool"}
    for param in (
        "automatic_sync_start_hour",
        "automatic_sync_stop_hour",
        "maximum_concurrent_item_syncs",
        "automatic_sync_refresh_interval",
        "automatic_sync_setting_refresh_interval",
        "transfer_throttling_bandwidth_total",
        "transfer_nfc_max_concurrent_transfers_per_host",
        "priority_transfer_threads_pool_size",
        "transfer_threads_pool_size",
    ):
        module_args[param] = {"type": "int"}

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
