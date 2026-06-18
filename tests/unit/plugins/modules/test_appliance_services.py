# -*- coding: utf-8 -*-
# Copyright: (c) 2026, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import pytest
from unittest.mock import patch, MagicMock

from ansible_collections.vmware.vmware_rest.plugins.modules import (
    appliance_services as module_under_test,
)
from ...common.utils import (
    AnsibleExitJson,
    exit_json,
    set_module_args,
    _response,
)

SERVICE_PATH = "/appliance/services/ntpd"
STOPPED_SERVICE = {"description": "ntpd.service", "state": "STOPPED"}
STARTED_SERVICE = {"description": "ntpd.service", "state": "STARTED"}


@patch.object(module_under_test, "AnsibleModule")
@patch.object(module_under_test.VmwareRestCrudModule, "_create_client")
def test_start_service(mock_create_client, mock_ansible_module, mock_client):
    mock_create_client.return_value = mock_client
    mock_module = MagicMock()
    mock_ansible_module.return_value = mock_module
    mock_module.check_mode = False
    mock_module.params = set_module_args({"service": "ntpd", "state": "start"})
    mock_module.exit_json.side_effect = exit_json

    mock_client.get.return_value = _response(200, STOPPED_SERVICE)
    mock_client.request.return_value = _response(204, None)

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_client.get.assert_called_once_with(SERVICE_PATH)
    mock_client.request.assert_called_once_with(
        "POST", SERVICE_PATH, query={"action": "start"}
    )
    assert exc.value.kwargs == {"changed": True}


@patch.object(module_under_test, "AnsibleModule")
@patch.object(module_under_test.VmwareRestCrudModule, "_create_client")
def test_start_already_started(mock_create_client, mock_ansible_module, mock_client):
    mock_create_client.return_value = mock_client
    mock_module = MagicMock()
    mock_ansible_module.return_value = mock_module
    mock_module.check_mode = False
    mock_module.params = set_module_args({"service": "ntpd", "state": "start"})
    mock_module.exit_json.side_effect = exit_json

    mock_client.get.return_value = _response(200, STARTED_SERVICE)

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_client.request.assert_not_called()
    assert exc.value.kwargs == {"changed": False, "value": STARTED_SERVICE}
