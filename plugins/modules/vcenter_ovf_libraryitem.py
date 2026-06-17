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
module: vcenter_ovf_libraryitem
short_description: Manage OVF library items in a vCenter content library.
description:
  - Creates a library item in a content library from a virtual machine or virtual appliance OVF package.
  - Deploys an OVF library item to a resource pool or returns OVF deployment metadata.
  - Use I(state=present) to export a virtual machine or virtual appliance to a content library.
  - Use I(state=deploy) to deploy an OVF library item to a resource pool.
  - Use I(state=filter) to retrieve OVF deployment metadata for an OVF library item.
  - When exporting to an existing library item with the same name, the module reports no change.
  - Metadata such as name and description is not updated for an existing library item; see the
    examples for a workaround when updating description.
author:
  - Ansible Eco Content Team (@eco-ansible-content)
extends_documentation_fragment:
  - vmware.vmware_rest.connection_params
options:
  state:
    description:
      - The operation to perform.
      - Use C(present) to create or overwrite a library item from a source virtual machine or virtual appliance.
      - Use C(deploy) to deploy an OVF library item.
      - Use C(filter) to retrieve OVF deployment metadata.
    type: str
    choices:
      - present
      - deploy
      - filter
    default: present
  client_token:
    description:
      - Client-generated token used to retry a request if the client fails to get a response from the server.
      - If the original request succeeded, the result of that request is returned; otherwise the operation is retried.
      - If omitted, the server creates a token.
    type: str
  ovf_library_item_id:
    description:
      - Identifier of the content library item containing the OVF package.
      - Must be an identifier (MOID) for a C(com.vmware.content.library.Item) resource.
      - Required when I(state=deploy) or I(state=filter).
    type: str
  source:
    description:
      - Source virtual machine or virtual appliance to export to a library item.
      - Required when I(state=present).
    type: dict
    suboptions:
      type:
        description:
          - Type of the deployable resource.
        type: str
        choices:
          - VirtualMachine
          - VirtualApp
        required: true
      id:
        description:
          - Identifier of the deployable resource.
          - Must be an identifier (MOID) for a C(VirtualMachine) or C(VirtualApp) resource.
        type: str
        required: true
  target:
    description:
      - Target specification for the selected operation.
      - When I(state=present), specifies the content library or library item to create or update.
      - When I(state=deploy) or I(state=filter), specifies the deployment target resource pool and optional host or folder.
    type: dict
    required: true
    suboptions:
      library_id:
        description:
          - Identifier of the library in which a new library item should be created.
          - Must be an identifier (MOID) for a C(com.vmware.content.Library) resource.
          - Required when creating a new library item unless I(library_item_id) is specified.
        type: str
      library_item_id:
        description:
          - Identifier of the library item to update.
          - Must be an identifier (MOID) for a C(com.vmware.content.library.Item) resource.
          - When specified, the existing library item content is overwritten.
        type: str
      resource_pool_id:
        description:
          - Identifier of the resource pool to which the virtual machine or virtual appliance should be attached.
          - Must be an identifier (MOID) for a C(ResourcePool) resource.
          - Required when I(state=deploy) or I(state=filter).
        type: str
      host_id:
        description:
          - Identifier of the target host on which the virtual machine or virtual appliance will run.
          - Must be an identifier (MOID) for a C(HostSystem) resource.
        type: str
      folder_id:
        description:
          - Identifier of the vCenter folder that should contain the virtual machine or virtual appliance.
          - Must be an identifier (MOID) for a C(Folder) resource.
        type: str
  create_spec:
    description:
      - Information used to create the OVF package from the source virtual machine or virtual appliance.
      - Required when I(state=present).
    type: dict
    suboptions:
      name:
        description:
          - Name to use in the OVF descriptor stored in the library item.
          - If omitted, the server uses the source name.
        type: str
      description:
        description:
          - Description to use in the OVF descriptor stored in the library item.
          - If omitted, the server uses the source annotation.
        type: str
      flags:
        description:
          - Flags to use for OVF package creation.
          - Supported flags can be obtained from the C(GET /vcenter/ovf/export-flag) API.
        type: list
        elements: str
      library_item_source_id:
        description:
          - Source identifier of the library item for image identification.
          - Must be an identifier (MOID) for a C(com.vmware.content.library.Item) resource.
        type: str
  deployment_spec:
    description:
      - Specification of how the OVF package should be deployed to the target.
      - Required when I(state=deploy).
    type: dict
    suboptions:
      name:
        description:
          - Name assigned to the deployed virtual machine or virtual appliance.
        type: str
      annotation:
        description:
          - Annotation assigned to the deployed virtual machine or virtual appliance.
        type: str
      accept_all_eula:
        description:
          - Whether to accept all End User License Agreements.
        type: bool
        required: true
      network_mappings:
        description:
          - Target network mapping for OVF network sections.
          - Keys are OVF network section identifiers; values must be identifiers (MOID) for a C(Network) resource.
        type: dict
      subnet_mappings:
        description:
          - Target subnet mapping for OVF network sections.
          - Keys are OVF network section identifiers; values must be identifiers (MOID) for a C(Folder) resource.
        type: dict
      storage_mappings:
        description:
          - Target storage mapping for OVF storage group sections.
        type: dict
      storage_provisioning:
        description:
          - Default storage provisioning type for OVF storage sections.
        type: str
        choices:
          - thin
          - thick
          - eagerZeroedThick
      storage_profile_id:
        description:
          - Default storage profile for OVF storage sections.
          - Must be an identifier (MOID) for a C(StorageProfile) resource.
        type: str
      locale:
        description:
          - Locale to use when parsing the OVF descriptor.
        type: str
      flags:
        description:
          - Flags to use for deployment.
          - Supported flags can be obtained from the C(GET /vcenter/ovf/import-flag) API.
        type: list
        elements: str
      additional_parameters:
        description:
          - Additional OVF parameters required by the OVF descriptor.
        type: list
        elements: dict
      default_datastore_id:
        description:
          - Default datastore for OVF storage sections.
          - Must be an identifier (MOID) for a C(Datastore) resource.
        type: str
      vm_config_spec:
        description:
          - Virtual machine configuration settings to use instead of the OVF descriptor hardware specifications.
        type: dict
      tag_params:
        description:
          - Tag parameters used to attach tags to a virtual machine during deployment.
        type: dict
