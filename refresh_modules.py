#!/usr/bin/env python

import argparse
import ast
import json
import re
import yaml
import pathlib

from pprint import pprint


MODULE_TEMPLATE = """
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = ""

ANSIBLE_METADATA = {
    "metadata_version": "1.1",
    "status": ["preview"],
    "supported_by": "community",
}

IN_QUERY_PARAMETER = None

import ansible_collections.ansible.vmware_rest.plugins.module_utils.vmware_httpapi as vmware_httpapi

def gen_args(module):
    args = ""
    for i in IN_QUERY_PARAMETER:
        v = module.params.get(i)
        if not v:
            continue
        if not args:
            args = "?"
        else:
            args += "&"
        if isinstance(v, list):
            for j in v:
                args += i + "=" + j
        elif isinstance(v, bool) and v:
            args += i + "=true"
        else:
            args += i + "=" + v
    return args

def url(module):
    pass

def prepare_argument_spec():
    argument_spec = vmware_httpapi.VmwareRestModule.create_argument_spec()
    return argument_spec


def main():
    pass



if __name__ == "__main__":
    main()
"""


class Resource:
    def __init__(self, name):
        self.name = name
        self.operations = {}

    @staticmethod
    def path_to_name(path):
        def is_element(i):
            if i and not "{" in i:
                return True
            else:
                return False

        _path = path.path.split("?")[0]

        elements = [i for i in _path.split("/") if is_element(i)]
        if elements[0:3] == ["rest", "com", "vmware"]:
            elements = elements[3:]
        elif elements[0:2] == ["rest", "hvc"]:
            elements = elements[1:]
        elif elements[0:2] == ["rest", "appliance"]:
            elements = elements[1:]
        elif elements[0:2] == ["rest", "vcenter"]:
            elements = elements[1:]
        elif elements[:1] == ["api"]:
            elements = elements[1:]

        module_name = "_".join(elements)
        return module_name.replace("-", "")


