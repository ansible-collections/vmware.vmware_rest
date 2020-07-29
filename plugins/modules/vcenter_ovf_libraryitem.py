from __future__ import absolute_import, division, print_function

__metaclass__ = type
import socket
import json

DOCUMENTATION = """
module: vcenter_ovf_libraryitem
short_description: Handle resource of type vcenter_ovf_libraryitem
description: Handle resource of type vcenter_ovf_libraryitem
options:
  client_token:
    description:
    - Client-generated token used to retry a request if the client fails to get a
      response from the server. If the original request succeeded, the result of that
      request will be returned, otherwise the operation will be retried.
    type: str
  create_spec:
    description:
    - Information used to create the OVF package from the source virtual machine or
      virtual appliance. Required with I(state=['create'])
    - 'Validate attributes are:'
    - ' - C(description) (str): Description to use in the OVF descriptor stored in
      the library item.'
    - ' - C(flags) (list): Flags to use for OVF package creation. The supported flags
      can be obtained using {@link ExportFlag#list}.'
    - ' - C(name) (str): Name to use in the OVF descriptor stored in the library item.'
    type: dict
  deployment_spec:
    description:
    - Specification of how the OVF package should be deployed to the target. Required
      with I(state=['deploy'])
    - 'Validate attributes are:'
    - ' - C(accept_all_EULA) (bool): Whether to accept all End User License Agreements.
      See {@link OvfSummary#eulas}.'
    - ' - C(additional_parameters) (list): Additional OVF parameters that may be needed
      for the deployment. Additional OVF parameters may be required by the OVF descriptor
      of the OVF package in the library item. Examples of OVF parameters that can
      be specified through this {@term field} include, but are not limited to: <ul>
      <li>{@link DeploymentOptionParams}</li> <li>{@link ExtraConfigParams}</li> <li>{@link
      IpAllocationParams}</li> <li>{@link PropertyParams}</li> <li>{@link ScaleOutParams}</li>
      <li>{@link VcenterExtensionParams}</li> </ul>'
    - ' - C(annotation) (str): Annotation assigned to the deployed target virtual
      machine or virtual appliance.'
    - ' - C(default_datastore_id) (str): Default datastore to use for all sections
      of type vmw:StorageSection in the OVF descriptor.'
    - ' - C(flags) (list): Flags to be use for deployment. The supported flag values
      can be obtained using {@link ImportFlag#list}.'
    - ' - C(locale) (str): The locale to use for parsing the OVF descriptor.'
    - ' - C(name) (str): Name assigned to the deployed target virtual machine or virtual
      appliance.'
    - ' - C(network_mappings) (list): Specification of the target network to use for
      sections of type ovf:NetworkSection in the OVF descriptor. The key in the {@term
      map} is the section identifier of the ovf:NetworkSection section in the OVF
      descriptor and the value is the target network to be used for deployment.'
    - ' - C(storage_mappings) (list): Specification of the target storage to use for
      sections of type vmw:StorageGroupSection in the OVF descriptor. The key in the
      {@term map} is the section identifier of the ovf:StorageGroupSection section
      in the OVF descriptor and the value is the target storage specification to be
      used for deployment. See {@link StorageGroupMapping}.'
    - ' - C(storage_profile_id) (str): Default storage profile to use for all sections
      of type vmw:StorageSection in the OVF descriptor.'
    - ' - C(storage_provisioning) (str): The {@name DiskProvisioningType} defines
      the virtual disk provisioning types that can be set for a disk on the target
      platform.'
    type: dict
  ovf_library_item_id:
    description:
    - Identifier of the content library item containing the OVF package to be deployed.
      Required with I(state=['deploy', 'filter'])
    type: str
  source:
    description:
    - Identifier of the virtual machine or virtual appliance to use as the source.
      Required with I(state=['create'])
    - 'Validate attributes are:'
    - ' - C(id) (str): Identifier of the deployable resource.'
    - ' - C(type) (str): Type of the deployable resource.'
    type: dict
  state:
    choices:
    - create
    - deploy
    - filter
    description: []
    type: str
  target:
    description:
    - Specification of the target content library and library item.
    - 'Validate attributes are:'
    - ' - C(library_id) (str): Identifier of the library in which a new library item
      should be created. This {@term field} is not used if the {@name #libraryItemId}
      {@term field} is specified.'
    - ' - C(library_item_id) (str): Identifier of the library item that should be
      should be updated.'
    type: dict
  ~action:
    choices:
    - deploy
    description:
    - ~action=deploy Required with I(state=['deploy'])
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
        "choices": ["deploy"],
        "operationIds": ["deploy"],
    }
    argument_spec["target"] = {
        "type": "dict",
        "operationIds": ["create", "deploy", "filter"],
    }
    argument_spec["state"] = {"type": "str", "choices": ["create", "deploy", "filter"]}
    argument_spec["source"] = {"type": "dict", "operationIds": ["create"]}
    argument_spec["ovf_library_item_id"] = {
        "type": "str",
        "operationIds": ["deploy", "filter"],
    }
    argument_spec["deployment_spec"] = {"type": "dict", "operationIds": ["deploy"]}
    argument_spec["create_spec"] = {"type": "dict", "operationIds": ["create"]}
    argument_spec["client_token"] = {
        "type": "str",
        "operationIds": ["create", "deploy"],
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
    return "https://{vcenter_hostname}/rest/com/vmware/vcenter/ovf/library-item".format(
        **params
    )


async def entry_point(module, session):
    func = globals()[("_" + module.params["state"])]
    return await func(module.params, session)


async def _create(params, session):
    accepted_fields = ["client_token", "create_spec", "source", "target"]
    if "create" == "create":
        _exists = await exists(params, session)
        if _exists:
            return await update_changed_flag({"value": _exists}, 200, "get")
    spec = {}
    for i in accepted_fields:
        if params[i]:
            spec[i] = params[i]
    _url = "https://{vcenter_hostname}/rest/com/vmware/vcenter/ovf/library-item".format(
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


async def _deploy(params, session):
    accepted_fields = ["client_token", "deployment_spec", "target"]
    if "deploy" == "create":
        _exists = await exists(params, session)
        if _exists:
            return await update_changed_flag({"value": _exists}, 200, "get")
    spec = {}
    for i in accepted_fields:
        if params[i]:
            spec[i] = params[i]
    _url = "https://{vcenter_hostname}/rest/com/vmware/vcenter/ovf/library-item/id:{ovf_library_item_id}".format(
        **params
    )
    async with session.post(_url, json={"spec": spec}) as resp:
        try:
            if resp.headers["Content-Type"] == "application/json":
                _json = await resp.json()
        except KeyError:
            _json = {}
        if (
            ("deploy" == "create")
            and (resp.status in [200, 201])
            and ("value" in _json)
        ):
            if type(_json["value"]) == dict:
                _id = list(_json["value"].values())[0]
            else:
                _id = _json["value"]
            _json = {"value": (await get_device_info(params, session, _url, _id))}
        return await update_changed_flag(_json, resp.status, "deploy")


async def _filter(params, session):
    accepted_fields = ["target"]
    if "filter" == "create":
        _exists = await exists(params, session)
        if _exists:
            return await update_changed_flag({"value": _exists}, 200, "get")
    spec = {}
    for i in accepted_fields:
        if params[i]:
            spec[i] = params[i]
    _url = "https://{vcenter_hostname}/rest/com/vmware/vcenter/ovf/library-item/id:{ovf_library_item_id}?~action=filter".format(
        **params
    )
    async with session.post(_url, json={"spec": spec}) as resp:
        try:
            if resp.headers["Content-Type"] == "application/json":
                _json = await resp.json()
        except KeyError:
            _json = {}
        if (
            ("filter" == "create")
            and (resp.status in [200, 201])
            and ("value" in _json)
        ):
            if type(_json["value"]) == dict:
                _id = list(_json["value"].values())[0]
            else:
                _id = _json["value"]
            _json = {"value": (await get_device_info(params, session, _url, _id))}
        return await update_changed_flag(_json, resp.status, "filter")


if __name__ == "__main__":
    import asyncio

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
