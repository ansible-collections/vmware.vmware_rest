from __future__ import absolute_import, division, print_function

__metaclass__ = type
import socket
import json

DOCUMENTATION = "author:\n- Ansible VMware team\ndescription: Handle resource of type vcenter_guest_customizationspecs\nextends_documentation_fragment: []\nmodule: vcenter_guest_customizationspecs_info\nnotes:\n- Tested on vSphere 7.0\noptions:\n  filter.OS_type:\n    choices:\n    - WINDOWS\n    - LINUX\n    description:\n    - The CustomizationSpecs.OsType enumerated type defines the types of guest operating\n      systems for which guest customization is supported.\n    type: str\n  filter.names:\n    description:\n    - 'Names that guest customization specifications must have to match the filter\n      (see CustomizationSpecs.Summary.name).\n\n      If unset or empty, guest customization specifications with any name match the\n      filter.\n\n      When clients pass a value of this structure as a parameter, the field must contain\n      identifiers for the resource type: vcenter.guest.CustomizationSpec. When operations\n      return a value of this structure as a result, the field will contain identifiers\n      for the resource type: vcenter.guest.CustomizationSpec.'\n    type: list\n  name:\n    description:\n    - 'The name of the customization specification.\n\n      The parameter must be an identifier for the resource type: vcenter.guest.CustomizationSpec.\n      Required with I(state=[''get''])'\n    type: str\nrequirements:\n- python >= 3.6\nshort_description: Handle resource of type vcenter_guest_customizationspecs\nversion_added: 1.0.0\n"
IN_QUERY_PARAMETER = ["filter.names", "filter.OS_type"]
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
    argument_spec["name"] = {"type": "str", "operationIds": ["get"]}
    argument_spec["filter.names"] = {"type": "list", "operationIds": ["list"]}
    argument_spec["filter.OS_type"] = {
        "type": "str",
        "choices": ["LINUX", "WINDOWS"],
        "operationIds": ["list"],
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
    if params["name"]:
        return "https://{vcenter_hostname}/rest/vcenter/guest/customization-specs/{name}".format(
            **params
        ) + gen_args(
            params, IN_QUERY_PARAMETER
        )
    else:
        return "https://{vcenter_hostname}/rest/vcenter/guest/customization-specs".format(
            **params
        ) + gen_args(
            params, IN_QUERY_PARAMETER
        )


async def entry_point(module, session):
    async with session.get(url(module.params)) as resp:
        _json = await resp.json()
        return await update_changed_flag(_json, resp.status, "get")


if __name__ == "__main__":
    import asyncio

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