version_added: 4.11.0
requirements: []
notes:
  - Generated from vSphere API spec 9.1.0.
  - Has support for vSphere API 7.0.3.
  - Has support for vSphere API 8.0.2.
"""

EXAMPLES = r"""
- name: Export a virtual machine as an OVF library item
  vmware.vmware_rest.vcenter_ovf_libraryitem:
    session_timeout: 2900
    source:
      type: VirtualMachine
      id: vm-1001
    target:
      library_id: fbcc0f38-b7d9-4243-95f6-fb28f1ab35a6
    create_spec:
      name: Golden Image
      description: A golden image for templating
      flags: []
    state: present
  register: ovf_item

- name: Update an existing OVF library item description
  vmware.vmware_rest.vcenter_ovf_libraryitem:
    session_timeout: 2900
    source:
      type: VirtualMachine
      id: vm-1001
    target:
      library_id: fbcc0f38-b7d9-4243-95f6-fb28f1ab35a6
      library_item_id: "{{ ovf_item.id }}"
    create_spec:
      description: An updated description for this template
      flags: []
    state: present

- name: Deploy an OVF library item
  vmware.vmware_rest.vcenter_ovf_libraryitem:
    ovf_library_item_id: 3994f858-2d45-4dac-b407-0643a29308bd
    state: deploy
    target:
      resource_pool_id: resgroup-1009
    deployment_spec:
      name: deployed-vm
      accept_all_eula: true
      storage_provisioning: thin
  register: deployment

- name: Get OVF deployment metadata
  vmware.vmware_rest.vcenter_ovf_libraryitem:
    ovf_library_item_id: 3994f858-2d45-4dac-b407-0643a29308bd
    state: filter
    target:
      resource_pool_id: resgroup-1009
  register: ovf_summary
"""

RETURN = r"""
id:
  description:
    - Identifier of the OVF library item or deployed resource, when available.
  returned: On success
  type: str
  sample: 3994f858-2d45-4dac-b407-0643a29308bd

