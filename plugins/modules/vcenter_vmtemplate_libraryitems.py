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
module: vcenter_vmtemplate_libraryitems
short_description: Manage virtual machine templates in vCenter content libraries.
description:
  - Create and deploy virtual machine template library items in VMware vCenter content libraries.
  - Use C(state=present) to create a new library item by capturing an existing virtual machine
    as a virtual machine template.
  - Use C(state=deploy) to deploy a new virtual machine from an existing virtual machine template
    library item onto a target resource pool, host, or cluster.

author:
  - Ansible Eco Content Team (@eco-ansible-content)

extends_documentation_fragment:
  - vmware.vmware_rest.connection_params

options:
  state:
    description:
      - The desired state of the resource.
      - Use C(present) to create a virtual machine template library item from a source virtual machine.
      - Use C(deploy) to deploy a new virtual machine from a template library item.
      - Only C(present) supports idempotence.
    type: str
    default: present
    choices:
      - present
      - deploy
  template_library_item:
    description:
      - Identifier of the template library item to deploy from.
      - Must be an identifier (MOID) for a C(TemplateLibraryItem) resource.
      - Required when C(state=deploy).
    type: str
    required: false
  source_vm:
    description:
      - Identifier of the source virtual machine to create the library item from.
      - Must be an identifier (MOID) for a C(VirtualMachine) resource.
      - Required when C(state=present).
      - This property was added in vSphere API 6.8.
    type: str
    required: false
  name:
    description:
      - When C(state=present), the name of the new library item to create.
      - When C(state=deploy), the name of the new virtual machine to deploy.
      - Required for both C(present) and C(deploy).
      - This property was added in vSphere API 6.8.
    type: str
    required: false
  description:
    description:
      - Description for the new library item.
      - If not set, the new library item inherits the description of the source virtual machine.
      - This property was added in vSphere API 6.8.
    type: str
    required: false
  library:
    description:
      - Identifier of the content library in which the new library item should be created.
      - Must be an identifier (MOID) for a C(com.vmware.content.Library) resource.
      - Required when C(state=present).
      - This property was added in vSphere API 6.8.
    type: str
    required: false
  vm_home_storage:
    description:
      - Storage location for the virtual machine template's configuration and log files.
      - If not set, the configuration and log files are placed on the default storage backing
        associated with the library given in I(library).
      - This property was added in vSphere API 6.8.
    type: dict
    required: false
    suboptions:
      datastore:
        description:
          - Identifier of the datastore that holds the template's configuration and log files.
          - Must be an identifier (MOID) for a C(Datastore) resource.
          - This suboption is currently required.
          - If I(storage_policy) is also set and is incompatible with this datastore, the template
            is flagged as out of compliance with that storage policy.
          - This property was added in vSphere API 6.8.
        type: str
        required: false
      storage_policy:
        description:
          - Storage policy for the template's configuration and log files.
          - If not set, I(datastore) must be specified and the configuration and log files use the
            default storage policy of that datastore.
          - This property was added in vSphere API 6.8.
        type: dict
        required: false
        suboptions:
          type:
            description:
              - Policy type to apply to the template's configuration and log files.
              - USE_SPECIFIED_POLICY - Use the storage policy given in I(policy).
              - This property was added in vSphere API 6.8.
            type: str
            required: true
            choices:
              - USE_SPECIFIED_POLICY
          policy:
            description:
              - Identifier of the storage policy to use.
              - Must be an identifier (MOID) for a C(com.vmware.spbm.StorageProfile) resource.
              - Only relevant when I(type) is C(USE_SPECIFIED_POLICY).
              - This property was added in vSphere API 6.8.
            type: str
            required: false
  disk_storage:
    description:
      - Default storage specification for the virtual machine template's disks.
      - Applies to any disk not listed in I(disk_storage_overrides).
      - If neither I(disk_storage) nor I(disk_storage_overrides) is set, the disks are placed on the
        default storage backing associated with the library given in I(library).
      - This property was added in vSphere API 6.8.
    type: dict
    required: false
    suboptions:
      datastore:
        description:
          - Identifier of the datastore for the template's disks.
          - Must be an identifier (MOID) for a C(Datastore) resource.
          - This suboption is currently required.
          - If I(storage_policy) is also set and is incompatible with this datastore, the disk is
            flagged as out of compliance with that storage policy.
          - This property was added in vSphere API 6.8.
        type: str
        required: false
      storage_policy:
        description:
          - Storage policy for the template's disks.
          - If not set, I(datastore) must be specified and the disks use the default storage policy
            of that datastore.
          - This property was added in vSphere API 6.8.
        type: dict
        required: false
        suboptions:
          type:
            description:
              - Policy type to apply to the template's disks.
              - USE_SPECIFIED_POLICY - Use the storage policy given in I(policy).
              - This property was added in vSphere API 6.8.
            type: str
            required: true
            choices:
              - USE_SPECIFIED_POLICY
          policy:
            description:
              - Identifier of the storage policy to use.
              - Must be an identifier (MOID) for a C(com.vmware.spbm.StorageProfile) resource.
              - Only relevant when I(type) is C(USE_SPECIFIED_POLICY).
              - This property was added in vSphere API 6.8.
            type: str
            required: false
  disk_storage_overrides:
    description:
      - Per-disk storage specifications for the virtual machine template.
      - Specified as a mapping of source virtual machine disk identifiers (MOIDs of
        C(com.vmware.vcenter.vm.hardware.Disk) resources) to their storage specifications.
      - Disks not listed here fall back to I(disk_storage), or to the library's default storage
        backing if I(disk_storage) is also unset.
      - This property was added in vSphere API 6.8.
    type: dict
    required: false
  placement:
    description:
      - Placement information for the virtual machine template.
      - This suboption is currently required.
      - Each specified value is used for placement. If the values, or the values combined with the
        placement of the source virtual machine, are contradictory, the operation fails.
      - This property was added in vSphere API 6.8.
    type: dict
    required: false
    suboptions:
      folder:
        description:
          - Identifier of the virtual machine folder to place the template in.
          - Must be an identifier (MOID) for a C(Folder) resource.
          - If not set, the template is placed in the same folder as the source virtual machine.
          - This property was added in vSphere API 6.8.
        type: str
        required: false
      resource_pool:
        description:
          - Identifier of the resource pool to place the template in.
          - Must be an identifier (MOID) for a C(ResourcePool) resource.
          - If not set, the system attempts to choose a suitable resource pool; the operation fails
            if one cannot be chosen.
          - This property was added in vSphere API 6.8.
        type: str
        required: false
      host:
        description:
          - Identifier of the host to place the template on.
          - Must be an identifier (MOID) for a C(HostSystem) resource.
          - If I(resource_pool) is also set, it must belong to this host. If I(cluster) is also set,
            this host must be a member of that cluster.
          - May be omitted if I(resource_pool) or I(cluster) is set. If not set, the system attempts
            to choose a suitable host; the operation fails if one cannot be chosen.
          - This property was added in vSphere API 6.8.
        type: str
        required: false
      cluster:
        description:
          - Identifier of the cluster to place the template on.
          - Must be an identifier (MOID) for a C(ClusterComputeResource) resource.
          - If I(resource_pool) is also set, it must belong to this cluster. If I(host) is also set,
            it must be a member of this cluster.
          - It is recommended to leave this unset when I(resource_pool) or I(host) is specified.
          - This property was added in vSphere API 6.8.
        type: str
        required: false
  powered_on:
    description:
      - Whether the deployed virtual machine should be powered on after deployment.
      - Applies when C(state=deploy). If not set, the virtual machine is left powered off.
      - This property was added in vSphere API 6.8.
    type: bool
    required: false
  guest_customization:
    description:
      - Guest customization to apply to the deployed virtual machine.
      - Applies when C(state=deploy). If not set, the guest operating system is not customized.
      - This property was added in vSphere API 6.8.
    type: dict
    required: false
    suboptions:
      name:
        description:
          - Name of an existing guest customization specification to apply.
          - If not set, no guest customization is performed.
          - This property was added in vSphere API 6.8.
        type: str
        required: false
  hardware_customization:
    description:
      - Hardware changes to apply to the deployed virtual machine.
      - Applies when C(state=deploy). If not set, the deployed virtual machine keeps the same
        hardware configuration as the template.
      - This property was added in vSphere API 6.8.
    type: dict
    required: false
    suboptions:
      nics:
        description:
          - Mapping of Ethernet adapters to update, keyed by adapter identifier (MOID of a
            C(com.vmware.vcenter.vm.hardware.Ethernet) resource).
          - If not set, all adapters stay connected to the same networks as in the template. An
            adapter with a manual MAC address keeps its address; adapters with generated or assigned
            MAC addresses receive new addresses.
          - This property was added in vSphere API 6.8.
        type: dict
        required: false
      disks_to_remove:
        description:
          - Identifiers of disks to remove from the deployed virtual machine.
          - Each entry must be an identifier (MOID) for a C(com.vmware.vcenter.vm.hardware.Disk) resource.
          - If not set, all disks are copied to the deployed virtual machine.
          - This property was added in vSphere API 6.8.
        type: list
        required: false
        elements: str
      disks_to_update:
        description:
          - Per-disk update specifications for the deployed virtual machine, keyed by disk identifier
            (MOID of a C(com.vmware.vcenter.vm.hardware.Disk) resource).
          - If not set, disks keep the same settings as the corresponding disks in the template.
          - This property was added in vSphere API 6.8.
        type: dict
        required: false
      cpu_update:
        description:
          - CPU changes to apply to the deployed virtual machine.
          - If not set, the deployed virtual machine keeps the template's CPU settings.
          - This property was added in vSphere API 6.8.
        type: dict
        required: false
        suboptions:
          num_cpus:
            description:
              - Number of virtual processors for the deployed virtual machine.
              - If not set, the deployed virtual machine keeps the template's CPU count.
              - This property was added in vSphere API 6.8.
            type: int
            required: false
          num_cores_per_socket:
            description:
              - Number of cores per socket for the deployed virtual machine.
              - If not set, the deployed virtual machine keeps the template's cores-per-socket value.
              - This property was added in vSphere API 6.8.
            type: int
            required: false
      memory_update:
        description:
          - Memory changes to apply to the deployed virtual machine.
          - If not set, the deployed virtual machine keeps the template's memory settings.
          - This property was added in vSphere API 6.8.
        type: dict
        required: false
        suboptions:
          memory:
            description:
              - Memory size for the deployed virtual machine, in MB.
              - If not set, the deployed virtual machine keeps the template's memory size.
              - This property was added in vSphere API 6.8.
            type: int
            required: false
  tags:
    description:
      - Tags to attach to the deployed virtual machine.
      - Applies when C(state=deploy).
      - This property was added in vSphere API 9.1.0.0.
    type: list
    required: false
    elements: dict
    suboptions:
      tag_id:
        description:
          - Identifier of the vSphere tag to attach.
          - If both I(tag_id) and I(tag_name_spec) are set, they must refer to the same vSphere tag.
          - Required if I(tag_name_spec) is not set.
          - This property was added in vSphere API 9.1.0.0.
        type: str
        required: false
      tag_name_spec:
        description:
          - Identifies the tag to attach by its name and category.
          - If both I(tag_id) and I(tag_name_spec) are set, they must refer to the same vSphere tag.
          - Required if I(tag_id) is not set.
          - This property was added in vSphere API 9.1.0.0.
        type: dict
        required: false
        suboptions:
          tag_name:
            description:
              - The name of the tag to attach.
              - This property was added in vSphere API 9.1.0.0.
            type: str
            required: true
          category_name:
            description:
              - The name of the vSphere category that the tag belongs to.
              - This property was added in vSphere API 9.1.0.0.
            type: str
            required: true