class AnsibleModuleBase:
    def __init__(self, resource, definitions):
        self.resource = resource
        self.definitions = definitions
        self.name = resource.name
        self.description = "Handle resource of type {name}".format(
            name=resource.name
        )

    def parameters(self):
        def itera(operationId):
            versions = sorted(list(self.resource.operations[operationId].keys()))
            print(versions)
            print(self.resource.operations[operationId][versions[0]])
            for version in versions:
                print(version)
                for parameter in AnsibleModule._flatten_parameter(
                    self.resource.operations[operationId][version][2], self.definitions
                ):
                    print('-> %s' % parameter)
                    name = parameter["name"]
                    if name == "spec":
                        for i in parameter["subkeys"]:
                            i["since_version"] = version
                            yield i
                    else:
                        parameter["since_version"] = version
                        yield parameter

        results = {}
        for operationId in self.default_operationIds:
            if not operationId in self.resource.operations:
                continue
            for parameter in itera(operationId):
                print(parameter)
                name = parameter["name"]
                if name not in results:
                    results[name] = parameter
                    results[name]["operationIds"] = []
                results[name]["operationIds"].append(operationId)

        for name, result in results.items():
            if result.get("required"):
                if (
                    len(
                        set(self.default_operationIds)
                        - set(result["operationIds"])
                    )
                    > 0
                ):
                    result[
                        "description"
                    ] += " Required with I(state={})".format(
                        list(set(result["operationIds"]))
                    )
                del result["required"]
                result["required_if"] = set(result["operationIds"])

        results["state"] = {
            "name": "state",
            "default": "present",
            "type": "str",
            "enum": list(self.default_operationIds),
        }

        return results.values()

    def gen_arguments_py(self):
        def _add_key(assign, key, value):
            k = [ast.Constant(value=key, kind=None)]
            v = [ast.Constant(value=value, kind=None)]
            assign.value.keys.append(k)
            assign.value.values.append(v)

        ARGUMENT_TPL = """argument_spec['{name}'] = {{}}"""

        parameter_names = [i["name"] for i in self.parameters()]
        for parameter in self.parameters():
            assign = ast.parse(
                ARGUMENT_TPL.format(name=parameter["name"])
            ).body[0]

            if (
                hasattr(self, "list_index")
                and self.list_index()
                and self.list_index() not in parameter_names
            ):
                assign = ast.parse(
                    ARGUMENT_TPL.format(name=self.list_index())
                ).body[0]
                _add_key(assign, "aliases", [parameter["name"]])
                parameter["name"] = self.list_index()

            if parameter.get("required"):
                if (
                    hasattr(self, "list_index")
                    and self.list_index() == parameter["name"]
                ):
                    pass
                else:
                    _add_key(assign, "required", True)

            _add_key(assign, "type", self.python_type(parameter["type"]))
            if "enum" in parameter:
                _add_key(assign, "choices", sorted(parameter["enum"]))

            if "operationIds" in parameter:
                _add_key(assign, "operationIds", parameter["operationIds"])

            yield assign

    def gen_documentation(self):

        documentation = {
            "author": ["Ansible VMware team"],
            "description": self.description,
            "extends_documentation_fragment": [
                "ansible.vmware_rest.VmwareRestModule.documentation"
            ],
            "module": self.name,
            "notes": ["Tested on vSphere 6.7"],
            "options": {},
            "requirements": ["python >= 2.7"],
            "short_description": self.description,
            "version_added": "2.10",
        }

        for parameter in self.parameters():
            description = []
            option = {
                "type": parameter["type"],
            }
            if parameter.get("required"):
                option["required"] = True
            if parameter.get("description"):
                description.append(parameter["description"])
            if parameter.get("subkeys"):
                description.append("Validate attributes are:")
                for subkey in parameter.get("subkeys"):
                    subkey["type"] = self.python_type(subkey["type"])
                    description.append(
                        " - C({name}) ({type}): {description}".format(**subkey)
                    )
            option["description"] = description
            option["type"] = self.python_type(option["type"])
            if "enum" in parameter:
                option["choices"] = parameter["enum"]

            documentation["options"][parameter["name"]] = option
        return yaml.dump(documentation)

    def gen_url_func(self):
        last_operation = self.last_operation(list(self.default_operationIds)[0])
        path = last_operation[1]

        url_func = ast.parse(self.URL.format(path=path)).body[0]
        return url_func

    def python_type(self, value):
        TYPE_MAPPING = {
            "string": "str",
            "array": "list",
            "object": "dict",
            "boolean": "bool",
        }
        return TYPE_MAPPING.get(value, value)

    @staticmethod
    def _property_to_parameter(prop_struct, definitions):

        required_keys = prop_struct.get("required", [])
        try:
            properties = prop_struct["properties"]
        except KeyError:
            return prop_struct

        for name, v in properties.items():
            parameter = {
                "name": name,
                "type": v.get("type", "str"),  # 'str' by default, should be ok
                "description": v.get("description", ""),
                "required": True if name in required_keys else False,
            }

            if "$ref" in v:
                ref = definitions.get(v)
                if "properties" in ref:
                    subkeys = AnsibleModule._property_to_parameter(
                        definitions.get(v), definitions
                    )
                    parameter["type"] = "dict"
                    parameter["subkeys"] = list(subkeys)
                else:
                    for k, v in ref.items():
                        parameter[k] = v

            yield parameter

    @staticmethod
    def _flatten_parameter(parameter_structure, definitions):
        for i in parameter_structure:
            if "schema" in i:
                schema = definitions.get(i["schema"])
                for j in AnsibleModule._property_to_parameter(
                    schema, definitions
                ):
                    yield j
            else:
                yield i

    def in_query_parameters(self):
        return [p["name"] for p in self.parameters() if p.get("in") == "query"]

    def gen_main_func(self):
        raise NotImplementedError()

    def renderer(self):
        syntax_tree = ast.parse(MODULE_TEMPLATE)

        arguments = self.gen_arguments_py()
        documentation = self.gen_documentation()
        url_func = self.gen_url_func()
        main_func = self.gen_main_func()
        in_query_parameters = self.in_query_parameters()

        class SumTransformer(ast.NodeTransformer):
            def visit_FunctionDef(self, node):
                if node.name == "url":
                    node.body[0] = url_func
                elif node.name == "main":
                    node = main_func
                elif node.name == "prepare_argument_spec":
                    for arg in arguments:
                        node.body.insert(1, arg)
                return node

            def visit_Assign(self, node):
                if node.targets[0].id == "DOCUMENTATION":
                    node.value = ast.Str(documentation)

                if node.targets[0].id == "IN_QUERY_PARAMETER":
                    node.value = ast.Str(in_query_parameters)

                return node

        syntax_tree = SumTransformer().visit(syntax_tree)
        syntax_tree = ast.fix_missing_locations(syntax_tree)
        import astunparse

        print("rendering {name}".format(name=self.name))
        module_dir = pathlib.Path("plugins/modules")
        module_dir.mkdir(exist_ok=True)
        module_py_file = module_dir / "{name}.py".format(name=self.name)
        with module_py_file.open("w") as fd:
            fd.write(astunparse.unparse(syntax_tree))

    def last_operation(self, operationId):
        last_version = sorted(list(self.resource.operations[operationId].keys()))[-1]
        return self.resource.operations[operationId][last_version]