value:
  description:
    - Result of the create, deploy, or filter operation.
  returned: On success
  type: dict
  sample:
    succeeded: true
    ovf_library_item_id: 3994f858-2d45-4dac-b407-0643a29308bd
    error:
      errors: []
      warnings: []
      information: []
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.vmware.vmware_rest.plugins.module_utils._argument_spec import (
    connection_params_argument_spec,
)
from ansible_collections.vmware.vmware_rest.plugins.module_utils._errors import (
    UnexpectedAPIResponse,
)
from ansible_collections.vmware.vmware_rest.plugins.module_utils._module_base import (
    VmwareRestModuleBase,
    normalize_list_response,
)

CREATE_PATH = "/vcenter/ovf/library-item"
DEPLOY_PATH = "/vcenter/ovf/library-item/{ovf_library_item_id}?action=deploy"
FILTER_PATH = "/vcenter/ovf/library-item/{ovf_library_item_id}?action=filter"
LIBRARY_ITEMS_PATH = "/content/library/item"
LIBRARY_ITEM_PATH = "/content/library/item/{library_item_id}"


class VmwareRestOvfLibraryItemModule(VmwareRestModuleBase):
    PAYLOAD_FORMAT = {
        "create": {
            "query": {},
            "body": {
                "create_spec": "create_spec",
                "source": "source",
                "target": "target",
            },
            "path": {},
        },
        "deploy": {
            "query": {},
            "body": {
                "deployment_spec": "deployment_spec",
                "target": "target",
            },
            "path": {"ovf_library_item_id": "ovf_library_item_id"},
        },
        "filter": {
            "query": {},
            "body": {"target": "target"},
            "path": {"ovf_library_item_id": "ovf_library_item_id"},
        },
    }

    def _request_headers(self):
        client_token = self.params.get("client_token")
        if client_token:
            return {"Client-Token": client_token}
        return None

    def _post(self, path, body):
        headers = self._request_headers()
        response = self.client.request("POST", path, data=body, headers=headers)
        if response.status not in (200, 201):
            self.client.error_handler.handle_request_error(
                exception=UnexpectedAPIResponse(response.status, response.data),
                method="POST",
                path=path,
                request_kwargs={"data": body, "headers": headers},
            )
        return response

    def _validate_operation_result(self, result):
        if result.get("succeeded") is False:
            self.module.fail_json(
                msg="OVF library item operation failed",
                value=result,
            )
        error = result.get("error") or {}
        errors = error.get("errors") or []
        if errors:
            self.module.fail_json(
                msg="OVF library item operation reported errors",
                value=result,
            )

    def _get_library_item(self, library_item_id):
        path = self.build_path(LIBRARY_ITEM_PATH, {"library_item_id": library_item_id})
        response = self.client.get(path)
        if response.status == 404:
            return None
        item = response.json
        if "id" not in item:
            item["id"] = library_item_id
        return item

    def _find_library_item_by_name(self, library_id, name):
        if not library_id or not name:
            return None

        response = self.client.get(LIBRARY_ITEMS_PATH, query={"library_id": library_id})
        if response.status == 404:
            return None

        for item_id in normalize_list_response(response.json):
            item = self._get_library_item(item_id)
            if item and item.get("name") == name:
                return item
        return None

    def ensure_present(self):
        target = self.params.get("target") or {}
        create_spec = self.params.get("create_spec") or {}
        library_item_id = target.get("library_item_id")
        library_id = target.get("library_id")
        item_name = create_spec.get("name")

        if not library_item_id and library_id and item_name:
            existing = self._find_library_item_by_name(library_id, item_name)
            if existing:
                return {
                    "changed": False,
                    "id": existing["id"],
                    "value": existing,
                }

        body = self.build_payload(self.PAYLOAD_FORMAT["create"])
        if not self.module.check_mode:
            response = self._post(CREATE_PATH, body)
            result = response.json
            self._validate_operation_result(result)

            ovf_library_item_id = result.get("ovf_library_item_id")
            response_payload = {"changed": True, "value": result}
            if ovf_library_item_id:
                response_payload["id"] = ovf_library_item_id
            return response_payload

        return {"changed": True}

    def ensure_deploy(self):
        ovf_library_item_id = self.params.get("ovf_library_item_id")
        if not ovf_library_item_id:
            self.module.fail_json(
                msg="ovf_library_item_id is required when state=deploy"
            )
        if not self.params.get("deployment_spec"):
            self.module.fail_json(msg="deployment_spec is required when state=deploy")

        path = self.build_path(DEPLOY_PATH)
        body = self.build_payload(self.PAYLOAD_FORMAT["deploy"])
        if not self.module.check_mode:
            response = self._post(path, body)
            result = response.json
            self._validate_operation_result(result)

            response_payload = {"changed": True, "value": result}
            resource_id = result.get("resource_id")
            if resource_id:
                if isinstance(resource_id, dict):
                    response_payload["id"] = resource_id.get("id")
                else:
                    response_payload["id"] = resource_id
            return response_payload

        return {"changed": True}

    def ensure_filter(self):
        ovf_library_item_id = self.params.get("ovf_library_item_id")
        if not ovf_library_item_id:
            self.module.fail_json(
                msg="ovf_library_item_id is required when state=filter"
            )

        path = self.build_path(FILTER_PATH)
        body = self.build_payload(self.PAYLOAD_FORMAT["filter"])
        response = self._post(path, body)
        result = response.json
        return {"changed": False, "value": result}


