from __future__ import absolute_import, division, print_function

__metaclass__ = type
import socket
import json

DOCUMENTATION = """
module: vcenter_certificatemanagement_vcenter_tls
short_description: Handle resource of type vcenter_certificatemanagement_vcenter_tls
description: Handle resource of type vcenter_certificatemanagement_vcenter_tls
options:
  action:
    choices:
    - replace-vmca-signed
    description:
    - action=replace-vmca-signed Required with I(state=['replace_vmca_signed'])
    type: str
  cert:
    description:
    - Certificate string in PEM format. Required with I(state=['set'])
    type: str
  common_name:
    description:
    - The common name of the host for which certificate is generated
    - If unset will default to PNID of host.
    type: str
  country:
    description:
    - Country field in certificate subject Required with I(state=['replace_vmca_signed'])
    type: str
  duration:
    description:
    - The duration (in days) of the new TLS certificate. The duration should be less
      than or equal to 730 days.
    - If unset, the duration will be 730 days (two years).
    type: int
  email_address:
    description:
    - Email field in Certificate extensions Required with I(state=['replace_vmca_signed'])
    type: str
  key:
    description:
    - Private key string in PEM format.
    - If unset the private key from the certificate store will be used. It is required
      when replacing the certificate with a third party signed certificate.
    type: str
  key_size:
    description:
    - The size of the key to be used for public and private key generation.
    - If unset the key size will be '2048'.
    type: int
  locality:
    description:
    - Locality field in certificate subject Required with I(state=['replace_vmca_signed'])
    type: str
  organization:
    description:
    - Organization field in certificate subject Required with I(state=['replace_vmca_signed'])
    type: str
  organization_unit:
    description:
    - Organization unit field in certificate subject Required with I(state=['replace_vmca_signed'])
    type: str
  root_cert:
    description:
    - Third party Root CA certificate in PEM format.
    - If unset the new third party root CA certificate will not be added to the trust
      store. It is required when replacing the certificate with a third party signed
      certificate if the root certificate of the third party is not already a trusted
      root.
    type: str
  state:
    choices:
    - renew
    - replace_vmca_signed
    - set
    description: []
    type: str
  state_or_province:
    description:
    - State field in certificate subject Required with I(state=['replace_vmca_signed'])
    type: str
  subject_alt_name:
    description:
    - SubjectAltName is list of Dns Names and Ip addresses
    - If unset PNID of host will be used as IPAddress or Hostname for certificate
      generation .
    type: list
author:
- Ansible VMware team
version_added: 1.0.0
requirements:
- python >= 3.6
"""
IN_QUERY_PARAMETER = ["action"]
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
    argument_spec["subject_alt_name"] = {
        "type": "list",
        "operationIds": ["replace_vmca_signed"],
    }
    argument_spec["state_or_province"] = {
        "type": "str",
        "operationIds": ["replace_vmca_signed"],
    }
    argument_spec["state"] = {
        "type": "str",
        "choices": ["renew", "replace_vmca_signed", "set"],
    }
    argument_spec["root_cert"] = {"type": "str", "operationIds": ["set"]}
    argument_spec["organization_unit"] = {
        "type": "str",
        "operationIds": ["replace_vmca_signed"],
    }
    argument_spec["organization"] = {
        "type": "str",
        "operationIds": ["replace_vmca_signed"],
    }
    argument_spec["locality"] = {"type": "str", "operationIds": ["replace_vmca_signed"]}
    argument_spec["key_size"] = {"type": "int", "operationIds": ["replace_vmca_signed"]}
    argument_spec["key"] = {"type": "str", "operationIds": ["set"]}
    argument_spec["email_address"] = {
        "type": "str",
        "operationIds": ["replace_vmca_signed"],
    }
    argument_spec["duration"] = {"type": "int", "operationIds": ["renew"]}
    argument_spec["country"] = {"type": "str", "operationIds": ["replace_vmca_signed"]}
    argument_spec["common_name"] = {
        "type": "str",
        "operationIds": ["replace_vmca_signed"],
    }
    argument_spec["cert"] = {"type": "str", "operationIds": ["set"]}
    argument_spec["action"] = {
        "type": "str",
        "choices": ["replace-vmca-signed"],
        "operationIds": ["replace_vmca_signed"],
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
    return "https://{vcenter_hostname}/rest/vcenter/certificate-management/vcenter/tls".format(
        **params
    )


async def entry_point(module, session):
    func = globals()[("_" + module.params["state"])]
    return await func(module.params, session)


async def _renew(params, session):
    accepted_fields = ["duration"]
    if "renew" == "create":
        _exists = await exists(params, session)
        if _exists:
            return await update_changed_flag({"value": _exists}, 200, "get")
    spec = {}
    for i in accepted_fields:
        if params[i]:
            spec[i] = params[i]
    _url = "https://{vcenter_hostname}/rest/vcenter/certificate-management/vcenter/tls?action=renew".format(
        **params
    )
    async with session.post(_url, json={"spec": spec}) as resp:
        try:
            if resp.headers["Content-Type"] == "application/json":
                _json = await resp.json()
        except KeyError:
            _json = {}
        if ("renew" == "create") and (resp.status in [200, 201]) and ("value" in _json):
            if type(_json["value"]) == dict:
                _id = list(_json["value"].values())[0]
            else:
                _id = _json["value"]
            _json = {"value": (await get_device_info(params, session, _url, _id))}
        return await update_changed_flag(_json, resp.status, "renew")


async def _replace_vmca_signed(params, session):
    accepted_fields = [
        "common_name",
        "country",
        "email_address",
        "key_size",
        "locality",
        "organization",
        "organization_unit",
        "state_or_province",
        "subject_alt_name",
    ]
    if "replace_vmca_signed" == "create":
        _exists = await exists(params, session)
        if _exists:
            return await update_changed_flag({"value": _exists}, 200, "get")
    spec = {}
    for i in accepted_fields:
        if params[i]:
            spec[i] = params[i]
    _url = "https://{vcenter_hostname}/rest/vcenter/certificate-management/vcenter/tls".format(
        **params
    )
    async with session.post(_url, json={"spec": spec}) as resp:
        try:
            if resp.headers["Content-Type"] == "application/json":
                _json = await resp.json()
        except KeyError:
            _json = {}
        if (
            ("replace_vmca_signed" == "create")
            and (resp.status in [200, 201])
            and ("value" in _json)
        ):
            if type(_json["value"]) == dict:
                _id = list(_json["value"].values())[0]
            else:
                _id = _json["value"]
            _json = {"value": (await get_device_info(params, session, _url, _id))}
        return await update_changed_flag(_json, resp.status, "replace_vmca_signed")


async def _set(params, session):
    accepted_fields = ["cert", "key", "root_cert"]
    if "set" == "create":
        _exists = await exists(params, session)
        if _exists:
            return await update_changed_flag({"value": _exists}, 200, "get")
    spec = {}
    for i in accepted_fields:
        if params[i]:
            spec[i] = params[i]
    _url = "https://{vcenter_hostname}/rest/vcenter/certificate-management/vcenter/tls".format(
        **params
    )
    async with session.put(_url, json={"spec": spec}) as resp:
        try:
            if resp.headers["Content-Type"] == "application/json":
                _json = await resp.json()
        except KeyError:
            _json = {}
        if ("set" == "create") and (resp.status in [200, 201]) and ("value" in _json):
            if type(_json["value"]) == dict:
                _id = list(_json["value"].values())[0]
            else:
                _id = _json["value"]
            _json = {"value": (await get_device_info(params, session, _url, _id))}
        return await update_changed_flag(_json, resp.status, "set")


if __name__ == "__main__":
    import asyncio

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
