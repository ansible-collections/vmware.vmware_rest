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
short_description: Manage the global configuration of the vCenter Content Library Service.
description:
  - Update the service-wide settings that control how the vCenter Content Library Service behaves.
  - These settings govern the automatic synchronization of subscribed libraries, the number of
    concurrent item and file transfers, and the bandwidth used when transferring content.
  - The configuration is a single, global object; there is only one instance per vCenter, so no
    identifier is required to select it.
  - Only the values you supply are changed. Some settings require a restart of the Content Library
    Service before they take effect, as noted on the individual options.

author:
  - Ansible Eco Content Team (@eco-ansible-content)

extends_documentation_fragment:
  - vmware.vmware_rest.connection_params

options:
  state:
    description:
      - The desired state of the resource.
      - Use C(present) to create or update the resource.
    type: str
    default: present
    choices:
      - present
  automatic_sync_enabled:
    description:
      - Whether the Content Library Service automatically synchronizes subscribed libraries.
      - When enabled, all subscribed libraries are synchronized daily, and libraries that have their
        own automatic synchronization turned on are synchronized every hour between
        O(automatic_sync_start_hour) and O(automatic_sync_stop_hour).
      - The default value is V(true).
    type: bool
    required: false
  automatic_sync_enabled_setting:
    description:
      - Read-only metadata that describes the O(automatic_sync_enabled) setting, such as whether a
        service restart is required and any constraints on its value.
      - This is returned by the get operation. It is accepted, but not required, on update.
      - This property was added in vSphere API 9.1.0.0.
    type: dict
    required: false
    suboptions:
      name:
        description:
          - The name of the configuration.
          - This property was added in vSphere API 9.1.0.0.
        type: str
        required: true
      reboot_required:
        description:
          - Flag indicates if reboot of the Content Library Service is required to apply the change after the configuration's value is updated.
          - This property was added in vSphere API 9.1.0.0.
        type: bool
        required: true
      constraints:
        description:
          - The constraints that can apply to the value of the configuration. Each entry has ConstraintType and value.
          - This property was added in vSphere API 9.1.0.0.
        type: list
        required: true
        elements: dict
  automatic_sync_start_hour:
    description:
      - The hour at which the automatic synchronization will start. This value is between 0 (midnight) and 23 inclusive.
      - The default value is 20.
    type: int
    required: false
  automatic_sync_start_hour_setting:
    description:
      - Read-only metadata that describes the O(automatic_sync_start_hour) setting, such as whether a
        service restart is required and any constraints on its value.
      - This is returned by the get operation. It is accepted, but not required, on update.
      - This property was added in vSphere API 9.1.0.0.
    type: dict
    required: false
    suboptions:
      name:
        description:
          - The name of the configuration.
          - This property was added in vSphere API 9.1.0.0.
        type: str
        required: true
      reboot_required:
        description:
          - Flag indicates if reboot of the Content Library Service is required to apply the change after the configuration's value is updated.
          - This property was added in vSphere API 9.1.0.0.
        type: bool
        required: true
      constraints:
        description:
          - The constraints that can apply to the value of the configuration. Each entry has ConstraintType and value.
          - This property was added in vSphere API 9.1.0.0.
        type: list
        required: true
        elements: dict
  automatic_sync_stop_hour:
    description:
      - The hour at which the automatic synchronization will stop. Any active synchronization
        operation will continue to run, however no new synchronization operations will be triggered
        after the stop hour. This value is between 0 (midnight) and 23 inclusive.
      - The default value is 7.
    type: int
    required: false
  automatic_sync_stop_hour_setting:
    description:
      - Read-only metadata that describes the O(automatic_sync_stop_hour) setting, such as whether a
        service restart is required and any constraints on its value.
      - This is returned by the get operation. It is accepted, but not required, on update.
      - This property was added in vSphere API 9.1.0.0.
    type: dict
    required: false
    suboptions:
      name:
        description:
          - The name of the configuration.
          - This property was added in vSphere API 9.1.0.0.
        type: str
        required: true
      reboot_required:
        description:
          - Flag indicates if reboot of the Content Library Service is required to apply the change after the configuration's value is updated.
          - This property was added in vSphere API 9.1.0.0.
        type: bool
        required: true
      constraints:
        description:
          - The constraints that can apply to the value of the configuration. Each entry has ConstraintType and value.
          - This property was added in vSphere API 9.1.0.0.
        type: list
        required: true
        elements: dict
  maximum_concurrent_item_syncs:
    description:
      - The maximum allowed number of library items to synchronize concurrently from remote
        libraries. This must be a positive number. The service may not be able to guarantee the
        requested concurrency if there is no available capacity.
      - This setting is global across all subscribed libraries. The default value is 5.
    type: int
    required: false
  maximum_concurrent_item_syncs_setting:
    description:
      - Read-only metadata that describes the O(maximum_concurrent_item_syncs) setting, such as whether a
        service restart is required and any constraints on its value.
      - This is returned by the get operation. It is accepted, but not required, on update.
      - This property was added in vSphere API 9.1.0.0.
    type: dict
    required: false
    suboptions:
      name:
        description:
          - The name of the configuration.
          - This property was added in vSphere API 9.1.0.0.
        type: str
        required: true
      reboot_required:
        description:
          - Flag indicates if reboot of the Content Library Service is required to apply the change after the configuration's value is updated.
          - This property was added in vSphere API 9.1.0.0.
        type: bool
        required: true
      constraints:
        description:
          - The constraints that can apply to the value of the configuration. Each entry has ConstraintType and value.
          - This property was added in vSphere API 9.1.0.0.
        type: list
        required: true
        elements: dict
  automatic_sync_refresh_interval:
    description:
      - The interval in minutes between two consecutive automatic synchronizations of all subscribed
        content libraries within the automatic synchronization window defined by
        O(automatic_sync_start_hour) and O(automatic_sync_stop_hour).
      - The default value is 240 minutes.
      - This property was added in vSphere API 9.1.0.0.
    type: int
    required: false
  automatic_sync_refresh_interval_setting:
    description:
      - Read-only metadata that describes the O(automatic_sync_refresh_interval) setting, such as whether a
        service restart is required and any constraints on its value.
      - This is returned by the get operation. It is accepted, but not required, on update.
      - This property was added in vSphere API 9.1.0.0.
    type: dict
    required: false
    suboptions:
      name:
        description:
          - The name of the configuration.
          - This property was added in vSphere API 9.1.0.0.
        type: str
        required: true
      reboot_required:
        description:
          - Flag indicates if reboot of the Content Library Service is required to apply the change after the configuration's value is updated.
          - This property was added in vSphere API 9.1.0.0.
        type: bool
        required: true
      constraints:
        description:
          - The constraints that can apply to the value of the configuration. Each entry has ConstraintType and value.
          - This property was added in vSphere API 9.1.0.0.
        type: list
        required: true
        elements: dict
  automatic_sync_setting_refresh_interval:
    description:
      - The interval in seconds after some automatic synchronization settings are changed and before
        the Content Library Service applies the settings. The affected settings include
        O(automatic_sync_refresh_interval), O(automatic_sync_start_hour) and
        O(automatic_sync_stop_hour).
      - The default value is 600 seconds. This setting requires restart of the content library service to take effect when changed.
      - This property was added in vSphere API 9.1.0.0.
    type: int
    required: false
  automatic_sync_setting_refresh_interval_setting:
    description:
      - Read-only metadata that describes the O(automatic_sync_setting_refresh_interval) setting, such as whether a
        service restart is required and any constraints on its value.
      - This is returned by the get operation. It is accepted, but not required, on update.
      - This property was added in vSphere API 9.1.0.0.
    type: dict
    required: false
    suboptions:
      name:
        description:
          - The name of the configuration.
          - This property was added in vSphere API 9.1.0.0.
        type: str
        required: true
      reboot_required:
        description:
          - Flag indicates if reboot of the Content Library Service is required to apply the change after the configuration's value is updated.
          - This property was added in vSphere API 9.1.0.0.
        type: bool
        required: true
      constraints:
        description:
          - The constraints that can apply to the value of the configuration. Each entry has ConstraintType and value.
          - This property was added in vSphere API 9.1.0.0.
        type: list
        required: true
        elements: dict
  transfer_throttling_bandwidth_total:
    description:
      - Maximum Bandwidth usage threshold in Mbps across all transfers handled by the Content Library Service.
      - The default value is 0 Mbit/s which means unlimited bandwidth.
      - This property was added in vSphere API 9.1.0.0.
    type: int
    required: false
  transfer_throttling_bandwidth_total_setting:
    description:
      - Read-only metadata that describes the O(transfer_throttling_bandwidth_total) setting, such as whether a
        service restart is required and any constraints on its value.
      - This is returned by the get operation. It is accepted, but not required, on update.
      - This property was added in vSphere API 9.1.0.0.
    type: dict
    required: false
    suboptions:
      name:
        description:
          - The name of the configuration.
          - This property was added in vSphere API 9.1.0.0.
        type: str
        required: true
      reboot_required:
        description:
          - Flag indicates if reboot of the Content Library Service is required to apply the change after the configuration's value is updated.
          - This property was added in vSphere API 9.1.0.0.
        type: bool
        required: true
      constraints:
        description:
          - The constraints that can apply to the value of the configuration. Each entry has ConstraintType and value.
          - This property was added in vSphere API 9.1.0.0.
        type: list
        required: true
        elements: dict
  transfer_nfc_max_concurrent_transfers_per_host:
    description:
      - Maximum concurrent NFC transfers limit per ESXi host. This setting controls how many
        concurrent NFC sessions can be opened to a single ESXi host during transfers. Each file being
        transferred uses a single NFC connection.
      - This limit is shared across content library workflows requiring NFC transfers such as OVF
        template deployments, uploading or downloading an item, sync etc. The default value is 8.
      - This property was added in vSphere API 9.1.0.0.
    type: int
    required: false
  transfer_nfc_max_concurrent_transfers_per_host_setting:
    description:
      - Read-only metadata that describes the O(transfer_nfc_max_concurrent_transfers_per_host) setting, such as whether a
        service restart is required and any constraints on its value.
      - This is returned by the get operation. It is accepted, but not required, on update.
      - This property was added in vSphere API 9.1.0.0.
    type: dict
    required: false
    suboptions:
      name:
        description:
          - The name of the configuration.
          - This property was added in vSphere API 9.1.0.0.
        type: str
        required: true
      reboot_required:
        description:
          - Flag indicates if reboot of the Content Library Service is required to apply the change after the configuration's value is updated.
          - This property was added in vSphere API 9.1.0.0.
        type: bool
        required: true
      constraints:
        description:
          - The constraints that can apply to the value of the configuration. Each entry has ConstraintType and value.
          - This property was added in vSphere API 9.1.0.0.
        type: list
        required: true
        elements: dict
  priority_transfer_threads_pool_size:
    description:
      - Maximum number of concurrent transfers that is allowed to transfer priority files by the
        Content Library Service. Currently priority files include OVF descriptor file.
      - The default value is 5. This setting requires restart of the content library service to take effect when changed.
      - This property was added in vSphere API 9.1.0.0.
    type: int
    required: false
  priority_transfer_threads_pool_size_setting:
    description:
      - Read-only metadata that describes the O(priority_transfer_threads_pool_size) setting, such as whether a
        service restart is required and any constraints on its value.
      - This is returned by the get operation. It is accepted, but not required, on update.
      - This property was added in vSphere API 9.1.0.0.
    type: dict
    required: false
    suboptions:
      name:
        description:
          - The name of the configuration.
          - This property was added in vSphere API 9.1.0.0.
        type: str
        required: true
      reboot_required:
        description:
          - Flag indicates if reboot of the Content Library Service is required to apply the change after the configuration's value is updated.
          - This property was added in vSphere API 9.1.0.0.
        type: bool
        required: true
      constraints:
        description:
          - The constraints that can apply to the value of the configuration. Each entry has ConstraintType and value.
          - This property was added in vSphere API 9.1.0.0.
        type: list
        required: true
        elements: dict
  transfer_threads_pool_size:
    description:
      - Maximum number of concurrent transfers that is allowed to transfer non-priority files by the Content Library Service.
      - The default value is 20. This setting requires restart of the content library service to take effect when changed.
      - This property was added in vSphere API 9.1.0.0.
    type: int
    required: false
  transfer_threads_pool_size_setting:
    description:
      - Read-only metadata that describes the O(transfer_threads_pool_size) setting, such as whether a
        service restart is required and any constraints on its value.
      - This is returned by the get operation. It is accepted, but not required, on update.
      - This property was added in vSphere API 9.1.0.0.
    type: dict
    required: false
    suboptions:
      name:
        description:
          - The name of the configuration.
          - This property was added in vSphere API 9.1.0.0.
        type: str
        required: true
      reboot_required:
        description:
          - Flag indicates if reboot of the Content Library Service is required to apply the change after the configuration's value is updated.
          - This property was added in vSphere API 9.1.0.0.
        type: bool
        required: true
      constraints:
        description:
          - The constraints that can apply to the value of the configuration. Each entry has ConstraintType and value.
          - This property was added in vSphere API 9.1.0.0.
        type: list
        required: true
        elements: dict

