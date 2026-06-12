## Insert the module header (.agents/references/modules/header.py) here.
## Note to AI: If a comment starts with two hashes (##), it is a note to the AI, not to be included in the final file.
## Values in angle brackets (<>) are placeholders for values that will be replaced by the AI.
## Otherwise, values should be considered examples or descriptions of the actual values. The AI should read the value, and use
## it as a reference, not as a literal value (unless otherwise specified).


## These imports are definitely needed. You may need additional imports from the _module_base.py file.
## Check it for helper methods and other useful imports.
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.vmware.vmware_rest.plugins.module_utils._argument_spec import (
    connection_params_argument_spec
)
from ansible_collections.vmware.vmware_rest.plugins.module_utils._module_base import (
    VmwareRestInfoModuleBase
)


## Use fetch_list() from VmwareRestModuleBase for collection GET + normalize_list_response.
class VmwareRestInfoModule(VmwareRestInfoModuleBase):
    ## This structure describes the format of the payload expected by the end-points
    PAYLOAD_FORMAT = {
        "get": {"query": {}, "body": {}, "path": {}}
    }

    def get_info(self):
        """
        Primary entry point for the module. This method should be called from the main method of the module.

        The method should reutrn information about the resource to the user. This is typically detailed information about the resource(s) being queried.
        If the resource is not found, it should not raise and error, but should return an empty list or dictionary.

        A common pattern would be to:
        1. Get resource MOID(s) first, based on the filters provided by the user (LIST)
        2. Use the MOID(s) to get detailed information about the resource(s) (GET)
        3. Return the detailed information about the resource(s). Include the MOID in the result for each resource, if possible.
        """
        result = []
        searched_resource_ids_response = self.client.get(
          method="GET",
          path="<api uri path from spec, e.g. /vcenter/resource-pool; Client adds /api prefix>",
          ## The options below should be filled in with the appropriate values. They are all optional.
          ## They query and data specs come from the vSphere API specification, and the values should come from the module parameters.
          query=None, ## This should be a dictionary of the query parameters for the API call.
          data=None, ## This should be a dictionary of the data to be sent to the API call.
          headers=None, ## This should be a dictionary of the headers to be sent to the API call.
          bytes=None, ## This should be the bytes to be sent to the API call. If not None, the data parameter will be ignored.
        )
        if searched_resource_ids_response.status == 404:
          return result

        for resource_id in searched_resource_ids_response.json["value"]:
          resource_info = self.client.get(
              method="GET",
              path="<api uri path from spec, e.g. /vcenter/resource-pool/{resource_id}; Client adds /api prefix>",
              query=None,
              data=None,
              headers=None,
              bytes=None,
          )
          resource_json = resource_info.json
          if 'info' not in resource_json:
            resource_json['id'] = resource_id

          result.append(resource_json)
        return result


def main():
    ## The Ansible moudle spec is described in this documentation: https://docs.ansible.com/projects/ansible/latest/dev_guide/developing_program_flow_modules.html#argument-spec
    ## Use this section as a starting point for the module spec, and add to it as needed.
    module_args = connection_params_argument_spec()
    ## Add API-specific options to module_args here.
    ## For dict options, nest suboptions under the 'options' key in argument_spec
    ## and document them with 'suboptions' in DOCUMENTATION.
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    info_module = VmwareRestInfoModule(module)
    result = info_module.get_info()
    module.exit_json(**result)


if __name__ == '__main__':
    main()
