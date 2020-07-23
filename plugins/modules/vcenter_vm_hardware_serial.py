from __future__ import absolute_import, division, print_function

__metaclass__ = type
import socket
import json

DOCUMENTATION = "author:\n- Ansible VMware team\ndescription: Handle resource of type vcenter_vm_hardware_serial\nextends_documentation_fragment: []\nmodule: vcenter_vm_hardware_serial\nnotes:\n- Tested on vSphere 7.0\noptions:\n  allow_guest_control:\n    description:\n    - 'Flag indicating whether the guest can connect and disconnect the device.\n\n      If unset, the value is unchanged.'\n    type: bool\n  backing:\n    description:\n    - \"Physical resource backing for the virtual serial port. \\n This field may only\\\n      \\ be modified if the virtual machine is not powered on or the virtual serial\\\n      \\ port is not connected.\\n\\nIf unset, the value is unchanged.\"\n    - 'Validate attributes are:'\n    - ' - C(file) (str): Path of the file backing the virtual serial port.\n\n      This field is optional and it is only relevant when the value of Serial.BackingSpec.type\n      is FILE.'\n    - \" - C(host_device) (str): Name of the device backing the virtual serial port.\\\n      \\ \\n\\n\\nIf unset, the virtual serial port will be configured to automatically\\\n      \\ detect a suitable host device.\"\n    - \" - C(network_location) (str): URI specifying the location of the network service\\\n      \\ backing the virtual serial port. \\n   - If Serial.BackingSpec.type is NETWORK_SERVER,\\\n      \\ this field is the location used by clients to connect to this server. The\\\n      \\ hostname part of the URI should either be empty or should specify the address\\\n      \\ of the host on which the virtual machine is running.\\n   - If Serial.BackingSpec.type\\\n      \\ is NETWORK_CLIENT, this field is the location used by the virtual machine\\\n      \\ to connect to the remote server.\\n \\nThis field is optional and it is only\\\n      \\ relevant when the value of Serial.BackingSpec.type is one of NETWORK_SERVER\\\n      \\ or NETWORK_CLIENT.\"\n    - ' - C(no_rx_loss) (bool): Flag that enables optimized data transfer over the\n      pipe. When the value is true, the host buffers data to prevent data overrun.\n      This allows the virtual machine to read all of the data transferred over the\n      pipe with no data loss.\n\n      If unset, defaults to false.'\n    - ' - C(pipe) (str): Name of the pipe backing the virtual serial port.\n\n      This field is optional and it is only relevant when the value of Serial.BackingSpec.type\n      is one of PIPE_SERVER or PIPE_CLIENT.'\n    - ' - C(proxy) (str): Proxy service that provides network access to the network\n      backing. If set, the virtual machine initiates a connection with the proxy service\n      and forwards the traffic to the proxy.\n\n      If unset, no proxy service should be used.'\n    - ' - C(type) (str): The Serial.BackingType enumerated type defines the valid\n      backing types for a virtual serial port.'\n    type: dict\n  port:\n    description:\n    - 'Virtual serial port identifier.\n\n      The parameter must be an identifier for the resource type: vcenter.vm.hardware.SerialPort.\n      Required with I(state=[''update'', ''delete''])'\n    type: str\n  start_connected:\n    description:\n    - 'Flag indicating whether the virtual device should be connected whenever the\n      virtual machine is powered on.\n\n      If unset, the value is unchanged.'\n    type: bool\n  state:\n    choices:\n    - update\n    - delete\n    - create\n    description: []\n    type: str\n  vm:\n    description:\n    - 'Virtual machine identifier.\n\n      The parameter must be an identifier for the resource type: VirtualMachine.'\n    type: str\n  yield_on_poll:\n    description:\n    - \"CPU yield behavior. If set to true, the virtual machine will periodically relinquish\\\n      \\ the processor if its sole task is polling the virtual serial port. The amount\\\n      \\ of time it takes to regain the processor will depend on the degree of other\\\n      \\ virtual machine activity on the host. \\n This field may be modified at any\\\n      \\ time, and changes applied to a connected virtual serial port take effect immediately.\\n\\\n      \\nIf unset, the value is unchanged.\"\n    type: bool\nrequirements:\n- python >= 3.6\nshort_description: Handle resource of type vcenter_vm_hardware_serial\nversion_added: 1.0.0\n"
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
    argument_spec["yield_on_poll"] = {
        "type": "bool",
        "operationIds": ["create", "update"],
    }
    argument_spec["vm"] = {
        "type": "str",
        "operationIds": ["create", "delete", "update"],
    }
    argument_spec["state"] = {"type": "str", "choices": ["create", "delete", "update"]}
    argument_spec["start_connected"] = {
        "type": "bool",
        "operationIds": ["create", "update"],
    }
    argument_spec["port"] = {"type": "str", "operationIds": ["delete", "update"]}
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
    return "https://{vcenter_hostname}/rest/vcenter/vm/{vm}/hardware/serial".format(
        **params
    )


async def entry_point(module, session):
    func = globals()[("_" + module.params["state"])]
    return await func(module.params, session)


async def _create(params, session):
    accepted_fields = [
        "allow_guest_control",
        "backing",
        "start_connected",
        "yield_on_poll",
    ]
    if "create" == "create":
        _exists = await exists(params, session)
        if _exists:
            return await update_changed_flag({"value": _exists}, 200, "get")
    spec = {}
    for i in accepted_fields:
        if params[i]:
            spec[i] = params[i]
    _url = "https://{vcenter_hostname}/rest/vcenter/vm/{vm}/hardware/serial".format(
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
    _url = "https://{vcenter_hostname}/rest/vcenter/vm/{vm}/hardware/serial/{port}".format(
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
        "start_connected",
        "yield_on_poll",
    ]
    if "update" == "create":
        _exists = await exists(params, session)
        if _exists:
            return await update_changed_flag({"value": _exists}, 200, "get")
    spec = {}
    for i in accepted_fields:
        if params[i]:
            spec[i] = params[i]
    _url = "https://{vcenter_hostname}/rest/vcenter/vm/{vm}/hardware/serial/{port}".format(
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
