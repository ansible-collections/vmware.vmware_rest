#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2021, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# template: header.j2

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = r"""
module: content_locallibrary
short_description: Handle resource of type content_locallibrary
description: Handle resource of type content_locallibrary
options:
  action:
    choices:
    - publish
    description:
    - ~action=publish Required with I(state=['publish'])
    type: str
  client_token:
    description:
    - 'A unique token generated on the client for each creation request. The token
      should be a universally unique identifier (UUID), for example: C(b8a2a2e3-2314-43cd-a871-6ede0f429751).
      This token can be used to guarantee idempotent creation.'
    type: str
  create_spec:
    description:
    - Specification for the new local library. Required with I(state=['present'])
    - 'Valid attributes are:'
    - ' - C(creation_time) (str): The date and time when this library was created.'
    - ' - C(description) (str): A human-readable description for this library.'
    - ' - C(id) (str): An identifier which uniquely identifies this Library.'
    - ' - C(last_modified_time) (str): The date and time when this library was last
      updated. This field is updated automatically when the library properties are
      changed. This field is not affected by adding, removing, or modifying a library
      item or its content within the library. Tagging the library or syncing the subscribed
      library does not alter this field.'
    - ' - C(last_sync_time) (str): The date and time when this library was last synchronized.
      This field applies only to subscribed libraries. It is updated every time a
      synchronization is triggered on the library. The value is not set for a local
      library.'
    - ' - C(name) (str): The name of the library. A Library is identified by a human-readable
      name. Library names cannot be undefined or an empty string. Names do not have
      to be unique.'
    - ' - C(optimization_info) (dict): Defines various optimizations and optimization
      parameters applied to this library.'
    - '   - Accepted keys:'
    - '     - optimize_remote_publishing (boolean): If set to C(True) then library
      would be optimized for remote publishing. Turn it on if remote publishing is
      dominant use case for this library. Remote publishing means here that publisher
      and subscribers are not the part of the same vCenter SSO domain. Any optimizations
      could be done as result of turning on this optimization during library creation.
      For example, library content could be stored in different format but optimizations
      are not limited to just storage format. Note, that value of this toggle could
      be set only during creation of the library and you would need to migrate your
      library in case you need to change this value (optimize the library for different
      use case).'
    - ' - C(publish_info) (dict): Defines how this library is published so that it
      can be subscribed to by a remote subscribed library. The C(publish_info) defines
      where and how the metadata for this local library is accessible. A local library
      is only published publically if C(publish_info.published) is C(True).'
    - '   - Accepted keys:'
    - '     - authentication_method (string): The authentication_method indicates
      how a subscribed library should authenticate to the published library endpoint.'
    - 'Accepted value for this field:'
    - '       - C(BASIC)'
    - '       - C(NONE)'
    - '     - current_password (string): The current password to verify. This field
      is available starting in vSphere 6.7.'
    - '     - password (string): The new password to require for authentication.'
    - '     - persist_json_enabled (boolean): Whether library and library item metadata
      are persisted in the storage backing as JSON files. This flag only applies if
      the local library is published. Enabling JSON persistence allows you to synchronize
      a subscribed library manually instead of over HTTP. You copy the local library
      content and metadata to another storage backing manually and then create a subscribed
      library referencing the location of the library JSON file in the C(subscription_info.subscriptionurl).
      When the subscribed library''s storage backing matches the subscription URL,
      files do not need to be copied to the subscribed library. For a library backed
      by a datastore, the library JSON file will be stored at the path contentlib-{library_id}/lib.json
      on the datastore. For a library backed by a remote file system, the library
      JSON file will be stored at {library_id}/lib.json in the remote file system
      path.'
    - '     - publish_url (string): The URL to which the library metadata is published
      by the Content Library Service. This value can be used to set the C(subscription_info.subscriptionurl)
      property when creating a subscribed library.'
    - '     - published (boolean): Whether the local library is published.'
    - '     - user_name (string): The username to require for authentication.'
    - ' - C(server_guid) (str): The unique identifier of the vCenter server where
      the library exists.'
    - ' - C(storage_backings) (list): The list of default storage backings which are
      available for this library. A storage backing defines a default storage location
      which can be used to store files for library items in this library. Some library
      items, for instance, virtual machine template items, support files that may
      be distributed across various storage backings. One or more item files may or
      may not be located on the default storage backing. Multiple default storage
      locations are not currently supported but may become supported in future releases.'
    - ' - C(subscription_info) (dict): Defines the subscription behavior for this
      Library. The C(subscription_info) defines how this subscribed library synchronizes
      to a remote source. Setting the value will determine the remote source to which
      the library synchronizes, and how. Changing the subscription will result in
      synchronizing to a new source. If the new source differs from the old one, the
      old library items and data will be lost. Setting C(subscription_info.automaticSyncEnabled)
      to false will halt subscription but will not remove existing cached data.'
    - '   - Accepted keys:'
    - '     - authentication_method (string): Indicate how the subscribed library
      should authenticate with the published library endpoint.'
    - 'Accepted value for this field:'
    - '       - C(BASIC)'
    - '       - C(NONE)'
    - '     - automatic_sync_enabled (boolean): Whether the library should participate
      in automatic library synchronization. In order for automatic synchronization
      to happen, the global C(configuration_model.automaticSyncEnabled) option must
      also be true. The subscription is still active even when automatic synchronization
      is turned off, but synchronization is only activated with an explicit call to
      Subscribed Library Sync or Subscribed Item Sync. In other words, manual synchronization
      is still available even when automatic synchronization is disabled.'
    - '     - on_demand (boolean): Indicates whether a library item''s content will
      be synchronized only on demand. If this is set to C(True), then the library
      item''s metadata will be synchronized but the item''s content (its files) will
      not be synchronized. The Content Library Service will synchronize the content
      upon request only. This can cause the first use of the content to have a noticeable
      delay. Items without synchronized content can be forcefully synchronized in
      advance using the Subscribed Item Sync call with C(forceSyncContent} set to
      true. Once content has been synchronized, the content can removed with the {@link
      SubscribedItem#evict) call. If this value is set to C(False), all content will
      be synchronized in advance.'
    - '     - password (string): The password to use when authenticating. The password
      must be set when using a password-based authentication method; empty strings
      are not allowed.'
    - '     - source_info (object): Information about the source published library.
      This field will be set for a subscribed library which is associated with a subscription
      of the published library.'
    - '     - ssl_thumbprint (string): An optional SHA-1 hash of the SSL certificate
      for the remote endpoint. If this value is defined the SSL certificate will be
      verified by comparing it to the SSL thumbprint. The SSL certificate must verify
      against the thumbprint. When specified, the standard certificate chain validation
      behavior is not used. The certificate chain is validated normally if this value
      is not set.'
    - '     - subscription_url (string): The URL of the endpoint where the metadata
      for the remotely published library is being served. This URL can be the C(publish_info.publishUrl)
      of the published library (for example, https://server/path/lib.json). If the
      source content comes from a published library with C(publish_info.persistJsonEnabled),
      the subscription URL can be a URL pointing to the library JSON file on a datastore
      or remote file system. The supported formats are: vSphere 6.5 <ul> <li>ds:///vmfs/volumes/{uuid}/mylibrary/lib.json
      (for datastore)</li> <li>nfs://server/path/mylibrary/lib.json (for NFSv3 server
      on vCenter Server Appliance)</li> <li>nfs://server/path/mylibrary/lib.json?version=4
      (for NFSv4 server on vCenter Server Appliance) </li> <li>smb://server/path/mylibrary/lib.json
      (for SMB server)</li> </ul> vSphere 6.0 <ul> <li>file://server/mylibrary/lib.json
      (for UNC server on vCenter Server for Windows)</li> <li>file:///path/mylibrary/lib.json
      (for local file system)</li> </ul> When you specify a DS subscription URL, the
      datastore must be on the same vCenter Server as the subscribed library. When
      you specify an NFS or SMB subscription URL, the C(Storage Backing URI) of the
      subscribed library must be on the same remote file server and should share a
      common parent path with the subscription URL.'
    - '     - user_name (string): The username to use when authenticating. The username
      must be set when using a password-based authentication method. Empty strings
      are allowed for usernames.'
    - ' - C(type) (str): The Library Type defines the type of a Library. The type
      of a library can be used to determine which additional services can be performed
      with a library.'
    - '   - Accepted values:'
    - '     - LOCAL'
    - '     - SUBSCRIBED'
    - ' - C(version) (str): A version number which is updated on metadata changes.
      This value allows clients to detect concurrent updates and prevent accidental
      clobbering of data. This value represents a number which is incremented every
      time library properties, such as name or description, are changed. It is not
      incremented by changes to a library item within the library, including adding
      or removing items. It is also not affected by tagging the library.'
    type: dict
  library_id:
    description:
    - Identifier of the local library to delete. Required with I(state=['absent',
      'present', 'publish'])
    type: str
  state:
    choices:
    - absent
    - present
    - publish
    default: present
    description: []
    type: str
  subscriptions:
    description:
    - The list of subscriptions to publish this library to.
    - 'Valid attributes are:'
    - ' - C(subscription) (str): Identifier of the subscription associated with the
      subscribed library.'
    - '   This key is required.'
    elements: dict
    type: list
  update_spec:
    description:
    - Specification for the new local library. Required with I(state=['present'])
    - 'Valid attributes are:'
    - ' - C(creation_time) (str): The date and time when this library was created.'
    - ' - C(description) (str): A human-readable description for this library.'
    - ' - C(id) (str): An identifier which uniquely identifies this Library.'
    - ' - C(last_modified_time) (str): The date and time when this library was last
      updated. This field is updated automatically when the library properties are
      changed. This field is not affected by adding, removing, or modifying a library
      item or its content within the library. Tagging the library or syncing the subscribed
      library does not alter this field.'
    - ' - C(last_sync_time) (str): The date and time when this library was last synchronized.
      This field applies only to subscribed libraries. It is updated every time a
      synchronization is triggered on the library. The value is not set for a local
      library.'
    - ' - C(name) (str): The name of the library. A Library is identified by a human-readable
      name. Library names cannot be undefined or an empty string. Names do not have
      to be unique.'
    - ' - C(optimization_info) (dict): Defines various optimizations and optimization
      parameters applied to this library.'
    - '   - Accepted keys:'
    - '     - optimize_remote_publishing (boolean): If set to C(True) then library
      would be optimized for remote publishing. Turn it on if remote publishing is
      dominant use case for this library. Remote publishing means here that publisher
      and subscribers are not the part of the same vCenter SSO domain. Any optimizations
      could be done as result of turning on this optimization during library creation.
      For example, library content could be stored in different format but optimizations
      are not limited to just storage format. Note, that value of this toggle could
      be set only during creation of the library and you would need to migrate your
      library in case you need to change this value (optimize the library for different
      use case).'
    - ' - C(publish_info) (dict): Defines how this library is published so that it
      can be subscribed to by a remote subscribed library. The C(publish_info) defines
      where and how the metadata for this local library is accessible. A local library
      is only published publically if C(publish_info.published) is C(True).'
    - '   - Accepted keys:'
    - '     - authentication_method (string): The authentication_method indicates
      how a subscribed library should authenticate to the published library endpoint.'
    - 'Accepted value for this field:'
    - '       - C(BASIC)'
    - '       - C(NONE)'
    - '     - current_password (string): The current password to verify. This field
      is available starting in vSphere 6.7.'
    - '     - password (string): The new password to require for authentication.'
    - '     - persist_json_enabled (boolean): Whether library and library item metadata
      are persisted in the storage backing as JSON files. This flag only applies if
      the local library is published. Enabling JSON persistence allows you to synchronize
      a subscribed library manually instead of over HTTP. You copy the local library
      content and metadata to another storage backing manually and then create a subscribed
      library referencing the location of the library JSON file in the C(subscription_info.subscriptionurl).
      When the subscribed library''s storage backing matches the subscription URL,
      files do not need to be copied to the subscribed library. For a library backed
      by a datastore, the library JSON file will be stored at the path contentlib-{library_id}/lib.json
      on the datastore. For a library backed by a remote file system, the library
      JSON file will be stored at {library_id}/lib.json in the remote file system
      path.'
    - '     - publish_url (string): The URL to which the library metadata is published
      by the Content Library Service. This value can be used to set the C(subscription_info.subscriptionurl)
      property when creating a subscribed library.'
    - '     - published (boolean): Whether the local library is published.'
    - '     - user_name (string): The username to require for authentication.'
    - ' - C(server_guid) (str): The unique identifier of the vCenter server where
      the library exists.'
    - ' - C(storage_backings) (list): The list of default storage backings which are
      available for this library. A storage backing defines a default storage location
      which can be used to store files for library items in this library. Some library
      items, for instance, virtual machine template items, support files that may
      be distributed across various storage backings. One or more item files may or
      may not be located on the default storage backing. Multiple default storage
      locations are not currently supported but may become supported in future releases.'
    - ' - C(subscription_info) (dict): Defines the subscription behavior for this
      Library. The C(subscription_info) defines how this subscribed library synchronizes
      to a remote source. Setting the value will determine the remote source to which
      the library synchronizes, and how. Changing the subscription will result in
      synchronizing to a new source. If the new source differs from the old one, the
      old library items and data will be lost. Setting C(subscription_info.automaticSyncEnabled)
      to false will halt subscription but will not remove existing cached data.'
    - '   - Accepted keys:'
    - '     - authentication_method (string): Indicate how the subscribed library
      should authenticate with the published library endpoint.'
    - 'Accepted value for this field:'
    - '       - C(BASIC)'
    - '       - C(NONE)'
    - '     - automatic_sync_enabled (boolean): Whether the library should participate
      in automatic library synchronization. In order for automatic synchronization
      to happen, the global C(configuration_model.automaticSyncEnabled) option must
      also be true. The subscription is still active even when automatic synchronization
      is turned off, but synchronization is only activated with an explicit call to
      Subscribed Library Sync or Subscribed Item Sync. In other words, manual synchronization
      is still available even when automatic synchronization is disabled.'
    - '     - on_demand (boolean): Indicates whether a library item''s content will
      be synchronized only on demand. If this is set to C(True), then the library
      item''s metadata will be synchronized but the item''s content (its files) will
      not be synchronized. The Content Library Service will synchronize the content
      upon request only. This can cause the first use of the content to have a noticeable
      delay. Items without synchronized content can be forcefully synchronized in
      advance using the Subscribed Item Sync call with C(forceSyncContent} set to
      true. Once content has been synchronized, the content can removed with the {@link
      SubscribedItem#evict) call. If this value is set to C(False), all content will
      be synchronized in advance.'
    - '     - password (string): The password to use when authenticating. The password
      must be set when using a password-based authentication method; empty strings
      are not allowed.'
    - '     - source_info (object): Information about the source published library.
      This field will be set for a subscribed library which is associated with a subscription
      of the published library.'
    - '     - ssl_thumbprint (string): An optional SHA-1 hash of the SSL certificate
      for the remote endpoint. If this value is defined the SSL certificate will be
      verified by comparing it to the SSL thumbprint. The SSL certificate must verify
      against the thumbprint. When specified, the standard certificate chain validation
      behavior is not used. The certificate chain is validated normally if this value
      is not set.'
    - '     - subscription_url (string): The URL of the endpoint where the metadata
      for the remotely published library is being served. This URL can be the C(publish_info.publishUrl)
      of the published library (for example, https://server/path/lib.json). If the
      source content comes from a published library with C(publish_info.persistJsonEnabled),
      the subscription URL can be a URL pointing to the library JSON file on a datastore
      or remote file system. The supported formats are: vSphere 6.5 <ul> <li>ds:///vmfs/volumes/{uuid}/mylibrary/lib.json
      (for datastore)</li> <li>nfs://server/path/mylibrary/lib.json (for NFSv3 server
      on vCenter Server Appliance)</li> <li>nfs://server/path/mylibrary/lib.json?version=4
      (for NFSv4 server on vCenter Server Appliance) </li> <li>smb://server/path/mylibrary/lib.json
      (for SMB server)</li> </ul> vSphere 6.0 <ul> <li>file://server/mylibrary/lib.json
      (for UNC server on vCenter Server for Windows)</li> <li>file:///path/mylibrary/lib.json
      (for local file system)</li> </ul> When you specify a DS subscription URL, the
      datastore must be on the same vCenter Server as the subscribed library. When
      you specify an NFS or SMB subscription URL, the C(Storage Backing URI) of the
      subscribed library must be on the same remote file server and should share a
      common parent path with the subscription URL.'
    - '     - user_name (string): The username to use when authenticating. The username
      must be set when using a password-based authentication method. Empty strings
      are allowed for usernames.'
    - ' - C(type) (str): The Library Type defines the type of a Library. The type
      of a library can be used to determine which additional services can be performed
      with a library.'
    - '   - Accepted values:'
    - '     - LOCAL'
    - '     - SUBSCRIBED'
    - ' - C(version) (str): A version number which is updated on metadata changes.
      This value allows clients to detect concurrent updates and prevent accidental
      clobbering of data. This value represents a number which is incremented every
      time library properties, such as name or description, are changed. It is not
      incremented by changes to a library item within the library, including adding
      or removing items. It is also not affected by tagging the library.'
    type: dict
  vcenter_hostname:
    description:
    - The hostname or IP address of the vSphere vCenter
    - If the value is not specified in the task, the value of environment variable
      C(VMWARE_HOST) will be used instead.
    required: true
    type: str
  vcenter_password:
    description:
    - The vSphere vCenter username
    - If the value is not specified in the task, the value of environment variable
      C(VMWARE_PASSWORD) will be used instead.
    required: true
    type: str
  vcenter_rest_log_file:
    description:
    - 'You can use this optional parameter to set the location of a log file. '
    - 'This file will be used to record the HTTP REST interaction. '
    - 'The file will be stored on the host that run the module. '
    - 'If the value is not specified in the task, the value of '
    - environment variable C(VMWARE_REST_LOG_FILE) will be used instead.
    type: str
  vcenter_username:
    description:
    - The vSphere vCenter username
    - If the value is not specified in the task, the value of environment variable
      C(VMWARE_USER) will be used instead.
    required: true
    type: str
  vcenter_validate_certs:
    default: true
    description:
    - Allows connection when SSL certificates are not valid. Set to C(false) when
      certificates are not trusted.
    - If the value is not specified in the task, the value of environment variable
      C(VMWARE_VALIDATE_CERTS) will be used instead.
    type: bool
author:
- Goneri Le Bouder (@goneri) <goneri@lebouder.net>
version_added: 1.0.0
requirements:
- python >= 3.6
- aiohttp
"""