class AnsibleModule(AnsibleModuleBase):

    URL = """
return "{path}".format(**module.params)
"""

    def __init__(self, resource, definitions):
        super().__init__(resource, definitions)
        # TODO: We can probably do better
        self.default_operationIds = set(
            list(self.resource.operations.keys())
        ) - set(["get", "list"])

    def gen_main_func(self):
        MAIN_FUNC = """
def main():
    module = vmware_httpapi.VmwareRestModule(
        argument_spec=prepare_argument_spec(),
        #supports_check_mode=True,
        #is_multipart=True,
    )

    import q
    globals()["_" + module.params['state']](module)
    module.exit()
"""
        main_func = ast.parse(MAIN_FUNC)

        for operation in self.default_operationIds:
            (verb, path, _) = self.last_operation(operation)
            if "$" in operation:
                print(
                    "skipping operation {operation} for {path}".format(
                        operation=operation, path=path
                    )
                )
                continue

            FUNC_NO_DATA_TPL = """
def _{operation}(module):
    module.{verb}(url="{path}".format(**module.params) + gen_args(module))
"""
            FUNC_WITH_DATA_TPL = """
def _{operation}(module):
    accepted_fields = []
    spec = {{}}
    for i in accepted_fields:
        if module.params[i]:
            spec[i] = module.params[i]
    module.{verb}(url="{path}".format(**module.params), data={{'spec': spec}})
"""

            data_accepted_fields = []
            for p in self.parameters():
                if "operationIds" in p:
                    if operation in p["operationIds"]:
                        if not p.get("in") in ["path", "query"]:
                            data_accepted_fields.append(p["name"])

            if data_accepted_fields:
                func = ast.parse(
                    FUNC_WITH_DATA_TPL.format(
                        operation=operation, verb=verb, path=path
                    )
                ).body[0]
                func.body[0].value.elts = [
                    ast.Constant(value=i, kind=None)
                    for i in data_accepted_fields
                ]
            else:
                func = ast.parse(
                    FUNC_NO_DATA_TPL.format(
                        operation=operation, verb=verb, path=path,
                    )
                ).body[0]

            main_func.body.append(func)

        return main_func.body


