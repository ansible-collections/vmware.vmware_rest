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
module: vcenter_vm_info
short_description: PLACEHOLDER
description:
  - PLACEHOLDER

author:
  - Ansible Eco Content Team (@eco-ansible-content)

extends_documentation_fragment:
  - vmware.vmware_rest.connection_params

options:
  vm:
    description:
      - Identifier of the vm to manage.
      - Must be an identifier (MOID) for a C(Vm) resource.
    type: str
    required: false
  vms:
    description:
      - Identifiers of virtual machines that can match the filter.
      - If missing or 'null' or empty, virtual machines with any identifier match the filter.
      - When clients pass a value of this schema as a parameter, the property must contain identifiers (MOIDs) for the resource type 'VirtualMachine'. When operations return a value of this schema as a response, the property will contain identifiers (MOIDs) for the resource type 'VirtualMachine'.
    type: list
    required: false
    elements: str
  names:
    aliases:
      - filter_names
    description:
      - Names that virtual machines must have to match the filter (see *Vcenter.VM.Info.name*).
      - If missing or 'null' or empty, virtual machines with any name match the filter.
    type: list
    required: false
    elements: str
  folders:
    aliases:
      - filter_folders
    description:
      - Folders that must contain the virtual machine for the virtual machine to match the filter.
      - If missing or 'null' or empty, virtual machines in any folder match the filter.
      - When clients pass a value of this schema as a parameter, the property must contain identifiers (MOIDs) for the resource type 'Folder'. When operations return a value of this schema as a response, the property will contain identifiers (MOIDs) for the resource type 'Folder'.
    type: list
    required: false
    elements: str
  datacenters:
    aliases:
      - filter_datacenters
    description:
      - Datacenters that must contain the virtual machine for the virtual machine to match the filter.
      - If missing or 'null' or empty, virtual machines in any datacenter match the filter.
      - When clients pass a value of this schema as a parameter, the property must contain identifiers (MOIDs) for the resource type 'Datacenter'. When operations return a value of this schema as a response, the property will contain identifiers (MOIDs) for the resource type 'Datacenter'.
    type: list
    required: false
    elements: str
  hosts:
    description:
      - Hosts that must contain the virtual machine for the virtual machine to match the filter.
      - If missing or 'null' or empty, virtual machines on any host match the filter.
      - When clients pass a value of this schema as a parameter, the property must contain identifiers (MOIDs) for the resource type 'HostSystem'. When operations return a value of this schema as a response, the property will contain identifiers (MOIDs) for the resource type 'HostSystem'.
    type: list
    required: false
    elements: str
  clusters:
    description:
      - Clusters that must contain the virtual machine for the virtual machine to match the filter.
      - If missing or 'null' or empty, virtual machines in any cluster match the filter.
      - When clients pass a value of this schema as a parameter, the property must contain identifiers (MOIDs) for the resource type 'ClusterComputeResource'. When operations return a value of this schema as a response, the property will contain identifiers (MOIDs) for the resource type 'ClusterComputeResource'.
    type: list
    required: false
    elements: str
  resource_pools:
    description:
      - Resource pools that must contain the virtual machine for the virtual machine to match the filter.
      - If missing or 'null' or empty, virtual machines in any resource pool match the filter.
      - When clients pass a value of this schema as a parameter, the property must contain identifiers (MOIDs) for the resource type 'ResourcePool'. When operations return a value of this schema as a response, the property will contain identifiers (MOIDs) for the resource type 'ResourcePool'.
    type: list
    required: false
    elements: str
  power_states:
    description:
      - Power states that a virtual machine must be in to match the filter (see *Vcenter.Vm.Power.Info.state*.
      - POWERED_OFF - The virtual machine is powered off.
      - POWERED_ON - The virtual machine is powered on.
      - SUSPENDED - The virtual machine is suspended.
      - For more information see *Vcenter.Vm.Power.State*.
      - If missing or 'null' or empty, virtual machines in any power state match the filter.
    type: list
    required: false
    elements: str

version_added: 5.0.0

requirements: []

notes:
  - Generated from vSphere API spec 9.1.0.
"""

EXAMPLES = r"""
"""

RETURN = r"""
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

MOID_PARAMETER_HINTS = ["vm"]

LIST_ENDPOINT = "/vcenter/vm"
ITEM_ENDPOINT = "/vcenter/vm/{vm}"


LIST_OPERATION = OperationConfig(
    name="list",
    uri=LIST_ENDPOINT,
    http_method="GET",
    query_spec={
        "vms": {
            "required": False,
        },
        "names": {
            "required": False,
        },
        "folders": {
            "required": False,
        },
        "datacenters": {
            "required": False,
        },
        "hosts": {
            "required": False,
        },
        "clusters": {
            "required": False,
        },
        "resource_pools": {
            "required": False,
        },
        "power_states": {
            "required": False,
        },
    },
)

GET_OPERATION = OperationConfig(
    name="get",
    uri=ITEM_ENDPOINT,
    http_method="GET",
)


def create_module_argument_spec() -> dict:
    module_args = connection_params_argument_spec()
    module_args["clusters"] = {
        "type": "list",
        "elements": "str",
    }
    module_args["datacenters"] = {
        "type": "list",
        "aliases": ["filter_datacenters"],
        "elements": "str",
    }
    module_args["folders"] = {
        "type": "list",
        "aliases": ["filter_folders"],
        "elements": "str",
    }
    module_args["hosts"] = {
        "type": "list",
        "elements": "str",
    }
    module_args["names"] = {
        "type": "list",
        "aliases": ["filter_names"],
        "elements": "str",
    }
    module_args["power_states"] = {
        "type": "list",
        "elements": "str",
    }
    module_args["resource_pools"] = {
        "type": "list",
        "elements": "str",
    }
    module_args["vm"] = {
        "type": "str",
    }
    module_args["vms"] = {
        "type": "list",
        "elements": "str",
    }
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
        list_operation_config=LIST_OPERATION,
    )
    try:
        result = info_module.get_resource_info()
    except VmwareModuleError as e:
        module.fail_json(**e.to_module_fail_json_output())
    module.exit_json(**result)


if __name__ == "__main__":
    main()
