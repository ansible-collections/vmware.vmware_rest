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
module: appliance_vmon_service
short_description: Manage vCenter appliance service states.
description:
  - Start, stop, or restart a vCenter appliance service.
  - This module can also be used to manage a service's startup settings.
  - This module is not idempotent.

deprecated:
  removed_in: 6.0.0
  why: This endpoint is no longer supported by Broadcom.
  alternative: Use M(vmware.vmware_rest.appliance_services) for service management.

author:
  - Ansible Eco Content Team (@eco-ansible-content)

extends_documentation_fragment:
  - vmware.vmware_rest.connection_params

options:
  service:
    description:
      - Identifier of the service whose state is being managed.
    required: true
    type: str

  request_body:
    description:
      - Properties to set when managing a service and O(state) is C(present).
    type: dict
    required: false
    suboptions:
      startup_type:
        choices:
          - AUTOMATIC
          - DISABLED
          - MANUAL
        description:
          - The type of startup strategy for the service.
        type: str
        required: true

  state:
    choices:
      - start
      - stop
      - present
    default: present
    description:
      - Whether to attempt to start or stop the service, or manage the the startup_type (C(present)).
    type: str

version_added: 5.0.0
requirements: []

notes:
  - Generated from vSphere API spec 8.0.2.
"""

EXAMPLES = r"""
- name: Adjust vpxd configuration
  vmware.vmware_rest.appliance_vmon_service:
    service: vpxd
    startup_type: AUTOMATIC

- name: Start the vpxd configuration
  vmware.vmware_rest.appliance_vmon_service:
    service: vpxd
    state: start
"""

RETURN = r"""
value:
  description: The raw API response body from the vCenter operation. Empty when the operation returns no content.
  returned: On success
  type: raw
  sample: {}
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

MOID_PARAMETER_HINTS = ["service"]

LIST_ENDPOINT = "/appliance/vmon/service"
ITEM_ENDPOINT = "/appliance/vmon/service/{service}"


LIST_OPERATION = OperationConfig(
    name="list",
    uri=LIST_ENDPOINT,
    http_method="GET",
)

GET_OPERATION = OperationConfig(
    name="get",
    uri=ITEM_ENDPOINT,
    http_method="GET",
)

ACTION_OPERATIONS = {
    "start": OperationConfig(
        name="start",
        uri="/appliance/vmon/service/{service}/start",
        http_method="POST",
    ),
    "stop": OperationConfig(
        name="stop",
        uri="/appliance/vmon/service/{service}/stop",
        http_method="POST",
    ),
}

UPDATE_OPERATION = OperationConfig(
    name="update",
    uri=ITEM_ENDPOINT,
    http_method="PATCH",
    body_spec={
        "request_body": {
            "required": True,
            "subspec": {
                "startup_type": {
                    "required": True,
                },
            },
        },
    },
)


def create_module_argument_spec() -> dict:
    module_args = connection_params_argument_spec()
    module_args["service"] = {"type": "str", "required": True}
    module_args["request_body"] = {
        "type": "dict",
        "options": {
            "startup_type": {
                "type": "str",
                "choices": ["AUTOMATIC", "DISABLED", "MANUAL"],
                "required": True,
            }
        },
    }
    module_args["state"] = {
        "type": "str",
        "choices": ["present", "start", "stop"],
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
        list_operation_config=LIST_OPERATION,
        update_operation_config=UPDATE_OPERATION,
        action_operations=ACTION_OPERATIONS,
    )

    try:
        if module.params["state"] == "present":
            result = crud_module.ensure_present()
        elif module.params["state"] in ACTION_OPERATIONS:
            result = crud_module.perform_action()
        else:
            module.fail_json(
                msg="Unsupported state: {0}".format(module.params["state"])
            )
    except VmwareModuleError as e:
        module.fail_json(**e.to_module_fail_json_output())

    module.exit_json(**result)


if __name__ == "__main__":
    main()
