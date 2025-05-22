# vmware.vmware_rest Turbo Mode

This collection is capable of leveraging a feature of the cloud.common collection called the "turbo server". This is basically a caching mechanism that speeds up repeated API calls. This collection has used turbo mode up until version 4.8.0. With the release of 4.8.0, turbo mode is disabled by default but can be re-enabled using an environment variable.

Read more about the turbo server in the cloud.common documentation [here](https://github.com/ansible-collections/cloud.common?tab=readme-ov-file#ansible-turbo-module).

## Enabling or Disabling

By default, the turbo server mode is disabled. You can explicitly enable or disable it using an environment variable.
If you are executing the playbook using localhost:
```bash
export VMWARE_ENABLE_TURBO="true"   # or 1, or True
ansible-playbook .....
```

You can also set it in the playbook `environment`:
```yaml
- name: Do something
  hosts: my_host
  environment:
    VMWARE_ENABLE_TURBO: true
  tasks:
    .....
```

## Pros and Cons

The turbo server works by creating a local cache of Ansible files on the remote Ansible host. It opens a socket on the host as a mechanism for modules to read and write from the cache. This enables the first module to load whatever librarys are required and setup API connections, store them in the cache, and allow other modules to reuse those resources. <b>It noticeably speeds up module execution time.</b>

Because data needs to be passed through the socket to read/write from the cache, <b>there are restrictions on the type of data that can be returned by modules.</b> Everything needs to be serializable, and not all python objects are by default.

The socket and server also add complexity and additional layers of obfuscation to the Ansible process. <b>Errors during module execution can be mangled or obscured</b> as data is passed through the turbo server socket. Errors will often become completely masked and give unhelpful messages to the user.

Finally, <b>the cache includes many pieces of the module execution process which can hinder execution on multiple resources</b>. For example, since the authentication to a vCenter will be cached, you cannot use one vCenter for a module call and then switch to a second vCenter immediately after. See issue [364](https://github.com/ansible-collections/vmware.vmware_rest/issues/364).
