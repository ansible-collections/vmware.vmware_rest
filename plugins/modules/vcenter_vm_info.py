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
short_description: Gather information about virtual machines in vCenter.
description:
  - Retrieve information about one or more virtual machines managed by vCenter.
  - When a virtual machine identifier is supplied, return the full configuration details for that single
    virtual machine, including its hardware, boot options, CPU, memory, disks, and network adapters.
  - When no identifier is supplied, return a summary list of virtual machines, optionally narrowed using
    the available filters such as names, folders, datacenters, hosts, clusters, resource pools, and power states.

author:
  - Ansible Eco Content Team (@eco-ansible-content)

extends_documentation_fragment:
  - vmware.vmware_rest.connection_params

options:
  vm:
    description:
      - Identifier of the virtual machine to retrieve full configuration details for.
      - Must be the MOID (managed object identifier) of a C(Vm) resource.
      - When set, the module returns detailed information about this single virtual machine instead of a summary list.
    type: str
    required: false
  vms:
    description:
      - Limit the results to virtual machines with these identifiers (MOIDs).
      - Each value must be the MOID of a C(Vm) resource.
      - If omitted or empty, virtual machines with any identifier match the filter.
    type: list
    required: false
    elements: str
  names:
    aliases:
      - filter_names
    description:
      - Limit the results to virtual machines with these display names.
      - If omitted or empty, virtual machines with any name match the filter.
    type: list
    required: false
    elements: str
  folders:
    aliases:
      - filter_folders
    description:
      - Limit the results to virtual machines contained in these folders.
      - Each value must be the MOID of a C(Folder) resource.
      - If omitted or empty, virtual machines in any folder match the filter.
    type: list
    required: false
    elements: str
  datacenters:
    aliases:
      - filter_datacenters
    description:
      - Limit the results to virtual machines contained in these datacenters.
      - Each value must be the MOID of a C(Datacenter) resource.
      - If omitted or empty, virtual machines in any datacenter match the filter.
    type: list
    required: false
    elements: str
  hosts:
    description:
      - Limit the results to virtual machines running on these hosts.
      - Each value must be the MOID of a C(HostSystem) resource.
      - If omitted or empty, virtual machines on any host match the filter.
    type: list
    required: false
    elements: str
  clusters:
    description:
      - Limit the results to virtual machines contained in these clusters.
      - Each value must be the MOID of a C(ClusterComputeResource) resource.
      - If omitted or empty, virtual machines in any cluster match the filter.
    type: list
    required: false
    elements: str
  resource_pools:
    description:
      - Limit the results to virtual machines contained in these resource pools.
      - Each value must be the MOID of a C(ResourcePool) resource.
      - If omitted or empty, virtual machines in any resource pool match the filter.
    type: list
    required: false
    elements: str
  power_states:
    description:
      - Limit the results to virtual machines that are in one of these power states.
      - V(POWERED_OFF) - The virtual machine is powered off.
      - V(POWERED_ON) - The virtual machine is powered on.
      - V(SUSPENDED) - The virtual machine is suspended.
      - If omitted or empty, virtual machines in any power state match the filter.
    type: list
    required: false
    elements: str

version_added: 5.0.0

requirements: []

notes:
  - Generated from vSphere API spec 9.1.0.
"""

EXAMPLES = r"""
- name: List all virtual machines
  vmware.vmware_rest.vcenter_vm_info:
  register: all_vms

- name: Get full details about a specific virtual machine
  vmware.vmware_rest.vcenter_vm_info:
    vm: vm-1013
  register: my_vm

- name: Filter virtual machines by name
  vmware.vmware_rest.vcenter_vm_info:
    names:
      - my_test_vm
  register: filtered_vms

- name: Find powered-on virtual machines in specific clusters
  vmware.vmware_rest.vcenter_vm_info:
    clusters:
      - domain-c1007
    power_states:
      - POWERED_ON
  register: running_vms
"""

RETURN = r"""
id:
  description: MOID of the queried virtual machine.
  returned: When only one resource, with a MOID, was queried.
  sample: vm-1013
  type: str
value:
  description:
    - Raw output from the API response.
    - This output is maintained for consistency with version 4.x and earlier of this collection.
      It is recommended to switch to the info return key for a more consistent and documented output.
  returned: On success.
  sample:
    name: my_test_vm
    power_state: POWERED_ON
    guest_os: RHEL_9_64
    cpu:
      count: 2
      cores_per_socket: 1
      hot_add_enabled: false
      hot_remove_enabled: false
    memory:
      size_mib: 4096
      hot_add_enabled: false
    disks:
      "2000":
        label: Hard disk 1
        type: SCSI
        capacity: 17179869184
    nics:
      "4000":
        label: Network adapter 1
        type: VMXNET3
        mac_address: "00:50:56:aa:bb:cc"
        state: CONNECTED
  type: raw
info:
  description: A list of virtual machines matching the query.
  returned: On success.
  sample:
    - vm: vm-1013
      name: my_test_vm
      power_state: POWERED_ON
      cpu_count: 2
      memory_size_mib: 4096
  type: list
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
