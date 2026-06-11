#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright: (c) <YEAR>, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#
# This module is generated using LLM agents and skills defined in the vmware.vmware_rest repository.
# See: https://github.com/ansible-collections/vmware.vmware_rest
#

## Note to AI: If a comment starts with two hashes (##), it is a note to the AI, not to be included in the final file.
## Values in angle brackets (<>) are placeholders for values that will be replaced by the AI.
## Otherwise, values should be considered examples or descriptions of the actual values. The AI should read the value, and use
## it as a reference, not as a literal value (unless otherwise specified).


DOCUMENTATION = r"""
## This section is the documentation for the module. It should be a valid yaml document that shows how to use the module in an ansible playbook.
module: <MODULE_NAME>
short_description: A short description of what the module does or what it is used for. Should be one or two sentences.
description: >-
  A longer description of what the module does or what it is used for. Should be a few sentences. It can
  include general information about the module, interactions with the vSphere API, and any other relevant information.
  Keep it concise and to the point, this is not meant to be a comprehensive documentation, it is meant to be a quick
  reference for the module.

## This section is literal, do not change it.
author:
  - Ansible Eco Content Team (@eco-ansible-content)
## End of literal section.

options:
  ## This should be a dictionary of all the options for the module. The options described here should reflect the
  ## argument_spec dictionary in the python code in this module.
  ## CRUD modules must include a state option when the API supports multiple lifecycle operations.
  state:
    description:
      - The desired state of the resource.
      - Use C(present) to create or update the resource.
      - Use C(absent) to delete the resource.
    type: str
    choices:
      - present
      - absent
    default: present
  <OPTION_NAME>:
    description:
      - A list of one or two sentences describing the option.
      - Each line can address a different aspect of the option. For example, specify relationships with other options,
        or what specific value(s) mean in real terms.
      - Do not include the default value, the type, or a list of choices. Those are documented in additional attributes.
    type: The python type of the option, e.g. str, int, bool, list, dict.
    required: true or false, whether the option is always required or optional.
    default: The default value of the option, if any. If there is no default value, this can be omitted.
    choices: A list of valid choices for the option, if any. If there are not specific valid choices, this can be omitted.
    elements: The type of the elements of the option, if the option is a list. If the option is not a list, this can be omitted.
    options: A dictionary of options for the option, if the option is a dictionary or the option is a list of element dictionaries. Otherwise, this can be omitted.

version_added: The current version of this collection, as seen in the galaxy.yml file's version attribute.
requirements: []

notes:
  - Include a sentence about what version of the API spec was used to generate the module.
"""

EXAMPLES = r"""
## This should be a valid yaml document that shows how to use the module in an ansible playbook.
## Each example should have a self-explanatory task name, or have a brief comment
## explaining what the example is doing.
## Examples should focus how to use the module, not on the expected output. The expected output is documented in the RETURN section.
## Examples should not try to show all usage scenarios, but rather focus on the most common or important scenarios (create, update, delete).
## If there are complex or many options, use a single example to show the most common usage, and use a separate example to show the complex usage.
## Examples should be in the following format:
## - name: <TASK_NAME>
##   vmware.vmware_rest.<MODULE_NAME>:
##     state: present
##     <OPTION_NAME>: <VALUE>
"""

RETURN = r"""
## This section is a spec for the expected output of the module.
## Example:
value:
  description:
    - The resource representation after the operation.
  returned: On success
  sample: {}
  type: dict
"""


## This structure describes the format of the payload expected by the end-points.
## Include one entry per supported operation (create, update, delete, set, etc.).
PAYLOAD_FORMAT = {
    "create": {"query": {}, "body": {}, "path": {}},
    "update": {"query": {}, "body": {}, "path": {}},
    "delete": {"query": {}, "body": {}, "path": {}},
}

## This section is literal, do not change it.
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.vmware.vmware_rest.plugins.module_utils._argument_spec import (
    prepare_argument_spec
)
from ansible_collections.vmware.vmware_rest.plugins.module_utils._client import (
    Client
)
from ansible_collections.vmware.vmware_rest.plugins.module_utils._errors import (
    UnexpectedAPIResponse,
)
## End of literal section.


