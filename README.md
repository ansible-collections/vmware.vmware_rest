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
[vmware.vmware_rest.vcenter_cluster_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_cluster_info_module.rst)|Collect the information associated with the vCenter clusters
[vmware.vmware_rest.vcenter_datacenter](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_datacenter_module.rst)|Manage the datacenter of a vCenter
[vmware.vmware_rest.vcenter_datacenter_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_datacenter_info_module.rst)|Collect the information associated with the vCenter datacenters
[vmware.vmware_rest.vcenter_datastore_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_datastore_info_module.rst)|Collect the information associated with the vCenter datastores
[vmware.vmware_rest.vcenter_folder_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_folder_info_module.rst)|Collect the information associated with the vCenter folders
[vmware.vmware_rest.vcenter_host](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_host_module.rst)|Manage the host of a vCenter
[vmware.vmware_rest.vcenter_host_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_host_info_module.rst)|Collect the information associated with the vCenter hosts
[vmware.vmware_rest.vcenter_network_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_network_info_module.rst)|Collect the information associated with the vCenter networks
[vmware.vmware_rest.vcenter_resourcepool](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_resourcepool_module.rst)|Manage the resourcepool of a vCenter
[vmware.vmware_rest.vcenter_resourcepool_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_resourcepool_info_module.rst)|Collect the information associated with the vCenter resourcepools
[vmware.vmware_rest.vcenter_storage_policies_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_storage_policies_info_module.rst)|Collect the information associated with the vCenter storage policiess
[vmware.vmware_rest.vcenter_vm](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_vm_module.rst)|Manage the vm of a vCenter
[vmware.vmware_rest.vcenter_vm_guest_identity_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_vm_guest_identity_info_module.rst)|Collect the guest identity information
[vmware.vmware_rest.vcenter_vm_guest_localfilesystem_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_vm_guest_localfilesystem_info_module.rst)|Collect the guest localfilesystem information
[vmware.vmware_rest.vcenter_vm_guest_networking_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_vm_guest_networking_info_module.rst)|Collect the guest networking information
[vmware.vmware_rest.vcenter_vm_guest_networking_interfaces_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_vm_guest_networking_interfaces_info_module.rst)|Collect the guest networking interfaces information
[vmware.vmware_rest.vcenter_vm_guest_networking_routes_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_vm_guest_networking_routes_info_module.rst)|Collect the guest networking routes information
[vmware.vmware_rest.vcenter_vm_hardware](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_vm_hardware_module.rst)|Manage the hardware of a VM
[vmware.vmware_rest.vcenter_vm_hardware_adapter_sata](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_vm_hardware_adapter_sata_module.rst)|Manage the SATA adapter of a VM
[vmware.vmware_rest.vcenter_vm_hardware_adapter_sata_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_vm_hardware_adapter_sata_info_module.rst)|Collect the SATA adapter information from a VM
[vmware.vmware_rest.vcenter_vm_hardware_adapter_scsi](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_vm_hardware_adapter_scsi_module.rst)|Manage the SCSI adapter of a VM
[vmware.vmware_rest.vcenter_vm_hardware_adapter_scsi_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_vm_hardware_adapter_scsi_info_module.rst)|Collect the SCSI adapter information from a VM
[vmware.vmware_rest.vcenter_vm_hardware_boot](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_vm_hardware_boot_module.rst)|Manage the boot of a VM
[vmware.vmware_rest.vcenter_vm_hardware_boot_device](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_vm_hardware_boot_device_module.rst)|Manage the boot device of a VM
[vmware.vmware_rest.vcenter_vm_hardware_boot_device_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_vm_hardware_boot_device_info_module.rst)|Collect the boot device information from a VM
[vmware.vmware_rest.vcenter_vm_hardware_boot_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_vm_hardware_boot_info_module.rst)|Collect the boot information from a VM
[vmware.vmware_rest.vcenter_vm_hardware_cdrom](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_vm_hardware_cdrom_module.rst)|Manage the cdrom of a VM
[vmware.vmware_rest.vcenter_vm_hardware_cdrom_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_vm_hardware_cdrom_info_module.rst)|Collect the cdrom information from a VM
[vmware.vmware_rest.vcenter_vm_hardware_cpu](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_vm_hardware_cpu_module.rst)|Manage the cpu of a VM
[vmware.vmware_rest.vcenter_vm_hardware_cpu_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_vm_hardware_cpu_info_module.rst)|Collect the cpu information from a VM
[vmware.vmware_rest.vcenter_vm_hardware_disk](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_vm_hardware_disk_module.rst)|Manage the disk of a VM
[vmware.vmware_rest.vcenter_vm_hardware_disk_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_vm_hardware_disk_info_module.rst)|Collect the disk information from a VM
[vmware.vmware_rest.vcenter_vm_hardware_ethernet](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_vm_hardware_ethernet_module.rst)|Manage the ethernet of a VM
[vmware.vmware_rest.vcenter_vm_hardware_ethernet_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_vm_hardware_ethernet_info_module.rst)|Collect the ethernet information from a VM
[vmware.vmware_rest.vcenter_vm_hardware_floppy](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_vm_hardware_floppy_module.rst)|Manage the floppy of a VM
[vmware.vmware_rest.vcenter_vm_hardware_floppy_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_vm_hardware_floppy_info_module.rst)|Collect the floppy information from a VM
[vmware.vmware_rest.vcenter_vm_hardware_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_vm_hardware_info_module.rst)|Manage the info of a VM
[vmware.vmware_rest.vcenter_vm_hardware_memory](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_vm_hardware_memory_module.rst)|Manage the memory of a VM
[vmware.vmware_rest.vcenter_vm_hardware_memory_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_vm_hardware_memory_info_module.rst)|Collect the memory information from a VM
[vmware.vmware_rest.vcenter_vm_hardware_parallel](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_vm_hardware_parallel_module.rst)|Manage the parallel of a VM
[vmware.vmware_rest.vcenter_vm_hardware_parallel_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_vm_hardware_parallel_info_module.rst)|Collect the parallel information from a VM
[vmware.vmware_rest.vcenter_vm_hardware_serial](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_vm_hardware_serial_module.rst)|Manage the serial of a VM
[vmware.vmware_rest.vcenter_vm_hardware_serial_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_vm_hardware_serial_info_module.rst)|Collect the serial information from a VM
[vmware.vmware_rest.vcenter_vm_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_vm_info_module.rst)|Collect the  information from a VM
[vmware.vmware_rest.vcenter_vm_libraryitem_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_vm_libraryitem_info_module.rst)|Collect the libraryitem  information from a VM
[vmware.vmware_rest.vcenter_vm_power](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_vm_power_module.rst)|Manage the power of a VM
[vmware.vmware_rest.vcenter_vm_power_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_vm_power_info_module.rst)|Collect the power  information from a VM
[vmware.vmware_rest.vcenter_vm_storage_policy](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_vm_storage_policy_module.rst)|Manage the storage policy of a VM
[vmware.vmware_rest.vcenter_vm_storage_policy_compliance_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_vm_storage_policy_compliance_info_module.rst)|Collect the storage policy compliance  information from a VM
[vmware.vmware_rest.vcenter_vm_storage_policy_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_vm_storage_policy_info_module.rst)|Collect the storage policy  information from a VM
[vmware.vmware_rest.vcenter_vm_tools](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_vm_tools_module.rst)|Manage the tools of a VM
[vmware.vmware_rest.vcenter_vm_tools_info](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/docs/vmware.vmware_rest.vcenter_vm_tools_info_module.rst)|Collect the tools  information from a VM

<!--end collection content-->

## Installation and Usage

### Installing the Collection from Ansible Galaxy

Before using the VMware collection, you need to install the collection with the `ansible-galaxy` CLI:

    ansible-galaxy collection install vmware.vmware_rest

You can also include it in a `requirements.yml` file and install it via `ansible-galaxy collection install -r requirements.yml` using the format:

```yaml
collections:
- name: vmware.vmware_rest
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
