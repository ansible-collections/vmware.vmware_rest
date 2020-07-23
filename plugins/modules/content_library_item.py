from __future__ import absolute_import, division, print_function

__metaclass__ = type
import socket
import json

DOCUMENTATION = "author:\n- Ansible VMware team\ndescription: Handle resource of type content_library_item\nextends_documentation_fragment: []\nmodule: content_library_item\nnotes:\n- Tested on vSphere 7.0\noptions:\n  cached:\n    description:\n    - Whether the item is cached. Possible values are 'true' or 'false'. See {@link\n      ItemModel#cached}.\n    type: bool\n  client_token:\n    description:\n    - 'A unique token generated on the client for each copy request. The token should\n      be a universally unique identifier (UUID), for example: {@code b8a2a2e3-2314-43cd-a871-6ede0f429751}.\n      This token can be used to guarantee idempotent copy.'\n    type: str\n  create_spec:\n    description:\n    - Specification that defines the properties of the new library item. Required\n      with I(state=['create'])\n    - 'Validate attributes are:'\n    - ' - C(cached) (bool): The status that indicates whether the library item is\n      on disk or not. The library item is cached when all its files are on disk.'\n    - ' - C(content_version) (str): The latest version of the file content list of\n      this library item.'\n    - ' - C(creation_time) (str): The date and time when this library item was created.'\n    - ' - C(description) (str): A human-readable description for this library item.'\n    - ' - C(id) (str): A unique identifier for this library item.'\n    - ' - C(last_modified_time) (str): The date and time when the metadata for this\n      library item was last changed. <p> This {@term field} is affected by changes\n      to the properties or file content of this item. It is not modified by changes\n      to the tags of the item, or by changes to the library which owns this item.'\n    - ' - C(last_sync_time) (str): The date and time when this library item was last\n      synchronized. <p> This {@term field} is updated every time a synchronization\n      is triggered on the library item, including when a synchronization is triggered\n      on the library to which this item belongs. The value is {@term unset} for a\n      library item that belongs to a local library.'\n    - ' - C(library_id) (str): The identifier of the {@link LibraryModel} to which\n      this item belongs.'\n    - ' - C(metadata_version) (str): A version number for the metadata of this library\n      item. <p> This value is incremented with each change to the metadata of this\n      item. Changes to name, description, and so on will increment this value. The\n      value is not incremented by changes to the content or tags of the item or the\n      library which owns it.'\n    - ' - C(name) (str): A human-readable name for this library item. <p> The name\n      may not be {@term unset} or an empty string. The name does not have to be unique,\n      even within the same library.'\n    - ' - C(size) (int): The library item size, in bytes. The size is the sum of the\n      size used on the storage backing for all the files in the item. When the library\n      item is not cached, the size is 0.'\n    - ' - C(source_id) (str): The identifier of the {@link ItemModel} to which this\n      item is synchronized to if the item belongs to a subscribed library. The value\n      is {@term unset} for a library item that belongs to a local library.'\n    - ' - C(type) (str): An optional type identifier which indicates the type adapter\n      plugin to use. <p> This {@term field} may be set to a non-empty string value\n      that corresponds to an identifier supported by a type adapter plugin present\n      in the Content Library Service. A type adapter plugin, if present for the specified\n      type, can provide additional information and services around the item content.\n      A type adapter can guide the upload process by creating file entries that are\n      in need of being uploaded to complete an item. <p> The types and plugins supported\n      by the Content Library Service can be queried using the {@link Type} {@term\n      service}.'\n    - ' - C(version) (str): A version number that is updated on metadata changes.\n      This value is used to validate update requests to provide optimistic concurrency\n      of changes. <p> This value represents a number that is incremented every time\n      library item properties, such as name or description, are changed. It is not\n      incremented by changes to the file content of the library item, including adding\n      or removing files. It is also not affected by tagging the library item.'\n    type: dict\n  destination_create_spec:\n    description:\n    - Specification for the new library item to be created. Required with I(state=['copy'])\n    - 'Validate attributes are:'\n    - ' - C(cached) (bool): The status that indicates whether the library item is\n      on disk or not. The library item is cached when all its files are on disk.'\n    - ' - C(content_version) (str): The latest version of the file content list of\n      this library item.'\n    - ' - C(creation_time) (str): The date and time when this library item was created.'\n    - ' - C(description) (str): A human-readable description for this library item.'\n    - ' - C(id) (str): A unique identifier for this library item.'\n    - ' - C(last_modified_time) (str): The date and time when the metadata for this\n      library item was last changed. <p> This {@term field} is affected by changes\n      to the properties or file content of this item. It is not modified by changes\n      to the tags of the item, or by changes to the library which owns this item.'\n    - ' - C(last_sync_time) (str): The date and time when this library item was last\n      synchronized. <p> This {@term field} is updated every time a synchronization\n      is triggered on the library item, including when a synchronization is triggered\n      on the library to which this item belongs. The value is {@term unset} for a\n      library item that belongs to a local library.'\n    - ' - C(library_id) (str): The identifier of the {@link LibraryModel} to which\n      this item belongs.'\n    - ' - C(metadata_version) (str): A version number for the metadata of this library\n      item. <p> This value is incremented with each change to the metadata of this\n      item. Changes to name, description, and so on will increment this value. The\n      value is not incremented by changes to the content or tags of the item or the\n      library which owns it.'\n    - ' - C(name) (str): A human-readable name for this library item. <p> The name\n      may not be {@term unset} or an empty string. The name does not have to be unique,\n      even within the same library.'\n    - ' - C(size) (int): The library item size, in bytes. The size is the sum of the\n      size used on the storage backing for all the files in the item. When the library\n      item is not cached, the size is 0.'\n    - ' - C(source_id) (str): The identifier of the {@link ItemModel} to which this\n      item is synchronized to if the item belongs to a subscribed library. The value\n      is {@term unset} for a library item that belongs to a local library.'\n    - ' - C(type) (str): An optional type identifier which indicates the type adapter\n      plugin to use. <p> This {@term field} may be set to a non-empty string value\n      that corresponds to an identifier supported by a type adapter plugin present\n      in the Content Library Service. A type adapter plugin, if present for the specified\n      type, can provide additional information and services around the item content.\n      A type adapter can guide the upload process by creating file entries that are\n      in need of being uploaded to complete an item. <p> The types and plugins supported\n      by the Content Library Service can be queried using the {@link Type} {@term\n      service}.'\n    - ' - C(version) (str): A version number that is updated on metadata changes.\n      This value is used to validate update requests to provide optimistic concurrency\n      of changes. <p> This value represents a number that is incremented every time\n      library item properties, such as name or description, are changed. It is not\n      incremented by changes to the file content of the library item, including adding\n      or removing files. It is also not affected by tagging the library item.'\n    type: dict\n  force_sync_content:\n    description:\n    - Whether to synchronize file content as well as metadata. This {@term parameter}\n      applies only if the subscription is on-demand. Required with I(state=['publish'])\n    type: bool\n  library_id:\n    description:\n    - The identifier of the library containing the item. See {@link ItemModel#libraryId}.\n    type: str\n  library_item_id:\n    description:\n    - Identifier of the library item to update. Required with I(state=['update', 'delete',\n      'publish'])\n    type: str\n  name:\n    description:\n    - The name of the library item. The name is case-insensitive. See {@link ItemModel#name}.\n    type: str\n  source_id:\n    description:\n    - The identifier of the library item as reported by the publisher. See {@link\n      ItemModel#sourceId}.\n    type: str\n  source_library_item_id:\n    description:\n    - Identifier of the existing library item from which the content will be copied.\n      Required with I(state=['copy'])\n    type: str\n  state:\n    choices:\n    - update\n    - copy\n    - delete\n    - create\n    - publish\n    - find\n    description: []\n    type: str\n  subscriptions:\n    description:\n    - The list of subscriptions to publish this library item to.\n    type: list\n  type:\n    description:\n    - The type of the library item. The type is case-insensitive. See {@link ItemModel#type}.\n    type: str\n  update_spec:\n    description:\n    - Specification of the properties to set. Required with I(state=['update'])\n    - 'Validate attributes are:'\n    - ' - C(cached) (bool): The status that indicates whether the library item is\n      on disk or not. The library item is cached when all its files are on disk.'\n    - ' - C(content_version) (str): The latest version of the file content list of\n      this library item.'\n    - ' - C(creation_time) (str): The date and time when this library item was created.'\n    - ' - C(description) (str): A human-readable description for this library item.'\n    - ' - C(id) (str): A unique identifier for this library item.'\n    - ' - C(last_modified_time) (str): The date and time when the metadata for this\n      library item was last changed. <p> This {@term field} is affected by changes\n      to the properties or file content of this item. It is not modified by changes\n      to the tags of the item, or by changes to the library which owns this item.'\n    - ' - C(last_sync_time) (str): The date and time when this library item was last\n      synchronized. <p> This {@term field} is updated every time a synchronization\n      is triggered on the library item, including when a synchronization is triggered\n      on the library to which this item belongs. The value is {@term unset} for a\n      library item that belongs to a local library.'\n    - ' - C(library_id) (str): The identifier of the {@link LibraryModel} to which\n      this item belongs.'\n    - ' - C(metadata_version) (str): A version number for the metadata of this library\n      item. <p> This value is incremented with each change to the metadata of this\n      item. Changes to name, description, and so on will increment this value. The\n      value is not incremented by changes to the content or tags of the item or the\n      library which owns it.'\n    - ' - C(name) (str): A human-readable name for this library item. <p> The name\n      may not be {@term unset} or an empty string. The name does not have to be unique,\n      even within the same library.'\n    - ' - C(size) (int): The library item size, in bytes. The size is the sum of the\n      size used on the storage backing for all the files in the item. When the library\n      item is not cached, the size is 0.'\n    - ' - C(source_id) (str): The identifier of the {@link ItemModel} to which this\n      item is synchronized to if the item belongs to a subscribed library. The value\n      is {@term unset} for a library item that belongs to a local library.'\n    - ' - C(type) (str): An optional type identifier which indicates the type adapter\n      plugin to use. <p> This {@term field} may be set to a non-empty string value\n      that corresponds to an identifier supported by a type adapter plugin present\n      in the Content Library Service. A type adapter plugin, if present for the specified\n      type, can provide additional information and services around the item content.\n      A type adapter can guide the upload process by creating file entries that are\n      in need of being uploaded to complete an item. <p> The types and plugins supported\n      by the Content Library Service can be queried using the {@link Type} {@term\n      service}.'\n    - ' - C(version) (str): A version number that is updated on metadata changes.\n      This value is used to validate update requests to provide optimistic concurrency\n      of changes. <p> This value represents a number that is incremented every time\n      library item properties, such as name or description, are changed. It is not\n      incremented by changes to the file content of the library item, including adding\n      or removing files. It is also not affected by tagging the library item.'\n    type: dict\n  ~action:\n    choices:\n    - copy\n    description:\n    - ~action=copy Required with I(state=['publish', 'copy'])\n    type: str\nrequirements:\n- python >= 3.6\nshort_description: Handle resource of type content_library_item\nversion_added: 1.0.0\n"
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
        "choices": ["copy"],
        "operationIds": ["copy", "publish"],
    }
    argument_spec["update_spec"] = {"type": "dict", "operationIds": ["update"]}
    argument_spec["type"] = {"type": "str", "operationIds": ["find"]}
    argument_spec["subscriptions"] = {"type": "list", "operationIds": ["publish"]}
    argument_spec["state"] = {
        "type": "str",
        "choices": ["copy", "create", "delete", "find", "publish", "update"],
    }
    argument_spec["source_library_item_id"] = {"type": "str", "operationIds": ["copy"]}
    argument_spec["source_id"] = {"type": "str", "operationIds": ["find"]}
    argument_spec["name"] = {"type": "str", "operationIds": ["find"]}
    argument_spec["library_item_id"] = {
        "type": "str",
        "operationIds": ["delete", "publish", "update"],
    }
    argument_spec["library_id"] = {"type": "str", "operationIds": ["find"]}
    argument_spec["force_sync_content"] = {"type": "bool", "operationIds": ["publish"]}
    argument_spec["destination_create_spec"] = {
        "type": "dict",
        "operationIds": ["copy"],
    }
    argument_spec["create_spec"] = {"type": "dict", "operationIds": ["create"]}
    argument_spec["client_token"] = {"type": "str", "operationIds": ["copy", "create"]}
    argument_spec["cached"] = {"type": "bool", "operationIds": ["find"]}
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
    return "https://{vcenter_hostname}/rest/com/vmware/content/library/item".format(
        **params
    )


