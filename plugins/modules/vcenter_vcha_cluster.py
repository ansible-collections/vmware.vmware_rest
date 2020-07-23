from __future__ import absolute_import, division, print_function

__metaclass__ = type
import socket
import json

DOCUMENTATION = "author:\n- Ansible VMware team\ndescription: Handle resource of type vcenter_vcha_cluster\nextends_documentation_fragment: []\nmodule: vcenter_vcha_cluster\nnotes:\n- Tested on vSphere 7.0\noptions:\n  active:\n    description:\n    - Contains the active node's network configuration. Required with I(state=['deploy'])\n    - 'Validate attributes are:'\n    - ' - C(ha_ip) (dict): IP specification for the HA network.'\n    - \" - C(ha_network) (str): The identifier of the Network object used for the HA\\\n      \\ network.\\n If the Cluster.ActiveSpec.ha-network field is set, then the Cluster.ActiveSpec.ha-network-type\\\n      \\ field must be set.\\n If the Cluster.ActiveSpec.ha-network field is unset,\\\n      \\ then the Cluster.ActiveSpec.ha-network-type field is ignored.\\nIf unset and\\\n      \\ the Cluster.ActiveSpec.ha-network-type field is unset, then the second NIC\\\n      \\ is assumed to be already configured.\\n If unset and the Cluster.ActiveSpec.ha-network\\\n      \\ field is set, then an error is reported.\\nWhen clients pass a value of this\\\n      \\ structure as a parameter, the field must be an identifier for the resource\\\n      \\ type: Network:VCenter. When operations return a value of this structure as\\\n      \\ a result, the field will be an identifier for the resource type: Network:VCenter.\"\n    - ' - C(ha_network_type) (str): The NetworkType enumerated type defines the type\n      of a vCenter Server network.'\n    type: dict\n  deployment:\n    choices:\n    - AUTO\n    - MANUAL\n    description:\n    - The Cluster.Type enumerated type defines the possible deployment types for a\n      VCHA Cluster. Required with I(state=['deploy'])\n    type: str\n  force_delete:\n    description:\n    - \"Flag controlling in what circumstances the virtual machines will be deleted.\\\n      \\ For this flag to take effect, the VCHA cluster should have been successfully\\\n      \\ configured using automatic deployment. \\n   -  If true, the Cluster.UndeploySpec.vms\\\n      \\ field will be ignored, the VCHA cluster specific information is removed, and\\\n      \\ the passive and witness virtual machines will be deleted.\\n   -  If false,\\\n      \\ the Cluster.UndeploySpec.vms field contains the information identifying the\\\n      \\ passive and witness virtual machines.\\n \\n     =  If the Cluster.UndeploySpec.vms\\\n      \\ field is set, then it will be validated prior to deleting the passive and\\\n      \\ witness virtual machines and VCHA cluster specific information is removed.\\n\\\n      \\     =  If the Cluster.UndeploySpec.vms field is unset, then the passive and\\\n      \\ witness virtual machines will not be deleted. The customer should delete them\\\n      \\ in order to cleanup completely. VCHA cluster specific information is removed.\\n\\\n      \\  \\nIf unset, the Cluster.UndeploySpec.vms field contains the information identifying\\\n      \\ the passive and witness virtual machines. \\n   -  If the Cluster.UndeploySpec.vms\\\n      \\ field is set, then it will be validated prior to deleting the passive and\\\n      \\ witness virtual machines. VCHA cluster specific information is removed.\\n\\\n      \\   -  If the Cluster.UndeploySpec.vms field is unset, then the passive and\\\n      \\ witness virtual machines will not be deleted. The customer should delete them\\\n      \\ in order to cleanup completely. VCHA cluster specific information is removed.\\n\"\n    type: bool\n  passive:\n    description:\n    - Contains the passive node's placement configuration. Required with I(state=['deploy'])\n    - 'Validate attributes are:'\n    - ' - C(failover_ip) (dict): IP specification for the management network.\n\n      If unset, then it will assume the public IP address of the Active vCenter Server.'\n    - ' - C(ha_ip) (dict): IP specification for the HA network.'\n    - ' - C(placement) (dict): Contains the placement configuration of the node.\n\n      If unset, then the it is assumed that the clone will be done manually by the\n      customer. In this case, the placement configuration for the witness node should\n      also be omitted. Only the network configuration will be setup. Once the passive\n      and witness nodes are cloned from the active node, the VCHA high availability\n      is turned on.'\n    type: dict\n  planned:\n    description:\n    - \"If false, a failover is initiated immediately and may result in data loss.\\n\\\n      \\ If true, a failover is initated after the Active node flushes its state to\\\n      \\ Passive and there is no data loss. Required with I(state=['failover'])\"\n    type: bool\n  state:\n    choices:\n    - undeploy\n    - deploy\n    - failover\n    description: []\n    type: str\n  vc_spec:\n    description:\n    - 'Contains the active node''s management vCenter server credentials.\n\n      If unset, then the active vCenter Server instance is assumed to be either self-managed\n      or else in enhanced linked mode and managed by a linked vCenter Server instance.'\n    - 'Validate attributes are:'\n    - ' - C(active_location) (dict): Connection information for the management vCenter\n      Server of the Active Node in a VCHA Cluster.'\n    type: dict\n  vms:\n    description:\n    - \"Contains virtual machine information for the passive and witness virtual machines.\\\n      \\ For this flag to take effect, the VCHA cluster should have been successfully\\\n      \\ configured using automatic deployment. \\n If set, the Cluster.UndeploySpec.force-delete\\\n      \\ field controls whether this information is validated. \\n\\n   -  If the Cluster.UndeploySpec.force-delete\\\n      \\ field is true, then this information is ignored, VCHA cluster specific information\\\n      \\ is removed and the passive and witness virtual machines will be deleted.\\n\\\n      \\   -  If the Cluster.UndeploySpec.force-delete field is unset or false, then\\\n      \\ this information is validated prior to deleting the passive and witness virtual\\\n      \\ machines. VCHA cluster specific information is removed.\\n \\nIf unset, the\\\n      \\ Cluster.UndeploySpec.force-delete field controls the deletion of the passive\\\n      \\ and witness virtual machines. \\n   -  If the Cluster.UndeploySpec.force-delete\\\n      \\ field is true, then the passive and witness virtual machines will be deleted.\\\n      \\ VCHA cluster specific information is removed. \\n  -  If the Cluster.UndeploySpec.force-delete\\\n      \\ field is unset or false, then the passive and witness virtual machines will\\\n      \\ not be deleted. The customer should delete them in order to cleanup completely.\\\n      \\ VCHA cluster specific information is removed. \\n\"\n    - 'Validate attributes are:'\n    - ' - C(passive) (dict): The virtual machine information of the passive node.'\n    - ' - C(witness) (dict): The virtual machine information of the witness node.'\n    type: dict\n  vmw-task:\n    choices:\n    - 'true'\n    description:\n    - vmw-task=true Required with I(state=['failover'])\n    type: str\n  witness:\n    description:\n    - Contains the witness node's placement configuration. Required with I(state=['deploy'])\n    - 'Validate attributes are:'\n    - ' - C(ha_ip) (dict): IP specification for the HA network.'\n    - ' - C(placement) (dict): Contains the placement configuration of the node.\n\n      If unset, then it is assumed that the clone will be done manually by the customer.\n      In this case, the placement configuration for the witness node should also be\n      omitted. Only the network configuration will be setup. Once the passive and\n      witness nodes are cloned from the active node, the VCHA high availability is\n      turned on.'\n    type: dict\nrequirements:\n- python >= 3.6\nshort_description: Handle resource of type vcenter_vcha_cluster\nversion_added: 1.0.0\n"
IN_QUERY_PARAMETER = ["vmw-task"]
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
    argument_spec["witness"] = {"type": "dict", "operationIds": ["deploy"]}
    argument_spec["vmw-task"] = {
        "type": "str",
        "choices": ["true"],
        "operationIds": ["failover"],
    }
    argument_spec["vms"] = {"type": "dict", "operationIds": ["undeploy"]}
    argument_spec["vc_spec"] = {"type": "dict", "operationIds": ["deploy", "undeploy"]}
    argument_spec["state"] = {
        "type": "str",
        "choices": ["deploy", "failover", "undeploy"],
    }
    argument_spec["planned"] = {"type": "bool", "operationIds": ["failover"]}
    argument_spec["passive"] = {"type": "dict", "operationIds": ["deploy"]}
    argument_spec["force_delete"] = {"type": "bool", "operationIds": ["undeploy"]}
    argument_spec["deployment"] = {
        "type": "str",
        "choices": ["AUTO", "MANUAL"],
        "operationIds": ["deploy"],
    }
    argument_spec["active"] = {"type": "dict", "operationIds": ["deploy"]}
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
    return "https://{vcenter_hostname}/rest/vcenter/vcha/cluster".format(**params)


