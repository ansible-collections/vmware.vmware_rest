# -*- coding: utf-8 -*-
# Copyright: (c) 2026, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import pytest
from unittest.mock import patch, MagicMock, call

from ansible_collections.vmware.vmware_rest.plugins.modules import (
    appliance_networking_interfaces_ipv4 as module_under_test,
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

IPV4_PATH = "/appliance/networking/interfaces/nic0/ipv4"

CURRENT_STATIC = {
    "configurable": True,
    "mode": "STATIC",
    "address": "10.20.80.191",
    "prefix": 24,
    "default_gateway": "10.20.80.1",
}

UPDATED_DHCP = {
    "configurable": True,
    "mode": "DHCP",
}

DEFAULT_PARAMS = {
    "state": "present",
    "mode": None,
    "address": None,
    "prefix": None,
    "default_gateway": None,
}

@patch.object(module_under_test, "AnsibleModule")
@patch.object(module_under_test.VmwareRestCrudModule, "_create_client")
def test_update_mode_to_dhcp(mock_create_client, mock_ansible_module, mock_client):
    mock_create_client.return_value = mock_client
    mock_module = MagicMock()
    mock_ansible_module.return_value = mock_module
    mock_module.check_mode = False
    mock_module.params = set_module_args({"interface_name": "nic0", "mode": "DHCP"})
    mock_module.exit_json.side_effect = exit_json

    mock_client.get.side_effect = [
        _response(200, CURRENT_STATIC),
        _response(200, UPDATED_DHCP),
    ]
    mock_client.request.return_value = _response(200, None)

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_client.get.assert_has_calls([call(IPV4_PATH), call(IPV4_PATH)])
    mock_client.request.assert_called_once_with("PUT", IPV4_PATH, data={"mode": "DHCP"})
    assert exc.value.kwargs == {"changed": True, "value": UPDATED_DHCP}

@patch.object(module_under_test, "AnsibleModule")
@patch.object(module_under_test.VmwareRestCrudModule, "_create_client")
def test_no_change_idempotent(mock_create_client, mock_ansible_module, mock_client):
    mock_create_client.return_value = mock_client
    mock_module = MagicMock()
    mock_ansible_module.return_value = mock_module
    mock_module.check_mode = False
    mock_module.params = set_module_args(
        {
            "interface_name": "nic0",
            "mode": "STATIC",
            "address": "10.20.80.191",
            "prefix": 24,
            "default_gateway": "10.20.80.1",
        }
    )
    mock_module.exit_json.side_effect = exit_json

    mock_client.get.return_value = _response(200, CURRENT_STATIC)

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_client.get.assert_called_once_with(IPV4_PATH)
    mock_client.request.assert_not_called()
    assert exc.value.kwargs == {"changed": False, "value": CURRENT_STATIC}

@patch.object(module_under_test, "AnsibleModule")
@patch.object(module_under_test.VmwareRestCrudModule, "_create_client")
def test_interface_not_found(mock_create_client, mock_ansible_module, mock_client):
    mock_create_client.return_value = mock_client
    mock_module = MagicMock()
    mock_ansible_module.return_value = mock_module
    mock_module.check_mode = False
    mock_module.params = set_module_args({"interface_name": "nic0", "mode": "DHCP"})
    mock_module.fail_json.side_effect = fail_json

    mock_client.get.return_value = _response(404, None)

    with pytest.raises(AnsibleFailJson) as exc:
        module_under_test.main()

    assert "Network interface not found" in exc.value.kwargs["msg"]
