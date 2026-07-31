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
module: vcenter_ovf_libraryitem
short_description: Deploy an OVF package from a content library item or create a library item from a virtual machine.
description:
  - Deploy an OVF package stored in a content library item to a resource pool, or create an OVF library
    item from an existing virtual machine or virtual appliance.
  - Use C(state=deploy) to deploy an OVF package from a library item to a resource pool, creating a
    virtual machine or virtual appliance.
  - Use C(state=filter) to retrieve information about an OVF package in a library item, including
    deployment options, networks, and storage groups, to prepare for deployment.

author:
  - Ansible Eco Content Team (@eco-ansible-content)

extends_documentation_fragment:
  - vmware.vmware_rest.connection_params

options:
  state:
    description:
      - The action to perform on the OVF library item.
      - Use C(deploy) to deploy the OVF package from a content library item to a resource pool.
      - Use C(filter) to retrieve deployment information from the OVF package without deploying.
    type: str
    required: true
    choices:
      - deploy
      - filter
  ovf_library_item_id:
    description:
      - Identifier of the content library item containing the OVF package.
      - Required for both C(deploy) and C(filter) operations.
    type: str
    required: false
  source:
    description:
      - The source virtual machine or virtual appliance to create an OVF library item from.
    type: dict
    required: false
    suboptions:
      type:
        description:
          - Type of the deployable resource.
          - Must be one of C(VirtualMachine) or C(VirtualApp).
        type: str
        required: true
      id:
        description:
          - Identifier of the deployable resource.
          - Must be an identifier for a C(VirtualMachine) or C(VirtualApp) resource.
        type: str
        required: true
  target:
    description:
      - The target resource pool and optional folder for deploying the OVF package.
    type: dict
    required: false
    suboptions:
      library_id:
        description:
          - Identifier of the content library in which a new library item should be created.
          - Not used if I(library_item_id) is specified.
          - This property is currently required.
        type: str
        required: false
      library_item_id:
        description:
          - Identifier of the library item that should be updated.
          - If not specified, a new library item will be created and I(library_id) must be set.
        type: str
        required: false
  create_spec:
    description:
      - Specification for creating an OVF library item from a virtual machine or virtual appliance.
    type: dict
    required: false
    suboptions:
      name:
        description:
          - Name to use in the OVF descriptor stored in the library item.
          - If missing or 'null', the server will use source's current name.
        type: str
        required: false
      description:
        description:
          - Description to use in the OVF descriptor stored in the library item.
          - If missing or 'null', the server will use source's current annotation.
        type: str
        required: false
      flags:
        description:
          - Flags to use for OVF package creation. The supported flags can be obtained using GET /vcenter/ovf/export-flag.
          - If missing or 'null', no flags will be used.
        type: list
        required: false
        elements: str
      library_item_source_id:
        description:
          - Source identifier of the library item for image identification.
          - This property was added in vSphere API 9.1.0.0.
          - If not specified, no source identifier will be used.
        type: str
        required: false
  deployment_spec:
    description:
      - Specification for deploying the OVF package to a resource pool.
    type: dict
    required: false
    suboptions:
      name:
        description:
          - Name assigned to the deployed target virtual machine or virtual appliance.
          - If missing or 'null', the server will use the name from the OVF package.
        type: str
        required: false
      annotation:
        description:
          - Annotation assigned to the deployed target virtual machine or virtual appliance.
          - If missing or 'null', the server will use the annotation from the OVF package.
        type: str
        required: false
      accept_all_eula:
        description:
          - Whether to accept all End User License Agreements. See Vcenter.Ovf.LibraryItem.OvfSummary.EULAs.
        type: bool
        required: true
      network_mappings:
        description:
          - Mapping of OVF network section identifiers to target network MOIDs.
          - If not specified, the server will choose a network mapping.
        type: dict
        required: false
      subnet_mappings:
        description:
          - Mapping of OVF network section identifiers to target subnet folder MOIDs.
          - If set, takes precedence over I(network_mappings).
          - This property was added in vSphere API 9.1.0.0.
          - If not specified, I(network_mappings) will be used.
        type: dict
        required: false
      storage_mappings:
        description:
          - Mapping of OVF storage group section identifiers to target storage specifications.
          - If not specified, the server will choose a storage mapping.
        type: dict
        required: false
      storage_provisioning:
        description:
          - Default storage provisioning type to use for all sections of type vmw:StorageSection
            in the OVF descriptor.
          - C(thin) - Space is allocated and zeroed on demand as used.
          - C(thick) - All space is allocated at creation time, zeroed on demand.
          - C(eagerZeroedThick) - All space is allocated and wiped clean at creation time.
          - If not specified, the server will choose the provisioning type.
        type: str
        required: false
        choices:
          - thin
          - thick
          - eagerZeroedThick
      storage_profile_id:
        description:
          - Default storage profile MOID to use for all sections of type vmw:StorageSection
            in the OVF descriptor.
          - If not specified, the server will choose the default profile.
        type: str
        required: false
      locale:
        description:
          - The locale to use for parsing the OVF descriptor.
          - If missing or 'null', the server locale will be used.
        type: str
        required: false
      flags:
        description:
          - Flags to be use for deployment. The supported flag values can be obtained using GET /vcenter/ovf/import-flag.
          - If missing or 'null', no flags will be used.
        type: list
        required: false
        elements: str
      additional_parameters:
        description:
          - Additional OVF parameters that may be needed for the deployment.
          - "If not specified, the server will choose default settings."
        type: list
        required: false
        elements: dict
        suboptions:
          type:
            description:
              - Unique identifier describing the type of the OVF parameters.
              - The value is the name of the OVF parameters schema.
            type: str
            required: false
      default_datastore_id:
        description:
          - Default datastore MOID to use for all sections of type vmw:StorageSection
            in the OVF descriptor.
          - If not specified, the server will choose the default datastore.
        type: str
        required: false
      vm_config_spec:
        description:
          - Virtual machine configuration settings to use in place of the OVF descriptor.
          - If set, the OVF descriptor acts as a disk descriptor only.
          - Other deployment spec fields like I(name) and storage settings are still honored.
          - This property was added in vSphere API 8.0.2.0.
          - If not specified, VM specifications from the OVF descriptor will be used.
        type: dict
        required: false
        suboptions:
          provider:
            description:
              - Selects the provider for the VM configuration specification.
              - C(XML) - A vim.vm.ConfigSpec serialized to XML and base64 encoded.
              - This property was added in vSphere API 8.0.2.0.
            type: str
            required: true
            choices:
              - XML
          xml:
            description:
              - A vim.vm.ConfigSpec serialized to XML and base64 encoded.
              - Only relevant when I(provider) is C(XML).
              - This property was added in vSphere API 8.0.2.0.
            type: str
            required: false
      tag_params:
        description:
          - Tag parameters for attaching tags to a VM during deployment.
          - This property was added in vSphere API 9.1.0.0.
        type: dict
        required: false
        suboptions:
          tags:
            description:
              - List of tag parameters for attaching tags while deploying a VM.
              - This property was added in vSphere API 9.1.0.0.
            type: list
            required: false
            elements: dict
          type:
            description:
              - Unique identifier describing the type of the OVF parameters.
              - The value is the name of the OVF parameters schema.
            type: str
            required: false