async def entry_point(module, session):
    func = globals()[("_" + module.params["state"])]
    return await func(module.params, session)


async def _deploy(params, session):
    accepted_fields = ["active", "deployment", "passive", "vc_spec", "witness"]
    if "deploy" == "create":
        _exists = await exists(params, session)
        if _exists:
            return await update_changed_flag({"value": _exists}, 200, "get")
    spec = {}
    for i in accepted_fields:
        if params[i]:
            spec[i] = params[i]
    _url = "https://{vcenter_hostname}/rest/vcenter/vcha/cluster?action=deploy&vmw-task=true".format(
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


async def _failover(params, session):
    accepted_fields = ["planned"]
    if "failover" == "create":
        _exists = await exists(params, session)
        if _exists:
            return await update_changed_flag({"value": _exists}, 200, "get")
    spec = {}
    for i in accepted_fields:
        if params[i]:
            spec[i] = params[i]
    _url = "https://{vcenter_hostname}/rest/vcenter/vcha/cluster".format(**params)
    async with session.post(_url, json={"spec": spec}) as resp:
        try:
            if resp.headers["Content-Type"] == "application/json":
                _json = await resp.json()
        except KeyError:
            _json = {}
        if (
            ("failover" == "create")
            and (resp.status in [200, 201])
            and ("value" in _json)
        ):
            if type(_json["value"]) == dict:
                _id = list(_json["value"].values())[0]
            else:
                _id = _json["value"]
            _json = {"value": (await get_device_info(params, session, _url, _id))}
        return await update_changed_flag(_json, resp.status, "failover")


async def _undeploy(params, session):
    accepted_fields = ["force_delete", "vc_spec", "vms"]
    if "undeploy" == "create":
        _exists = await exists(params, session)
        if _exists:
            return await update_changed_flag({"value": _exists}, 200, "get")
    spec = {}
    for i in accepted_fields:
        if params[i]:
            spec[i] = params[i]
    _url = "https://{vcenter_hostname}/rest/vcenter/vcha/cluster?action=undeploy&vmw-task=true".format(
        **params
    )
    async with session.post(_url, json={"spec": spec}) as resp:
        try:
            if resp.headers["Content-Type"] == "application/json":
                _json = await resp.json()
        except KeyError:
            _json = {}
        if (
            ("undeploy" == "create")
            and (resp.status in [200, 201])
            and ("value" in _json)
        ):
            if type(_json["value"]) == dict:
                _id = list(_json["value"].values())[0]
            else:
                _id = _json["value"]
            _json = {"value": (await get_device_info(params, session, _url, _id))}
        return await update_changed_flag(_json, resp.status, "undeploy")


if __name__ == "__main__":
    import asyncio

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
