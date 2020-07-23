from __future__ import absolute_import, division, print_function

__metaclass__ = type
import socket
import json

DOCUMENTATION = "author:\n- Ansible VMware team\ndescription: Handle resource of type vcenter_vm_hardware_ethernet\nextends_documentation_fragment: []\nmodule: vcenter_vm_hardware_ethernet\nnotes:\n- Tested on vSphere 7.0\noptions:\n  allow_guest_control:\n    description:\n    - 'Flag indicating whether the guest can connect and disconnect the device.\n\n      If unset, the value is unchanged.'\n    type: bool\n  backing:\n    description:\n    - \"Physical resource backing for the virtual Ethernet adapter. \\n This field may\\\n      \\ be modified at any time, and changes will be applied the next time the virtual\\\n      \\ machine is powered on.\\n\\nIf unset, the value is unchanged.\"\n    - 'Validate attributes are:'\n    - ' - C(distributed_port) (str): Key of the distributed virtual port that backs\n      the virtual Ethernet adapter. Depending on the type of the Portgroup, the port\n      may be specified using this field. If the portgroup type is early-binding (also\n      known as static), a port is assigned when the Ethernet adapter is configured\n      to use the port. The port may be either automatically or specifically assigned\n      based on the value of this field. If the portgroup type is ephemeral, the port\n      is created and assigned to a virtual machine when it is powered on and the Ethernet\n      adapter is connected. This field cannot be specified as no free ports exist\n      before use.\n\n      May be used to specify a port when the network specified on the Ethernet.BackingSpec.network\n      field is a static or early binding distributed portgroup. If unset, the port\n      will be automatically assigned to the Ethernet adapter based on the policy embodied\n      by the portgroup type.'\n    - ' - C(network) (str): Identifier of the network that backs the virtual Ethernet\n      adapter.\n\n      This field is optional and it is only relevant when the value of Ethernet.BackingSpec.type\n      is one of STANDARD_PORTGROUP, DISTRIBUTED_PORTGROUP, or OPAQUE_NETWORK.\n\n      When clients pass a value of this structure as a parameter, the field must be\n      an identifier for the resource type: Network. When operations return a value\n      of this structure as a result, the field will be an identifier for the resource\n      type: Network.'\n    - ' - C(type) (str): The Ethernet.BackingType enumerated type defines the valid\n      backing types for a virtual Ethernet adapter.'\n    type: dict\n  mac_address:\n    description:\n    - \"MAC address. \\n This field may be modified at any time, and changes will be\\\n      \\ applied the next time the virtual machine is powered on.\\n\\nIf unset, the\\\n      \\ value is unchanged. Must be specified if Ethernet.UpdateSpec.mac-type is MANUAL.\\\n      \\ Must be unset if the MAC address type is not MANUAL.\"\n    type: str\n  mac_type:\n    choices:\n    - MANUAL\n    - GENERATED\n    - ASSIGNED\n    description:\n    - The Ethernet.MacAddressType enumerated type defines the valid MAC address origins\n      for a virtual Ethernet adapter.\n    type: str\n  nic:\n    description:\n    - 'Virtual Ethernet adapter identifier.\n\n      The parameter must be an identifier for the resource type: vcenter.vm.hardware.Ethernet.\n      Required with I(state=[''update'', ''delete''])'\n    type: str\n  pci_slot_number:\n    description:\n    - 'Address of the virtual Ethernet adapter on the PCI bus. If the PCI address\n      is invalid, the server will change when it the VM is started or as the device\n      is hot added.\n\n      If unset, the server will choose an available address when the virtual machine\n      is powered on.'\n    type: int\n  start_connected:\n    description:\n    - 'Flag indicating whether the virtual device should be connected whenever the\n      virtual machine is powered on.\n\n      If unset, the value is unchanged.'\n    type: bool\n  state:\n    choices:\n    - update\n    - delete\n    - create\n    description: []\n    type: str\n  type:\n    choices:\n    - E1000\n    - E1000E\n    - PCNET32\n    - VMXNET\n    - VMXNET2\n    - VMXNET3\n    description:\n    - The Ethernet.EmulationType enumerated type defines the valid emulation types\n      for a virtual Ethernet adapter.\n    type: str\n  upt_compatibility_enabled:\n    description:\n    - \"Flag indicating whether Universal Pass-Through (UPT) compatibility should be\\\n      \\ enabled on this virtual Ethernet adapter. \\n This field may be modified at\\\n      \\ any time, and changes will be applied the next time the virtual machine is\\\n      \\ powered on.\\n\\nIf unset, the value is unchanged. Must be unset if the emulation\\\n      \\ type of the virtual Ethernet adapter is not VMXNET3.\"\n    type: bool\n  vm:\n    description:\n    - 'Virtual machine identifier.\n\n      The parameter must be an identifier for the resource type: VirtualMachine.'\n    type: str\n  wake_on_lan_enabled:\n    description:\n    - \"Flag indicating whether wake-on-LAN shoud be enabled on this virtual Ethernet\\\n      \\ adapter. \\n This field may be modified at any time, and changes will be applied\\\n      \\ the next time the virtual machine is powered on.\\n\\nIf unset, the value is\\\n      \\ unchanged.\"\n    type: bool\nrequirements:\n- python >= 3.6\nshort_description: Handle resource of type vcenter_vm_hardware_ethernet\nversion_added: 1.0.0\n"
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
    argument_spec["wake_on_lan_enabled"] = {
        "type": "bool",
        "operationIds": ["create", "update"],
    }
    argument_spec["vm"] = {
        "type": "str",
        "operationIds": ["create", "delete", "update"],
    }
    argument_spec["upt_compatibility_enabled"] = {
        "type": "bool",
        "operationIds": ["create", "update"],
    }
    argument_spec["type"] = {
        "type": "str",
        "choices": ["E1000", "E1000E", "PCNET32", "VMXNET", "VMXNET2", "VMXNET3"],
        "operationIds": ["create"],
    }
    argument_spec["state"] = {"type": "str", "choices": ["create", "delete", "update"]}
    argument_spec["start_connected"] = {
        "type": "bool",
        "operationIds": ["create", "update"],
    }
    argument_spec["pci_slot_number"] = {"type": "int", "operationIds": ["create"]}
    argument_spec["nic"] = {"type": "str", "operationIds": ["delete", "update"]}
    argument_spec["mac_type"] = {
        "type": "str",
        "choices": ["ASSIGNED", "GENERATED", "MANUAL"],
        "operationIds": ["create", "update"],
    }
    argument_spec["mac_address"] = {"type": "str", "operationIds": ["create", "update"]}
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
    return "https://{vcenter_hostname}/rest/vcenter/vm/{vm}/hardware/ethernet".format(
        **params
    )


