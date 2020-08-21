#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = """
module: content_library_subscriptions
short_description: Handle resource of type content_library_subscriptions
description: Handle resource of type content_library_subscriptions
options:
  client_token:
    description:
    - 'A unique token generated on the client for each creation request. The token
      should be a universally unique identifier (UUID), for example: {@code b8a2a2e3-2314-43cd-a871-6ede0f429751}.
      This token can be used to guarantee idempotent creation.'
    type: str
  library:
    description:
    - Identifier of the published library.
    type: str
  state:
    choices:
    - create
    - delete
    - update
    description: []
    type: str
  subscribed_library:
    description:
    - Specification for the subscribed library to be associated with the subscription.
      Required with I(state=['create'])
    - 'Validate attributes are:'
    - ' - C(location) (str): The {@name Location} defines the location of subscribed
      library relative to the published library.'
    - ' - C(new_subscribed_library) (dict): Specification for creating a new subscribed
      library associated with the subscription.'
    - ' - C(placement) (dict): Placement specification for the virtual machine template
      library items on the subscribed library.'
    - ' - C(subscribed_library) (str): Identifier of the existing subscribed library
      to associate with the subscription. Only the subscribed libraries for which
      {@link SubscriptionInfo#subscriptionUrl} property is set to the {@link PublishInfo#publishUrl}
      of the published library can be associated with the subscription.'
    - ' - C(target) (str): The {@name Target} defines the options related to the target
      subscribed library which will be associated with the subscription.'
    - ' - C(vcenter) (dict): Specification for the subscribed library''s vCenter Server
      instance.'
    type: dict
  subscribed_library_placement:
    description:
    - Placement specification for the virtual machine template items of the subscribed
      library. Updating this information will only affect new or updated items, existing
      items will not be moved. The entire placement configuration of the subscribed
      library will replaced by the new specification.
    - 'Validate attributes are:'
    - ' - C(cluster) (str): Cluster onto which the virtual machine template should
      be placed. If {@name #cluster} and {@name #resourcePool} are both specified,
      {@name #resourcePool} must belong to {@name #cluster}. If {@name #cluster} and
      {@name #host} are both specified, {@name #host} must be a member of {@name #cluster}.
      If {@name #resourcePool} or {@name #host} is specified, it is recommended that
      this {@term field} be {@term unset}.'
    - ' - C(folder) (str): Virtual machine folder into which the virtual machine template
      should be placed.'
    - ' - C(host) (str): Host onto which the virtual machine template should be placed.
      If {@name #host} and {@name #resourcePool} are both specified, {@name #resourcePool}
      must belong to {@name #host}. If {@name #host} and {@name #cluster} are both
      specified, {@name #host} must be a member of {@name #cluster}.'
    - ' - C(network) (str): Network that backs the virtual Ethernet adapters in the
      virtual machine template.'
    - ' - C(resource_pool) (str): Resource pool into which the virtual machine template
      should be placed.'
    type: dict
  subscribed_library_vcenter:
    description:
    - Specification for the subscribed library's vCenter Server instance.
    - 'Validate attributes are:'
    - ' - C(hostname) (str): The hostname of the subscribed library''s vCenter Server.'
    - ' - C(https_port) (int): The HTTPS port of the vCenter Server instance where
      the subscribed library exists.'
    type: dict
  subscription:
    description:
    - subscription identifier. Required with I(state=['delete', 'update'])
    type: str
author:
- Ansible VMware team
version_added: 1.0.0
requirements:
- python >= 3.6
"""

IN_QUERY_PARAMETER = []

import socket
import json
from ansible.module_utils.basic import env_fallback

try:
    from ansible_collections.cloud.common.plugins.module_utils.turbo.module import (
        AnsibleTurboModule as AnsibleModule,
    )
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
    argument_spec["library"] = {
        "type": "str",
        "operationIds": ["create", "delete", "update"],
    }
    argument_spec["state"] = {"type": "str", "choices": ["create", "delete", "update"]}
    argument_spec["subscribed_library"] = {"type": "dict", "operationIds": ["create"]}
    argument_spec["subscribed_library_placement"] = {
        "type": "dict",
        "operationIds": ["update"],
    }
    argument_spec["subscribed_library_vcenter"] = {
        "type": "dict",
        "operationIds": ["update"],
    }
    argument_spec["subscription"] = {
        "type": "str",
        "operationIds": ["delete", "update"],
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
            if isinstance(_json["value"], dict):
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
            if isinstance(_json["value"], dict):
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
