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
    appliance_networking_interfaces_ipv6 as module_under_test,
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

IPV6_PATH = "/appliance/networking/interfaces/nic0/ipv6"

CURRENT_AUTOCONF = {
    "dhcp": False,
    "autoconf": False,
    "addresses": [],
    "default_gateway": "",
    "configurable": True,
}

UPDATED_AUTOCONF = {
    "dhcp": False,
    "autoconf": True,
    "addresses": [],
    "default_gateway": "",
    "configurable": True,
}

DEFAULT_PARAMS = {
    "state": "present",
    "dhcp": None,
    "autoconf": None,
    "addresses": None,
    "default_gateway": None,
}


@pytest.fixture
def mock_client():
    return MagicMock()


def set_module_args(args):
    return {**CONNECTION_PARAMS, **DEFAULT_PARAMS, **args}


@patch.object(module_under_test, "AnsibleModule")
@patch.object(module_under_test.VmwareRestCrudModule, "_create_client")
def test_enable_autoconf(mock_create_client, mock_ansible_module, mock_client):
    mock_create_client.return_value = mock_client
    mock_module = MagicMock()
    mock_ansible_module.return_value = mock_module
    mock_module.check_mode = False
    mock_module.params = set_module_args(
        {
            "interface_name": "nic0",
            "autoconf": True,
            "dhcp": False,
            "addresses": [],
            "default_gateway": "",
        }
    )
    mock_module.exit_json.side_effect = exit_json

    mock_client.get.side_effect = [
        _response(200, CURRENT_AUTOCONF),
        _response(200, UPDATED_AUTOCONF),
    ]
    mock_client.put.return_value = _response(200, None)

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_client.get.assert_has_calls([call(IPV6_PATH), call(IPV6_PATH)])
    mock_client.put.assert_called_once_with(
        IPV6_PATH,
        data={
            "dhcp": False,
            "autoconf": True,
            "addresses": [],
            "default_gateway": "",
        },
    )
    assert exc.value.kwargs == {"changed": True, "value": UPDATED_AUTOCONF}


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
            "autoconf": True,
            "dhcp": False,
            "addresses": [],
            "default_gateway": "",
        }
    )
    mock_module.exit_json.side_effect = exit_json

    mock_client.get.return_value = _response(200, UPDATED_AUTOCONF)

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_client.get.assert_called_once_with(IPV6_PATH)
    mock_client.put.assert_not_called()
    assert exc.value.kwargs == {"changed": False, "value": UPDATED_AUTOCONF}


@patch.object(module_under_test, "AnsibleModule")
@patch.object(module_under_test.VmwareRestCrudModule, "_create_client")
def test_interface_not_found(mock_create_client, mock_ansible_module, mock_client):
    mock_create_client.return_value = mock_client
    mock_module = MagicMock()
    mock_ansible_module.return_value = mock_module
    mock_module.check_mode = False
    mock_module.params = set_module_args({"interface_name": "nic0", "autoconf": True})
    mock_module.fail_json.side_effect = fail_json

    mock_client.get.return_value = _response(404, None)

    with pytest.raises(AnsibleFailJson) as exc:
        module_under_test.main()

    assert "Network interface not found" in exc.value.kwargs["msg"]
