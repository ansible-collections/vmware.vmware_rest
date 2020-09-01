# Ansible Collection: community.vmware_rest

This repo hosts the `community.vmware_rest` Ansible Collection.

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
### Httpapi plugins
Name | Description
--- | ---

### Modules
Name | Description
--- | ---
[vmware.vmware_rest.vcenter_cluster_info](https://github.com/ansible-collections/vmware_rest.git/blob/main/docs/vmware.vmware_rest.vcenter_cluster_info_module.rst)|Handle resource of type vcenter_cluster
[vmware.vmware_rest.vcenter_datacenter](https://github.com/ansible-collections/vmware_rest.git/blob/main/docs/vmware.vmware_rest.vcenter_datacenter_module.rst)|Handle resource of type vcenter_datacenter
[vmware.vmware_rest.vcenter_datacenter_info](https://github.com/ansible-collections/vmware_rest.git/blob/main/docs/vmware.vmware_rest.vcenter_datacenter_info_module.rst)|Handle resource of type vcenter_datacenter
[vmware.vmware_rest.vcenter_datastore_info](https://github.com/ansible-collections/vmware_rest.git/blob/main/docs/vmware.vmware_rest.vcenter_datastore_info_module.rst)|Handle resource of type vcenter_datastore
[vmware.vmware_rest.vcenter_folder_info](https://github.com/ansible-collections/vmware_rest.git/blob/main/docs/vmware.vmware_rest.vcenter_folder_info_module.rst)|Handle resource of type vcenter_folder
[vmware.vmware_rest.vcenter_host](https://github.com/ansible-collections/vmware_rest.git/blob/main/docs/vmware.vmware_rest.vcenter_host_module.rst)|Handle resource of type vcenter_host
[vmware.vmware_rest.vcenter_host_info](https://github.com/ansible-collections/vmware_rest.git/blob/main/docs/vmware.vmware_rest.vcenter_host_info_module.rst)|Handle resource of type vcenter_host
[vmware.vmware_rest.vcenter_network_info](https://github.com/ansible-collections/vmware_rest.git/blob/main/docs/vmware.vmware_rest.vcenter_network_info_module.rst)|Handle resource of type vcenter_network
[vmware.vmware_rest.vcenter_vm](https://github.com/ansible-collections/vmware_rest.git/blob/main/docs/vmware.vmware_rest.vcenter_vm_module.rst)|Handle resource of type vcenter_vm
[vmware.vmware_rest.vcenter_vm_compute_policies_info](https://github.com/ansible-collections/vmware_rest.git/blob/main/docs/vmware.vmware_rest.vcenter_vm_compute_policies_info_module.rst)|Handle resource of type vcenter_vm_compute_policies
[vmware.vmware_rest.vcenter_vm_console_tickets](https://github.com/ansible-collections/vmware_rest.git/blob/main/docs/vmware.vmware_rest.vcenter_vm_console_tickets_module.rst)|Handle resource of type vcenter_vm_console_tickets
[vmware.vmware_rest.vcenter_vm_guest_customization](https://github.com/ansible-collections/vmware_rest.git/blob/main/docs/vmware.vmware_rest.vcenter_vm_guest_customization_module.rst)|Handle resource of type vcenter_vm_guest_customization
[vmware.vmware_rest.vcenter_vm_guest_identity_info](https://github.com/ansible-collections/vmware_rest.git/blob/main/docs/vmware.vmware_rest.vcenter_vm_guest_identity_info_module.rst)|Handle resource of type vcenter_vm_guest_identity
[vmware.vmware_rest.vcenter_vm_guest_localfilesystem_info](https://github.com/ansible-collections/vmware_rest.git/blob/main/docs/vmware.vmware_rest.vcenter_vm_guest_localfilesystem_info_module.rst)|Handle resource of type vcenter_vm_guest_localfilesystem
[vmware.vmware_rest.vcenter_vm_guest_networking_info](https://github.com/ansible-collections/vmware_rest.git/blob/main/docs/vmware.vmware_rest.vcenter_vm_guest_networking_info_module.rst)|Handle resource of type vcenter_vm_guest_networking
[vmware.vmware_rest.vcenter_vm_guest_networking_interfaces_info](https://github.com/ansible-collections/vmware_rest.git/blob/main/docs/vmware.vmware_rest.vcenter_vm_guest_networking_interfaces_info_module.rst)|Handle resource of type vcenter_vm_guest_networking_interfaces
[vmware.vmware_rest.vcenter_vm_guest_networking_routes_info](https://github.com/ansible-collections/vmware_rest.git/blob/main/docs/vmware.vmware_rest.vcenter_vm_guest_networking_routes_info_module.rst)|Handle resource of type vcenter_vm_guest_networking_routes
[vmware.vmware_rest.vcenter_vm_guest_power](https://github.com/ansible-collections/vmware_rest.git/blob/main/docs/vmware.vmware_rest.vcenter_vm_guest_power_module.rst)|Handle resource of type vcenter_vm_guest_power
[vmware.vmware_rest.vcenter_vm_guest_power_info](https://github.com/ansible-collections/vmware_rest.git/blob/main/docs/vmware.vmware_rest.vcenter_vm_guest_power_info_module.rst)|Handle resource of type vcenter_vm_guest_power
[vmware.vmware_rest.vcenter_vm_hardware](https://github.com/ansible-collections/vmware_rest.git/blob/main/docs/vmware.vmware_rest.vcenter_vm_hardware_module.rst)|Handle resource of type vcenter_vm_hardware
[vmware.vmware_rest.vcenter_vm_hardware_action_upgrade](https://github.com/ansible-collections/vmware_rest.git/blob/main/docs/vmware.vmware_rest.vcenter_vm_hardware_action_upgrade_module.rst)|Handle resource of type vcenter_vm_hardware_action_upgrade
[vmware.vmware_rest.vcenter_vm_hardware_adapter_sata](https://github.com/ansible-collections/vmware_rest.git/blob/main/docs/vmware.vmware_rest.vcenter_vm_hardware_adapter_sata_module.rst)|Handle resource of type vcenter_vm_hardware_adapter_sata
[vmware.vmware_rest.vcenter_vm_hardware_adapter_sata_info](https://github.com/ansible-collections/vmware_rest.git/blob/main/docs/vmware.vmware_rest.vcenter_vm_hardware_adapter_sata_info_module.rst)|Handle resource of type vcenter_vm_hardware_adapter_sata
[vmware.vmware_rest.vcenter_vm_hardware_adapter_scsi](https://github.com/ansible-collections/vmware_rest.git/blob/main/docs/vmware.vmware_rest.vcenter_vm_hardware_adapter_scsi_module.rst)|Handle resource of type vcenter_vm_hardware_adapter_scsi
[vmware.vmware_rest.vcenter_vm_hardware_adapter_scsi_info](https://github.com/ansible-collections/vmware_rest.git/blob/main/docs/vmware.vmware_rest.vcenter_vm_hardware_adapter_scsi_info_module.rst)|Handle resource of type vcenter_vm_hardware_adapter_scsi
[vmware.vmware_rest.vcenter_vm_hardware_boot](https://github.com/ansible-collections/vmware_rest.git/blob/main/docs/vmware.vmware_rest.vcenter_vm_hardware_boot_module.rst)|Handle resource of type vcenter_vm_hardware_boot
[vmware.vmware_rest.vcenter_vm_hardware_boot_device](https://github.com/ansible-collections/vmware_rest.git/blob/main/docs/vmware.vmware_rest.vcenter_vm_hardware_boot_device_module.rst)|Handle resource of type vcenter_vm_hardware_boot_device
[vmware.vmware_rest.vcenter_vm_hardware_boot_device_info](https://github.com/ansible-collections/vmware_rest.git/blob/main/docs/vmware.vmware_rest.vcenter_vm_hardware_boot_device_info_module.rst)|Handle resource of type vcenter_vm_hardware_boot_device
[vmware.vmware_rest.vcenter_vm_hardware_boot_info](https://github.com/ansible-collections/vmware_rest.git/blob/main/docs/vmware.vmware_rest.vcenter_vm_hardware_boot_info_module.rst)|Handle resource of type vcenter_vm_hardware_boot
[vmware.vmware_rest.vcenter_vm_hardware_cdrom](https://github.com/ansible-collections/vmware_rest.git/blob/main/docs/vmware.vmware_rest.vcenter_vm_hardware_cdrom_module.rst)|Handle resource of type vcenter_vm_hardware_cdrom
[vmware.vmware_rest.vcenter_vm_hardware_cdrom_connect](https://github.com/ansible-collections/vmware_rest.git/blob/main/docs/vmware.vmware_rest.vcenter_vm_hardware_cdrom_connect_module.rst)|Handle resource of type vcenter_vm_hardware_cdrom_connect
[vmware.vmware_rest.vcenter_vm_hardware_cdrom_disconnect](https://github.com/ansible-collections/vmware_rest.git/blob/main/docs/vmware.vmware_rest.vcenter_vm_hardware_cdrom_disconnect_module.rst)|Handle resource of type vcenter_vm_hardware_cdrom_disconnect
[vmware.vmware_rest.vcenter_vm_hardware_cdrom_info](https://github.com/ansible-collections/vmware_rest.git/blob/main/docs/vmware.vmware_rest.vcenter_vm_hardware_cdrom_info_module.rst)|Handle resource of type vcenter_vm_hardware_cdrom
[vmware.vmware_rest.vcenter_vm_hardware_cpu](https://github.com/ansible-collections/vmware_rest.git/blob/main/docs/vmware.vmware_rest.vcenter_vm_hardware_cpu_module.rst)|Handle resource of type vcenter_vm_hardware_cpu
[vmware.vmware_rest.vcenter_vm_hardware_cpu_info](https://github.com/ansible-collections/vmware_rest.git/blob/main/docs/vmware.vmware_rest.vcenter_vm_hardware_cpu_info_module.rst)|Handle resource of type vcenter_vm_hardware_cpu
[vmware.vmware_rest.vcenter_vm_hardware_disk](https://github.com/ansible-collections/vmware_rest.git/blob/main/docs/vmware.vmware_rest.vcenter_vm_hardware_disk_module.rst)|Handle resource of type vcenter_vm_hardware_disk
[vmware.vmware_rest.vcenter_vm_hardware_disk_info](https://github.com/ansible-collections/vmware_rest.git/blob/main/docs/vmware.vmware_rest.vcenter_vm_hardware_disk_info_module.rst)|Handle resource of type vcenter_vm_hardware_disk
[vmware.vmware_rest.vcenter_vm_hardware_ethernet](https://github.com/ansible-collections/vmware_rest.git/blob/main/docs/vmware.vmware_rest.vcenter_vm_hardware_ethernet_module.rst)|Handle resource of type vcenter_vm_hardware_ethernet
[vmware.vmware_rest.vcenter_vm_hardware_ethernet_connect](https://github.com/ansible-collections/vmware_rest.git/blob/main/docs/vmware.vmware_rest.vcenter_vm_hardware_ethernet_connect_module.rst)|Handle resource of type vcenter_vm_hardware_ethernet_connect
[vmware.vmware_rest.vcenter_vm_hardware_ethernet_disconnect](https://github.com/ansible-collections/vmware_rest.git/blob/main/docs/vmware.vmware_rest.vcenter_vm_hardware_ethernet_disconnect_module.rst)|Handle resource of type vcenter_vm_hardware_ethernet_disconnect
[vmware.vmware_rest.vcenter_vm_hardware_ethernet_info](https://github.com/ansible-collections/vmware_rest.git/blob/main/docs/vmware.vmware_rest.vcenter_vm_hardware_ethernet_info_module.rst)|Handle resource of type vcenter_vm_hardware_ethernet
[vmware.vmware_rest.vcenter_vm_hardware_floppy](https://github.com/ansible-collections/vmware_rest.git/blob/main/docs/vmware.vmware_rest.vcenter_vm_hardware_floppy_module.rst)|Handle resource of type vcenter_vm_hardware_floppy
[vmware.vmware_rest.vcenter_vm_hardware_floppy_connect](https://github.com/ansible-collections/vmware_rest.git/blob/main/docs/vmware.vmware_rest.vcenter_vm_hardware_floppy_connect_module.rst)|Handle resource of type vcenter_vm_hardware_floppy_connect
[vmware.vmware_rest.vcenter_vm_hardware_floppy_disconnect](https://github.com/ansible-collections/vmware_rest.git/blob/main/docs/vmware.vmware_rest.vcenter_vm_hardware_floppy_disconnect_module.rst)|Handle resource of type vcenter_vm_hardware_floppy_disconnect
[vmware.vmware_rest.vcenter_vm_hardware_floppy_info](https://github.com/ansible-collections/vmware_rest.git/blob/main/docs/vmware.vmware_rest.vcenter_vm_hardware_floppy_info_module.rst)|Handle resource of type vcenter_vm_hardware_floppy
[vmware.vmware_rest.vcenter_vm_hardware_info](https://github.com/ansible-collections/vmware_rest.git/blob/main/docs/vmware.vmware_rest.vcenter_vm_hardware_info_module.rst)|Handle resource of type vcenter_vm_hardware
[vmware.vmware_rest.vcenter_vm_hardware_memory](https://github.com/ansible-collections/vmware_rest.git/blob/main/docs/vmware.vmware_rest.vcenter_vm_hardware_memory_module.rst)|Handle resource of type vcenter_vm_hardware_memory
[vmware.vmware_rest.vcenter_vm_hardware_memory_info](https://github.com/ansible-collections/vmware_rest.git/blob/main/docs/vmware.vmware_rest.vcenter_vm_hardware_memory_info_module.rst)|Handle resource of type vcenter_vm_hardware_memory
[vmware.vmware_rest.vcenter_vm_hardware_parallel](https://github.com/ansible-collections/vmware_rest.git/blob/main/docs/vmware.vmware_rest.vcenter_vm_hardware_parallel_module.rst)|Handle resource of type vcenter_vm_hardware_parallel
[vmware.vmware_rest.vcenter_vm_hardware_parallel_connect](https://github.com/ansible-collections/vmware_rest.git/blob/main/docs/vmware.vmware_rest.vcenter_vm_hardware_parallel_connect_module.rst)|Handle resource of type vcenter_vm_hardware_parallel_connect
[vmware.vmware_rest.vcenter_vm_hardware_parallel_disconnect](https://github.com/ansible-collections/vmware_rest.git/blob/main/docs/vmware.vmware_rest.vcenter_vm_hardware_parallel_disconnect_module.rst)|Handle resource of type vcenter_vm_hardware_parallel_disconnect
[vmware.vmware_rest.vcenter_vm_hardware_parallel_info](https://github.com/ansible-collections/vmware_rest.git/blob/main/docs/vmware.vmware_rest.vcenter_vm_hardware_parallel_info_module.rst)|Handle resource of type vcenter_vm_hardware_parallel
[vmware.vmware_rest.vcenter_vm_hardware_serial](https://github.com/ansible-collections/vmware_rest.git/blob/main/docs/vmware.vmware_rest.vcenter_vm_hardware_serial_module.rst)|Handle resource of type vcenter_vm_hardware_serial
[vmware.vmware_rest.vcenter_vm_hardware_serial_connect](https://github.com/ansible-collections/vmware_rest.git/blob/main/docs/vmware.vmware_rest.vcenter_vm_hardware_serial_connect_module.rst)|Handle resource of type vcenter_vm_hardware_serial_connect
[vmware.vmware_rest.vcenter_vm_hardware_serial_disconnect](https://github.com/ansible-collections/vmware_rest.git/blob/main/docs/vmware.vmware_rest.vcenter_vm_hardware_serial_disconnect_module.rst)|Handle resource of type vcenter_vm_hardware_serial_disconnect
[vmware.vmware_rest.vcenter_vm_hardware_serial_info](https://github.com/ansible-collections/vmware_rest.git/blob/main/docs/vmware.vmware_rest.vcenter_vm_hardware_serial_info_module.rst)|Handle resource of type vcenter_vm_hardware_serial
[vmware.vmware_rest.vcenter_vm_info](https://github.com/ansible-collections/vmware_rest.git/blob/main/docs/vmware.vmware_rest.vcenter_vm_info_module.rst)|Handle resource of type vcenter_vm
[vmware.vmware_rest.vcenter_vm_libraryitem_info](https://github.com/ansible-collections/vmware_rest.git/blob/main/docs/vmware.vmware_rest.vcenter_vm_libraryitem_info_module.rst)|Handle resource of type vcenter_vm_libraryitem
[vmware.vmware_rest.vcenter_vm_power](https://github.com/ansible-collections/vmware_rest.git/blob/main/docs/vmware.vmware_rest.vcenter_vm_power_module.rst)|Handle resource of type vcenter_vm_power
[vmware.vmware_rest.vcenter_vm_power_info](https://github.com/ansible-collections/vmware_rest.git/blob/main/docs/vmware.vmware_rest.vcenter_vm_power_info_module.rst)|Handle resource of type vcenter_vm_power
[vmware.vmware_rest.vcenter_vm_storage_policy](https://github.com/ansible-collections/vmware_rest.git/blob/main/docs/vmware.vmware_rest.vcenter_vm_storage_policy_module.rst)|Handle resource of type vcenter_vm_storage_policy
[vmware.vmware_rest.vcenter_vm_storage_policy_compliance](https://github.com/ansible-collections/vmware_rest.git/blob/main/docs/vmware.vmware_rest.vcenter_vm_storage_policy_compliance_module.rst)|Handle resource of type vcenter_vm_storage_policy_compliance
[vmware.vmware_rest.vcenter_vm_storage_policy_compliance_info](https://github.com/ansible-collections/vmware_rest.git/blob/main/docs/vmware.vmware_rest.vcenter_vm_storage_policy_compliance_info_module.rst)|Handle resource of type vcenter_vm_storage_policy_compliance
[vmware.vmware_rest.vcenter_vm_storage_policy_info](https://github.com/ansible-collections/vmware_rest.git/blob/main/docs/vmware.vmware_rest.vcenter_vm_storage_policy_info_module.rst)|Handle resource of type vcenter_vm_storage_policy
[vmware.vmware_rest.vcenter_vm_tools](https://github.com/ansible-collections/vmware_rest.git/blob/main/docs/vmware.vmware_rest.vcenter_vm_tools_module.rst)|Handle resource of type vcenter_vm_tools
[vmware.vmware_rest.vcenter_vm_tools_info](https://github.com/ansible-collections/vmware_rest.git/blob/main/docs/vmware.vmware_rest.vcenter_vm_tools_info_module.rst)|Handle resource of type vcenter_vm_tools
[vmware.vmware_rest.vcenter_vm_tools_installer](https://github.com/ansible-collections/vmware_rest.git/blob/main/docs/vmware.vmware_rest.vcenter_vm_tools_installer_module.rst)|Handle resource of type vcenter_vm_tools_installer
[vmware.vmware_rest.vcenter_vm_tools_installer_info](https://github.com/ansible-collections/vmware_rest.git/blob/main/docs/vmware.vmware_rest.vcenter_vm_tools_installer_info_module.rst)|Handle resource of type vcenter_vm_tools_installer

<!--end collection content-->

## Installation and Usage

### Installing the Collection from Ansible Galaxy

Before using the VMware community collection, you need to install the collection with the `ansible-galaxy` CLI:

    ansible-galaxy collection install community.vmware_rest

You can also include it in a `requirements.yml` file and install it via `ansible-galaxy collection install -r requirements.yml` using the format:

```yaml
collections:
- name: community.vmware_rest
```

Please note this collection depends on Python 3.6 or greater.

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
