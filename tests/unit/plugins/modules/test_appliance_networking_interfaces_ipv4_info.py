# -*- coding: utf-8 -*-
# Copyright: (c) 2026, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import pytest
from unittest.mock import patch, MagicMock

from ansible_collections.vmware.vmware_rest.plugins.modules import (
    appliance_networking_interfaces_ipv4_info as module_under_test,
)
from ...common.utils import (
    AnsibleExitJson,
    exit_json,
    set_module_args,
    _response,
)

IPV4_PATH = "/appliance/networking/interfaces/nic0/ipv4"

IPV4_CONFIG = {
    "configurable": True,
    "mode": "STATIC",
    "address": "10.20.80.191",
    "prefix": 24,
    "default_gateway": "10.20.80.1",
}


@patch.object(module_under_test, "AnsibleModule")
@patch.object(module_under_test.VmwareRestInfoModule, "_create_client")
def test_get_ipv4_config(mock_create_client, mock_ansible_module, mock_client):
    mock_create_client.return_value = mock_client
    mock_module = MagicMock()
    mock_ansible_module.return_value = mock_module
    mock_module.params = set_module_args({"interface_name": "nic0"})
    mock_module.exit_json.side_effect = exit_json

    mock_client.get.return_value = _response(200, IPV4_CONFIG)

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_client.get.assert_called_once_with(IPV4_PATH)
    assert exc.value.kwargs == {"value": IPV4_CONFIG}


@patch.object(module_under_test, "AnsibleModule")
@patch.object(module_under_test.VmwareRestInfoModule, "_create_client")
def test_get_ipv4_not_found(mock_create_client, mock_ansible_module, mock_client):
    mock_create_client.return_value = mock_client
    mock_module = MagicMock()
    mock_ansible_module.return_value = mock_module
    mock_module.params = set_module_args({"interface_name": "nic0"})
    mock_module.exit_json.side_effect = exit_json

    mock_client.get.return_value = _response(404, None)

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_client.get.assert_called_once_with(IPV4_PATH)
    assert exc.value.kwargs == {"value": None}
