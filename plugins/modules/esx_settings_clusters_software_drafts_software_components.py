from __future__ import absolute_import, division, print_function

__metaclass__ = type
import socket
import json

DOCUMENTATION = "author:\n- Ansible VMware team\ndescription: Handle resource of type esx_settings_clusters_software_drafts_software_components\nextends_documentation_fragment: []\nmodule: esx_settings_clusters_software_drafts_software_components\nnotes:\n- Tested on vSphere 7.0\noptions:\n  cluster:\n    description:\n    - Identifier of the cluster.\n    type: str\n  component:\n    description:\n    - Identifier of the component. Required with I(state=['set', 'delete'])\n    type: str\n  draft:\n    description:\n    - Identifier of the working copy document.\n    type: str\n  state:\n    choices:\n    - set\n    - update\n    - delete\n    description: []\n    type: str\nrequirements:\n- python >= 3.6\nshort_description: Handle resource of type esx_settings_clusters_software_drafts_software_components\nversion_added: 1.0.0\n"
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
    argument_spec["state"] = {"type": "str", "choices": ["delete", "set", "update"]}
    argument_spec["draft"] = {
        "type": "str",
        "operationIds": ["delete", "set", "update"],
    }
    argument_spec["component"] = {"type": "str", "operationIds": ["delete", "set"]}
    argument_spec["cluster"] = {
        "type": "str",
        "operationIds": ["delete", "set", "update"],
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
    return "https://{vcenter_hostname}/rest/api/esx/settings/clusters/{cluster}/software/drafts/{draft}/software/components".format(
        **params
    )


async def entry_point(module, session):
    func = globals()[("_" + module.params["state"])]
    return await func(module.params, session)


async def _delete(params, session):
    _url = "https://{vcenter_hostname}/rest/api/esx/settings/clusters/{cluster}/software/drafts/{draft}/software/components/{component}".format(
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


async def _set(params, session):
    _url = "https://{vcenter_hostname}/rest/api/esx/settings/clusters/{cluster}/software/drafts/{draft}/software/components/{component}".format(
        **params
    ) + gen_args(
        params, IN_QUERY_PARAMETER
    )
    async with session.put(_url) as resp:
        try:
            if resp.headers["Content-Type"] == "application/json":
                _json = await resp.json()
        except KeyError:
            _json = {}
        return await update_changed_flag(_json, resp.status, "set")


async def _update(params, session):
    _url = "https://{vcenter_hostname}/rest/api/esx/settings/clusters/{cluster}/software/drafts/{draft}/software/components".format(
        **params
    ) + gen_args(
        params, IN_QUERY_PARAMETER
    )
    async with session.patch(_url) as resp:
        try:
            if resp.headers["Content-Type"] == "application/json":
                _json = await resp.json()
        except KeyError:
            _json = {}
        return await update_changed_flag(_json, resp.status, "update")


if __name__ == "__main__":
    import asyncio

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
