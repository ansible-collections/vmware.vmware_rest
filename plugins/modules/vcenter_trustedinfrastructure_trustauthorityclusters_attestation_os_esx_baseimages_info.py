#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = """
module: vcenter_trustedinfrastructure_trustauthorityclusters_attestation_os_esx_baseimages_info
short_description: Handle resource of type vcenter_trustedinfrastructure_trustauthorityclusters_attestation_os_esx_baseimages
description: Handle resource of type vcenter_trustedinfrastructure_trustauthorityclusters_attestation_os_esx_baseimages
options:
  cluster:
    description:
    - The id of the cluster on which the operation will be executed.
    - 'The parameter must be an identifier for the resource type: ClusterComputeResource.'
    type: str
  display_name:
    description:
    - Search criteria by ESX base image version version numbers.
    - displayName if {@term.unset} return all ESX display version numbers.
    type: list
  health:
    description:
    - Search criteria by health indicator.
    - health if {@term.unset} return all health indicators.
    type: list
  version:
    description:
    - Search criteria by ESX base image version numbers.
    - version if {@term.unset} return all ESX version numbers.
    - 'When clients pass a value of this structure as a parameter, the field must
      contain identifiers for the resource type: vcenter.trusted_infrastructure.trust_authority_clusters.attestation.os.esx.BaseImage.
      When operations return a value of this structure as a result, the field will
      contain identifiers for the resource type: vcenter.trusted_infrastructure.trust_authority_clusters.attestation.os.esx.BaseImage.'
    type: str
  vmw-task:
    choices:
    - 'true'
    description:
    - vmw-task=true
    type: str
author:
- Ansible VMware team
version_added: 1.0.0
requirements:
- python >= 3.6
"""

IN_QUERY_PARAMETER = ["display_name", "health", "vmw-task"]

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

    argument_spec["cluster"] = {"type": "str", "operationIds": ["get", "list"]}
    argument_spec["display_name"] = {"type": "list", "operationIds": ["list"]}
    argument_spec["health"] = {"type": "list", "operationIds": ["list"]}
    argument_spec["version"] = {"type": "str", "operationIds": ["get", "list"]}
    argument_spec["vmw-task"] = {
        "type": "str",
        "choices": ["true"],
        "operationIds": ["get", "list"],
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

    if params["version"]:
        return "https://{vcenter_hostname}/rest/api/vcenter/trusted-infrastructure/trust-authority-clusters/{cluster}/attestation/os/esx/base-images/{version}".format(
            **params
        ) + gen_args(
            params, IN_QUERY_PARAMETER
        )
    else:
        return "https://{vcenter_hostname}/rest/api/vcenter/trusted-infrastructure/trust-authority-clusters/{cluster}/attestation/os/esx/base-images".format(
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
