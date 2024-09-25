# VMWare Rest

# Development Guide

See [Ansible Using collections](https://docs.ansible.com/ansible/latest/user_guide/collections_using.html) for more details.

## How To: Generate Collection Modules

1. Get the OpenAPI spec from VCenter
    a. Clone https://github.com/vmware/vmware-openapi-generator
    b. Run `python vmsgen.py -vc 'your_vcenter_ip_or_hostname' -o gen_out --insecure --oas 2 --deprecate-slash-rest --fetch-authentication-metadata` from within the checked out repo
    c. validate the directory `gen_out` has the spec files. Note `--oas 2` generates version 2 spec files. Version 3 seems bugged https://github.com/vmware/vmware-openapi-generator/issues/73

2. Add/Replace the spec in this repo
    a. in `config/api_specifications` there are directories corresponding to VCenter versions. If the version you are generating a spec for does not exist, create it.
    b. Copy the files you generated in step 1 (`gen_out/*.json`) to the directory matching your VCenter version in `config/api_specifications`

3. Configure the content builder tool manifest
    a. Update the `config/MANIFEST.yml`. The `plugins.api_object_path` property should be whatever version of VCenter you generated the specs for
    b. **Note**: the property `plugins.module_version` should always be `1.0.0`
    c. For more information on the command and input arguments, please refer to the tool's [README](https://github.com/ansible-community/ansible.content_builder#resource-module-scaffolding-generated-using-openapi-based-json).

4. Install Extra Pip Requirements
    a. Run from the root of the repo: `pip install -r config/requirements.txt`
    b. These requirements are taken from the content builder tool repo

4. Run the content builder tool
    a. Install the tool, if needed: `ansible-galaxy collection install git+https://github.com/ansible-community/ansible.content_builder.git`
    b. Run the tool from the root of the repo: `ansible-playbook config/generate.yml`

5. Copy the new content to the repo
    a. Once the playbook finishes successfully, you can view the new content in `config/output`
    b. Copy the contents of `config/output` to the proper places in this repo
    c. The main things to copy will be `plugins`, `tests`, and `runtime`. The other generated files probably dont need to replace the existing files

#### (Optional) Update the `RETURN Block` of the vmware modules using the test-suite

The `generate.yml` playbook will copy the old blocks to the new modules. You can refresh the blocks if you introduce a new API version.

**Note** The steps below will run a playbook that stops all of the VMs in a vcenter. It will also potentially wipe out the examples and return values in each module, so please review changes carefully.

Create `/tmp/inventory-vmware_rest` like:
```
[vmware_rest]
localhost ansible_connection=local

[vmware_rest:vars]
vcenter_hostname=your_hostname
vcenter_username=your_admin
vcenter_password=your_pass
```

Run:
```
    mkdir -p ~/.ansible/collections/ansible_collections/goneri/utils
    git clone https://github.com/goneri/ansible-collection-goneri.utils.git ~/.ansible/collections/ansible_collections/goneri/utils
    cd ~/.ansible/collections/ansible_collections/vmware/vmware_rest/tests/integration/targets/vcenter_vm_scenario1
    ./refresh_RETURN_block.sh
    cd ~/.ansible/collections/ansible_collections/goneri/utils
    ./scripts/inject_RETURN.py ~/.ansible/collections/ansible_collections/vmware/vmware_rest/manual/source/vmware_rest_scenarios/task_outputs ~/.ansible/collections/ansible_collections/vmware/vmware_rest --config-file config/inject_RETURN.yaml
```

## More Details on Content Builder

To use the content builder tool, you need to provide a YAML file that contains all the information needed to generate a vmware module. You can find the necessary files, such as the [api specification](https://github.com/ansible-collections/vmware.vmware_rest/tree/main/config/api_specifications) and the [modules.yaml](https://github.com/ansible-collections/vmware.vmware_rest/tree/main/config/modules.yaml), in the repository. You can copy these files to your local path and customize them as per your requirements. After that, you must specify the path of these files in the input yaml file against the api_object_path and resource parameter. If you want to generate both examples and modules, set the action parameter to `generate_all`. If you only want to generate examples, use `action: generate_examples`, and for only modules, use `action: generate_modules`. For more information on the command and input arguments, please refer to the tool's [README](https://github.com/ansible-community/ansible.content_builder#resource-module-scaffolding-generated-using-openapi-based-json).

Once the modules are generated in the location mentioned in `collection:path`, you can follow the below steps to refresh the RETURN block in the module documentaion.
