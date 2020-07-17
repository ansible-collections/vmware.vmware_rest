#!/usr/bin/env python3

import argparse
import ast
import json
import re
import yaml
import pathlib
import astunparse

from pprint import pprint


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
        # workaround for vcenter_vm_power
        if elements[-1] in ('stop', 'start', 'suspend', 'reset'):
            elements = elements[:-1]
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
            for parameter in AnsibleModule._flatten_parameter(
                self.resource.operations[operationId][2], self.definitions
            ):
                name = parameter["name"]
                if name == "spec":
                    for i in parameter["subkeys"]:
                        yield i
                else:
                    yield parameter

        results = {}
        for operationId in self.default_operationIds:
            if not operationId in self.resource.operations:
                continue
            for parameter in itera(operationId):
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

            if parameter["name"] in ["user_name", "username", "password"]:
                _add_key(assign, "nolog", True)

            if parameter.get("required"):
                if (
                    hasattr(self, "list_index")
                    and self.list_index() == parameter["name"]
                ):
                    pass
                else:
                    _add_key(assign, "required", True)

            # "bus" option defaulting on 0
            if parameter["name"] == "bus":
                _add_key(assign, "default", 0)

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
            # "extends_documentation_fragment": [
            #     "ansible.vmware_rest.VmwareRestModule.documentation"
            # ],
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
        first_operation = list(self.resource.operations.values())[0]
        path = first_operation[1]

        if not path.startswith("/rest"): # Pre 7.0.0
            path = "/rest" + path

        url_func = ast.parse(self.URL.format(path=path)).body[0]
        return url_func

    def python_type(self, value):
        TYPE_MAPPING = {
            "array": "list",
            "boolean": "bool",
            "integer": "int",
            "object": "dict",
            "string": "str",
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
        #syntax_tree = ast.parse(MODULE_TEMPLATE)
        DEFAULT_MODULE = """
#!/usr/bin/env python
# Info module template
from __future__ import absolute_import, division, print_function
__metaclass__ = type
import socket
import json

DOCUMENTATION = ""

IN_QUERY_PARAMETER = None


from ansible.module_utils.basic import env_fallback
from ansible_module.turbo.module import AnsibleTurboModule as AnsibleModule
# from ansible.module_utils.basic import AnsibleModule
from ansible_collections.vmware.vmware_rest.plugins.module_utils.vmware_rest import (
    gen_args,
    open_session,
    update_changed_flag)



def prepare_argument_spec():
    argument_spec = {{
        "vcenter_hostname": dict(
            type='str',
            required=False,
            fallback=(env_fallback, ['VMWARE_HOST']),
        ),
        "vcenter_username": dict(
            type='str',
            required=False,
            fallback=(env_fallback, ['VMWARE_USER']),
        ),
        "vcenter_password": dict(
            type='str',
            required=False,
            no_log=True,
            fallback=(env_fallback, ['VMWARE_PASSWORD']),
        ),
        "vcenter_certs": dict(
            type='bool',
            required=False,
            no_log=True,
            fallback=(env_fallback, ['VMWARE_VALIDATE_CERTS']),
        )
    }}




    return argument_spec

async def get_device_info(params, session, _url, _key):
    async with session.get(_url + '/' + _key) as resp:
        _json = (await resp.json())
        entry = _json['value']
        entry['_key'] = _key
        return entry



async def list_devices(params, session):
    existing_entries = []
    _url = url(params)
    async with session.get(_url) as resp:
        _json = (await resp.json())
        devices = _json['value']
    for device in devices:
        _id = list(device.values())[0]
        existing_entries.append((await get_device_info(params, session, _url, _id)))
    return existing_entries


async def exists(params, session):
    unicity_keys = ["bus", "pci_slot_number"]
    devices = await list_devices(params, session)
    for device in devices:
        for k in unicity_keys:
            if params.get(k) is not None and device.get(k) != params.get(k):
                break
        else:
            return device



async def main( ):
    module_args = prepare_argument_spec()
    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)
    session = await open_session(vcenter_hostname=module.params['vcenter_hostname'], vcenter_username=module.params['vcenter_username'], vcenter_password=module.params['vcenter_password'])
    result = await entry_point(module, session)
    module.exit_json(**result)

def url(params):
    pass

def entry_point():
    pass

if __name__ == '__main__':
    import asyncio
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

"""
        syntax_tree = ast.parse(DEFAULT_MODULE.format(name=self.name))
        arguments = self.gen_arguments_py()
        documentation = self.gen_documentation()
        url_func = self.gen_url_func()
        #main_func = self.gen_main_func()
        entry_point_func = self.gen_entry_point_func()

        in_query_parameters = self.in_query_parameters()


        class SumTransformer(ast.NodeTransformer):
            def visit_FunctionDef(self, node):

                return node

            def visit_Assign(self, node):


                if node.targets[0].id == "IN_QUERY_PARAMETER":
                    node.value = ast.Str(in_query_parameters)

                return node


            def visit_FunctionDef(self, node):
                if node.name == "url":
                    node.body[0] = url_func
                elif node.name == "entry_point":
                    node = entry_point_func
                elif node.name == "prepare_argument_spec":
                    for arg in arguments:
                        node.body.insert(1, arg)
                return node
            def visit_Assign(self, node):
                if not isinstance(node.targets[0], ast.Name):
                    pass
                elif node.targets[0].id == "DOCUMENTATION":
                   node.value = ast.Str(documentation)
                elif node.targets[0].id == "IN_QUERY_PARAMETER":
                    node.value = ast.Str(in_query_parameters)
                return node

        syntax_tree = SumTransformer().visit(syntax_tree)
        syntax_tree = ast.fix_missing_locations(syntax_tree)


        module_dir = pathlib.Path("plugins/modules")
        module_dir.mkdir(exist_ok=True)
        module_py_file = module_dir / "{name}.py".format(name=self.name)
        with module_py_file.open("w") as fd:
            fd.write(astunparse.unparse(syntax_tree))



class AnsibleModule(AnsibleModuleBase):

    URL = """
return "https://{{vcenter_hostname}}{path}".format(**params)
"""

    def __init__(self, resource, definitions):
        super().__init__(resource, definitions)
        # TODO: We can probably do better
        self.default_operationIds = set(
            list(self.resource.operations.keys())
        ) - set(["get", "list"])

    def gen_entry_point_func(self):
        MAIN_FUNC = """
async def entry_point(module, session):
    func = globals()["_" + module.params['state']]
    return await func(module.params, session)
"""
        main_func = ast.parse(MAIN_FUNC.format(name=self.name))

        for operation in self.default_operationIds:
            (verb, path, _) = self.resource.operations[operation]
            if not path.startswith("/rest"): # TODO
                path = "/rest" + path
            if "$" in operation:
                print(
                    "skipping operation {operation} for {path}".format(
                        operation=operation, path=path
                    )
                )
                continue

            FUNC_NO_DATA_TPL = """
async def _{operation}(params, session):
    _url = "https://{{vcenter_hostname}}{path}".format(**params) + gen_args(params, IN_QUERY_PARAMETER)
    async with session.{verb}(_url) as resp:
        try:
            if resp.headers["Content-Type"] == "application/json":
                _json = await resp.json()
        except KeyError:
            _json = {{}}
        return await update_changed_flag(_json, resp.status, "{operation}")
"""
            FUNC_WITH_DATA_TPL = """
async def _{operation}(params, session):
    accepted_fields = []

    if "{operation}" == "create":
        _exists = await exists(params, session)
        if _exists:
            return (await update_changed_flag({{"value": _exists}}, 200, 'get'))

    spec = {{}}
    for i in accepted_fields:
        if params[i]:
            spec[i] = params[i]
    _url = "https://{{vcenter_hostname}}{path}".format(**params)
    async with session.{verb}(_url, json={{'spec': spec}}) as resp:
        try:
            if resp.headers["Content-Type"] == "application/json":
                _json = await resp.json()
        except KeyError:
            _json = {{}}
        # Update the value field with all the details
        if "{operation}" == "create" and "value" in _json:
            if type(_json["value"]) == dict:
                _id = list(_json["value"].values())[0]
            else:
                _id = _json["value"]
            _json = {{"value": await get_device_info(params, session, _url, _id)}}

        return await update_changed_flag(_json, resp.status, "{operation}")
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
if params['{list_index}']:
    return "https://{{vcenter_hostname}}{path}".format(**params) + gen_args(params, IN_QUERY_PARAMETER)
else:
    return "https://{{vcenter_hostname}}{list_path}".format(**params) + gen_args(params, IN_QUERY_PARAMETER)
"""

    URL_LIST_ONLY = """
return "https://{{vcenter_hostname}}{list_path}".format(**params) + gen_args(params, IN_QUERY_PARAMETER)
"""

    URL = """
return "https://{{vcenter_hostname}}{path}".format(**params) + gen_args(params, IN_QUERY_PARAMETER)
"""

    def __init__(self, resource, definitions):
        super().__init__(resource, definitions)
        self.name = resource.name + "_info"
        self.default_operationIds = ["get", "list"]

    def list_index(self):
        if "get" not in self.resource.operations:
            return
        path = self.resource.operations["get"][1]
        m = re.search(r"{([-\w]+)}$", path)
        if m:
            return m.group(1)

    def parameters(self):
        return [i for i in list(super().parameters()) if i["name"] != "state"]

    def gen_url_func(self):
        path = None
        list_path = None
        if "get" in self.resource.operations:
            path = self.resource.operations["get"][1]
        if "list" in self.resource.operations:
            list_path = self.resource.operations["list"][1]

        if path and not path.startswith("/rest"): # Pre 7.0.0
            path = "/rest" + path
        if list_path and not list_path.startswith("/rest"): # Pre 7.0.0
            list_path = "/rest" + list_path

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

    def gen_entry_point_func(self):
        FUNC = """
async def entry_point(module, session):
    async with session.get(url(module.params)) as resp:
        _json = await resp.json()
        return await update_changed_flag(_json, resp.status, "get")
"""
        return ast.parse(FUNC.format(name=self.name)).body[0]


class Definitions:
    def __init__(self, data):
        super().__init__()
        self.definitions = data

    # e.g: #/definitions/com.vmware.vcenter.inventory.datastore_find
    def _ref_to_dotted(self, ref):
        return ref["$ref"].split("/")[2]

    def get(self, ref):
        dotted = self._ref_to_dotted(ref)
        v = self.definitions[dotted]
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
    def __init__(self, file_path):
        super().__init__()
        self.definitions = []
        self.paths = {}
        self.resources = {}
        self.file_path = file_path
        self.open(file_path)

    def open(self, json_definition):
        data = json.loads(json_definition.open().read())
        self.definitions = Definitions(data["definitions"])
        self.load_paths(data["paths"])

    def load_paths(self, paths):
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

    def init_resources(self):
        for path in self.paths.values():
            name = Resource.path_to_name(path)
            if not name in self.resources:
                self.resources[name] = Resource(name)
                self.resources[name].description = ""  # path.summary(verb)

            for k, v in path.operations.items():
                if k in self.resources[name].operations:
                    raise Exception(
                        "operationId already defined: %s vs %s"
                        % (self.resources[name].operations[k], v)
                    )
                k = k.replace(
                    "$task", ""
                )  # NOTE: Not sure if this is the right thing to do
                self.resources[name].operations[k] = v


def main():
    module_list = []
    p = pathlib.Path("7.0.0")
    for json_file in p.glob("*.json"):
        if str(json_file) == "7.0.0/appliance.json":
            continue
        if str(json_file) == "7.0.0/api.json":
            continue
        print("Generating modules from {}".format(json_file))
        swagger_file = SwaggerFile(json_file)
        swagger_file.init_resources()

        for resource in swagger_file.resources.values():
            print(resource.name)
            if resource.name == "appliance_networking":
                continue
            if "get" in resource.operations or "list" in resource.operations:
                module = AnsibleInfoModule(
                    resource, definitions=swagger_file.definitions
                )
                if len(module.default_operationIds) > 0:
                    module.renderer()
                    module_list.append(module.name)
            module = AnsibleModule(
                resource, definitions=swagger_file.definitions
            )
            if len(module.default_operationIds) > 0:
                module.renderer()
                module_list.append(module.name)
        print(module_list)
# NOTE: module_defaults are not yet supported by ansible/ansible, maybe 2.11.
#    meta_dir = pathlib.Path("meta")
#    meta_dir.mkdir(exist_ok=True)
#    runtime_yaml = meta_dir / "runtime.yml"
#    with runtime_yaml.open('w') as fd:
#        fd.write(yaml.dump({"action_groups": {"vmware_rest": module_list}}))


if __name__ == "__main__":
    main()
