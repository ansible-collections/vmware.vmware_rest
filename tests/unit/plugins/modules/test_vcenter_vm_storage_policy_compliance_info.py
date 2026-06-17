# -*- coding: utf-8 -*-
# Copyright: (c) 2026, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import json
import pytest
from unittest.mock import patch, MagicMock

from ansible_collections.vmware.vmware_rest.plugins.module_utils._client import (
    Response,
)
from ansible_collections.vmware.vmware_rest.plugins.modules import (
    vcenter_vm_storage_policy_compliance_info as module_under_test,
)


class AnsibleExitJson(Exception):
    def __init__(self, kwargs):
        self.kwargs = kwargs


class AnsibleFailJson(Exception):
    def __init__(self, kwargs):
        self.kwargs = kwargs


def exit_json(*args, **kwargs):
    if args:
        kwargs.update(args[0])
    raise AnsibleExitJson(kwargs)


def fail_json(*args, **kwargs):
    if args:
        kwargs.update(args[0])
    raise AnsibleFailJson(kwargs)


def _response(status, body):
    data = json.dumps(body).encode("utf-8") if body is not None else b""
    return Response(status, data)


CONNECTION_PARAMS = {
    "vcenter_hostname": "vcenter.example.com",
    "vcenter_username": "admin",
    "vcenter_password": "secret",
    "vcenter_validate_certs": False,
    "vcenter_rest_log_file": None,
    "session_timeout": None,
}

# Vcenter.Vm.Storage.Policy.Compliance.Info (required: overall_compliance, disks)
COMPLIANCE_INFO = {
    "overall_compliance": "COMPLIANT",
    "vm_home": {
        "status": "COMPLIANT",
        "check_time": "2026-01-15T10:30:00Z",
        "policy": "policy-123",
        "failure_cause": [],
    },
    "disks": {
        "2000": {
            "status": "COMPLIANT",
            "check_time": "2026-01-15T10:30:00Z",
            "policy": "policy-123",
            "failure_cause": [],
        },
    },
}


@pytest.fixture
def mock_client():
    return MagicMock()


@pytest.fixture
def module_args():
    return {"vm": "vm-1009"}


def set_module_args(args):
    return {**CONNECTION_PARAMS, **args}


@patch.object(module_under_test, "AnsibleModule")
@patch.object(module_under_test.VmwareRestInfoModule, "_create_client")
def test_get_success(mock_create_client, mock_ansible_module, mock_client, module_args):
    # GET /vcenter/vm/{vm}/storage/policy/compliance — Vcenter.Vm.Storage.Policy.Compliance_get — 200
    mock_create_client.return_value = mock_client
    mock_module = MagicMock()
    mock_ansible_module.return_value = mock_module
    mock_module.params = set_module_args(module_args)
    mock_module.exit_json.side_effect = exit_json

    mock_client.get.return_value = _response(200, COMPLIANCE_INFO)

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_client.get.assert_called_once_with(
        "/vcenter/vm/vm-1009/storage/policy/compliance"
    )
    mock_module.exit_json.assert_called_once()
    assert exc.value.kwargs == {"value": COMPLIANCE_INFO}


@patch.object(module_under_test, "AnsibleModule")
@patch.object(module_under_test.VmwareRestInfoModule, "_create_client")
def test_get_not_found(
    mock_create_client, mock_ansible_module, mock_client, module_args
):
    # GET /vcenter/vm/{vm}/storage/policy/compliance — Vcenter.Vm.Storage.Policy.Compliance_get — 404
    mock_create_client.return_value = mock_client
    mock_module = MagicMock()
    mock_ansible_module.return_value = mock_module
    mock_module.params = set_module_args(module_args)
    mock_module.exit_json.side_effect = exit_json

    mock_client.get.return_value = _response(404, {"type": "NOT_FOUND"})

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_module.exit_json.assert_called_once()
    assert exc.value.kwargs == {"value": {}}


@patch.object(module_under_test, "AnsibleModule")
@patch.object(module_under_test.VmwareRestInfoModule, "_create_client")
def test_get_null_response(
    mock_create_client, mock_ansible_module, mock_client, module_args
):
    # GET /vcenter/vm/{vm}/storage/policy/compliance — Vcenter.Vm.Storage.Policy.Compliance_get — 200 nullable
    mock_create_client.return_value = mock_client
    mock_module = MagicMock()
    mock_ansible_module.return_value = mock_module
    mock_module.params = set_module_args(module_args)
    mock_module.exit_json.side_effect = exit_json

    mock_client.get.return_value = Response(200, b"null")

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_module.exit_json.assert_called_once()
    assert exc.value.kwargs == {"value": {}}
