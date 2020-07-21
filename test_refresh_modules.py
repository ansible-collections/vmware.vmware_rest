import ast
import pytest
import types

import refresh_modules as rm

my_parameters = [
    {"name": "aaa", "type": "boolean", "description": "a second parameter",},
    {
        "name": "aaa",
        "type": "integer",
        "required": True,
        "description": "a second parameter",
        "subkeys": [{"type": "ccc", "name": "a_subkey", "description": "more blabla"}],
    },
    {
        "name": "ccc",
        "type": "list",
        "description": "3rd parameter is enum",
        "enum": ["a", "b", "c"],
    },
]


def test_normalize_description():
    assert rm.normalize_description(["a", "b"]) == ["a", "b"]
    assert rm.normalize_description(["{@name DayOfWeek}"]) == ["day of the week"]
    assert rm.normalize_description([" {@term enumerated type}"]) == [""]


def test_python_type():
    assert rm.python_type("array") == "list"
    assert rm.python_type("list") == "list"
    assert rm.python_type("boolean") == "bool"


def test_path_to_name():
    assert rm.path_to_name("/rest/cis/tasks") == "rest_cis_tasks"
    assert (
        rm.path_to_name("/rest/com/vmware/cis/tagging/category")
        == "cis_tagging_category"
    )
    assert (
        rm.path_to_name("/rest/com/vmware/cis/tagging/category/id:{category_id}")
        == "cis_tagging_category"
    )
    assert (
        rm.path_to_name(
            "/rest/com/vmware/cis/tagging/category/id:{category_id}?~action=add-to-used-by"
        )
        == "cis_tagging_category"
    )
    assert (
        rm.path_to_name("/rest/vcenter/vm/{vm}/hardware/ethernet/{nic}/disconnect")
        == "vcenter_vm_hardware_ethernet_disconnect"
    )


def test_gen_documentation():

    assert rm.gen_documentation("foo", "bar", my_parameters) == {
        "author": ["Ansible VMware team"],
        "description": "bar",
        "extends_documentation_fragment": [],
        "module": "foo",
        "notes": ["Tested on vSphere 7.0"],
        "options": {
            "aaa": {
                "description": [
                    "a second parameter",
                    "Validate attributes are:",
                    " - C(a_subkey) (ccc): more blabla",
                ],
                "required": True,
                "type": "int",
            },
            "ccc": {
                "choices": ["a", "b", "c"],
                "description": ["3rd parameter is enum"],
                "type": "list",
            },
        },
        "requirements": ["python >= 3.6"],
        "short_description": "bar",
        "version_added": "1.0.0",
    }


def test_gen_arguments_py(monkeypatch):
    assert type(rm.gen_arguments_py([])) == types.GeneratorType
    assert list(rm.gen_arguments_py([])) == []
    ret = rm.gen_arguments_py(my_parameters)
    assert ast.dump(ret.__next__().value) == ast.dump(
        ast.Dict(
            keys=[[ast.Constant(value="type")]], values=[[ast.Constant(value="bool")]]
        )
    )
    assert ast.dump(ret.__next__().value) == ast.dump(
        ast.Dict(
            keys=[[ast.Constant(value="required")], [ast.Constant(value="type")]],
            values=[[ast.Constant(value=True)], [ast.Constant(value="int")]],
        )
    )
