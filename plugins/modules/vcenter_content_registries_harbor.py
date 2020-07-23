from __future__ import absolute_import, division, print_function

__metaclass__ = type
import socket
import json

DOCUMENTATION = "author:\n- Ansible VMware team\ndescription: Handle resource of type vcenter_content_registries_harbor\nextends_documentation_fragment: []\nmodule: vcenter_content_registries_harbor\nnotes:\n- Tested on vSphere 7.0\noptions:\n  client_token:\n    description:\n    - 'A unique token generated on the client for each creation request. The token\n      should be a universally unique identifier (UUID), for example: {@code b8a2a2e3-2314-43cd-a871-6ede0f429751}.\n      This token can be used to guarantee idempotent creation.'\n    type: str\n  cluster:\n    description:\n    - Identifier of the cluster hosting the registry.\n    type: str\n  garbage_collection:\n    description:\n    - Garbage collection configuration for the Harbor registry.\n    - 'Validate attributes are:'\n    - ' - C(day_of_week) (str): The day of the week describes the supported days of\n      the week to run a specific operation for a container registry.'\n    - ' - C(hour) (int): Hour at which garbage collection should run.'\n    - ' - C(minute) (int): Minute at which garbage collection should run.'\n    - ' - C(type) (str): The {@name Recurrence} defines the supported values for how\n      often to run a specific operation for a container registry.'\n    type: dict\n  registry:\n    description:\n    - Identifier of the registry. Required with I(state=['delete'])\n    type: str\n  state:\n    choices:\n    - create\n    - delete\n    description: []\n    type: str\n  storage:\n    description:\n    - Storage associated with the Harbor registry. The list contains only one storage\n      backing in this version. Required with I(state=['create'])\n    type: list\nrequirements:\n- python >= 3.6\nshort_description: Handle resource of type vcenter_content_registries_harbor\nversion_added: 1.0.0\n"
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
    argument_spec["storage"] = {"type": "list", "operationIds": ["create"]}
    argument_spec["state"] = {"type": "str", "choices": ["create", "delete"]}
    argument_spec["registry"] = {"type": "str", "operationIds": ["delete"]}
    argument_spec["garbage_collection"] = {"type": "dict", "operationIds": ["create"]}
    argument_spec["cluster"] = {"type": "str", "operationIds": ["create"]}
    argument_spec["client_token"] = {"type": "str", "operationIds": ["create"]}
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
    return "https://{vcenter_hostname}/rest/vcenter/content/registries/harbor".format(
        **params
    )


async def entry_point(module, session):
    func = globals()[("_" + module.params["state"])]
    return await func(module.params, session)


async def _create(params, session):
    accepted_fields = ["client_token", "cluster", "garbage_collection", "storage"]
    if "create" == "create":
        _exists = await exists(params, session)
        if _exists:
            return await update_changed_flag({"value": _exists}, 200, "get")
    spec = {}
    for i in accepted_fields:
        if params[i]:
            spec[i] = params[i]
    _url = "https://{vcenter_hostname}/rest/vcenter/content/registries/harbor".format(
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
    _url = "https://{vcenter_hostname}/rest/vcenter/content/registries/harbor/{registry}".format(
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
