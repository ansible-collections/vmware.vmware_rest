# -*- coding: utf-8 -*-
# Copyright: (c) 2026, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import pytest
from unittest.mock import patch, MagicMock

from ansible_collections.vmware.vmware_rest.plugins.modules import (
    vcenter_vm_storage_policy_compliance_info as module_under_test,
)
from ...common.utils import (
    AnsibleExitJson,
    exit_json,
    set_module_args,
    _response,
)

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
def module_args():
    return {"vm": "vm-1009"}


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

    mock_client.get.return_value = _response(200, None)

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_module.exit_json.assert_called_once()
    assert exc.value.kwargs == {"value": {}}
