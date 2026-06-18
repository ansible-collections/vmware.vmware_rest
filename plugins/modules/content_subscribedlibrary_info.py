#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright: (c) 2026, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#
# This module is generated using LLM agents and skills defined in the vmware.vmware_rest repository.
# See: https://github.com/ansible-collections/vmware.vmware_rest
#

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
module: content_subscribedlibrary_info
short_description: Get subscribed content library information.
description:
  - Returns information about subscribed content libraries in the Content Library Service.
  - When I(library_id) is specified, returns information for that library only.
  - When I(library_id) is omitted, lists all subscribed libraries with detailed
    information for each library.
  - Requires the C(System.Read) privilege.
author:
  - Ansible Eco Content Team (@eco-ansible-content)
extends_documentation_fragment:
  - vmware.vmware_rest.connection_params
options:
  library_id:
    description:
      - Identifier of the subscribed library to return.
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
- name: List subscribed content libraries
  vmware.vmware_rest.content_subscribedlibrary_info:
  register: subscribed_libraries

- name: Get a specific subscribed content library
  vmware.vmware_rest.content_subscribedlibrary_info:
    library_id: subscribed-library-id
  register: subscribed_library
"""

RETURN = r"""
value:
  description:
    - Subscribed content library information.
    - Returns a list of library dictionaries when I(library_id) is omitted.
    - Returns a single library dictionary when I(library_id) is specified.
  returned: On success
  type: raw
  sample:
    - creation_time: "2024-01-01T00:00:00.000Z"
      description: Example subscribed library
      id: subscribed-library-id
      last_modified_time: "2024-01-02T00:00:00.000Z"
      name: example-subscribed-library
      type: SUBSCRIBED
  contains:
    id:
      description:
        - Identifier (MOID) for a C(com.vmware.content.Library) resource.
      type: str
      sample: subscribed-library-id
    name:
      description:
        - Name of the library.
      type: str
      sample: example-subscribed-library
    description:
      description:
        - Human-readable description of the library.
      type: str
      sample: Example subscribed library
    type:
      description:
        - Library type.
      type: str
      sample: SUBSCRIBED
      choices:
        - LOCAL
        - SUBSCRIBED
    creation_time:
      description:
        - Date and time when the library was created.
      type: str
      sample: "2024-01-01T00:00:00.000Z"
    last_modified_time:
      description:
        - Date and time when the library was last updated.
      type: str
      sample: "2024-01-02T00:00:00.000Z"
    last_sync_time:
      description:
        - Date and time when the library was last synchronized.
      type: str
      sample: "2024-01-02T12:00:00.000Z"
    version:
      description:
        - Version number updated on metadata changes.
      type: str
    server_guid:
      description:
        - Identifier (MOID) for a C(com.vmware.vcenter.VCenter) resource where the library exists.
      type: str
    security_policy_id:
      description:
        - Identifier (MOID) for a C(com.vmware.content.Library) security policy applied to the library.
      type: str
    storage_backings:
      description:
        - Default storage backings available for the library.
      type: list
      elements: dict
    subscription_info:
      description:
        - Subscription behavior for the subscribed library.
      type: dict
    publish_info:
      description:
        - Publication settings for the library.
      type: dict
    optimization_info:
      description:
        - Optimizations applied to the library.
      type: dict
    state_info:
      description:
        - State information for the library.
      type: dict
    configuration_info:
      description:
        - Library-level configuration settings.
      type: dict
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.vmware.vmware_rest.plugins.module_utils._argument_spec import (
    connection_params_argument_spec,
)
from ansible_collections.vmware.vmware_rest.plugins.module_utils._module_base import (
    VmwareRestInfoModuleBase,
)

LIST_PATH = "/content/subscribed-library"
LIBRARY_PATH = "/content/subscribed-library/{library_id}"


class VmwareRestInfoModule(VmwareRestInfoModuleBase):
    PAYLOAD_FORMAT = {
        "list": {"query": {}, "body": {}, "path": {}},
        "get": {"query": {}, "body": {}, "path": {"libraryId": "library_id"}},
    }

    def _get_library(self, library_id):
        response = self.client.get(
            self.build_path(LIBRARY_PATH, {"library_id": library_id})
        )
        if response.status == 404:
            return None
        library = response.json
        if "id" not in library:
            library["id"] = library_id
        return library

    def get_info(self):
        library_id = self.params.get("library_id")
        if library_id:
            library = self._get_library(library_id)
            if library is None:
                self.module.fail_json(
                    msg="Subscribed content library not found: {0}".format(library_id)
                )
            return library

        library_ids = self.fetch_list(LIST_PATH, self.PAYLOAD_FORMAT["list"])
        result = []
        for item_id in library_ids:
            library = self._get_library(item_id)
            if library is not None:
                result.append(library)
        return result


def main():
    module_args = connection_params_argument_spec()
    module_args["library_id"] = {"type": "str"}

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
    )

    info_module = VmwareRestInfoModule(module)
    result = info_module.get_info()
    module.exit_json(value=result)


if __name__ == "__main__":
    main()
