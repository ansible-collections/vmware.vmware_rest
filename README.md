# Ansible Collection: vmware.vmware_rest

This repo hosts the `vmware.vmware_rest` Ansible Collection.

The **vmware.vmware_rest** collection is part of the **Red Hat Ansible Certified Content for VMware** offering that brings Ansible automation to VMware. This collection brings forward the possibility to manage vSphere resources and automate operator tasks.

This collection is generated using the VMware vSphere REST OpenAPI specifications. It does not rely on the VMware SDKs [`Pyvmomi`](https://github.com/vmware/pyvmomi) and [`vSphere Automation SDK for Python`](https://github.com/vmware/vsphere-automation-sdk-python), nor any python packages that do not come with `ansible-core`.

System programmers can enable pipelines to setup, tear down and deploy VMs while system administrators can automate time consuming repetitive tasks inevitably freeing up their time. New VMware users can find comfort in Ansible's familiarity and expedite their proficiency in record time.

### Known limitations

These modules are based on the [vSphere REST API](https://developer.broadcom.com/sdks/vcf-api-specification/latest/). This API provides partial functionality to the vSphere environment. Feature requests for functionality that is not directly tied to an API endpoint should be created in the [vmware.vmware](https://github.com/ansible-collections/vmware.vmware) collection.


## Requirements

There are no additional requirements for this collection, apart from those that already come with supported python installations.

## Compatibility

### vSphere

In previous versions of this collection, the major version of the collection was built to support a specific major version of vSphere.
Starting with version `5.0.0`, the collection will support multiple versions of vSphere when possible.

Module notes will dictate what versions of vSphere was used to generate the module, and what versions of vSphere should be compatible. If there is a known incompatibility or deprecation, that will also be listed in the module notes.

### Ansible version

This collection has been tested against following Ansible versions: **>=2.16.0**.


## Installation

Before using this collection, you need to install it with the Ansible Galaxy command-line tool:

```sh
ansible-galaxy collection install vmware.vmware_rest
```

You can also include it in a requirements.yml file and install it with `ansible-galaxy collection install -r requirements.yml`, using the format:

```sh
collections:
  - name: vmware.vmware_rest
```

Note that if you install the collection from Ansible Galaxy, it will not be upgraded automatically when you upgrade the Ansible package.
To upgrade the collection to the latest available version, run the following command:

```sh
ansible-galaxy collection install vmware.vmware_rest --upgrade
```

You can also install a specific version of the collection, for example, if you need to install a different version. Use the following syntax to install version 5.0.0:

```sh
ansible-galaxy collection install vmware.vmware_rest:5.0.0
```


## Use Cases

* Use Case Name: Modify vCenter Appliance Configuration
  * Actors:
    * System Admin
  * Description:
    * A systems administrator can modify the configuration of a running vCenter appliance.
  * Modules:
    * `vmware.vmware_rest.appliance_networking_interfaces_ipv4` - Sets the IPv4 network configuration for specific network interface
    * `vmware.vmware_rest.appliance_networking_interfaces_ipv6` - Sets the IPv6 network configuration for specific interface
    * `vmware.vmware_rest.appliance_vmon_service` - Lists the details of services managed by vMon

* Use Case Name: Manage a Content Library
  * Actors:
    * System Admin
  * Description:
    * The system administrator can create or manage a content library.
  * Modules:
    * `vmware.vmware_rest.content_configuration` - Updates the library configuration

* Use Case Name: Manage a VMs Settings
  * Actors:
    * System Admin
  * Description:
    * The system administrator can manage a VMs settings.
  * Modules:
    * `vmware.vmware_rest.vcenter_vm_guest_filesystem_directories` - Creates a directory in the guest operating system
    * `vmware.vmware_rest.vcenter_vm_hardware_boot_device` - Sets the virtual devices that will be used to boot the virtual machine
    * `vmware.vmware_rest.vcenter_vm_hardware_boot` - Updates the boot-related settings of a virtual machine
    * `vmware.vmware_rest.vcenter_vm_hardware_parallel` - Adds a virtual parallel port to the virtual machine
    * `vmware.vmware_rest.vcenter_vm_hardware` - Updates the virtual hardware settings of a virtual machine
    * `vmware.vmware_rest.vcenter_vm_hardware_serial` - Adds a virtual serial port to the virtual machine
    * `vmware.vmware_rest.vcenter_vm_storage_policy` - Updates the storage policy configuration of a virtual machine and/or its associated virtual hard disks
    * `vmware.vmware_rest.vcenter_vm_tools_installer` - Connects the VMware Tools CD installer as a CD-ROM for the guest operating system
    * `vmware.vmware_rest.vcenter_vm_tools` - Updates the properties of VMware Tools

## Testing

All releases will meet the following test criteria.

* 100% success for [Integration](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/tests/integration) tests.
* 100% success for [Unit](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/tests/unit) tests.
* 100% success for [Sanity](https://docs.ansible.com/ansible/latest/dev_guide/testing/sanity/index.html#all-sanity-tests) tests as part of [ansible-test](https://docs.ansible.com/ansible/latest/dev_guide/testing.html#run-sanity-tests).
* 100% success for [ansible-lint](https://ansible.readthedocs.io/projects/lint/) allowing only false positives.


## Contributing

This community is currently accepting contributions. We encourage you to open [git issues](https://github.com/ansible-collections/vmware.vmware_rest/issues) for bugs, comments or feature requests.
Please feel free to submit a PR to resolve the issue. Modules are generated so changes to them most likely will not be applied directly.

Refer to the [Ansible community guide](https://docs.ansible.com/ansible/devel/community/index.html).

### Development

This collection can be generated using AI and leveraging the skills/subagents in `.agents/`. Please refer to the [vmware module generation](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/development.md).


## Communication

* Join the Ansible forum:
  * [Get Help](https://forum.ansible.com/c/help/6): get help or help others.
  * [Posts tagged with 'vmware'](https://forum.ansible.com/tag/vmware): subscribe to participate in collection-related conversations.
  * [Ansible VMware Automation Working Group](https://forum.ansible.com/g/ansible-vmware): by joining the team you will automatically get subscribed to the posts tagged with ['vmware'](https://forum.ansible.com/tag/vmware).
  * [Social Spaces](https://forum.ansible.com/c/chat/4): gather and interact with fellow enthusiasts.
  * [News & Announcements](https://forum.ansible.com/c/news/5): track project-wide announcements including social events.

* The Ansible [Bullhorn newsletter](https://docs.ansible.com/ansible/devel/community/communication.html#the-bullhorn): used to announce releases and important changes.

For more information about communication, see the [Ansible communication guide](https://docs.ansible.com/ansible/devel/community/communication.html).


## Support

As Red Hat Ansible Certified Content, this collection is entitled to support through the Ansible Automation Platform (AAP) using the **Create issue** button on the top right corner.

If a support case cannot be opened with Red Hat and the collection has been obtained either from Galaxy or GitHub, there may community help available via:
- GitHub issues for bugs or feature requests: https://github.com/ansible-collections/vmware.vmware_rest/issues
- the [Ansible Forum](https://forum.ansible.com/) for general inqueries or workflow questions


## Release Notes and Roadmap

A list of available releases can be found on the github [release page](https://github.com/ansible-collections/vmware.vmware_rest/releases).
A changelog may be found attached to the release, or in the [CHANGELOG.rst](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/CHANGELOG.rst)

Note, some collections release before an ansible-core version reaches End of Life (EOL), thus the version of ansible-core that is supported must be a version that is currently supported.
For AAP users, to see the supported ansible-core versions, review the [AAP Life Cycle](https://access.redhat.com/support/policy/updates/ansible-automation-platform).
For Galaxy and GitHub users, to see the supported ansible-core versions, review the [ansible-core support matrix](https://docs.ansible.com/ansible/latest/reference_appendices/release_and_maintenance.html#ansible-core-support-matrix).


## Related Information

The `vmware.vmware` collection offers additional functionality. It is also a certified collection.
The `community.vmware` collection offers additional community supported functionality.

- [Ansible Collection overview](https://github.com/ansible-collections/overview)
- [Ansible User guide](https://docs.ansible.com/ansible/latest/user_guide/index.html)
- [Ansible Developer guide](https://docs.ansible.com/ansible/latest/dev_guide/index.html)

## License Information

GNU General Public License v3.0 or later
See [LICENSE](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/LICENSE) to see the full text.
