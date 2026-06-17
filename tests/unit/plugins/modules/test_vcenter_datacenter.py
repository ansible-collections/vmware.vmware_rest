# -*- coding: utf-8 -*-
# Copyright: (c) 2026, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import pytest
from unittest.mock import patch, MagicMock

from ansible_collections.vmware.vmware_rest.plugins.modules import (
    vcenter_datacenter as module_under_test,
)
from ...common.utils import (
    AnsibleExitJson,
    exit_json,
    mock_client,
    set_module_args,
    _response,
)

@patch.object(module_under_test, "AnsibleModule")
@patch.object(module_under_test.VmwareRestCrudModule, "_create_client")
def test_create_datacenter(mock_create_client, mock_ansible_module, mock_client):
    mock_create_client.return_value = mock_client
    mock_module = MagicMock()
    mock_ansible_module.return_value = mock_module
    mock_module.check_mode = False
    mock_module.params = set_module_args(
        {
            "state": "present",
            "name": "my_dc",
            "folder": None,
            "datacenter": None,
            "force": None,
        }
    )
    mock_module.exit_json.side_effect = exit_json
    mock_client.get.return_value = _response(200, [])
    mock_client.post.return_value = _response(200, "datacenter-1001")
    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()
    assert exc.value.kwargs["changed"] is True
    assert exc.value.kwargs["value"] == "datacenter-1001"
