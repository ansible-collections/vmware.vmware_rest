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
module: vcenter_vm_guest_filesystem_directories
short_description: Manages directories in a virtual machine guest filesystem.
description:
  - Creates, deletes, moves, or creates temporary directories in a virtual machine guest
    operating system through VMware Tools guest operations.
  - Use I(state=present) to create a directory.
  - Use I(state=absent) to delete a directory.
  - Use I(state=move) to rename or move a directory.
  - Use I(state=create_temporary) to create a guest temporary directory.
  - Guest credentials are required for all operations.
author:
  - Ansible Eco Content Team (@eco-ansible-content)
extends_documentation_fragment:
  - vmware.vmware_rest.connection_params
options:
  state:
    description:
      - The desired directory operation.
      - Use C(present) to create a directory.
      - Use C(absent) to delete a directory.
      - Use C(move) to rename or move a directory.
      - Use C(create_temporary) to create a temporary directory.
    type: str
    choices:
      - present
      - absent
      - move
      - create_temporary
    default: present
  vm:
    description:
      - Identifier of the virtual machine.
      - Must be an identifier (MOID) for a C(VirtualMachine) resource.
    type: str
    required: true
  path:
    description:
      - Complete path to the directory for create, delete, or move operations.
    type: str
  new_path:
    description:
      - Complete destination path when I(state=move).
      - Cannot be a path to an existing directory or file.
    type: str
  create_parents:
    description:
      - Whether parent directories should be created when I(state=present).
      - If any failure occurs, some parent directories could be left behind.
    type: bool
  recursive:
    description:
      - Whether all files and subdirectories are deleted when I(state=absent).
      - When false, the directory must be empty for deletion to succeed.
    type: bool
  prefix:
    description:
      - Prefix for the new temporary directory when I(state=create_temporary).
    type: str
  suffix:
    description:
      - Suffix for the new temporary directory when I(state=create_temporary).
    type: str
  parent_path:
    description:
      - Complete path to the parent directory when I(state=create_temporary).
      - When not set, a guest-specific default is used.
    type: str
  credentials:
    description:
      - Guest authentication credentials for the operation.
    type: dict
    required: true
    suboptions:
      interactive_session:
        description:
          - Whether the operation interacts with the logged-in desktop session in the guest.
          - The logged-on user must match the user specified in the credentials.
          - Currently only supported for C(USERNAME_PASSWORD) credentials.
        type: bool
        required: true
      type:
        description:
          - Guest credentials type.
        type: str
        required: true
        choices:
          - USERNAME_PASSWORD
          - SAML_BEARER_TOKEN
      user_name:
        description:
          - Guest username for C(USERNAME_PASSWORD) credentials.
          - For C(SAML_BEARER_TOKEN), the guest user associated with the credentials.
        type: str
      password:
        description:
          - Password for C(USERNAME_PASSWORD) credentials.
        type: str
      saml_token:
        description:
          - SAML bearer token for C(SAML_BEARER_TOKEN) credentials.
        type: str
version_added: 4.11.0
requirements: []
notes:
  - Generated from vSphere API spec 9.1.0.
  - Has support for vSphere API 7.0.3.
  - Has support for vSphere API 8.0.2.
"""

EXAMPLES = r"""
- name: Create a directory in the guest filesystem
  vmware.vmware_rest.vcenter_vm_guest_filesystem_directories:
    vm: vm-1001
    path: /tmp/my/path
    create_parents: true
    credentials:
      interactive_session: false
      type: USERNAME_PASSWORD
      user_name: root
      password: "{{ guest_password }}"

- name: Move a guest directory
  vmware.vmware_rest.vcenter_vm_guest_filesystem_directories:
    vm: vm-1001
    state: move
    path: /tmp/my/path
    new_path: /tmp/my/new_path
    credentials:
      interactive_session: false
      type: USERNAME_PASSWORD
      user_name: root
      password: "{{ guest_password }}"

- name: Create a temporary guest directory
  vmware.vmware_rest.vcenter_vm_guest_filesystem_directories:
    vm: vm-1001
    state: create_temporary
    prefix: ansible
    suffix: test
    credentials:
      interactive_session: false
      type: USERNAME_PASSWORD
      user_name: root
      password: "{{ guest_password }}"
  register: temp_dir

- name: Delete a guest directory
  vmware.vmware_rest.vcenter_vm_guest_filesystem_directories:
    vm: vm-1001
    state: absent
    path: /tmp/my/path
    recursive: true
    credentials:
      interactive_session: false
      type: USERNAME_PASSWORD
      user_name: root
      password: "{{ guest_password }}"
"""

RETURN = r"""
value:
  description:
    - API response details for idempotent outcomes, or the temporary directory path
      when I(state=create_temporary).
  returned: When the operation is idempotent or when I(state=create_temporary)
  type: raw
  sample: /tmp/ansibleXXXXXXtest
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.vmware.vmware_rest.plugins.module_utils._argument_spec import (
    connection_params_argument_spec,
)
from ansible_collections.vmware.vmware_rest.plugins.module_utils._errors import (
    UnexpectedAPIResponse,
)
from ansible_collections.vmware.vmware_rest.plugins.module_utils._module_base import (
    VmwareRestModuleBase,
)

DIRECTORIES_PATH = "/vcenter/vm/{vm}/guest/filesystem/directories"

