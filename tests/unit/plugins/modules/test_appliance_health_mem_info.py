# -*- coding: utf-8 -*-
# Copyright: (c) 2026, Ansible Project

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import pytest
from unittest.mock import patch, MagicMock

from ansible_collections.vmware.vmware_rest.plugins.modules import (
    appliance_health_mem_info as module_under_test,
)
from ...common.utils import (
    AnsibleExitJson,
    CONNECTION_PARAMS,
    exit_json,
    _response,
)


@patch.object(module_under_test, "AnsibleModule")
@patch.object(module_under_test.VmwareRestInfoModule, "_create_client")
def test_get_success(mock_create_client, mock_ansible_module, mock_client):
    mock_create_client.return_value = mock_client
    mock_module = MagicMock()
    mock_ansible_module.return_value = mock_module
    mock_module.params = {**CONNECTION_PARAMS}
    mock_module.exit_json.side_effect = exit_json
    mock_client.get.return_value = _response(200, "green")

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_client.get.assert_called_once_with("/appliance/health/mem")
    assert exc.value.kwargs == {"value": "green"}


@patch.object(module_under_test, "AnsibleModule")
@patch.object(module_under_test.VmwareRestInfoModule, "_create_client")
def test_get_not_found(mock_create_client, mock_ansible_module, mock_client):
    mock_create_client.return_value = mock_client
    mock_module = MagicMock()
    mock_ansible_module.return_value = mock_module
    mock_module.params = {**CONNECTION_PARAMS}
    mock_module.exit_json.side_effect = exit_json
    mock_client.get.return_value = _response(404, None)

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    assert exc.value.kwargs == {"value": None}
