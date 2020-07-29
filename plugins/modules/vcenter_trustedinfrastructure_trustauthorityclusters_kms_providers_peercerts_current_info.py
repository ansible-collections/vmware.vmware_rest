from __future__ import absolute_import, division, print_function

__metaclass__ = type
import socket
import json

DOCUMENTATION = """
module: vcenter_trustedinfrastructure_trustauthorityclusters_kms_providers_peercerts_current_info
short_description: Handle resource of type vcenter_trustedinfrastructure_trustauthorityclusters_kms_providers_peercerts_current
description: Handle resource of type vcenter_trustedinfrastructure_trustauthorityclusters_kms_providers_peercerts_current
options:
  cluster:
    description:
    - Identifier of the cluster.
    - 'The parameter must be an identifier for the resource type: ClusterComputeResource.
      Required with I(state=[''list''])'
    type: str
  provider:
    description:
    - Identifier of the provider.
    - 'The parameter must be an identifier for the resource type: vcenter.trusted_infrastructure.trust_authority_clusters.kms.Provider.
      Required with I(state=[''list''])'
    type: str
  server_names:
    description:
    - Names that key server must have to match the filter (see CurrentPeerCertificates.Summary.server-name).
    - If unset or empty, key servers with any name match the filter.
    type: list
  trusted:
    description:
    - Trust status that server certificates must have to match the filter (see CurrentPeerCertificates.Summary.trusted).
    - If unset, trusted and untrusted server certificates match the filter.
    type: bool
  vmw-task:
    choices:
    - 'true'
    description:
    - vmw-task=true Required with I(state=['list'])
    type: str
author:
- Ansible VMware team
version_added: 1.0.0
requirements:
- python >= 3.6
"""
IN_QUERY_PARAMETER = ["server_names", "trusted", "vmw-task"]
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
        "operationIds": ["list"],
    }
    argument_spec["trusted"] = {"type": "bool", "operationIds": ["list"]}
    argument_spec["server_names"] = {"type": "list", "operationIds": ["list"]}
    argument_spec["provider"] = {"type": "str", "operationIds": ["list"]}
    argument_spec["cluster"] = {"type": "str", "operationIds": ["list"]}
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
    return "https://{vcenter_hostname}/rest/api/vcenter/trusted-infrastructure/trust-authority-clusters/{cluster}/kms/providers/{provider}/peer-certs/current".format(
        **params
    ) + gen_args(
        params, IN_QUERY_PARAMETER
    )


async def entry_point(module, session):
    async with session.get(url(module.params)) as resp:
        _json = await resp.json()
        return await update_changed_flag(_json, resp.status, "get")


if __name__ == "__main__":
    import asyncio

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
