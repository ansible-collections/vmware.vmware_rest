# -*- coding: utf-8 -*-
# Copyright: (c) 2026, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import json
import pytest
from unittest.mock import patch, MagicMock

from ansible_collections.vmware.vmware_rest.plugins.module_utils._client import (
    Response,
)
from ansible_collections.vmware.vmware_rest.plugins.modules import (
    appliance_infraprofile_configs as module_under_test,
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

# POST /appliance/infraprofile/configs?action=export — export, 200 JSON string
EXPORT_JSON_STRING = (
    '{"action":"RESTART_SERVICE","productName":"VMware vCenter Server",'
    '"profiles":{"ApplianceManagement":{"name":"ApplianceManagement"}}}'
)
EXPORT_PARSED = {
    "action": "RESTART_SERVICE",
    "productName": "VMware vCenter Server",
    "profiles": {"ApplianceManagement": {"name": "ApplianceManagement"}},
}


@pytest.fixture
def mock_client():
    return MagicMock()


def set_module_args(args):
    return {**CONNECTION_PARAMS, **args}


@patch.object(module_under_test, "AnsibleModule")
@patch.object(module_under_test.VmwareRestModule, "_create_client")
def test_export_profiles(mock_create_client, mock_ansible_module, mock_client):
    mock_create_client.return_value = mock_client
    mock_module = MagicMock()
    mock_ansible_module.return_value = mock_module
    mock_module.params = set_module_args(
        {
            "state": "export",
            "profiles": ["ApplianceManagement"],
            "description": None,
            "encryption_key": None,
        }
    )
    mock_module.exit_json.side_effect = exit_json

    mock_client.post.return_value = _response(200, EXPORT_JSON_STRING)

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_client.post.assert_called_once_with(
        "/appliance/infraprofile/configs",
        data={"profiles": ["ApplianceManagement"]},
        query={"action": "export"},
    )
    mock_module.exit_json.assert_called_once()
    assert exc.value.kwargs == {"changed": True, "value": EXPORT_PARSED}


@patch.object(module_under_test, "AnsibleModule")
@patch.object(module_under_test.VmwareRestModule, "_create_client")
def test_export_all_profiles(mock_create_client, mock_ansible_module, mock_client):
    mock_create_client.return_value = mock_client
    mock_module = MagicMock()
    mock_ansible_module.return_value = mock_module
    mock_module.params = set_module_args(
        {
            "state": "export",
            "profiles": None,
            "description": None,
            "encryption_key": None,
        }
    )
    mock_module.exit_json.side_effect = exit_json

    mock_client.post.return_value = _response(200, EXPORT_JSON_STRING)

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_client.post.assert_called_once_with(
        "/appliance/infraprofile/configs",
        data={},
        query={"action": "export"},
    )
    mock_module.exit_json.assert_called_once()
    assert exc.value.kwargs == {"changed": True, "value": EXPORT_PARSED}
