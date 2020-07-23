from __future__ import absolute_import, division, print_function

__metaclass__ = type
import socket
import json

DOCUMENTATION = "author:\n- Ansible VMware team\ndescription: Handle resource of type vcenter_vm_hardware_disk\nextends_documentation_fragment: []\nmodule: vcenter_vm_hardware_disk\nnotes:\n- Tested on vSphere 7.0\noptions:\n  backing:\n    description:\n    - \"Physical resource backing for the virtual disk. \\n This field may only be modified\\\n      \\ if the virtual machine is not powered on.\\n\\nIf unset, the value is unchanged.\"\n    - 'Validate attributes are:'\n    - ' - C(type) (str): The Disk.BackingType enumerated type defines the valid backing\n      types for a virtual disk.'\n    - ' - C(vmdk_file) (str): Path of the VMDK file backing the virtual disk.\n\n      This field is optional and it is only relevant when the value of Disk.BackingSpec.type\n      is VMDK_FILE.'\n    type: dict\n  disk:\n    description:\n    - 'Virtual disk identifier.\n\n      The parameter must be an identifier for the resource type: vcenter.vm.hardware.Disk.\n      Required with I(state=[''update'', ''delete''])'\n    type: str\n  ide:\n    description:\n    - 'Address for attaching the device to a virtual IDE adapter.\n\n      If unset, the server will choose an available address; if none is available,\n      the request will fail.'\n    - 'Validate attributes are:'\n    - ' - C(master) (bool): Flag specifying whether the device should be the master\n      or slave device on the IDE adapter.\n\n      If unset, the server will choose an available connection type. If no IDE connections\n      are available, the request will be rejected.'\n    - ' - C(primary) (bool): Flag specifying whether the device should be attached\n      to the primary or secondary IDE adapter of the virtual machine.\n\n      If unset, the server will choose a adapter with an available connection. If\n      no IDE connections are available, the request will be rejected.'\n    type: dict\n  new_vmdk:\n    description:\n    - 'Specification for creating a new VMDK backing for the virtual disk. Exactly\n      one of Disk.CreateSpec.backing or Disk.CreateSpec.new-vmdk must be specified.\n\n      If unset, a new VMDK backing will not be created.'\n    - 'Validate attributes are:'\n    - ' - C(capacity) (int): Capacity of the virtual disk backing in bytes.\n\n      If unset, defaults to a guest-specific capacity.'\n    - ' - C(name) (str): Base name of the VMDK file. The name should not include the\n      ''.vmdk'' file extension.\n\n      If unset, a name (derived from the name of the virtual machine) will be chosen\n      by the server.'\n    - ' - C(storage_policy) (dict): The Disk.StoragePolicySpec structure contains\n      information about the storage policy that is to be associated the with VMDK\n      file.\n\n      If unset the default storage policy of the target datastore (if applicable)\n      is applied. Currently a default storage policy is only supported by object based\n      datastores : VVol & vSAN. For non- object datastores, if unset then no storage\n      policy would be associated with the VMDK file.'\n    type: dict\n  sata:\n    description:\n    - 'Address for attaching the device to a virtual SATA adapter.\n\n      If unset, the server will choose an available address; if none is available,\n      the request will fail.'\n    - 'Validate attributes are:'\n    - ' - C(bus) (int): Bus number of the adapter to which the device should be attached.'\n    - ' - C(unit) (int): Unit number of the device.\n\n      If unset, the server will choose an available unit number on the specified adapter.\n      If there are no available connections on the adapter, the request will be rejected.'\n    type: dict\n  scsi:\n    description:\n    - 'Address for attaching the device to a virtual SCSI adapter.\n\n      If unset, the server will choose an available address; if none is available,\n      the request will fail.'\n    - 'Validate attributes are:'\n    - ' - C(bus) (int): Bus number of the adapter to which the device should be attached.'\n    - ' - C(unit) (int): Unit number of the device.\n\n      If unset, the server will choose an available unit number on the specified adapter.\n      If there are no available connections on the adapter, the request will be rejected.'\n    type: dict\n  state:\n    choices:\n    - update\n    - delete\n    - create\n    description: []\n    type: str\n  type:\n    choices:\n    - IDE\n    - SCSI\n    - SATA\n    description:\n    - The Disk.HostBusAdapterType enumerated type defines the valid types of host\n      bus adapters that may be used for attaching a virtual storage device to a virtual\n      machine.\n    type: str\n  vm:\n    description:\n    - 'Virtual machine identifier.\n\n      The parameter must be an identifier for the resource type: VirtualMachine.'\n    type: str\nrequirements:\n- python >= 3.6\nshort_description: Handle resource of type vcenter_vm_hardware_disk\nversion_added: 1.0.0\n"
IN_QUERY_PARAMETER = []
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
    argument_spec["vm"] = {
        "type": "str",
        "operationIds": ["create", "delete", "update"],
    }
    argument_spec["type"] = {
        "type": "str",
        "choices": ["IDE", "SATA", "SCSI"],
        "operationIds": ["create"],
    }
    argument_spec["state"] = {"type": "str", "choices": ["create", "delete", "update"]}
    argument_spec["scsi"] = {"type": "dict", "operationIds": ["create"]}
    argument_spec["sata"] = {"type": "dict", "operationIds": ["create"]}
    argument_spec["new_vmdk"] = {"type": "dict", "operationIds": ["create"]}
    argument_spec["ide"] = {"type": "dict", "operationIds": ["create"]}
    argument_spec["disk"] = {"type": "str", "operationIds": ["delete", "update"]}
    argument_spec["backing"] = {"type": "dict", "operationIds": ["create", "update"]}
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
    return "https://{vcenter_hostname}/rest/vcenter/vm/{vm}/hardware/disk".format(
        **params
    )


