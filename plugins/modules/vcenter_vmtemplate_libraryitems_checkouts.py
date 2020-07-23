from __future__ import absolute_import, division, print_function

__metaclass__ = type
import socket
import json

DOCUMENTATION = "author:\n- Ansible VMware team\ndescription: Handle resource of type vcenter_vmtemplate_libraryitems_checkouts\nextends_documentation_fragment: []\nmodule: vcenter_vmtemplate_libraryitems_checkouts\nnotes:\n- Tested on vSphere 7.0\noptions:\n  action:\n    choices:\n    - check-in\n    description:\n    - action=check-in Required with I(state=['check_in', 'check_out'])\n    type: str\n  message:\n    description:\n    - Message describing the changes made to the virtual machine. Required with I(state=['check_in'])\n    type: str\n  name:\n    description:\n    - Name of the virtual machine to check out of the library item.\n    type: str\n  placement:\n    description:\n    - Information used to place the checked out virtual machine.\n    - 'Validate attributes are:'\n    - ' - C(cluster) (str): Cluster onto which the virtual machine should be placed.\n      If {@name #cluster} and {@name #resourcePool} are both specified, {@name #resourcePool}\n      must belong to {@name #cluster}. If {@name #cluster} and {@name #host} are both\n      specified, {@name #host} must be a member of {@name #cluster}.'\n    - ' - C(folder) (str): Virtual machine folder into which the virtual machine should\n      be placed.'\n    - ' - C(host) (str): Host onto which the virtual machine should be placed. If\n      {@name #host} and {@name #resourcePool} are both specified, {@name #resourcePool}\n      must belong to {@name #host}. If {@name #host} and {@name #cluster} are both\n      specified, {@name #host} must be a member of {@name #cluster}.'\n    - ' - C(resource_pool) (str): Resource pool into which the virtual machine should\n      be placed.'\n    type: dict\n  powered_on:\n    description:\n    - Specifies whether the virtual machine should be powered on after check out.\n    type: bool\n  state:\n    choices:\n    - check_in\n    - delete\n    - check_out\n    description: []\n    type: str\n  template_library_item:\n    description:\n    - Identifier of the content library item in which the virtual machine is checked\n      in.\n    type: str\n  vm:\n    description:\n    - Identifier of the virtual machine to check into the library item. Required with\n      I(state=['check_in', 'delete'])\n    type: str\nrequirements:\n- python >= 3.6\nshort_description: Handle resource of type vcenter_vmtemplate_libraryitems_checkouts\nversion_added: 1.0.0\n"
IN_QUERY_PARAMETER = ["action"]
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
    argument_spec["vm"] = {"type": "str", "operationIds": ["check_in", "delete"]}
    argument_spec["template_library_item"] = {
        "type": "str",
        "operationIds": ["check_in", "check_out", "delete"],
    }
    argument_spec["state"] = {
        "type": "str",
        "choices": ["check_in", "check_out", "delete"],
    }
    argument_spec["powered_on"] = {"type": "bool", "operationIds": ["check_out"]}
    argument_spec["placement"] = {"type": "dict", "operationIds": ["check_out"]}
    argument_spec["name"] = {"type": "str", "operationIds": ["check_out"]}
    argument_spec["message"] = {"type": "str", "operationIds": ["check_in"]}
    argument_spec["action"] = {
        "type": "str",
        "choices": ["check-in"],
        "operationIds": ["check_in", "check_out"],
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
    return "https://{vcenter_hostname}/rest/vcenter/vm-template/library-items/{template_library_item}/check-outs".format(
        **params
    )


async def entry_point(module, session):
    func = globals()[("_" + module.params["state"])]
    return await func(module.params, session)


async def _check_in(params, session):
    accepted_fields = ["message"]
    if "check_in" == "create":
        _exists = await exists(params, session)
        if _exists:
            return await update_changed_flag({"value": _exists}, 200, "get")
    spec = {}
    for i in accepted_fields:
        if params[i]:
            spec[i] = params[i]
    _url = "https://{vcenter_hostname}/rest/vcenter/vm-template/library-items/{template_library_item}/check-outs/{vm}".format(
        **params
    )
    async with session.post(_url, json={"spec": spec}) as resp:
        try:
            if resp.headers["Content-Type"] == "application/json":
                _json = await resp.json()
        except KeyError:
            _json = {}
        if (
            ("check_in" == "create")
            and (resp.status in [200, 201])
            and ("value" in _json)
        ):
            if type(_json["value"]) == dict:
                _id = list(_json["value"].values())[0]
            else:
                _id = _json["value"]
            _json = {"value": (await get_device_info(params, session, _url, _id))}
        return await update_changed_flag(_json, resp.status, "check_in")


async def _check_out(params, session):
    accepted_fields = ["name", "placement", "powered_on"]
    if "check_out" == "create":
        _exists = await exists(params, session)
        if _exists:
            return await update_changed_flag({"value": _exists}, 200, "get")
    spec = {}
    for i in accepted_fields:
        if params[i]:
            spec[i] = params[i]
    _url = "https://{vcenter_hostname}/rest/vcenter/vm-template/library-items/{template_library_item}/check-outs".format(
        **params
    )
    async with session.post(_url, json={"spec": spec}) as resp:
        try:
            if resp.headers["Content-Type"] == "application/json":
                _json = await resp.json()
        except KeyError:
            _json = {}
        if (
            ("check_out" == "create")
            and (resp.status in [200, 201])
            and ("value" in _json)
        ):
            if type(_json["value"]) == dict:
                _id = list(_json["value"].values())[0]
            else:
                _id = _json["value"]
            _json = {"value": (await get_device_info(params, session, _url, _id))}
        return await update_changed_flag(_json, resp.status, "check_out")


async def _delete(params, session):
    _url = "https://{vcenter_hostname}/rest/vcenter/vm-template/library-items/{template_library_item}/check-outs/{vm}".format(
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


if __name__ == "__main__":
    import asyncio

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
