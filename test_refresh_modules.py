import pytest


from refresh_modules import AnsibleModule


def test_flatten_parameter_in_path():
    parameter_struct = [
        {
            "description": "System name identifier.",
            "in": "path",
            "name": "systemName",
            "required": True,
            "type": "string",
        },
        {
            "description": "Archive identifier.",
            "in": "path",
            "name": "archive",
            "required": True,
            "type": "string",
        },
    ]
    result = AnsibleModule._flatten_parameter(parameter_struct, None)
    assert list(result) == parameter_struct


def test_flatten_parameter_schema():
    parameter_struct = [
        {
            "description": "Identifier of the service element.",
            "in": "path",
            "name": "service_id",
            "required": True,
            "type": "string",
        },
        {
            "in": "body",
            "name": "request_body",
            "required": True,
            "schema": {
                "$ref": "#/definitions/a_list"
            },
        },
        {
            "name": "bba",
            "$ref": "#/definitions/just_a_key"
        },

    ]

    expectation = [
        {
            "description": "Identifier of the service element.",
            "in": "path",
            "name": "service_id",
            "required": True,
            "type": "string",
        },
        {
            "description": "Identifier of the operation element.",
            "name": "operation_id",
            "required": True,
            "type": "string",
        },
        {
            "description": "Identifier of the service element.",
            "name": "service_id",
            "required": True,
            "type": "string",
        },
    ]

    class Definitions:
        def get(self, key):
            my_dict = {
                "#/definitions/a_list": {
                    "properties": {
                        "operation_id": {
                            "description": "Identifier of the operation "
                            "element.",
                            "type": "string",
                        },
                        "service_id": {
                            "description": "Identifier of the service "
                            "element.",
                            "type": "string",
                        },
                    },
                    "required": ["service_id", "operation_id"],
                    "type": "object",
                },
                "#/definitions/just_a_key": {
                        "my_Value": {
                            "description": "some value"
                        },
                    }
            }
            return my_dict[key["$ref"]]

    result = AnsibleModule._flatten_parameter(parameter_struct, Definitions())
    assert list(result) == expectation
