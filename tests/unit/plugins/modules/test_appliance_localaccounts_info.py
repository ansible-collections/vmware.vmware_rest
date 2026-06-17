# -*- coding: utf-8 -*-
# Copyright: (c) 2026, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import pytest
from unittest.mock import patch, MagicMock, call

from ansible_collections.vmware.vmware_rest.plugins.modules import (
    appliance_localaccounts_info as module_under_test,
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

ROOT_ACCOUNT = {
    "enabled": True,
    "fullname": "root",
    "has_password": True,
    "roles": ["superAdmin"],
}

ADMIN_ACCOUNT = {
    "enabled": True,
    "fullname": "Administrator",
    "has_password": True,
    "roles": ["admin"],
}

@patch.object(module_under_test, "AnsibleModule")
@patch.object(module_under_test.VmwareRestInfoModule, "_create_client")
def test_list_accounts(mock_create_client, mock_ansible_module, mock_client):
    # GET /appliance/local-accounts — list; GET /appliance/local-accounts/{username} — get
    mock_create_client.return_value = mock_client
    mock_module = MagicMock()
    mock_ansible_module.return_value = mock_module
    mock_module.params = set_module_args({"username": None})
    mock_module.exit_json.side_effect = exit_json

    mock_client.get.side_effect = [
        _response(200, ["root", "admin"]),
        _response(200, ROOT_ACCOUNT),
        _response(200, ADMIN_ACCOUNT),
    ]

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_client.get.assert_has_calls(
        [
            call("/appliance/local-accounts", query=None),
            call("/appliance/local-accounts/root"),
            call("/appliance/local-accounts/admin"),
        ]
    )
    mock_module.exit_json.assert_called_once()
    assert exc.value.kwargs == {
        "value": [
            dict(ROOT_ACCOUNT, username="root"),
            dict(ADMIN_ACCOUNT, username="admin"),
        ],
    }

@patch.object(module_under_test, "AnsibleModule")
@patch.object(module_under_test.VmwareRestInfoModule, "_create_client")
def test_get_single_account(mock_create_client, mock_ansible_module, mock_client):
    mock_create_client.return_value = mock_client
    mock_module = MagicMock()
    mock_ansible_module.return_value = mock_module
    mock_module.params = set_module_args({"username": "root"})
    mock_module.exit_json.side_effect = exit_json

    mock_client.get.return_value = _response(200, ROOT_ACCOUNT)

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_client.get.assert_called_once_with("/appliance/local-accounts/root")
    mock_module.exit_json.assert_called_once()
    assert exc.value.kwargs == {"value": dict(ROOT_ACCOUNT, username="root")}

@patch.object(module_under_test, "AnsibleModule")
@patch.object(module_under_test.VmwareRestInfoModule, "_create_client")
def test_get_account_not_found(mock_create_client, mock_ansible_module, mock_client):
    mock_create_client.return_value = mock_client
    mock_module = MagicMock()
    mock_ansible_module.return_value = mock_module
    mock_module.params = set_module_args({"username": "missing"})
    mock_module.fail_json.side_effect = fail_json

    mock_client.get.return_value = _response(404, None)

    with pytest.raises(AnsibleFailJson) as exc:
        module_under_test.main()

    mock_client.get.assert_called_once_with("/appliance/local-accounts/missing")
    mock_module.fail_json.assert_called_once()
    assert "Local account not found" in exc.value.kwargs["msg"]
