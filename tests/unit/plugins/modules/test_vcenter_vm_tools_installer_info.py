# -*- coding: utf-8 -*-
# Copyright: (c) 2026, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import pytest
from unittest.mock import patch, MagicMock

from ansible_collections.vmware.vmware_rest.plugins.modules import (
    vcenter_vm_tools_installer_info as module_under_test,
)
from ...common.utils import (
    AnsibleExitJson,
    exit_json,
    set_module_args,
    _response,
)

VM_MOID = "vm-1009"
INSTALLER_PATH = "/vcenter/vm/{0}/tools/installer".format(VM_MOID)


@pytest.fixture
def module_args():
    return {"vm": VM_MOID}


@patch.object(module_under_test, "AnsibleModule")
@patch.object(module_under_test.VmwareRestInfoModule, "_create_client")
def test_get_installer_connected(
    mock_create_client, mock_ansible_module, mock_client, module_args
):
    # GET /vcenter/vm/{vm}/tools/installer — Vcenter.Vm.Tools.Installer_get — 200
    mock_create_client.return_value = mock_client
    mock_module = MagicMock()
    mock_ansible_module.return_value = mock_module
    mock_module.params = set_module_args(module_args)
    mock_module.exit_json.side_effect = exit_json

    mock_client.get.return_value = _response(200, {"is_connected": True})

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_client.get.assert_called_once_with(INSTALLER_PATH)
    mock_module.exit_json.assert_called_once()
    assert exc.value.kwargs == {"value": {"is_connected": True}}


@patch.object(module_under_test, "AnsibleModule")
@patch.object(module_under_test.VmwareRestInfoModule, "_create_client")
def test_get_installer_not_connected(
    mock_create_client, mock_ansible_module, mock_client, module_args
):
    # GET /vcenter/vm/{vm}/tools/installer — Vcenter.Vm.Tools.Installer_get — 200
    mock_create_client.return_value = mock_client
    mock_module = MagicMock()
    mock_ansible_module.return_value = mock_module
    mock_module.params = set_module_args(module_args)
    mock_module.exit_json.side_effect = exit_json

    mock_client.get.return_value = _response(200, {"is_connected": False})

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_client.get.assert_called_once_with(INSTALLER_PATH)
    assert exc.value.kwargs == {"value": {"is_connected": False}}


@patch.object(module_under_test, "AnsibleModule")
@patch.object(module_under_test.VmwareRestInfoModule, "_create_client")
def test_get_installer_not_found(
    mock_create_client, mock_ansible_module, mock_client, module_args
):
    # GET /vcenter/vm/{vm}/tools/installer — Vcenter.Vm.Tools.Installer_get — 404
    mock_create_client.return_value = mock_client
    mock_module = MagicMock()
    mock_ansible_module.return_value = mock_module
    mock_module.params = set_module_args(module_args)
    mock_module.exit_json.side_effect = exit_json

    mock_client.get.return_value = _response(404, {"error_type": "NOT_FOUND"})

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_client.get.assert_called_once_with(INSTALLER_PATH)
    assert exc.value.kwargs == {"value": {}}
