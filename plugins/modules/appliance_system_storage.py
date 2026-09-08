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
module: appliance_system_storage
short_description: Resize the storage partitions of the vCenter Server Appliance.
description:
  - Resize all storage partitions of the vCenter Server Appliance to use 100 percent
    of the underlying disk size.
  - Use this module after enlarging one or more of the appliance's virtual disks so
    that the partitions grow to fill the newly available space.
  - Use M(vmware.vmware_rest.appliance_system_storage_info) to view the disk to
    partition mapping before resizing.

author:
  - Ansible Eco Content Team (@eco-ansible-content)

extends_documentation_fragment:
  - vmware.vmware_rest.connection_params

options:
  state:
    description:
      - The resize action to perform on the appliance storage partitions.
      - Use C(resize) to resize all partitions to 100 percent of the disk size.
      - Use C(resize-ex) to resize all partitions and return the size of each
        partition before and after the operation.
      - Neither action is idempotent; each run attempts to resize the partitions.
    type: str
    required: true
    choices:
      - resize
      - resize-ex

version_added: 5.0.0

requirements: []

notes:
  - Generated from vSphere API spec 9.1.0.
"""

EXAMPLES = r"""
- name: Resize all appliance storage partitions to fill their disks
  vmware.vmware_rest.appliance_system_storage:
    state: resize

- name: Resize partitions and report the size change of each one
  vmware.vmware_rest.appliance_system_storage:
    state: resize-ex
  register: resize_result
"""

RETURN = r"""
value:
  description:
    - The raw API response body from the vCenter operation.
    - Empty when O(state=resize).
    - When O(state=resize-ex), a mapping of each partition to its size in MB before
      and after the resize.
  returned: On success
  type: raw
  sample:
    /storage/log:
      old_size: 10240
      new_size: 25600
    /storage/db:
      old_size: 10240
      new_size: 25600
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
ITEM_ENDPOINT = "/appliance/system/storage"


GET_OPERATION = OperationConfig(
    name="get",
    uri=ITEM_ENDPOINT,
    http_method="GET",
)


ACTION_OPERATIONS = {
    "resize": OperationConfig(
        name="resize",
        uri="/appliance/system/storage?action=resize",
        http_method="POST",
    ),
    "resize-ex": OperationConfig(
        name="resize-ex",
        uri="/appliance/system/storage?action=resize-ex",
        http_method="POST",
    ),
}


def create_module_argument_spec() -> dict:
    module_args = connection_params_argument_spec()
    module_args["state"] = {
        "type": "str",
        "choices": ["resize", "resize-ex"],
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
