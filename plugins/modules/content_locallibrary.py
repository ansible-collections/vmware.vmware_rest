from __future__ import absolute_import, division, print_function

__metaclass__ = type
import socket
import json

DOCUMENTATION = """
module: content_locallibrary
short_description: Handle resource of type content_locallibrary
description: Handle resource of type content_locallibrary
options:
  client_token:
    description:
    - 'A unique token generated on the client for each creation request. The token
      should be a universally unique identifier (UUID), for example: {@code b8a2a2e3-2314-43cd-a871-6ede0f429751}.
      This token can be used to guarantee idempotent creation.'
    type: str
  create_spec:
    description:
    - Specification for the new local library. Required with I(state=['create'])
    - 'Validate attributes are:'
    - ' - C(creation_time) (str): The date and time when this library was created.'
    - ' - C(description) (str): A human-readable description for this library.'
    - ' - C(id) (str): An identifier which uniquely identifies this {@name LibraryModel}.'
    - ' - C(last_modified_time) (str): The date and time when this library was last
      updated. <p> This {@term field} is updated automatically when the library properties
      are changed. This {@term field} is not affected by adding, removing, or modifying
      a library item or its content within the library. Tagging the library or syncing
      the subscribed library does not alter this {@term field}.'
    - ' - C(last_sync_time) (str): The date and time when this library was last synchronized.
      <p> This {@term field} applies only to subscribed libraries. It is updated every
      time a synchronization is triggered on the library. The value is {@term unset}
      for a local library.'
    - ' - C(name) (str): The name of the library. <p> A Library is identified by a
      human-readable name. Library names cannot be undefined or an empty string. Names
      do not have to be unique.'
    - ' - C(optimization_info) (dict): Defines various optimizations and optimization
      parameters applied to this library.'
    - ' - C(publish_info) (dict): Defines how this library is published so that it
      can be subscribed to by a remote subscribed library. <p> The {@link PublishInfo}
      defines where and how the metadata for this local library is accessible. A local
      library is only published publically if {@link PublishInfo#published} is {@code
      true}.'
    - ' - C(server_guid) (str): The unique identifier of the vCenter server where
      the library exists.'
    - ' - C(storage_backings) (list): The list of default storage backings which are
      available for this library. <p> A {@link StorageBacking} defines a default storage
      location which can be used to store files for library items in this library.
      Some library items, for instance, virtual machine template items, support files
      that may be distributed across various storage backings. One or more item files
      may or may not be located on the default storage backing. <p> Multiple default
      storage locations are not currently supported but may become supported in future
      releases.'
    - ' - C(subscription_info) (dict): Defines the subscription behavior for this
      Library. <p> The {@link SubscriptionInfo} defines how this subscribed library
      synchronizes to a remote source. Setting the value will determine the remote
      source to which the library synchronizes, and how. Changing the subscription
      will result in synchronizing to a new source. If the new source differs from
      the old one, the old library items and data will be lost. Setting {@link SubscriptionInfo#automaticSyncEnabled}
      to false will halt subscription but will not remove existing cached data.'
    - ' - C(type) (str): The {@name LibraryType} defines the type of a {@link LibraryModel}.
      <p> The type of a library can be used to determine which additional services
      can be performed with a library.'
    - ' - C(version) (str): A version number which is updated on metadata changes.
      This value allows clients to detect concurrent updates and prevent accidental
      clobbering of data. <p> This value represents a number which is incremented
      every time library properties, such as name or description, are changed. It
      is not incremented by changes to a library item within the library, including
      adding or removing items. It is also not affected by tagging the library.'
    type: dict
  library_id:
    description:
    - Identifier of the local library to update. Required with I(state=['delete',
      'publish', 'update'])
    type: str
  state:
    choices:
    - create
    - delete
    - publish
    - update
    description: []
    type: str
  subscriptions:
    description:
    - The list of subscriptions to publish this library to.
    type: list
  update_spec:
    description:
    - Specification of the new property values to set on the local library. Required
      with I(state=['update'])
    - 'Validate attributes are:'
    - ' - C(creation_time) (str): The date and time when this library was created.'
    - ' - C(description) (str): A human-readable description for this library.'
    - ' - C(id) (str): An identifier which uniquely identifies this {@name LibraryModel}.'
    - ' - C(last_modified_time) (str): The date and time when this library was last
      updated. <p> This {@term field} is updated automatically when the library properties
      are changed. This {@term field} is not affected by adding, removing, or modifying
      a library item or its content within the library. Tagging the library or syncing
      the subscribed library does not alter this {@term field}.'
    - ' - C(last_sync_time) (str): The date and time when this library was last synchronized.
      <p> This {@term field} applies only to subscribed libraries. It is updated every
      time a synchronization is triggered on the library. The value is {@term unset}
      for a local library.'
    - ' - C(name) (str): The name of the library. <p> A Library is identified by a
      human-readable name. Library names cannot be undefined or an empty string. Names
      do not have to be unique.'
    - ' - C(optimization_info) (dict): Defines various optimizations and optimization
      parameters applied to this library.'
    - ' - C(publish_info) (dict): Defines how this library is published so that it
      can be subscribed to by a remote subscribed library. <p> The {@link PublishInfo}
      defines where and how the metadata for this local library is accessible. A local
      library is only published publically if {@link PublishInfo#published} is {@code
      true}.'
    - ' - C(server_guid) (str): The unique identifier of the vCenter server where
      the library exists.'
    - ' - C(storage_backings) (list): The list of default storage backings which are
      available for this library. <p> A {@link StorageBacking} defines a default storage
      location which can be used to store files for library items in this library.
      Some library items, for instance, virtual machine template items, support files
      that may be distributed across various storage backings. One or more item files
      may or may not be located on the default storage backing. <p> Multiple default
      storage locations are not currently supported but may become supported in future
      releases.'
    - ' - C(subscription_info) (dict): Defines the subscription behavior for this
      Library. <p> The {@link SubscriptionInfo} defines how this subscribed library
      synchronizes to a remote source. Setting the value will determine the remote
      source to which the library synchronizes, and how. Changing the subscription
      will result in synchronizing to a new source. If the new source differs from
      the old one, the old library items and data will be lost. Setting {@link SubscriptionInfo#automaticSyncEnabled}
      to false will halt subscription but will not remove existing cached data.'
    - ' - C(type) (str): The {@name LibraryType} defines the type of a {@link LibraryModel}.
      <p> The type of a library can be used to determine which additional services
      can be performed with a library.'
    - ' - C(version) (str): A version number which is updated on metadata changes.
      This value allows clients to detect concurrent updates and prevent accidental
      clobbering of data. <p> This value represents a number which is incremented
      every time library properties, such as name or description, are changed. It
      is not incremented by changes to a library item within the library, including
      adding or removing items. It is also not affected by tagging the library.'
    type: dict
  ~action:
    choices:
    - publish
    description:
    - ~action=publish Required with I(state=['publish'])
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
        "choices": ["publish"],
        "operationIds": ["publish"],
    }
    argument_spec["update_spec"] = {"type": "dict", "operationIds": ["update"]}
    argument_spec["subscriptions"] = {"type": "list", "operationIds": ["publish"]}
    argument_spec["state"] = {
        "type": "str",
        "choices": ["create", "delete", "publish", "update"],
    }
    argument_spec["library_id"] = {
        "type": "str",
        "operationIds": ["delete", "publish", "update"],
    }
    argument_spec["create_spec"] = {"type": "dict", "operationIds": ["create"]}
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
    return "https://{vcenter_hostname}/rest/com/vmware/content/local-library".format(
        **params
    )


async def entry_point(module, session):
    func = globals()[("_" + module.params["state"])]
    return await func(module.params, session)


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
    _url = "https://{vcenter_hostname}/rest/com/vmware/content/local-library".format(
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
    _url = "https://{vcenter_hostname}/rest/com/vmware/content/local-library/id:{library_id}".format(
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


async def _publish(params, session):
    accepted_fields = ["subscriptions"]
    if "publish" == "create":
        _exists = await exists(params, session)
        if _exists:
            return await update_changed_flag({"value": _exists}, 200, "get")
    spec = {}
    for i in accepted_fields:
        if params[i]:
            spec[i] = params[i]
    _url = "https://{vcenter_hostname}/rest/com/vmware/content/local-library/id:{library_id}".format(
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
    _url = "https://{vcenter_hostname}/rest/com/vmware/content/local-library/id:{library_id}".format(
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
