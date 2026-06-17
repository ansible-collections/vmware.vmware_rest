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
module: vcenter_vm_storage_policy
short_description: Configures storage policies for a virtual machine.
description:
  - Updates storage policies associated with a virtual machine's home directory
    and/or its virtual disks.
  - Only parameters explicitly specified by the user are sent to the API.
  - Use I(state=present) to apply storage policy changes.
author:
  - Ansible Eco Content Team (@eco-ansible-content)
extends_documentation_fragment:
  - vmware.vmware_rest.connection_params
options:
  state:
    description:
      - The desired state of the storage policy configuration.
      - Use C(present) to update storage policies on the virtual machine.
      - C(absent) is not supported because the API does not provide a delete operation.
    type: str
    choices:
      - present
      - absent
    default: present
  vm:
    description:
      - Virtual machine identifier.
      - Must be an identifier (MOID) for a C(VirtualMachine) resource.
    type: str
    required: true
  vm_home:
    description:
      - Storage policy specification for the virtual machine home directory.
    type: dict
    suboptions:
      type:
        description:
          - Policy type to use when updating the virtual machine home directory.
        type: str
        required: true
        choices:
          - USE_SPECIFIED_POLICY
          - USE_DEFAULT_POLICY
      policy:
        description:
          - Storage policy identifier.
          - Required when I(type=USE_SPECIFIED_POLICY).
          - Must be an identifier (MOID) for a C(com.vmware.vcenter.StoragePolicy) resource.
        type: str
  disks:
    description:
      - Storage policy specifications for virtual disks.
      - Keys must be identifiers (MOIDs) for C(com.vmware.vcenter.vm.hardware.Disk) resources.
    type: dict
    suboptions:
      type:
        description:
          - Policy type to use when updating the virtual disk.
        type: str
        required: true
        choices:
          - USE_SPECIFIED_POLICY
          - USE_DEFAULT_POLICY
      policy:
        description:
          - Storage policy identifier.
          - Required when I(type=USE_SPECIFIED_POLICY).
          - Must be an identifier (MOID) for a C(com.vmware.vcenter.StoragePolicy) resource.
        type: str
version_added: 4.11.0
requirements: []
notes:
  - Generated from vSphere API spec 9.1.0.
  - Has support for vSphere API 7.0.3.
  - Has support for vSphere API 8.0.2.
"""

EXAMPLES = r"""
- name: Set VM home to default storage policy
  vmware.vmware_rest.vcenter_vm_storage_policy:
    vm: vm-1009
    vm_home:
      type: USE_DEFAULT_POLICY

- name: Set storage policy on a virtual disk
  vmware.vmware_rest.vcenter_vm_storage_policy:
    vm: vm-1009
    disks:
      "2000":
        type: USE_SPECIFIED_POLICY
        policy: policy-123

- name: Attempt to remove storage policies (not supported by API)
  vmware.vmware_rest.vcenter_vm_storage_policy:
    state: absent
    vm: vm-1009
"""

RETURN = r"""
value:
  description:
    - Storage policy information for the virtual machine after an update, or the
      current configuration when no change was made.
  returned: On success when I(state=present)
  type: dict
  sample:
    vm_home: policy-123
    disks:
      "2000": policy-456
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.vmware.vmware_rest.plugins.module_utils._argument_spec import (
    connection_params_argument_spec,
)
from ansible_collections.vmware.vmware_rest.plugins.module_utils._module_base import (
    VmwareRestCrudModuleBase,
)

PATH = "/vcenter/vm/{vm}/storage/policy"

POLICY_TYPE_CHOICES = ["USE_SPECIFIED_POLICY", "USE_DEFAULT_POLICY"]

VM_HOME_POLICY_OPTIONS = {
    "type": {
        "type": "str",
        "choices": POLICY_TYPE_CHOICES,
        "required": True,
    },
    "policy": {"type": "str"},
}

_UPDATE_BODY = {
    "vm_home": "vm_home",
    "disks": "disks",
}


class VmwareRestCrudModule(VmwareRestCrudModuleBase):
    PAYLOAD_FORMAT = {
        "update": {
            "query": {},
            "body": _UPDATE_BODY,
            "path": {"vm": "vm"},
        },
    }

    UPDATABLE_PARAMS = ("vm_home", "disks")

    def ensure_present(self):
        update_body = self.build_payload(self.PAYLOAD_FORMAT["update"])
        if not update_body:
            self.module.fail_json(
                msg="At least one of vm_home or disks must be specified when state is present"
            )

        path = self.build_path(PATH)
        response = self.client.get(path)
        if response.status == 404:
            self.module.fail_json(
                msg="Virtual machine not found: {0}".format(self.params["vm"])
            )

        current = response.json
        if not self._update_needed(current, update_body):
            return {"changed": False, "value": current}

        if not self.module.check_mode:
            self.client.patch(path, data=update_body)
            updated = self.client.get(path)
            return {"changed": True, "value": updated.json}

        return {"changed": True, "value": current}

    def ensure_absent(self):
        return {"changed": False}

    def _update_needed(self, current, desired):
        if "vm_home" in desired:
            vm_home_spec = desired["vm_home"]
            if vm_home_spec.get("type") == "USE_SPECIFIED_POLICY":
                if current.get("vm_home") != vm_home_spec.get("policy"):
                    return True
            elif vm_home_spec.get("type") == "USE_DEFAULT_POLICY":
                return True

        if "disks" in desired:
            current_disks = current.get("disks", {})
            for disk_id, disk_spec in desired["disks"].items():
                if disk_spec.get("type") == "USE_SPECIFIED_POLICY":
                    if current_disks.get(disk_id) != disk_spec.get("policy"):
                        return True
                elif disk_spec.get("type") == "USE_DEFAULT_POLICY":
                    return True

        return False


def main():
    module_args = connection_params_argument_spec()
    module_args["state"] = {
        "type": "str",
        "choices": ["present", "absent"],
        "default": "present",
    }
    module_args["vm"] = {"type": "str", "required": True}
    module_args["vm_home"] = {
        "type": "dict",
        "options": VM_HOME_POLICY_OPTIONS,
    }
    module_args["disks"] = {"type": "dict"}

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
