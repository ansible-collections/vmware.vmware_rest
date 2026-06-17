# -*- coding: utf-8 -*-
# Copyright: (c) 2026, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import pytest
from unittest.mock import patch, MagicMock

from ansible_collections.vmware.vmware_rest.plugins.modules import (
    vcenter_vm_tools_info as module_under_test,
)
from ...common.utils import (
    AnsibleExitJson,
    exit_json,
    mock_client,
    set_module_args,
    _response,
)

# components/schemas/Vcenter.Vm.Tools.Info (required: auto_update_supported, run_state, upgrade_policy)
TOOLS_INFO = {
    "auto_update_supported": True,
    "run_state": "RUNNING",
    "upgrade_policy": "MANUAL",
    "version_status": "CURRENT",
    "version": "12.1.5",
    "version_number": 12389,
    "install_type": "OPEN_VM_TOOLS",
    "guest_reboot_status": {
        "reboot_requested": False,
    },
}

@patch.object(module_under_test, "AnsibleModule")
@patch.object(module_under_test.VmwareRestInfoModule, "_create_client")
def test_get_success(mock_create_client, mock_ansible_module, mock_client):
    # GET /vcenter/vm/{vm}/tools — Vcenter.Vm.Tools_get, 200 Vcenter.Vm.Tools.Info
    mock_create_client.return_value = mock_client
    mock_module = MagicMock()
    mock_ansible_module.return_value = mock_module
    mock_module.params = set_module_args({"vm": "vm-1001"})
    mock_module.exit_json.side_effect = exit_json

    mock_client.get.return_value = _response(200, TOOLS_INFO)

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_client.get.assert_called_once_with("/vcenter/vm/vm-1001/tools")
    mock_module.exit_json.assert_called_once()
    assert exc.value.kwargs == {"value": TOOLS_INFO}

@patch.object(module_under_test, "AnsibleModule")
@patch.object(module_under_test.VmwareRestInfoModule, "_create_client")
def test_get_not_found(mock_create_client, mock_ansible_module, mock_client):
    # GET /vcenter/vm/{vm}/tools — Vcenter.Vm.Tools_get, 404 NotFound
    mock_create_client.return_value = mock_client
    mock_module = MagicMock()
    mock_ansible_module.return_value = mock_module
    mock_module.params = set_module_args({"vm": "vm-missing"})
    mock_module.exit_json.side_effect = exit_json

    mock_client.get.return_value = _response(404, None)

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_client.get.assert_called_once_with("/vcenter/vm/vm-missing/tools")
    mock_module.exit_json.assert_called_once()
    assert exc.value.kwargs == {"value": {}}