version_added: 5.0.0

requirements: []

notes:
  - Generated from vSphere API spec 9.1.0.
"""

EXAMPLES = r"""
- name: Enable automatic synchronization of subscribed libraries
  vmware.vmware_rest.content_configuration:
    automatic_sync_enabled: true

- name: Tune the automatic synchronization window and transfer limits
  vmware.vmware_rest.content_configuration:
    automatic_sync_enabled: true
    automatic_sync_start_hour: 22
    automatic_sync_stop_hour: 6
    maximum_concurrent_item_syncs: 10
    transfer_throttling_bandwidth_total: 500
"""

RETURN = r"""
value:
  description: The raw API response body from the vCenter operation.
  returned: On success
  sample: {}
  type: raw
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
ITEM_ENDPOINT = "/content/configuration"


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
        "automatic_sync_enabled": {
            "required": False,
        },
        "automatic_sync_enabled_setting": {
            "required": False,
            "subspec": {
                "name": {
                    "required": False,
                },
                "reboot_required": {
                    "required": False,
                },
                "constraints": {
                    "required": False,
                },
            },
        },
        "automatic_sync_start_hour": {
            "required": False,
        },
        "automatic_sync_start_hour_setting": {
            "required": False,
            "subspec": {
                "name": {
                    "required": False,
                },
                "reboot_required": {
                    "required": False,
                },
                "constraints": {
                    "required": False,
                },
            },
        },
        "automatic_sync_stop_hour": {
            "required": False,
        },
        "automatic_sync_stop_hour_setting": {
            "required": False,
            "subspec": {
                "name": {
                    "required": False,
                },
                "reboot_required": {
                    "required": False,
                },
                "constraints": {
                    "required": False,
                },
            },
        },
        "maximum_concurrent_item_syncs": {
            "required": False,
        },
        "maximum_concurrent_item_syncs_setting": {
            "required": False,
            "subspec": {
                "name": {
                    "required": False,
                },
                "reboot_required": {
                    "required": False,
                },
                "constraints": {
                    "required": False,
                },
            },
        },
        "automatic_sync_refresh_interval": {
            "required": False,
        },
        "automatic_sync_refresh_interval_setting": {
            "required": False,
            "subspec": {
                "name": {
                    "required": False,
                },
                "reboot_required": {
                    "required": False,
                },
                "constraints": {
                    "required": False,
                },
            },
        },
        "automatic_sync_setting_refresh_interval": {
            "required": False,
        },
        "automatic_sync_setting_refresh_interval_setting": {
            "required": False,
            "subspec": {
                "name": {
                    "required": False,
                },
                "reboot_required": {
                    "required": False,
                },
                "constraints": {
                    "required": False,
                },
            },
        },
        "transfer_throttling_bandwidth_total": {
            "required": False,
        },
        "transfer_throttling_bandwidth_total_setting": {
            "required": False,
            "subspec": {
                "name": {
                    "required": False,
                },
                "reboot_required": {
                    "required": False,
                },
                "constraints": {
                    "required": False,
                },
            },
        },
        "transfer_nfc_max_concurrent_transfers_per_host": {
            "required": False,
        },
        "transfer_nfc_max_concurrent_transfers_per_host_setting": {
            "required": False,
            "subspec": {
                "name": {
                    "required": False,
                },
                "reboot_required": {
                    "required": False,
                },
                "constraints": {
                    "required": False,
                },
            },
        },
        "priority_transfer_threads_pool_size": {
            "required": False,
        },
        "priority_transfer_threads_pool_size_setting": {
            "required": False,
            "subspec": {
                "name": {
                    "required": False,
                },
                "reboot_required": {
                    "required": False,
                },
                "constraints": {
                    "required": False,
                },
            },
        },
        "transfer_threads_pool_size": {
            "required": False,
        },
        "transfer_threads_pool_size_setting": {
            "required": False,
            "subspec": {
                "name": {
                    "required": False,
                },
                "reboot_required": {
                    "required": False,
                },
                "constraints": {
                    "required": False,
                },
            },
        },
    },
)