def build_path(params, path_template):
    ## Substitute path parameters from module params into the API path template.
    ## Example: "/vcenter/datacenter/{datacenter}" with params["datacenter"] = "dc-1"
    ## returns "/vcenter/datacenter/dc-1"
    path = path_template
    for key, value in params.items():
        path = path.replace("{" + key + "}", str(value))
    return path


def build_payload(params, payload_format):
    ## Build request body from module params using PAYLOAD_FORMAT body mapping.
    body = {}
    for api_field, module_param in payload_format.get("body", {}).items():
        if module_param in params and params[module_param] is not None:
            body[api_field] = params[module_param]
    return body


def build_query(params, payload_format):
    ## Build query parameters from module params using PAYLOAD_FORMAT query mapping.
    query = {}
    for api_param, module_param in payload_format.get("query", {}).items():
        if module_param in params and params[module_param] is not None:
            query[api_param] = params[module_param]
    return query or None


def ensure_present(client, module, path_template):
    ## Implement create-or-update logic:
    ## 1. GET current state (404 means resource does not exist).
    ## 2. If absent, POST to create.
    ## 3. If present, compare current vs desired; PUT/PATCH only if different.
    ## 4. Return changed=True only when the resource was actually modified.
    path = build_path(module.params, path_template)
    payload_format = PAYLOAD_FORMAT["update"]
    desired = build_payload(module.params, payload_format)

    try:
        current_resp = client.get(path)
        current = current_resp.json
        exists = True
    except UnexpectedAPIResponse as err:
        if err.message and "404" in err.message:
            exists = False
            current = {}
        else:
            module.fail_json(msg="Failed to get current state: {0}".format(err))

    if not exists:
        create_format = PAYLOAD_FORMAT["create"]
        create_path = build_path(module.params, path_template)
        create_body = build_payload(module.params, create_format)
        create_query = build_query(module.params, create_format)
        response = client.post(create_path, data=create_body, query=create_query)
        result = response.json
        result["changed"] = True
        return result

    if current == desired:
        return {"changed": False, "value": current}

    update_body = build_payload(module.params, payload_format)
    update_query = build_query(module.params, payload_format)
    response = client.put(path, data=update_body, query=update_query)
    result = response.json
    result["changed"] = True
    return result


def ensure_absent(client, module, path_template):
    ## Implement delete logic:
    ## 1. GET or attempt DELETE.
    ## 2. If resource does not exist (404), return changed=False.
    ## 3. Otherwise DELETE and return changed=True.
    path = build_path(module.params, path_template)

    try:
        client.get(path)
    except UnexpectedAPIResponse as err:
        if err.message and "404" in err.message:
            return {"changed": False}
        module.fail_json(msg="Failed to check resource existence: {0}".format(err))

    delete_format = PAYLOAD_FORMAT["delete"]
    delete_query = build_query(module.params, delete_format)
    client.delete(path, query=delete_query)
    return {"changed": True}


def main():
    ## The Ansible module spec is described in this documentation: https://docs.ansible.com/projects/ansible/latest/dev_guide/developing_program_flow_modules.html#argument-spec
    ## Use this section as a starting point for the module spec, and add to it as needed.
    ## CRUD modules must set supports_check_mode=False.
    module_args = prepare_argument_spec()
    module_args["state"] = {
        "type": "str",
        "choices": ["present", "absent"],
        "default": "present",
    }
    ## Add API-specific options to module_args here.

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False,
    )
    ## End of module spec section.

    ## This section is literal, do not change it.
    try:
        client = Client(
            host=module.params["vcenter_hostname"],
            username=module.params["vcenter_username"],
            password=module.params["vcenter_password"],
            validate_certs=module.params["vcenter_validate_certs"],
            timeout=module.params["session_timeout"],
            log_file=module.params["vcenter_rest_log_file"],
        )
    except Exception as err:
        module.fail_json(msg="Failed to create a client for vCenter: {0}".format(err))
    ## End of literal section.

    path_template = "<api uri path with {param} placeholders>"

    if module.params["state"] == "present":
        result = ensure_present(client, module, path_template)
    elif module.params["state"] == "absent":
        result = ensure_absent(client, module, path_template)
    else:
        module.fail_json(msg="Unsupported state: {0}".format(module.params["state"]))

    module.exit_json(**result)
