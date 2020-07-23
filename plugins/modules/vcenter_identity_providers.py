from __future__ import absolute_import, division, print_function

__metaclass__ = type
import socket
import json

DOCUMENTATION = "author:\n- Ansible VMware team\ndescription: Handle resource of type vcenter_identity_providers\nextends_documentation_fragment: []\nmodule: vcenter_identity_providers\nnotes:\n- Tested on vSphere 7.0\noptions:\n  active_directory_over_ldap:\n    description:\n    - Identity management configuration. If the protocol is LDAP, the configuration\n      must be set, else InvalidArgument is thrown.\n    - 'Validate attributes are:'\n    - ' - C(cert_chain) (dict): SSL certificate chain in base64 encoding.'\n    - ' - C(groups_base_dn) (str): Base distinguished name for groups'\n    - ' - C(password) (str): Password to connect to the active directory server.'\n    - ' - C(server_endpoints) (list): Active directory server endpoints. At least\n      one active directory server endpoint must be set.'\n    - ' - C(user_name) (str): User name to connect to the active directory server.'\n    - ' - C(users_base_dn) (str): Base distinguished name for users'\n    type: dict\n  auth_query_params:\n    description:\n    - <p>key/value pairs that are to be appended to the authEndpoint request.</p>\n      <p>How to append to authEndpoint request:</p> If the map is not empty, a \"?\"\n      is added to the endpoint URL, and combination of each k and each string in the\n      v is added with an \"&\" delimiter. Details:<ul> <li>If the value contains only\n      one string, then the key is added with \"k=v\".</li> <li>If the value is an empty\n      list, then the key is added without a \"=v\".</li> <li>If the value contains multiple\n      strings, then the key is repeated in the query-string for each string in the\n      value.</li></ul>\n    type: list\n  config_tag:\n    choices:\n    - Oauth2\n    - Oidc\n    description:\n    - The {@name ConfigType} {@term structure} contains the possible types of vCenter\n      Server identity providers. Required with I(state=['create', 'update'])\n    type: str\n  domain_names:\n    description:\n    - Set of fully qualified domain names to trust when federating with this identity\n      provider. Tokens from this identity provider will only be validated if the user\n      belongs to one of these domains, and any domain-qualified groups in the tokens\n      will be filtered to include only those groups that belong to one of these domains.\n    type: list\n  groups_claim:\n    description:\n    - Specifies which claim provides the group membership for the token subject. These\n      groups will be used for mapping to local groups per the claim map.\n    type: str\n  idm_endpoints:\n    description:\n    - Identity management endpoints. When specified, at least one endpoint must be\n      provided.\n    type: list\n  idm_protocol:\n    choices:\n    - REST\n    - SCIM\n    - LDAP\n    description:\n    - The {@name IdmProtocol} {@term structure} contains the possible types of communication\n      protocols to the identity management endpoints.\n    type: str\n  is_default:\n    description:\n    - Specifies whether the provider is the default provider. Setting {@name CreateSpec#isDefault}\n      of current provider to True makes all other providers non-default. If no other\n      providers created in this vCenter Server before, this parameter will be disregarded,\n      and the provider will always be set to the default.\n    type: bool\n  make_default:\n    description:\n    - Specifies whether to make this the default provider. If {@name UpdateSpec#makeDefault}\n      is set to true, this provider will be flagged as the default provider and any\n      other providers that had previously been flagged as the default will be made\n      non-default. If {@name UpdateSpec#makeDefault} is set to false, this provider's\n      default flag will not be modified.\n    type: bool\n  name:\n    description:\n    - The user friendly name for the provider. This name can be used for human-readable\n      identification purposes, but it does not have to be unique, as the system will\n      use internal UUIDs to differentiate providers.\n    type: str\n  oauth2:\n    description:\n    - OAuth2 CreateSpec\n    - 'Validate attributes are:'\n    - ' - C(auth_endpoint) (str): Authentication/authorization endpoint of the provider'\n    - ' - C(auth_query_params) (list): <p>key/value pairs that are to be appended\n      to the authEndpoint request.</p> <p>How to append to authEndpoint request:</p>\n      If the map is not empty, a \"?\" is added to the endpoint URL, and combination\n      of each k and each string in the v is added with an \"&\" delimiter. Details:<ul>\n      <li>If the value contains only one string, then the key is added with \"k=v\".</li>\n      <li>If the value is an empty list, then the key is added without a \"=v\".</li>\n      <li>If the value contains multiple strings, then the key is repeated in the\n      query-string for each string in the value.</li></ul>'\n    - ' - C(authentication_method) (str): The {@name Oauth2AuthenticationMethod} {@term\n      structure} contains the possible types of OAuth2 authentication methods.'\n    - ' - C(claim_map) (list): The map used to transform an OAuth2 claim to a corresponding\n      claim that vCenter Server understands. Currently only the key \"perms\" is supported.\n      The key \"perms\" is used for mapping the \"perms\" claim of incoming JWT. The value\n      is another map with an external group as the key and a vCenter Server group\n      as value.'\n    - ' - C(client_id) (str): Client identifier to connect to the provider'\n    - ' - C(client_secret) (str): The secret shared between the client and the provider'\n    - ' - C(issuer) (str): The identity provider namespace. It is used to validate\n      the issuer in the acquired OAuth2 token.'\n    - ' - C(public_key_uri) (str): Endpoint to retrieve the provider public key for\n      validation'\n    - ' - C(token_endpoint) (str): Token endpoint of the provider'\n    type: dict\n  oidc:\n    description:\n    - OIDC CreateSpec\n    - 'Validate attributes are:'\n    - ' - C(claim_map) (list): The map used to transform an OAuth2 claim to a corresponding\n      claim that vCenter Server understands. Currently only the key \"perms\" is supported.\n      The key \"perms\" is used for mapping the \"perms\" claim of incoming JWT. The value\n      is another map with an external group as the key and a vCenter Server group\n      as value.'\n    - ' - C(client_id) (str): Client identifier to connect to the provider'\n    - ' - C(client_secret) (str): The secret shared between the client and the provider'\n    - ' - C(discovery_endpoint) (str): Endpoint to retrieve the provider metadata'\n    type: dict\n  org_ids:\n    description:\n    - The set of orgIds as part of SDDC creation which provides the basis for tenancy\n    type: list\n  provider:\n    description:\n    - the identifier of the provider to update Required with I(state=['update', 'delete'])\n    type: str\n  reset_groups_claim:\n    description:\n    - 'Flag indicating whether any existing groups claim value should be removed.\n      If this field is set to {@code true}, the existing groups claim value is removed\n      which defaults to backwards compatibility with CSP. In this case, the groups\n      for the subject will be comprised of the groups in ''group_names'' and ''group_ids''\n      claims. If this field is set to {@code false}, the existing groups claim will\n      be changed to the value specified in {@link #groupsClaim}, if any.'\n    type: bool\n  reset_upn_claim:\n    description:\n    - 'Flag indicating whether the user principal name (UPN) claim should be set back\n      to its default value. If this field is set to {@code true}, the user principal\n      name (UPN) claim will be set to ''acct'', which is used for backwards compatibility\n      with CSP. If this field is set to {@code false}, the existing user principal\n      name (UPN) claim will be changed to the value specified in {@link #upnClaim},\n      if any.'\n    type: bool\n  state:\n    choices:\n    - create\n    - update\n    - delete\n    description: []\n    type: str\n  upn_claim:\n    description:\n    - Specifies which claim provides the user principal name (UPN) for the user.\n    type: str\nrequirements:\n- python >= 3.6\nshort_description: Handle resource of type vcenter_identity_providers\nversion_added: 1.0.0\n"
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
        if ("create" == "create") and ("value" in _json):
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
        if ("update" == "create") and ("value" in _json):
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
