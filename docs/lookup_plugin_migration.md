# Lookup Plugin Migration

Starting with version 4.8.0, the lookup plugins `vmware.vmware_rest.*_moid` have been deprecated. They will not work with ansible-core 2.19 or above.

The recommended replacement is `vmware.vmware.moid_from_path`, which is available in vmware.vmware version 2.1 and above. This document will show how you can migrate to the new lookup plugins.

### Authentication

To make migration easier, the same authentication methods that worked for the vmware.vmware_rest plugins will work for the vmware.vmware plugins.

## Differences

Both plugins are capable of looking up an object's MoID, but they do so in fundamentally different ways. The vmware.vmware plugin extends the ansible-core library, while the vmware.vmware_rest plugins extend the cloud.common turbo plugin library. Here are the main differences:

### Output

The vmware.vmware_rest plugins will automatically convert multiple MoIDs to a list. This is inconsistent with the Ansible base plugin behavior, which requires that you specify `wantlist=True` to get a list back.
```
# This will return 'vm-1,vm-2,vm-3'
- name: Lookup many vms
  ansible.builtin.debug:
    msg: "{{ lookup('vmware.vmware.moid_from_path', '/my_dc/vms/') }}"

# This will return ['vm-1', 'vm-2', 'vm-3']
- name: Lookup many vms
  ansible.builtin.debug:
    msg: "{{ lookup('vmware.vmware.moid_from_path', '/my_dc/vms/', wantlist=true) }}"

# This will return 'vm-1'
- name: Lookup many vms
  ansible.builtin.debug:
    msg: "{{ lookup('vmware.vmware.moid_from_path', '/my_dc/vms/my-vm') }}"

# This will return ['vm-1']
- name: Lookup many vms
  ansible.builtin.debug:
    msg: "{{ lookup('vmware.vmware.moid_from_path', '/my_dc/vms/my-vm', wantlist=true) }}"
```

### Object types are inferred

There is only one lookup plugin for vmware.vmware. If you specify a path to a single object you do not need to specify the object type for vmware.vmware lookups. The plugin will return that MoID regardless of the object type. If the path ends in a slash, for example `/my-datacenter/vms/`, all objects found in that container will be returned. You can limit the type of object returned using an optional `type` parameter. For example:

```yaml
# This will return ESXi hosts or resource pools stored directly under the cluster 'foo'
- name: Lookup all 'host' objects in cluster 'foo'
  ansible.builtin.debug:
    msg: "{{ lookup('vmware.vmware.moid_from_path', '/my_dc/host/foo/') }}"

# This will return just ESXi hosts stored directly under the cluster 'foo'
- name: Lookup all 'host' objects in cluster 'foo'
  ansible.builtin.debug:
    msg: "{{ lookup('vmware.vmware.moid_from_path', '/my_dc/host/foo/', type='host') }}"

# This will return the cluster 'foo'
- name: Lookup all 'host' objects in cluster 'foo'
  ansible.builtin.debug:
    msg: "{{ lookup('vmware.vmware.moid_from_path', '/my_dc/host/foo') }}"
```

### Search paths must be valid inventory paths

The vmware.vmware_rest plugins worked by stepping through the provided "path" and using each part to create an additional filter for the final object search. This means that the provided search path did not need to be an actual vSphere inventory path. It also means that the plugin makes multiple API calls for every search.

For vmware.vmware, you must use a valid inventory path. For example:
```bash
# Datacenters are held at the root of the path. These are valid paths.
/my-dc
/my-dc/

# Everything else is held in one of four folders. These are valid paths.
/my-dc/host/
/my-dc/vm/
/my-dc/network/
/my-dc/datastore/

# These are not valid paths
/my-dc/my-cluster           # should be /my-dc/host/my-cluster
/my-dc/prod/my-datastore    # should be /my-dc/datastore/prod/my-datastore
```

There are a few ways to define VM pathing. VMs are not stored in clusters (directly). They are stored in resource pools, ESXi hosts, or folders.
```bash
/my-dc/vm/my-cluster                     # this is not a valid path.

/my-dc/vm/prod                           # this returns all VMs in folder prod
/my-dc/host/my-cluster/my-esxi/          # this returns all VMs on the ESXi host
/my-dc/host/my-cluster/Resources/        # this returns all VMs in the cluster's default resource pool
```
