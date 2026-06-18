# -*- coding: utf-8 -*-
# Copyright: (c) 2026, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import pytest
from unittest.mock import patch, MagicMock

from ansible_collections.vmware.vmware_rest.plugins.modules import (
    appliance_services_info as module_under_test,
)
from ...common.utils import (
    AnsibleExitJson,
    exit_json,
    set_module_args,
    _response,
)

LIST_PATH = "/appliance/services"
SERVICE_PATH = "/appliance/services/ntpd"

SERVICES_MAP = {
    "ntpd": {"description": "ntpd.service", "state": "STARTED"},
    "vpxd": {"description": "vpxd.service", "state": "STARTED"},
}

NTPD_INFO = {"description": "ntpd.service", "state": "STARTED", "id": "ntpd"}


@patch.object(module_under_test, "AnsibleModule")
@patch.object(module_under_test.VmwareRestInfoModule, "_create_client")
def test_list_services(mock_create_client, mock_ansible_module, mock_client):
    mock_create_client.return_value = mock_client
    mock_module = MagicMock()
    mock_ansible_module.return_value = mock_module
    mock_module.params = set_module_args({})
    mock_module.exit_json.side_effect = exit_json

    mock_client.get.return_value = _response(200, SERVICES_MAP)

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_client.get.assert_called_once_with(LIST_PATH)
    result = exc.value.kwargs["value"]
    assert len(result) == 2
    assert result[0]["id"] in ("ntpd", "vpxd")


@patch.object(module_under_test, "AnsibleModule")
@patch.object(module_under_test.VmwareRestInfoModule, "_create_client")
def test_get_service(mock_create_client, mock_ansible_module, mock_client):
    mock_create_client.return_value = mock_client
    mock_module = MagicMock()
    mock_ansible_module.return_value = mock_module
    mock_module.params = set_module_args({"service": "ntpd"})
    mock_module.exit_json.side_effect = exit_json

    mock_client.get.return_value = _response(
        200, {"description": "ntpd.service", "state": "STARTED"}
    )

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_client.get.assert_called_once_with(SERVICE_PATH)
    assert exc.value.kwargs == {"value": NTPD_INFO}