EXAMPLES = r"""
"""

RETURN = r"""
"""

# This structure describes the format of the data expected by the end-points
PAYLOAD_FORMAT = {
    "list": {"query": {}, "body": {}, "path": {}},
    "create": {
        "query": {},
        "body": {"client_token": "client_token", "create_spec": "create_spec"},
        "path": {},
    },
    "delete": {"query": {}, "body": {}, "path": {"library_id": "library_id"}},
    "get": {"query": {}, "body": {}, "path": {"library_id": "library_id"}},
    "update": {
        "query": {},
        "body": {"update_spec": "update_spec"},
        "path": {"library_id": "library_id"},
    },
    "publish": {
        "query": {"~action": "~action"},
        "body": {"subscriptions": "subscriptions"},
        "path": {"library_id": "library_id"},
    },
}  # pylint: disable=line-too-long

import json
import socket
from ansible.module_utils.basic import env_fallback

try:
    from ansible_collections.cloud.common.plugins.module_utils.turbo.exceptions import (
        EmbeddedModuleFailure,
    )
    from ansible_collections.cloud.common.plugins.module_utils.turbo.module import (
        AnsibleTurboModule as AnsibleModule,
    )

    AnsibleModule.collection_name = "vmware.vmware_rest"
except ImportError:
    from ansible.module_utils.basic import AnsibleModule
