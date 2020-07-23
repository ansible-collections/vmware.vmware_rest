from __future__ import absolute_import, division, print_function

__metaclass__ = type
import socket
import json

DOCUMENTATION = "author:\n- Ansible VMware team\ndescription: Handle resource of type stats_rsrcaddrs\nextends_documentation_fragment: []\nmodule: stats_rsrcaddrs_info\nnotes:\n- Tested on vSphere 7.0\noptions:\n  id:\n    description:\n    - 'Resource Address ID.\n\n      The parameter must be an identifier for the resource type: vstats.model.RsrcAddr.\n      Required with I(state=[''get''])'\n    type: str\n  page:\n    description:\n    - 'The ResourceAddresses.FilterSpec.page field is used to retrieve paged data\n      for large result sets. It is an opaque paging token obtained from a prior call\n      to the ResourceAddresses.list API. Warning: This attribute is available as Technology\n      Preview. These are early access APIs provided to test, automate and provide\n      feedback on the feature. Since this can change based on feedback, VMware does\n      not guarantee backwards compatibility and recommends against using them in production\n      environments. Some Technology Preview APIs might only be applicable to specific\n      environments.\n\n      when set a follow up page in a paged result set will be delivered.'\n    type: str\n  resources:\n    description:\n    - \"Resources to include in the query. Each resource is specified through a composite\\\n      \\ string that follows the following format. \\n type.<resource type>[.<scheme>]=<resource\\\n      \\ id> \\n\\n resource type specifies the type of resource for example VM, VCPU\\\n      \\ etc. \\n\\n scheme is an optional element to disambiguate the resource as needed\\\n      \\ for example to differentiate managed object id from uuid. \\n\\n resource id\\\n      \\ is the unique resource identifier value for example: vm-41 \\n\\n Example values\\\n      \\ include: type.VM=vm-41, type.VCPU=1, type.VM.moid=vm-41\\n. Warning: This attribute\\\n      \\ is available as Technology Preview. These are early access APIs provided to\\\n      \\ test, automate and provide feedback on the feature. Since this can change\\\n      \\ based on feedback, VMware does not guarantee backwards compatibility and recommends\\\n      \\ against using them in production environments. Some Technology Preview APIs\\\n      \\ might only be applicable to specific environments.\\nWhen left unset the result\\\n      \\ will not be filtered for specific resources.\"\n    type: list\n  types:\n    description:\n    - 'List of Resource types. Warning: This attribute is available as Technology\n      Preview. These are early access APIs provided to test, automate and provide\n      feedback on the feature. Since this can change based on feedback, VMware does\n      not guarantee backwards compatibility and recommends against using them in production\n      environments. Some Technology Preview APIs might only be applicable to specific\n      environments.\n\n      When unset the result will not be filtered by resource types.\n\n      When clients pass a value of this structure as a parameter, the field must contain\n      identifiers for the resource type: vstats.model.RsrcType. When operations return\n      a value of this structure as a result, the field will contain identifiers for\n      the resource type: vstats.model.RsrcType.'\n    type: list\nrequirements:\n- python >= 3.6\nshort_description: Handle resource of type stats_rsrcaddrs\nversion_added: 1.0.0\n"
IN_QUERY_PARAMETER = ["types", "resources", "page"]
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
    argument_spec["types"] = {"type": "list", "operationIds": ["list"]}
    argument_spec["resources"] = {"type": "list", "operationIds": ["list"]}
    argument_spec["page"] = {"type": "str", "operationIds": ["list"]}
    argument_spec["id"] = {"type": "str", "operationIds": ["get"]}
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
    if params["id"]:
        return "https://{vcenter_hostname}/rest/api/stats/rsrc-addrs/{id}".format(
            **params
        ) + gen_args(params, IN_QUERY_PARAMETER)
    else:
        return "https://{vcenter_hostname}/rest/api/stats/rsrc-addrs".format(
            **params
        ) + gen_args(params, IN_QUERY_PARAMETER)


async def entry_point(module, session):
    async with session.get(url(module.params)) as resp:
        _json = await resp.json()
        return await update_changed_flag(_json, resp.status, "get")


if __name__ == "__main__":
    import asyncio

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
