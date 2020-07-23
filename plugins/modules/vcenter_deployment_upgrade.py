from __future__ import absolute_import, division, print_function

__metaclass__ = type
import socket
import json

DOCUMENTATION = "author:\n- Ansible VMware team\ndescription: Handle resource of type vcenter_deployment_upgrade\nextends_documentation_fragment: []\nmodule: vcenter_deployment_upgrade\nnotes:\n- Tested on vSphere 7.0\noptions:\n  action:\n    choices:\n    - cancel\n    description:\n    - action=cancel Required with I(state=['cancel'])\n    type: str\n  auto_answer:\n    description:\n    - Use the default option for any questions that may come up during appliance configuration.\n    type: bool\n  history:\n    description:\n    - 'Determines how vCenter history will be migrated during the upgrade process.\n      vCenter history consists of: <ul> <li>Statistics</li> <li>Events</li> <li>Tasks</li>\n      </ul> By default only core data will be migrated. Use this spec to define which\n      part of vCenter history data will be migrated and when.'\n    - 'Validate attributes are:'\n    - ' - C(data_set) (str): The {@name HistoryMigrationOption} defines the vCenter\n      history migration option choices.'\n    - ' - C(defer_import) (bool): Defines how vCenter history will be migrated. If\n      set to true, vCenter history will be migrated separately after successful upgrade\n      or migration, otherwise it will be migrated along with core data during the\n      upgrade or migration process.'\n    type: dict\n  psc:\n    description:\n    - Information that are specific to this Platform Services Controller.\n    - 'Validate attributes are:'\n    - ' - C(ceip_enabled) (bool): Customer experience improvement program should be\n      enabled or disabled for this Platform Services Controller upgrade.'\n    type: dict\n  source_appliance:\n    description:\n    - Source appliance spec. Required with I(state=['check', 'start'])\n    - 'Validate attributes are:'\n    - ' - C(hostname) (str): The IP address or DNS resolvable name of the source appliance.'\n    - ' - C(https_port) (int): The HTTPS port of the source appliance.'\n    - ' - C(root_password) (str): The password of the root user on the source appliance.'\n    - ' - C(ssh_thumbprint) (str): MD5 thumbprint of the server SSH key will be used\n      for verification.'\n    - ' - C(ssh_verify) (bool): Appliance SSH verification should be enabled or disabled.\n      By default it is disabled and will not use any verification. If thumbprint is\n      provided, thumbprint verification will be performed.'\n    - ' - C(ssl_thumbprint) (str): SHA1 thumbprint of the server SSL certificate will\n      be used for verification.'\n    - ' - C(ssl_verify) (bool): SSL verification should be enabled or disabled for\n      the source appliance validations. By default it is enabled and will use SSL\n      certificate for verification. If thumbprint is provided, will use thumbprint\n      for the verification.'\n    - ' - C(sso_admin_password) (str): The SSO administrator account password.'\n    - ' - C(sso_admin_username) (str): The SSO administrator account on the source\n      appliance.'\n    type: dict\n  source_location:\n    description:\n    - Source location spec. Required with I(state=['check', 'start'])\n    - 'Validate attributes are:'\n    - ' - C(hostname) (str): The IP address or DNS resolvable name of the container.'\n    - ' - C(https_port) (int): The HTTPS port of the container.'\n    - ' - C(password) (str): The administrator account password.'\n    - ' - C(ssl_thumbprint) (str): SHA1 thumbprint of the server SSL certificate will\n      be used for verification.'\n    - ' - C(ssl_verify) (bool): SSL verification should be enabled or disabled. If\n      {@name #sslVerify} is true and and {@name #sslThumbprint} is {@term unset},\n      the CA certificate will be used for verification. If {@name #sslVerify} is true\n      and {@name #sslThumbprint} is set then the thumbprint will be used for verification.\n      No verification will be performed if {@name #sslVerify} value is set to false.'\n    - ' - C(username) (str): The administrator account on the host.'\n    type: dict\n  state:\n    choices:\n    - cancel\n    - check\n    - start\n    description: []\n    type: str\n  vcsa_embedded:\n    description:\n    - Information that are specific to this embedded vCenter Server.\n    - 'Validate attributes are:'\n    - ' - C(ceip_enabled) (bool): Customer experience improvement program should be\n      enabled or disabled for this embedded vCenter Server upgrade.'\n    type: dict\nrequirements:\n- python >= 3.6\nshort_description: Handle resource of type vcenter_deployment_upgrade\nversion_added: 1.0.0\n"
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
    argument_spec["vcsa_embedded"] = {
        "type": "dict",
        "operationIds": ["check", "start"],
    }
    argument_spec["state"] = {"type": "str", "choices": ["cancel", "check", "start"]}
    argument_spec["source_location"] = {
        "type": "dict",
        "operationIds": ["check", "start"],
    }
    argument_spec["source_appliance"] = {
        "type": "dict",
        "operationIds": ["check", "start"],
    }
    argument_spec["psc"] = {"type": "dict", "operationIds": ["check", "start"]}
    argument_spec["history"] = {"type": "dict", "operationIds": ["check", "start"]}
    argument_spec["auto_answer"] = {"type": "bool", "operationIds": ["check", "start"]}
    argument_spec["action"] = {
        "type": "str",
        "choices": ["cancel"],
        "operationIds": ["cancel"],
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
    return "https://{vcenter_hostname}/rest/vcenter/deployment/upgrade".format(**params)


async def entry_point(module, session):
    func = globals()[("_" + module.params["state"])]
    return await func(module.params, session)


async def _cancel(params, session):
    _url = "https://{vcenter_hostname}/rest/vcenter/deployment/upgrade".format(
        **params
    ) + gen_args(params, IN_QUERY_PARAMETER)
    async with session.post(_url) as resp:
        try:
            if resp.headers["Content-Type"] == "application/json":
                _json = await resp.json()
        except KeyError:
            _json = {}
        return await update_changed_flag(_json, resp.status, "cancel")


async def _check(params, session):
    accepted_fields = [
        "auto_answer",
        "history",
        "psc",
        "source_appliance",
        "source_location",
        "vcsa_embedded",
    ]
    if "check" == "create":
        _exists = await exists(params, session)
        if _exists:
            return await update_changed_flag({"value": _exists}, 200, "get")
    spec = {}
    for i in accepted_fields:
        if params[i]:
            spec[i] = params[i]
    _url = "https://{vcenter_hostname}/rest/vcenter/deployment/upgrade?action=check".format(
        **params
    )
    async with session.post(_url, json={"spec": spec}) as resp:
        try:
            if resp.headers["Content-Type"] == "application/json":
                _json = await resp.json()
        except KeyError:
            _json = {}
        if ("check" == "create") and ("value" in _json):
            if type(_json["value"]) == dict:
                _id = list(_json["value"].values())[0]
            else:
                _id = _json["value"]
            _json = {"value": (await get_device_info(params, session, _url, _id))}
        return await update_changed_flag(_json, resp.status, "check")


async def _start(params, session):
    accepted_fields = [
        "auto_answer",
        "history",
        "psc",
        "source_appliance",
        "source_location",
        "vcsa_embedded",
    ]
    if "start" == "create":
        _exists = await exists(params, session)
        if _exists:
            return await update_changed_flag({"value": _exists}, 200, "get")
    spec = {}
    for i in accepted_fields:
        if params[i]:
            spec[i] = params[i]
    _url = "https://{vcenter_hostname}/rest/vcenter/deployment/upgrade?action=start".format(
        **params
    )
    async with session.post(_url, json={"spec": spec}) as resp:
        try:
            if resp.headers["Content-Type"] == "application/json":
                _json = await resp.json()
        except KeyError:
            _json = {}
        if ("start" == "create") and ("value" in _json):
            if type(_json["value"]) == dict:
                _id = list(_json["value"].values())[0]
            else:
                _id = _json["value"]
            _json = {"value": (await get_device_info(params, session, _url, _id))}
        return await update_changed_flag(_json, resp.status, "start")


if __name__ == "__main__":
    import asyncio

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
