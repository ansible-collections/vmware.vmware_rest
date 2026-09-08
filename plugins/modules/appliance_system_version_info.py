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
module: appliance_system_version_info
short_description: Gather version information about the vCenter Server Appliance.
description:
  - Retrieve version information about the vCenter Server Appliance.
  - Returns details such as the product name, version, build number, deployment type,
    release name, and the date and time when the appliance was first installed.
  - When the appliance has been patched, the summary and release date of the applied
    patch are also reported.
  - Use this module to confirm the running version and build of the appliance before
    or after applying updates.

author:
  - Ansible Eco Content Team (@eco-ansible-content)

extends_documentation_fragment:
  - vmware.vmware_rest.connection_params

options: {}

version_added: 5.0.0

requirements: []

notes:
  - Generated from vSphere API spec 9.1.0.
"""

EXAMPLES = r"""
- name: Gather version information about the appliance
  vmware.vmware_rest.appliance_system_version_info:
  register: appliance_version

- name: Show the appliance product name, version, and build
  ansible.builtin.debug:
    msg: "{{ appliance_version.value.product }} {{ appliance_version.value.version }} build {{ appliance_version.value.build }}"
"""

RETURN = r"""
value:
  description: Detailed version information about the appliance.
  returned: On success
  type: dict
  sample:
    version: "9.1.0.10000"
    product: "VMware vCenter Server"
    build: "12345678"
    type: "vCenter Server with an embedded Platform Services Controller"
    name: "VMware vCenter Server 9.1.0"
    install_time: "2024-07-31T18:18:32.000Z"
    summary: ""
    releasedate: ""
info:
  description: A list containing the version information about the appliance.
  returned: On success
  elements: dict
  type: list
  sample:
    - version: "9.1.0.10000"
      product: "VMware vCenter Server"
      build: "12345678"
      type: "vCenter Server with an embedded Platform Services Controller"
      name: "VMware vCenter Server 9.1.0"
      install_time: "2024-07-31T18:18:32.000Z"
      summary: ""
      releasedate: ""
"""


from ansible.module_utils.basic import AnsibleModule
from ansible_collections.vmware.vmware_rest.plugins.module_utils._argument_spec import (
    connection_params_argument_spec,
)
from ansible_collections.vmware.vmware_rest.plugins.module_utils._errors import (
    VmwareModuleError,
)
from ansible_collections.vmware.vmware_rest.plugins.module_utils._info_module import (
    VmwareRestInfoModuleBase,
)
from ansible_collections.vmware.vmware_rest.plugins.module_utils._operation_configs import (
    OperationConfig,
)

MOID_PARAMETER_HINTS = []

LIST_ENDPOINT = ""
ITEM_ENDPOINT = "/appliance/system/version"


GET_OPERATION = OperationConfig(
    name="get",
    uri=ITEM_ENDPOINT,
    http_method="GET",
)


def create_module_argument_spec() -> dict:
    module_args = connection_params_argument_spec()
    return module_args


def main():
    module = AnsibleModule(
        argument_spec=create_module_argument_spec(),
        supports_check_mode=True,
    )

    info_module = VmwareRestInfoModuleBase(
        module=module,
        moid_parameter_hints=MOID_PARAMETER_HINTS,
        get_operation_config=GET_OPERATION,
    )
    try:
        result = info_module.get_resource_info()
    except VmwareModuleError as e:
        module.fail_json(**e.to_module_fail_json_output())
    module.exit_json(**result)


if __name__ == "__main__":
    main()
