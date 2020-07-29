from __future__ import absolute_import, division, print_function

__metaclass__ = type
import socket
import json

DOCUMENTATION = """
module: vcenter_deployment_install_psc_replicated
short_description: Handle resource of type vcenter_deployment_install_psc_replicated
description: Handle resource of type vcenter_deployment_install_psc_replicated
options:
  action:
    choices:
    - check
    description:
    - action=check
    type: str
  https_port:
    description:
    - The HTTPS port of the external PSC appliance.
    type: int
  partner_hostname:
    description:
    - The IP address or DNS resolvable name of the partner PSC appliance.
    type: str
  ssl_thumbprint:
    description:
    - SHA1 thumbprint of the server SSL certificate will be used for verification.
    type: str
  ssl_verify:
    description:
    - SSL verification should be enabled or disabled.
    type: bool
  sso_admin_password:
    description:
    - The SSO administrator account password.
    type: str
  sso_site_name:
    description:
    - The SSO sitename that will be used in PSC replication.
    type: str
  state:
    choices:
    - check
    description: []
    type: str
author:
- Ansible VMware team
version_added: 1.0.0
requirements:
- python >= 3.6
"""
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
    argument_spec["state"] = {"type": "str", "choices": ["check"]}
    argument_spec["sso_site_name"] = {"type": "str", "operationIds": ["check"]}
    argument_spec["sso_admin_password"] = {"type": "str", "operationIds": ["check"]}
    argument_spec["ssl_verify"] = {"type": "bool", "operationIds": ["check"]}
    argument_spec["ssl_thumbprint"] = {"type": "str", "operationIds": ["check"]}
    argument_spec["partner_hostname"] = {"type": "str", "operationIds": ["check"]}
    argument_spec["https_port"] = {"type": "int", "operationIds": ["check"]}
    argument_spec["action"] = {
        "type": "str",
        "choices": ["check"],
        "operationIds": ["check"],
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
    return "https://{vcenter_hostname}/rest/vcenter/deployment/install/psc/replicated".format(
        **params
    )


async def entry_point(module, session):
    func = globals()[("_" + module.params["state"])]
    return await func(module.params, session)


async def _check(params, session):
    accepted_fields = [
        "https_port",
        "partner_hostname",
        "ssl_thumbprint",
        "ssl_verify",
        "sso_admin_password",
        "sso_site_name",
    ]
    if "check" == "create":
        _exists = await exists(params, session)
        if _exists:
            return await update_changed_flag({"value": _exists}, 200, "get")
    spec = {}
    for i in accepted_fields:
        if params[i]:
            spec[i] = params[i]
    _url = "https://{vcenter_hostname}/rest/vcenter/deployment/install/psc/replicated".format(
        **params
    )
    async with session.post(_url, json={"spec": spec}) as resp:
        try:
            if resp.headers["Content-Type"] == "application/json":
                _json = await resp.json()
        except KeyError:
            _json = {}
        if ("check" == "create") and (resp.status in [200, 201]) and ("value" in _json):
            if type(_json["value"]) == dict:
                _id = list(_json["value"].values())[0]
            else:
                _id = _json["value"]
            _json = {"value": (await get_device_info(params, session, _url, _id))}
        return await update_changed_flag(_json, resp.status, "check")


if __name__ == "__main__":
    import asyncio

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