async def entry_point(module, session):
    func = globals()[("_" + module.params["state"])]
    return await func(module.params, session)


async def _create(params, session):
    accepted_fields = [
        "allow_guest_control",
        "backing",
        "mac_address",
        "mac_type",
        "pci_slot_number",
        "start_connected",
        "type",
        "upt_compatibility_enabled",
        "wake_on_lan_enabled",
    ]
    if "create" == "create":
        _exists = await exists(params, session)
        if _exists:
            return await update_changed_flag({"value": _exists}, 200, "get")
    spec = {}
    for i in accepted_fields:
        if params[i]:
            spec[i] = params[i]
    _url = "https://{vcenter_hostname}/rest/vcenter/vm/{vm}/hardware/ethernet".format(
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
    _url = "https://{vcenter_hostname}/rest/vcenter/vm/{vm}/hardware/ethernet/{nic}".format(
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
    accepted_fields = [
        "allow_guest_control",
        "backing",
        "mac_address",
        "mac_type",
        "start_connected",
        "upt_compatibility_enabled",
        "wake_on_lan_enabled",
    ]
    if "update" == "create":
        _exists = await exists(params, session)
        if _exists:
            return await update_changed_flag({"value": _exists}, 200, "get")
    spec = {}
    for i in accepted_fields:
        if params[i]:
            spec[i] = params[i]
    _url = "https://{vcenter_hostname}/rest/vcenter/vm/{vm}/hardware/ethernet/{nic}".format(
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