version_added: 5.0.0

requirements: []

notes:
  - Generated from vSphere API spec 9.1.0.
"""

EXAMPLES = r"""
- name: Deploy an OVF library item to a resource pool
  vmware.vmware_rest.vcenter_ovf_libraryitem:
    ovf_library_item_id: "{{ library_item_id }}"
    state: deploy
    target:
      library_id: "{{ library_id }}"
    deployment_spec:
      name: my-deployed-vm
      accept_all_eula: true
      storage_provisioning: thin

- name: Deploy an OVF library item with network mappings
  vmware.vmware_rest.vcenter_ovf_libraryitem:
    ovf_library_item_id: "{{ library_item_id }}"
    state: deploy
    target:
      library_id: "{{ library_id }}"
    deployment_spec:
      name: my-deployed-vm
      annotation: Deployed from content library
      accept_all_eula: true
      network_mappings:
        VM Network: "{{ network_id }}"
      storage_provisioning: thin
      default_datastore_id: "{{ datastore_id }}"

- name: Filter an OVF library item to get deployment information
  vmware.vmware_rest.vcenter_ovf_libraryitem:
    ovf_library_item_id: "{{ library_item_id }}"
    state: filter
    target:
      library_id: "{{ library_id }}"
"""

RETURN = r"""
id:
  description:
    - Identifier of the deployed resource or the created library item.
  returned: When state is set to a supported action
  sample: vm-1234
  type: str
