# VMWare Rest

# Development Guide

See [Ansible Using collections](https://docs.ansible.com/ansible/latest/user_guide/collections_using.html) for more details.

## How To: Generate Collection Modules

Modules in this collection are generated using an AI agent, and a vSphere REST API spec.

The process is designed to be API spec driven, self-iterative, and include testing and validation. You can generate one or multiple modules.

For performance purposes, its best to be sure your AI agent loads the projects subagents. For example, for claude you can do,
```
mkdir -p .claude/agents/;
cp -R .agents/subagents/* .claude/agents/
```

An example prompt would be:
```
using the module generation workflow and vsphere 9 api spec, generate vcenter_resourcepool and vcenter_resourcepool_info.
```

### API Spec

There is an AI skill dedicated to getting the API spec from Broadcom. It basically just runs a python script `.agents/scripts/fetch_vsphere_openapi_spec.py`, so you can do this manually if needed.

The module generation workflow will automatically get the API spec requested, if it does not exist.
