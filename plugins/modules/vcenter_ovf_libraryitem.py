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
short_description: Manage OVF packages in vCenter content libraries.
description:
  - Create, deploy, and inspect OVF packages stored in VMware vCenter content libraries.
  - Use C(state=present) to export a virtual machine or virtual appliance as an OVF package
    into a content library item.
  - Use C(state=deploy) to deploy an OVF package from a content library item into a new
    virtual machine or virtual appliance on a target resource pool.
  - Use C(state=filter) to retrieve deployment information from an OVF package, such as
    network and storage requirements, EULAs, and additional parameters needed before deploying.

author:
  - Ansible Eco Content Team (@eco-ansible-content)

extends_documentation_fragment:
  - vmware.vmware_rest.connection_params

options:
  state:
    description:
      - The desired state of the resource.
      - Use C(present) to create or update the resource.
      - Use C(deploy) to perform the deploy action.
      - Use C(filter) to perform the filter action.
      - Only C(present) supports idempotence.
    type: str
    default: present
    choices:
      - present
      - deploy
      - filter
  ovf_library_item_id:
    description:
      - Identifier of the OVF library item to manage.
      - Required when C(state=deploy) or C(state=filter).
    type: str
    required: false
  source:
    description:
      - The virtual machine or virtual appliance to export as an OVF package.
      - Required when C(state=present).
    type: dict
    required: false
    suboptions:
      type:
        description:
          - Type of the source resource to export.
          - Must be one of C(VirtualMachine) or C(VirtualApp).
        type: str
        required: true
      id:
        description:
          - MOID of the source virtual machine or virtual appliance to export.
        type: str
        required: true
  target:
    description:
      - The destination for the operation.
      - When C(state=present), specifies the content library and optional library item to store the OVF package.
      - When C(state=deploy), specifies the resource pool, host, and folder where the VM or vApp will be created.
      - When C(state=filter), specifies the resource pool used to evaluate deployment requirements.
    type: dict
    required: false
    suboptions:
      library_id:
        description:
          - MOID of the content library in which a new library item should be created.
          - Not used if I(library_item_id) is specified.
          - This property is currently required when C(state=present).
        type: str
        required: false
      library_item_id:
        description:
          - MOID of an existing library item to update with the new OVF package.
          - If omitted, a new library item will be created. I(library_id) must be specified if this property is set.
        type: str
        required: false
      resource_pool_id:
        description:
          - MOID of the resource pool to which the virtual machine or virtual appliance should be deployed.
        type: str
        required: false
      host_id:
        description:
          - MOID of the target host on which the virtual machine or virtual appliance will run.
          - The target host must be a member of the cluster that contains the resource pool identified by I(resource_pool_id).
          - If omitted, the server will automatically select a target host from the resource pool when it is a stand-alone host or a cluster with DRS enabled.
        type: str
        required: false
      folder_id:
        description:
          - MOID of the vCenter folder that should contain the virtual machine or virtual appliance. The folder must be a virtual machine folder.
          - If omitted, the server will choose the deployment folder.
        type: str
        required: false
  create_spec:
    description:
      - Specification for creating the OVF package in the content library.
      - Allows overriding the name and description stored in the OVF descriptor.
      - Only used when C(state=present).
    type: dict
    required: false
    suboptions:
      name:
        description:
          - Name to use in the OVF descriptor stored in the library item.
          - If omitted, the server will use source's current name.
        type: str
        required: false
      description:
        description:
          - Description to use in the OVF descriptor stored in the library item.
          - If omitted, the server will use source's current annotation.
        type: str
        required: false
      flags:
        description:
          - Flags to use for OVF package creation.
          - If omitted, no flags will be used.
        type: list
        required: false
        elements: str
      library_item_source_id:
        description:
          - MOID of a source library item used for image identification.
          - This property was added in __vSphere API 9.1.0.0__.
          - If omitted, no source identifier will be used.
        type: str
        required: false
  deployment_spec:
    description:
      - Specification controlling how an OVF package is deployed to a resource pool.
      - Includes settings for naming, networking, storage, and EULA acceptance.
      - Only used when C(state=deploy).
    type: dict
    required: false
    suboptions:
      name:
        description:
          - Name assigned to the deployed target virtual machine or virtual appliance.
          - If omitted, the server will use the name from the OVF package.
        type: str
        required: false
      annotation:
        description:
          - Annotation assigned to the deployed target virtual machine or virtual appliance.
          - If omitted, the server will use the annotation from the OVF package.
        type: str
        required: false
      accept_all_eula:
        description:
          - Whether to accept all End User License Agreements included in the OVF package.
          - Use C(state=filter) to retrieve the EULAs before deploying.
        type: bool
        required: true
      network_mappings:
        description:
          - Mapping of OVF network names to vCenter network MOIDs.
          - The key is the network name from the OVF descriptor and the value is the MOID of the target vCenter network.
          - If omitted, the server will choose a network mapping.
        type: dict
        required: false
      subnet_mappings:
        description:
          - Mapping of OVF network names to vCenter subnet folder MOIDs.
          - The key is the network name from the OVF descriptor and the value is the MOID of the target subnet folder.
            If set, this takes precedence over I(network_mappings).
          - This property was added in __vSphere API 9.1.0.0__.
          - If omitted, I(network_mappings) will be used instead.
        type: dict
        required: false
      storage_mappings:
        description:
          - Mapping of OVF storage group names to target storage specifications.
          - The key is the storage group name from the OVF descriptor and the value is the target storage specification.
          - If omitted, the server will choose a storage mapping.
        type: dict
        required: false
      storage_provisioning:
        description:
          - Default storage provisioning type to use for all sections of type vmw:StorageSection in the OVF descriptor.
          - thin - A thin provisioned virtual disk has space allocated and zeroed on demand as the space is used.
          - thick - A thick provisioned virtual disk has all space allocated at creation time and the space is zeroed
            on demand as the space is used.
          - eagerZeroedThick - An eager zeroed thick provisioned virtual disk has all space allocated and wiped clean
            of any previous contents on the physical media at creation time.
          - Disks specified as eager zeroed thick may take longer time to create than disks specified with the other
            disk provisioning types.
          - If omitted, the server will choose the provisioning type.
        type: str
        required: false
        choices:
          - thin
          - thick
          - eagerZeroedThick
      storage_profile_id:
        description:
          - MOID of the default storage profile to use for all storage sections in the OVF descriptor.
          - If omitted, the server will choose the default profile.
        type: str
        required: false
      locale:
        description:
          - The locale to use for parsing the OVF descriptor.
          - If omitted, the server locale will be used.
        type: str
        required: false
      flags:
        description:
          - Flags to use for deployment.
          - If omitted, no flags will be used.
        type: list
        required: false
        elements: str
      additional_parameters:
        description:
          - Additional OVF parameters that may be needed for the deployment.
          - These parameters may be required by the OVF descriptor of the OVF package. Use
            C(state=filter) to discover which additional parameters are available.
          - Examples include deployment options, extra config, IP allocation, OVF properties,
            scale out, and vCenter extension parameters.
          - If omitted, the server will choose default settings for all parameters necessary
            for the deploy operation.
        type: list
        required: false
        elements: dict
        suboptions:
          type:
            description:
              - Unique identifier describing the type of the OVF parameters. The value is the name of
                the OVF parameters schema.
              - This property must be provided in the input parameters when deploying an OVF package.
                This property will always be present in the result when retrieving information about an
                OVF package.
            type: str
            required: false
      default_datastore_id:
        description:
          - MOID of the default datastore to use for all storage sections in the OVF descriptor.
          - If omitted, the server will choose the default datastore.
        type: str
        required: false
      vm_config_spec:
        description:
          - Virtual machine configuration settings to use in place of those defined in the OVF descriptor.
          - When set, the OVF descriptor is used only for disk definitions, while hardware specifications
            come from this configuration.
          - Other deployment spec settings such as I(name), I(storage_mappings), I(storage_profile_id),
            I(storage_provisioning), and I(default_datastore_id) still apply and are not overridden.
          - This property was added in __vSphere API 8.0.2.0__.
          - If omitted, the virtual machine specifications from the OVF descriptor will be used.
        type: dict
        required: false
        suboptions:
          provider:
            description:
              - The format provider for the VM configuration specification.
              - C(XML) - A vim.vm.ConfigSpec serialized to XML and base64 encoded.
              - This property was added in __vSphere API 8.0.2.0__.
            type: str
            required: true
            choices:
              - XML
          xml:
            description:
              - A vim.vm.ConfigSpec serialized to XML and base64 encoded.
              - This property was added in __vSphere API 8.0.2.0__.
              - Only relevant when I(provider) is set to C(XML).
            type: str
            required: false
      tag_params:
        description:
          - Tag parameters that contain the information required to attach tags to a VM during VM deployment.
          - This property was added in __vSphere API 9.1.0.0__.
          - This property is optional because it was added in a newer version than its parent node.
        type: dict
        required: false
        suboptions:
          tags:
            description:
              - List of tag parameters which contains information required to attach tags while deploying a VM.
              - This property was added in __vSphere API 9.1.0.0__.
              - This property is not used for the 'create' operation. It will always be present in the response
                of the 'get' or 'list' operations. It is not used for the 'update' operation.
            type: list
            required: false
            elements: dict
          type:
            description:
              - Unique identifier describing the type of the OVF parameters. The value is the name of the OVF parameters schema.
              - This property must be provided in the input parameters when deploying an OVF package. This property will always
                be present in the result when retrieving information about an OVF package.
            type: str
            required: false