"""


from ansible.module_utils.basic import AnsibleModule
from ansible_collections.vmware.vmware_rest.plugins.module_utils._argument_spec import (
    connection_params_argument_spec,
)
from ansible_collections.vmware.vmware_rest.plugins.module_utils._errors import (
    VmwareModuleError,
)
from ansible_collections.vmware.vmware_rest.plugins.module_utils._crud_module import (
    VmwareRestCrudModuleBase,
)
from ansible_collections.vmware.vmware_rest.plugins.module_utils._operation_configs import (
    OperationConfig,
)

MOID_PARAMETER_HINTS = ["ovf_library_item_id"]

LIST_ENDPOINT = ""
ITEM_ENDPOINT = "/vcenter/ovf/library-item"


ACTION_OPERATIONS = {
    "deploy": OperationConfig(
        name="deploy",
        uri="/vcenter/ovf/library-item/{ovf_library_item_id}?action=deploy",
        http_method="POST",
        body_spec={
            "target": {
                "required": True,
                "subspec": {
                    "library_id": {
                        "required": False,
                    },
                    "library_item_id": {
                        "required": False,
                    },
                },
            },
            "deployment_spec": {
                "required": True,
                "subspec": {
                    "name": {
                        "required": False,
                    },
                    "annotation": {
                        "required": False,
                    },
                    "accept_all_eula": {
                        "required": False,
                    },
                    "network_mappings": {
                        "required": False,
                    },
                    "subnet_mappings": {
                        "required": False,
                    },
                    "storage_mappings": {
                        "required": False,
                    },
                    "storage_provisioning": {
                        "required": False,
                    },
                    "storage_profile_id": {
                        "required": False,
                    },
                    "locale": {
                        "required": False,
                    },
                    "flags": {
                        "required": False,
                    },
                    "additional_parameters": {
                        "required": False,
                    },
                    "default_datastore_id": {
                        "required": False,
                    },
                    "vm_config_spec": {
                        "required": False,
                        "subspec": {
                            "provider": {
                                "required": False,
                            },
                            "xml": {
                                "required": False,
                            },
                        },
                    },
                    "tag_params": {
                        "required": False,
                        "subspec": {
                            "tags": {
                                "required": False,
                            },
                            "type": {
                                "required": False,
                            },
                        },
                    },
                },
            },
        },
    ),
    "filter": OperationConfig(
        name="filter",
        uri="/vcenter/ovf/library-item/{ovf_library_item_id}?action=filter",
        http_method="POST",
        body_spec={
            "target": {
                "required": True,
                "subspec": {
                    "library_id": {
                        "required": False,
                    },
                    "library_item_id": {
                        "required": False,
                    },
                },
            },
        },
    ),
}


def create_module_argument_spec() -> dict:
    module_args = connection_params_argument_spec()
    module_args["create_spec"] = {
        "type": "dict",
        "options": {
            "name": {
                "type": "str",
            },
            "description": {
                "type": "str",
            },
            "flags": {
                "type": "list",
                "elements": "str",
            },
            "library_item_source_id": {
                "type": "str",
            },
        },
    }
    module_args["deployment_spec"] = {
        "type": "dict",
        "options": {
            "name": {
                "type": "str",
            },
            "annotation": {
                "type": "str",
            },
            "accept_all_eula": {
                "type": "bool",
                "required": True,
            },
            "network_mappings": {
                "type": "dict",
            },
            "subnet_mappings": {
                "type": "dict",
            },
            "storage_mappings": {
                "type": "dict",
            },
            "storage_provisioning": {
                "type": "str",
                "choices": ["thin", "thick", "eagerZeroedThick"],
            },
            "storage_profile_id": {
                "type": "str",
            },
            "locale": {
                "type": "str",
            },
            "flags": {
                "type": "list",
                "elements": "str",
            },
            "additional_parameters": {
                "type": "list",
                "elements": "dict",
                "options": {
                    "type": {
                        "type": "str",
                    },
                },
            },
            "default_datastore_id": {
                "type": "str",
            },
            "vm_config_spec": {
                "type": "dict",
                "options": {
                    "provider": {
                        "type": "str",
                        "choices": ["XML"],
                        "required": True,
                    },
                    "xml": {
                        "type": "str",
                    },
                },
            },
            "tag_params": {
                "type": "dict",
                "options": {
                    "tags": {
                        "type": "list",
                        "elements": "dict",
                    },
                    "type": {
                        "type": "str",
                    },
                },
            },
        },
    }
    module_args["ovf_library_item_id"] = {
        "type": "str",
    }
    module_args["source"] = {
        "type": "dict",
        "options": {
            "type": {
                "type": "str",
                "required": True,
            },
            "id": {
                "type": "str",
                "required": True,
            },
        },
    }
    module_args["target"] = {
        "type": "dict",
        "options": {
            "library_id": {
                "type": "str",
            },
            "library_item_id": {
                "type": "str",
            },
        },
    }
    module_args["state"] = {
        "type": "str",
        "choices": ["deploy", "filter"],
        "required": True,
    }
    return module_args


def main():
    module = AnsibleModule(
        argument_spec=create_module_argument_spec(),
        supports_check_mode=True,
    )

    crud_module = VmwareRestCrudModuleBase(
        module=module,
        moid_parameter_hints=MOID_PARAMETER_HINTS,
        action_operations=ACTION_OPERATIONS,
    )

    try:
        if module.params["state"] == "present":
            result = crud_module.ensure_present()
        elif module.params["state"] == "absent":
            result = crud_module.ensure_absent()
        elif module.params["state"] in ACTION_OPERATIONS:
            result = crud_module.perform_action()
        else:
            module.fail_json(
                msg="Unsupported state: {0}".format(module.params["state"])
            )
    except VmwareModuleError as e:
        module.fail_json(**e.to_module_fail_json_output())

    module.exit_json(**result)


if __name__ == "__main__":
    main()
