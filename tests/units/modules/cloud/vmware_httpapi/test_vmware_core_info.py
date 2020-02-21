from __future__ import absolute_import, division, print_function

__metaclass__ = type

import pytest

from .conftest import enable_vcr

import six
if six.PY3:
    from unittest.mock import ANY as ANY
else:
    import mock.ANY as ANY


@enable_vcr()
def test_empty_vm_list(run_module):
    exit_json = run_module(
        "vmware_core_info", {"object_type": "vm", "filters": [{"names": "a"}]}
    )
    exit_json.assert_called_with(
        ANY,
        invocation={
            "module_args": {
                "object_type": "vm",
                "filters": [{"names": "a"}],
                "allow_multiples": False,
                "log_level": "normal",
                "status_code": [200],
            },
            "module_kwargs": {
                "is_multipart": False,
                "use_object_handler": True,
            },
        },
        vm={"value": []},
    )


@pytest.mark.skip(reason="currently broken")
@enable_vcr()
def test_empty_vm_list_with_no_filter(run_module):
    exit_json, fail_json = run_module(
        "vmware_core_info", {"object_type": "vm"}
    )
    fail_json.assert_called_with(
        ANY,
        invocation={
            "module_args": {
                "object_type": "vm",
                "filters": [],
                "allow_multiples": False,
                "log_level": "normal",
                "status_code": [200],
            },
            "module_kwargs": {
                "is_multipart": False,
                "use_object_handler": True,
            },
        },
        vm={"value": []},
    )
