from __future__ import absolute_import, division, print_function

__metaclass__ = type
import socket
import json

DOCUMENTATION = "author:\n- Ansible VMware team\ndescription: Handle resource of type vcenter_vcha_cluster_passive\nextends_documentation_fragment: []\nmodule: vcenter_vcha_cluster_passive\nnotes:\n- Tested on vSphere 7.0\noptions:\n  failover_ip:\n    description:\n    - 'Failover IP address that this node must assume after the failover to serve\n      client requests.\n\n      If unset, then the public IP address of the Active vCenter Server is assumed.'\n    - 'Validate attributes are:'\n    - ' - C(default_gateway) (str): The IP address of the Gateway for this interface.\n\n      If unset, gateway will not be used for the network interface.'\n    - ' - C(dns_servers) (list): The list of IP addresses of the DNS servers for this\n      interface. This list is a comma separated list.\n\n      If unset, DNS servers will not be used for the network interface.'\n    - ' - C(ip_family) (str): The IpFamily enumerated type defines the Ip address\n      family.'\n    - ' - C(ipv4) (dict): If the family of the ip is IPV4, then this will point to\n      IPv4 address specification.\n\n      This field is optional and it is only relevant when the value of IpSpec.ip-family\n      is IPV4.'\n    - ' - C(ipv6) (dict): If the family of the ip is IPV6, then this will point to\n      IPv6 address specification.\n\n      This field is optional and it is only relevant when the value of IpSpec.ip-family\n      is IPV6.'\n    type: dict\n  ha_ip:\n    description:\n    - 'Contains the VCHA HA network configuration of the node. All cluster communication\n      (state replication, heartbeat, cluster messages) happens over this network.\n\n      If unset, then the stored network configuration for the VCHA HA network for\n      the passive node will be used.'\n    - 'Validate attributes are:'\n    - ' - C(default_gateway) (str): The IP address of the Gateway for this interface.\n\n      If unset, gateway will not be used for the network interface.'\n    - ' - C(dns_servers) (list): The list of IP addresses of the DNS servers for this\n      interface. This list is a comma separated list.\n\n      If unset, DNS servers will not be used for the network interface.'\n    - ' - C(ip_family) (str): The IpFamily enumerated type defines the Ip address\n      family.'\n    - ' - C(ipv4) (dict): If the family of the ip is IPV4, then this will point to\n      IPv4 address specification.\n\n      This field is optional and it is only relevant when the value of IpSpec.ip-family\n      is IPV4.'\n    - ' - C(ipv6) (dict): If the family of the ip is IPV6, then this will point to\n      IPv6 address specification.\n\n      This field is optional and it is only relevant when the value of IpSpec.ip-family\n      is IPV6.'\n    type: dict\n  placement:\n    description:\n    - Contains the node's placement information.\n    - 'Validate attributes are:'\n    - ' - C(folder) (str): The identifier of the folder to deploy the VCHA node to.\n\n      When clients pass a value of this structure as a parameter, the field must be\n      an identifier for the resource type: Folder:VCenter. When operations return\n      a value of this structure as a result, the field will be an identifier for the\n      resource type: Folder:VCenter.'\n    - \" - C(ha_network) (str): The identifier of the Network object used for the HA\\\n      \\ network.\\n If the PlacementSpec.ha-network field is set, then the {#link #haNetworkType}\\\n      \\ field must be set.\\n If the PlacementSpec.ha-network field is unset, then\\\n      \\ the PlacementSpec.ha-network-type field is ignored.\\nIf unset and the PlacementSpec.ha-network-type\\\n      \\ field is unset, then the same network present on the Active node virtual machine\\\n      \\ is used to deploy the virtual machine with an assumption that the network\\\n      \\ is present on the destination.\\n\\nWhen clients pass a value of this structure\\\n      \\ as a parameter, the field must be an identifier for the resource type: Network:VCenter.\\\n      \\ When operations return a value of this structure as a result, the field will\\\n      \\ be an identifier for the resource type: Network:VCenter.\"\n    - ' - C(ha_network_type) (str): The NetworkType enumerated type defines the type\n      of a vCenter Server network.'\n    - ' - C(host) (str): The identifier of the host to deploy the VCHA node to.\n\n      If unset, see vim.vm.RelocateSpec.host.\n\n      When clients pass a value of this structure as a parameter, the field must be\n      an identifier for the resource type: HostSystem:VCenter. When operations return\n      a value of this structure as a result, the field will be an identifier for the\n      resource type: HostSystem:VCenter.'\n    - \" - C(management_network) (str): The identifier of the Network object used for\\\n      \\ the Management network. If the PlacementSpec.management-network field is set,\\\n      \\ then the PlacementSpec.management-network-type field must be set.\\n If the\\\n      \\ PlacementSpec.management-network field is unset, then the PlacementSpec.management-network-type\\\n      \\ field is ignored.\\nIf unset and the PlacementSpec.management-network-type\\\n      \\ field is unset, then the same network present on the Active node virtual machine\\\n      \\ is used to deploy the virtual machine with an assumption that the network\\\n      \\ is present on the destination.\\n\\nWhen clients pass a value of this structure\\\n      \\ as a parameter, the field must be an identifier for the resource type: Network:VCenter.\\\n      \\ When operations return a value of this structure as a result, the field will\\\n      \\ be an identifier for the resource type: Network:VCenter.\"\n    - ' - C(management_network_type) (str): The NetworkType enumerated type defines\n      the type of a vCenter Server network.'\n    - ' - C(name) (str): The name of the VCHA node to be used for the virtual machine\n      name.'\n    - ' - C(resource_pool) (str): The identifier of the resource pool to deploy the\n      VCHA node to.\n\n      If unset, then the active node''s resource pool will be used.\n\n      When clients pass a value of this structure as a parameter, the field must be\n      an identifier for the resource type: ResourcePool:VCenter. When operations return\n      a value of this structure as a result, the field will be an identifier for the\n      resource type: ResourcePool:VCenter.'\n    - ' - C(storage) (dict): The storage specification to deploy the VCHA node to.\n\n      If unset, see vim.vm.RelocateSpec.datastore.'\n    type: dict\n  state:\n    choices:\n    - redeploy\n    - check\n    description: []\n    type: str\n  vc_spec:\n    description:\n    - 'Contains the active node''s management vCenter server credentials.\n\n      If unset, then the active vCenter Server instance is assumed to be either self-managed\n      or else in enhanced linked mode and managed by a linked vCenter Server instance.'\n    - 'Validate attributes are:'\n    - ' - C(active_location) (dict): Connection information for the management vCenter\n      Server of the Active Node in a VCHA Cluster.'\n    type: dict\n  vmw-task:\n    choices:\n    - 'true'\n    description:\n    - vmw-task=true Required with I(state=['redeploy'])\n    type: str\nrequirements:\n- python >= 3.6\nshort_description: Handle resource of type vcenter_vcha_cluster_passive\nversion_added: 1.0.0\n"
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
    argument_spec["vmw-task"] = {
        "type": "str",
        "choices": ["true"],
        "operationIds": ["redeploy"],
    }
    argument_spec["vc_spec"] = {"type": "dict", "operationIds": ["check", "redeploy"]}
    argument_spec["state"] = {"type": "str", "choices": ["check", "redeploy"]}
    argument_spec["placement"] = {"type": "dict", "operationIds": ["check", "redeploy"]}
    argument_spec["ha_ip"] = {"type": "dict", "operationIds": ["redeploy"]}
    argument_spec["failover_ip"] = {"type": "dict", "operationIds": ["redeploy"]}
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
    return "https://{vcenter_hostname}/rest/vcenter/vcha/cluster/passive".format(
        **params
    )