version_added: 5.0.0

requirements: []

notes:
  - Generated from vSphere API spec 9.1.0.
"""

EXAMPLES = r"""
- name: Create a VM template library item from an existing virtual machine
  vmware.vmware_rest.vcenter_vmtemplate_libraryitems:
    name: my-vm-template
    source_vm: vm-1001
    library: 570bdaa2-5f0a-45c8-8bb5-1234567890ab
    placement:
      folder: group-v1002
      resource_pool: resgroup-1003
    state: present

- name: Create a VM template library item with a specific home datastore
  vmware.vmware_rest.vcenter_vmtemplate_libraryitems:
    name: my-vm-template
    description: Golden image for web servers
    source_vm: vm-1001
    library: 570bdaa2-5f0a-45c8-8bb5-1234567890ab
    vm_home_storage:
      datastore: datastore-1004
    disk_storage:
      datastore: datastore-1004
    placement:
      resource_pool: resgroup-1003
    state: present

- name: Deploy a virtual machine from a template library item
  vmware.vmware_rest.vcenter_vmtemplate_libraryitems:
    template_library_item: 8a5f1c2d-9b3e-4f6a-8c7d-abcdef012345
    name: deployed-vm
    powered_on: true
    placement:
      folder: group-v1002
      resource_pool: resgroup-1003
    state: deploy