version_added: 5.0.0

requirements: []

notes:
  - Generated from vSphere API spec 9.1.0.
"""

EXAMPLES = r"""
- name: Export a virtual machine to a content library as an OVF package
  vmware.vmware_rest.vcenter_ovf_libraryitem:
    source:
      type: VirtualMachine
      id: vm-123
    target:
      library_id: lib-456
    create_spec:
      name: my-vm-template
      description: OVF export of my production web server
    state: present

- name: Export a virtual machine into an existing library item
  vmware.vmware_rest.vcenter_ovf_libraryitem:
    source:
      type: VirtualMachine
      id: vm-123
    target:
      library_id: lib-456
      library_item_id: item-789
    create_spec:
      name: my-vm-template
    state: present

- name: Deploy an OVF package from a content library item
  vmware.vmware_rest.vcenter_ovf_libraryitem:
    ovf_library_item_id: item-789
    target:
      resource_pool_id: resgroup-1001
      folder_id: group-v1002
      host_id: host-1003
    deployment_spec:
      name: deployed-vm
      accept_all_eula: true
      storage_provisioning: thin
      network_mappings:
        VM Network: network-1004
    state: deploy

- name: Deploy an OVF package with a specific datastore and storage profile
  vmware.vmware_rest.vcenter_ovf_libraryitem:
    ovf_library_item_id: item-789
    target:
      resource_pool_id: resgroup-1001
    deployment_spec:
      name: deployed-vm-custom-storage
      accept_all_eula: true
      default_datastore_id: datastore-1005
      storage_profile_id: storageprofile-1006
      storage_provisioning: eagerZeroedThick
    state: deploy