def main():
    module_args = connection_params_argument_spec()
    module_args["state"] = {
        "type": "str",
        "choices": ["present", "deploy", "filter"],
        "default": "present",
    }
    module_args["client_token"] = {"type": "str", "no_log": True}
    module_args["ovf_library_item_id"] = {"type": "str"}
    module_args["source"] = {
        "type": "dict",
        "options": {
            "type": {
                "type": "str",
                "choices": ["VirtualMachine", "VirtualApp"],
                "required": True,
            },
            "id": {"type": "str", "required": True},
        },
    }
    module_args["target"] = {
        "type": "dict",
        "required": True,
        "options": {
            "library_id": {"type": "str"},
            "library_item_id": {"type": "str"},
            "resource_pool_id": {"type": "str"},
            "host_id": {"type": "str"},
            "folder_id": {"type": "str"},
        },
    }
    module_args["create_spec"] = {
        "type": "dict",
        "options": {
            "name": {"type": "str"},
            "description": {"type": "str"},
            "flags": {"type": "list", "elements": "str"},
            "library_item_source_id": {"type": "str"},
        },
    }
    module_args["deployment_spec"] = {
        "type": "dict",
        "options": {
            "name": {"type": "str"},
            "annotation": {"type": "str"},
            "accept_all_eula": {"type": "bool", "required": True},
            "network_mappings": {"type": "dict"},
            "subnet_mappings": {"type": "dict"},
            "storage_mappings": {"type": "dict"},
            "storage_provisioning": {
                "type": "str",
                "choices": ["thin", "thick", "eagerZeroedThick"],
            },
            "storage_profile_id": {"type": "str"},
            "locale": {"type": "str"},
            "flags": {"type": "list", "elements": "str"},
            "additional_parameters": {
                "type": "list",
                "elements": "dict",
            },
            "default_datastore_id": {"type": "str"},
            "vm_config_spec": {"type": "dict"},
            "tag_params": {"type": "dict"},
        },
    }

    module = AnsibleModule(
        argument_spec=module_args,
        required_if=[
            ("state", "present", ["source", "create_spec"]),
            ("state", "deploy", ["ovf_library_item_id", "deployment_spec"]),
            ("state", "filter", ["ovf_library_item_id"]),
        ],
        supports_check_mode=True,
    )

    ovf_module = VmwareRestOvfLibraryItemModule(module)
    state = module.params["state"]
    if state == "present":
        result = ovf_module.ensure_present()
    elif state == "deploy":
        result = ovf_module.ensure_deploy()
    elif state == "filter":
        result = ovf_module.ensure_filter()
    else:
        module.fail_json(msg="Unsupported state: {0}".format(state))

    module.exit_json(**result)


if __name__ == "__main__":
    main()
