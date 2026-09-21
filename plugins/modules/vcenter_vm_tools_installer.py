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
module: vcenter_vm_tools_installer
short_description: Connect or disconnect the VMware Tools installer CD-ROM of a virtual machine.
description:
  - Connect or disconnect the VMware Tools installer CD image on a virtual machine.
  - Connecting mounts the VMware Tools installer as a CD-ROM for the guest operating system so that
    the Tools installation can be started from inside the guest.
  - On Windows guests with autorun enabled, connecting typically starts the installer automatically,
    though it still requires user input in the guest to complete. On other guest operating systems the
    installer is made available but must be launched with guest-specific steps.
  - This module only mounts or unmounts the installer media; it does not perform the installation itself.
    To track installation progress, query the Tools status with M(vmware.vmware_rest.vcenter_vm_tools_info).

author:
  - Ansible Eco Content Team (@eco-ansible-content)

extends_documentation_fragment:
  - vmware.vmware_rest.connection_params

options:
  state:
    description:
      - The action to perform on the VMware Tools installer media.
      - Use C(connect) to mount the VMware Tools installer as a CD-ROM in the guest.
      - Use C(disconnect) to unmount the VMware Tools installer CD image.
      - Both actions are always applied and do not support idempotence.
    type: str
    required: true
    choices:
      - connect
      - disconnect
  vm:
    description:
      - Identifier of the virtual machine whose VMware Tools installer media should be managed.
      - Must be an identifier (MOID) for a C(Vm) resource.
    type: str
    required: true

version_added: 5.0.0

requirements: []

notes:
  - Generated from vSphere API spec 9.1.0.
"""

EXAMPLES = r"""
- name: Connect the VMware Tools installer CD-ROM
  vmware.vmware_rest.vcenter_vm_tools_installer:
    vm: vm-1013
    state: connect

- name: Disconnect the VMware Tools installer CD image
  vmware.vmware_rest.vcenter_vm_tools_installer:
    vm: vm-1013
    state: disconnect
"""

RETURN = r"""
id:
  description: MOID of the managed virtual machine.
  returned: When state is set to a supported action.
  sample: vm-1013
  type: str
value:
  description:
    - The raw API response body from the vCenter operation.
    - The connect and disconnect actions return an empty body on success.
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

MOID_PARAMETER_HINTS = ["vm"]

LIST_ENDPOINT = ""
ITEM_ENDPOINT = "/vcenter/vm/{vm}/tools/installer"


GET_OPERATION = OperationConfig(
    name="get",
    uri=ITEM_ENDPOINT,
    http_method="GET",
)


ACTION_OPERATIONS = {
    "connect": OperationConfig(
        name="connect",
        uri="/vcenter/vm/{vm}/tools/installer?action=connect",
        http_method="POST",
    ),
    "disconnect": OperationConfig(
        name="disconnect",
        uri="/vcenter/vm/{vm}/tools/installer?action=disconnect",
        http_method="POST",
    ),
}


def create_module_argument_spec() -> dict:
    module_args = connection_params_argument_spec()
    module_args["vm"] = {
        "type": "str",
        "required": True,
    }
    module_args["state"] = {
        "type": "str",
        "choices": ["connect", "disconnect"],
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