- name: Deploy a virtual machine with CPU and memory customization
  vmware.vmware_rest.vcenter_vmtemplate_libraryitems:
    template_library_item: 8a5f1c2d-9b3e-4f6a-8c7d-abcdef012345
    name: deployed-vm-custom
    powered_on: true
    placement:
      resource_pool: resgroup-1003
    hardware_customization:
      cpu_update:
        num_cpus: 4
        num_cores_per_socket: 2
      memory_update:
        memory: 8192
    state: deploy
"""

RETURN = r"""
id:
  description:
    - Identifier of the managed resource.
    - When C(state=present), this is the identifier of the created virtual machine template library item.
    - When C(state=deploy), this is the identifier of the deployed virtual machine.
  returned: When state is present, or when state is set to a supported action
  sample: vm-1010
  type: str
value:
  description:
    - The raw API response body from the vCenter operation.
    - When C(state=present), the identifier of the created library item.
    - When C(state=deploy), the identifier of the deployed virtual machine.
  returned: On success
  sample: vm-1010
  type: raw
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

MOID_PARAMETER_HINTS = ["template_library_item"]

LIST_ENDPOINT = "/vcenter/vm-template/library-items"
ITEM_ENDPOINT = "/vcenter/vm-template/library-items/{template_library_item}"


