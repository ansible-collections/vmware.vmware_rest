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
module: vcenter_datacenter
short_description: Creates or deletes a datacenter in vCenter.
description:
  - Manages datacenters in vCenter.
  - Use I(state=present) to ensure a datacenter exists.
  - Use I(state=absent) to delete a datacenter.
  - The vSphere API does not support updating an existing datacenter; when the
    datacenter already exists, the module makes no changes.
author:
  - Ansible Eco Content Team (@eco-ansible-content)
extends_documentation_fragment:
  - vmware.vmware_rest.connection_params
options:
  state:
    description:
      - The desired state of the datacenter.
      - Use C(present) to create a datacenter when it does not exist.
      - Use C(absent) to delete the datacenter.
    type: str
    choices:
      - present
      - absent
    default: present
  name:
    description:
      - Name of the datacenter.
      - Required when creating a datacenter.
      - When I(state=absent), can be used to locate the datacenter when I(datacenter)
        is not set.
    type: str
  folder:
    description:
      - Datacenter folder in which the new datacenter should be created.
      - Must be an identifier (MOID) for a C(Folder) resource.
    type: str
  datacenter:
    description:
      - Identifier of the datacenter to delete.
      - Must be an identifier (MOID) for a C(Datacenter) resource.
      - When not set, I(name) is used to locate the datacenter.
    type: str
  force:
    description:
      - Whether to force removal of the datacenter.
    type: bool
version_added: 4.11.0
requirements: []
notes:
  - Generated from vSphere API spec 9.1.0.
  - Has support for vSphere API 7.0.3.
  - Has support for vSphere API 8.0.2.
"""

EXAMPLES = r"""
- name: Create a datacenter
  vmware.vmware_rest.vcenter_datacenter:
    name: my_datacenter

- name: Create a datacenter in a folder
  vmware.vmware_rest.vcenter_datacenter:
    name: my_datacenter
    folder: group-d1

- name: Delete a datacenter
  vmware.vmware_rest.vcenter_datacenter:
    state: absent
    datacenter: datacenter-1001

- name: Delete a datacenter by name
  vmware.vmware_rest.vcenter_datacenter:
    state: absent
    name: my_datacenter
    force: true
"""

RETURN = r"""
id:
  description:
    - The MOID of the datacenter.
  returned: On success when I(state=present) and the datacenter already exists
  type: str
  sample: datacenter-1001

value:
  description:
    - The MOID of the datacenter after create.
  returned: On success when I(state=present) and the datacenter was created
  type: str
  sample: datacenter-1001
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.vmware.vmware_rest.plugins.module_utils._argument_spec import (
    connection_params_argument_spec,
)
from ansible_collections.vmware.vmware_rest.plugins.module_utils._module_base import (
    VmwareRestCrudModuleBase,
    find_summary_id,
)

LIST_PATH = "/vcenter/datacenter"
ITEM_PATH = "/vcenter/datacenter/{datacenter}"

_CREATE_BODY = {
    "name": "name",
    "folder": "folder",
}


class VmwareRestCrudModule(VmwareRestCrudModuleBase):
    PAYLOAD_FORMAT = {
        "create": {
            "query": {},
            "body": _CREATE_BODY,
            "path": {},
        },
        "delete": {
            "query": {"force": "force"},
            "body": {},
            "path": {"datacenter": "datacenter"},
        },
        "list": {
            "query": {"names": "name"},
            "body": {},
            "path": {},
        },
    }

    UPDATABLE_PARAMS = ()

    def ensure_present(self):
        datacenter = self.params.get("datacenter")
        if datacenter:
            return self._ensure_present_by_id(datacenter)

        name = self.params.get("name")
        if not name:
            self.module.fail_json(msg="name is required when creating a datacenter")

        found_id = self._find_by_name(name)
        if found_id:
            return {"changed": False, "id": found_id}

        return self._create()

    def ensure_absent(self):
        datacenter = self.resolve_resource_id(
            "datacenter",
            "name",
            self._find_by_name,
        )
        if not datacenter:
            return {"changed": False}

        path = self.build_path(ITEM_PATH, {"datacenter": datacenter})
        response = self.client.get(path)
        if response.status == 404:
            return {"changed": False}

        delete_query = self.build_query(self.PAYLOAD_FORMAT["delete"])
        if not self.module.check_mode:
            self.client.delete(path, query=delete_query or None)
        return {"changed": True}

    def _create(self):
        create_body = self.build_payload(self.PAYLOAD_FORMAT["create"])
        if not self.module.check_mode:
            response = self.client.post(LIST_PATH, data=create_body)
            datacenter_id = response.json
        else:
            datacenter_id = None
        return {"changed": True, "value": datacenter_id, "id": datacenter_id}

    def _ensure_present_by_id(self, datacenter):
        path = self.build_path(ITEM_PATH, {"datacenter": datacenter})
        response = self.client.get(path)
        if response.status == 404:
            self.module.fail_json(msg="Datacenter not found: {0}".format(datacenter))

        return {"changed": False, "id": datacenter}

    def _find_by_name(self, name):
        summaries = self.fetch_list(LIST_PATH, self.PAYLOAD_FORMAT["list"])
        return find_summary_id(summaries, name, id_key="datacenter")


def main():
    module_args = connection_params_argument_spec()
    module_args["state"] = {
        "type": "str",
        "choices": ["present", "absent"],
        "default": "present",
    }
    module_args["name"] = {"type": "str"}
    module_args["folder"] = {"type": "str"}
    module_args["datacenter"] = {"type": "str"}
    module_args["force"] = {"type": "bool"}

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
    )

    crud_module = VmwareRestCrudModule(module)

    if module.params["state"] == "present":
        result = crud_module.ensure_present()
    elif module.params["state"] == "absent":
        result = crud_module.ensure_absent()
    else:
        module.fail_json(msg="Unsupported state: {0}".format(module.params["state"]))

    module.exit_json(**result)


if __name__ == "__main__":
    main()
