================================
vmware.vmware_rest Release Notes
================================

.. contents:: Topics


v1.0.2
======

Minor Changes
-------------

- vcenter_resourcepool - add example in documentation.
- vcenter_resourcepool_info - add example in documentation.

v1.0.1
======

Minor Changes
-------------

- Ensure the shellcheck sanity test pass

v1.0.0
======

Minor Changes
-------------

- documentation - clarify that we don't have any required parameters.
- vcenter_host_connect - remove the module, use ``vcenter_host``
- vcenter_host_disconnect - remove the module, use ``vcenter_host``
- vcenter_storage_policies - remove vcenter_storage_policies
- vcenter_storage_policies_compliance_vm_info - remove the module
- vcenter_storage_policies_entities_compliance_info - remove the module
- vcenter_storage_policies_vm_info - remove the module

New Modules
-----------

- vcenter_cluster_info - Collect the information associated with the vCenter clusters
- vcenter_datacenter - Manage the datacenter of a vCenter
- vcenter_datacenter_info - Collect the information associated with the vCenter datacenters
- vcenter_datastore_info - Collect the information associated with the vCenter datastores
- vcenter_folder_info - Collect the information associated with the vCenter folders
- vcenter_host - Manage the host of a vCenter
- vcenter_host_info - Collect the information associated with the vCenter hosts
- vcenter_network_info - Collect the information associated with the vCenter networks
- vcenter_resourcepool - Manage the resourcepool of a vCenter
- vcenter_resourcepool_info - Collect the information associated with the vCenter resourcepools
- vcenter_storage_policies_info - Collect the information associated with the vCenter storage policiess
- vcenter_vm - Manage the vm of a vCenter
- vcenter_vm_guest_identity_info - Collect the guest identity information
- vcenter_vm_guest_localfilesystem_info - Collect the guest localfilesystem information
- vcenter_vm_guest_networking_info - Collect the guest networking information
- vcenter_vm_guest_networking_interfaces_info - Collect the guest networking interfaces information
- vcenter_vm_guest_networking_routes_info - Collect the guest networking routes information
- vcenter_vm_hardware - Manage the hardware of a VM
- vcenter_vm_hardware_adapter_sata - Manage the SATA adapter of a VM
- vcenter_vm_hardware_adapter_sata_info - Collect the SATA adapter information from a VM
- vcenter_vm_hardware_adapter_scsi - Manage the SCSI adapter of a VM
- vcenter_vm_hardware_adapter_scsi_info - Collect the SCSI adapter information from a VM
- vcenter_vm_hardware_boot - Manage the boot of a VM
- vcenter_vm_hardware_boot_device - Manage the boot device of a VM
- vcenter_vm_hardware_boot_device_info - Collect the boot device information from a VM
- vcenter_vm_hardware_boot_info - Collect the boot information from a VM
- vcenter_vm_hardware_cdrom - Manage the cdrom of a VM
- vcenter_vm_hardware_cdrom_info - Collect the cdrom information from a VM
- vcenter_vm_hardware_cpu - Manage the cpu of a VM
- vcenter_vm_hardware_cpu_info - Collect the cpu information from a VM
- vcenter_vm_hardware_disk - Manage the disk of a VM
- vcenter_vm_hardware_disk_info - Collect the disk information from a VM
- vcenter_vm_hardware_ethernet - Manage the ethernet of a VM
- vcenter_vm_hardware_ethernet_info - Collect the ethernet information from a VM
- vcenter_vm_hardware_floppy - Manage the floppy of a VM
- vcenter_vm_hardware_floppy_info - Collect the floppy information from a VM
- vcenter_vm_hardware_info - Manage the info of a VM
- vcenter_vm_hardware_memory - Manage the memory of a VM
- vcenter_vm_hardware_memory_info - Collect the memory information from a VM
- vcenter_vm_hardware_parallel - Manage the parallel of a VM
- vcenter_vm_hardware_parallel_info - Collect the parallel information from a VM
- vcenter_vm_hardware_serial - Manage the serial of a VM
- vcenter_vm_hardware_serial_info - Collect the serial information from a VM
- vcenter_vm_info - Collect the  information from a VM
- vcenter_vm_libraryitem_info - Collect the libraryitem  information from a VM
- vcenter_vm_power - Manage the power of a VM
- vcenter_vm_power_info - Collect the power  information from a VM
- vcenter_vm_storage_policy - Manage the storage policy of a VM
- vcenter_vm_storage_policy_compliance_info - Collect the storage policy compliance  information from a VM
- vcenter_vm_storage_policy_info - Collect the storage policy  information from a VM
- vcenter_vm_tools - Manage the tools of a VM
- vcenter_vm_tools_info - Collect the tools  information from a VM

v0.4.0
======

Minor Changes
-------------

- The format of the output of the Modules is now documented in the RETURN block.
- vcenter_rest_log_file - this optional parameter can be used to point on the log file where all the HTTP interaction will be record.

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