async def entry_point(module, session):
    func = globals()[("_" + module.params["state"])]
    return await func(module.params, session)


async def _create(params, session):
    accepted_fields = ["backing", "ide", "new_vmdk", "sata", "scsi", "type"]
    if "create" == "create":
        _exists = await exists(params, session)
        if _exists:
            return await update_changed_flag({"value": _exists}, 200, "get")
    spec = {}
    for i in accepted_fields:
        if params[i]:
            spec[i] = params[i]
    _url = "https://{vcenter_hostname}/rest/vcenter/vm/{vm}/hardware/disk".format(
        **params
    )
    async with session.post(_url, json={"spec": spec}) as resp:
        try:
            if resp.headers["Content-Type"] == "application/json":
                _json = await resp.json()
        except KeyError:
            _json = {}
        if (
            ("create" == "create")
            and (resp.status in [200, 201])
            and ("value" in _json)
        ):
            if type(_json["value"]) == dict:
                _id = list(_json["value"].values())[0]
            else:
                _id = _json["value"]
            _json = {"value": (await get_device_info(params, session, _url, _id))}
        return await update_changed_flag(_json, resp.status, "create")


async def _delete(params, session):
    _url = "https://{vcenter_hostname}/rest/vcenter/vm/{vm}/hardware/disk/{disk}".format(
        **params
    ) + gen_args(
        params, IN_QUERY_PARAMETER
    )
    async with session.delete(_url) as resp:
        try:
            if resp.headers["Content-Type"] == "application/json":
                _json = await resp.json()
        except KeyError:
            _json = {}
        return await update_changed_flag(_json, resp.status, "delete")


async def _update(params, session):
    accepted_fields = ["backing"]
    if "update" == "create":
        _exists = await exists(params, session)
        if _exists:
            return await update_changed_flag({"value": _exists}, 200, "get")
    spec = {}
    for i in accepted_fields:
        if params[i]:
            spec[i] = params[i]
    _url = "https://{vcenter_hostname}/rest/vcenter/vm/{vm}/hardware/disk/{disk}".format(
        **params
    )
    async with session.patch(_url, json={"spec": spec}) as resp:
        try:
            if resp.headers["Content-Type"] == "application/json":
                _json = await resp.json()
        except KeyError:
            _json = {}
        if (
            ("update" == "create")
            and (resp.status in [200, 201])
            and ("value" in _json)
        ):
            if type(_json["value"]) == dict:
                _id = list(_json["value"].values())[0]
            else:
                _id = _json["value"]
            _json = {"value": (await get_device_info(params, session, _url, _id))}
        return await update_changed_flag(_json, resp.status, "update")


if __name__ == "__main__":
    import asyncio

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