from ansible_collections.vmware.vmware_rest.plugins.module_utils.vmware_rest import (
    build_full_device_list,
    exists,
    gen_args,
    get_device_info,
    get_subdevice_type,
    list_devices,
    open_session,
    prepare_payload,
    update_changed_flag,
)


def prepare_argument_spec():
    argument_spec = {
        "vcenter_hostname": dict(
            type="str", required=True, fallback=(env_fallback, ["VMWARE_HOST"]),
        ),
        "vcenter_username": dict(
            type="str", required=True, fallback=(env_fallback, ["VMWARE_USER"]),
        ),
        "vcenter_password": dict(
            type="str",
            required=True,
            no_log=True,
            fallback=(env_fallback, ["VMWARE_PASSWORD"]),
        ),
        "vcenter_validate_certs": dict(
            type="bool",
            required=False,
            default=True,
            fallback=(env_fallback, ["VMWARE_VALIDATE_CERTS"]),
        ),
        "vcenter_rest_log_file": dict(
            type="str",
            required=False,
            fallback=(env_fallback, ["VMWARE_REST_LOG_FILE"]),
        ),
    }

    argument_spec["client_token"] = {"type": "str"}
    argument_spec["create_spec"] = {"type": "dict"}
    argument_spec["library_id"] = {"type": "str"}
    argument_spec["state"] = {
        "type": "str",
        "choices": ["absent", "present", "publish"],
        "default": "present",
    }
    argument_spec["subscriptions"] = {"type": "list", "elements": "dict"}
    argument_spec["update_spec"] = {"type": "dict"}
    argument_spec["action"] = {"type": "str", "choices": ["publish"]}

    return argument_spec


