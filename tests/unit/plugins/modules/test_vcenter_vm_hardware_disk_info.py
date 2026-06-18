# -*- coding: utf-8 -*-
# Copyright: (c) 2026, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import pytest
from unittest.mock import patch, MagicMock

from ansible_collections.vmware.vmware_rest.plugins.modules import (
    vcenter_vm_hardware_disk_info as module_under_test,
)
from ...common.utils import (
    AnsibleExitJson,
    exit_json,
    set_module_args,
    _response,
)

API_PATH = "/vcenter/vm/{vm}/hardware/disk"
SAMPLE_BODY = [
    {
        "disk": "2000",
        "label": "Hard disk 1",
        "type": "SCSI",
        "capacity": 10737418240,
        "backing": {
            "type": "VMDK_FILE",
            "vmdk_file": "[datastore1] vm-1001/vm-1001.vmdk",
        },
    }
]


@patch.object(module_under_test, "AnsibleModule")
@patch.object(module_under_test.VmwareRestInfoModule, "_create_client")
def test_get_success(mock_create_client, mock_ansible_module, mock_client):
    mock_create_client.return_value = mock_client
    mock_module = MagicMock()
    mock_ansible_module.return_value = mock_module
    mock_module.params = set_module_args({"vm": "vm-1"})
    mock_module.exit_json.side_effect = exit_json
    mock_client.get.side_effect = [
        _response(200, ["disk-1"]),
        _response(200, {"capacity": 1024}),
    ]
    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()
    assert "value" in exc.value.kwargs


@patch.object(module_under_test, "AnsibleModule")
@patch.object(module_under_test.VmwareRestInfoModule, "_create_client")
def test_get_not_found(mock_create_client, mock_ansible_module, mock_client):
    mock_create_client.return_value = mock_client
    mock_module = MagicMock()
    mock_ansible_module.return_value = mock_module
    mock_module.params = set_module_args({"vm": "vm-1"})
    mock_module.exit_json.side_effect = exit_json
    mock_client.get.return_value = _response(404, None)
    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()
    assert exc.value.kwargs.get("value") in ([], None)
