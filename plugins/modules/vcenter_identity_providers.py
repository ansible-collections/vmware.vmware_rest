from __future__ import absolute_import, division, print_function

__metaclass__ = type
import socket
import json

DOCUMENTATION = """
module: vcenter_identity_providers
short_description: Handle resource of type vcenter_identity_providers
description: Handle resource of type vcenter_identity_providers
options:
  active_directory_over_ldap:
    description:
    - Identity management configuration. If the protocol is LDAP, the configuration
      must be set, else InvalidArgument is thrown.
    - 'Validate attributes are:'
    - ' - C(cert_chain) (dict): SSL certificate chain in base64 encoding.'
    - ' - C(groups_base_dn) (str): Base distinguished name for groups'
    - ' - C(password) (str): Password to connect to the active directory server.'
    - ' - C(server_endpoints) (list): Active directory server endpoints. At least
      one active directory server endpoint must be set.'
    - ' - C(user_name) (str): User name to connect to the active directory server.'
    - ' - C(users_base_dn) (str): Base distinguished name for users'
    type: dict
  auth_query_params:
    description:
    - <p>key/value pairs that are to be appended to the authEndpoint request.</p>
      <p>How to append to authEndpoint request:</p> If the map is not empty, a "?"
      is added to the endpoint URL, and combination of each k and each string in the
      v is added with an "&" delimiter. Details:<ul> <li>If the value contains only
      one string, then the key is added with "k=v".</li> <li>If the value is an empty
      list, then the key is added without a "=v".</li> <li>If the value contains multiple
      strings, then the key is repeated in the query-string for each string in the
      value.</li></ul>
    type: list
  config_tag:
    choices:
    - Oauth2
    - Oidc
    description:
    - The {@name ConfigType} {@term structure} contains the possible types of vCenter
      Server identity providers. Required with I(state=['create', 'update'])
    type: str
  domain_names:
    description:
    - Set of fully qualified domain names to trust when federating with this identity
      provider. Tokens from this identity provider will only be validated if the user
      belongs to one of these domains, and any domain-qualified groups in the tokens
      will be filtered to include only those groups that belong to one of these domains.
    type: list
  groups_claim:
    description:
    - Specifies which claim provides the group membership for the token subject. These
      groups will be used for mapping to local groups per the claim map.
    type: str
  idm_endpoints:
    description:
    - Identity management endpoints. When specified, at least one endpoint must be
      provided.
    type: list
  idm_protocol:
    choices:
    - LDAP
    - REST
    - SCIM
    description:
    - The {@name IdmProtocol} {@term structure} contains the possible types of communication
      protocols to the identity management endpoints.
    type: str
  is_default:
    description:
    - Specifies whether the provider is the default provider. Setting {@name CreateSpec#isDefault}
      of current provider to True makes all other providers non-default. If no other
      providers created in this vCenter Server before, this parameter will be disregarded,
      and the provider will always be set to the default.
    type: bool
  make_default:
    description:
    - Specifies whether to make this the default provider. If {@name UpdateSpec#makeDefault}
      is set to true, this provider will be flagged as the default provider and any
      other providers that had previously been flagged as the default will be made
      non-default. If {@name UpdateSpec#makeDefault} is set to false, this provider's
      default flag will not be modified.
    type: bool
  name:
    description:
    - The user friendly name for the provider. This name can be used for human-readable
      identification purposes, but it does not have to be unique, as the system will
      use internal UUIDs to differentiate providers.
    type: str
  oauth2:
    description:
    - OAuth2 UpdateSpec
    - 'Validate attributes are:'
    - ' - C(auth_endpoint) (str): Authentication/authorization endpoint of the provider'
    - ' - C(auth_query_params) (list): key/value pairs that are to be appended to
      the authEndpoint request. How to append to authEndpoint request: If the map
      is not empty, a "?" is added to the endpoint URL, and combination of each k
      and each string in the v is added with an "&" delimiter. Details: If the value
      contains only one string, then the key is added with "k=v". If the value is
      an empty list, then the key is added without a "=v". If the value contains multiple
      strings, then the key is repeated in the query-string for each string in the
      value. If the map is empty, deletes all params.'
    - ' - C(authentication_method) (str): The {@name Oauth2AuthenticationMethod} {@term
      structure} contains the possible types of OAuth2 authentication methods.'
    - ' - C(claim_map) (list): The map used to transform an OAuth2 claim to a corresponding
      claim that vCenter Server understands. Currently only the key "perms" is supported.
      The key "perms" is used for mapping the "perms" claim of incoming JWT. The value
      is another map with an external group as the key and a vCenter Server group
      as value.'
    - ' - C(client_id) (str): Client identifier to connect to the provider'
    - ' - C(client_secret) (str): Shared secret between identity provider and client'
    - ' - C(issuer) (str): The identity provider namespace. It is used to validate
      the issuer in the acquired OAuth2 token'
    - ' - C(public_key_uri) (str): Endpoint to retrieve the provider public key for
      validation'
    - ' - C(token_endpoint) (str): Token endpoint of the provider.'
    type: dict
  oidc:
    description:
    - OIDC UpdateSpec
    - 'Validate attributes are:'
    - ' - C(claim_map) (list): The map used to transform an OAuth2 claim to a corresponding
      claim that vCenter Server understands. Currently only the key "perms" is supported.
      The key "perms" is used for mapping the "perms" claim of incoming JWT. The value
      is another map with an external group as the key and a vCenter Server group
      as value.'
    - ' - C(client_id) (str): Client identifier to connect to the provider'
    - ' - C(client_secret) (str): The secret shared between the client and the provider'
    - ' - C(discovery_endpoint) (str): Endpoint to retrieve the provider metadata'
    type: dict
  org_ids:
    description:
    - The set of orgIds as part of SDDC creation which provides the basis for tenancy
    type: list
  provider:
    description:
    - the identifier of the provider to update Required with I(state=['delete', 'update'])
    type: str
  reset_groups_claim:
    description:
    - 'Flag indicating whether any existing groups claim value should be removed.
      If this field is set to {@code true}, the existing groups claim value is removed
      which defaults to backwards compatibility with CSP. In this case, the groups
      for the subject will be comprised of the groups in ''group_names'' and ''group_ids''
      claims. If this field is set to {@code false}, the existing groups claim will
      be changed to the value specified in {@link #groupsClaim}, if any.'
    type: bool
  reset_upn_claim:
    description:
    - 'Flag indicating whether the user principal name (UPN) claim should be set back
      to its default value. If this field is set to {@code true}, the user principal
      name (UPN) claim will be set to ''acct'', which is used for backwards compatibility
      with CSP. If this field is set to {@code false}, the existing user principal
      name (UPN) claim will be changed to the value specified in {@link #upnClaim},
      if any.'
    type: bool
  state:
    choices:
    - create
    - delete
    - update
    description: []
    type: str
  upn_claim:
    description:
    - Specifies which claim provides the user principal name (UPN) for the subject
      of the token.
    type: str
author:
- Ansible VMware team
version_added: 1.0.0
requirements:
- python >= 3.6
"""
IN_QUERY_PARAMETER = []
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
    argument_spec["upn_claim"] = {"type": "str", "operationIds": ["create", "update"]}
    argument_spec["state"] = {"type": "str", "choices": ["create", "delete", "update"]}
    argument_spec["reset_upn_claim"] = {"type": "bool", "operationIds": ["update"]}
    argument_spec["reset_groups_claim"] = {"type": "bool", "operationIds": ["update"]}
    argument_spec["provider"] = {"type": "str", "operationIds": ["delete", "update"]}
    argument_spec["org_ids"] = {"type": "list", "operationIds": ["create", "update"]}
    argument_spec["oidc"] = {"type": "dict", "operationIds": ["create", "update"]}
    argument_spec["oauth2"] = {"type": "dict", "operationIds": ["create", "update"]}
    argument_spec["name"] = {"type": "str", "operationIds": ["create", "update"]}
    argument_spec["make_default"] = {"type": "bool", "operationIds": ["update"]}
    argument_spec["is_default"] = {"type": "bool", "operationIds": ["create"]}
    argument_spec["idm_protocol"] = {
        "type": "str",
        "choices": ["LDAP", "REST", "SCIM"],
        "operationIds": ["create", "update"],
    }
    argument_spec["idm_endpoints"] = {
        "type": "list",
        "operationIds": ["create", "update"],
    }
    argument_spec["groups_claim"] = {
        "type": "str",
        "operationIds": ["create", "update"],
    }
    argument_spec["domain_names"] = {
        "type": "list",
        "operationIds": ["create", "update"],
    }
    argument_spec["config_tag"] = {
        "type": "str",
        "choices": ["Oauth2", "Oidc"],
        "operationIds": ["create", "update"],
    }
    argument_spec["auth_query_params"] = {
        "type": "list",
        "operationIds": ["create", "update"],
    }
    argument_spec["active_directory_over_ldap"] = {
        "type": "dict",
        "operationIds": ["create", "update"],
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
    return "https://{vcenter_hostname}/rest/vcenter/identity/providers".format(**params)


async def entry_point(module, session):
    func = globals()[("_" + module.params["state"])]
    return await func(module.params, session)


async def _create(params, session):
    accepted_fields = [
        "active_directory_over_ldap",
        "auth_query_params",
        "config_tag",
        "domain_names",
        "groups_claim",
        "idm_endpoints",
        "idm_protocol",
        "is_default",
        "name",
        "oauth2",
        "oidc",
        "org_ids",
        "upn_claim",
    ]
    if "create" == "create":
        _exists = await exists(params, session)
        if _exists:
            return await update_changed_flag({"value": _exists}, 200, "get")
    spec = {}
    for i in accepted_fields:
        if params[i]:
            spec[i] = params[i]
    _url = "https://{vcenter_hostname}/rest/vcenter/identity/providers".format(**params)
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


async def _delete(params, session):
    _url = "https://{vcenter_hostname}/rest/vcenter/identity/providers/{provider}".format(
        **params
    ) + gen_args(
        params, IN_QUERY_PARAMETER
    )
    async with session.delete(_url) as resp:
        try:
            if resp.headers["Content-Type"] == "application/json":
                _json = await resp.json()
        except KeyError:
            _json = {}
        return await update_changed_flag(_json, resp.status, "delete")


async def _update(params, session):
    accepted_fields = [
        "active_directory_over_ldap",
        "auth_query_params",
        "config_tag",
        "domain_names",
        "groups_claim",
        "idm_endpoints",
        "idm_protocol",
        "make_default",
        "name",
        "oauth2",
        "oidc",
        "org_ids",
        "reset_groups_claim",
        "reset_upn_claim",
        "upn_claim",
    ]
    if "update" == "create":
        _exists = await exists(params, session)
        if _exists:
            return await update_changed_flag({"value": _exists}, 200, "get")
    spec = {}
    for i in accepted_fields:
        if params[i]:
            spec[i] = params[i]
    _url = "https://{vcenter_hostname}/rest/vcenter/identity/providers/{provider}".format(
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
            if type(_json["value"]) == dict:
                _id = list(_json["value"].values())[0]
            else:
                _id = _json["value"]
            _json = {"value": (await get_device_info(params, session, _url, _id))}
        return await update_changed_flag(_json, resp.status, "update")


if __name__ == "__main__":
    import asyncio

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
