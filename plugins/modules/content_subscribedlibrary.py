#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = """
module: content_subscribedlibrary
short_description: Handle resource of type content_subscribedlibrary
description: Handle resource of type content_subscribedlibrary
options:
  client_token:
    description:
    - 'Unique token generated on the client for each creation request. The token should
      be a universally unique identifier (UUID), for example: {@code b8a2a2e3-2314-43cd-a871-6ede0f429751}.
      This token can be used to guarantee idempotent creation.'
    type: str
  create_spec:
    description:
    - Specification for the new subscribed library. Required with I(state=['create'])
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
    - Identifier of the subscribed library whose content should be evicted. Required
      with I(state=['delete', 'evict', 'sync', 'update'])
    type: str
  state:
    choices:
    - create
    - delete
    - evict
    - probe
    - sync
    - update
    description: []
    type: str
  subscription_info:
    description:
    - The subscription info to be probed. Required with I(state=['probe'])
    - 'Validate attributes are:'
    - ' - C(authentication_method) (str): Indicate how the subscribed library should
      authenticate with the published library endpoint.'
    - ' - C(automatic_sync_enabled) (bool): Whether the library should participate
      in automatic library synchronization. In order for automatic synchronization
      to happen, the global {@link ConfigurationModel#automaticSyncEnabled} option
      must also be true. The subscription is still active even when automatic synchronization
      is turned off, but synchronization is only activated with an explicit call to
      {@link SubscribedLibrary#sync} or {@link SubscribedItem#sync}. In other words,
      manual synchronization is still available even when automatic synchronization
      is disabled.'
    - ' - C(on_demand) (bool): Indicates whether a library item''s content will be
      synchronized only on demand. <p> If this is set to {@code true}, then the library
      item''s metadata will be synchronized but the item''s content (its files) will
      not be synchronized. The Content Library Service will synchronize the content
      upon request only. This can cause the first use of the content to have a noticeable
      delay. <p> Items without synchronized content can be forcefully synchronized
      in advance using the {@link SubscribedItem#sync} call with {@param.name forceSyncContent}
      set to true. Once content has been synchronized, the content can removed with
      the {@link SubscribedItem#evict} call. <p> If this value is set to {@code false},
      all content will be synchronized in advance.'
    - ' - C(password) (str): The password to use when authenticating. <p> The password
      must be set when using a password-based authentication method; empty strings
      are not allowed.'
    - ' - C(source_info) (dict): Information about the source published library. This
      {@term field} will be set for a subscribed library which is associated with
      a subscription of the published library.'
    - ' - C(ssl_thumbprint) (str): An optional SHA-1 hash of the SSL certificate for
      the remote endpoint. <p> If this value is defined the SSL certificate will be
      verified by comparing it to the SSL thumbprint. The SSL certificate must verify
      against the thumbprint. When specified, the standard certificate chain validation
      behavior is not used. The certificate chain is validated normally if this value
      is {@term unset}.'
    - ' - C(subscription_url) (str): The URL of the endpoint where the metadata for
      the remotely published library is being served. <p> This URL can be the {@link
      PublishInfo#publishUrl} of the published library (for example, https://server/path/lib.json).
      <p> If the source content comes from a published library with {@link PublishInfo#persistJsonEnabled},
      the subscription URL can be a URL pointing to the library JSON file on a datastore
      or remote file system. The supported formats are: <p> vSphere 6.5 <ul> <li>ds:///vmfs/volumes/{uuid}/mylibrary/lib.json
      (for datastore)</li> <li>nfs://server/path/mylibrary/lib.json (for NFSv3 server
      on vCenter Server Appliance)</li> <li>nfs://server/path/mylibrary/lib.json?version=4
      (for NFSv4 server on vCenter Server Appliance) </li> <li>smb://server/path/mylibrary/lib.json
      (for SMB server)</li> </ul> <p> vSphere 6.0 <ul> <li>file://server/mylibrary/lib.json
      (for UNC server on vCenter Server for Windows)</li> <li>file:///path/mylibrary/lib.json
      (for local file system)</li> </ul> <p> When you specify a DS subscription URL,
      the datastore must be on the same vCenter Server as the subscribed library.
      When you specify an NFS or SMB subscription URL, the {@link StorageBacking#storageUri}
      of the subscribed library must be on the same remote file server and should
      share a common parent path with the subscription URL.'
    - ' - C(user_name) (str): The username to use when authenticating. <p> The username
      must be set when using a password-based authentication method. Empty strings
      are allowed for usernames.'
    type: dict
  update_spec:
    description:
    - Specification of the new property values to set on the subscribed library. Required
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
    - sync
    description:
    - ~action=sync Required with I(state=['sync'])
    type: str
author:
- Ansible VMware team
version_added: 1.0.0
requirements:
- python >= 3.6
"""

IN_QUERY_PARAMETER = ["~action"]

import socket
import json
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
            type="str", required=False, fallback=(env_fallback, ["VMWARE_HOST"]),
        ),
        "vcenter_username": dict(
            type="str", required=False, fallback=(env_fallback, ["VMWARE_USER"]),
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

    argument_spec["client_token"] = {"type": "str", "operationIds": ["create"]}
    argument_spec["create_spec"] = {"type": "dict", "operationIds": ["create"]}
    argument_spec["library_id"] = {
        "type": "str",
        "operationIds": ["delete", "evict", "sync", "update"],
    }
    argument_spec["state"] = {
        "type": "str",
        "choices": ["create", "delete", "evict", "probe", "sync", "update"],
    }
    argument_spec["subscription_info"] = {"type": "dict", "operationIds": ["probe"]}
    argument_spec["update_spec"] = {"type": "dict", "operationIds": ["update"]}
    argument_spec["~action"] = {
        "type": "str",
        "choices": ["sync"],
        "operationIds": ["sync"],
    }

    return argument_spec


async def get_device_info(params, session, _url, _key):
    async with session.get(_url + "/" + _key) as resp:
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
            if params.get(k) is not None and device.get(k) != params.get(k):
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

    return "https://{vcenter_hostname}/rest/com/vmware/content/subscribed-library".format(
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
    _url = "https://{vcenter_hostname}/rest/com/vmware/content/subscribed-library".format(
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
            if isinstance(_json["value"], dict):
                _id = list(_json["value"].values())[0]
            else:
                _id = _json["value"]
            _json = {"value": (await get_device_info(params, session, _url, _id))}
        return await update_changed_flag(_json, resp.status, "create")


async def _delete(params, session):
    _url = "https://{vcenter_hostname}/rest/com/vmware/content/subscribed-library/id:{library_id}".format(
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


async def _evict(params, session):
    _url = "https://{vcenter_hostname}/rest/com/vmware/content/subscribed-library/id:{library_id}?~action=evict".format(
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
        return await update_changed_flag(_json, resp.status, "evict")


async def _probe(params, session):
    accepted_fields = ["subscription_info"]
    if "probe" == "create":
        _exists = await exists(params, session)
        if _exists:
            return await update_changed_flag({"value": _exists}, 200, "get")
    spec = {}
    for i in accepted_fields:
        if params[i]:
            spec[i] = params[i]
    _url = "https://{vcenter_hostname}/rest/com/vmware/content/subscribed-library?~action=probe".format(
        **params
    )
    async with session.post(_url, json={"spec": spec}) as resp:
        try:
            if resp.headers["Content-Type"] == "application/json":
                _json = await resp.json()
        except KeyError:
            _json = {}
        if ("probe" == "create") and (resp.status in [200, 201]) and ("value" in _json):
            if isinstance(_json["value"], dict):
                _id = list(_json["value"].values())[0]
            else:
                _id = _json["value"]
            _json = {"value": (await get_device_info(params, session, _url, _id))}
        return await update_changed_flag(_json, resp.status, "probe")


async def _sync(params, session):
    _url = "https://{vcenter_hostname}/rest/com/vmware/content/subscribed-library/id:{library_id}".format(
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
        return await update_changed_flag(_json, resp.status, "sync")


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
    _url = "https://{vcenter_hostname}/rest/com/vmware/content/subscribed-library/id:{library_id}".format(
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
            if isinstance(_json["value"], dict):
                _id = list(_json["value"].values())[0]
            else:
                _id = _json["value"]
            _json = {"value": (await get_device_info(params, session, _url, _id))}
        return await update_changed_flag(_json, resp.status, "update")


if __name__ == "__main__":
    import asyncio

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
