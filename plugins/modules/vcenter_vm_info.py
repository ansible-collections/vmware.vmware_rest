#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = """
module: vcenter_vm_info
short_description: Collect the  information from a VM
description: Collect the  information from a VM
options:
  filter_clusters:
    description:
    - Clusters that must contain the virtual machine for the virtual machine to match
      the filter.
    - If unset or empty, virtual machines in any cluster match the filter.
    - 'When clients pass a value of this structure as a parameter, the field must
      contain the id of resources returned by M(vcenter_cluster_info). '
    elements: str
    type: list
  filter_datacenters:
    description:
    - Datacenters that must contain the virtual machine for the virtual machine to
      match the filter.
    - If unset or empty, virtual machines in any datacenter match the filter.
    - 'When clients pass a value of this structure as a parameter, the field must
      contain the id of resources returned by M(vcenter_datacenter_info). '
    elements: str
    type: list
  filter_folders:
    description:
    - Folders that must contain the virtual machine for the virtual machine to match
      the filter.
    - If unset or empty, virtual machines in any folder match the filter.
    - 'When clients pass a value of this structure as a parameter, the field must
      contain the id of resources returned by M(vcenter_folder_info). '
    elements: str
    type: list
  filter_hosts:
    description:
    - Hosts that must contain the virtual machine for the virtual machine to match
      the filter.
    - If unset or empty, virtual machines on any host match the filter.
    - 'When clients pass a value of this structure as a parameter, the field must
      contain the id of resources returned by M(vcenter_host_info). '
    elements: str
    type: list
  filter_names:
    description:
    - Names that virtual machines must have to match the filter (see I(name)).
    - If unset or empty, virtual machines with any name match the filter.
    elements: str
    type: list
  filter_power_states:
    description:
    - Power states that a virtual machine must be in to match the filter (see I()
    - If unset or empty, virtual machines in any power state match the filter.
    elements: str
    type: list
  filter_resource_pools:
    description:
    - Resource pools that must contain the virtual machine for the virtual machine
      to match the filter.
    - If unset or empty, virtual machines in any resource pool match the filter.
    - 'When clients pass a value of this structure as a parameter, the field must
      contain the id of resources returned by M(vcenter_resourcepool_info). '
    elements: str
    type: list
  filter_vms:
    description:
    - Identifiers of virtual machines that can match the filter.
    - If unset or empty, virtual machines with any identifier match the filter.
    - 'When clients pass a value of this structure as a parameter, the field must
      contain the id of resources returned by M(vcenter_vm_info). '
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
  vcenter_rest_log_file:
    description:
    - 'You can use this optional parameter to set the location of a log file. '
    - 'This file will be used to record the HTTP REST interaction. '
    - 'The file will be stored on the host that run the module. '
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
    - The parameter must be the id of a resource returned by M(vcenter_vm_info).
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

RETURN = """
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
            "boot": "spec/boot",
            "boot_devices": "spec/boot_devices",
            "cdroms": "spec/cdroms",
            "cpu": "spec/cpu",
            "disks": "spec/disks",
            "floppies": "spec/floppies",
            "guest_OS": "spec/guest_OS",
            "hardware_version": "spec/hardware_version",
            "memory": "spec/memory",
            "name": "spec/name",
            "nics": "spec/nics",
            "parallel_ports": "spec/parallel_ports",
            "placement": "spec/placement",
            "sata_adapters": "spec/sata_adapters",
            "scsi_adapters": "spec/scsi_adapters",
            "serial_ports": "spec/serial_ports",
            "storage_policy": "spec/storage_policy",
        },
        "path": {},
    },
    "delete": {"query": {}, "body": {}, "path": {"vm": "vm"}},
    "get": {"query": {}, "body": {}, "path": {"vm": "vm"}},
    "relocate": {
        "query": {},
        "body": {"disks": "spec/disks", "placement": "spec/placement"},
        "path": {"vm": "vm"},
    },
    "unregister": {"query": {}, "body": {}, "path": {"vm": "vm"}},
    "clone": {
        "query": {},
        "body": {
            "disks_to_remove": "spec/disks_to_remove",
            "disks_to_update": "spec/disks_to_update",
            "guest_customization_spec": "spec/guest_customization_spec",
            "name": "spec/name",
            "placement": "spec/placement",
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
            "nics_to_update": "spec/nics_to_update",
            "parallel_ports_to_update": "spec/parallel_ports_to_update",
            "placement": "spec/placement",
            "serial_ports_to_update": "spec/serial_ports_to_update",
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
            "placement": "spec/placement",
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
    build_full_device_list,
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
        "vcenter_rest_log_file": dict(
            type="str",
            required=False,
            fallback=(env_fallback, ["VMWARE_REST_LOG_FILE"]),
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
    if not module.params["vcenter_hostname"]:
        module.fail_json("vcenter_hostname cannot be empty")
    if not module.params["vcenter_username"]:
        module.fail_json("vcenter_username cannot be empty")
    if not module.params["vcenter_password"]:
        module.fail_json("vcenter_password cannot be empty")
    session = await open_session(
        vcenter_hostname=module.params["vcenter_hostname"],
        vcenter_username=module.params["vcenter_username"],
        vcenter_password=module.params["vcenter_password"],
        log_file=module.params["vcenter_rest_log_file"],
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
    url = build_url(module.params)
    async with session.get(url) as resp:
        _json = await resp.json()
        if module.params.get("vm"):
            _json["id"] = module.params.get("vm")
        elif module.params.get("label"):  # TODO extend the list of filter
            _json = await exists(module.params, session, url)
        else:  # list context, retrieve the details of each entry
            try:
                if (
                    isinstance(_json["value"][0]["vm"], str)
                    and len(list(_json["value"][0].values())) == 1
                ):
                    # this is a list of id, we fetch the details
                    full_device_list = await build_full_device_list(session, url, _json)
                    _json = {"value": [i["value"] for i in full_device_list]}
            except (TypeError, KeyError, IndexError):
                pass

        return await update_changed_flag(_json, resp.status, "get")


if __name__ == "__main__":
    import asyncio

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
