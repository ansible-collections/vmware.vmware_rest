# -*- coding: utf-8 -*-
# Copyright: (c) 2026, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import pytest
from unittest.mock import patch, MagicMock

from ansible_collections.vmware.vmware_rest.plugins.modules import (
    appliance_networking as module_under_test,
)
from ...common.utils import (
    AnsibleExitJson,
    exit_json,
    set_module_args,
    _response,
)

NETWORKING_PATH = "/appliance/networking"
NETWORKING_INFO = {
    "dns": {
        "mode": "STATIC",
        "hostname": "vcenter.example.com",
        "servers": ["192.168.1.1"],
    },
    "interfaces": {
        "nic0": {
            "mac": "00:0C:29:94:BB:5A",
            "name": "nic0",
            "status": "up",
        },
    },
}


@patch.object(module_under_test, "AnsibleModule")
@patch.object(module_under_test.VmwareRestModule, "_create_client")
def test_update_ipv6_enabled(mock_create_client, mock_ansible_module, mock_client):
    mock_create_client.return_value = mock_client
    mock_module = MagicMock()
    mock_ansible_module.return_value = mock_module
    mock_module.check_mode = False
    mock_module.params = set_module_args({"state": "present", "ipv6_enabled": False})
    mock_module.exit_json.side_effect = exit_json

    mock_client.patch.return_value = _response(204, None)
    mock_client.get.return_value = _response(200, NETWORKING_INFO)

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_client.patch.assert_called_once_with(
        NETWORKING_PATH, data={"ipv6_enabled": False}
    )
    assert mock_client.get.call_count == 2
    mock_client.get.assert_any_call(NETWORKING_PATH)
    assert exc.value.kwargs == {"changed": True, "value": NETWORKING_INFO}


@patch.object(module_under_test, "AnsibleModule")
@patch.object(module_under_test.VmwareRestModule, "_create_client")
def test_reset_networking(mock_create_client, mock_ansible_module, mock_client):
    mock_create_client.return_value = mock_client
    mock_module = MagicMock()
    mock_ansible_module.return_value = mock_module
    mock_module.check_mode = False
    mock_module.params = set_module_args({"state": "reset"})
    mock_module.exit_json.side_effect = exit_json

    mock_client.request.return_value = _response(204, None)

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_client.request.assert_called_once_with(
        "POST", NETWORKING_PATH, query={"action": "reset"}
    )
    assert exc.value.kwargs == {"changed": True}
