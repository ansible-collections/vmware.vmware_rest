================================
vmware.vmware_rest Release Notes
================================

.. contents:: Topics


v0.3.0
======

Minor Changes
-------------

- Better documentation
- The module RETURN sections are now defined.
- vcenter_resourcepool - new module
- vcenter_resourcepool_info - new module
- vcenter_storage_policies - new module
- vcenter_storage_policies_compliance_vm_info - new module
- vcenter_storage_policies_entities_compliance_info - new module
- vcenter_storage_policies_info - new module
- vcenter_storage_policies_vm_info - new module

Deprecated Features
-------------------

- vcenter_vm_storage_policy_compliance - drop the module, it returns 404 error.
- vcenter_vm_tools - remove the ``upgrade`` state.
- vcenter_vm_tools_installer - remove the module from the collection.

v0.2.0
======

Bugfixes
--------

- Improve the documentation of the modules
- minor_changes - drop vcenter_vm_compute_policies_info because the API is flagged as Technology Preview
- minor_changes - drop vcenter_vm_console_tickets because the API is flagged as Technology Preview
- minor_changes - drop vcenter_vm_guest_power and keep vcenter_vm_power which provides the same features

v0.1.0
======

Bugfixes
--------

- Fix logic in vmware_cis_category_info module.