def create_module_argument_spec() -> dict:
    module_args = connection_params_argument_spec()
    module_args["automatic_sync_enabled"] = {
        "type": "bool",
    }
    module_args["automatic_sync_enabled_setting"] = {
        "type": "dict",
        "options": {
            "name": {
                "type": "str",
                "required": True,
            },
            "reboot_required": {
                "type": "bool",
                "required": True,
            },
            "constraints": {
                "type": "list",
                "elements": "dict",
                "required": True,
            },
        },
    }
    module_args["automatic_sync_refresh_interval"] = {
        "type": "int",
    }
    module_args["automatic_sync_refresh_interval_setting"] = {
        "type": "dict",
        "options": {
            "name": {
                "type": "str",
                "required": True,
            },
            "reboot_required": {
                "type": "bool",
                "required": True,
            },
            "constraints": {
                "type": "list",
                "elements": "dict",
                "required": True,
            },
        },
    }
    module_args["automatic_sync_setting_refresh_interval"] = {
        "type": "int",
    }
    module_args["automatic_sync_setting_refresh_interval_setting"] = {
        "type": "dict",
        "options": {
            "name": {
                "type": "str",
                "required": True,
            },
            "reboot_required": {
                "type": "bool",
                "required": True,
            },
            "constraints": {
                "type": "list",
                "elements": "dict",
                "required": True,
            },
        },
    }
    module_args["automatic_sync_start_hour"] = {
        "type": "int",
    }
    module_args["automatic_sync_start_hour_setting"] = {
        "type": "dict",
        "options": {
            "name": {
                "type": "str",
                "required": True,
            },
            "reboot_required": {
                "type": "bool",
                "required": True,
            },
            "constraints": {
                "type": "list",
                "elements": "dict",
                "required": True,
            },
        },
    }
    module_args["automatic_sync_stop_hour"] = {
        "type": "int",
    }
    module_args["automatic_sync_stop_hour_setting"] = {
        "type": "dict",
        "options": {
            "name": {
                "type": "str",
                "required": True,
            },
            "reboot_required": {
                "type": "bool",
                "required": True,
            },
            "constraints": {
                "type": "list",
                "elements": "dict",
                "required": True,
            },
        },
    }
    module_args["maximum_concurrent_item_syncs"] = {
        "type": "int",
    }
    module_args["maximum_concurrent_item_syncs_setting"] = {
        "type": "dict",
        "options": {
            "name": {
                "type": "str",
                "required": True,
            },
            "reboot_required": {
                "type": "bool",
                "required": True,
            },
            "constraints": {
                "type": "list",
                "elements": "dict",
                "required": True,
            },
        },
    }
    module_args["priority_transfer_threads_pool_size"] = {
        "type": "int",
    }
    module_args["priority_transfer_threads_pool_size_setting"] = {
        "type": "dict",
        "options": {
            "name": {
                "type": "str",
                "required": True,
            },
            "reboot_required": {
                "type": "bool",
                "required": True,
            },
            "constraints": {
                "type": "list",
                "elements": "dict",
                "required": True,
            },
        },
    }
    module_args["transfer_nfc_max_concurrent_transfers_per_host"] = {
        "type": "int",
    }
    module_args["transfer_nfc_max_concurrent_transfers_per_host_setting"] = {
        "type": "dict",
        "options": {
            "name": {
                "type": "str",
                "required": True,
            },
            "reboot_required": {
                "type": "bool",
                "required": True,
            },
            "constraints": {
                "type": "list",
                "elements": "dict",
                "required": True,
            },
        },
    }
    module_args["transfer_threads_pool_size"] = {
        "type": "int",
    }
    module_args["transfer_threads_pool_size_setting"] = {
        "type": "dict",
        "options": {
            "name": {
                "type": "str",
                "required": True,
            },
            "reboot_required": {
                "type": "bool",
                "required": True,
            },
            "constraints": {
                "type": "list",
                "elements": "dict",
                "required": True,
            },
        },
    }
    module_args["transfer_throttling_bandwidth_total"] = {
        "type": "int",
    }
    module_args["transfer_throttling_bandwidth_total_setting"] = {
        "type": "dict",
        "options": {
            "name": {
                "type": "str",
                "required": True,
            },
            "reboot_required": {
                "type": "bool",
                "required": True,
            },
            "constraints": {
                "type": "list",
                "elements": "dict",
                "required": True,
            },
        },
    }
    module_args["state"] = {
        "type": "str",
        "choices": ["present"],
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
    )

    try:
        if module.params["state"] == "present":
            result = crud_module.ensure_present()
        else:
            module.fail_json(
                msg="Unsupported state: {0}".format(module.params["state"])
            )
    except VmwareModuleError as e:
        module.fail_json(**e.to_module_fail_json_output())

    module.exit_json(**result)


if __name__ == "__main__":
    main()