class AnsibleInfoModule(AnsibleModuleBase):

    URL_WITH_LIST = """
if module.params['{list_index}']:
    return "{path}".format(**module.params) + gen_args(module)
else:
    return "{list_path}".format(**module.params) + gen_args(module)
"""

    URL_LIST_ONLY = """
return "{list_path}".format(**module.params) + gen_args(module)
"""

    URL = """
return "{path}".format(**module.params) + gen_args(module)
"""

    def __init__(self, resource, definitions):
        super().__init__(resource, definitions)
        self.name = resource.name + "_info"
        self.default_operationIds = ["get", "list"]

    def list_index(self):
        if "get" not in self.resource.operations:
            return
        path = self.last_operation("get")[1]
        m = re.search(r"{([-\w]+)}$", path)
        if m:
            return m.group(1)

    def parameters(self):
        return [i for i in list(super().parameters()) if i["name"] != "state"]

    def gen_url_func(self):
        path = None
        list_path = None

        if "get" in self.resource.operations:
            path = self.last_operation("get")[1]
        if "list" in self.resource.operations:
            path = self.last_operation("list")[1]

        if not path:
            url_func = ast.parse(
                self.URL_LIST_ONLY.format(list_path=list_path)
            ).body[0]
        elif list_path and path.endswith("}"):
            url_func = ast.parse(
                self.URL_WITH_LIST.format(
                    path=path,
                    list_path=list_path,
                    list_index=self.list_index(),
                )
            ).body[0]
        else:
            url_func = ast.parse(self.URL.format(path=path)).body[0]
        return url_func

    def gen_main_func(self):
        MAIN_FUNC = """
def main():
    module = vmware_httpapi.VmwareRestModule(
        argument_spec=prepare_argument_spec(),
        supports_check_mode=True,
        is_multipart=True,
    )
    module.get(url=url(module))
    module.exit()
"""
        return ast.parse(MAIN_FUNC).body[0]

    def write_functional_tests(self):
        base_dir = pathlib.Path(
            "tests/integration/targets/{name}".format(name=self.name)
        )
        tasks_dir = base_dir / "tasks/"
        tasks_dir.mkdir(parents=True, exist_ok=True)

        p = tasks_dir / "main.yaml"
        module_arguments = {}

        data = []
        parameter_names = [i["name"] for i in self.parameters()]
        if "vm" in parameter_names:
            data += [
                {
                    "vcenter_vm_info": {"filter.names": ["test_vm1"]},
                    "register": "test_vm1",
                }
            ]

        if re.search(r"appliance_networking_interfaces_ipv\d_info", self.name):
            module_arguments = {"interface_name": "nic0"}
        elif "vm" in parameter_names:
            module_arguments = {"vm": "{{ test_vm1.result.value[0].vm }}"}
        # elif 'systemName' in self.parameters:
        #     module_arguments = {'systemName': 'vcenter.test'}

        data += [{"{name}".format(name=self.name): module_arguments}]
        p.write_text(yaml.dump(data))

        p = base_dir / "aliases"
        p.write_text("network/vmware_rest\n")
        if self.name in [
            "appliance_health_messages_info",
            "appliance_health_system_lastcheck_info",  # This one is broken on MY installation. I need to troubleshoot that later.
            "appliance_monitoring_query_info",  # My bet, the API doc is not up to date: fatal: [vcenter.test]: FAILED! => {"changed": false, "msg": "Structure operation-input is missing a field \"item\""}
            "appliance_networking_dns_servers_info",  # {"changed": false, "msg": "Internal error. See logs for details. https://vcenter.test/appliance/support-bundle"}
            "appliance_networking_info",  # fatal: [vcenter.test]: FAILED! => {"changed": false, "msg": "Error in method invocation ('netmgr --get failed with error. Err = %s', b'')"}
            "appliance_recovery_backup_systemname_archives_info",  # "fatal: [vcenter.test]: FAILED! => {"changed": false, "msg": "Structure operation-input is missing a field \"loc_spec\""}
            "appliance_recovery_backup_systemname_info",  # fatal: [vcenter.test]: FAILED! => {"changed": false, "msg": "Structure operation-input is missing a field \"loc_spec\""}
            "appliance_recovery_reconciliation_job_info",  # fatal: [vcenter.test]: FAILED! => {"changed": false, "msg": "Requested object was not found."}
            "appliance_recovery_restore_job_info",  #  fatal: [vcenter.test]: FAILED! => {"changed": false, "msg": "Status for 'RESTORE' does not exist."}
            "appliance_system_uptime_info",  # fatal: [vcenter.test]: FAILED! => {"changed": false, "msg": "Internal error. See logs for details. https://vcenter.test/appliance/support-bundle"}
            "appliance_update_pending_info",  # fatal: [vcenter.test]: FAILED! => {"changed": false, "msg": "Structure operation-input is missing a field \"source_type\""}
            "appliance_update_staged_info",  # fatal: [vcenter.test]: FAILED! => {"changed": false, "msg": "Nothing is staged"}
            "com_vmware_content_library_item_downloadsession_file_info",  # fatal: [vcenter.test]: FAILED! => {"changed": false, "msg": "Unable to validate input to method com.vmware.content.library.item.downloadsession.file.list"}
            "com_vmware_content_library_item_file_info",  # fatal: [vcenter.test]: FAILED! => {"changed": false, "msg": "Unable to validate input to method com.vmware.content.library.item.file.list"}
            "com_vmware_content_library_item_info",  # fatal: [vcenter.test]: FAILED! => {"changed": false, "msg": "Unable to validate input to method com.vmware.content.library.item.list"}
            "com_vmware_content_library_item_storage_info",  # fatal: [vcenter.test]: FAILED! => {"changed": false, "msg": "Unable to validate input to method com.vmware.content.library.item.storage.list"}
            "com_vmware_content_library_item_updatesession_file_info",  # fatal: [vcenter.test]: FAILED! => {"changed": false, "msg": "Unable to validate input to method com.vmware.content.library.item.updatesession.file.list"}
            "com_vmware_vapi_info",  # fatal: [vcenter.test]: FAILED! => {"changed": false, "msg": "Requested object was not found."}
            "com_vmware_vapi_metadata_authentication_service_operation_info",  # fatal: [vcenter.test]: FAILED! => {"changed": false, "msg": "Unable to validate input to method com.vmware.vapi.metadata.authentication.service.operation.list"}
            "com_vmware_vapi_metadata_metamodel_resource_model_info",  # fatal: [vcenter.test]: FAILED! => {"changed": false, "msg": "Unable to validate input to method com.vmware.vapi.metadata.metamodel.resource.model.list"}
            "com_vmware_vapi_metadata_privilege_service_operation_info",
            "com_vmware_vcenter_ovf_importflag_info",
            "vcenter_deployment_install_info",  # fatal: [vcenter.test]: FAILED! => {"changed": false, "msg": "Failed to retrieve the saved specification file. The appliance is not configured through the deployment API."}
            "vcenter_deployment_install_initialconfig_remotepsc_thumbprint_info",  # fatal: [vcenter.test]: FAILED! => {"changed": false, "msg": "Structure operation-input is missing a field \"spec\""}
            "vcenter_deployment_question_info",  # fatal: [vcenter.test]: FAILED! => {"changed": false, "msg": "This appliance is not in QUESTION_RAISED state, so there is no question that can be returned."}
            "vcenter_deployment_upgrade_info",  # fatal: [vcenter.test]: FAILED! => {"changed": false, "msg": "Failed to retrieve the saved specification file. The appliance is not configured through the deployment API."}
            "vcenter_storage_policies_compliance_vm_info",  # fatal: [vcenter.test]: FAILED! => {"changed": false, "msg": "Unable to validate input to method com.vmware.vcenter.storage.policies.compliance.VM.list"}
            "vcenter_storage_policies_entities_compliance_info",  # fatal: [vcenter.test]: FAILED! => {"changed": false, "msg": "Requested object was not found."}
            "vcenter_vcha_cluster_mode_info",  # fatal: [vcenter.test]: FAILED! => {"changed": false, "msg": "The operation is not allowed in the current state."}
        ]:
            p.write_text("disabled\n")
        elif (
            len(
                [
                    i
                    for i in self.parameters()
                    if i["name"] != "vm" and i.get("required")
                ]
            )
            > 0
        ):
            p.write_text("disabled\n")


