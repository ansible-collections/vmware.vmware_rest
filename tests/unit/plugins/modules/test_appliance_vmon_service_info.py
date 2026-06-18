# -*- coding: utf-8 -*-
# Copyright: (c) 2026, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import pytest
from unittest.mock import patch, MagicMock

from ansible_collections.vmware.vmware_rest.plugins.modules import (
    appliance_vmon_service_info as module_under_test,
)
from ...common.utils import (
    AnsibleExitJson,
    exit_json,
    set_module_args,
    _response,
)

LIST_PATH = "/rest/appliance/vmon/service"
SERVICE_PATH = "/rest/appliance/vmon/service/vpxd"

SERVICE_LIST = {
    "value": [
        {
            "key": "vpxd",
            "value": {
                "name_key": "cis.vpxd.ServiceName",
                "description_key": "cis.vpxd.ServiceDescription",
                "startup_type": "AUTOMATIC",
                "state": "STARTED",
            },
        }
    ]
}

SERVICE_INFO = {
    "value": {
        "name_key": "cis.vpxd.ServiceName",
        "description_key": "cis.vpxd.ServiceDescription",
        "startup_type": "AUTOMATIC",
        "state": "STARTED",
    }
}


@patch.object(module_under_test, "AnsibleModule")
@patch.object(module_under_test.VmwareRestInfoModule, "_create_client")
def test_list_services(mock_create_client, mock_ansible_module, mock_client):
    mock_create_client.return_value = mock_client
    mock_module = MagicMock()
    mock_ansible_module.return_value = mock_module
    mock_module.params = set_module_args({})
    mock_module.exit_json.side_effect = exit_json

    mock_client.get.return_value = _response(200, SERVICE_LIST)

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_client.get.assert_called_once_with(LIST_PATH)
    assert exc.value.kwargs == {"value": SERVICE_LIST["value"]}


@patch.object(module_under_test, "AnsibleModule")
@patch.object(module_under_test.VmwareRestInfoModule, "_create_client")
def test_get_service(mock_create_client, mock_ansible_module, mock_client):
    mock_create_client.return_value = mock_client
    mock_module = MagicMock()
    mock_ansible_module.return_value = mock_module
    mock_module.params = set_module_args({"service": "vpxd"})
    mock_module.exit_json.side_effect = exit_json

    mock_client.get.return_value = _response(200, SERVICE_INFO)

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_client.get.assert_called_once_with(SERVICE_PATH)
    assert exc.value.kwargs == {"value": SERVICE_INFO["value"]}
