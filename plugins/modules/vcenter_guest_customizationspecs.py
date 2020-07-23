from __future__ import absolute_import, division, print_function

__metaclass__ = type
import socket
import json

DOCUMENTATION = "author:\n- Ansible VMware team\ndescription: Handle resource of type vcenter_guest_customizationspecs\nextends_documentation_fragment: []\nmodule: vcenter_guest_customizationspecs\nnotes:\n- Tested on vSphere 7.0\noptions:\n  customization_spec:\n    description:\n    - content to be converted to the spec. Required with I(state=['import_specification'])\n    type: str\n  description:\n    description:\n    - Description of the specification. Required with I(state=['create', 'set'])\n    type: str\n  fingerprint:\n    description:\n    - The fingerprint is a unique identifier for a given version of the configuration.\n      Each change to the configuration will update this value. A client cannot change\n      this value. If specified when updating a specification, the changes will only\n      be applied if the current fingerprint matches the specified fingerprint. This\n      field can be used to guard against updates that has happened between the specification\n      content was read and until it is applied. Required with I(state=['set'])\n    type: str\n  format:\n    choices:\n    - JSON\n    - XML\n    description:\n    - The CustomizationSpecs.Format enumerated type specifies the formats the customization\n      specification can be exported to. Required with I(state=['export'])\n    type: str\n  name:\n    description:\n    - Name of the specification. Required with I(state=['create', 'delete', 'set',\n      'export'])\n    type: str\n  spec:\n    description:\n    - The specification object. Required with I(state=['create', 'set'])\n    - 'Validate attributes are:'\n    - ' - C(configuration_spec) (dict): Settings to be applied to the guest during\n      the customization.'\n    - ' - C(global_DNS_settings) (dict): Global DNS settings constitute the DNS settings\n      that are not specific to a particular virtual network adapter.'\n    - ' - C(interfaces) (list): IP settings that are specific to a particular virtual\n      network adapter. The AdapterMapping structure maps a network adapter''s MAC\n      address to its IPSettings. May be empty if there are no network adapters, else\n      should match number of network adapters configured for the VM.'\n    type: dict\n  state:\n    choices:\n    - import_specification\n    - create\n    - delete\n    - set\n    - export\n    description: []\n    type: str\nrequirements:\n- python >= 3.6\nshort_description: Handle resource of type vcenter_guest_customizationspecs\nversion_added: 1.0.0\n"
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
    argument_spec["state"] = {
        "type": "str",
        "choices": ["create", "delete", "export", "import_specification", "set"],
    }
    argument_spec["spec"] = {"type": "dict", "operationIds": ["create", "set"]}
    argument_spec["name"] = {
        "type": "str",
        "operationIds": ["create", "delete", "export", "set", "set"],
    }
    argument_spec["format"] = {
        "type": "str",
        "choices": ["JSON", "XML"],
        "operationIds": ["export"],
    }
    argument_spec["fingerprint"] = {"type": "str", "operationIds": ["set"]}
    argument_spec["description"] = {"type": "str", "operationIds": ["create", "set"]}
    argument_spec["customization_spec"] = {
        "type": "str",
        "operationIds": ["import_specification"],
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
    return "https://{vcenter_hostname}/rest/vcenter/guest/customization-specs".format(
        **params
    )


async def entry_point(module, session):
    func = globals()[("_" + module.params["state"])]
    return await func(module.params, session)


async def _create(params, session):
    accepted_fields = ["description", "name", "spec"]
    if "create" == "create":
        _exists = await exists(params, session)
        if _exists:
            return await update_changed_flag({"value": _exists}, 200, "get")
    spec = {}
    for i in accepted_fields:
        if params[i]:
            spec[i] = params[i]
    _url = "https://{vcenter_hostname}/rest/vcenter/guest/customization-specs".format(
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
    accepted_fields = ["name"]
    if "delete" == "create":
        _exists = await exists(params, session)
        if _exists:
            return await update_changed_flag({"value": _exists}, 200, "get")
    spec = {}
    for i in accepted_fields:
        if params[i]:
            spec[i] = params[i]
    _url = "https://{vcenter_hostname}/rest/vcenter/guest/customization-specs/{name}".format(
        **params
    )
    async with session.delete(_url, json={"spec": spec}) as resp:
        try:
            if resp.headers["Content-Type"] == "application/json":
                _json = await resp.json()
        except KeyError:
            _json = {}
        if (
            ("delete" == "create")
            and (resp.status in [200, 201])
            and ("value" in _json)
        ):
            if type(_json["value"]) == dict:
                _id = list(_json["value"].values())[0]
            else:
                _id = _json["value"]
            _json = {"value": (await get_device_info(params, session, _url, _id))}
        return await update_changed_flag(_json, resp.status, "delete")


async def _export(params, session):
    accepted_fields = ["format", "name"]
    if "export" == "create":
        _exists = await exists(params, session)
        if _exists:
            return await update_changed_flag({"value": _exists}, 200, "get")
    spec = {}
    for i in accepted_fields:
        if params[i]:
            spec[i] = params[i]
    _url = "https://{vcenter_hostname}/rest/vcenter/guest/customization-specs/{name}?action=export".format(
        **params
    )
    async with session.post(_url, json={"spec": spec}) as resp:
        try:
            if resp.headers["Content-Type"] == "application/json":
                _json = await resp.json()
        except KeyError:
            _json = {}
        if (
            ("export" == "create")
            and (resp.status in [200, 201])
            and ("value" in _json)
        ):
            if type(_json["value"]) == dict:
                _id = list(_json["value"].values())[0]
            else:
                _id = _json["value"]
            _json = {"value": (await get_device_info(params, session, _url, _id))}
        return await update_changed_flag(_json, resp.status, "export")


async def _import_specification(params, session):
    accepted_fields = ["customization_spec"]
    if "import_specification" == "create":
        _exists = await exists(params, session)
        if _exists:
            return await update_changed_flag({"value": _exists}, 200, "get")
    spec = {}
    for i in accepted_fields:
        if params[i]:
            spec[i] = params[i]
    _url = "https://{vcenter_hostname}/rest/vcenter/guest/customization-specs?action=import".format(
        **params
    )
    async with session.post(_url, json={"spec": spec}) as resp:
        try:
            if resp.headers["Content-Type"] == "application/json":
                _json = await resp.json()
        except KeyError:
            _json = {}
        if (
            ("import_specification" == "create")
            and (resp.status in [200, 201])
            and ("value" in _json)
        ):
            if type(_json["value"]) == dict:
                _id = list(_json["value"].values())[0]
            else:
                _id = _json["value"]
            _json = {"value": (await get_device_info(params, session, _url, _id))}
        return await update_changed_flag(_json, resp.status, "import_specification")


async def _set(params, session):
    accepted_fields = ["description", "fingerprint", "name", "spec"]
    if "set" == "create":
        _exists = await exists(params, session)
        if _exists:
            return await update_changed_flag({"value": _exists}, 200, "get")
    spec = {}
    for i in accepted_fields:
        if params[i]:
            spec[i] = params[i]
    _url = "https://{vcenter_hostname}/rest/vcenter/guest/customization-specs/{name}".format(
        **params
    )
    async with session.post(_url, json={"spec": spec}) as resp:
        try:
            if resp.headers["Content-Type"] == "application/json":
                _json = await resp.json()
        except KeyError:
            _json = {}
        if ("set" == "create") and (resp.status in [200, 201]) and ("value" in _json):
            if type(_json["value"]) == dict:
                _id = list(_json["value"].values())[0]
            else:
                _id = _json["value"]
            _json = {"value": (await get_device_info(params, session, _url, _id))}
        return await update_changed_flag(_json, resp.status, "set")


if __name__ == "__main__":
    import asyncio

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
