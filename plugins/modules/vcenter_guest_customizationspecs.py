from __future__ import absolute_import, division, print_function

__metaclass__ = type
import socket
import json

DOCUMENTATION = """
module: vcenter_guest_customizationspecs
short_description: Handle resource of type vcenter_guest_customizationspecs
description: Handle resource of type vcenter_guest_customizationspecs
options:
  customization_spec:
    description:
    - content to be converted to the spec. Required with I(state=['import_specification'])
    type: str
  description:
    description:
    - Description of the specification. Required with I(state=['create', 'set'])
    type: str
  fingerprint:
    description:
    - The fingerprint is a unique identifier for a given version of the configuration.
      Each change to the configuration will update this value. A client cannot change
      this value. If specified when updating a specification, the changes will only
      be applied if the current fingerprint matches the specified fingerprint. This
      field can be used to guard against updates that has happened between the specification
      content was read and until it is applied. Required with I(state=['set'])
    type: str
  format:
    choices:
    - JSON
    - XML
    description:
    - The CustomizationSpecs.Format enumerated type specifies the formats the customization
      specification can be exported to. Required with I(state=['export'])
    type: str
  name:
    description:
    - The name of the customization specification that needs to be deleted.
    - 'The parameter must be an identifier for the resource type: vcenter.guest.CustomizationSpec.
      Required with I(state=[''create'', ''delete'', ''export'', ''set''])'
    type: str
  spec:
    description:
    - The specification object. Required with I(state=['create', 'set'])
    - 'Validate attributes are:'
    - ' - C(configuration_spec) (dict): Settings to be applied to the guest during
      the customization.'
    - ' - C(global_DNS_settings) (dict): Global DNS settings constitute the DNS settings
      that are not specific to a particular virtual network adapter.'
    - ' - C(interfaces) (list): IP settings that are specific to a particular virtual
      network adapter. The AdapterMapping structure maps a network adapter''s MAC
      address to its IPSettings. May be empty if there are no network adapters, else
      should match number of network adapters configured for the VM.'
    type: dict
  state:
    choices:
    - create
    - delete
    - export
    - import_specification
    - set
    description: []
    type: str
author:
- Ansible VMware team
version_added: 1.0.0
requirements:
- python >= 3.6
"""
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
    accepted_fields = ["description", "spec"]
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
    _url = "https://{vcenter_hostname}/rest/vcenter/guest/customization-specs/{name}".format(
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


async def _export(params, session):
    accepted_fields = ["format"]
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
    accepted_fields = ["description", "fingerprint", "spec"]
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
