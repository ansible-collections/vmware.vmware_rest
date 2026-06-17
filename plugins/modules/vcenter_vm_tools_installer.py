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
module: vcenter_vm_tools_installer
short_description: Manage the VMware Tools installer CD-ROM for a virtual machine.
description:
  - Connects or disconnects the VMware Tools installer CD image for a virtual machine.
  - Use I(state=present) to connect the VMware Tools CD installer as a CD-ROM for the
    guest operating system.
  - Use I(state=absent) to disconnect the VMware Tools installer CD image.
  - On Windows guest operating systems with autorun, connecting the installer may
    initiate the Tools installation which requires user input to complete.
author:
  - Ansible Eco Content Team (@eco-ansible-content)
extends_documentation_fragment:
  - vmware.vmware_rest.connection_params
options:
  state:
    description:
      - The desired connection state of the VMware Tools installer CD-ROM.
      - Use C(present) to connect the VMware Tools installer CD image.
      - Use C(absent) to disconnect the VMware Tools installer CD image.
    type: str
    choices:
      - present
      - absent
    default: present
  vm:
    description:
      - Identifier of the virtual machine.
      - Must be an identifier (MOID) for a C(VirtualMachine) resource.
    type: str
    required: true
version_added: 4.11.0
requirements: []
notes:
  - Generated from vSphere API spec 9.1.0.
  - Has support for vSphere API 7.0.3.
  - Has support for vSphere API 8.0.2.
"""

EXAMPLES = r"""
- name: Connect the VMware Tools installer CD
  vmware.vmware_rest.vcenter_vm_tools_installer:
    vm: vm-1009

- name: Disconnect the VMware Tools installer CD
  vmware.vmware_rest.vcenter_vm_tools_installer:
    state: absent
    vm: vm-1009
"""

RETURN = r"""
value:
  description:
    - Current installer connection state when already in the desired state.
  returned: On success when the installer state was already in the desired state
  type: dict
  sample:
    is_connected: true
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

INSTALLER_PATH = "/vcenter/vm/{vm}/tools/installer"


class VmwareRestCrudModule(VmwareRestCrudModuleBase):
    PAYLOAD_FORMAT = {
        "get": {"query": {}, "body": {}, "path": {"vm": "vm"}},
        "connect": {
            "query": {"action": "connect"},
            "body": {},
            "path": {"vm": "vm"},
        },
        "disconnect": {
            "query": {"action": "disconnect"},
            "body": {},
            "path": {"vm": "vm"},
        },
    }

    UPDATABLE_PARAMS = ()

    def _get_installer_info(self):
        path = self.build_path(INSTALLER_PATH)
        response = self.client.get(path)
        if response.status == 404:
            self.client.error_handler.handle_request_error(
                exception=UnexpectedAPIResponse(response.status, response.data),
                method="GET",
                path=path,
                request_kwargs={},
            )
        return response.json

    def _post_action(self, operation):
        path = self.build_path(INSTALLER_PATH)
        query = {"action": operation}
        response = self.client.request("POST", path, query=query)
        if response.status != 204:
            self.client.error_handler.handle_request_error(
                exception=UnexpectedAPIResponse(response.status, response.data),
                method="POST",
                path=path,
                request_kwargs={"query": query},
            )

    def ensure_present(self):
        current = self._get_installer_info()
        if current.get("is_connected"):
            return {"changed": False, "value": current}

        if not self.module.check_mode:
            self._post_action("connect")
        return {"changed": True}

    def ensure_absent(self):
        current = self._get_installer_info()
        if not current.get("is_connected"):
            return {"changed": False, "value": current}

        if not self.module.check_mode:
            self._post_action("disconnect")
        return {"changed": True}


def main():
    module_args = connection_params_argument_spec()
    module_args["state"] = {
        "type": "str",
        "choices": ["present", "absent"],
        "default": "present",
    }
    module_args["vm"] = {"type": "str", "required": True}

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
