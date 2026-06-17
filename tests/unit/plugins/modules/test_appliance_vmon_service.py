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
    appliance_vmon_service as module_under_test,
)


class AnsibleExitJson(Exception):
    def __init__(self, kwargs):
        self.kwargs = kwargs


def exit_json(*args, **kwargs):
    if args:
        kwargs.update(args[0])
    raise AnsibleExitJson(kwargs)


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

SERVICE_PATH = "/rest/appliance/vmon/service/vpxd"
START_PATH = "/rest/appliance/vmon/service/vpxd/start"
STOPPED_SERVICE = {
    "value": {
        "name_key": "cis.vpxd.ServiceName",
        "description_key": "cis.vpxd.ServiceDescription",
        "startup_type": "MANUAL",
        "state": "STOPPED",
    }
}
STARTED_SERVICE = {
    "value": {
        "name_key": "cis.vpxd.ServiceName",
        "description_key": "cis.vpxd.ServiceDescription",
        "startup_type": "AUTOMATIC",
        "state": "STARTED",
    }
}


@pytest.fixture
def mock_client():
    return MagicMock()


def set_module_args(args):
    return {**CONNECTION_PARAMS, **args}


@patch.object(module_under_test, "AnsibleModule")
@patch.object(module_under_test.VmwareRestCrudModule, "_create_client")
def test_start_service(mock_create_client, mock_ansible_module, mock_client):
    mock_create_client.return_value = mock_client
    mock_module = MagicMock()
    mock_ansible_module.return_value = mock_module
    mock_module.check_mode = False
    mock_module.params = set_module_args({"service": "vpxd", "state": "start"})
    mock_module.exit_json.side_effect = exit_json

    mock_client.get.return_value = _response(200, STOPPED_SERVICE)
    mock_client.request.return_value = _response(200, None)

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_client.get.assert_called_once_with(SERVICE_PATH)
    mock_client.request.assert_called_once_with("POST", START_PATH)
    assert exc.value.kwargs == {"changed": True}


@patch.object(module_under_test, "AnsibleModule")
@patch.object(module_under_test.VmwareRestCrudModule, "_create_client")
def test_start_already_started(mock_create_client, mock_ansible_module, mock_client):
    mock_create_client.return_value = mock_client
    mock_module = MagicMock()
    mock_ansible_module.return_value = mock_module
    mock_module.check_mode = False
    mock_module.params = set_module_args({"service": "vpxd", "state": "start"})
    mock_module.exit_json.side_effect = exit_json

    mock_client.get.return_value = _response(200, STARTED_SERVICE)

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_client.request.assert_not_called()
    assert exc.value.kwargs == {
        "changed": False,
        "value": STARTED_SERVICE["value"],
    }


@patch.object(module_under_test, "AnsibleModule")
@patch.object(module_under_test.VmwareRestCrudModule, "_create_client")
def test_update_startup_type(mock_create_client, mock_ansible_module, mock_client):
    mock_create_client.return_value = mock_client
    mock_module = MagicMock()
    mock_ansible_module.return_value = mock_module
    mock_module.check_mode = False
    mock_module.params = set_module_args(
        {
            "service": "vpxd",
            "state": "present",
            "startup_type": "AUTOMATIC",
        }
    )
    mock_module.exit_json.side_effect = exit_json

    mock_client.get.side_effect = [
        _response(200, STOPPED_SERVICE),
        _response(200, STARTED_SERVICE),
    ]
    mock_client.patch.return_value = _response(200, None)

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_client.patch.assert_called_once_with(
        SERVICE_PATH,
        data={"spec": {"startup_type": "AUTOMATIC"}},
    )
    assert exc.value.kwargs == {
        "changed": True,
        "value": STARTED_SERVICE["value"],
    }


@patch.object(module_under_test, "AnsibleModule")
@patch.object(module_under_test.VmwareRestCrudModule, "_create_client")
def test_present_no_change(mock_create_client, mock_ansible_module, mock_client):
    mock_create_client.return_value = mock_client
    mock_module = MagicMock()
    mock_ansible_module.return_value = mock_module
    mock_module.check_mode = False
    mock_module.params = set_module_args(
        {
            "service": "vpxd",
            "state": "present",
            "startup_type": "AUTOMATIC",
        }
    )
    mock_module.exit_json.side_effect = exit_json

    mock_client.get.return_value = _response(200, STARTED_SERVICE)

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_client.patch.assert_not_called()
    assert exc.value.kwargs == {
        "changed": False,
        "value": STARTED_SERVICE["value"],
    }
