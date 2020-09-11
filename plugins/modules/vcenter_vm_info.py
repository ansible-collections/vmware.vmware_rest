#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = """
module: vcenter_vm_info
short_description: Handle resource of type vcenter_vm
description: Handle resource of type vcenter_vm
options:
  filter_clusters:
    description:
    - Clusters that must contain the virtual machine for the virtual machine to match
      the filter.
    - If unset or empty, virtual machines in any cluster match the filter.
    - 'When clients pass a value of this structure as a parameter, the field must
      contain identifiers for the resource type: ClusterComputeResource. When operations
      return a value of this structure as a result, the field will contain identifiers
      for the resource type: ClusterComputeResource.'
    elements: str
    type: list
  filter_datacenters:
    description:
    - Datacenters that must contain the virtual machine for the virtual machine to
      match the filter.
    - If unset or empty, virtual machines in any datacenter match the filter.
    - 'When clients pass a value of this structure as a parameter, the field must
      contain identifiers for the resource type: Datacenter. When operations return
      a value of this structure as a result, the field will contain identifiers for
      the resource type: Datacenter.'
    elements: str
    type: list
  filter_folders:
    description:
    - Folders that must contain the virtual machine for the virtual machine to match
      the filter.
    - If unset or empty, virtual machines in any folder match the filter.
    - 'When clients pass a value of this structure as a parameter, the field must
      contain identifiers for the resource type: Folder. When operations return a
      value of this structure as a result, the field will contain identifiers for
      the resource type: Folder.'
    elements: str
    type: list
  filter_hosts:
    description:
    - Hosts that must contain the virtual machine for the virtual machine to match
      the filter.
    - If unset or empty, virtual machines on any host match the filter.
    - 'When clients pass a value of this structure as a parameter, the field must
      contain identifiers for the resource type: HostSystem. When operations return
      a value of this structure as a result, the field will contain identifiers for
      the resource type: HostSystem.'
    elements: str
    type: list
  filter_names:
    description:
    - Names that virtual machines must have to match the filter (see VM.Info.name).
    - If unset or empty, virtual machines with any name match the filter.
    elements: str
    type: list
  filter_power_states:
    description:
    - Power states that a virtual machine must be in to match the filter (see Power.Info.state.
    - If unset or empty, virtual machines in any power state match the filter.
    elements: str
    type: list
  filter_resource_pools:
    description:
    - Resource pools that must contain the virtual machine for the virtual machine
      to match the filter.
    - If unset or empty, virtual machines in any resource pool match the filter.
    - 'When clients pass a value of this structure as a parameter, the field must
      contain identifiers for the resource type: ResourcePool. When operations return
      a value of this structure as a result, the field will contain identifiers for
      the resource type: ResourcePool.'
    elements: str
    type: list
  filter_vms:
    description:
    - Identifiers of virtual machines that can match the filter.
    - If unset or empty, virtual machines with any identifier match the filter.
    - 'When clients pass a value of this structure as a parameter, the field must
      contain identifiers for the resource type: VirtualMachine. When operations return
      a value of this structure as a result, the field will contain identifiers for
      the resource type: VirtualMachine.'
    elements: str
    type: list
  vcenter_hostname:
    description:
    - The hostname or IP address of the vSphere vCenter
    - If the value is not specified in the task, the value of environment variable
      C(VMWARE_HOST) will be used instead.
    required: true
    type: str
  vcenter_password:
    description:
    - The vSphere vCenter username
    - If the value is not specified in the task, the value of environment variable
      C(VMWARE_PASSWORD) will be used instead.
    required: true
    type: str
  vcenter_username:
    description:
    - The vSphere vCenter username
    - If the value is not specified in the task, the value of environment variable
      C(VMWARE_USER) will be used instead.
    required: true
    type: str
  vcenter_validate_certs:
    default: true
    description:
    - Allows connection when SSL certificates are not valid. Set to C(false) when
      certificates are not trusted.
    - If the value is not specified in the task, the value of environment variable
      C(VMWARE_VALIDATE_CERTS) will be used instead.
    type: bool
  vm:
    description:
    - Virtual machine identifier.
    - 'The parameter must be an identifier for the resource type: VirtualMachine.
      Required with I(state=[''get''])'
    type: str
author:
- Goneri Le Bouder (@goneri) <goneri@lebouder.net>
version_added: 1.0.0
requirements:
- python >= 3.6
- aiohttp
"""

EXAMPLES = """
- name: Look up the VM called test_vm1 in the inventory
  register: search_result
  vcenter_vm_info:
    filter_names:
    - test_vm1
- name: Collect information about a specific VM
  vcenter_vm_info:
    vm: '{{ search_result.value[0].vm }}'
  register: test_vm1_info
- name: Collect the list of the existing VM
  vcenter_vm_info:
  register: existing_vms
  until: existing_vms is not failed
- name: Look up the VM called test_vm1 in the inventory
  register: search_result
  vcenter_vm_info:
    filter_names:
    - test_vm1
- name: Search with an invalid filter
  vcenter_vm_info:
    filter_names: test_vm1_does_not_exists
"""

# This structure describes the format of the data expected by the end-points
PAYLOAD_FORMAT = {
    "list": {
        "query": {
            "filter.clusters": "filter.clusters",
            "filter.datacenters": "filter.datacenters",
            "filter.folders": "filter.folders",
            "filter.hosts": "filter.hosts",
            "filter.names": "filter.names",
            "filter.power_states": "filter.power_states",
            "filter.resource_pools": "filter.resource_pools",
            "filter.vms": "filter.vms",
        },
        "body": {},
        "path": {},
    },
    "create": {
        "query": {},
        "body": {
            "boot": {
                "delay": "spec/boot/delay",
                "efi_legacy_boot": "spec/boot/efi_legacy_boot",
                "enter_setup_mode": "spec/boot/enter_setup_mode",
                "network_protocol": "spec/boot/network_protocol",
                "retry": "spec/boot/retry",
                "retry_delay": "spec/boot/retry_delay",
                "type": "spec/boot/type",
            },
            "boot_devices": {"type": "spec/boot_devices/type"},
            "cdroms": {
                "allow_guest_control": "spec/cdroms/allow_guest_control",
                "backing": "spec/cdroms/backing",
                "ide": "spec/cdroms/ide",
                "sata": "spec/cdroms/sata",
                "start_connected": "spec/cdroms/start_connected",
                "type": "spec/cdroms/type",
            },
            "cpu": {
                "cores_per_socket": "spec/cpu/cores_per_socket",
                "count": "spec/cpu/count",
                "hot_add_enabled": "spec/cpu/hot_add_enabled",
                "hot_remove_enabled": "spec/cpu/hot_remove_enabled",
            },
            "disks": {
                "backing": "spec/disks/backing",
                "ide": "spec/disks/ide",
                "new_vmdk": "spec/disks/new_vmdk",
                "sata": "spec/disks/sata",
                "scsi": "spec/disks/scsi",
                "type": "spec/disks/type",
            },
            "floppies": {
                "allow_guest_control": "spec/floppies/allow_guest_control",
                "backing": "spec/floppies/backing",
                "start_connected": "spec/floppies/start_connected",
            },
            "guest_OS": "spec/guest_OS",
            "hardware_version": "spec/hardware_version",
            "memory": {
                "hot_add_enabled": "spec/memory/hot_add_enabled",
                "size_MiB": "spec/memory/size_MiB",
            },
            "name": "spec/name",
            "nics": {
                "allow_guest_control": "spec/nics/allow_guest_control",
                "backing": "spec/nics/backing",
                "mac_address": "spec/nics/mac_address",
                "mac_type": "spec/nics/mac_type",
                "pci_slot_number": "spec/nics/pci_slot_number",
                "start_connected": "spec/nics/start_connected",
                "type": "spec/nics/type",
                "upt_compatibility_enabled": "spec/nics/upt_compatibility_enabled",
                "wake_on_lan_enabled": "spec/nics/wake_on_lan_enabled",
            },
            "parallel_ports": {
                "allow_guest_control": "spec/parallel_ports/allow_guest_control",
                "backing": "spec/parallel_ports/backing",
                "start_connected": "spec/parallel_ports/start_connected",
            },
            "placement": {
                "cluster": "spec/placement/cluster",
                "datastore": "spec/placement/datastore",
                "folder": "spec/placement/folder",
                "host": "spec/placement/host",
                "resource_pool": "spec/placement/resource_pool",
            },
            "sata_adapters": {
                "bus": "spec/sata_adapters/bus",
                "pci_slot_number": "spec/sata_adapters/pci_slot_number",
                "type": "spec/sata_adapters/type",
            },
            "scsi_adapters": {
                "bus": "spec/scsi_adapters/bus",
                "pci_slot_number": "spec/scsi_adapters/pci_slot_number",
                "sharing": "spec/scsi_adapters/sharing",
                "type": "spec/scsi_adapters/type",
            },
            "serial_ports": {
                "allow_guest_control": "spec/serial_ports/allow_guest_control",
                "backing": "spec/serial_ports/backing",
                "start_connected": "spec/serial_ports/start_connected",
                "yield_on_poll": "spec/serial_ports/yield_on_poll",
            },
            "storage_policy": {"policy": "spec/storage_policy/policy"},
        },
        "path": {},
    },
    "delete": {"query": {}, "body": {}, "path": {"vm": "vm"}},
    "get": {"query": {}, "body": {}, "path": {"vm": "vm"}},
    "relocate": {
        "query": {},
        "body": {
            "disks": {"key": "spec/disks/key", "value": "spec/disks/value"},
            "placement": {
                "cluster": "spec/placement/cluster",
                "datastore": "spec/placement/datastore",
                "folder": "spec/placement/folder",
                "host": "spec/placement/host",
                "resource_pool": "spec/placement/resource_pool",
            },
        },
        "path": {"vm": "vm"},
    },
    "unregister": {"query": {}, "body": {}, "path": {"vm": "vm"}},
    "clone": {
        "query": {},
        "body": {
            "disks_to_remove": "spec/disks_to_remove",
            "disks_to_update": {
                "key": "spec/disks_to_update/key",
                "value": "spec/disks_to_update/value",
            },
            "guest_customization_spec": {"name": "spec/guest_customization_spec/name"},
            "name": "spec/name",
            "placement": {
                "cluster": "spec/placement/cluster",
                "datastore": "spec/placement/datastore",
                "folder": "spec/placement/folder",
                "host": "spec/placement/host",
                "resource_pool": "spec/placement/resource_pool",
            },
            "power_on": "spec/power_on",
            "source": "spec/source",
        },
        "path": {},
    },
    "instant_clone": {
        "query": {},
        "body": {
            "bios_uuid": "spec/bios_uuid",
            "disconnect_all_nics": "spec/disconnect_all_nics",
            "name": "spec/name",
            "nics_to_update": {
                "key": "spec/nics_to_update/key",
                "value": "spec/nics_to_update/value",
            },
            "parallel_ports_to_update": {
                "key": "spec/parallel_ports_to_update/key",
                "value": "spec/parallel_ports_to_update/value",
            },
            "placement": {
                "datastore": "spec/placement/datastore",
                "folder": "spec/placement/folder",
                "resource_pool": "spec/placement/resource_pool",
            },
            "serial_ports_to_update": {
                "key": "spec/serial_ports_to_update/key",
                "value": "spec/serial_ports_to_update/value",
            },
            "source": "spec/source",
        },
        "path": {},
    },
    "register": {
        "query": {},
        "body": {
            "datastore": "spec/datastore",
            "datastore_path": "spec/datastore_path",
            "name": "spec/name",
            "path": "spec/path",
            "placement": {
                "cluster": "spec/placement/cluster",
                "folder": "spec/placement/folder",
                "host": "spec/placement/host",
                "resource_pool": "spec/placement/resource_pool",
            },
        },
        "path": {},
    },
}

import socket
import json
from ansible.module_utils.basic import env_fallback

try:
    from ansible_collections.cloud.common.plugins.module_utils.turbo.module import (
        AnsibleTurboModule as AnsibleModule,
    )
except ImportError:
    from ansible.module_utils.basic import AnsibleModule
from ansible_collections.vmware.vmware_rest.plugins.module_utils.vmware_rest import (
    exists,
    gen_args,
    get_device_info,
    get_subdevice_type,
    list_devices,
    open_session,
    prepare_payload,
    update_changed_flag,
)


def prepare_argument_spec():
    argument_spec = {
        "vcenter_hostname": dict(
            type="str", required=True, fallback=(env_fallback, ["VMWARE_HOST"]),
        ),
        "vcenter_username": dict(
            type="str", required=True, fallback=(env_fallback, ["VMWARE_USER"]),
        ),
        "vcenter_password": dict(
            type="str",
            required=True,
            no_log=True,
            fallback=(env_fallback, ["VMWARE_PASSWORD"]),
        ),
        "vcenter_validate_certs": dict(
            type="bool",
            required=False,
            default=True,
            fallback=(env_fallback, ["VMWARE_VALIDATE_CERTS"]),
        ),
    }

    argument_spec["filter_clusters"] = {"type": "list", "elements": "str"}
    argument_spec["filter_datacenters"] = {"type": "list", "elements": "str"}
    argument_spec["filter_folders"] = {"type": "list", "elements": "str"}
    argument_spec["filter_hosts"] = {"type": "list", "elements": "str"}
    argument_spec["filter_names"] = {"type": "list", "elements": "str"}
    argument_spec["filter_power_states"] = {"type": "list", "elements": "str"}
    argument_spec["filter_resource_pools"] = {"type": "list", "elements": "str"}
    argument_spec["filter_vms"] = {"type": "list", "elements": "str"}
    argument_spec["vm"] = {"type": "str"}

    return argument_spec


async def main():
    module_args = prepare_argument_spec()
    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)
    session = await open_session(
        vcenter_hostname=module.params["vcenter_hostname"],
        vcenter_username=module.params["vcenter_username"],
        vcenter_password=module.params["vcenter_password"],
    )
    result = await entry_point(module, session)
    module.exit_json(**result)


def build_url(params):

    if params["vm"]:
        _in_query_parameters = PAYLOAD_FORMAT["get"]["query"].keys()
        return ("https://{vcenter_hostname}" "/rest/vcenter/vm/{vm}").format(
            **params
        ) + gen_args(params, _in_query_parameters)
    else:
        _in_query_parameters = PAYLOAD_FORMAT["list"]["query"].keys()
        return ("https://{vcenter_hostname}" "/rest/vcenter/vm").format(
            **params
        ) + gen_args(params, _in_query_parameters)


async def entry_point(module, session):
    async with session.get(build_url(module.params)) as resp:
        _json = await resp.json()
        if module.params.get("vm"):
            _json["id"] = module.params.get("vm")
        return await update_changed_flag(_json, resp.status, "get")


if __name__ == "__main__":
    import asyncio

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