class Definitions:
    def __init__(self, data):
        super().__init__()
        self.definitions = data

    # e.g: #/definitions/com.vmware.vcenter.inventory.datastore_find
    def _ref_to_dotted(self, ref):
        return ref["$ref"].split("/")[2]

    def get(self, ref):
        dotted = self._ref_to_dotted(ref)
        if dotted not in self.definitions:
            print("Cannot find key {dotted}".format(dotted=dotted))
            return {}
        v = self.definitions[self._ref_to_dotted(ref)]
        return v


class Path:
    def __init__(self, path, value):
        super().__init__()
        self.path = path
        self.operations = {}
        self.verb = {}
        self.value = value

    def summary(self, verb):
        return self.value[verb]["summary"]


class SwaggerFile:
    def __init__(self):
        super().__init__()
        self.definitions = []
        self.paths = {}
        self.resources = {}

    def open(self, json_definition, version):
        data = json.loads(json_definition.open().read())
        self.definitions = Definitions(data["definitions"])
        self.load_paths(data["paths"], version)

    def load_paths(self, paths, version):
        for path in [Path(p, v) for p, v in paths.items()]:
            # if not path.path.startswith("/vcenter/vm/{vm}/hardware/adapter/sata"):
            #     continue
            if not path in self.paths:
                self.paths[path.path] = path
            for verb, desc in path.value.items():
                operationId = desc["operationId"]
                path.operations[operationId] = (
                    verb,
                    path.path,
                    desc["parameters"],
                )

    def init_resources(self, version):
        for path in self.paths.values():
            name = Resource.path_to_name(path)
            if not name in self.resources:
                self.resources[name] = Resource(name)
                self.resources[name].description = ""  # path.summary(verb)
                self.resources[name].since_version = version

            for k, v in path.operations.items():
                if not v:
                    raise Exception(k)
                # if k in self.resources[name].operations:
                #     # raise Exception(
                #     #     "operationId already defined: %s vs %s"
                #     #     % (self.resources[name].operations[k], v)
                #     # )
                #     continue
                k = k.replace(
                    "$task", ""
                )  # NOTE: Not sure if this is the right thing to do
                self.resources[name].operations[k] = {version: v}


