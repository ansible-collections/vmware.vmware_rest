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
module: vcenter_vmtemplate_libraryitems
short_description: Create or deploy virtual machine template library items.
description:
  - Creates a library item containing a virtual machine template from a source virtual
    machine, or deploys a virtual machine from an existing template library item.
  - Use I(state=present) to create a template library item from I(source_vm).
  - Use I(state=deploy) to deploy a virtual machine from I(template_library_item).
author:
  - Ansible Eco Content Team (@eco-ansible-content)
extends_documentation_fragment:
  - vmware.vmware_rest.connection_params
options:
  state:
    description:
      - The desired operation.
      - Use C(present) to create a template library item from a source virtual machine.
      - Use C(deploy) to deploy a virtual machine from a template library item.
    type: str
    choices:
      - present
      - deploy
    default: present
  name:
    description:
      - Name of the template library item or deployed virtual machine.
    type: str
    required: true
  library:
    description:
      - Identifier of the content library.
      - Must be an identifier (MOID) for a C(Library) resource.
      - Required when I(state=present).
    type: str
  source_vm:
    description:
      - Identifier of the source virtual machine used to create the template.
      - Must be an identifier (MOID) for a C(VirtualMachine) resource.
      - Required when I(state=present).
    type: str
  template_library_item:
    description:
      - Identifier of the template library item to deploy.
      - Must be an identifier (MOID) for a C(VmTemplateLibraryItem) resource.
      - Required when I(state=deploy).
    type: str
  description:
    description:
      - Description of the template library item or deployed virtual machine.
    type: str
  placement:
    description:
      - Placement information for the template or deployed virtual machine.
    type: dict
    suboptions:
      folder:
        description:
          - Folder for the virtual machine.
          - Must be an identifier (MOID) for a C(Folder) resource.
        type: str
      resource_pool:
        description:
          - Resource pool for the virtual machine.
          - Must be an identifier (MOID) for a C(ResourcePool) resource.
        type: str
      host:
        description:
          - Host for the virtual machine.
          - Must be an identifier (MOID) for a C(Host) resource.
        type: str
      cluster:
        description:
          - Cluster for the virtual machine.
          - Must be an identifier (MOID) for a C(Cluster) resource.
        type: str
  vm_home_storage:
    description:
      - Storage specification for the virtual machine home directory.
    type: dict
    suboptions:
      datastore:
        description:
          - Datastore for the virtual machine home directory.
          - Must be an identifier (MOID) for a C(Datastore) resource.
        type: str
      storage_policy:
        description:
          - Storage policy for the virtual machine home directory.
        type: dict
        suboptions:
          type:
            description:
              - Storage policy type.
            type: str
            choices:
              - USE_SOURCE_POLICY
              - USE_DEFAULT_POLICY
              - USE_SPECIFIED_POLICY
          policy:
            description:
              - Identifier of the storage policy.
              - Must be an identifier (MOID) for a C(StoragePolicy) resource.
            type: str
  disk_storage:
    description:
      - Storage specification for virtual machine disks.
    type: dict
    suboptions:
      datastore:
        description:
          - Datastore for virtual machine disks.
          - Must be an identifier (MOID) for a C(Datastore) resource.
        type: str
      storage_policy:
        description:
          - Storage policy for virtual machine disks.
        type: dict
        suboptions:
          type:
            description:
              - Storage policy type.
            type: str
            choices:
              - USE_SOURCE_POLICY
              - USE_DEFAULT_POLICY
              - USE_SPECIFIED_POLICY
          policy:
            description:
              - Identifier of the storage policy.
              - Must be an identifier (MOID) for a C(StoragePolicy) resource.
            type: str
  disk_storage_overrides:
    description:
      - Per-disk storage specifications keyed by disk identifier.
    type: dict
  powered_on:
    description:
      - Whether the deployed virtual machine is powered on.
      - Relevant when I(state=deploy).
    type: bool
