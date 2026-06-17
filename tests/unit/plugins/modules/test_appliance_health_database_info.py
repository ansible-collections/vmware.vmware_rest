# -*- coding: utf-8 -*-
# Copyright: (c) 2026, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import pytest
from unittest.mock import patch, MagicMock

from ansible_collections.vmware.vmware_rest.plugins.modules import (
    appliance_health_database_info as module_under_test,
)
from ...common.utils import (
    AnsibleExitJson,
    exit_json,
    mock_client,
    set_module_args,
    _response,
)

# GET /appliance/health/database — operationId get, 200 schema ApplianceHealthDatabaseInfo
DATABASE_HEALTH_HEALTHY = {
    "status": "HEALTHY",
    "messages": [],
}

DATABASE_HEALTH_DEGRADED = {
    "status": "DEGRADED",
    "messages": [
        {
            "severity": "WARNING",
            "message": {
                "id": "com.vmware.appliance.health.database.warning",
                "default_message": "Database issue detected",
                "args": [],
            },
        }
    ],
}

@patch.object(module_under_test, "AnsibleModule")
@patch.object(module_under_test.VmwareRestInfoModule, "_create_client")
def test_get_success_healthy(mock_create_client, mock_ansible_module, mock_client):
    mock_create_client.return_value = mock_client
    mock_module = MagicMock()
    mock_ansible_module.return_value = mock_module
    mock_module.params = set_module_args({})
    mock_module.exit_json.side_effect = exit_json

    mock_client.get.return_value = _response(200, DATABASE_HEALTH_HEALTHY)

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_client.get.assert_called_once_with("/appliance/health/database")
    mock_module.exit_json.assert_called_once()
    assert exc.value.kwargs == {"value": DATABASE_HEALTH_HEALTHY}

@patch.object(module_under_test, "AnsibleModule")
@patch.object(module_under_test.VmwareRestInfoModule, "_create_client")
def test_get_success_degraded_with_messages(
    mock_create_client, mock_ansible_module, mock_client
):
    mock_create_client.return_value = mock_client
    mock_module = MagicMock()
    mock_ansible_module.return_value = mock_module
    mock_module.params = set_module_args({})
    mock_module.exit_json.side_effect = exit_json

    mock_client.get.return_value = _response(200, DATABASE_HEALTH_DEGRADED)

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_client.get.assert_called_once_with("/appliance/health/database")
    mock_module.exit_json.assert_called_once()
    assert exc.value.kwargs == {"value": DATABASE_HEALTH_DEGRADED}

@patch.object(module_under_test, "AnsibleModule")
@patch.object(module_under_test.VmwareRestInfoModule, "_create_client")
def test_get_not_found(mock_create_client, mock_ansible_module, mock_client):
    mock_create_client.return_value = mock_client
    mock_module = MagicMock()
    mock_ansible_module.return_value = mock_module
    mock_module.params = set_module_args({})
    mock_module.exit_json.side_effect = exit_json

    mock_client.get.return_value = _response(404, None)

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_client.get.assert_called_once_with("/appliance/health/database")
    mock_module.exit_json.assert_called_once()
    assert exc.value.kwargs == {"value": {}}
