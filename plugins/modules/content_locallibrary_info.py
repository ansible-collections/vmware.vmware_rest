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
module: content_locallibrary_info
short_description: Get information about local content libraries.
description:
  - Returns information about local content libraries in the Content Library service.
  - When I(library_id) is specified, returns information for that local library only.
  - When I(library_id) is omitted, lists all local libraries with detailed information
    for each library.
author:
  - Ansible Eco Content Team (@eco-ansible-content)
extends_documentation_fragment:
  - vmware.vmware_rest.connection_params
options:
  library_id:
    description:
      - Identifier of the local content library to return.
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
- name: List all local content libraries
  vmware.vmware_rest.content_locallibrary_info:
  register: local_libraries

- name: Get a specific local content library
  vmware.vmware_rest.content_locallibrary_info:
    library_id: "{{ library_id }}"
  register: local_library
"""

RETURN = r"""
value:
  description:
    - Local content library information.
    - Returns a list of library dictionaries when I(library_id) is omitted.
    - Returns a single library dictionary when I(library_id) is specified.
  returned: On success
  type: raw
  sample:
    - creation_time: "2024-01-01T00:00:00.000Z"
      description: automated
      id: library-id
      last_modified_time: "2024-01-01T00:00:00.000Z"
      name: my-local-library
      type: LOCAL
  contains:
    id:
      description:
        - Identifier of the local content library.
        - Must be an identifier (MOID) for a C(com.vmware.content.Library) resource.
      type: str
      sample: library-id
    name:
      description:
        - Name of the local content library.
      type: str
      sample: my-local-library
    description:
      description:
        - Human-readable description of the local content library.
      type: str
      sample: automated
    type:
      description:
        - Type of the content library.
      type: str
      choices:
        - LOCAL
        - SUBSCRIBED
      sample: LOCAL
    creation_time:
      description:
        - Date and time when the library was created.
      type: str
    last_modified_time:
      description:
        - Date and time when the library properties were last updated.
      type: str
    version:
      description:
        - Version number updated when library metadata changes.
      type: str
    server_guid:
      description:
        - Unique identifier of the vCenter Server where the library exists.
        - Must be an identifier (MOID) for a C(com.vmware.vcenter.VCenter) resource.
      type: str
    storage_backings:
      description:
        - Default storage backings available for library items.
      type: list
      elements: dict
    publish_info:
      description:
        - Publishing configuration for the local library.
      type: dict
    state_info:
      description:
        - State information of the library.
      type: dict
    configuration_info:
      description:
        - Configuration settings at the individual content library level.
      type: dict
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.vmware.vmware_rest.plugins.module_utils._argument_spec import (
    connection_params_argument_spec,
)
from ansible_collections.vmware.vmware_rest.plugins.module_utils._module_base import (
    VmwareRestInfoModuleBase,
)

LIST_PATH = "/content/local-library"
LIBRARY_PATH = "/content/local-library/{library_id}"


class VmwareRestInfoModule(VmwareRestInfoModuleBase):
    PAYLOAD_FORMAT = {
        "list": {"query": {}, "body": {}, "path": {}},
        "get": {"query": {}, "body": {}, "path": {"library_id": "library_id"}},
    }

    def _get_library(self, library_id):
        response = self.client.get(
            self.build_path(LIBRARY_PATH, {"library_id": library_id})
        )
        if response.status == 404:
            return None
        library = response.json
        library["id"] = library_id
        return library

    def get_info(self):
        library_id = self.params.get("library_id")
        if library_id:
            library = self._get_library(library_id)
            if library is None:
                self.module.fail_json(
                    msg="Local content library not found: {0}".format(library_id)
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
