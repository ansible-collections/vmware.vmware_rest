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
module: appliance_services
short_description: Restart, start, or stop a vCenter appliance service.
description:
  - Perform lifecycle actions on a vCenter Server Appliance service.
  - Use this module to restart, start, or stop an individual service by its identifier.
  - This module is not idempotent; the requested action is always performed.

author:
  - Ansible Eco Content Team (@eco-ansible-content)

extends_documentation_fragment:
  - vmware.vmware_rest.connection_params

options:
  state:
    description:
      - The lifecycle action to perform on the service.
      - Use C(restart) to restart the service.
      - Use C(start) to start the service.
      - Use C(stop) to stop the service.
      - None of these actions are idempotent; the requested action is always performed.
    type: str
    required: true
    choices:
      - restart
      - start
      - stop
  service:
    description:
      - Identifier of the service to act on.
      - This is the service identifier used by vCenter (for example C(ntpd)).
    type: str
    required: false

version_added: 5.0.0

requirements: []

notes:
  - Generated from vSphere API spec 9.1.0.
"""

EXAMPLES = r"""
- name: Restart the ntpd service
  vmware.vmware_rest.appliance_services:
    service: ntpd
    state: restart

- name: Stop the ntpd service
  vmware.vmware_rest.appliance_services:
    service: ntpd
    state: stop

- name: Start the ntpd service
  vmware.vmware_rest.appliance_services:
    service: ntpd
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

LIST_ENDPOINT = "/appliance/services"
ITEM_ENDPOINT = "/appliance/services/{service}"


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
    "restart": OperationConfig(
        name="restart",
        uri="/appliance/services/{service}?action=restart",
        http_method="POST",
    ),
    "start": OperationConfig(
        name="start",
        uri="/appliance/services/{service}?action=start",
        http_method="POST",
    ),
    "stop": OperationConfig(
        name="stop",
        uri="/appliance/services/{service}?action=stop",
        http_method="POST",
    ),
}


def create_module_argument_spec() -> dict:
    module_args = connection_params_argument_spec()
    module_args["service"] = {
        "type": "str",
    }
    module_args["state"] = {
        "type": "str",
        "choices": ["restart", "start", "stop"],
        "required": True,
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
        action_operations=ACTION_OPERATIONS,
    )

    try:
        if module.params["state"] in ACTION_OPERATIONS:
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