async def main():
    required_if = list(
        [
            ["state", "present", ["create_spec", "library_id", "update_spec"], True],
            ["state", "absent", ["library_id"], True],
            ["state", "publish", ["library_id", "~action"], True],
        ]
    )

    module_args = prepare_argument_spec()
    module = AnsibleModule(
        argument_spec=module_args, required_if=required_if, supports_check_mode=True
    )
    if not module.params["vcenter_hostname"]:
        module.fail_json("vcenter_hostname cannot be empty")
    if not module.params["vcenter_username"]:
        module.fail_json("vcenter_username cannot be empty")
    if not module.params["vcenter_password"]:
        module.fail_json("vcenter_password cannot be empty")
    try:
        session = await open_session(
            vcenter_hostname=module.params["vcenter_hostname"],
            vcenter_username=module.params["vcenter_username"],
            vcenter_password=module.params["vcenter_password"],
            validate_certs=module.params["vcenter_validate_certs"],
            log_file=module.params["vcenter_rest_log_file"],
        )
    except EmbeddedModuleFailure as err:
        module.fail_json(err.get_message())
    result = await entry_point(module, session)
    module.exit_json(**result)


# template: default_module.j2
def build_url(params):
    return (
        "https://{vcenter_hostname}" "/rest/com/vmware/content/local-library"
    ).format(**params)


