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
module: vcenter_vm_guest_filesystem_directories
short_description: Manage directories in the guest operating system of a virtual machine.
description:
  - Create, delete, or move directories within the guest operating system of a
    running virtual machine.
  - Operations are performed through VMware Tools, so VMware Tools must be
    installed and running in the guest, and valid guest credentials must be
    supplied for every action.
  - Use O(state=create) to create a directory, O(state=createTemporary) to create
    a uniquely named temporary directory, O(state=delete) to remove a directory,
    and O(state=move) to move or rename a directory.
  - None of the actions are idempotent; each call performs the requested guest
    operation directly.

author:
  - Ansible Eco Content Team (@eco-ansible-content)

extends_documentation_fragment:
  - vmware.vmware_rest.connection_params

options:
  state:
    description:
      - The desired state of the resource.
      - Use C(create) to perform the create action.
      - Use C(createTemporary) to perform the createTemporary action.
      - Use C(delete) to perform the delete action.
      - Use C(move) to perform the move action.
      - This module does not support idempotence.
    type: str
    required: true
    choices:
      - create
      - createTemporary
      - delete
      - move
  vm:
    description:
      - Identifier of the vm to manage.
      - Must be an identifier (MOID) for a C(Vm) resource.
    type: str
    required: true
  credentials:
    description:
      - The guest operating system credentials used to authenticate and run the
        requested operation inside the virtual machine.
      - Required for every action.
    type: dict
    required: false
    suboptions:
      interactive_session:
        description:
          - If V(true), the operation interacts with the logged-in desktop session
            in the guest. This requires that the logged-on user matches the user
            named in O(credentials.user_name).
          - Only supported when O(credentials.type=USERNAME_PASSWORD).
        type: bool
        required: false
      type:
        description:
          - The type of guest credentials being supplied.
          - V(USERNAME_PASSWORD) authenticates with a guest username and password.
            Supply O(credentials.user_name) and O(credentials.password).
          - V(SAML_BEARER_TOKEN) authenticates with a SAML bearer token obtained
            from the VMware SSO server, associated with a guest account through a
            guest alias. Supply O(credentials.saml_token) and optionally
            O(credentials.user_name).
        type: str
        required: false
        choices:
          - USERNAME_PASSWORD
          - SAML_BEARER_TOKEN
      user_name:
        description:
          - The guest username to authenticate as.
          - When O(credentials.type=USERNAME_PASSWORD), this is the guest account
            username.
          - When O(credentials.type=SAML_BEARER_TOKEN), this is the guest user to
            associate with the token. If omitted, a guest-dependent mapping
            determines which guest account is used.
        type: str
        required: false
      password:
        description:
          - The password for the guest account named in O(credentials.user_name).
          - Only relevant when O(credentials.type=USERNAME_PASSWORD).
        type: str
        required: false
      saml_token:
        description:
          - The SAML bearer token used to authenticate within the guest.
          - Only relevant when O(credentials.type=SAML_BEARER_TOKEN).
        type: str
        required: false
  path:
    description:
      - The complete path, in the guest filesystem, of the directory to act on.
      - When O(state=create), this is the directory to create.
      - When O(state=delete), this is the directory to delete.
      - When O(state=move), this is the existing directory to move or rename.
      - Required when O(state=create), O(state=delete), or O(state=move).
    type: str
    required: false
  create_parents:
    description:
      - Whether to create any missing parent directories along the path.
      - If a failure occurs, some parent directories may be left behind.
      - When omitted, parent directories are not created.
      - Used when O(state=create).
    type: bool
    required: false
  prefix:
    description:
      - The prefix for the name of the new temporary directory.
      - Required when O(state=createTemporary).
    type: str
    required: false
  suffix:
    description:
      - The suffix for the name of the new temporary directory.
      - Required when O(state=createTemporary).
    type: str
    required: false
  parent_path:
    description:
      - The complete path, in the guest filesystem, of the directory in which to
        create the new temporary directory.
      - When omitted, a guest-specific default location is used.
      - Used when O(state=createTemporary).
    type: str
    required: false
  recursive:
    description:
      - If V(true), all files and subdirectories are deleted as well. If V(false),
        the directory must be empty for the deletion to succeed.
      - When omitted, directory contents are not deleted.
      - Used when O(state=delete).
    type: bool
    required: false
  new_path:
    description:
      - The complete path, in the guest filesystem, to move the directory to, or
        its new name.
      - It must not point to an existing directory or an existing file.
      - Required when O(state=move).
    type: str
    required: false

version_added: 5.0.0

requirements: []

notes:
  - Generated from vSphere API spec 9.1.0.
"""

EXAMPLES = r"""
- name: Create a directory in the guest
  vmware.vmware_rest.vcenter_vm_guest_filesystem_directories:
    vm: vm-1234
    state: create
    path: /tmp/ansible_app
    credentials:
      type: USERNAME_PASSWORD
      user_name: root
      password: guest_password

- name: Create a directory and any missing parent directories
  vmware.vmware_rest.vcenter_vm_guest_filesystem_directories:
    vm: vm-1234
    state: create
    path: /opt/app/config/nested
    create_parents: true
    credentials:
      type: USERNAME_PASSWORD
      user_name: root
      password: guest_password

