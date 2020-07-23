from __future__ import absolute_import, division, print_function

__metaclass__ = type
import socket
import json

DOCUMENTATION = "author:\n- Ansible VMware team\ndescription: Handle resource of type content_subscribedlibrary\nextends_documentation_fragment: []\nmodule: content_subscribedlibrary\nnotes:\n- Tested on vSphere 7.0\noptions:\n  client_token:\n    description:\n    - 'Unique token generated on the client for each creation request. The token should\n      be a universally unique identifier (UUID), for example: {@code b8a2a2e3-2314-43cd-a871-6ede0f429751}.\n      This token can be used to guarantee idempotent creation.'\n    type: str\n  create_spec:\n    description:\n    - Specification for the new subscribed library. Required with I(state=['create'])\n    - 'Validate attributes are:'\n    - ' - C(creation_time) (str): The date and time when this library was created.'\n    - ' - C(description) (str): A human-readable description for this library.'\n    - ' - C(id) (str): An identifier which uniquely identifies this {@name LibraryModel}.'\n    - ' - C(last_modified_time) (str): The date and time when this library was last\n      updated. <p> This {@term field} is updated automatically when the library properties\n      are changed. This {@term field} is not affected by adding, removing, or modifying\n      a library item or its content within the library. Tagging the library or syncing\n      the subscribed library does not alter this {@term field}.'\n    - ' - C(last_sync_time) (str): The date and time when this library was last synchronized.\n      <p> This {@term field} applies only to subscribed libraries. It is updated every\n      time a synchronization is triggered on the library. The value is {@term unset}\n      for a local library.'\n    - ' - C(name) (str): The name of the library. <p> A Library is identified by a\n      human-readable name. Library names cannot be undefined or an empty string. Names\n      do not have to be unique.'\n    - ' - C(optimization_info) (dict): Defines various optimizations and optimization\n      parameters applied to this library.'\n    - ' - C(publish_info) (dict): Defines how this library is published so that it\n      can be subscribed to by a remote subscribed library. <p> The {@link PublishInfo}\n      defines where and how the metadata for this local library is accessible. A local\n      library is only published publically if {@link PublishInfo#published} is {@code\n      true}.'\n    - ' - C(server_guid) (str): The unique identifier of the vCenter server where\n      the library exists.'\n    - ' - C(storage_backings) (list): The list of default storage backings which are\n      available for this library. <p> A {@link StorageBacking} defines a default storage\n      location which can be used to store files for library items in this library.\n      Some library items, for instance, virtual machine template items, support files\n      that may be distributed across various storage backings. One or more item files\n      may or may not be located on the default storage backing. <p> Multiple default\n      storage locations are not currently supported but may become supported in future\n      releases.'\n    - ' - C(subscription_info) (dict): Defines the subscription behavior for this\n      Library. <p> The {@link SubscriptionInfo} defines how this subscribed library\n      synchronizes to a remote source. Setting the value will determine the remote\n      source to which the library synchronizes, and how. Changing the subscription\n      will result in synchronizing to a new source. If the new source differs from\n      the old one, the old library items and data will be lost. Setting {@link SubscriptionInfo#automaticSyncEnabled}\n      to false will halt subscription but will not remove existing cached data.'\n    - ' - C(type) (str): The {@name LibraryType} defines the type of a {@link LibraryModel}.\n      <p> The type of a library can be used to determine which additional services\n      can be performed with a library.'\n    - ' - C(version) (str): A version number which is updated on metadata changes.\n      This value allows clients to detect concurrent updates and prevent accidental\n      clobbering of data. <p> This value represents a number which is incremented\n      every time library properties, such as name or description, are changed. It\n      is not incremented by changes to a library item within the library, including\n      adding or removing items. It is also not affected by tagging the library.'\n    type: dict\n  library_id:\n    description:\n    - Identifier of the subscribed library to update. Required with I(state=['update',\n      'delete', 'sync', 'evict'])\n    type: str\n  state:\n    choices:\n    - update\n    - sync\n    - probe\n    - delete\n    - create\n    - evict\n    description: []\n    type: str\n  subscription_info:\n    description:\n    - The subscription info to be probed. Required with I(state=['probe'])\n    - 'Validate attributes are:'\n    - ' - C(authentication_method) (str): Indicate how the subscribed library should\n      authenticate with the published library endpoint.'\n    - ' - C(automatic_sync_enabled) (bool): Whether the library should participate\n      in automatic library synchronization. In order for automatic synchronization\n      to happen, the global {@link ConfigurationModel#automaticSyncEnabled} option\n      must also be true. The subscription is still active even when automatic synchronization\n      is turned off, but synchronization is only activated with an explicit call to\n      {@link SubscribedLibrary#sync} or {@link SubscribedItem#sync}. In other words,\n      manual synchronization is still available even when automatic synchronization\n      is disabled.'\n    - ' - C(on_demand) (bool): Indicates whether a library item''s content will be\n      synchronized only on demand. <p> If this is set to {@code true}, then the library\n      item''s metadata will be synchronized but the item''s content (its files) will\n      not be synchronized. The Content Library Service will synchronize the content\n      upon request only. This can cause the first use of the content to have a noticeable\n      delay. <p> Items without synchronized content can be forcefully synchronized\n      in advance using the {@link SubscribedItem#sync} call with {@param.name forceSyncContent}\n      set to true. Once content has been synchronized, the content can removed with\n      the {@link SubscribedItem#evict} call. <p> If this value is set to {@code false},\n      all content will be synchronized in advance.'\n    - ' - C(password) (str): The password to use when authenticating. <p> The password\n      must be set when using a password-based authentication method; empty strings\n      are not allowed.'\n    - ' - C(source_info) (dict): Information about the source published library. This\n      {@term field} will be set for a subscribed library which is associated with\n      a subscription of the published library.'\n    - ' - C(ssl_thumbprint) (str): An optional SHA-1 hash of the SSL certificate for\n      the remote endpoint. <p> If this value is defined the SSL certificate will be\n      verified by comparing it to the SSL thumbprint. The SSL certificate must verify\n      against the thumbprint. When specified, the standard certificate chain validation\n      behavior is not used. The certificate chain is validated normally if this value\n      is {@term unset}.'\n    - ' - C(subscription_url) (str): The URL of the endpoint where the metadata for\n      the remotely published library is being served. <p> This URL can be the {@link\n      PublishInfo#publishUrl} of the published library (for example, https://server/path/lib.json).\n      <p> If the source content comes from a published library with {@link PublishInfo#persistJsonEnabled},\n      the subscription URL can be a URL pointing to the library JSON file on a datastore\n      or remote file system. The supported formats are: <p> vSphere 6.5 <ul> <li>ds:///vmfs/volumes/{uuid}/mylibrary/lib.json\n      (for datastore)</li> <li>nfs://server/path/mylibrary/lib.json (for NFSv3 server\n      on vCenter Server Appliance)</li> <li>nfs://server/path/mylibrary/lib.json?version=4\n      (for NFSv4 server on vCenter Server Appliance) </li> <li>smb://server/path/mylibrary/lib.json\n      (for SMB server)</li> </ul> <p> vSphere 6.0 <ul> <li>file://server/mylibrary/lib.json\n      (for UNC server on vCenter Server for Windows)</li> <li>file:///path/mylibrary/lib.json\n      (for local file system)</li> </ul> <p> When you specify a DS subscription URL,\n      the datastore must be on the same vCenter Server as the subscribed library.\n      When you specify an NFS or SMB subscription URL, the {@link StorageBacking#storageUri}\n      of the subscribed library must be on the same remote file server and should\n      share a common parent path with the subscription URL.'\n    - ' - C(user_name) (str): The username to use when authenticating. <p> The username\n      must be set when using a password-based authentication method. Empty strings\n      are allowed for usernames.'\n    type: dict\n  update_spec:\n    description:\n    - Specification of the new property values to set on the subscribed library. Required\n      with I(state=['update'])\n    - 'Validate attributes are:'\n    - ' - C(creation_time) (str): The date and time when this library was created.'\n    - ' - C(description) (str): A human-readable description for this library.'\n    - ' - C(id) (str): An identifier which uniquely identifies this {@name LibraryModel}.'\n    - ' - C(last_modified_time) (str): The date and time when this library was last\n      updated. <p> This {@term field} is updated automatically when the library properties\n      are changed. This {@term field} is not affected by adding, removing, or modifying\n      a library item or its content within the library. Tagging the library or syncing\n      the subscribed library does not alter this {@term field}.'\n    - ' - C(last_sync_time) (str): The date and time when this library was last synchronized.\n      <p> This {@term field} applies only to subscribed libraries. It is updated every\n      time a synchronization is triggered on the library. The value is {@term unset}\n      for a local library.'\n    - ' - C(name) (str): The name of the library. <p> A Library is identified by a\n      human-readable name. Library names cannot be undefined or an empty string. Names\n      do not have to be unique.'\n    - ' - C(optimization_info) (dict): Defines various optimizations and optimization\n      parameters applied to this library.'\n    - ' - C(publish_info) (dict): Defines how this library is published so that it\n      can be subscribed to by a remote subscribed library. <p> The {@link PublishInfo}\n      defines where and how the metadata for this local library is accessible. A local\n      library is only published publically if {@link PublishInfo#published} is {@code\n      true}.'\n    - ' - C(server_guid) (str): The unique identifier of the vCenter server where\n      the library exists.'\n    - ' - C(storage_backings) (list): The list of default storage backings which are\n      available for this library. <p> A {@link StorageBacking} defines a default storage\n      location which can be used to store files for library items in this library.\n      Some library items, for instance, virtual machine template items, support files\n      that may be distributed across various storage backings. One or more item files\n      may or may not be located on the default storage backing. <p> Multiple default\n      storage locations are not currently supported but may become supported in future\n      releases.'\n    - ' - C(subscription_info) (dict): Defines the subscription behavior for this\n      Library. <p> The {@link SubscriptionInfo} defines how this subscribed library\n      synchronizes to a remote source. Setting the value will determine the remote\n      source to which the library synchronizes, and how. Changing the subscription\n      will result in synchronizing to a new source. If the new source differs from\n      the old one, the old library items and data will be lost. Setting {@link SubscriptionInfo#automaticSyncEnabled}\n      to false will halt subscription but will not remove existing cached data.'\n    - ' - C(type) (str): The {@name LibraryType} defines the type of a {@link LibraryModel}.\n      <p> The type of a library can be used to determine which additional services\n      can be performed with a library.'\n    - ' - C(version) (str): A version number which is updated on metadata changes.\n      This value allows clients to detect concurrent updates and prevent accidental\n      clobbering of data. <p> This value represents a number which is incremented\n      every time library properties, such as name or description, are changed. It\n      is not incremented by changes to a library item within the library, including\n      adding or removing items. It is also not affected by tagging the library.'\n    type: dict\n  ~action:\n    choices:\n    - sync\n    description:\n    - ~action=sync Required with I(state=['sync'])\n    type: str\nrequirements:\n- python >= 3.6\nshort_description: Handle resource of type content_subscribedlibrary\nversion_added: 1.0.0\n"
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
        "choices": ["sync"],
        "operationIds": ["sync"],
    }
    argument_spec["update_spec"] = {"type": "dict", "operationIds": ["update"]}
    argument_spec["subscription_info"] = {"type": "dict", "operationIds": ["probe"]}
    argument_spec["state"] = {
        "type": "str",
        "choices": ["create", "delete", "evict", "probe", "sync", "update"],
    }
    argument_spec["library_id"] = {
        "type": "str",
        "operationIds": ["delete", "evict", "sync", "update"],
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
            if type(_json["value"]) == dict:
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
            if type(_json["value"]) == dict:
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
