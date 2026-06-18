# -*- coding: utf-8 -*-
# Copyright: (c) 2026, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import pytest
from unittest.mock import patch, MagicMock

from ansible_collections.vmware.vmware_rest.plugins.modules import (
    vcenter_vm_tools_installer as module_under_test,
)
from ...common.utils import (
    AnsibleExitJson,
    exit_json,
    set_module_args,
    _response,
)

VM_MOID = "vm-1009"
INSTALLER_PATH = "/vcenter/vm/{0}/tools/installer".format(VM_MOID)


@patch.object(module_under_test, "AnsibleModule")
@patch.object(module_under_test.VmwareRestCrudModule, "_create_client")
def test_connect_already_connected(
    mock_create_client, mock_ansible_module, mock_client
):
    # GET Vcenter.Vm.Tools.Installer_get — 200, installer already connected
    mock_create_client.return_value = mock_client
    mock_module = MagicMock()
    mock_ansible_module.return_value = mock_module
    mock_module.check_mode = False
    mock_module.params = set_module_args({"vm": VM_MOID, "state": "present"})
    mock_module.exit_json.side_effect = exit_json

    mock_client.get.return_value = _response(200, {"is_connected": True})

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_client.get.assert_called_once_with(INSTALLER_PATH)
    mock_client.request.assert_not_called()
    assert exc.value.kwargs == {
        "changed": False,
        "value": {"is_connected": True},
    }


@patch.object(module_under_test, "AnsibleModule")
@patch.object(module_under_test.VmwareRestCrudModule, "_create_client")
def test_connect_success(mock_create_client, mock_ansible_module, mock_client):
    # GET Vcenter.Vm.Tools.Installer_get — 200, then POST connect — 204
    mock_create_client.return_value = mock_client
    mock_module = MagicMock()
    mock_ansible_module.return_value = mock_module
    mock_module.check_mode = False
    mock_module.params = set_module_args({"vm": VM_MOID, "state": "present"})
    mock_module.exit_json.side_effect = exit_json

    mock_client.get.return_value = _response(200, {"is_connected": False})
    mock_client.request.return_value = _response(204, None)

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_client.get.assert_called_once_with(INSTALLER_PATH)
    mock_client.request.assert_called_once_with(
        "POST",
        INSTALLER_PATH,
        query={"action": "connect"},
    )
    assert exc.value.kwargs == {"changed": True}


@patch.object(module_under_test, "AnsibleModule")
@patch.object(module_under_test.VmwareRestCrudModule, "_create_client")
def test_disconnect_already_disconnected(
    mock_create_client, mock_ansible_module, mock_client
):
    # GET Vcenter.Vm.Tools.Installer_get — 200, installer already disconnected
    mock_create_client.return_value = mock_client
    mock_module = MagicMock()
    mock_ansible_module.return_value = mock_module
    mock_module.check_mode = False
    mock_module.params = set_module_args({"vm": VM_MOID, "state": "absent"})
    mock_module.exit_json.side_effect = exit_json

    mock_client.get.return_value = _response(200, {"is_connected": False})

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_client.get.assert_called_once_with(INSTALLER_PATH)
    mock_client.request.assert_not_called()
    assert exc.value.kwargs == {
        "changed": False,
        "value": {"is_connected": False},
    }


@patch.object(module_under_test, "AnsibleModule")
@patch.object(module_under_test.VmwareRestCrudModule, "_create_client")
def test_disconnect_success(mock_create_client, mock_ansible_module, mock_client):
    # GET Vcenter.Vm.Tools.Installer_get — 200, then POST disconnect — 204
    mock_create_client.return_value = mock_client
    mock_module = MagicMock()
    mock_ansible_module.return_value = mock_module
    mock_module.check_mode = False
    mock_module.params = set_module_args({"vm": VM_MOID, "state": "absent"})
    mock_module.exit_json.side_effect = exit_json

    mock_client.get.return_value = _response(200, {"is_connected": True})
    mock_client.request.return_value = _response(204, None)

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_client.get.assert_called_once_with(INSTALLER_PATH)
    mock_client.request.assert_called_once_with(
        "POST",
        INSTALLER_PATH,
        query={"action": "disconnect"},
    )
    assert exc.value.kwargs == {"changed": True}