version_added: 4.11.0
requirements: []
notes:
  - Generated from vSphere API spec 9.1.0.
  - Has support for vSphere API 7.0.3.
  - Has support for vSphere API 8.0.2.
"""

EXAMPLES = r"""
- name: Create a VM template library item
  vmware.vmware_rest.vcenter_vmtemplate_libraryitems:
    name: my-template
    library: library-1001
    source_vm: vm-1001
    placement:
      folder: group-v42
      resource_pool: resgroup-8
      cluster: domain-c9

- name: Deploy a virtual machine from a template library item
  vmware.vmware_rest.vcenter_vmtemplate_libraryitems:
    state: deploy
    name: my-deployed-vm
    template_library_item: item-1001
    placement:
      folder: group-v42
      resource_pool: resgroup-8
      cluster: domain-c9
"""

RETURN = r"""
id:
  description:
    - Identifier of the template library item or deployed virtual machine.
  returned: On success
  type: str
  sample: item-1001

value:
  description:
    - Identifier of the created template library item or deployed virtual machine.
  returned: On success
  type: str
  sample: vm-2001
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.vmware.vmware_rest.plugins.module_utils._argument_spec import (
    connection_params_argument_spec,
)
from ansible_collections.vmware.vmware_rest.plugins.module_utils._module_base import (
    VmwareRestCrudModuleBase,
    normalize_list_response,
)

CREATE_PATH = "/vcenter/vm-template/library-items"
TEMPLATE_ITEM_PATH = "/vcenter/vm-template/library-items/{template_library_item}"
LIBRARY_ITEMS_PATH = "/content/library/item"
CONTENT_ITEM_PATH = "/content/library/item/{library_item_id}"
DEPLOY_PATH = "/vcenter/vm-template/library-items/{template_library_item}"

_PLACEMENT_ARG_SPEC = {
    "type": "dict",
    "options": {
        "folder": {"type": "str"},
        "resource_pool": {"type": "str"},
        "host": {"type": "str"},
        "cluster": {"type": "str"},
    },
}

_STORAGE_POLICY_ARG_SPEC = {
    "type": "dict",
    "options": {
        "type": {
            "type": "str",
            "choices": [
                "USE_SOURCE_POLICY",
                "USE_DEFAULT_POLICY",
                "USE_SPECIFIED_POLICY",
            ],
        },
        "policy": {"type": "str"},
    },
}

_STORAGE_ARG_SPEC = {
    "type": "dict",
    "options": {
        "datastore": {"type": "str"},
        "storage_policy": _STORAGE_POLICY_ARG_SPEC,
    },
}

_CREATE_BODY = {
    "description": "description",
    "disk_storage": "disk_storage",
    "disk_storage_overrides": "disk_storage_overrides",
    "library": "library",
    "name": "name",
    "placement": "placement",
    "source_vm": "source_vm",
    "vm_home_storage": "vm_home_storage",
}

_DEPLOY_BODY = {
    "description": "description",
    "disk_storage": "disk_storage",
    "disk_storage_overrides": "disk_storage_overrides",
    "name": "name",
    "placement": "placement",
    "powered_on": "powered_on",
    "vm_home_storage": "vm_home_storage",
}