- name: Create a uniquely named temporary directory
  vmware.vmware_rest.vcenter_vm_guest_filesystem_directories:
    vm: vm-1234
    state: createTemporary
    prefix: ansible_
    suffix: _tmp
    parent_path: /tmp
    credentials:
      type: USERNAME_PASSWORD
      user_name: root
      password: guest_password
  register: temp_dir

- name: Move or rename a directory
  vmware.vmware_rest.vcenter_vm_guest_filesystem_directories:
    vm: vm-1234
    state: move
    path: /tmp/ansible_app
    new_path: /opt/ansible_app
    credentials:
      type: USERNAME_PASSWORD
      user_name: root
      password: guest_password

- name: Delete a directory and all of its contents
  vmware.vmware_rest.vcenter_vm_guest_filesystem_directories:
    vm: vm-1234
    state: delete
    path: /opt/ansible_app
    recursive: true
    credentials:
      type: USERNAME_PASSWORD
      user_name: root
      password: guest_password
"""

RETURN = r"""
value:
  description:
    - The raw API response body from the vCenter operation.
    - When O(state=createTemporary), this is the complete path of the newly
      created temporary directory in the guest.
    - For O(state=create), O(state=delete), and O(state=move) the operation
      returns no content.
  returned: On success
  type: raw
  sample: /tmp/ansible_abc123_tmp
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

MOID_PARAMETER_HINTS = ["vm"]

LIST_ENDPOINT = ""
ITEM_ENDPOINT = ""


ACTION_OPERATIONS = {
    "create": OperationConfig(
        name="create",
        uri="/vcenter/vm/{vm}/guest/filesystem/directories?action=create",
        http_method="POST",
        body_spec={
            "credentials": {
                "required": True,
                "subspec": {
                    "interactive_session": {
                        "required": False,
                    },
                    "type": {
                        "required": False,
                    },
                    "user_name": {
                        "required": False,
                    },
                    "password": {
                        "required": False,
                    },
                    "saml_token": {
                        "required": False,
                    },
                },
            },
            "path": {
                "required": True,
            },
            "create_parents": {
                "required": False,
            },
        },
    ),
    "createTemporary": OperationConfig(
        name="createTemporary",
        uri="/vcenter/vm/{vm}/guest/filesystem/directories?action=createTemporary",
        http_method="POST",
        body_spec={
            "credentials": {
                "required": True,
                "subspec": {
                    "interactive_session": {
                        "required": False,
                    },
                    "type": {
                        "required": False,
                    },
                    "user_name": {
                        "required": False,
                    },
                    "password": {
                        "required": False,
                    },
                    "saml_token": {
                        "required": False,
                    },
                },
            },
            "prefix": {
                "required": True,
            },
            "suffix": {
                "required": True,
            },
            "parent_path": {
                "required": False,
            },
        },
    ),
    "delete": OperationConfig(
        name="delete",
        uri="/vcenter/vm/{vm}/guest/filesystem/directories?action=delete",
        http_method="POST",
        body_spec={
            "credentials": {
                "required": True,
                "subspec": {
                    "interactive_session": {
                        "required": False,
                    },
                    "type": {
                        "required": False,
                    },
                    "user_name": {
                        "required": False,
                    },
                    "password": {
                        "required": False,
                    },
                    "saml_token": {
                        "required": False,
                    },
                },
            },
            "path": {
                "required": True,
            },
            "recursive": {
                "required": False,
            },
        },
    ),
    "move": OperationConfig(
        name="move",
        uri="/vcenter/vm/{vm}/guest/filesystem/directories?action=move",
        http_method="POST",
        body_spec={
            "credentials": {
                "required": True,
                "subspec": {
                    "interactive_session": {
                        "required": False,
                    },
                    "type": {
                        "required": False,
                    },
                    "user_name": {
                        "required": False,
                    },
                    "password": {
                        "required": False,
                    },
                    "saml_token": {
                        "required": False,
                    },
                },
            },
            "path": {
                "required": True,
            },
            "new_path": {
                "required": True,
            },
        },
    ),
}


def create_module_argument_spec() -> dict:
    module_args = connection_params_argument_spec()
    module_args["create_parents"] = {
        "type": "bool",
    }
    module_args["credentials"] = {
        "type": "dict",
        "options": {
            "interactive_session": {
                "type": "bool",
            },
            "type": {
                "type": "str",
                "choices": ["USERNAME_PASSWORD", "SAML_BEARER_TOKEN"],
            },
            "user_name": {
                "type": "str",
            },
            "password": {
                "type": "str",
                "no_log": True,
            },
            "saml_token": {
                "type": "str",
                "no_log": True,
            },
        },
    }
    module_args["new_path"] = {
        "type": "str",
    }
    module_args["parent_path"] = {
        "type": "str",
    }
    module_args["path"] = {
        "type": "str",
    }
    module_args["prefix"] = {
        "type": "str",
    }
    module_args["recursive"] = {
        "type": "bool",
    }
    module_args["suffix"] = {
        "type": "str",
    }
    module_args["vm"] = {
        "type": "str",
        "required": True,
    }
    module_args["state"] = {
        "type": "str",
        "choices": ["create", "createTemporary", "delete", "move"],
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
