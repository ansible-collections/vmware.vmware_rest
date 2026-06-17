# -*- coding: utf-8 -*-
# Copyright: (c) 2026, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import pytest
from unittest.mock import patch, MagicMock

from ansible_collections.vmware.vmware_rest.plugins.modules import (
    content_subscribedlibrary_info as module_under_test,
)
from ...common.utils import (
    AnsibleExitJson,
    exit_json,
    mock_client,
    set_module_args,
    _response,
)

API_PATH = "/content/subscribed-library"
SAMPLE_BODY = [
    {
        "creation_time": "2024-01-01T00:00:00.000Z",
        "description": "Example subscribed library",
        "id": "subscribed-library-id",
        "last_modified_time": "2024-01-02T00:00:00.000Z",
        "name": "example-subscribed-library",
        "type": "SUBSCRIBED",
    }
]

@patch.object(module_under_test, "AnsibleModule")
@patch.object(module_under_test.VmwareRestInfoModule, "_create_client")
def test_get_success(mock_create_client, mock_ansible_module, mock_client):
    mock_create_client.return_value = mock_client
    mock_module = MagicMock()
    mock_ansible_module.return_value = mock_module
    mock_module.params = set_module_args({})
    mock_module.exit_json.side_effect = exit_json
    mock_client.get.side_effect = [
        _response(200, ["lib-1"]),
        _response(200, {"name": "my-lib", "type": "LOCAL"}),
    ]
    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()
    assert exc.value.kwargs["value"][0]["id"] == "lib-1"

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
    assert exc.value.kwargs == {"value": []}
