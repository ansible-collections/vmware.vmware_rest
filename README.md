# Ansible Collection: vmware.vmware_rest 

This repo hosts the `vmware.vmware_rest` Ansible Collection.

The collection includes the VMware modules and plugins supported by Ansible VMware community to help the management of VMware infrastructure. These modules are different from `community.vmware` since they are based upon VMware vSphere REST API interface and not relying on any third party libraries such as [`Pyvmomi`](https://github.com/vmware/pyvmomi) and [`vSphere Automation SDK for Python`](https://github.com/vmware/vsphere-automation-sdk-python).

<!--start requires_ansible-->
## Ansible version compatibility

This collection has been tested against following Ansible versions: **>=2.9.10**.

Plugins and modules within a collection may be tested with only specific Ansible versions.
A collection may contain metadata that identifies these versions.
PEP440 is the schema used to describe the versions of Ansible.
<!--end requires_ansible-->

## Content

<!--start collection content-->
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
[vmware.vmware_rest.appliance_health_softwarepackages_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.appliance_health_softwarepackages_info_module.rst)|Get information on available software updates available in the remote vSphere Update Manager repository. Red indicates that security updates are available. Orange indicates that non-security updates are available. Green indicates that there are no updates available. Gray indicates that there was an error retreiving information on software updates.
[vmware.vmware_rest.appliance_health_storage_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.appliance_health_storage_info_module.rst)|Get storage health.
[vmware.vmware_rest.appliance_health_swap_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.appliance_health_swap_info_module.rst)|Get swap health.
[vmware.vmware_rest.appliance_health_system_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.appliance_health_system_info_module.rst)|Get overall health of system.
[vmware.vmware_rest.appliance_infraprofile_configs](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.appliance_infraprofile_configs_module.rst)|Exports the desired profile specification.
[vmware.vmware_rest.appliance_infraprofile_configs_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.appliance_infraprofile_configs_info_module.rst)|List all the profiles which are registered.
[vmware.vmware_rest.appliance_localaccounts](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.appliance_localaccounts_module.rst)|Update selected fields in local user account properties.
[vmware.vmware_rest.appliance_localaccounts_globalpolicy](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.appliance_localaccounts_globalpolicy_module.rst)|Set the global password policy.
[vmware.vmware_rest.appliance_localaccounts_globalpolicy_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.appliance_localaccounts_globalpolicy_info_module.rst)|Get the global password policy.
[vmware.vmware_rest.appliance_localaccounts_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.appliance_localaccounts_info_module.rst)|Get the local user account information.
[vmware.vmware_rest.appliance_monitoring_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.appliance_monitoring_info_module.rst)|Get monitored item info
[vmware.vmware_rest.appliance_monitoring_query](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.appliance_monitoring_query_module.rst)|Get monitoring data.
[vmware.vmware_rest.appliance_networking](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.appliance_networking_module.rst)|Enable or Disable ipv6 on all interfaces
[vmware.vmware_rest.appliance_networking_dns_domains](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.appliance_networking_dns_domains_module.rst)|Add domain to DNS search domains.
[vmware.vmware_rest.appliance_networking_dns_domains_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.appliance_networking_dns_domains_info_module.rst)|Get list of DNS search domains.
[vmware.vmware_rest.appliance_networking_dns_hostname](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.appliance_networking_dns_hostname_module.rst)|Test the Fully Qualified Domain Name.
[vmware.vmware_rest.appliance_networking_dns_hostname_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.appliance_networking_dns_hostname_info_module.rst)|Get the Fully Qualified Doman Name.
[vmware.vmware_rest.appliance_networking_dns_servers](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.appliance_networking_dns_servers_module.rst)|Test if dns servers are reachable.
[vmware.vmware_rest.appliance_networking_dns_servers_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.appliance_networking_dns_servers_info_module.rst)|Get DNS server configuration.
[vmware.vmware_rest.appliance_networking_firewall_inbound](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.appliance_networking_firewall_inbound_module.rst)|Set the ordered list of firewall rules to allow or deny traffic from one or more incoming IP addresses. This overwrites the existing firewall rules and creates a new rule list. Within the list of traffic rules, rules are processed in order of appearance, from top to bottom. For example, the list of rules can be as follows: <table> <tr> <th>Address</th><th>Prefix</th><th>Interface Name</th><th>Policy</th> </tr> <tr> <td>10.112.0.1</td><td>0</td><td>*</td><td>REJECT</td> </tr> <tr> <td>10.112.0.1</td><td>0</td><td>nic0</td><td>ACCEPT</td> </tr> </table> In the above example, the first rule drops all packets originating from 10.112.0.1 and<br> the second rule accepts all packets originating from 10.112.0.1 only on nic0. In effect, the second rule is always ignored which is not desired, hence the order has to be swapped. When a connection matches a firewall rule, further processing for the connection stops, and the appliance ignores any additional firewall rules you have set.
[vmware.vmware_rest.appliance_networking_firewall_inbound_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.appliance_networking_firewall_inbound_info_module.rst)|Get the ordered list of firewall rules. Within the list of traffic rules, rules are processed in order of appearance, from top to bottom. When a connection matches a firewall rule, further processing for the connection stops, and the appliance ignores any additional firewall rules you have set.
[vmware.vmware_rest.appliance_networking_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.appliance_networking_info_module.rst)|Get Networking information for all configured interfaces.
[vmware.vmware_rest.appliance_networking_interfaces_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.appliance_networking_interfaces_info_module.rst)|Get information about a particular network interface.
[vmware.vmware_rest.appliance_networking_interfaces_ipv4](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.appliance_networking_interfaces_ipv4_module.rst)|Set IPv4 network configuration for specific network interface.
[vmware.vmware_rest.appliance_networking_interfaces_ipv4_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.appliance_networking_interfaces_ipv4_info_module.rst)|Get IPv4 network configuration for specific NIC.
[vmware.vmware_rest.appliance_networking_interfaces_ipv6](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.appliance_networking_interfaces_ipv6_module.rst)|Set IPv6 network configuration for specific interface.
[vmware.vmware_rest.appliance_networking_interfaces_ipv6_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.appliance_networking_interfaces_ipv6_info_module.rst)|Get IPv6 network configuration for specific interface.
[vmware.vmware_rest.appliance_networking_noproxy](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.appliance_networking_noproxy_module.rst)|Sets servers for which no proxy configuration should be applied. This operation sets environment variables. In order for this operation to take effect, a logout from appliance or a service restart is required. If IPv4 is enabled, "127.0.0.1" and "localhost" will always bypass the proxy (even if they are not explicitly configured).
[vmware.vmware_rest.appliance_networking_noproxy_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.appliance_networking_noproxy_info_module.rst)|Returns servers for which no proxy configuration will be applied.
[vmware.vmware_rest.appliance_networking_proxy](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.appliance_networking_proxy_module.rst)|Tests a proxy configuration by testing the connection to the proxy server and test host.
[vmware.vmware_rest.appliance_networking_proxy_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.appliance_networking_proxy_info_module.rst)|Gets the proxy configuration for a specific protocol.
[vmware.vmware_rest.appliance_ntp](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.appliance_ntp_module.rst)|Test the connection to a list of ntp servers.
[vmware.vmware_rest.appliance_ntp_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.appliance_ntp_info_module.rst)|Get the NTP configuration status. If you run the 'timesync.get' command, you can retrieve the current time synchronization method (NTP- or VMware Tools-based). The 'ntp' command always returns the NTP server information, even when the time synchronization mode is not set to NTP. If the time synchronization mode is not NTP-based, the NTP server status is displayed as down.
[vmware.vmware_rest.appliance_services](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.appliance_services_module.rst)|Stops a service
[vmware.vmware_rest.appliance_services_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.appliance_services_info_module.rst)|Returns the state of a service.
[vmware.vmware_rest.appliance_shutdown](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.appliance_shutdown_module.rst)|Reboot the appliance.
[vmware.vmware_rest.appliance_shutdown_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.appliance_shutdown_info_module.rst)|Get details about the pending shutdown action.
[vmware.vmware_rest.appliance_system_globalfips](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.appliance_system_globalfips_module.rst)|Enable/Disable Global FIPS mode for the appliance. <p><b>Caution:</b> Changing the value of this setting will reboot the Appliance.
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
[vmware.vmware_rest.appliance_vmon_service](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.appliance_vmon_service_module.rst)|Stops a service
[vmware.vmware_rest.appliance_vmon_service_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.appliance_vmon_service_info_module.rst)|Returns the state of a service.
[vmware.vmware_rest.content_library_item_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.content_library_item_info_module.rst)|Returns the {@link ItemModel} with the given identifier.
[vmware.vmware_rest.content_locallibrary](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.content_locallibrary_module.rst)|Updates the properties of a local library. <p> This is an incremental update to the local library. {@term Fields} that are {@term unset} in the update specification will be left unchanged.
[vmware.vmware_rest.content_locallibrary_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.content_locallibrary_info_module.rst)|Returns a given local library.
[vmware.vmware_rest.content_subscribedlibrary](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.content_subscribedlibrary_module.rst)|Updates the properties of a subscribed library. <p> This is an incremental update to the subscribed library. {@term Fields} that are {@term unset} in the update specification will be left unchanged.
[vmware.vmware_rest.content_subscribedlibrary_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.content_subscribedlibrary_info_module.rst)|Returns a given subscribed library.
[vmware.vmware_rest.vcenter_cluster_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_cluster_info_module.rst)|Retrieves information about the cluster corresponding to {@param.name cluster}.
[vmware.vmware_rest.vcenter_datacenter](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_datacenter_module.rst)|Create a new datacenter in the vCenter inventory
[vmware.vmware_rest.vcenter_datacenter_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_datacenter_info_module.rst)|Retrieves information about the datacenter corresponding to {@param.name datacenter}.
[vmware.vmware_rest.vcenter_datastore_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_datastore_info_module.rst)|Retrieves information about the datastore indicated by {@param.name datastore}.
[vmware.vmware_rest.vcenter_folder_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_folder_info_module.rst)|Returns information about at most 1000 visible (subject to permission checks) folders in vCenter matching the {@link FilterSpec}.
[vmware.vmware_rest.vcenter_host](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_host_module.rst)|Connect to the host corresponding to {@param.name host} previously added to the vCenter server.
[vmware.vmware_rest.vcenter_host_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_host_info_module.rst)|Returns information about at most 2500 visible (subject to permission checks) hosts in vCenter matching the {@link FilterSpec}.
[vmware.vmware_rest.vcenter_network_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_network_info_module.rst)|Returns information about at most 1000 visible (subject to permission checks) networks in vCenter matching the {@link FilterSpec}.
[vmware.vmware_rest.vcenter_resourcepool](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_resourcepool_module.rst)|Updates the configuration of a resource pool.
[vmware.vmware_rest.vcenter_resourcepool_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_resourcepool_info_module.rst)|Retrieves information about the resource pool indicated by {@param.name resourcePool}.
[vmware.vmware_rest.vcenter_storage_policies_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_storage_policies_info_module.rst)|Returns information about at most 1024 visible (subject to permission checks) storage solicies availabe in vCenter. These storage policies can be used for provisioning virtual machines or disks.
[vmware.vmware_rest.vcenter_vm](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_vm_module.rst)|Creates a virtual machine from existing virtual machine files on storage.
[vmware.vmware_rest.vcenter_vm_guest_customization](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_vm_guest_customization_module.rst)|Applies a customization specification in {@param.name spec} on the virtual machine in {@param.name vm}. This {@term operation} only sets the specification settings for the virtual machine. The actual customization happens inside the guest when the virtual machine is powered on. If {@param.name spec} has {@term unset} values, then any pending customization settings for the virtual machine are cleared. If there is a pending customization for the virtual machine and {@param.name spec} has valid content, then the existing customization setting will be overwritten with the new settings.
[vmware.vmware_rest.vcenter_vm_guest_environment_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_vm_guest_environment_info_module.rst)|Reads a single environment variable from the guest operating system. <p> If the authentication uses {@link Credentials#interactiveSession}, then the environment being read will be that of the user logged into the desktop. Otherwise it's the environment of the system user. <p>
[vmware.vmware_rest.vcenter_vm_guest_filesystem](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_vm_guest_filesystem_module.rst)|Initiates an operation to transfer a file to or from the guest. <p> If the power state of the Virtual Machine is changed when the file transfer is in progress, or the Virtual Machine is migrated, then the transfer operation is aborted. <p> When transferring a file into the guest and overwriting an existing file, the old file attributes are not preserved. <p> In order to ensure a secure connection to the host when transferring a file using HTTPS, the X.509 certificate for the host must be used to authenticate the remote end of the connection. The certificate of the host that the virtual machine is running on can be retrieved using the following fields: XXX insert link to certificate in Host config XXX <p>
[vmware.vmware_rest.vcenter_vm_guest_filesystem_directories](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_vm_guest_filesystem_directories_module.rst)|Creates a temporary directory. <p> Creates a new unique temporary directory for the user to use as needed. The guest operating system may clean up the directory after a guest specific amount of time if {@param.name parentPath} is not set, or the user can remove the directory when no longer needed. <p> The new directory name will be created in a guest-specific format using {@param.name prefix}, a guest generated string and {@param.name suffix} in {@param.name parentPath}. <p>
[vmware.vmware_rest.vcenter_vm_guest_filesystem_files](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_vm_guest_filesystem_files_module.rst)|Creates a temporary file. <p> Creates a new unique temporary file for the user to use as needed. The user is responsible for removing it when it is no longer needed. <p> The new file name will be created in a guest-specific format using {@param.name prefix}, a guest generated string and {@param.name suffix} in {@param.name parentPath}. <p>
[vmware.vmware_rest.vcenter_vm_guest_filesystem_files_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_vm_guest_filesystem_files_info_module.rst)|Returns information about a file or directory in the guest. <p>
[vmware.vmware_rest.vcenter_vm_guest_identity_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_vm_guest_identity_info_module.rst)|Return information about the guest.
[vmware.vmware_rest.vcenter_vm_guest_localfilesystem_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_vm_guest_localfilesystem_info_module.rst)|Returns details of the local file systems in the guest operating system.
[vmware.vmware_rest.vcenter_vm_guest_networking_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_vm_guest_networking_info_module.rst)|Returns information about the network configuration in the guest operating system.
[vmware.vmware_rest.vcenter_vm_guest_networking_interfaces_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_vm_guest_networking_interfaces_info_module.rst)|Returns information about the networking interfaces in the guest operating system.
[vmware.vmware_rest.vcenter_vm_guest_networking_routes_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_vm_guest_networking_routes_info_module.rst)|Returns information about network routing in the guest operating system.
[vmware.vmware_rest.vcenter_vm_guest_operations_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_vm_guest_operations_info_module.rst)|Get information about the guest operation status.
[vmware.vmware_rest.vcenter_vm_guest_power](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_vm_guest_power_module.rst)|Issues a request to the guest operating system asking it to perform a reboot. This request returns immediately and does not wait for the guest operating system to complete the operation.
[vmware.vmware_rest.vcenter_vm_guest_power_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_vm_guest_power_info_module.rst)|Returns information about the guest operating system power state.
[vmware.vmware_rest.vcenter_vm_guest_processes](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_vm_guest_processes_module.rst)|Terminates a process in the guest OS. <p> On Posix guests, the process is sent a TERM signal.  If that doesn't terminate the process, a KILL signal is sent.  A process may still be running if it's stuck. <p>
[vmware.vmware_rest.vcenter_vm_guest_processes_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_vm_guest_processes_info_module.rst)|Returns the status of a process running in the guest operating system, including those started by {@link Processes#create} that may have recently completed. <p>
[vmware.vmware_rest.vcenter_vm_hardware](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_vm_hardware_module.rst)|Upgrades the virtual machine to a newer virtual hardware version.
[vmware.vmware_rest.vcenter_vm_hardware_adapter_sata](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_vm_hardware_adapter_sata_module.rst)|Adds a virtual SATA adapter to the virtual machine.
[vmware.vmware_rest.vcenter_vm_hardware_adapter_sata_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_vm_hardware_adapter_sata_info_module.rst)|Returns information about a virtual SATA adapter.
[vmware.vmware_rest.vcenter_vm_hardware_adapter_scsi](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_vm_hardware_adapter_scsi_module.rst)|Updates the configuration of a virtual SCSI adapter.
[vmware.vmware_rest.vcenter_vm_hardware_adapter_scsi_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_vm_hardware_adapter_scsi_info_module.rst)|Returns information about a virtual SCSI adapter.
[vmware.vmware_rest.vcenter_vm_hardware_boot](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_vm_hardware_boot_module.rst)|Updates the boot-related settings of a virtual machine.
[vmware.vmware_rest.vcenter_vm_hardware_boot_device](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_vm_hardware_boot_device_module.rst)|Sets the virtual devices that will be used to boot the virtual machine.  The virtual machine will check the devices in order, attempting to boot from each, until the virtual machine boots successfully.  If the {@term list} is empty, the virtual machine will use a default boot sequence. There should be no more than one instance of {@link Entry} for a given device type except {@link Device.Type#ETHERNET} in the {@term list}.
[vmware.vmware_rest.vcenter_vm_hardware_boot_device_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_vm_hardware_boot_device_info_module.rst)|Returns an ordered list of boot devices for the virtual machine. If the {@term list} is empty, the virtual machine uses a default boot sequence.
[vmware.vmware_rest.vcenter_vm_hardware_boot_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_vm_hardware_boot_info_module.rst)|Returns the boot-related settings of a virtual machine.
[vmware.vmware_rest.vcenter_vm_hardware_cdrom](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_vm_hardware_cdrom_module.rst)|Adds a virtual CD-ROM device to the virtual machine.
[vmware.vmware_rest.vcenter_vm_hardware_cdrom_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_vm_hardware_cdrom_info_module.rst)|Returns information about a virtual CD-ROM device.
[vmware.vmware_rest.vcenter_vm_hardware_cpu](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_vm_hardware_cpu_module.rst)|Updates the CPU-related settings of a virtual machine.
[vmware.vmware_rest.vcenter_vm_hardware_cpu_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_vm_hardware_cpu_info_module.rst)|Returns the CPU-related settings of a virtual machine.
[vmware.vmware_rest.vcenter_vm_hardware_disk](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_vm_hardware_disk_module.rst)|Updates the configuration of a virtual disk.  An update {@term operation} can be used to detach the existing VMDK file and attach another VMDK file to the virtual machine.
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
[vmware.vmware_rest.vcenter_vm_power](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_vm_power_module.rst)|Powers off a powered-on or suspended virtual machine.
[vmware.vmware_rest.vcenter_vm_power_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_vm_power_info_module.rst)|Returns the power state information of a virtual machine.
[vmware.vmware_rest.vcenter_vm_storage_policy](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_vm_storage_policy_module.rst)|Updates the storage policy configuration of a virtual machine and/or its associated virtual hard disks.
[vmware.vmware_rest.vcenter_vm_storage_policy_compliance](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_vm_storage_policy_compliance_module.rst)|Returns the storage policy Compliance {@link Info} of a virtual machine after explicitly re-computing compliance check.
[vmware.vmware_rest.vcenter_vm_storage_policy_compliance_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_vm_storage_policy_compliance_info_module.rst)|Returns the cached storage policy compliance information of a virtual machine.
[vmware.vmware_rest.vcenter_vm_storage_policy_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_vm_storage_policy_info_module.rst)|Returns Information about Storage Policy associated with a virtual machine's home directory and/or its virtual hard disks.
[vmware.vmware_rest.vcenter_vm_tools](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_vm_tools_module.rst)|Begins the Tools upgrade process. To monitor the status of the Tools upgrade, clients should check the Tools status by calling {@link #get} and examining {@name Info#versionStatus} and {@name Info#runState}.
[vmware.vmware_rest.vcenter_vm_tools_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_vm_tools_info_module.rst)|Get the properties of VMware Tools.
[vmware.vmware_rest.vcenter_vm_tools_installer](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_vm_tools_installer_module.rst)|Connects the VMware Tools CD installer as a CD-ROM for the guest operating system. On Windows guest operating systems with autorun, this should cause the installer to initiate the Tools installation which will need user input to complete. On other (non-Windows) guest operating systems this will make the Tools installation available, and a a user will need to do guest-specific actions.  On Linux, this includes opening an archive and running the installer. To monitor the status of the Tools install, clients should check the {@name vcenter.vm.Tools.Info#versionStatus} and {@name vcenter.vm.Tools.Info#runState} from {@link vcenter.vm.Tools#get}
[vmware.vmware_rest.vcenter_vm_tools_installer_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_vm_tools_installer_info_module.rst)|Get information about the VMware Tools installer.

<!--end collection content-->

## Installation and Usage

### Install the dependencies

This collection depends on Python 3.6 or greater and [aiohttp](https://docs.aiohttp.org/en/stable/).

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

## Communication

We have a dedicated Working Group for VMware.
You can find other people interested in this in `#ansible-vmware` on Freenode IRC.
For more information about communities, meetings and agendas see https://github.com/ansible/community/wiki/VMware.

## License

GNU General Public License v3.0 or later

See [LICENSE](LICENSE) to see the full text.
