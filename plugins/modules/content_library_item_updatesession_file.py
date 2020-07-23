from __future__ import absolute_import, division, print_function

__metaclass__ = type
import socket
import json

DOCUMENTATION = "author:\n- Ansible VMware team\ndescription: Handle resource of type content_library_item_updatesession_file\nextends_documentation_fragment: []\nmodule: content_library_item_updatesession_file\nnotes:\n- Tested on vSphere 7.0\noptions:\n  file_name:\n    description:\n    - Name of the file to be removed. Required with I(state=['remove'])\n    type: str\n  file_spec:\n    description:\n    - Specification for the file that needs to be added or updated. This includes\n      whether the client wants to push the content or have the server pull it. Required\n      with I(state=['add'])\n    - 'Validate attributes are:'\n    - ' - C(checksum_info) (dict): The checksum of the file. If specified, the server\n      will verify the checksum once the file is received. If there is a mismatch,\n      the upload will fail. For ova files, this value should not be set.'\n    - ' - C(name) (str): The name of the file being uploaded.'\n    - ' - C(size) (int): The file size, in bytes.'\n    - ' - C(source_endpoint) (dict): Location from which the Content Library Service\n      will fetch the file, rather than requiring a client to upload the file.'\n    - ' - C(source_type) (str): The {@name SourceType} defines how the file content\n      is retrieved.'\n    type: dict\n  state:\n    choices:\n    - add\n    - validate\n    - remove\n    description: []\n    type: str\n  update_session_id:\n    description:\n    - Identifier of the update session to be modified.\n    type: str\n  ~action:\n    choices:\n    - add\n    description:\n    - ~action=add Required with I(state=['add'])\n    type: str\nrequirements:\n- python >= 3.6\nshort_description: Handle resource of type content_library_item_updatesession_file\nversion_added: 1.0.0\n"
IN_QUERY_PARAMETER = ["~action"]
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
    argument_spec["~action"] = {
        "type": "str",
        "choices": ["add"],
        "operationIds": ["add"],
    }
    argument_spec["update_session_id"] = {
        "type": "str",
        "operationIds": ["add", "remove", "validate"],
    }
    argument_spec["state"] = {"type": "str", "choices": ["add", "remove", "validate"]}
    argument_spec["file_spec"] = {"type": "dict", "operationIds": ["add"]}
    argument_spec["file_name"] = {"type": "str", "operationIds": ["remove"]}
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
    return "https://{vcenter_hostname}/rest/com/vmware/content/library/item/updatesession/file".format(
        **params
    )


async def entry_point(module, session):
    func = globals()[("_" + module.params["state"])]
    return await func(module.params, session)


async def _add(params, session):
    accepted_fields = ["file_spec"]
    if "add" == "create":
        _exists = await exists(params, session)
        if _exists:
            return await update_changed_flag({"value": _exists}, 200, "get")
    spec = {}
    for i in accepted_fields:
        if params[i]:
            spec[i] = params[i]
    _url = "https://{vcenter_hostname}/rest/com/vmware/content/library/item/updatesession/file/id:{update_session_id}".format(
        **params
    )
    async with session.post(_url, json={"spec": spec}) as resp:
        try:
            if resp.headers["Content-Type"] == "application/json":
                _json = await resp.json()
        except KeyError:
            _json = {}
        if ("add" == "create") and ("value" in _json):
            if type(_json["value"]) == dict:
                _id = list(_json["value"].values())[0]
            else:
                _id = _json["value"]
            _json = {"value": (await get_device_info(params, session, _url, _id))}
        return await update_changed_flag(_json, resp.status, "add")


async def _remove(params, session):
    accepted_fields = ["file_name"]
    if "remove" == "create":
        _exists = await exists(params, session)
        if _exists:
            return await update_changed_flag({"value": _exists}, 200, "get")
    spec = {}
    for i in accepted_fields:
        if params[i]:
            spec[i] = params[i]
    _url = "https://{vcenter_hostname}/rest/com/vmware/content/library/item/updatesession/file/id:{update_session_id}?~action=remove".format(
        **params
    )
    async with session.post(_url, json={"spec": spec}) as resp:
        try:
            if resp.headers["Content-Type"] == "application/json":
                _json = await resp.json()
        except KeyError:
            _json = {}
        if ("remove" == "create") and ("value" in _json):
            if type(_json["value"]) == dict:
                _id = list(_json["value"].values())[0]
            else:
                _id = _json["value"]
            _json = {"value": (await get_device_info(params, session, _url, _id))}
        return await update_changed_flag(_json, resp.status, "remove")


async def _validate(params, session):
    _url = "https://{vcenter_hostname}/rest/com/vmware/content/library/item/updatesession/file/id:{update_session_id}?~action=validate".format(
        **params
    ) + gen_args(
        params, IN_QUERY_PARAMETER
    )
    async with session.post(_url) as resp:
        try:
            if resp.headers["Content-Type"] == "application/json":
                _json = await resp.json()
        except KeyError:
            _json = {}
        return await update_changed_flag(_json, resp.status, "validate")


if __name__ == "__main__":
    import asyncio

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