_CREDENTIALS_OPTIONS = {
    "interactive_session": {"type": "bool", "required": True},
    "type": {
        "type": "str",
        "required": True,
        "choices": ["USERNAME_PASSWORD", "SAML_BEARER_TOKEN"],
    },
    "user_name": {"type": "str"},
    "password": {"type": "str", "no_log": True},
    "saml_token": {"type": "str", "no_log": True},
}

_PAYLOAD_FORMAT = {
    "create": {
        "query": {},
        "body": {
            "create_parents": "create_parents",
            "credentials": "credentials",
            "path": "path",
        },
        "path": {"vm": "vm"},
    },
    "delete": {
        "query": {},
        "body": {
            "credentials": "credentials",
            "path": "path",
            "recursive": "recursive",
        },
        "path": {"vm": "vm"},
    },
    "move": {
        "query": {},
        "body": {
            "credentials": "credentials",
            "new_path": "new_path",
            "path": "path",
        },
        "path": {"vm": "vm"},
    },
    "create_temporary": {
        "query": {},
        "body": {
            "credentials": "credentials",
            "parent_path": "parent_path",
            "prefix": "prefix",
            "suffix": "suffix",
        },
        "path": {"vm": "vm"},
    },
}

_ACTIONS = {
    "create": "create",
    "delete": "delete",
    "move": "move",
    "create_temporary": "createTemporary",
}


class VmwareRestModule(VmwareRestModuleBase):
    PAYLOAD_FORMAT = _PAYLOAD_FORMAT

    def _error_payload(self, response):
        try:
            return response.json
        except Exception:
            return {}

    def _is_already_exists(self, error):
        if error.get("type") == "com.vmware.vapi.std.errors.already_exists":
            return True
        value = error.get("value")
        if isinstance(value, dict) and value.get("error_type") == "ALREADY_EXISTS":
            return True
        return False

    def _is_not_found(self, error):
        if error.get("type") == "com.vmware.vapi.std.errors.not_found":
            return True
        value = error.get("value")
        if isinstance(value, dict) and value.get("error_type") == "NOT_FOUND":
            return True
        return False

    def _fail_unexpected(self, response, method, path, request_kwargs):
        self.client.error_handler.handle_request_error(
            exception=UnexpectedAPIResponse(response.status, response.data),
            method=method,
            path=path,
            request_kwargs=request_kwargs,
        )

    def _post_action(self, operation):
        path = self.build_path(DIRECTORIES_PATH)
        body = self.build_payload(self.PAYLOAD_FORMAT[operation])
        query = {"action": _ACTIONS[operation]}
        request_kwargs = {"data": body, "query": query}
        response = self.client.request("POST", path, data=body, query=query)
        return response, path, request_kwargs

    def run_create(self):
        response, path, request_kwargs = self._post_action("create")
        if response.status == 204:
            return {"changed": True}

        error = self._error_payload(response)
        if self._is_already_exists(error):
            value = error.get("value", error)
            return {"changed": False, "value": value}

        self._fail_unexpected(response, "POST", path, request_kwargs)

    def run_delete(self):
        response, path, request_kwargs = self._post_action("delete")
        if response.status == 204:
            return {"changed": True}

        error = self._error_payload(response)
        if response.status == 404 or self._is_not_found(error):
            return {"changed": False}

        self._fail_unexpected(response, "POST", path, request_kwargs)

    def run_move(self):
        response, path, request_kwargs = self._post_action("move")
        if response.status == 204:
            return {"changed": True}

        self._fail_unexpected(response, "POST", path, request_kwargs)

    def run_create_temporary(self):
        response, path, request_kwargs = self._post_action("create_temporary")
        if response.status != 200:
            self._fail_unexpected(response, "POST", path, request_kwargs)

        result = response.json
        if isinstance(result, dict) and "value" in result:
            result = result["value"]
        return {"changed": True, "value": result}


def main():
    module_args = connection_params_argument_spec()
    module_args["state"] = {
        "type": "str",
        "choices": ["present", "absent", "move", "create_temporary"],
        "default": "present",
    }
    module_args["vm"] = {"type": "str", "required": True}
    module_args["path"] = {"type": "str"}
    module_args["new_path"] = {"type": "str"}
    module_args["create_parents"] = {"type": "bool"}
    module_args["recursive"] = {"type": "bool"}
    module_args["prefix"] = {"type": "str"}
    module_args["suffix"] = {"type": "str"}
    module_args["parent_path"] = {"type": "str"}
    module_args["credentials"] = {
        "type": "dict",
        "required": True,
        "options": _CREDENTIALS_OPTIONS,
    }

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False,
        required_if=[
            ("state", "present", ["path", "credentials"]),
            ("state", "absent", ["path", "credentials"]),
            ("state", "move", ["path", "new_path", "credentials"]),
            ("state", "create_temporary", ["prefix", "suffix", "credentials"]),
        ],
    )

    guest_module = VmwareRestModule(module)
    state = module.params["state"]

    if state == "present":
        result = guest_module.run_create()
    elif state == "absent":
        result = guest_module.run_delete()
    elif state == "move":
        result = guest_module.run_move()
    elif state == "create_temporary":
        result = guest_module.run_create_temporary()
    else:
        module.fail_json(msg="Unsupported state: {0}".format(state))

    module.exit_json(**result)


if __name__ == "__main__":
    main()
