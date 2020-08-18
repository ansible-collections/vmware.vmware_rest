#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = """
module: vcenter_vcha_cluster
short_description: Handle resource of type vcenter_vcha_cluster
description: Handle resource of type vcenter_vcha_cluster
options:
  active:
    description:
    - Contains the active node's network configuration. Required with I(state=['deploy'])
    - 'Validate attributes are:'
    - ' - C(ha_ip) (dict): IP specification for the HA network.'
    - ' - C(ha_network) (str): The identifier of the Network object used for the HA
      network.'
    - ' If the Cluster.ActiveSpec.ha-network field is set, then the Cluster.ActiveSpec.ha-network-type
      field must be set.'
    - ' If the Cluster.ActiveSpec.ha-network field is unset, then the Cluster.ActiveSpec.ha-network-type
      field is ignored.'
    - If unset and the Cluster.ActiveSpec.ha-network-type field is unset, then the
      second NIC is assumed to be already configured.
    - ' If unset and the Cluster.ActiveSpec.ha-network field is set, then an error
      is reported.'
    - 'When clients pass a value of this structure as a parameter, the field must
      be an identifier for the resource type: Network:VCenter. When operations return
      a value of this structure as a result, the field will be an identifier for the
      resource type: Network:VCenter.'
    - ' - C(ha_network_type) (str): The NetworkType enumerated type defines the type
      of a vCenter Server network.'
    type: dict
  deployment:
    choices:
    - AUTO
    - MANUAL
    description:
    - The Cluster.Type enumerated type defines the possible deployment types for a
      VCHA Cluster. Required with I(state=['deploy'])
    type: str
  force_delete:
    description:
    - 'Flag controlling in what circumstances the virtual machines will be deleted.
      For this flag to take effect, the VCHA cluster should have been successfully
      configured using automatic deployment. '
    - '   -  If true, the Cluster.UndeploySpec.vms field will be ignored, the VCHA
      cluster specific information is removed, and the passive and witness virtual
      machines will be deleted.'
    - '   -  If false, the Cluster.UndeploySpec.vms field contains the information
      identifying the passive and witness virtual machines.'
    - ' '
    - '     =  If the Cluster.UndeploySpec.vms field is set, then it will be validated
      prior to deleting the passive and witness virtual machines and VCHA cluster
      specific information is removed.'
    - '     =  If the Cluster.UndeploySpec.vms field is unset, then the passive and
      witness virtual machines will not be deleted. The customer should delete them
      in order to cleanup completely. VCHA cluster specific information is removed.'
    - '  '
    - 'If unset, the Cluster.UndeploySpec.vms field contains the information identifying
      the passive and witness virtual machines. '
    - '   -  If the Cluster.UndeploySpec.vms field is set, then it will be validated
      prior to deleting the passive and witness virtual machines. VCHA cluster specific
      information is removed.'
    - '   -  If the Cluster.UndeploySpec.vms field is unset, then the passive and
      witness virtual machines will not be deleted. The customer should delete them
      in order to cleanup completely. VCHA cluster specific information is removed.'
    type: bool
  passive:
    description:
    - Contains the passive node's placement configuration. Required with I(state=['deploy'])
    - 'Validate attributes are:'
    - ' - C(failover_ip) (dict): IP specification for the management network.'
    - If unset, then it will assume the public IP address of the Active vCenter Server.
    - ' - C(ha_ip) (dict): IP specification for the HA network.'
    - ' - C(placement) (dict): Contains the placement configuration of the node.'
    - If unset, then the it is assumed that the clone will be done manually by the
      customer. In this case, the placement configuration for the witness node should
      also be omitted. Only the network configuration will be setup. Once the passive
      and witness nodes are cloned from the active node, the VCHA high availability
      is turned on.
    type: dict
  planned:
    description:
    - If false, a failover is initiated immediately and may result in data loss.
    - ' If true, a failover is initated after the Active node flushes its state to
      Passive and there is no data loss. Required with I(state=[''failover''])'
    type: bool
  state:
    choices:
    - deploy
    - failover
    - undeploy
    description: []
    type: str
  vc_spec:
    description:
    - Contains the active node's management vCenter server credentials.
    - If unset, then the active vCenter Server instance is assumed to be either self-managed
      or else in enhanced linked mode and managed by a linked vCenter Server instance.
    - 'Validate attributes are:'
    - ' - C(active_location) (dict): Connection information for the management vCenter
      Server of the Active Node in a VCHA Cluster.'
    type: dict
  vms:
    description:
    - 'Contains virtual machine information for the passive and witness virtual machines.
      For this flag to take effect, the VCHA cluster should have been successfully
      configured using automatic deployment. '
    - ' If set, the Cluster.UndeploySpec.force-delete field controls whether this
      information is validated. '
    - '   -  If the Cluster.UndeploySpec.force-delete field is true, then this information
      is ignored, VCHA cluster specific information is removed and the passive and
      witness virtual machines will be deleted.'
    - '   -  If the Cluster.UndeploySpec.force-delete field is unset or false, then
      this information is validated prior to deleting the passive and witness virtual
      machines. VCHA cluster specific information is removed.'
    - ' '
    - 'If unset, the Cluster.UndeploySpec.force-delete field controls the deletion
      of the passive and witness virtual machines. '
    - '   -  If the Cluster.UndeploySpec.force-delete field is true, then the passive
      and witness virtual machines will be deleted. VCHA cluster specific information
      is removed. '
    - '  -  If the Cluster.UndeploySpec.force-delete field is unset or false, then
      the passive and witness virtual machines will not be deleted. The customer should
      delete them in order to cleanup completely. VCHA cluster specific information
      is removed. '
    - 'Validate attributes are:'
    - ' - C(passive) (dict): The virtual machine information of the passive node.'
    - ' - C(witness) (dict): The virtual machine information of the witness node.'
    type: dict
  vmw-task:
    choices:
    - 'true'
    description:
    - vmw-task=true Required with I(state=['failover'])
    type: str
  witness:
    description:
    - Contains the witness node's placement configuration. Required with I(state=['deploy'])
    - 'Validate attributes are:'
    - ' - C(ha_ip) (dict): IP specification for the HA network.'
    - ' - C(placement) (dict): Contains the placement configuration of the node.'
    - If unset, then it is assumed that the clone will be done manually by the customer.
      In this case, the placement configuration for the witness node should also be
      omitted. Only the network configuration will be setup. Once the passive and
      witness nodes are cloned from the active node, the VCHA high availability is
      turned on.
    type: dict