async def entry_point(module, session):

    if module.params["state"] == "present":
        if "_create" in globals():
            operation = "create"
        else:
            operation = "update"
    elif module.params["state"] == "absent":
        operation = "delete"
    else:
        operation = module.params["state"]

    func = globals()["_" + operation]

    return await func(module.params, session)


async def _create(params, session):

    if params["library_id"]:
        _json = await get_device_info(session, build_url(params), params["library_id"])
    else:
        _json = await exists(params, session, build_url(params), ["library_id"])
    if _json:
        if "_update" in globals():
            params["library_id"] = _json["id"]
            return await globals()["_update"](params, session)
        return await update_changed_flag(_json, 200, "get")

    payload = prepare_payload(params, PAYLOAD_FORMAT["create"])
    _url = (
        "https://{vcenter_hostname}" "/rest/com/vmware/content/local-library"
    ).format(**params)
    async with session.post(_url, json=payload) as resp:
        if resp.status == 500:
            text = await resp.text()
            raise EmbeddedModuleFailure(
                f"Request has failed: status={resp.status}, {text}"
            )
        try:
            if resp.headers["Content-Type"] == "application/json":
                _json = await resp.json()
        except KeyError:
            _json = {}
        # Update the value field with all the details
        if (resp.status in [200, 201]) and "value" in _json:
            if isinstance(_json["value"], dict):
                _id = list(_json["value"].values())[0]
            else:
                _id = _json["value"]
            _json = await get_device_info(session, _url, _id)

        return await update_changed_flag(_json, resp.status, "create")


