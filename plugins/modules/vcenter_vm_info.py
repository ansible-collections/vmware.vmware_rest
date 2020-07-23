from __future__ import absolute_import, division, print_function

__metaclass__ = type
import socket
import json

DOCUMENTATION = "author:\n- Ansible VMware team\ndescription: Handle resource of type vcenter_vm\nextends_documentation_fragment: []\nmodule: vcenter_vm_info\nnotes:\n- Tested on vSphere 7.0\noptions:\n  filter.clusters:\n    description:\n    - 'Clusters that must contain the virtual machine for the virtual machine to match\n      the filter.\n\n      If unset or empty, virtual machines in any cluster match the filter.\n\n      When clients pass a value of this structure as a parameter, the field must contain\n      identifiers for the resource type: ClusterComputeResource. When operations return\n      a value of this structure as a result, the field will contain identifiers for\n      the resource type: ClusterComputeResource.'\n    type: list\n  filter.datacenters:\n    description:\n    - 'Datacenters that must contain the virtual machine for the virtual machine to\n      match the filter.\n\n      If unset or empty, virtual machines in any datacenter match the filter.\n\n      When clients pass a value of this structure as a parameter, the field must contain\n      identifiers for the resource type: Datacenter. When operations return a value\n      of this structure as a result, the field will contain identifiers for the resource\n      type: Datacenter.'\n    type: list\n  filter.folders:\n    description:\n    - 'Folders that must contain the virtual machine for the virtual machine to match\n      the filter.\n\n      If unset or empty, virtual machines in any folder match the filter.\n\n      When clients pass a value of this structure as a parameter, the field must contain\n      identifiers for the resource type: Folder. When operations return a value of\n      this structure as a result, the field will contain identifiers for the resource\n      type: Folder.'\n    type: list\n  filter.hosts:\n    description:\n    - 'Hosts that must contain the virtual machine for the virtual machine to match\n      the filter.\n\n      If unset or empty, virtual machines on any host match the filter.\n\n      When clients pass a value of this structure as a parameter, the field must contain\n      identifiers for the resource type: HostSystem. When operations return a value\n      of this structure as a result, the field will contain identifiers for the resource\n      type: HostSystem.'\n    type: list\n  filter.names:\n    description:\n    - 'Names that virtual machines must have to match the filter (see VM.Info.name).\n\n      If unset or empty, virtual machines with any name match the filter.'\n    type: list\n  filter.power_states:\n    description:\n    - 'Power states that a virtual machine must be in to match the filter (see Power.Info.state.\n\n      If unset or empty, virtual machines in any power state match the filter.'\n    type: list\n  filter.resource_pools:\n    description:\n    - 'Resource pools that must contain the virtual machine for the virtual machine\n      to match the filter.\n\n      If unset or empty, virtual machines in any resource pool match the filter.\n\n      When clients pass a value of this structure as a parameter, the field must contain\n      identifiers for the resource type: ResourcePool. When operations return a value\n      of this structure as a result, the field will contain identifiers for the resource\n      type: ResourcePool.'\n    type: list\n  filter.vms:\n    description:\n    - 'Identifiers of virtual machines that can match the filter.\n\n      If unset or empty, virtual machines with any identifier match the filter.\n\n      When clients pass a value of this structure as a parameter, the field must contain\n      identifiers for the resource type: VirtualMachine. When operations return a\n      value of this structure as a result, the field will contain identifiers for\n      the resource type: VirtualMachine.'\n    type: list\n  vm:\n    description:\n    - 'Virtual machine identifier.\n\n      The parameter must be an identifier for the resource type: VirtualMachine. Required\n      with I(state=[''get''])'\n    type: str\nrequirements:\n- python >= 3.6\nshort_description: Handle resource of type vcenter_vm\nversion_added: 1.0.0\n"
IN_QUERY_PARAMETER = [
    "filter.vms",
    "filter.names",
    "filter.folders",
    "filter.datacenters",
    "filter.hosts",
    "filter.clusters",
    "filter.resource_pools",
    "filter.power_states",
]
from ansible.module_utils.basic import env_fallback

try:
    from ansible_module.turbo.module import AnsibleTurboModule as AnsibleModule
except ImportError:
    from ansible.module_utils.basic import AnsibleModule
from ansible_collections.vmware.vmware_rest.plugins.module_utils.vmware_rest import (
    gen_args,
    open_session,
    update_changed_flag,
)


def prepare_argument_spec():
    argument_spec = {
        "vcenter_hostname": dict(
            type="str", required=False, fallback=(env_fallback, ["VMWARE_HOST"])
        ),
        "vcenter_username": dict(
            type="str", required=False, fallback=(env_fallback, ["VMWARE_USER"])
        ),
        "vcenter_password": dict(
            type="str",
            required=False,
            no_log=True,
            fallback=(env_fallback, ["VMWARE_PASSWORD"]),
        ),
        "vcenter_certs": dict(
            type="bool",
            required=False,
            no_log=True,
            fallback=(env_fallback, ["VMWARE_VALIDATE_CERTS"]),
        ),
    }
    argument_spec["vm"] = {"type": "str", "operationIds": ["get"]}
    argument_spec["filter.vms"] = {"type": "list", "operationIds": ["list"]}
    argument_spec["filter.resource_pools"] = {"type": "list", "operationIds": ["list"]}
    argument_spec["filter.power_states"] = {"type": "list", "operationIds": ["list"]}
    argument_spec["filter.names"] = {"type": "list", "operationIds": ["list"]}
    argument_spec["filter.hosts"] = {"type": "list", "operationIds": ["list"]}
    argument_spec["filter.folders"] = {"type": "list", "operationIds": ["list"]}
    argument_spec["filter.datacenters"] = {"type": "list", "operationIds": ["list"]}
    argument_spec["filter.clusters"] = {"type": "list", "operationIds": ["list"]}
    return argument_spec


async def get_device_info(params, session, _url, _key):
    async with session.get(((_url + "/") + _key)) as resp:
        _json = await resp.json()
        entry = _json["value"]
        entry["_key"] = _key
        return entry


async def list_devices(params, session):
    existing_entries = []
    _url = url(params)
    async with session.get(_url) as resp:
        _json = await resp.json()
        devices = _json["value"]
    for device in devices:
        _id = list(device.values())[0]
        existing_entries.append((await get_device_info(params, session, _url, _id)))
    return existing_entries


async def exists(params, session):
    unicity_keys = ["bus", "pci_slot_number"]
    devices = await list_devices(params, session)
    for device in devices:
        for k in unicity_keys:
            if (params.get(k) is not None) and (device.get(k) != params.get(k)):
                break
        else:
            return device


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


def url(params):
    if params["vm"]:
        return "https://{vcenter_hostname}/rest/vcenter/vm/{vm}".format(
            **params
        ) + gen_args(params, IN_QUERY_PARAMETER)
    else:
        return "https://{vcenter_hostname}/rest/vcenter/vm".format(**params) + gen_args(
            params, IN_QUERY_PARAMETER
        )


async def entry_point(module, session):
    async with session.get(url(module.params)) as resp:
        _json = await resp.json()
        return await update_changed_flag(_json, resp.status, "get")


if __name__ == "__main__":
    import asyncio

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
