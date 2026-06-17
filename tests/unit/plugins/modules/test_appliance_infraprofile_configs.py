# -*- coding: utf-8 -*-
# Copyright: (c) 2026, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import pytest
from unittest.mock import patch, MagicMock

from ansible_collections.vmware.vmware_rest.plugins.modules import (
    appliance_infraprofile_configs as module_under_test,
)
from ...common.utils import (
    AnsibleExitJson,
    exit_json,
    mock_client,
    set_module_args,
    _response,
)

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