GET_OPERATION = OperationConfig(
    name="get",
    uri=ITEM_ENDPOINT,
    http_method="GET",
)

CREATE_OPERATION = OperationConfig(
    name="create",
    uri=LIST_ENDPOINT,
    http_method="POST",
    body_spec={
        "source_vm": {
            "required": True,
        },
        "name": {
            "required": True,
        },
        "description": {
            "required": False,
        },
        "library": {
            "required": True,
        },
        "vm_home_storage": {
            "required": False,
            "subspec": {
                "datastore": {
                    "required": False,
                },
                "storage_policy": {
                    "required": False,
                    "subspec": {
                        "type": {
                            "required": False,
                        },
                        "policy": {
                            "required": False,
                        },
                    },
                },
            },
        },
        "disk_storage": {
            "required": False,
            "subspec": {
                "datastore": {
                    "required": False,
                },
                "storage_policy": {
                    "required": False,
                    "subspec": {
                        "type": {
                            "required": False,
                        },
                        "policy": {
                            "required": False,
                        },
                    },
                },
            },
        },
        "disk_storage_overrides": {
            "required": False,
        },
        "placement": {
            "required": False,
            "subspec": {
                "folder": {
                    "required": False,
                },
                "resource_pool": {
                    "required": False,
                },
                "host": {
                    "required": False,
                },
                "cluster": {
                    "required": False,
                },
            },
        },
    },
)


