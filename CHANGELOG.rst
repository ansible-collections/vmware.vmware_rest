================================
vmware.vmware_rest Release Notes
================================

.. contents:: Topics


v2.0.0
======

Minor Changes
-------------

- Handle import error with correct exception raised while importing aiohttp

Breaking Changes / Porting Guide
--------------------------------

- The vmware_rest 2.0.0 support vSphere 7.0.2 onwards.
- vcenter_vm_storage_policy - the format of the ``disks`` parameter has changed.
- vcenter_vm_storage_policy - the module has a new mandatory paramter: ``vm_home``.

Bugfixes
--------

- Properly handle ``validate_certs`` as a boolean and accept all the standard Ansible values (``yes``, ``true``, ``y``, ``no``, etc).

New Modules
-----------

- appliance_access_consolecli - Set enabled state of the console-based controlled CLI (TTY1).
- appliance_access_consolecli_info - Get enabled state of the console-based controlled CLI (TTY1).
- appliance_access_dcui - Set enabled state of Direct Console User Interface (DCUI TTY2).
- appliance_access_dcui_info - Get enabled state of Direct Console User Interface (DCUI TTY2).
- appliance_access_shell - Set enabled state of BASH, that is, access to BASH from within the controlled CLI.
- appliance_access_shell_info - Get enabled state of BASH, that is, access to BASH from within the controlled CLI.
- appliance_access_ssh - Set enabled state of the SSH-based controlled CLI.
- appliance_access_ssh_info - Get enabled state of the SSH-based controlled CLI.
- appliance_health_applmgmt_info - Get health status of applmgmt services.
- appliance_health_database_info - Returns the health status of the database.
- appliance_health_databasestorage_info - Get database storage health.
- appliance_health_load_info - Get load health.
- appliance_health_mem_info - Get memory health.
- appliance_health_softwarepackages_info - Get information on available software updates available in the remote vSphere Update Manager repository
- appliance_health_storage_info - Get storage health.
- appliance_health_swap_info - Get swap health.
- appliance_health_system_info - Get overall health of system.
- appliance_infraprofile_configs - Exports the desired profile specification.
- appliance_infraprofile_configs_info - List all the profiles which are registered.
- appliance_localaccounts - Create a new local user account.
- appliance_localaccounts_globalpolicy - Set the global password policy.
- appliance_localaccounts_globalpolicy_info - Get the global password policy.
- appliance_localaccounts_info - Get the local user account information.
- appliance_monitoring_info - Get monitored item info
- appliance_monitoring_query - Get monitoring data.
- appliance_networking - Reset and restarts network configuration on all interfaces, also this will renew the DHCP lease for DHCP IP address.
- appliance_networking_dns_domains - Set DNS search domains.
- appliance_networking_dns_domains_info - Get list of DNS search domains.
- appliance_networking_dns_hostname - Set the Fully Qualified Domain Name.
- appliance_networking_dns_hostname_info - Get the Fully Qualified Doman Name.
- appliance_networking_dns_servers - Set the DNS server configuration
- appliance_networking_dns_servers_info - Get DNS server configuration.
- appliance_networking_firewall_inbound - Set the ordered list of firewall rules to allow or deny traffic from one or more incoming IP addresses
- appliance_networking_firewall_inbound_info - Get the ordered list of firewall rules
- appliance_networking_info - Get Networking information for all configured interfaces.
- appliance_networking_interfaces_info - Get information about a particular network interface.
- appliance_networking_interfaces_ipv4 - Set IPv4 network configuration for specific network interface.
- appliance_networking_interfaces_ipv4_info - Get IPv4 network configuration for specific NIC.
- appliance_networking_interfaces_ipv6 - Set IPv6 network configuration for specific interface.
- appliance_networking_interfaces_ipv6_info - Get IPv6 network configuration for specific interface.
- appliance_networking_noproxy - Sets servers for which no proxy configuration should be applied
- appliance_networking_noproxy_info - Returns servers for which no proxy configuration will be applied.
- appliance_networking_proxy - Configures which proxy server to use for the specified protocol
- appliance_networking_proxy_info - Gets the proxy configuration for a specific protocol.
- appliance_ntp - Set NTP servers
- appliance_ntp_info - Get the NTP configuration status
- appliance_services - Restarts a service
- appliance_services_info - Returns the state of a service.
- appliance_shutdown - Cancel pending shutdown action.
- appliance_shutdown_info - Get details about the pending shutdown action.
- appliance_system_globalfips - Enable/Disable Global FIPS mode for the appliance
- appliance_system_globalfips_info - Get current appliance FIPS settings.
- appliance_system_storage - Resize all partitions to 100 percent of disk size.
- appliance_system_storage_info - Get disk to partition mapping.
- appliance_system_time_info - Get system time.
- appliance_system_time_timezone - Set time zone.
- appliance_system_time_timezone_info - Get time zone.
- appliance_system_version_info - Get the version.
- appliance_timesync - Set time synchronization mode.
- appliance_timesync_info - Get time synchronization mode.
- appliance_update_info - Gets the current status of the appliance update.
- appliance_vmon_service - Lists details of services managed by vMon.
- appliance_vmon_service_info - Returns the state of a service.
- content_configuration - Updates the configuration
- content_configuration_info - Retrieves the current configuration values.
- content_library_item_info - Returns the {@link ItemModel} with the given identifier.
- content_locallibrary - Creates a new local library.
- content_locallibrary_info - Returns a given local library.
- content_subscribedlibrary - Creates a new subscribed library
- content_subscribedlibrary_info - Returns a given subscribed library.
- vcenter_ovf_libraryitem - Creates a library item in content library from a virtual machine or virtual appliance
- vcenter_vm_guest_environment_info - Reads a single environment variable from the guest operating system
- vcenter_vm_guest_filesystem - Initiates an operation to transfer a file to or from the guest
- vcenter_vm_guest_filesystem_directories - Creates a directory in the guest operating system
- vcenter_vm_guest_filesystem_files - Creates a temporary file
- vcenter_vm_guest_filesystem_files_info - Returns information about a file or directory in the guest
- vcenter_vm_guest_operations_info - Get information about the guest operation status.
- vcenter_vm_guest_processes - Starts a program in the guest operating system
- vcenter_vm_guest_processes_info - Returns the status of a process running in the guest operating system, including those started by {@link Processes#create} that may have recently completed

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
