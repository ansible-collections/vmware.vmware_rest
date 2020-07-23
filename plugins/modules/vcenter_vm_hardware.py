from __future__ import absolute_import, division, print_function

__metaclass__ = type
import socket
import json

DOCUMENTATION = "author:\n- Ansible VMware team\ndescription: Handle resource of type vcenter_vm_hardware\nextends_documentation_fragment: []\nmodule: vcenter_vm_hardware\nnotes:\n- Tested on vSphere 7.0\noptions:\n  state:\n    choices:\n    - update\n    description: []\n    type: str\n  upgrade_policy:\n    choices:\n    - NEVER\n    - AFTER_CLEAN_SHUTDOWN\n    - ALWAYS\n    description:\n    - The Hardware.UpgradePolicy enumerated type defines the valid virtual hardware\n      upgrade policies for a virtual machine.\n    type: str\n  upgrade_version:\n    choices:\n    - VMX_03\n    - VMX_04\n    - VMX_06\n    - VMX_07\n    - VMX_08\n    - VMX_09\n    - VMX_10\n    - VMX_11\n    - VMX_12\n    - VMX_13\n    - VMX_14\n    - VMX_15\n    - VMX_16\n    - VMX_17\n    description:\n    - The Hardware.Version enumerated type defines the valid virtual hardware versions\n      for a virtual machine. See https://kb.vmware.com/s/article/1003746 (Virtual\n      machine hardware versions (1003746)).\n    type: str\n  vm:\n    description:\n    - 'Virtual machine identifier.\n\n      The parameter must be an identifier for the resource type: VirtualMachine.'\n    type: str\nrequirements:\n- python >= 3.6\nshort_description: Handle resource of type vcenter_vm_hardware\nversion_added: 1.0.0\n"
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
    argument_spec["vm"] = {"type": "str", "operationIds": ["update"]}
    argument_spec["upgrade_version"] = {
        "type": "str",
        "choices": [
            "VMX_03",
            "VMX_04",
            "VMX_06",
            "VMX_07",
            "VMX_08",
            "VMX_09",
            "VMX_10",
            "VMX_11",
            "VMX_12",
            "VMX_13",
            "VMX_14",
            "VMX_15",
            "VMX_16",
            "VMX_17",
        ],
        "operationIds": ["update"],
    }
    argument_spec["upgrade_policy"] = {
        "type": "str",
        "choices": ["AFTER_CLEAN_SHUTDOWN", "ALWAYS", "NEVER"],
        "operationIds": ["update"],
    }
    argument_spec["state"] = {"type": "str", "choices": ["update"]}
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
    return "https://{vcenter_hostname}/rest/vcenter/vm/{vm}/hardware".format(**params)


async def entry_point(module, session):
    func = globals()[("_" + module.params["state"])]
    return await func(module.params, session)


async def _update(params, session):
    accepted_fields = ["upgrade_policy", "upgrade_version"]
    if "update" == "create":
        _exists = await exists(params, session)
        if _exists:
            return await update_changed_flag({"value": _exists}, 200, "get")
    spec = {}
    for i in accepted_fields:
        if params[i]:
            spec[i] = params[i]
    _url = "https://{vcenter_hostname}/rest/vcenter/vm/{vm}/hardware".format(**params)
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