class VmwareRestCrudModule(VmwareRestCrudModuleBase):
    PAYLOAD_FORMAT = {
        "create": {
            "query": {},
            "body": _CREATE_BODY,
            "path": {},
        },
        "deploy": {
            "query": {"action": "deploy"},
            "body": _DEPLOY_BODY,
            "path": {"template_library_item": "template_library_item"},
        },
        "list_library_items": {
            "query": {"library_id": "library"},
            "body": {},
            "path": {},
        },
    }

    UPDATABLE_PARAMS = ()

    def ensure_present(self):
        library = self.params.get("library")
        source_vm = self.params.get("source_vm")
        if not library:
            self.module.fail_json(
                msg="library is required when state is present"
            )
        if not source_vm:
            self.module.fail_json(
                msg="source_vm is required when state is present"
            )

        template_library_item = self.params.get("template_library_item")
        if template_library_item:
            info = self._get_template_info(template_library_item)
            if info is not None:
                return {
                    "changed": False,
                    "id": template_library_item,
                    "value": info,
                }

        existing_id = self._find_library_item_by_name(library, self.params["name"])
        if existing_id:
            info = self._get_template_info(existing_id)
            return {
                "changed": False,
                "id": existing_id,
                "value": info if info is not None else existing_id,
            }

        create_body = self.build_payload(self.PAYLOAD_FORMAT["create"])
        if not self.module.check_mode:
            response = self.client.post(CREATE_PATH, data=create_body)
            item_id = response.json
            if isinstance(item_id, dict):
                item_id = item_id.get("value", item_id)
            info = self._get_template_info(item_id)
        else:
            item_id = None
            info = {}
        return {
            "changed": True,
            "id": item_id,
            "value": info if info is not None else item_id,
        }

    def ensure_deploy(self):
        template_library_item = self.params.get("template_library_item")
        if not template_library_item:
            self.module.fail_json(
                msg="template_library_item is required when state is deploy"
            )

        path = self.build_path(DEPLOY_PATH, {"template_library_item": template_library_item})
        deploy_body = self.build_payload(self.PAYLOAD_FORMAT["deploy"])
        query = self.build_query(self.PAYLOAD_FORMAT["deploy"])
        if not self.module.check_mode:
            response = self.client.post(path, data=deploy_body, query=query)
            vm_id = response.json
            if isinstance(vm_id, dict):
                vm_id = vm_id.get("value", vm_id)
        else:
            vm_id = None
        return {"changed": True, "id": vm_id, "value": vm_id}

    def ensure_absent(self):
        self.module.fail_json(msg="state must be present or deploy")

    def _get_template_info(self, template_library_item):
        path = self.build_path(
            TEMPLATE_ITEM_PATH,
            {"template_library_item": template_library_item},
        )
        response = self.client.get(path)
        if response.status == 404:
            return None
        return response.json

    def _find_library_item_by_name(self, library_id, name):
        response = self.client.get(
            LIBRARY_ITEMS_PATH,
            query={"library_id": library_id},
        )
        if response.status == 404:
            return None

        item_ids = normalize_list_response(response.json)
        for item_id in item_ids:
            item_response = self.client.get(
                self.build_path(CONTENT_ITEM_PATH, {"library_item_id": item_id})
            )
            if item_response.status != 200:
                continue
            item_info = item_response.json
            if isinstance(item_info, dict) and item_info.get("name") == name:
                return item_id
        return None


def main():
    module_args = connection_params_argument_spec()
    module_args["state"] = {
        "type": "str",
        "choices": ["present", "deploy"],
        "default": "present",
    }
    module_args["name"] = {"type": "str", "required": True}
    module_args["library"] = {"type": "str"}
    module_args["source_vm"] = {"type": "str"}
    module_args["template_library_item"] = {"type": "str"}
    module_args["description"] = {"type": "str"}
    module_args["placement"] = _PLACEMENT_ARG_SPEC
    module_args["vm_home_storage"] = _STORAGE_ARG_SPEC
    module_args["disk_storage"] = _STORAGE_ARG_SPEC
    module_args["disk_storage_overrides"] = {"type": "dict"}
    module_args["powered_on"] = {"type": "bool"}

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
    )

    crud_module = VmwareRestCrudModule(module)
    state = module.params["state"]
    if state == "present":
        result = crud_module.ensure_present()
    elif state == "deploy":
        result = crud_module.ensure_deploy()
    else:
        module.fail_json(msg="Unsupported state: {0}".format(state))

    module.exit_json(**result)


if __name__ == "__main__":
    main()
