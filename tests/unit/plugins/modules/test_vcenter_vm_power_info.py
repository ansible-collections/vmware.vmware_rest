# -*- coding: utf-8 -*-
# Copyright: (c) 2026, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import pytest
from unittest.mock import patch, MagicMock

from ansible_collections.vmware.vmware_rest.plugins.modules import (
    vcenter_vm_power_info as module_under_test,
)
from ...common.utils import (
    AnsibleExitJson,
    AnsibleFailJson,
    exit_json,
    fail_json,
    mock_client,
    set_module_args,
    _response,
)

API_PATH = "/vcenter/vm/{vm}/power"
SAMPLE_BODY = {"state": "POWERED_ON", "clean_power_off": True}

def fail_json(*args, **kwargs):
    if args:
        kwargs.update(args[0])
    raise AnsibleFailJson(kwargs)

@patch.object(module_under_test, "AnsibleModule")
@patch.object(module_under_test.VmwareRestInfoModule, "_create_client")
def test_get_success(mock_create_client, mock_ansible_module, mock_client):
    mock_create_client.return_value = mock_client
    mock_module = MagicMock()
    mock_ansible_module.return_value = mock_module
    mock_module.params = set_module_args({"vm": "vm-1001"})
    mock_module.exit_json.side_effect = exit_json
    mock_client.get.return_value = _response(200, {"state": "POWERED_ON"})
    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()
    assert exc.value.kwargs["value"]["state"] == "POWERED_ON"

@patch.object(module_under_test, "AnsibleModule")
@patch.object(module_under_test.VmwareRestInfoModule, "_create_client")
def test_get_not_found(mock_create_client, mock_ansible_module, mock_client):
    mock_create_client.return_value = mock_client
    mock_module = MagicMock()
    mock_ansible_module.return_value = mock_module
    mock_module.params = set_module_args({"vm": "vm-1001"})
    mock_module.fail_json.side_effect = fail_json
    mock_client.get.return_value = _response(404, None)
    mock_client.error_handler.handle_request_error.side_effect = fail_json
    with pytest.raises(AnsibleFailJson):
        module_under_test.main()
