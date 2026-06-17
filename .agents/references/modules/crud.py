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
    VmwareRestCrudModuleBase
)


## Be sure to review the VmwareRestModuleBase and VmwareRestCrudModuleBase classes in
## plugins/module_utils/_module_base.py for helper methods (fetch_list, build_updatable_payload,
## resolve_resource_id, delete_if_exists, update_if_changed, params_differ, payload_body_subset).
class VmwareRestCrudModule(VmwareRestCrudModuleBase):
    ## Define create body once; derive update body with payload_body_subset excluding create-only fields.
    ## _CREATE_BODY = {"name": "name", "parent": "parent", ...}
    ## PAYLOAD_FORMAT = {
    ##     "create": {"query": {}, "body": _CREATE_BODY, "path": {}},
    ##     "update": {"query": {}, "body": payload_body_subset(_CREATE_BODY, exclude=("parent",)), "path": {}},
    ##     ...
    ## }
    ## UPDATABLE_PARAMS = ("name", ...)  # must align with update body module_param keys
    PAYLOAD_FORMAT = {
        "create": {"query": {}, "body": {}, "path": {}},
        "update": {"query": {}, "body": {}, "path": {}},
        "delete": {"query": {}, "body": {}, "path": {}},
    }

    UPDATABLE_PARAMS = ()

    def ensure_present(self, path_template: str) -> dict:
        """
        One of two primary entry points for the module. This method should be called from the main method of the module when
        the user has specified that the resource should be present (state=present).
        The present state ensures a resource exists and matches the desired parameters provided by the user.
        If the resource does not exist, it should be created.
        If the resource exists and does not match one or more desired parameters, it should be updated to match the desired parameters.
        If the resource exists and matches the desired parameters, it should do nothing.

        The method should return the MOID of the managed resource. It should also return a list of changed parameters, if any.
        If no change was made, the method should return None.
        Here is the general pattern for the method:
        1. GET current state (404 means resource does not exist).
        2. If absent, POST to create.
        3. If present, compare current vs desired; PUT/PATCH only if different.
        4. Return changed=True only when the resource was actually modified.

        Although this method is the primary entry point for the module, you should be wary of making it too complex. Many modules
        may benefit for helper methods dedicated to specific tasks, like creating the resource, comparing current and desired states,
        and updating the resource.
        """
        path = self.build_path(path_template)
        desired = self.build_payload(self.PAYLOAD_FORMAT["update"])

        ## Client methods have built-in error handling, so we can just call them and let them handle the errors.
        response = self.client.get(path)
        if response.status == 404:
            return {"changed": False}
        current = response.json
        exists = True

        if not exists:

            create_path = self.build_path(path_template)
            create_body = self.build_payload(self.PAYLOAD_FORMAT["create"])
            create_query = self.build_query(self.PAYLOAD_FORMAT["create"])
            if not self.module.check_mode:
                response = self.client.post(create_path, data=create_body, query=create_query)
                result = response.json
            else:
                result = {}
            result["changed"] = True
            return result

        ## The module should be idempotent. This means that the comparison between the desired parameters and the current state must be done
        ## recursively, and only by comparing parameters that are explicitly specified by the user.
        ## For example, if the user specifies a desired name for the resource, but does not specify a desired description,
        ## the module should not consider the description when comparing the current state to the desired state.
        ## This is because the description is not explicitly specified by the user, and is therefore not a desired parameter.
        if current == desired:
            return {"changed": False, "value": current}

        update_body = self.build_payload(self.PAYLOAD_FORMAT["update"])
        update_query = self.build_query(self.PAYLOAD_FORMAT["update"])
        if not self.module.check_mode:
            response = self.client.put(path, data=update_body, query=update_query)
            result = response.json
        else:
            result = {}
        result["changed"] = True
        return result


    def ensure_absent(self, path_template: str) -> dict:
        ## Implement delete logic:
        ## 1. GET or attempt DELETE.
        ## 2. If resource does not exist (404), return changed=False.
        ## 3. Otherwise DELETE and return changed=True.
        path = self.build_path(path_template)

        ## Client methods have built-in error handling, so we can just call them and let them handle the errors.
        response = self.client.get(path)
        if response.status == 404:
          return {"changed": False}

        delete_body = self.build_payload(self.PAYLOAD_FORMAT["delete"])
        delete_query = self.build_query(self.PAYLOAD_FORMAT["delete"])
        ## If the module is in check mode, do not actually delete the resource.
        if not self.module.check_mode:
            self.client.delete(path, query=delete_query)
        return {"changed": True}


def main():
    ## The Ansible module spec is described in this documentation: https://docs.ansible.com/projects/ansible/latest/dev_guide/developing_program_flow_modules.html#argument-spec
    ## Use this section as a starting point for the module spec, and add to it as needed.
    ## CRUD modules must set supports_check_mode to True or False; see below.
    module_args = connection_params_argument_spec()
    module_args["state"] = {
        "type": "str",
        "choices": ["present", "absent"],
        "default": "present",
    }
    ## Add API-specific options to module_args here.
    ## For dict options, nest suboptions under the 'options' key in argument_spec.
    ## Example:
    ## module_args["cpu_allocation"] = {
    ##     "type": "dict",
    ##     "options": {
    ##         "reservation": {"type": "int"},
    ##         "shares": {
    ##             "type": "dict",
    ##             "options": {"level": {"type": "str", "choices": ["LOW", "NORMAL", "HIGH", "CUSTOM"]}},
    ##         },
    ##     },
    ## }

    ## CRUD modules must set supports_check_mode to True or False, depending on whether the module can be executed in a
    ## read-only manner. In check mode, the module should execute as much of the logic as possible, but should not make any
    ## changes to the system. Operations like PUT, PATCH, and DELETE should be skipped in check mode (with the exception
    ## being the authentication operations).
    ## Obviously, not all return values can be set when running in check mode. For example, you cannot return the MOID of
    ## a resource that was created, since the module did not actually create the resource. This is OK and expected. Return
    ## what values you can; nothing additional is needed or needs to be documented.
    ## See the module code above for an example of how to encorporate check mode into the module.
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
    )
    ## End of module spec section.

    crud_module = VmwareRestCrudModule(module)

    path_template = "<api uri path from spec with {param} placeholders, e.g. /vcenter/resource-pool/{resource_pool}; Client adds /api prefix>"
    if module.params["state"] == "present":
        result = crud_module.ensure_present(path_template)
    elif module.params["state"] == "absent":
        result = crud_module.ensure_absent(path_template)
    else:
        module.fail_json(msg="Unsupported state: {0}".format(module.params["state"]))

    module.exit_json(**result)

if __name__ == '__main__':
    main()
