from __future__ import absolute_import, division, print_function

__metaclass__ = type
import socket
import json

DOCUMENTATION = "author:\n- Ansible VMware team\ndescription: Handle resource of type vcenter_certificatemanagement_vcenter_tlscsr\nextends_documentation_fragment: []\nmodule: vcenter_certificatemanagement_vcenter_tlscsr\nnotes:\n- Tested on vSphere 7.0\noptions:\n  common_name:\n    description:\n    - commonName will take PNID if not modified.\n    type: str\n  country:\n    description:\n    - Country field in certificate subject\n    type: str\n  email_address:\n    description:\n    - Email field in Certificate extensions\n    type: str\n  key_size:\n    description:\n    - keySize will take 2048 bits if not modified.\n    type: int\n  locality:\n    description:\n    - Locality field in certificate subject\n    type: str\n  organization:\n    description:\n    - Organization field in certificate subject\n    type: str\n  organization_unit:\n    description:\n    - Organization unit field in certificate subject\n    type: str\n  state:\n    choices:\n    - create\n    description: []\n    type: str\n  state_or_province:\n    description:\n    - State field in certificate subject\n    type: str\n  subject_alt_name:\n    description:\n    - subjectAltName is list of Dns Names and Ip addresses\n    type: list\nrequirements:\n- python >= 3.6\nshort_description: Handle resource of type vcenter_certificatemanagement_vcenter_tlscsr\nversion_added: 1.0.0\n"
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
    argument_spec["subject_alt_name"] = {"type": "list", "operationIds": ["create"]}
    argument_spec["state_or_province"] = {"type": "str", "operationIds": ["create"]}
    argument_spec["state"] = {"type": "str", "choices": ["create"]}
    argument_spec["organization_unit"] = {"type": "str", "operationIds": ["create"]}
    argument_spec["organization"] = {"type": "str", "operationIds": ["create"]}
    argument_spec["locality"] = {"type": "str", "operationIds": ["create"]}
    argument_spec["key_size"] = {"type": "int", "operationIds": ["create"]}
    argument_spec["email_address"] = {"type": "str", "operationIds": ["create"]}
    argument_spec["country"] = {"type": "str", "operationIds": ["create"]}
    argument_spec["common_name"] = {"type": "str", "operationIds": ["create"]}
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
    return "https://{vcenter_hostname}/rest/vcenter/certificate-management/vcenter/tls-csr".format(
        **params
    )


async def entry_point(module, session):
    func = globals()[("_" + module.params["state"])]
    return await func(module.params, session)


async def _create(params, session):
    accepted_fields = [
        "common_name",
        "country",
        "email_address",
        "key_size",
        "locality",
        "organization",
        "organization_unit",
        "state_or_province",
        "subject_alt_name",
    ]
    if "create" == "create":
        _exists = await exists(params, session)
        if _exists:
            return await update_changed_flag({"value": _exists}, 200, "get")
    spec = {}
    for i in accepted_fields:
        if params[i]:
            spec[i] = params[i]
    _url = "https://{vcenter_hostname}/rest/vcenter/certificate-management/vcenter/tls-csr".format(
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


if __name__ == "__main__":
    import asyncio

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
