# -*- coding: utf-8 -*-
# Copyright: (c) 2026, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible_collections.vmware.vmware_rest.plugins.module_utils._errors import (
    ApiCommunicationError,
    AuthError,
    UnexpectedAPIResponse,
    VmwareModuleError,
)


def test_vmware_module_error_message_and_fail_output():
    error = VmwareModuleError("something went wrong")
    assert str(error) == "something went wrong"
    assert error.to_module_fail_json_output() == {"msg": "something went wrong"}


def test_auth_error_is_vmware_module_error():
    error = AuthError("auth failed")
    assert isinstance(error, VmwareModuleError)
    assert error.to_module_fail_json_output() == {"msg": "auth failed"}


def test_unexpected_api_response_message():
    error = UnexpectedAPIResponse(500, b"internal error")
    assert "500" in str(error)
    assert "internal error" in str(error)
    assert error.to_module_fail_json_output() == {"msg": error.message}


def test_api_communication_error_default_message():
    exc = ValueError("connection reset")
    error = ApiCommunicationError(exception=exc)
    assert "ServiceNow API" in str(error)
    assert error.exception is exc


def test_api_communication_error_custom_message_and_context():
    exc = RuntimeError("boom")
    error = ApiCommunicationError(
        exception=exc,
        message="Failed to reach vCenter",
        method="GET",
        path="/api/vcenter/vm",
        timeout=30,
    )
    output = error.to_module_fail_json_output()
    assert output["msg"] == "Failed to reach vCenter"
    assert output["exception_info"] == {
        "message": "boom",
        "type": "RuntimeError",
    }
    assert output["debug_info"] == {
        "method": "GET",
        "path": "/api/vcenter/vm",
        "timeout": 30,
    }


def test_api_communication_error_excludes_non_jsonable_debug_values():
    exc = OSError("broken pipe")
    error = ApiCommunicationError(
        exception=exc,
        message="Request failed",
        method="POST",
        path="/api/vcenter/vm",
        callback=lambda: None,
    )
    output = error.to_module_fail_json_output()
    assert "callback" not in output["debug_info"]
    assert output["debug_info"]["method"] == "POST"