ACTION_OPERATIONS = {
    "deploy": OperationConfig(
        name="deploy",
        uri="/vcenter/vm-template/library-items/{template_library_item}?action=deploy",
        http_method="POST",
        body_spec={
            "name": {
                "required": True,
            },
            "description": {
                "required": False,
            },
            "vm_home_storage": {
                "required": False,
                "subspec": {
                    "datastore": {
                        "required": False,
                    },
                    "storage_policy": {
                        "required": False,
                        "subspec": {
                            "type": {
                                "required": False,
                            },
                            "policy": {
                                "required": False,
                            },
                        },
                    },
                },
            },
            "disk_storage": {
                "required": False,
                "subspec": {
                    "datastore": {
                        "required": False,
                    },
                    "storage_policy": {
                        "required": False,
                        "subspec": {
                            "type": {
                                "required": False,
                            },
                            "policy": {
                                "required": False,
                            },
                        },
                    },
                },
            },
            "disk_storage_overrides": {
                "required": False,
            },
            "placement": {
                "required": False,
                "subspec": {
                    "folder": {
                        "required": False,
                    },
                    "resource_pool": {
                        "required": False,
                    },
                    "host": {
                        "required": False,
                    },
                    "cluster": {
                        "required": False,
                    },
                },
            },
            "powered_on": {
                "required": False,
            },
            "guest_customization": {
                "required": False,
                "subspec": {
                    "name": {
                        "required": False,
                    },
                },
            },
            "hardware_customization": {
                "required": False,
                "subspec": {
                    "nics": {
                        "required": False,
                    },
                    "disks_to_remove": {
                        "required": False,
                    },
                    "disks_to_update": {
                        "required": False,
                    },
                    "cpu_update": {
                        "required": False,
                        "subspec": {
                            "num_cpus": {
                                "required": False,
                            },
                            "num_cores_per_socket": {
                                "required": False,
                            },
                        },
                    },
                    "memory_update": {
                        "required": False,
                        "subspec": {
                            "memory": {
                                "required": False,
                            },
                        },
                    },
                },
            },
            "tags": {
                "required": False,
            },
        },
    ),
}


def create_module_argument_spec() -> dict:
    module_args = connection_params_argument_spec()
    module_args["description"] = {
        "type": "str",
    }
    module_args["disk_storage"] = {
        "type": "dict",
        "options": {
            "datastore": {
                "type": "str",
            },
            "storage_policy": {
                "type": "dict",
                "options": {
                    "type": {
                        "type": "str",
                        "choices": ["USE_SPECIFIED_POLICY"],
                        "required": True,
                    },
                    "policy": {
                        "type": "str",
                    },
                },
            },
        },
    }
    module_args["disk_storage_overrides"] = {
        "type": "dict",
    }
    module_args["guest_customization"] = {
        "type": "dict",
        "options": {
            "name": {
                "type": "str",
            },
        },
    }
    module_args["hardware_customization"] = {
        "type": "dict",
        "options": {
            "nics": {
                "type": "dict",
            },
            "disks_to_remove": {
                "type": "list",
                "elements": "str",
            },
            "disks_to_update": {
                "type": "dict",
            },
            "cpu_update": {
                "type": "dict",
                "options": {
                    "num_cpus": {
                        "type": "int",
                    },
                    "num_cores_per_socket": {
                        "type": "int",
                    },
                },
            },
            "memory_update": {
                "type": "dict",
                "options": {
                    "memory": {
                        "type": "int",
                    },
                },
            },
        },
    }
    module_args["library"] = {
        "type": "str",
    }
    module_args["name"] = {
        "type": "str",
    }
    module_args["placement"] = {
        "type": "dict",
        "options": {
            "folder": {
                "type": "str",
            },
            "resource_pool": {
                "type": "str",
            },
            "host": {
                "type": "str",
            },
            "cluster": {
                "type": "str",
            },
        },
    }
    module_args["powered_on"] = {
        "type": "bool",
    }
    module_args["source_vm"] = {
        "type": "str",
    }
    module_args["tags"] = {
        "type": "list",
        "elements": "dict",
        "options": {
            "tag_id": {
                "type": "str",
            },
            "tag_name_spec": {
                "type": "dict",
                "options": {
                    "tag_name": {
                        "type": "str",
                        "required": True,
                    },
                    "category_name": {
                        "type": "str",
                        "required": True,
                    },
                },
            },
        },
    }
    module_args["template_library_item"] = {
        "type": "str",
    }
    module_args["vm_home_storage"] = {
        "type": "dict",
        "options": {
            "datastore": {
                "type": "str",
            },
            "storage_policy": {
                "type": "dict",
                "options": {
                    "type": {
                        "type": "str",
                        "choices": ["USE_SPECIFIED_POLICY"],
                        "required": True,
                    },
                    "policy": {
                        "type": "str",
                    },
                },
            },
        },
    }
    module_args["state"] = {
        "type": "str",
        "choices": ["present", "deploy"],
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
        get_operation_config=GET_OPERATION,
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