async def _delete(params, session):
    _in_query_parameters = PAYLOAD_FORMAT["delete"]["query"].keys()
    payload = prepare_payload(params, PAYLOAD_FORMAT["delete"])
    subdevice_type = get_subdevice_type(
        "/rest/com/vmware/content/local-library/id:{library_id}"
    )
    if subdevice_type and not params[subdevice_type]:
        _json = await exists(params, session, build_url(params))
        if _json:
            params[subdevice_type] = _json["id"]
    _url = (
        "https://{vcenter_hostname}"
        "/rest/com/vmware/content/local-library/id:{library_id}"
    ).format(**params) + gen_args(params, _in_query_parameters)
    async with session.delete(_url, json=payload) as resp:
        try:
            if resp.headers["Content-Type"] == "application/json":
                _json = await resp.json()
        except KeyError:
            _json = {}
        return await update_changed_flag(_json, resp.status, "delete")


async def _publish(params, session):
    _in_query_parameters = PAYLOAD_FORMAT["publish"]["query"].keys()
    payload = prepare_payload(params, PAYLOAD_FORMAT["publish"])
    subdevice_type = get_subdevice_type(
        "/rest/com/vmware/content/local-library/id:{library_id}"
    )
    if subdevice_type and not params[subdevice_type]:
        _json = await exists(params, session, build_url(params))
        if _json:
            params[subdevice_type] = _json["id"]
    _url = (
        "https://{vcenter_hostname}"
        "/rest/com/vmware/content/local-library/id:{library_id}"
    ).format(**params) + gen_args(params, _in_query_parameters)
    async with session.post(_url, json=payload) as resp:
        try:
            if resp.headers["Content-Type"] == "application/json":
                _json = await resp.json()
        except KeyError:
            _json = {}
        return await update_changed_flag(_json, resp.status, "publish")


async def _update(params, session):
    payload = prepare_payload(params, PAYLOAD_FORMAT["update"])
    _url = (
        "https://{vcenter_hostname}"
        "/rest/com/vmware/content/local-library/id:{library_id}"
    ).format(**params)
    async with session.get(_url) as resp:
        _json = await resp.json()
        for k, v in _json["value"].items():
            if k in payload and payload[k] == v:
                del payload[k]
            elif "spec" in payload:
                if k in payload["spec"] and payload["spec"][k] == v:
                    del payload["spec"][k]

        if payload == {} or payload == {"spec": {}}:
            # Nothing has changed
            _json["id"] = params.get("library_id")
            return await update_changed_flag(_json, resp.status, "get")
    async with session.patch(_url, json=payload) as resp:
        try:
            if resp.headers["Content-Type"] == "application/json":
                _json = await resp.json()
        except KeyError:
            _json = {}
        _json["id"] = params.get("library_id")
        return await update_changed_flag(_json, resp.status, "update")


if __name__ == "__main__":
    import asyncio

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