async def entry_point(module, session):
    func = globals()[("_" + module.params["state"])]
    return await func(module.params, session)


async def _copy(params, session):
    accepted_fields = ["client_token", "destination_create_spec"]
    if "copy" == "create":
        _exists = await exists(params, session)
        if _exists:
            return await update_changed_flag({"value": _exists}, 200, "get")
    spec = {}
    for i in accepted_fields:
        if params[i]:
            spec[i] = params[i]
    _url = "https://{vcenter_hostname}/rest/com/vmware/content/library/item/id:{source_library_item_id}".format(
        **params
    )
    async with session.post(_url, json={"spec": spec}) as resp:
        try:
            if resp.headers["Content-Type"] == "application/json":
                _json = await resp.json()
        except KeyError:
            _json = {}
        if ("copy" == "create") and (resp.status in [200, 201]) and ("value" in _json):
            if type(_json["value"]) == dict:
                _id = list(_json["value"].values())[0]
            else:
                _id = _json["value"]
            _json = {"value": (await get_device_info(params, session, _url, _id))}
        return await update_changed_flag(_json, resp.status, "copy")


async def _create(params, session):
    accepted_fields = ["client_token", "create_spec"]
    if "create" == "create":
        _exists = await exists(params, session)
        if _exists:
            return await update_changed_flag({"value": _exists}, 200, "get")
    spec = {}
    for i in accepted_fields:
        if params[i]:
            spec[i] = params[i]
    _url = "https://{vcenter_hostname}/rest/com/vmware/content/library/item".format(
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
    _url = "https://{vcenter_hostname}/rest/com/vmware/content/library/item/id:{library_item_id}".format(
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


async def _find(params, session):
    accepted_fields = ["cached", "library_id", "name", "source_id", "type"]
    if "find" == "create":
        _exists = await exists(params, session)
        if _exists:
            return await update_changed_flag({"value": _exists}, 200, "get")
    spec = {}
    for i in accepted_fields:
        if params[i]:
            spec[i] = params[i]
    _url = "https://{vcenter_hostname}/rest/com/vmware/content/library/item?~action=find".format(
        **params
    )
    async with session.post(_url, json={"spec": spec}) as resp:
        try:
            if resp.headers["Content-Type"] == "application/json":
                _json = await resp.json()
        except KeyError:
            _json = {}
        if ("find" == "create") and (resp.status in [200, 201]) and ("value" in _json):
            if type(_json["value"]) == dict:
                _id = list(_json["value"].values())[0]
            else:
                _id = _json["value"]
            _json = {"value": (await get_device_info(params, session, _url, _id))}
        return await update_changed_flag(_json, resp.status, "find")


async def _publish(params, session):
    accepted_fields = ["force_sync_content", "subscriptions"]
    if "publish" == "create":
        _exists = await exists(params, session)
        if _exists:
            return await update_changed_flag({"value": _exists}, 200, "get")
    spec = {}
    for i in accepted_fields:
        if params[i]:
            spec[i] = params[i]
    _url = "https://{vcenter_hostname}/rest/com/vmware/content/library/item/id:{library_item_id}".format(
        **params
    )
    async with session.post(_url, json={"spec": spec}) as resp:
        try:
            if resp.headers["Content-Type"] == "application/json":
                _json = await resp.json()
        except KeyError:
            _json = {}
        if (
            ("publish" == "create")
            and (resp.status in [200, 201])
            and ("value" in _json)
        ):
            if type(_json["value"]) == dict:
                _id = list(_json["value"].values())[0]
            else:
                _id = _json["value"]
            _json = {"value": (await get_device_info(params, session, _url, _id))}
        return await update_changed_flag(_json, resp.status, "publish")


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
    _url = "https://{vcenter_hostname}/rest/com/vmware/content/library/item/id:{library_item_id}".format(
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
