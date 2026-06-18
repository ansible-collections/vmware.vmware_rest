# -*- coding: utf-8 -*-
# Copyright: (c) 2026, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import pytest
from unittest.mock import patch, MagicMock

from ansible_collections.vmware.vmware_rest.plugins.modules import (
    vcenter_vm_storage_policy_compliance as module_under_test,
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
    return {"state": "check", "vm": "vm-1009"}


@patch.object(module_under_test, "AnsibleModule")
@patch.object(module_under_test.VmwareRestComplianceModule, "_create_client")
def test_check_success_minimal(
    mock_create_client, mock_ansible_module, mock_client, module_args
):
    # POST /vcenter/vm/{vm}/storage/policy/compliance?action=check — Vcenter.Vm.Storage.Policy.Compliance_check — 200
    mock_create_client.return_value = mock_client
    mock_module = MagicMock()
    mock_ansible_module.return_value = mock_module
    mock_module.params = set_module_args(module_args)
    mock_module.exit_json.side_effect = exit_json

    mock_client.post.return_value = _response(200, COMPLIANCE_INFO)

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_client.post.assert_called_once_with(
        "/vcenter/vm/vm-1009/storage/policy/compliance",
        data=None,
        query={"action": "check"},
    )
    mock_module.exit_json.assert_called_once()
    assert exc.value.kwargs == {"changed": True, "value": COMPLIANCE_INFO}


@patch.object(module_under_test, "AnsibleModule")
@patch.object(module_under_test.VmwareRestComplianceModule, "_create_client")
def test_check_success_with_vm_home_and_disks(
    mock_create_client, mock_ansible_module, mock_client, module_args
):
    # POST /vcenter/vm/{vm}/storage/policy/compliance?action=check — Vcenter.Vm.Storage.Policy.Compliance_check — 200
    mock_create_client.return_value = mock_client
    mock_module = MagicMock()
    mock_ansible_module.return_value = mock_module
    mock_module.params = set_module_args(
        {
            **module_args,
            "vm_home": True,
            "disks": ["2000", "2001"],
        }
    )
    mock_module.exit_json.side_effect = exit_json

    mock_client.post.return_value = _response(200, COMPLIANCE_INFO)

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    # Vcenter.Vm.Storage.Policy.Compliance.CheckSpec body
    mock_client.post.assert_called_once_with(
        "/vcenter/vm/vm-1009/storage/policy/compliance",
        data={"vm_home": True, "disks": ["2000", "2001"]},
        query={"action": "check"},
    )
    mock_module.exit_json.assert_called_once()
    assert exc.value.kwargs == {"changed": True, "value": COMPLIANCE_INFO}


@patch.object(module_under_test, "AnsibleModule")
@patch.object(module_under_test.VmwareRestComplianceModule, "_create_client")
def test_check_null_response(
    mock_create_client, mock_ansible_module, mock_client, module_args
):
    # POST /vcenter/vm/{vm}/storage/policy/compliance?action=check — Vcenter.Vm.Storage.Policy.Compliance_check — 200 nullable
    mock_create_client.return_value = mock_client
    mock_module = MagicMock()
    mock_ansible_module.return_value = mock_module
    mock_module.params = set_module_args(module_args)
    mock_module.exit_json.side_effect = exit_json

    mock_client.post.return_value = _response(200, None)

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_module.exit_json.assert_called_once()
    assert exc.value.kwargs == {"changed": True, "value": {}}
