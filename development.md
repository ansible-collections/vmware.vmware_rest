# VMWare
  
# Development Guide
## Installation

Install the ansible.content_builder tool.
```
pip install black==22.3.0 jsonschema jinja2==3.0.3 ansible-core
ansible-galaxy collection install git+https://github.com/ansible-community/ansible.content_builder.git
```

You can also include it in a `requirements.yml` file and install it via `ansible-galaxy collection install -r requirements.yml` using the format:

```
collections:
- name: ansible.content_builder
```

See [Ansible Using collections](https://docs.ansible.com/ansible/latest/user_guide/collections_using.html) for more details.

## Using the Content Builder tool to generate vmware modules:

To use the content builder tool, you need to provide a YAML file that contains all the information needed to generate a vmware module. You can find the necessary files, such as the [api specification](https://github.com/ansible-collections/vmware.vmware_rest/tree/main/config/api_specifications) and the [modules.yaml](https://github.com/ansible-collections/vmware.vmware_rest/tree/main/config/modules.yaml), in the repository. You can copy these files to your local path and customize them as per your requirements. After that, you must specify the path of these files in the input yaml file against the api_object_path and resource parameter. If you want to generate both examples and modules, set the action parameter to `generate_all`. If you only want to generate examples, use `action: generate_examples`, and for only modules, use `action: generate_modules`. For more information on the command and input arguments, please refer to the tool's [README](https://github.com/ansible-community/ansible.content_builder#resource-module-scaffolding-generated-using-openapi-based-json). To generate the vmware modules using the content_builder tool, you can use the following command:

```
ansible-playbook build.yaml -e manifest_file=MANIFEST.yaml
```

The build.yaml file should contain the following code:

```yaml
---
- hosts: localhost
  gather_facts: yes
  roles:
    - ansible.content_builder.run
```

And the MANIFEST.yaml file should contain the following code:

```yaml
---
collection:
  path: /collections/ansible_collections/vmware/vmware_rest
  namespace: vmware
  name: vmware_rest
plugins:
  - type: module_openapi
    name: "vmware_rest"
    content: cloud
    api_object_path: api_specifications/7.0.2
    resource: config
    action: generate_all
    unique_key: ""
    rm_swagger_json: ""
    module_version: "1.0.0"
    author: "Ansible Cloud Team"
```

Once the modules are generated in the location mentioned in `collection:path`, you can follow the below steps to refresh the RETURN block in the module documentaion.

**_Refresh the `RETURN Block` of the vmware modules using the test-suite:_**

Set the env variables mentioned in [tox.ini](https://github.com/ansible-collections/vmware.vmware_rest/blob/main/tox.ini#L47).
```
    mkdir -p ~/.ansible/collections/ansible_collections/goneri/utils
    git clone https://github.com/goneri/ansible-collection-goneri.utils.git ~/.ansible/collections/ansible_collections/goneri/utils
    cd ~/.ansible/collections/ansible_collections/vmware/vmware_rest/tests/integration/targets/vcenter_vm_scenario1
    ./refresh_RETURN_block.sh
    cd ~/.ansible/collections/ansible_collections/goneri/utils
    ./scripts/inject_RETURN.py ~/.ansible/collections/ansible_collections/vmware/vmware_rest/manual/source/vmware_rest_scenarios/task_outputs ~/.ansible/collections/ansible_collections/vmware/vmware_rest --config-file config/inject_RETURN.yaml
```
