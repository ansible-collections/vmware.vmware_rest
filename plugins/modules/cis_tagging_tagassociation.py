from __future__ import absolute_import, division, print_function

__metaclass__ = type
import socket
import json

DOCUMENTATION = "author:\n- Ansible VMware team\ndescription: Handle resource of type cis_tagging_tagassociation\nextends_documentation_fragment: []\nmodule: cis_tagging_tagassociation\nnotes:\n- Tested on vSphere 7.0\noptions:\n  object_id:\n    description:\n    - The identifier of the input object. Required with I(state=['detach', 'detach_multiple_tags_from_object',\n      'list_attachable_tags', 'attach', 'attach_multiple_tags_to_object', 'list_attached_tags'])\n    - 'Validate attributes are:'\n    - ' - C(id) (str): The identifier for a resource whose type is specified by {@link\n      #type}.'\n    - ' - C(type) (str): The type of resource being identified (for example {@code\n      com.acme.Person}). <p> {@term Services} that contain {@term operations} for\n      creating and deleting resources typically contain a {@term constant} specifying\n      the resource type for the resources being created and deleted. The API metamodel\n      metadata {@term services} include a {@term service} that allows retrieving all\n      the known resource types.'\n    type: dict\n  object_ids:\n    description:\n    - The identifiers of the input objects. Required with I(state=['detach_tag_from_multiple_objects',\n      'list_attached_tags_on_objects', 'attach_tag_to_multiple_objects'])\n    type: list\n  state:\n    choices:\n    - detach\n    - attach_tag_to_multiple_objects\n    - detach_multiple_tags_from_object\n    - list_attached_objects\n    - list_attachable_tags\n    - attach\n    - list_attached_objects_on_tags\n    - attach_multiple_tags_to_object\n    - detach_tag_from_multiple_objects\n    - list_attached_tags_on_objects\n    - list_attached_tags\n    description: []\n    type: str\n  tag_id:\n    description:\n    - The identifier of the input tag. Required with I(state=['detach', 'attach_tag_to_multiple_objects',\n      'list_attached_objects', 'attach', 'detach_tag_from_multiple_objects'])\n    type: str\n  tag_ids:\n    description:\n    - The identifiers of the input tags. Required with I(state=['detach_multiple_tags_from_object',\n      'list_attached_objects_on_tags', 'attach_multiple_tags_to_object'])\n    type: list\n  ~action:\n    choices:\n    - attach-tag-to-multiple-objects\n    description:\n    - ~action=attach-tag-to-multiple-objects Required with I(state=['list_attached_tags_on_objects',\n      'attach_tag_to_multiple_objects'])\n    type: str\nrequirements:\n- python >= 3.6\nshort_description: Handle resource of type cis_tagging_tagassociation\nversion_added: 1.0.0\n"
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
        "choices": ["attach-tag-to-multiple-objects"],
        "operationIds": [
            "attach_tag_to_multiple_objects",
            "list_attached_tags_on_objects",
        ],
    }
    argument_spec["tag_ids"] = {
        "type": "list",
        "operationIds": [
            "attach_multiple_tags_to_object",
            "detach_multiple_tags_from_object",
            "list_attached_objects_on_tags",
        ],
    }
    argument_spec["tag_id"] = {
        "type": "str",
        "operationIds": [
            "attach",
            "attach_tag_to_multiple_objects",
            "detach",
            "detach_tag_from_multiple_objects",
            "list_attached_objects",
        ],
    }
    argument_spec["state"] = {
        "type": "str",
        "choices": [
            "attach",
            "attach_multiple_tags_to_object",
            "attach_tag_to_multiple_objects",
            "detach",
            "detach_multiple_tags_from_object",
            "detach_tag_from_multiple_objects",
            "list_attachable_tags",
            "list_attached_objects",
            "list_attached_objects_on_tags",
            "list_attached_tags",
            "list_attached_tags_on_objects",
        ],
    }
    argument_spec["object_ids"] = {
        "type": "list",
        "operationIds": [
            "attach_tag_to_multiple_objects",
            "detach_tag_from_multiple_objects",
            "list_attached_tags_on_objects",
        ],
    }
    argument_spec["object_id"] = {
        "type": "dict",
        "operationIds": [
            "attach",
            "attach_multiple_tags_to_object",
            "detach",
            "detach_multiple_tags_from_object",
            "list_attachable_tags",
            "list_attached_tags",
        ],
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
    return "https://{vcenter_hostname}/rest/com/vmware/cis/tagging/tag-association".format(
        **params
    )


async def entry_point(module, session):
    func = globals()[("_" + module.params["state"])]
    return await func(module.params, session)


async def _attach(params, session):
    accepted_fields = ["object_id"]
    if "attach" == "create":
        _exists = await exists(params, session)
        if _exists:
            return await update_changed_flag({"value": _exists}, 200, "get")
    spec = {}
    for i in accepted_fields:
        if params[i]:
            spec[i] = params[i]
    _url = "https://{vcenter_hostname}/rest/com/vmware/cis/tagging/tag-association/id:{tag_id}?~action=attach".format(
        **params
    )
    async with session.post(_url, json={"spec": spec}) as resp:
        try:
            if resp.headers["Content-Type"] == "application/json":
                _json = await resp.json()
        except KeyError:
            _json = {}
        if (
            ("attach" == "create")
            and (resp.status in [200, 201])
            and ("value" in _json)
        ):
            if type(_json["value"]) == dict:
                _id = list(_json["value"].values())[0]
            else:
                _id = _json["value"]
            _json = {"value": (await get_device_info(params, session, _url, _id))}
        return await update_changed_flag(_json, resp.status, "attach")


async def _attach_multiple_tags_to_object(params, session):
    accepted_fields = ["object_id", "tag_ids"]
    if "attach_multiple_tags_to_object" == "create":
        _exists = await exists(params, session)
        if _exists:
            return await update_changed_flag({"value": _exists}, 200, "get")
    spec = {}
    for i in accepted_fields:
        if params[i]:
            spec[i] = params[i]
    _url = "https://{vcenter_hostname}/rest/com/vmware/cis/tagging/tag-association?~action=attach-multiple-tags-to-object".format(
        **params
    )
    async with session.post(_url, json={"spec": spec}) as resp:
        try:
            if resp.headers["Content-Type"] == "application/json":
                _json = await resp.json()
        except KeyError:
            _json = {}
        if (
            ("attach_multiple_tags_to_object" == "create")
            and (resp.status in [200, 201])
            and ("value" in _json)
        ):
            if type(_json["value"]) == dict:
                _id = list(_json["value"].values())[0]
            else:
                _id = _json["value"]
            _json = {"value": (await get_device_info(params, session, _url, _id))}
        return await update_changed_flag(
            _json, resp.status, "attach_multiple_tags_to_object"
        )


async def _attach_tag_to_multiple_objects(params, session):
    accepted_fields = ["object_ids"]
    if "attach_tag_to_multiple_objects" == "create":
        _exists = await exists(params, session)
        if _exists:
            return await update_changed_flag({"value": _exists}, 200, "get")
    spec = {}
    for i in accepted_fields:
        if params[i]:
            spec[i] = params[i]
    _url = "https://{vcenter_hostname}/rest/com/vmware/cis/tagging/tag-association/id:{tag_id}".format(
        **params
    )
    async with session.post(_url, json={"spec": spec}) as resp:
        try:
            if resp.headers["Content-Type"] == "application/json":
                _json = await resp.json()
        except KeyError:
            _json = {}
        if (
            ("attach_tag_to_multiple_objects" == "create")
            and (resp.status in [200, 201])
            and ("value" in _json)
        ):
            if type(_json["value"]) == dict:
                _id = list(_json["value"].values())[0]
            else:
                _id = _json["value"]
            _json = {"value": (await get_device_info(params, session, _url, _id))}
        return await update_changed_flag(
            _json, resp.status, "attach_tag_to_multiple_objects"
        )


async def _detach(params, session):
    accepted_fields = ["object_id"]
    if "detach" == "create":
        _exists = await exists(params, session)
        if _exists:
            return await update_changed_flag({"value": _exists}, 200, "get")
    spec = {}
    for i in accepted_fields:
        if params[i]:
            spec[i] = params[i]
    _url = "https://{vcenter_hostname}/rest/com/vmware/cis/tagging/tag-association/id:{tag_id}?~action=detach".format(
        **params
    )
    async with session.post(_url, json={"spec": spec}) as resp:
        try:
            if resp.headers["Content-Type"] == "application/json":
                _json = await resp.json()
        except KeyError:
            _json = {}
        if (
            ("detach" == "create")
            and (resp.status in [200, 201])
            and ("value" in _json)
        ):
            if type(_json["value"]) == dict:
                _id = list(_json["value"].values())[0]
            else:
                _id = _json["value"]
            _json = {"value": (await get_device_info(params, session, _url, _id))}
        return await update_changed_flag(_json, resp.status, "detach")


async def _detach_multiple_tags_from_object(params, session):
    accepted_fields = ["object_id", "tag_ids"]
    if "detach_multiple_tags_from_object" == "create":
        _exists = await exists(params, session)
        if _exists:
            return await update_changed_flag({"value": _exists}, 200, "get")
    spec = {}
    for i in accepted_fields:
        if params[i]:
            spec[i] = params[i]
    _url = "https://{vcenter_hostname}/rest/com/vmware/cis/tagging/tag-association?~action=detach-multiple-tags-from-object".format(
        **params
    )
    async with session.post(_url, json={"spec": spec}) as resp:
        try:
            if resp.headers["Content-Type"] == "application/json":
                _json = await resp.json()
        except KeyError:
            _json = {}
        if (
            ("detach_multiple_tags_from_object" == "create")
            and (resp.status in [200, 201])
            and ("value" in _json)
        ):
            if type(_json["value"]) == dict:
                _id = list(_json["value"].values())[0]
            else:
                _id = _json["value"]
            _json = {"value": (await get_device_info(params, session, _url, _id))}
        return await update_changed_flag(
            _json, resp.status, "detach_multiple_tags_from_object"
        )


async def _detach_tag_from_multiple_objects(params, session):
    accepted_fields = ["object_ids"]
    if "detach_tag_from_multiple_objects" == "create":
        _exists = await exists(params, session)
        if _exists:
            return await update_changed_flag({"value": _exists}, 200, "get")
    spec = {}
    for i in accepted_fields:
        if params[i]:
            spec[i] = params[i]
    _url = "https://{vcenter_hostname}/rest/com/vmware/cis/tagging/tag-association/id:{tag_id}?~action=detach-tag-from-multiple-objects".format(
        **params
    )
    async with session.post(_url, json={"spec": spec}) as resp:
        try:
            if resp.headers["Content-Type"] == "application/json":
                _json = await resp.json()
        except KeyError:
            _json = {}
        if (
            ("detach_tag_from_multiple_objects" == "create")
            and (resp.status in [200, 201])
            and ("value" in _json)
        ):
            if type(_json["value"]) == dict:
                _id = list(_json["value"].values())[0]
            else:
                _id = _json["value"]
            _json = {"value": (await get_device_info(params, session, _url, _id))}
        return await update_changed_flag(
            _json, resp.status, "detach_tag_from_multiple_objects"
        )


async def _list_attachable_tags(params, session):
    accepted_fields = ["object_id"]
    if "list_attachable_tags" == "create":
        _exists = await exists(params, session)
        if _exists:
            return await update_changed_flag({"value": _exists}, 200, "get")
    spec = {}
    for i in accepted_fields:
        if params[i]:
            spec[i] = params[i]
    _url = "https://{vcenter_hostname}/rest/com/vmware/cis/tagging/tag-association?~action=list-attachable-tags".format(
        **params
    )
    async with session.post(_url, json={"spec": spec}) as resp:
        try:
            if resp.headers["Content-Type"] == "application/json":
                _json = await resp.json()
        except KeyError:
            _json = {}
        if (
            ("list_attachable_tags" == "create")
            and (resp.status in [200, 201])
            and ("value" in _json)
        ):
            if type(_json["value"]) == dict:
                _id = list(_json["value"].values())[0]
            else:
                _id = _json["value"]
            _json = {"value": (await get_device_info(params, session, _url, _id))}
        return await update_changed_flag(_json, resp.status, "list_attachable_tags")


async def _list_attached_objects(params, session):
    _url = "https://{vcenter_hostname}/rest/com/vmware/cis/tagging/tag-association/id:{tag_id}?~action=list-attached-objects".format(
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
        return await update_changed_flag(_json, resp.status, "list_attached_objects")


async def _list_attached_objects_on_tags(params, session):
    accepted_fields = ["tag_ids"]
    if "list_attached_objects_on_tags" == "create":
        _exists = await exists(params, session)
        if _exists:
            return await update_changed_flag({"value": _exists}, 200, "get")
    spec = {}
    for i in accepted_fields:
        if params[i]:
            spec[i] = params[i]
    _url = "https://{vcenter_hostname}/rest/com/vmware/cis/tagging/tag-association?~action=list-attached-objects-on-tags".format(
        **params
    )
    async with session.post(_url, json={"spec": spec}) as resp:
        try:
            if resp.headers["Content-Type"] == "application/json":
                _json = await resp.json()
        except KeyError:
            _json = {}
        if (
            ("list_attached_objects_on_tags" == "create")
            and (resp.status in [200, 201])
            and ("value" in _json)
        ):
            if type(_json["value"]) == dict:
                _id = list(_json["value"].values())[0]
            else:
                _id = _json["value"]
            _json = {"value": (await get_device_info(params, session, _url, _id))}
        return await update_changed_flag(
            _json, resp.status, "list_attached_objects_on_tags"
        )


async def _list_attached_tags(params, session):
    accepted_fields = ["object_id"]
    if "list_attached_tags" == "create":
        _exists = await exists(params, session)
        if _exists:
            return await update_changed_flag({"value": _exists}, 200, "get")
    spec = {}
    for i in accepted_fields:
        if params[i]:
            spec[i] = params[i]
    _url = "https://{vcenter_hostname}/rest/com/vmware/cis/tagging/tag-association?~action=list-attached-tags".format(
        **params
    )
    async with session.post(_url, json={"spec": spec}) as resp:
        try:
            if resp.headers["Content-Type"] == "application/json":
                _json = await resp.json()
        except KeyError:
            _json = {}
        if (
            ("list_attached_tags" == "create")
            and (resp.status in [200, 201])
            and ("value" in _json)
        ):
            if type(_json["value"]) == dict:
                _id = list(_json["value"].values())[0]
            else:
                _id = _json["value"]
            _json = {"value": (await get_device_info(params, session, _url, _id))}
        return await update_changed_flag(_json, resp.status, "list_attached_tags")


async def _list_attached_tags_on_objects(params, session):
    accepted_fields = ["object_ids"]
    if "list_attached_tags_on_objects" == "create":
        _exists = await exists(params, session)
        if _exists:
            return await update_changed_flag({"value": _exists}, 200, "get")
    spec = {}
    for i in accepted_fields:
        if params[i]:
            spec[i] = params[i]
    _url = "https://{vcenter_hostname}/rest/com/vmware/cis/tagging/tag-association".format(
        **params
    )
    async with session.post(_url, json={"spec": spec}) as resp:
        try:
            if resp.headers["Content-Type"] == "application/json":
                _json = await resp.json()
        except KeyError:
            _json = {}
        if (
            ("list_attached_tags_on_objects" == "create")
            and (resp.status in [200, 201])
            and ("value" in _json)
        ):
            if type(_json["value"]) == dict:
                _id = list(_json["value"].values())[0]
            else:
                _id = _json["value"]
            _json = {"value": (await get_device_info(params, session, _url, _id))}
        return await update_changed_flag(
            _json, resp.status, "list_attached_tags_on_objects"
        )


if __name__ == "__main__":
    import asyncio

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
