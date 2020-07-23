from __future__ import absolute_import, division, print_function

__metaclass__ = type
import socket
import json

DOCUMENTATION = "author:\n- Ansible VMware team\ndescription: Handle resource of type vcenter_vm_hardware_cdrom\nextends_documentation_fragment: []\nmodule: vcenter_vm_hardware_cdrom\nnotes:\n- Tested on vSphere 7.0\noptions:\n  allow_guest_control:\n    description:\n    - 'Flag indicating whether the guest can connect and disconnect the device.\n\n      Defaults to false if unset.'\n    type: bool\n  backing:\n    description:\n    - 'Physical resource backing for the virtual CD-ROM device.\n\n      If unset, defaults to automatic detection of a suitable host device.'\n    - 'Validate attributes are:'\n    - ' - C(device_access_type) (str): The Cdrom.DeviceAccessType enumerated type\n      defines the valid device access types for a physical device packing of a virtual\n      CD-ROM device.'\n    - ' - C(host_device) (str): Name of the device that should be used as the virtual\n      CD-ROM device backing.\n\n      If unset, the virtual CD-ROM device will be configured to automatically detect\n      a suitable host device.'\n    - ' - C(iso_file) (str): Path of the image file that should be used as the virtual\n      CD-ROM device backing.\n\n      This field is optional and it is only relevant when the value of Cdrom.BackingSpec.type\n      is ISO_FILE.'\n    - ' - C(type) (str): The Cdrom.BackingType enumerated type defines the valid backing\n      types for a virtual CD-ROM device.'\n    type: dict\n  cdrom:\n    description:\n    - 'Virtual CD-ROM device identifier.\n\n      The parameter must be an identifier for the resource type: vcenter.vm.hardware.Cdrom.\n      Required with I(state=[''update'', ''delete''])'\n    type: str\n  ide:\n    description:\n    - 'Address for attaching the device to a virtual IDE adapter.\n\n      If unset, the server will choose an available address; if none is available,\n      the request will fail.'\n    - 'Validate attributes are:'\n    - ' - C(master) (bool): Flag specifying whether the device should be the master\n      or slave device on the IDE adapter.\n\n      If unset, the server will choose an available connection type. If no IDE connections\n      are available, the request will be rejected.'\n    - ' - C(primary) (bool): Flag specifying whether the device should be attached\n      to the primary or secondary IDE adapter of the virtual machine.\n\n      If unset, the server will choose a adapter with an available connection. If\n      no IDE connections are available, the request will be rejected.'\n    type: dict\n  sata:\n    description:\n    - 'Address for attaching the device to a virtual SATA adapter.\n\n      If unset, the server will choose an available address; if none is available,\n      the request will fail.'\n    - 'Validate attributes are:'\n    - ' - C(bus) (int): Bus number of the adapter to which the device should be attached.'\n    - ' - C(unit) (int): Unit number of the device.\n\n      If unset, the server will choose an available unit number on the specified adapter.\n      If there are no available connections on the adapter, the request will be rejected.'\n    type: dict\n  start_connected:\n    description:\n    - 'Flag indicating whether the virtual device should be connected whenever the\n      virtual machine is powered on.\n\n      Defaults to false if unset.'\n    type: bool\n  state:\n    choices:\n    - create\n    - update\n    - delete\n    description: []\n    type: str\n  type:\n    choices:\n    - IDE\n    - SATA\n    description:\n    - The Cdrom.HostBusAdapterType enumerated type defines the valid types of host\n      bus adapters that may be used for attaching a Cdrom to a virtual machine.\n    type: str\n  vm:\n    description:\n    - 'Virtual machine identifier.\n\n      The parameter must be an identifier for the resource type: VirtualMachine.'\n    type: str\nrequirements:\n- python >= 3.6\nshort_description: Handle resource of type vcenter_vm_hardware_cdrom\nversion_added: 1.0.0\n"
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
        "choices": ["IDE", "SATA"],
        "operationIds": ["create"],
    }
    argument_spec["state"] = {"type": "str", "choices": ["create", "delete", "update"]}
    argument_spec["start_connected"] = {
        "type": "bool",
        "operationIds": ["create", "update"],
    }
    argument_spec["sata"] = {"type": "dict", "operationIds": ["create"]}
    argument_spec["ide"] = {"type": "dict", "operationIds": ["create"]}
    argument_spec["cdrom"] = {"type": "str", "operationIds": ["delete", "update"]}
    argument_spec["backing"] = {"type": "dict", "operationIds": ["create", "update"]}
    argument_spec["allow_guest_control"] = {
        "type": "bool",
        "operationIds": ["create", "update"],
    }
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
    return "https://{vcenter_hostname}/rest/vcenter/vm/{vm}/hardware/cdrom".format(
        **params
    )


async def entry_point(module, session):
    func = globals()[("_" + module.params["state"])]
    return await func(module.params, session)


async def _create(params, session):
    accepted_fields = [
        "allow_guest_control",
        "backing",
        "ide",
        "sata",
        "start_connected",
        "type",
    ]
    if "create" == "create":
        _exists = await exists(params, session)
        if _exists:
            return await update_changed_flag({"value": _exists}, 200, "get")
    spec = {}
    for i in accepted_fields:
        if params[i]:
            spec[i] = params[i]
    _url = "https://{vcenter_hostname}/rest/vcenter/vm/{vm}/hardware/cdrom".format(
        **params
    )
    async with session.post(_url, json={"spec": spec}) as resp:
        try:
            if resp.headers["Content-Type"] == "application/json":
                _json = await resp.json()
        except KeyError:
            _json = {}
        if ("create" == "create") and ("value" in _json):
            if type(_json["value"]) == dict:
                _id = list(_json["value"].values())[0]
            else:
                _id = _json["value"]
            _json = {"value": (await get_device_info(params, session, _url, _id))}
        return await update_changed_flag(_json, resp.status, "create")


async def _delete(params, session):
    _url = "https://{vcenter_hostname}/rest/vcenter/vm/{vm}/hardware/cdrom/{cdrom}".format(
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
    accepted_fields = ["allow_guest_control", "backing", "start_connected"]
    if "update" == "create":
        _exists = await exists(params, session)
        if _exists:
            return await update_changed_flag({"value": _exists}, 200, "get")
    spec = {}
    for i in accepted_fields:
        if params[i]:
            spec[i] = params[i]
    _url = "https://{vcenter_hostname}/rest/vcenter/vm/{vm}/hardware/cdrom/{cdrom}".format(
        **params
    )
    async with session.patch(_url, json={"spec": spec}) as resp:
        try:
            if resp.headers["Content-Type"] == "application/json":
                _json = await resp.json()
        except KeyError:
            _json = {}
        if ("update" == "create") and ("value" in _json):
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
