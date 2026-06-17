# -*- coding: utf-8 -*-
# Copyright: (c) 2026, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import pytest
from unittest.mock import patch, MagicMock

from ansible_collections.vmware.vmware_rest.plugins.modules import (
    vcenter_vm_tools as module_under_test,
)
from ...common.utils import (
    AnsibleExitJson,
    AnsibleFailJson,
    exit_json,
    fail_json,
    mock_client,
    set_module_args,
    _response,
)

TOOLS_PATH = "/vcenter/vm/vm-1001/tools"

# components/schemas/Vcenter.Vm.Tools.Info
TOOLS_INFO_MANUAL = {
    "auto_update_supported": True,
    "run_state": "RUNNING",
    "upgrade_policy": "MANUAL",
    "version_status": "CURRENT",
}

TOOLS_INFO_POWER_CYCLE = {
    "auto_update_supported": True,
    "run_state": "RUNNING",
    "upgrade_policy": "UPGRADE_AT_POWER_CYCLE",
    "version_status": "CURRENT",
}

@patch.object(module_under_test, "AnsibleModule")
@patch.object(module_under_test.VmwareRestCrudModule, "_create_client")
def test_update_upgrade_policy_changed(
    mock_create_client, mock_ansible_module, mock_client
):
    # GET 200 + PATCH 204 + GET 200 — Vcenter.Vm.Tools_update
    mock_create_client.return_value = mock_client
    mock_module = MagicMock()
    mock_ansible_module.return_value = mock_module
    mock_module.check_mode = False
    mock_module.params = set_module_args(
        {
            "vm": "vm-1001",
            "state": "present",
            "upgrade_policy": "UPGRADE_AT_POWER_CYCLE",
        }
    )
    mock_module.exit_json.side_effect = exit_json

    mock_client.get.side_effect = [
        _response(200, TOOLS_INFO_MANUAL),
        _response(200, TOOLS_INFO_POWER_CYCLE),
    ]
    mock_client.patch.return_value = _response(204, None)

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    assert mock_client.get.call_count == 2
    mock_client.get.assert_any_call(TOOLS_PATH)
    mock_client.patch.assert_called_once_with(
        TOOLS_PATH,
        data={"upgrade_policy": "UPGRADE_AT_POWER_CYCLE"},
    )
    mock_module.exit_json.assert_called_once()
    assert exc.value.kwargs == {
        "changed": True,
        "value": TOOLS_INFO_POWER_CYCLE,
    }

@patch.object(module_under_test, "AnsibleModule")
@patch.object(module_under_test.VmwareRestCrudModule, "_create_client")
def test_update_no_change(mock_create_client, mock_ansible_module, mock_client):
    # GET 200, no PATCH when upgrade_policy already matches
    mock_create_client.return_value = mock_client
    mock_module = MagicMock()
    mock_ansible_module.return_value = mock_module
    mock_module.check_mode = False
    mock_module.params = set_module_args(
        {
            "vm": "vm-1001",
            "state": "present",
            "upgrade_policy": "MANUAL",
        }
    )
    mock_module.exit_json.side_effect = exit_json

    mock_client.get.return_value = _response(200, TOOLS_INFO_MANUAL)

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_client.get.assert_called_once_with(TOOLS_PATH)
    mock_client.patch.assert_not_called()
    mock_module.exit_json.assert_called_once()
    assert exc.value.kwargs == {
        "changed": False,
        "value": TOOLS_INFO_MANUAL,
    }

@patch.object(module_under_test, "AnsibleModule")
@patch.object(module_under_test.VmwareRestCrudModule, "_create_client")
def test_update_without_upgrade_policy(
    mock_create_client, mock_ansible_module, mock_client
):
    # GET 200, empty UpdateSpec when upgrade_policy not set
    mock_create_client.return_value = mock_client
    mock_module = MagicMock()
    mock_ansible_module.return_value = mock_module
    mock_module.check_mode = False
    mock_module.params = set_module_args(
        {
            "vm": "vm-1001",
            "state": "present",
            "upgrade_policy": None,
        }
    )
    mock_module.exit_json.side_effect = exit_json

    mock_client.get.return_value = _response(200, TOOLS_INFO_MANUAL)

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_client.get.assert_called_once_with(TOOLS_PATH)
    mock_client.patch.assert_not_called()
    mock_module.exit_json.assert_called_once()
    assert exc.value.kwargs == {
        "changed": False,
        "value": TOOLS_INFO_MANUAL,
    }

@patch.object(module_under_test, "AnsibleModule")
@patch.object(module_under_test.VmwareRestCrudModule, "_create_client")
def test_vm_not_found(mock_create_client, mock_ansible_module, mock_client):
    # GET 404 — Vcenter.Vm.Tools_get, virtual machine not found
    mock_create_client.return_value = mock_client
    mock_module = MagicMock()
    mock_ansible_module.return_value = mock_module
    mock_module.check_mode = False
    mock_module.params = set_module_args(
        {
            "vm": "vm-missing",
            "state": "present",
            "upgrade_policy": "MANUAL",
        }
    )
    mock_module.fail_json.side_effect = fail_json

    mock_client.get.return_value = _response(404, None)

    with pytest.raises(AnsibleFailJson) as exc:
        module_under_test.main()

    mock_client.get.assert_called_once_with("/vcenter/vm/vm-missing/tools")
    mock_client.patch.assert_not_called()
    mock_module.fail_json.assert_called_once()
    assert exc.value.kwargs == {
        "msg": "Virtual machine not found: vm-missing",
    }
