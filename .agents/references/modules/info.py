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
##     <OPTION_NAME>: <VALUE>
"""

RETURN = r"""
## This section is a spec for the expected output of the module.
## Example:
value:
  description:
    - Check if the Console CLI is enabled
  returned: On success (Other common values are: On failure, Always, On change)
  sample: 1
  type: int
"""


## This structure describes the format of the payload expected by the end-points
PAYLOAD_FORMAT = {
    "get": {"query": {}, "body": {}, "path": {}}
}

## This section is literal, do not change it.
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.vmware.vmware_rest.plugins.module_utils._argument_spec import (
    prepare_argument_spec
)
from ansible_collections.vmware.vmware_rest.plugins.module_utils._client import (
    Client
)
## End of literal section.


def main():
    ## The Ansible moudle spec is described in this documentation: https://docs.ansible.com/projects/ansible/latest/dev_guide/developing_program_flow_modules.html#argument-spec
    ## Use this section as a starting point for the module spec, and add to it as needed.
    module_args = prepare_argument_spec()
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
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
        module.fail_json("Failed to create a client for vCenter: {0}".format(err))
    ## End of literal section.

    response = client.request(
        method="GET",
        path="<api uri path>",
        ## The options below should be filled in with the appropriate values. They are all optional.
        ## They query and data specs come from the vSphere API specification, and the values should come from the module parameters.
        query=None, ## This should be a dictionary of the query parameters for the API call.
        data=None, ## This should be a dictionary of the data to be sent to the API call.
        headers=None, ## This should be a dictionary of the headers to be sent to the API call.
        bytes=None, ## This should be the bytes to be sent to the API call. If not None, the data parameter will be ignored.
    )

    module.exit_json(**response.json)