def main():
    input_files = ["appliance.json",  "cis.json",  "content.json",  "esx.json",  "stats.json",  "vapi.json", "vcenter.json"]
    for input_file in input_files:
        print("Generating modules from {}".format(input_file))
        swagger_file = SwaggerFile()
        for version in ["6.7.0", "7.0.0"]:
            input_file_path = pathlib.Path(version) / input_file
            if not input_file_path.exists():
                continue
            swagger_file.open(input_file_path, version=version)
            swagger_file.init_resources(version=version)

        for resource in swagger_file.resources.values():
            if "get" in resource.operations or "list" in resource.operations:
                module = AnsibleInfoModule(
                    resource, definitions=swagger_file.definitions
                )
                if len(module.default_operationIds) > 0:
                    module.write_functional_tests()
                    module.renderer()
            module = AnsibleModule(
                resource, definitions=swagger_file.definitions
            )
            if len(module.default_operationIds) > 0:
                module.renderer()


    # p = pathlib.Path("6.7.0")
    # for json_file in p.glob("*.json"):
    #     print("Generating modules from {}".format(json_file))
    #     swagger_file = SwaggerFile(json_file)
    #     swagger_file.init_resources()

    #     for resource in swagger_file.resources.values():
    #         if "get" in resource.operations or "list" in resource.operations:
    #             module = AnsibleInfoModule(
    #                 resource, definitions=swagger_file.definitions
    #             )
    #             if len(module.default_operationIds) > 0:
    #                 module.write_functional_tests()
    #                 module.renderer()
    #         module = AnsibleModule(
    #             resource, definitions=swagger_file.definitions
    #         )
    #         if len(module.default_operationIds) > 0:
    #             module.renderer()


if __name__ == "__main__":
    main()
