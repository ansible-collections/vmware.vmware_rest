# VMWare Rest

# Development Guide

See [Ansible Using collections](https://docs.ansible.com/ansible/latest/user_guide/collections_using.html) for more details.

## How To: Generate Collection Modules

Modules in this collection are generated using a script and a vSphere REST API spec. It is possible to regenerate modules without replacing the documentation. This is recommended unless you have access to an AI agent.

If you do have access to an agent, you can use the ansible-module-doc-review skill to help complete the documentation for the module from a raw generated state.

Refer to `content_generation/README.md` for more details.

### API Spec

There is a skill to help get the API spec from Broadcom. You can run `content_generation/fetch_vsphere_openapi_spec.py`.
