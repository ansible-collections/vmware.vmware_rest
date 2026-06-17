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
module: vcenter_vm_info
short_description: Get information about virtual machines.
description:
  - Returns information about virtual machines in vCenter.
  - When I(vm) is specified, returns detailed information for that virtual machine.
  - When I(vm) is omitted, lists virtual machines matching the optional filters and
    returns detailed information for each match.
author:
  - Ansible Eco Content Team (@eco-ansible-content)
extends_documentation_fragment:
  - vmware.vmware_rest.connection_params
options:
  vm:
    description:
      - Identifier of the virtual machine to retrieve.
      - Must be an identifier (MOID) for a C(VirtualMachine) resource.
      - When specified, only that virtual machine is returned.
    type: str
  vms:
    description:
      - Identifiers of virtual machines that can match the filter.
      - Each element must be an identifier (MOID) for a C(VirtualMachine) resource.
      - When omitted or empty, virtual machines with any identifier match the filter.
    type: list
    elements: str
  names:
    description:
      - Names that virtual machines must have to match the filter.
      - When omitted or empty, virtual machines with any name match the filter.
    type: list
    elements: str
  folders:
    description:
      - Folders that must contain the virtual machines for the virtual machine to
        match the filter.
      - Each element must be an identifier (MOID) for a C(Folder) resource.
      - When omitted or empty, virtual machines in any folder match the filter.
    type: list
    elements: str
  datacenters:
    description:
      - Datacenters that must contain the virtual machines for the virtual machine
        to match the filter.
      - Each element must be an identifier (MOID) for a C(Datacenter) resource.
      - When omitted or empty, virtual machines in any datacenter match the filter.
    type: list
    elements: str
  hosts:
    description:
      - Hosts that must contain the virtual machines for the virtual machine to match
        the filter.
      - Each element must be an identifier (MOID) for a C(Host) resource.
      - When omitted or empty, virtual machines on any host match the filter.
    type: list
    elements: str
  clusters:
    description:
      - Clusters that must contain the virtual machines for the virtual machine to
        match the filter.
      - Each element must be an identifier (MOID) for a C(Cluster) resource.
      - When omitted or empty, virtual machines in any cluster match the filter.
    type: list
    elements: str
  resource_pools:
    description:
      - Resource pools that must contain the virtual machines for the virtual machine
        to match the filter.
      - Each element must be an identifier (MOID) for a C(ResourcePool) resource.
      - When omitted or empty, virtual machines in any resource pool match the filter.
    type: list
    elements: str
  power_states:
    description:
      - Power states that virtual machines must be in to match the filter.
      - When omitted or empty, virtual machines in any power state match the filter.
    type: list
    elements: str
version_added: 4.11.0
requirements: []
notes:
  - Generated from vSphere API spec 9.1.0.
  - Has support for vSphere API 7.0.3.
  - Has support for vSphere API 8.0.2.
"""

EXAMPLES = r"""
- name: List all virtual machines
  vmware.vmware_rest.vcenter_vm_info:
  register: vms

- name: Get a virtual machine by MOID
  vmware.vmware_rest.vcenter_vm_info:
    vm: vm-1001
  register: vm_info

- name: List virtual machines matching a name filter
  vmware.vmware_rest.vcenter_vm_info:
    names:
      - my-vm
  register: filtered_vms
"""

RETURN = r"""
value:
  description:
    - Virtual machine information.
    - Returns a list of virtual machine dictionaries when I(vm) is omitted.
    - Returns a single virtual machine dictionary when I(vm) is specified.
  returned: On success
  type: raw
  sample:
    - name: my-vm
      guest_os: RHEL_9_64
      power_state: POWERED_OFF
      memory:
        size_mib: 4096
      cpu:
        count: 2
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.vmware.vmware_rest.plugins.module_utils._argument_spec import (
    connection_params_argument_spec,
)
from ansible_collections.vmware.vmware_rest.plugins.module_utils._errors import (
    UnexpectedAPIResponse,
)
from ansible_collections.vmware.vmware_rest.plugins.module_utils._module_base import (
    VmwareRestInfoModuleBase,
    normalize_list_response,
)

LIST_PATH = "/vcenter/vm"
VM_PATH = "/vcenter/vm/{vm}"


class VmwareRestInfoModule(VmwareRestInfoModuleBase):
    PAYLOAD_FORMAT = {
        "list": {
            "query": {
                "vms": "vms",
                "names": "names",
                "folders": "folders",
                "datacenters": "datacenters",
                "hosts": "hosts",
                "clusters": "clusters",
                "resource_pools": "resource_pools",
                "power_states": "power_states",
            },
            "body": {},
            "path": {},
        },
        "get": {
            "query": {},
            "body": {},
            "path": {"vm": "vm"},
        },
    }

    def _get_vm(self, vm_id, fail_if_missing=False):
        path = self.build_path(VM_PATH, {"vm": vm_id})
        response = self.client.get(path)
        if response.status == 404:
            if fail_if_missing:
                self.client.error_handler.handle_request_error(
                    exception=UnexpectedAPIResponse(
                        response.status, response.data
                    ),
                    method="GET",
                    path=path,
                    request_kwargs={},
                )
            return None

        info = response.json
        if isinstance(info, dict) and "vm" not in info:
            info["vm"] = vm_id
        return info

    def get_info(self):
        vm = self.params.get("vm")
        if vm:
            return self._get_vm(vm, fail_if_missing=True)

        query = self.build_query(self.PAYLOAD_FORMAT["list"])
        response = self.client.get(LIST_PATH, query=query or None)
        if response.status == 404:
            return []

        summaries = normalize_list_response(response.json)
        result = []
        for summary in summaries:
            vm_id = summary.get("vm")
            if not vm_id:
                continue
            info = self._get_vm(vm_id)
            if info is not None:
                result.append(info)
        return result


def main():
    module_args = connection_params_argument_spec()
    module_args["vm"] = {"type": "str"}
    module_args["vms"] = {"type": "list", "elements": "str"}
    module_args["names"] = {"type": "list", "elements": "str"}
    module_args["folders"] = {"type": "list", "elements": "str"}
    module_args["datacenters"] = {"type": "list", "elements": "str"}
    module_args["hosts"] = {"type": "list", "elements": "str"}
    module_args["clusters"] = {"type": "list", "elements": "str"}
    module_args["resource_pools"] = {"type": "list", "elements": "str"}
    module_args["power_states"] = {"type": "list", "elements": "str"}

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
    )

    info_module = VmwareRestInfoModule(module)
    result = info_module.get_info()
    module.exit_json(value=result)


if __name__ == "__main__":
    main()
