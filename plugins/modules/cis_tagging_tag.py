from __future__ import absolute_import, division, print_function

__metaclass__ = type
import socket
import json

DOCUMENTATION = """
module: cis_tagging_tag
short_description: Handle resource of type cis_tagging_tag
description: Handle resource of type cis_tagging_tag
options:
  category_id:
    description:
    - The identifier of the input category. Required with I(state=['list_tags_for_category'])
    type: str
  create_spec:
    description:
    - Specification for the new tag to be created. Required with I(state=['create'])
    - 'Validate attributes are:'
    - ' - C(category_id) (str): The unique identifier of the parent category in which
      this tag will be created.'
    - ' - C(description) (str): The description of the tag.'
    - ' - C(name) (str): The display name of the tag. The name must be unique within
      its category.'
    - ' - C(tag_id) (str): The identifier of the tag. If specified, tag will be created
      with the specified identifier. This has to be of the tag ManagedObject Id format
      urn:vmomi:InventoryServiceTag:<id>:GLOBAL The <id> cannot contain special character
      :'
    type: dict
  state:
    choices:
    - add_to_used_by
    - create
    - delete
    - list_tags_for_category
    - list_used_tags
    - remove_from_used_by
    - revoke_propagating_permissions
    - update
    description: []
    type: str
  tag_id:
    description:
    - The identifier of the input tag. Required with I(state=['add_to_used_by', 'delete',
      'remove_from_used_by', 'revoke_propagating_permissions', 'update'])
    type: str
  update_spec:
    description:
    - Specification to update the tag. Required with I(state=['update'])
    - 'Validate attributes are:'
    - ' - C(description) (str): The description of the tag.'
    - ' - C(name) (str): The display name of the tag.'
    type: dict
  used_by_entity:
    description:
    - The name of the user to be removed from the {@link TagModel#usedBy} {@term set}.
      Required with I(state=['add_to_used_by', 'list_used_tags', 'remove_from_used_by'])
    type: str
  ~action:
    choices:
    - add-to-used-by
    - list-tags-for-category
    description:
    - ~action=list-tags-for-category Required with I(state=['add_to_used_by', 'list_tags_for_category'])
    type: str
author:
- Ansible VMware team
version_added: 1.0.0
requirements:
- python >= 3.6
"""
IN_QUERY_PARAMETER = ["~action"]
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
    argument_spec["~action"] = {
        "type": "str",
        "choices": ["add-to-used-by", "list-tags-for-category"],
        "operationIds": ["add_to_used_by", "list_tags_for_category"],
    }
    argument_spec["used_by_entity"] = {
        "type": "str",
        "operationIds": ["add_to_used_by", "list_used_tags", "remove_from_used_by"],
    }
    argument_spec["update_spec"] = {"type": "dict", "operationIds": ["update"]}
    argument_spec["tag_id"] = {
        "type": "str",
        "operationIds": [
            "add_to_used_by",
            "delete",
            "remove_from_used_by",
            "revoke_propagating_permissions",
            "update",
        ],
    }
    argument_spec["state"] = {
        "type": "str",
        "choices": [
            "add_to_used_by",
            "create",
            "delete",
            "list_tags_for_category",
            "list_used_tags",
            "remove_from_used_by",
            "revoke_propagating_permissions",
            "update",
        ],
    }
    argument_spec["create_spec"] = {"type": "dict", "operationIds": ["create"]}
    argument_spec["category_id"] = {
        "type": "str",
        "operationIds": ["list_tags_for_category"],
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
    return "https://{vcenter_hostname}/rest/com/vmware/cis/tagging/tag".format(**params)


async def entry_point(module, session):
    func = globals()[("_" + module.params["state"])]
    return await func(module.params, session)


async def _add_to_used_by(params, session):
    accepted_fields = ["used_by_entity"]
    if "add_to_used_by" == "create":
        _exists = await exists(params, session)
        if _exists:
            return await update_changed_flag({"value": _exists}, 200, "get")
    spec = {}
    for i in accepted_fields:
        if params[i]:
            spec[i] = params[i]
    _url = "https://{vcenter_hostname}/rest/com/vmware/cis/tagging/tag/id:{tag_id}".format(
        **params
    )
    async with session.post(_url, json={"spec": spec}) as resp:
        try:
            if resp.headers["Content-Type"] == "application/json":
                _json = await resp.json()
        except KeyError:
            _json = {}
        if (
            ("add_to_used_by" == "create")
            and (resp.status in [200, 201])
            and ("value" in _json)
        ):
            if type(_json["value"]) == dict:
                _id = list(_json["value"].values())[0]
            else:
                _id = _json["value"]
            _json = {"value": (await get_device_info(params, session, _url, _id))}
        return await update_changed_flag(_json, resp.status, "add_to_used_by")


async def _create(params, session):
    accepted_fields = ["create_spec"]
    if "create" == "create":
        _exists = await exists(params, session)
        if _exists:
            return await update_changed_flag({"value": _exists}, 200, "get")
    spec = {}
    for i in accepted_fields:
        if params[i]:
            spec[i] = params[i]
    _url = "https://{vcenter_hostname}/rest/com/vmware/cis/tagging/tag".format(**params)
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
    _url = "https://{vcenter_hostname}/rest/com/vmware/cis/tagging/tag/id:{tag_id}".format(
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


async def _list_tags_for_category(params, session):
    _url = "https://{vcenter_hostname}/rest/com/vmware/cis/tagging/tag/id:{category_id}".format(
        **params
    ) + gen_args(
        params, IN_QUERY_PARAMETER
    )
    async with session.post(_url) as resp:
        try:
            if resp.headers["Content-Type"] == "application/json":
                _json = await resp.json()
        except KeyError:
            _json = {}
        return await update_changed_flag(_json, resp.status, "list_tags_for_category")


async def _list_used_tags(params, session):
    accepted_fields = ["used_by_entity"]
    if "list_used_tags" == "create":
        _exists = await exists(params, session)
        if _exists:
            return await update_changed_flag({"value": _exists}, 200, "get")
    spec = {}
    for i in accepted_fields:
        if params[i]:
            spec[i] = params[i]
    _url = "https://{vcenter_hostname}/rest/com/vmware/cis/tagging/tag?~action=list-used-tags".format(
        **params
    )
    async with session.post(_url, json={"spec": spec}) as resp:
        try:
            if resp.headers["Content-Type"] == "application/json":
                _json = await resp.json()
        except KeyError:
            _json = {}
        if (
            ("list_used_tags" == "create")
            and (resp.status in [200, 201])
            and ("value" in _json)
        ):
            if type(_json["value"]) == dict:
                _id = list(_json["value"].values())[0]
            else:
                _id = _json["value"]
            _json = {"value": (await get_device_info(params, session, _url, _id))}
        return await update_changed_flag(_json, resp.status, "list_used_tags")


async def _remove_from_used_by(params, session):
    accepted_fields = ["used_by_entity"]
    if "remove_from_used_by" == "create":
        _exists = await exists(params, session)
        if _exists:
            return await update_changed_flag({"value": _exists}, 200, "get")
    spec = {}
    for i in accepted_fields:
        if params[i]:
            spec[i] = params[i]
    _url = "https://{vcenter_hostname}/rest/com/vmware/cis/tagging/tag/id:{tag_id}?~action=remove-from-used-by".format(
        **params
    )
    async with session.post(_url, json={"spec": spec}) as resp:
        try:
            if resp.headers["Content-Type"] == "application/json":
                _json = await resp.json()
        except KeyError:
            _json = {}
        if (
            ("remove_from_used_by" == "create")
            and (resp.status in [200, 201])
            and ("value" in _json)
        ):
            if type(_json["value"]) == dict:
                _id = list(_json["value"].values())[0]
            else:
                _id = _json["value"]
            _json = {"value": (await get_device_info(params, session, _url, _id))}
        return await update_changed_flag(_json, resp.status, "remove_from_used_by")


async def _revoke_propagating_permissions(params, session):
    _url = "https://{vcenter_hostname}/rest/com/vmware/cis/tagging/tag/id:{tag_id}?~action=revoke-propagating-permissions".format(
        **params
    ) + gen_args(
        params, IN_QUERY_PARAMETER
    )
    async with session.post(_url) as resp:
        try:
            if resp.headers["Content-Type"] == "application/json":
                _json = await resp.json()
        except KeyError:
            _json = {}
        return await update_changed_flag(
            _json, resp.status, "revoke_propagating_permissions"
        )


async def _update(params, session):
    accepted_fields = ["update_spec"]
    if "update" == "create":
        _exists = await exists(params, session)
        if _exists:
            return await update_changed_flag({"value": _exists}, 200, "get")
    spec = {}
    for i in accepted_fields:
        if params[i]:
            spec[i] = params[i]
    _url = "https://{vcenter_hostname}/rest/com/vmware/cis/tagging/tag/id:{tag_id}".format(
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
