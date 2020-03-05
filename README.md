# Ansible Collection: community.vmware_rest

This repo hosts the `community.vmware_rest` Ansible Collection.

The collection includes the VMware modules and plugins supported by Ansible VMware community to help the management of VMware infrastructure. These modules are different from `community.vmware` since they are based upon VMware vSphere REST API interface and not relying on any third party libraries such as [`Pyvmomi`](https://github.com/vmware/pyvmomi) and [`vSphere Automation SDK for Python`](https://github.com/vmware/vsphere-automation-sdk-python).


## Installation and Usage

### Installing the Collection from Ansible Galaxy

Before using the VMware community collection, you need to install the collection with the `ansible-galaxy` CLI:

    ansible-galaxy collection install community.vmware_rest

You can also include it in a `requirements.yml` file and install it via `ansible-galaxy collection install -r requirements.yml` using the format:

```yaml
collections:
- name: community.vmware_rest
```

## Testing and Development

If you want to develop new content for this collection or improve what is already here, the easiest way to work on the collection is to clone it into one of the configured [`COLLECTIONS_PATHS`](https://docs.ansible.com/ansible/latest/reference_appendices/config.html#collections-paths), and work on it there.

- [Guidelines for VMware module development](https://docs.ansible.com/ansible/latest/dev_guide/platforms/vmware_guidelines.html)

### Testing with `ansible-test`

TBD

## Publishing New Version

TBD

## More Information

TBD

## Communication

We have a dedicated Working Group for VMware.
You can find other people interested in this in `#ansible-vmware` on Freenode IRC.
For more information about communities, meetings and agendas see https://github.com/ansible/community/wiki/VMware.

## License

GNU General Public License v3.0 or later

See [LICENSE](LICENSE) to see the full text.