author:
- Ansible VMware team
version_added: 1.0.0
requirements:
- python >= 3.6
"""

IN_QUERY_PARAMETER = ["vmw-task"]

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

    argument_spec["active"] = {"type": "dict", "operationIds": ["deploy"]}
    argument_spec["deployment"] = {
        "type": "str",
        "choices": ["AUTO", "MANUAL"],
        "operationIds": ["deploy"],
    }
    argument_spec["force_delete"] = {"type": "bool", "operationIds": ["undeploy"]}
    argument_spec["passive"] = {"type": "dict", "operationIds": ["deploy"]}
    argument_spec["planned"] = {"type": "bool", "operationIds": ["failover"]}
    argument_spec["state"] = {
        "type": "str",
        "choices": ["deploy", "failover", "undeploy"],
    }
    argument_spec["vc_spec"] = {"type": "dict", "operationIds": ["deploy", "undeploy"]}
    argument_spec["vms"] = {"type": "dict", "operationIds": ["undeploy"]}
    argument_spec["vmw-task"] = {
        "type": "str",
        "choices": ["true"],
        "operationIds": ["failover"],
    }
    argument_spec["witness"] = {"type": "dict", "operationIds": ["deploy"]}

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
            if isinstance(_json["value"], dict):
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
            if isinstance(_json["value"], dict):
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
            if isinstance(_json["value"], dict):
                _id = list(_json["value"].values())[0]
            else:
                _id = _json["value"]
            _json = {"value": (await get_device_info(params, session, _url, _id))}
        return await update_changed_flag(_json, resp.status, "undeploy")


if __name__ == "__main__":
    import asyncio

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
