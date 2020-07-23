from __future__ import absolute_import, division, print_function

__metaclass__ = type
import socket
import json

DOCUMENTATION = "author:\n- Ansible VMware team\ndescription: Handle resource of type vcenter_ovf_libraryitem\nextends_documentation_fragment: []\nmodule: vcenter_ovf_libraryitem\nnotes:\n- Tested on vSphere 7.0\noptions:\n  client_token:\n    description:\n    - Client-generated token used to retry a request if the client fails to get a\n      response from the server. If the original request succeeded, the result of that\n      request will be returned, otherwise the operation will be retried.\n    type: str\n  create_spec:\n    description:\n    - Information used to create the OVF package from the source virtual machine or\n      virtual appliance. Required with I(state=['create'])\n    - 'Validate attributes are:'\n    - ' - C(description) (str): Description to use in the OVF descriptor stored in\n      the library item.'\n    - ' - C(flags) (list): Flags to use for OVF package creation. The supported flags\n      can be obtained using {@link ExportFlag#list}.'\n    - ' - C(name) (str): Name to use in the OVF descriptor stored in the library item.'\n    type: dict\n  deployment_spec:\n    description:\n    - Specification of how the OVF package should be deployed to the target. Required\n      with I(state=['deploy'])\n    - 'Validate attributes are:'\n    - ' - C(accept_all_EULA) (bool): Whether to accept all End User License Agreements.\n      See {@link OvfSummary#eulas}.'\n    - ' - C(additional_parameters) (list): Additional OVF parameters that may be needed\n      for the deployment. Additional OVF parameters may be required by the OVF descriptor\n      of the OVF package in the library item. Examples of OVF parameters that can\n      be specified through this {@term field} include, but are not limited to: <ul>\n      <li>{@link DeploymentOptionParams}</li> <li>{@link ExtraConfigParams}</li> <li>{@link\n      IpAllocationParams}</li> <li>{@link PropertyParams}</li> <li>{@link ScaleOutParams}</li>\n      <li>{@link VcenterExtensionParams}</li> </ul>'\n    - ' - C(annotation) (str): Annotation assigned to the deployed target virtual\n      machine or virtual appliance.'\n    - ' - C(default_datastore_id) (str): Default datastore to use for all sections\n      of type vmw:StorageSection in the OVF descriptor.'\n    - ' - C(flags) (list): Flags to be use for deployment. The supported flag values\n      can be obtained using {@link ImportFlag#list}.'\n    - ' - C(locale) (str): The locale to use for parsing the OVF descriptor.'\n    - ' - C(name) (str): Name assigned to the deployed target virtual machine or virtual\n      appliance.'\n    - ' - C(network_mappings) (list): Specification of the target network to use for\n      sections of type ovf:NetworkSection in the OVF descriptor. The key in the {@term\n      map} is the section identifier of the ovf:NetworkSection section in the OVF\n      descriptor and the value is the target network to be used for deployment.'\n    - ' - C(storage_mappings) (list): Specification of the target storage to use for\n      sections of type vmw:StorageGroupSection in the OVF descriptor. The key in the\n      {@term map} is the section identifier of the ovf:StorageGroupSection section\n      in the OVF descriptor and the value is the target storage specification to be\n      used for deployment. See {@link StorageGroupMapping}.'\n    - ' - C(storage_profile_id) (str): Default storage profile to use for all sections\n      of type vmw:StorageSection in the OVF descriptor.'\n    - ' - C(storage_provisioning) (str): The {@name DiskProvisioningType} defines\n      the virtual disk provisioning types that can be set for a disk on the target\n      platform.'\n    type: dict\n  ovf_library_item_id:\n    description:\n    - Identifier of the content library item containing the OVF package to be deployed.\n      Required with I(state=['deploy', 'filter'])\n    type: str\n  source:\n    description:\n    - Identifier of the virtual machine or virtual appliance to use as the source.\n      Required with I(state=['create'])\n    - 'Validate attributes are:'\n    - ' - C(id) (str): Identifier of the deployable resource.'\n    - ' - C(type) (str): Type of the deployable resource.'\n    type: dict\n  state:\n    choices:\n    - create\n    - deploy\n    - filter\n    description: []\n    type: str\n  target:\n    description:\n    - Specification of the target content library and library item.\n    - 'Validate attributes are:'\n    - ' - C(library_id) (str): Identifier of the library in which a new library item\n      should be created. This {@term field} is not used if the {@name #libraryItemId}\n      {@term field} is specified.'\n    - ' - C(library_item_id) (str): Identifier of the library item that should be\n      should be updated.'\n    type: dict\n  ~action:\n    choices:\n    - deploy\n    description:\n    - ~action=deploy Required with I(state=['deploy'])\n    type: str\nrequirements:\n- python >= 3.6\nshort_description: Handle resource of type vcenter_ovf_libraryitem\nversion_added: 1.0.0\n"
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
