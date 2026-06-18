# -*- coding: utf-8 -*-
# Copyright: (c) 2026, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import pytest
from unittest.mock import patch, MagicMock

from ansible_collections.vmware.vmware_rest.plugins.modules import (
    appliance_monitoring_query as module_under_test,
)
from ...common.utils import (
    AnsibleExitJson,
    exit_json,
    set_module_args,
    _response,
)

QUERY_PARAMS = {
    "names": ["mem.total"],
    "interval": "MINUTES5",
    "function": "AVG",
    "start_time": "2024-10-30T00:00:00.000Z",
    "end_time": "2024-10-31T00:00:00.000Z",
}

QUERY_RESULT = [
    {
        "name": "mem.total",
        "interval": "MINUTES5",
        "function": "AVG",
        "start_time": "2024-10-30T00:00:00.000Z",
        "end_time": "2024-10-31T00:00:00.000Z",
        "data": ["1024", "2048"],
    },
]


@patch.object(module_under_test, "AnsibleModule")
@patch.object(module_under_test.VmwareRestQueryModule, "_create_client")
def test_query_monitoring_data(mock_create_client, mock_ansible_module, mock_client):
    # GET /appliance/monitoring/query — query, 200
    mock_create_client.return_value = mock_client
    mock_module = MagicMock()
    mock_ansible_module.return_value = mock_module
    mock_module.params = set_module_args(QUERY_PARAMS)
    mock_module.exit_json.side_effect = exit_json

    mock_client.get.return_value = _response(200, QUERY_RESULT)

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_client.get.assert_called_once_with(
        "/appliance/monitoring/query",
        query={
            "names": ["mem.total"],
            "interval": "MINUTES5",
            "function": "AVG",
            "start_time": "2024-10-30T00:00:00.000Z",
            "end_time": "2024-10-31T00:00:00.000Z",
        },
    )
    mock_module.exit_json.assert_called_once()
    assert exc.value.kwargs == {"value": QUERY_RESULT}


@patch.object(module_under_test, "AnsibleModule")
@patch.object(module_under_test.VmwareRestQueryModule, "_create_client")
def test_query_not_found(mock_create_client, mock_ansible_module, mock_client):
    mock_create_client.return_value = mock_client
    mock_module = MagicMock()
    mock_ansible_module.return_value = mock_module
    mock_module.params = set_module_args(QUERY_PARAMS)
    mock_module.exit_json.side_effect = exit_json

    mock_client.get.return_value = _response(404, None)

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_module.exit_json.assert_called_once()
    assert exc.value.kwargs == {"value": []}
