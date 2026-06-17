# -*- coding: utf-8 -*-
# Copyright: (c) 2026, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import json
import pytest
from unittest.mock import patch, MagicMock, call

from ansible_collections.vmware.vmware_rest.plugins.module_utils._client import (
    Response,
)
from ansible_collections.vmware.vmware_rest.plugins.modules import (
    appliance_localaccounts_globalpolicy as module_under_test,
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
    "vcenter_port": None,
    "vcenter_validate_certs": False,
    "vcenter_rest_log_file": None,
    "session_timeout": None,
}

PATH = "/appliance/local-accounts/global-policy"

CURRENT_POLICY = {
    "max_days": 90,
    "min_days": 1,
    "warn_days": 7,
    "minimum_length": 8,
}

UPDATED_POLICY = {
    "max_days": 90,
    "min_days": 1,
    "warn_days": 5,
    "minimum_length": 8,
}

DEFAULT_PARAMS = {
    "state": "present",
    "max_days": None,
    "min_days": None,
    "warn_days": None,
    "prior_password_remember_count": None,
    "failed_attempt_count_before_account_lockout": None,
    "length_of_lockout_period_in_seconds": None,
    "fail_interval_between_attempts": None,
    "minimum_length": None,
    "minimum_uppercase_char_count": None,
    "minimum_lowercase_char_count": None,
    "minimum_numerics_char_count": None,
    "minimum_special_char_count": None,
}


@pytest.fixture
def mock_client():
    return MagicMock()


def set_module_args(args):
    return {**CONNECTION_PARAMS, **DEFAULT_PARAMS, **args}


@patch.object(module_under_test, "AnsibleModule")
@patch.object(module_under_test.VmwareRestCrudModule, "_create_client")
def test_update_warn_days(mock_create_client, mock_ansible_module, mock_client):
    # PUT /appliance/local-accounts/global-policy — set, 204
    mock_create_client.return_value = mock_client
    mock_module = MagicMock()
    mock_ansible_module.return_value = mock_module
    mock_module.check_mode = False
    mock_module.params = set_module_args({"warn_days": 5})
    mock_module.exit_json.side_effect = exit_json

    mock_client.get.side_effect = [
        _response(200, CURRENT_POLICY),
        _response(200, UPDATED_POLICY),
    ]
    mock_client.request.return_value = _response(204, None)

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_client.get.assert_has_calls([call(PATH), call(PATH)])
    mock_client.request.assert_called_once_with("PUT", PATH, data={"warn_days": 5})
    mock_module.exit_json.assert_called_once()
    assert exc.value.kwargs == {"changed": True, "value": UPDATED_POLICY}


@patch.object(module_under_test, "AnsibleModule")
@patch.object(module_under_test.VmwareRestCrudModule, "_create_client")
def test_no_change_idempotent(mock_create_client, mock_ansible_module, mock_client):
    mock_create_client.return_value = mock_client
    mock_module = MagicMock()
    mock_ansible_module.return_value = mock_module
    mock_module.check_mode = False
    mock_module.params = set_module_args({"warn_days": 7})
    mock_module.exit_json.side_effect = exit_json

    mock_client.get.return_value = _response(200, CURRENT_POLICY)

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_client.get.assert_called_once_with(PATH)
    mock_client.request.assert_not_called()
    mock_module.exit_json.assert_called_once()
    assert exc.value.kwargs == {"changed": False, "value": CURRENT_POLICY}


@patch.object(module_under_test, "AnsibleModule")
@patch.object(module_under_test.VmwareRestCrudModule, "_create_client")
def test_no_params_specified(mock_create_client, mock_ansible_module, mock_client):
    mock_create_client.return_value = mock_client
    mock_module = MagicMock()
    mock_ansible_module.return_value = mock_module
    mock_module.check_mode = False
    mock_module.params = set_module_args({})
    mock_module.exit_json.side_effect = exit_json

    mock_client.get.return_value = _response(200, CURRENT_POLICY)

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_client.get.assert_called_once_with(PATH)
    mock_client.request.assert_not_called()
    mock_module.exit_json.assert_called_once()
    assert exc.value.kwargs == {"changed": False, "value": CURRENT_POLICY}
