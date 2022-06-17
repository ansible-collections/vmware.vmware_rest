# Ansible Collection: vmware.vmware_rest

This repo hosts the `vmware.vmware_rest` Ansible Collection.

The collection includes the VMware modules and plugins supported by Ansible VMware community to help the management of VMware infrastructure. These modules are different from `community.vmware` since they are based upon VMware vSphere REST API interface and not relying on any third party libraries such as [`Pyvmomi`](https://github.com/vmware/pyvmomi) and [`vSphere Automation SDK for Python`](https://github.com/vmware/vsphere-automation-sdk-python).

<!--start requires_ansible-->
## Ansible version compatibility

This collection has been tested against following Ansible versions: **>=2.9.10**.

For collections that support Ansible 2.9, please ensure you update your `network_os` to use the
fully qualified collection name (for example, `cisco.ios.ios`).
Plugins and modules within a collection may be tested with only specific Ansible versions.
A collection may contain metadata that identifies these versions.
PEP440 is the schema used to describe the versions of Ansible.
<!--end requires_ansible-->

## Python version compatibility

The collection depends on ``aiohttp`` has [requirement](https://docs.aiohttp.org/en/stable/) which requires Python 3.6 or greater.

## vSphere compatibility

The 2.0.0 version of this collection requires vSphere 7.0.2 or greater.

## Known limitations

### VM Template and folder structure

These modules are based on the [vSphere REST API](https://developer.vmware.com/apis/vsphere-automation/latest/). This API doesn't provide any mechanism to list or clone VM templates when they are stored in a VM folder.
To circumvent this limitation, you should store your VM templates in a [Content Library](https://docs.vmware.com/en/VMware-vSphere/7.0/com.vmware.vsphere.vm_admin.doc/GUID-254B2CE8-20A8-43F0-90E8-3F6776C2C896.html).

## Installation and Usage

### Install the dependencies

You can either install ``aiohttp`` using your OS package manager or using Python virtual environment.

Notes:
For RHEL, there is no ``python3-aiohttp`` package available (yet), you can either get it from EPEL or install ``aiohttp`` using pip.

### Installing the Collection from Ansible Galaxy

Before using the VMware collection, you need to install the collection with the `ansible-galaxy` CLI:

    ansible-galaxy collection install vmware.vmware_rest

You can also include it in a `requirements.yml` file and install it via `ansible-galaxy collection install -r requirements.yml` using the format:

```yaml
collections:
- name: vmware.vmware_rest
```

## Content

<!--start collection content-->
### Lookup plugins
Name | Description
--- | ---
[vmware.vmware_rest.cluster_moid](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.cluster_moid_lookup.rst)|Look up MoID for vSphere cluster objects using vCenter REST API
[vmware.vmware_rest.datacenter_moid](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.datacenter_moid_lookup.rst)|Look up MoID for vSphere datacenter objects using vCenter REST API
[vmware.vmware_rest.datastore_moid](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.datastore_moid_lookup.rst)|Look up MoID for vSphere datastore objects using vCenter REST API
[vmware.vmware_rest.folder_moid](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.folder_moid_lookup.rst)|Look up MoID for vSphere folder objects using vCenter REST API
[vmware.vmware_rest.host_moid](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.host_moid_lookup.rst)|Look up MoID for vSphere host objects using vCenter REST API
[vmware.vmware_rest.network_moid](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.network_moid_lookup.rst)|Look up MoID for vSphere network objects using vCenter REST API
[vmware.vmware_rest.resource_pool_moid](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.resource_pool_moid_lookup.rst)|Look up MoID for vSphere resource pool objects using vCenter REST API
[vmware.vmware_rest.vm_moid](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vm_moid_lookup.rst)|Look up MoID for vSphere vm objects using vCenter REST API

### Modules
Name | Description
--- | ---
[vmware.vmware_rest.appliance_access_consolecli](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.appliance_access_consolecli_module.rst)|Set enabled state of the console-based controlled CLI (TTY1).
[vmware.vmware_rest.appliance_access_consolecli_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.appliance_access_consolecli_info_module.rst)|Get enabled state of the console-based controlled CLI (TTY1).
[vmware.vmware_rest.appliance_access_dcui](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.appliance_access_dcui_module.rst)|Set enabled state of Direct Console User Interface (DCUI TTY2).
[vmware.vmware_rest.appliance_access_dcui_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.appliance_access_dcui_info_module.rst)|Get enabled state of Direct Console User Interface (DCUI TTY2).
[vmware.vmware_rest.appliance_access_shell](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.appliance_access_shell_module.rst)|Set enabled state of BASH, that is, access to BASH from within the controlled CLI.
[vmware.vmware_rest.appliance_access_shell_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.appliance_access_shell_info_module.rst)|Get enabled state of BASH, that is, access to BASH from within the controlled CLI.
[vmware.vmware_rest.appliance_access_ssh](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.appliance_access_ssh_module.rst)|Set enabled state of the SSH-based controlled CLI.
[vmware.vmware_rest.appliance_access_ssh_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.appliance_access_ssh_info_module.rst)|Get enabled state of the SSH-based controlled CLI.
[vmware.vmware_rest.appliance_health_applmgmt_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.appliance_health_applmgmt_info_module.rst)|Get health status of applmgmt services.
[vmware.vmware_rest.appliance_health_database_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.appliance_health_database_info_module.rst)|Returns the health status of the database.
[vmware.vmware_rest.appliance_health_databasestorage_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.appliance_health_databasestorage_info_module.rst)|Get database storage health.
[vmware.vmware_rest.appliance_health_load_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.appliance_health_load_info_module.rst)|Get load health.
[vmware.vmware_rest.appliance_health_mem_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.appliance_health_mem_info_module.rst)|Get memory health.
[vmware.vmware_rest.appliance_health_softwarepackages_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.appliance_health_softwarepackages_info_module.rst)|Get information on available software updates available in the remote vSphere Update Manager repository
[vmware.vmware_rest.appliance_health_storage_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.appliance_health_storage_info_module.rst)|Get storage health.
[vmware.vmware_rest.appliance_health_swap_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.appliance_health_swap_info_module.rst)|Get swap health.
[vmware.vmware_rest.appliance_health_system_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.appliance_health_system_info_module.rst)|Get overall health of system.
[vmware.vmware_rest.appliance_infraprofile_configs](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.appliance_infraprofile_configs_module.rst)|Exports the desired profile specification.
[vmware.vmware_rest.appliance_infraprofile_configs_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.appliance_infraprofile_configs_info_module.rst)|List all the profiles which are registered.
[vmware.vmware_rest.appliance_localaccounts_globalpolicy](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.appliance_localaccounts_globalpolicy_module.rst)|Set the global password policy.
[vmware.vmware_rest.appliance_localaccounts_globalpolicy_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.appliance_localaccounts_globalpolicy_info_module.rst)|Get the global password policy.
[vmware.vmware_rest.appliance_localaccounts_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.appliance_localaccounts_info_module.rst)|Get the local user account information.
[vmware.vmware_rest.appliance_monitoring_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.appliance_monitoring_info_module.rst)|Get monitored item info
[vmware.vmware_rest.appliance_monitoring_query](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.appliance_monitoring_query_module.rst)|Get monitoring data.
[vmware.vmware_rest.appliance_networking](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.appliance_networking_module.rst)|Reset and restarts network configuration on all interfaces, also this will renew the DHCP lease for DHCP IP address.
[vmware.vmware_rest.appliance_networking_dns_domains](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.appliance_networking_dns_domains_module.rst)|Set DNS search domains.
[vmware.vmware_rest.appliance_networking_dns_domains_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.appliance_networking_dns_domains_info_module.rst)|Get list of DNS search domains.
[vmware.vmware_rest.appliance_networking_dns_hostname](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.appliance_networking_dns_hostname_module.rst)|Set the Fully Qualified Domain Name.
[vmware.vmware_rest.appliance_networking_dns_hostname_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.appliance_networking_dns_hostname_info_module.rst)|Get the Fully Qualified Doman Name.
[vmware.vmware_rest.appliance_networking_dns_servers](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.appliance_networking_dns_servers_module.rst)|Set the DNS server configuration
[vmware.vmware_rest.appliance_networking_dns_servers_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.appliance_networking_dns_servers_info_module.rst)|Get DNS server configuration.
[vmware.vmware_rest.appliance_networking_firewall_inbound](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.appliance_networking_firewall_inbound_module.rst)|Set the ordered list of firewall rules to allow or deny traffic from one or more incoming IP addresses
[vmware.vmware_rest.appliance_networking_firewall_inbound_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.appliance_networking_firewall_inbound_info_module.rst)|Get the ordered list of firewall rules
[vmware.vmware_rest.appliance_networking_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.appliance_networking_info_module.rst)|Get Networking information for all configured interfaces.
[vmware.vmware_rest.appliance_networking_interfaces_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.appliance_networking_interfaces_info_module.rst)|Get information about a particular network interface.
[vmware.vmware_rest.appliance_networking_interfaces_ipv4](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.appliance_networking_interfaces_ipv4_module.rst)|Set IPv4 network configuration for specific network interface.
[vmware.vmware_rest.appliance_networking_interfaces_ipv4_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.appliance_networking_interfaces_ipv4_info_module.rst)|Get IPv4 network configuration for specific NIC.
[vmware.vmware_rest.appliance_networking_interfaces_ipv6](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.appliance_networking_interfaces_ipv6_module.rst)|Set IPv6 network configuration for specific interface.
[vmware.vmware_rest.appliance_networking_interfaces_ipv6_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.appliance_networking_interfaces_ipv6_info_module.rst)|Get IPv6 network configuration for specific interface.
[vmware.vmware_rest.appliance_networking_noproxy](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.appliance_networking_noproxy_module.rst)|Sets servers for which no proxy configuration should be applied
[vmware.vmware_rest.appliance_networking_noproxy_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.appliance_networking_noproxy_info_module.rst)|Returns servers for which no proxy configuration will be applied.
[vmware.vmware_rest.appliance_networking_proxy](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.appliance_networking_proxy_module.rst)|Configures which proxy server to use for the specified protocol
[vmware.vmware_rest.appliance_networking_proxy_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.appliance_networking_proxy_info_module.rst)|Gets the proxy configuration for a specific protocol.
[vmware.vmware_rest.appliance_ntp](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.appliance_ntp_module.rst)|Set NTP servers
[vmware.vmware_rest.appliance_ntp_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.appliance_ntp_info_module.rst)|Get the NTP configuration status
[vmware.vmware_rest.appliance_services](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.appliance_services_module.rst)|Restarts a service
[vmware.vmware_rest.appliance_services_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.appliance_services_info_module.rst)|Returns the state of a service.
[vmware.vmware_rest.appliance_shutdown](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.appliance_shutdown_module.rst)|Cancel pending shutdown action.
[vmware.vmware_rest.appliance_shutdown_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.appliance_shutdown_info_module.rst)|Get details about the pending shutdown action.
[vmware.vmware_rest.appliance_system_globalfips](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.appliance_system_globalfips_module.rst)|Enable/Disable Global FIPS mode for the appliance
[vmware.vmware_rest.appliance_system_globalfips_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.appliance_system_globalfips_info_module.rst)|Get current appliance FIPS settings.
[vmware.vmware_rest.appliance_system_storage](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.appliance_system_storage_module.rst)|Resize all partitions to 100 percent of disk size.
[vmware.vmware_rest.appliance_system_storage_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.appliance_system_storage_info_module.rst)|Get disk to partition mapping.
[vmware.vmware_rest.appliance_system_time_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.appliance_system_time_info_module.rst)|Get system time.
[vmware.vmware_rest.appliance_system_time_timezone](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.appliance_system_time_timezone_module.rst)|Set time zone.
[vmware.vmware_rest.appliance_system_time_timezone_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.appliance_system_time_timezone_info_module.rst)|Get time zone.
[vmware.vmware_rest.appliance_system_version_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.appliance_system_version_info_module.rst)|Get the version.
[vmware.vmware_rest.appliance_timesync](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.appliance_timesync_module.rst)|Set time synchronization mode.
[vmware.vmware_rest.appliance_timesync_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.appliance_timesync_info_module.rst)|Get time synchronization mode.
[vmware.vmware_rest.appliance_update_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.appliance_update_info_module.rst)|Gets the current status of the appliance update.
[vmware.vmware_rest.appliance_vmon_service](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.appliance_vmon_service_module.rst)|Lists details of services managed by vMon.
[vmware.vmware_rest.appliance_vmon_service_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.appliance_vmon_service_info_module.rst)|Returns the state of a service.
[vmware.vmware_rest.content_configuration](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.content_configuration_module.rst)|Updates the configuration
[vmware.vmware_rest.content_configuration_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.content_configuration_info_module.rst)|Retrieves the current configuration values.
[vmware.vmware_rest.content_library_item_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.content_library_item_info_module.rst)|Returns the {@link ItemModel} with the given identifier.
[vmware.vmware_rest.content_locallibrary](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.content_locallibrary_module.rst)|Creates a new local library.
[vmware.vmware_rest.content_locallibrary_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.content_locallibrary_info_module.rst)|Returns a given local library.
[vmware.vmware_rest.content_subscribedlibrary](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.content_subscribedlibrary_module.rst)|Creates a new subscribed library
[vmware.vmware_rest.content_subscribedlibrary_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.content_subscribedlibrary_info_module.rst)|Returns a given subscribed library.
[vmware.vmware_rest.vcenter_cluster_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_cluster_info_module.rst)|Retrieves information about the cluster corresponding to {@param.name cluster}.
[vmware.vmware_rest.vcenter_datacenter](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_datacenter_module.rst)|Create a new datacenter in the vCenter inventory
[vmware.vmware_rest.vcenter_datacenter_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_datacenter_info_module.rst)|Retrieves information about the datacenter corresponding to {@param.name datacenter}.
[vmware.vmware_rest.vcenter_datastore_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_datastore_info_module.rst)|Retrieves information about the datastore indicated by {@param.name datastore}.
[vmware.vmware_rest.vcenter_folder_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_folder_info_module.rst)|Returns information about at most 1000 visible (subject to permission checks) folders in vCenter matching the {@link FilterSpec}.
[vmware.vmware_rest.vcenter_host](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_host_module.rst)|Add a new standalone host in the vCenter inventory
[vmware.vmware_rest.vcenter_host_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_host_info_module.rst)|Returns information about at most 2500 visible (subject to permission checks) hosts in vCenter matching the {@link FilterSpec}.
[vmware.vmware_rest.vcenter_network_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_network_info_module.rst)|Returns information about at most 1000 visible (subject to permission checks) networks in vCenter matching the {@link FilterSpec}.
[vmware.vmware_rest.vcenter_ovf_libraryitem](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_ovf_libraryitem_module.rst)|Creates a library item in content library from a virtual machine or virtual appliance
[vmware.vmware_rest.vcenter_resourcepool](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_resourcepool_module.rst)|Creates a resource pool.
[vmware.vmware_rest.vcenter_resourcepool_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_resourcepool_info_module.rst)|Retrieves information about the resource pool indicated by {@param.name resourcePool}.
[vmware.vmware_rest.vcenter_storage_policies_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_storage_policies_info_module.rst)|Returns information about at most 1024 visible (subject to permission checks) storage solicies availabe in vCenter
[vmware.vmware_rest.vcenter_vm](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_vm_module.rst)|Creates a virtual machine.
[vmware.vmware_rest.vcenter_vm_guest_customization](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_vm_guest_customization_module.rst)|Applies a customization specification on the virtual machine
[vmware.vmware_rest.vcenter_vm_guest_filesystem_directories](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_vm_guest_filesystem_directories_module.rst)|Creates a directory in the guest operating system
[vmware.vmware_rest.vcenter_vm_guest_identity_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_vm_guest_identity_info_module.rst)|Return information about the guest.
[vmware.vmware_rest.vcenter_vm_guest_localfilesystem_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_vm_guest_localfilesystem_info_module.rst)|Returns details of the local file systems in the guest operating system.
[vmware.vmware_rest.vcenter_vm_guest_networking_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_vm_guest_networking_info_module.rst)|Returns information about the network configuration in the guest operating system.
[vmware.vmware_rest.vcenter_vm_guest_networking_interfaces_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_vm_guest_networking_interfaces_info_module.rst)|Returns information about the networking interfaces in the guest operating system.
[vmware.vmware_rest.vcenter_vm_guest_networking_routes_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_vm_guest_networking_routes_info_module.rst)|Returns information about network routing in the guest operating system.
[vmware.vmware_rest.vcenter_vm_guest_operations_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_vm_guest_operations_info_module.rst)|Get information about the guest operation status.
[vmware.vmware_rest.vcenter_vm_guest_power](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_vm_guest_power_module.rst)|Issues a request to the guest operating system asking it to perform a soft shutdown, standby (suspend) or soft reboot
[vmware.vmware_rest.vcenter_vm_guest_power_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_vm_guest_power_info_module.rst)|Returns information about the guest operating system power state.
[vmware.vmware_rest.vcenter_vm_hardware](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_vm_hardware_module.rst)|Updates the virtual hardware settings of a virtual machine.
[vmware.vmware_rest.vcenter_vm_hardware_adapter_sata](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_vm_hardware_adapter_sata_module.rst)|Adds a virtual SATA adapter to the virtual machine.
[vmware.vmware_rest.vcenter_vm_hardware_adapter_sata_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_vm_hardware_adapter_sata_info_module.rst)|Returns information about a virtual SATA adapter.
[vmware.vmware_rest.vcenter_vm_hardware_adapter_scsi](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_vm_hardware_adapter_scsi_module.rst)|Adds a virtual SCSI adapter to the virtual machine.
[vmware.vmware_rest.vcenter_vm_hardware_adapter_scsi_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_vm_hardware_adapter_scsi_info_module.rst)|Returns information about a virtual SCSI adapter.
[vmware.vmware_rest.vcenter_vm_hardware_boot](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_vm_hardware_boot_module.rst)|Updates the boot-related settings of a virtual machine.
[vmware.vmware_rest.vcenter_vm_hardware_boot_device](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_vm_hardware_boot_device_module.rst)|Sets the virtual devices that will be used to boot the virtual machine
[vmware.vmware_rest.vcenter_vm_hardware_boot_device_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_vm_hardware_boot_device_info_module.rst)|Returns an ordered list of boot devices for the virtual machine
[vmware.vmware_rest.vcenter_vm_hardware_boot_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_vm_hardware_boot_info_module.rst)|Returns the boot-related settings of a virtual machine.
[vmware.vmware_rest.vcenter_vm_hardware_cdrom](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_vm_hardware_cdrom_module.rst)|Adds a virtual CD-ROM device to the virtual machine.
[vmware.vmware_rest.vcenter_vm_hardware_cdrom_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_vm_hardware_cdrom_info_module.rst)|Returns information about a virtual CD-ROM device.
[vmware.vmware_rest.vcenter_vm_hardware_cpu](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_vm_hardware_cpu_module.rst)|Updates the CPU-related settings of a virtual machine.
[vmware.vmware_rest.vcenter_vm_hardware_cpu_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_vm_hardware_cpu_info_module.rst)|Returns the CPU-related settings of a virtual machine.
[vmware.vmware_rest.vcenter_vm_hardware_disk](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_vm_hardware_disk_module.rst)|Adds a virtual disk to the virtual machine
[vmware.vmware_rest.vcenter_vm_hardware_disk_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_vm_hardware_disk_info_module.rst)|Returns information about a virtual disk.
[vmware.vmware_rest.vcenter_vm_hardware_ethernet](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_vm_hardware_ethernet_module.rst)|Adds a virtual Ethernet adapter to the virtual machine.
[vmware.vmware_rest.vcenter_vm_hardware_ethernet_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_vm_hardware_ethernet_info_module.rst)|Returns information about a virtual Ethernet adapter.
[vmware.vmware_rest.vcenter_vm_hardware_floppy](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_vm_hardware_floppy_module.rst)|Adds a virtual floppy drive to the virtual machine.
[vmware.vmware_rest.vcenter_vm_hardware_floppy_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_vm_hardware_floppy_info_module.rst)|Returns information about a virtual floppy drive.
[vmware.vmware_rest.vcenter_vm_hardware_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_vm_hardware_info_module.rst)|Returns the virtual hardware settings of a virtual machine.
[vmware.vmware_rest.vcenter_vm_hardware_memory](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_vm_hardware_memory_module.rst)|Updates the memory-related settings of a virtual machine.
[vmware.vmware_rest.vcenter_vm_hardware_memory_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_vm_hardware_memory_info_module.rst)|Returns the memory-related settings of a virtual machine.
[vmware.vmware_rest.vcenter_vm_hardware_parallel](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_vm_hardware_parallel_module.rst)|Adds a virtual parallel port to the virtual machine.
[vmware.vmware_rest.vcenter_vm_hardware_parallel_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_vm_hardware_parallel_info_module.rst)|Returns information about a virtual parallel port.
[vmware.vmware_rest.vcenter_vm_hardware_serial](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_vm_hardware_serial_module.rst)|Adds a virtual serial port to the virtual machine.
[vmware.vmware_rest.vcenter_vm_hardware_serial_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_vm_hardware_serial_info_module.rst)|Returns information about a virtual serial port.
[vmware.vmware_rest.vcenter_vm_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_vm_info_module.rst)|Returns information about a virtual machine.
[vmware.vmware_rest.vcenter_vm_libraryitem_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_vm_libraryitem_info_module.rst)|Returns the information about the library item associated with the virtual machine.
[vmware.vmware_rest.vcenter_vm_power](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_vm_power_module.rst)|Operate a boot, hard shutdown, hard reset or hard suspend on a guest.
[vmware.vmware_rest.vcenter_vm_power_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_vm_power_info_module.rst)|Returns the power state information of a virtual machine.
[vmware.vmware_rest.vcenter_vm_storage_policy](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_vm_storage_policy_module.rst)|Updates the storage policy configuration of a virtual machine and/or its associated virtual hard disks.
[vmware.vmware_rest.vcenter_vm_storage_policy_compliance](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_vm_storage_policy_compliance_module.rst)|Returns the storage policy Compliance {@link Info} of a virtual machine after explicitly re-computing compliance check.
[vmware.vmware_rest.vcenter_vm_storage_policy_compliance_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_vm_storage_policy_compliance_info_module.rst)|Returns the cached storage policy compliance information of a virtual machine.
[vmware.vmware_rest.vcenter_vm_storage_policy_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_vm_storage_policy_info_module.rst)|Returns Information about Storage Policy associated with a virtual machine's home directory and/or its virtual hard disks.
[vmware.vmware_rest.vcenter_vm_tools](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_vm_tools_module.rst)|Update the properties of VMware Tools.
[vmware.vmware_rest.vcenter_vm_tools_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_vm_tools_info_module.rst)|Get the properties of VMware Tools.
[vmware.vmware_rest.vcenter_vm_tools_installer](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_vm_tools_installer_module.rst)|Connects the VMware Tools CD installer as a CD-ROM for the guest operating system
[vmware.vmware_rest.vcenter_vm_tools_installer_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_vm_tools_installer_info_module.rst)|Get information about the VMware Tools installer.
[vmware.vmware_rest.vcenter_vmtemplate_libraryitems](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_vmtemplate_libraryitems_module.rst)|Creates a library item in content library from a virtual machine
[vmware.vmware_rest.vcenter_vmtemplate_libraryitems_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_vmtemplate_libraryitems_info_module.rst)|Returns information about a virtual machine template contained in the library item specified by {@param.name templateLibraryItem}

<!--end collection content-->

### Documentation

The [VMware REST modules guide](https://docs.ansible.com/ansible/devel/scenario_guides/guide_vmware_rest.html) gives a step by step introduction of the collection.

## Testing and Development

Please, don't open Pull Request against the [vmware_rest](https://github.com/ansible-collections/vmware_rest) repository.
We use a project called [vmware_rest_code_generate](https://github.com/ansible-collections/vmware_rest_code_generator) to generate these modules and your change would be lost.


### Testing with `ansible-test`


```
virtualenv -p python3.7 .virtualenv/py37  # Or any other version greater than 3.6
source .virtualenv/py37/bin/activate
pip install -r requirements.txt -r test-requirements.txt
ansible-test network-integration --python 3.7 --inventory /tmp/inventory-vmware_rest vcenter_vm_scenario1
```

## Release notes

See [CHANGELOG.rst](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/CHANGELOG.rst).

## Releasing, Versioning and Deprecation

This collection follows [Semantic Versioning](https://semver.org/). More details on versioning can be found [in the Ansible docs](https://docs.ansible.com/ansible/latest/dev_guide/developing_collections.html#collection-versions).

We plan to regularly release new minor or bugfix versions once new features or bugfixes have been implemented.

Releasing the current major version happens from the `main` branch.

We currently are not planning any deprecations or new major releases like 2.0.0 containing backwards incompatible changes. If backwards incompatible changes are needed, we plan to deprecate the old behavior as early as possible. We also plan to backport at least bugfixes for the old major version for some time after releasing a new major version. We will not block community members from backporting other bugfixes and features from the latest stable version to older release branches, under the condition that these backports are of reasonable quality.

## Communication

We have a dedicated Working Group for VMware.
You can find other people interested in this in `#ansible-vmware` on [libera.chat](https://libera.chat/) IRC.
For more information about communities, meetings and agendas see https://github.com/ansible/community/wiki/VMware.

## Code of Conduct

This repository adheres to the [Ansible Community code of conduct](https://docs.ansible.com/ansible/latest/community/code_of_conduct.html)


## More information

<!-- List out where the user can find additional information, such as working group meeting times, slack/IRC channels, or documentation for the product this collection automates. At a minimum, link to: -->

- [Ansible Collection overview](https://github.com/ansible-collections/overview)
- [Ansible User guide](https://docs.ansible.com/ansible/latest/user_guide/index.html)
- [Ansible Developer guide](https://docs.ansible.com/ansible/latest/dev_guide/index.html)

## License

GNU General Public License v3.0 or later

See [LICENSE](LICENSE) to see the full text.
