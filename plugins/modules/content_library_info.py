#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright: (c) 2026, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#
# This module is generated using LLM agents and skills defined in the vmware.vmware_rest repository.
# See: https://github.com/ansible-collections/vmware.vmware_rest
#

DOCUMENTATION = r"""
module: content_library_info
short_description: Get information about content libraries.
description:
  - Returns information about content libraries in vCenter.
  - When I(library) is specified, returns the C(Content.LibraryModel) for that library.
  - When I(library) is omitted, lists all content libraries with their full details.
author:
  - Ansible Eco Content Team (@eco-ansible-content)
extends_documentation_fragment:
  - vmware.vmware_rest.connection_params
options:
  library:
    description:
      - Identifier of the content library to return.
      - Must be an identifier (MOID) for a C(com.vmware.content.Library) resource.
      - When specified, only that library is returned.
    type: str
version_added: 4.11.0
requirements: []
notes:
  - Generated from vSphere API spec 9.1.0.
  - Has support for vSphere API 7.0.3.
  - Has support for vSphere API 8.0.2.
"""

EXAMPLES = r"""
- name: List all content libraries
  vmware.vmware_rest.content_library_info:
  register: libraries

- name: Get information about a content library
  vmware.vmware_rest.content_library_info:
    library: "{{ library_id }}"
  register: library_info
"""

RETURN = r"""
value:
  description:
    - Content library information.
    - Returns a list of library dictionaries when I(library) is omitted.
    - Returns a single library dictionary when I(library) is specified.
  returned: On success
  type: raw
  sample:
    creation_time: "2024-01-15T10:30:00Z"
    description: Production templates
    id: 12345678-1234-1234-1234-123456789abc
    last_modified_time: "2024-06-01T14:00:00Z"
    name: prod-templates
    type: LOCAL
    version: "1"
  contains:
    id:
      description:
        - Content library identifier (MOID).
      type: str
      sample: 12345678-1234-1234-1234-123456789abc
    name:
      description:
        - Name of the content library.
      type: str
      sample: prod-templates
    description:
      description:
        - Human-readable description of the content library.
      type: str
      sample: Production templates
    type:
      description:
        - Library type.
      type: str
      choices:
        - LOCAL
        - SUBSCRIBED
      sample: LOCAL
    creation_time:
      description:
        - Date and time when the library was created.
      type: str
      sample: "2024-01-15T10:30:00Z"
    last_modified_time:
      description:
        - Date and time when the library was last updated.
      type: str
      sample: "2024-06-01T14:00:00Z"
    last_sync_time:
      description:
        - Date and time when the library was last synchronized.
        - Present only for subscribed libraries.
      type: str
      sample: "2024-06-01T12:00:00Z"
    version:
      description:
        - Version number updated on metadata changes.
      type: str
      sample: "1"
    server_guid:
      description:
        - Identifier (MOID) of the vCenter server where the library exists.
      type: str
    storage_backings:
      description:
        - Default storage backings available for the library.
      type: list
      elements: dict
    publish_info:
      description:
        - Publication settings for a local library.
      type: dict
    subscription_info:
      description:
        - Subscription settings for a subscribed library.
      type: dict
    security_policy_id:
      description:
        - Identifier (MOID) of the security policy applied to the library.
      type: str
    state_info:
      description:
        - State information of the library.
      type: dict
    configuration_info:
      description:
        - Library-level configuration settings.
      type: dict
    optimization_info:
      description:
        - Optimization settings applied to the library.
      type: dict
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.vmware.vmware_rest.plugins.module_utils._argument_spec import (
    connection_params_argument_spec,
)
from ansible_collections.vmware.vmware_rest.plugins.module_utils._errors import (
    UnexpectedAPIResponse,
)
from ansible_collections.vmware.vmware_rest.plugins.module_utils._module_base import (
    VmwareRestInfoModuleBase,
    normalize_list_response,
)

LIST_PATH = "/content/library"
LIBRARY_PATH = "/content/library/{library}"


class VmwareRestInfoModule(VmwareRestInfoModuleBase):
    PAYLOAD_FORMAT = {
        "list": {"query": {}, "body": {}, "path": {}},
        "get": {"query": {}, "body": {}, "path": {"library": "library"}},
    }

    def _get_library(self, library_id):
        path = self.build_path(LIBRARY_PATH, {"library": library_id})
        response = self.client.get(path)
        if response.status == 404:
            self.client.error_handler.handle_request_error(
                exception=UnexpectedAPIResponse(response.status, response.data),
                method="GET",
                path=path,
                request_kwargs={},
            )
        info = response.json
        if "id" not in info:
            info["id"] = library_id
        return info

    def get_info(self):
        library = self.params.get("library")
        if library:
            return self._get_library(library)

        response = self.client.get(LIST_PATH)
        if response.status == 404:
            return []

        library_ids = normalize_list_response(response.json)
        result = []
        for library_id in library_ids:
            result.append(self._get_library(library_id))
        return result


def main():
    module_args = connection_params_argument_spec()
    module_args["library"] = {"type": "str"}

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
    )

    info_module = VmwareRestInfoModule(module)
    result = info_module.get_info()
    module.exit_json(value=result)


if __name__ == "__main__":
    main()