- name: Retrieve OVF deployment information before deploying
  vmware.vmware_rest.vcenter_ovf_libraryitem:
    ovf_library_item_id: item-789
    target:
      resource_pool_id: resgroup-1001
    state: filter
"""

RETURN = r"""
id:
  description:
    - Identifier of the managed resource.
    - When C(state=present), this is the content library item identifier.
    - When C(state=deploy), this is the identifier of the deployed virtual machine or virtual appliance.
    - When C(state=filter), this is the OVF library item identifier that was queried.
  returned: When state is present, or when state is set to a supported action
  sample: item-789
  type: str
value:
  description:
    - The full API response body returned by the vCenter OVF library item operation.
    - When C(state=present), contains the operation result including library item ID
      and whether the operation succeeded.
    - When C(state=deploy), contains deployment result details including whether the
      operation succeeded, any errors, and resource references.
    - When C(state=filter), contains OVF deployment information such as network and
      storage requirements, EULAs, and additional parameters needed for deployment.
  returned: On success
  type: raw
  sample:
    succeeded: true
    resource_id:
      type: VirtualMachine
      id: vm-123
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

LIST_ENDPOINT = "/vcenter/ovf/library-item"
ITEM_ENDPOINT = ""


CREATE_OPERATION = OperationConfig(
    name="create",
    uri=LIST_ENDPOINT,
    http_method="POST",
    body_spec={
        "source": {
            "required": True,
            "subspec": {
                "type": {
                    "required": False,
                },
                "id": {
                    "required": False,
                },
            },
        },
        "target": {
            "required": True,
            "subspec": {
                "library_id": {
                    "required": False,
                },
                "library_item_id": {
                    "required": False,
                },
                "resource_pool_id": {
                    "required": False,
                },
                "host_id": {
                    "required": False,
                },
                "folder_id": {
                    "required": False,
                },
            },
        },
        "create_spec": {
            "required": True,
            "subspec": {
                "name": {
                    "required": False,
                },
                "description": {
                    "required": False,
                },
                "flags": {
                    "required": False,
                },
                "library_item_source_id": {
                    "required": False,
                },
            },
        },
    },
)


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
                    "resource_pool_id": {
                        "required": False,
                    },
                    "host_id": {
                        "required": False,
                    },
                    "folder_id": {
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
                    "resource_pool_id": {
                        "required": False,
                    },
                    "host_id": {
                        "required": False,
                    },
                    "folder_id": {
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
            "resource_pool_id": {
                "type": "str",
            },
            "host_id": {
                "type": "str",
            },
            "folder_id": {
                "type": "str",
            },
        },
    }
    module_args["state"] = {
        "type": "str",
        "choices": ["present", "deploy", "filter"],
        "default": "present",
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
        create_operation_config=CREATE_OPERATION,
        action_operations=ACTION_OPERATIONS,
    )

    try:
        if module.params["state"] == "present":
            result = crud_module.ensure_present()
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
