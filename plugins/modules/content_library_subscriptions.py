from __future__ import absolute_import, division, print_function

__metaclass__ = type
import socket
import json

DOCUMENTATION = "author:\n- Ansible VMware team\ndescription: Handle resource of type content_library_subscriptions\nextends_documentation_fragment: []\nmodule: content_library_subscriptions\nnotes:\n- Tested on vSphere 7.0\noptions:\n  client_token:\n    description:\n    - 'A unique token generated on the client for each creation request. The token\n      should be a universally unique identifier (UUID), for example: {@code b8a2a2e3-2314-43cd-a871-6ede0f429751}.\n      This token can be used to guarantee idempotent creation.'\n    type: str\n  library:\n    description:\n    - Identifier of the published library.\n    type: str\n  state:\n    choices:\n    - update\n    - delete\n    - create\n    description: []\n    type: str\n  subscribed_library:\n    description:\n    - Specification for the subscribed library to be associated with the subscription.\n      Required with I(state=['create'])\n    - 'Validate attributes are:'\n    - ' - C(location) (str): The {@name Location} defines the location of subscribed\n      library relative to the published library.'\n    - ' - C(new_subscribed_library) (dict): Specification for creating a new subscribed\n      library associated with the subscription.'\n    - ' - C(placement) (dict): Placement specification for the virtual machine template\n      library items on the subscribed library.'\n    - ' - C(subscribed_library) (str): Identifier of the existing subscribed library\n      to associate with the subscription. Only the subscribed libraries for which\n      {@link SubscriptionInfo#subscriptionUrl} property is set to the {@link PublishInfo#publishUrl}\n      of the published library can be associated with the subscription.'\n    - ' - C(target) (str): The {@name Target} defines the options related to the target\n      subscribed library which will be associated with the subscription.'\n    - ' - C(vcenter) (dict): Specification for the subscribed library''s vCenter Server\n      instance.'\n    type: dict\n  subscribed_library_placement:\n    description:\n    - Placement specification for the virtual machine template items of the subscribed\n      library. Updating this information will only affect new or updated items, existing\n      items will not be moved. The entire placement configuration of the subscribed\n      library will replaced by the new specification.\n    - 'Validate attributes are:'\n    - ' - C(cluster) (str): Cluster onto which the virtual machine template should\n      be placed. If {@name #cluster} and {@name #resourcePool} are both specified,\n      {@name #resourcePool} must belong to {@name #cluster}. If {@name #cluster} and\n      {@name #host} are both specified, {@name #host} must be a member of {@name #cluster}.\n      If {@name #resourcePool} or {@name #host} is specified, it is recommended that\n      this {@term field} be {@term unset}.'\n    - ' - C(folder) (str): Virtual machine folder into which the virtual machine template\n      should be placed.'\n    - ' - C(host) (str): Host onto which the virtual machine template should be placed.\n      If {@name #host} and {@name #resourcePool} are both specified, {@name #resourcePool}\n      must belong to {@name #host}. If {@name #host} and {@name #cluster} are both\n      specified, {@name #host} must be a member of {@name #cluster}.'\n    - ' - C(network) (str): Network that backs the virtual Ethernet adapters in the\n      virtual machine template.'\n    - ' - C(resource_pool) (str): Resource pool into which the virtual machine template\n      should be placed.'\n    type: dict\n  subscribed_library_vcenter:\n    description:\n    - Specification for the subscribed library's vCenter Server instance.\n    - 'Validate attributes are:'\n    - ' - C(hostname) (str): The hostname of the subscribed library''s vCenter Server.'\n    - ' - C(https_port) (int): The HTTPS port of the vCenter Server instance where\n      the subscribed library exists.'\n    type: dict\n  subscription:\n    description:\n    - subscription identifier. Required with I(state=['update', 'delete'])\n    type: str\nrequirements:\n- python >= 3.6\nshort_description: Handle resource of type content_library_subscriptions\nversion_added: 1.0.0\n"
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
    argument_spec["subscription"] = {
        "type": "str",
        "operationIds": ["delete", "update"],
    }
    argument_spec["subscribed_library_vcenter"] = {
        "type": "dict",
        "operationIds": ["update"],
    }
    argument_spec["subscribed_library_placement"] = {
        "type": "dict",
        "operationIds": ["update"],
    }
    argument_spec["subscribed_library"] = {"type": "dict", "operationIds": ["create"]}
    argument_spec["state"] = {"type": "str", "choices": ["create", "delete", "update"]}
    argument_spec["library"] = {
        "type": "str",
        "operationIds": ["create", "delete", "update"],
    }
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
    return "https://{vcenter_hostname}/rest/com/vmware/content/library/subscriptions".format(
        **params
    )


async def entry_point(module, session):
    func = globals()[("_" + module.params["state"])]
    return await func(module.params, session)


async def _create(params, session):
    accepted_fields = ["client_token", "subscribed_library"]
    if "create" == "create":
        _exists = await exists(params, session)
        if _exists:
            return await update_changed_flag({"value": _exists}, 200, "get")
    spec = {}
    for i in accepted_fields:
        if params[i]:
            spec[i] = params[i]
    _url = "https://{vcenter_hostname}/rest/com/vmware/content/library/subscriptions/id:{library}".format(
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
    accepted_fields = ["subscription"]
    if "delete" == "create":
        _exists = await exists(params, session)
        if _exists:
            return await update_changed_flag({"value": _exists}, 200, "get")
    spec = {}
    for i in accepted_fields:
        if params[i]:
            spec[i] = params[i]
    _url = "https://{vcenter_hostname}/rest/com/vmware/content/library/subscriptions/id:{library}?~action=delete".format(
        **params
    )
    async with session.post(_url, json={"spec": spec}) as resp:
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


async def _update(params, session):
    accepted_fields = [
        "subscribed_library_placement",
        "subscribed_library_vcenter",
        "subscription",
    ]
    if "update" == "create":
        _exists = await exists(params, session)
        if _exists:
            return await update_changed_flag({"value": _exists}, 200, "get")
    spec = {}
    for i in accepted_fields:
        if params[i]:
            spec[i] = params[i]
    _url = "https://{vcenter_hostname}/rest/com/vmware/content/library/subscriptions/id:{library}".format(
        **params
    )
    async with session.patch(_url, json={"spec": spec}) as resp:
        try:
            if resp.headers["Content-Type"] == "application/json":
                _json = await resp.json()
        except KeyError:
            _json = {}
        if (
            ("update" == "create")
            and (resp.status in [200, 201])
            and ("value" in _json)
        ):
            if type(_json["value"]) == dict:
                _id = list(_json["value"].values())[0]
            else:
                _id = _json["value"]
            _json = {"value": (await get_device_info(params, session, _url, _id))}
        return await update_changed_flag(_json, resp.status, "update")


if __name__ == "__main__":
    import asyncio

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
