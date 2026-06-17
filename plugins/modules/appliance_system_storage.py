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
module: appliance_system_storage
short_description: Resize all partitions to 100 percent of disk size.
description:
  - Resizes vCenter Server appliance storage partitions to use the full disk size.
  - Use I(state=resize) to resize all partitions without returning partition details.
  - Use I(state=resize_ex) to resize all partitions and return partition sizes before and after the operation.
author:
  - Ansible Eco Content Team (@eco-ansible-content)
extends_documentation_fragment:
  - vmware.vmware_rest.connection_params
options:
  state:
    description:
      - The storage resize operation to perform.
      - Use C(resize) to resize all partitions to 100 percent of disk size.
      - Use C(resize_ex) to resize all partitions and return partition size changes.
    type: str
    choices:
      - resize
      - resize_ex
    required: true
version_added: 4.11.0
requirements: []
notes:
  - Generated from vSphere API spec 9.1.0.
  - Has support for vSphere API 7.0.3.
  - Has support for vSphere API 8.0.2.
"""

EXAMPLES = r"""
- name: Resize all partitions and return partition size changes
  vmware.vmware_rest.appliance_system_storage:
    state: resize_ex
  register: storage_resize_result

- name: Resize all partitions
  vmware.vmware_rest.appliance_system_storage:
    state: resize
"""

RETURN = r"""
value:
  description:
    - Partition size changes keyed by partition name.
    - Returned only when I(state=resize_ex).
  returned: On success when I(state=resize_ex)
  type: dict
  sample:
    lv_root_0:
      new_size: 104312832
      old_size: 53985280
  contains:
    new_size:
      description:
        - New size of the partition in MB.
      type: int
      sample: 104312832
    old_size:
      description:
        - Original size of the partition in MB.
      type: int
      sample: 53985280
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
)

STORAGE_PATH = "/appliance/system/storage"

PAYLOAD_FORMAT = {
    "resize": {
        "query": {"action": "resize"},
        "body": {},
        "path": {},
    },
    "resize_ex": {
        "query": {"action": "resize-ex"},
        "body": {},
        "path": {},
    },
}


class VmwareRestCrudModule(VmwareRestCrudModuleBase):
    PAYLOAD_FORMAT = PAYLOAD_FORMAT

    UPDATABLE_PARAMS = ()

    def _post_resize(self, action):
        query = {"action": "resize-ex" if action == "resize_ex" else action}
        response = self.client.request("POST", STORAGE_PATH, query=query)
        expected_status = 204 if action == "resize" else 200
        if response.status != expected_status:
            self.client.error_handler.handle_request_error(
                exception=UnexpectedAPIResponse(response.status, response.data),
                method="POST",
                path=STORAGE_PATH,
                request_kwargs={"query": query},
            )
        return response

    def run_action(self, action):
        response = self._post_resize(action)
        result = {"changed": True}
        if action == "resize_ex":
            payload = response.json
            if isinstance(payload, dict) and "value" in payload:
                payload = payload["value"]
            result["value"] = payload
        return result

    def ensure_present(self):
        self.module.fail_json(
            msg="Use state resize or resize_ex to resize appliance storage partitions."
        )

    def ensure_absent(self):
        self.module.fail_json(
            msg="Use state resize or resize_ex to resize appliance storage partitions."
        )


def main():
    module_args = connection_params_argument_spec()
    module_args["state"] = {
        "type": "str",
        "choices": ["resize", "resize_ex"],
        "required": True,
    }

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False,
    )

    crud_module = VmwareRestCrudModule(module)
    result = crud_module.run_action(module.params["state"])
    module.exit_json(**result)


if __name__ == "__main__":
    main()