async def entry_point(module, session):
    func = globals()[("_" + module.params["state"])]
    return await func(module.params, session)


async def _check(params, session):
    accepted_fields = ["placement", "vc_spec"]
    if "check" == "create":
        _exists = await exists(params, session)
        if _exists:
            return await update_changed_flag({"value": _exists}, 200, "get")
    spec = {}
    for i in accepted_fields:
        if params[i]:
            spec[i] = params[i]
    _url = "https://{vcenter_hostname}/rest/vcenter/vcha/cluster/passive?action=check".format(
        **params
    )
    async with session.post(_url, json={"spec": spec}) as resp:
        try:
            if resp.headers["Content-Type"] == "application/json":
                _json = await resp.json()
        except KeyError:
            _json = {}
        if ("check" == "create") and (resp.status in [200, 201]) and ("value" in _json):
            if type(_json["value"]) == dict:
                _id = list(_json["value"].values())[0]
            else:
                _id = _json["value"]
            _json = {"value": (await get_device_info(params, session, _url, _id))}
        return await update_changed_flag(_json, resp.status, "check")


async def _redeploy(params, session):
    accepted_fields = ["failover_ip", "ha_ip", "placement", "vc_spec"]
    if "redeploy" == "create":
        _exists = await exists(params, session)
        if _exists:
            return await update_changed_flag({"value": _exists}, 200, "get")
    spec = {}
    for i in accepted_fields:
        if params[i]:
            spec[i] = params[i]
    _url = "https://{vcenter_hostname}/rest/vcenter/vcha/cluster/passive".format(
        **params
    )
    async with session.post(_url, json={"spec": spec}) as resp:
        try:
            if resp.headers["Content-Type"] == "application/json":
                _json = await resp.json()
        except KeyError:
            _json = {}
        if (
            ("redeploy" == "create")
            and (resp.status in [200, 201])
            and ("value" in _json)
        ):
            if type(_json["value"]) == dict:
                _id = list(_json["value"].values())[0]
            else:
                _id = _json["value"]
            _json = {"value": (await get_device_info(params, session, _url, _id))}
        return await update_changed_flag(_json, resp.status, "redeploy")


if __name__ == "__main__":
    import asyncio

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
