# -*- coding: utf-8 -*-
# Copyright: (c) 2026, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import json
import pytest
from unittest.mock import patch, MagicMock, call

from ansible_collections.vmware.vmware_rest.plugins.module_utils._client import (
    Response,
)
from ansible_collections.vmware.vmware_rest.plugins.modules import (
    vcenter_vm_storage_policy as module_under_test,
)


class AnsibleExitJson(Exception):
    def __init__(self, kwargs):
        self.kwargs = kwargs


class AnsibleFailJson(Exception):
    def __init__(self, kwargs):
        self.kwargs = kwargs


def exit_json(*args, **kwargs):
    if args:
        kwargs.update(args[0])
    raise AnsibleExitJson(kwargs)


def fail_json(*args, **kwargs):
    if args:
        kwargs.update(args[0])
    raise AnsibleFailJson(kwargs)


def _response(status, body):
    data = json.dumps(body).encode("utf-8") if body is not None else b""
    return Response(status, data)


CONNECTION_PARAMS = {
    "vcenter_hostname": "vcenter.example.com",
    "vcenter_username": "admin",
    "vcenter_password": "secret",
    "vcenter_validate_certs": False,
    "vcenter_rest_log_file": None,
    "session_timeout": None,
}

VM = "vm-1009"
POLICY_PATH = "/vcenter/vm/{0}/storage/policy".format(VM)

CURRENT_POLICY = {
    "vm_home": "policy-123",
    "disks": {
        "2000": "policy-456",
    },
}

UPDATED_VM_HOME_POLICY = {
    "vm_home": "policy-789",
    "disks": {
        "2000": "policy-456",
    },
}

UPDATED_DISK_POLICY = {
    "vm_home": "policy-123",
    "disks": {
        "2000": "policy-999",
    },
}


@pytest.fixture
def mock_client():
    return MagicMock()


def set_module_args(args):
    return {**CONNECTION_PARAMS, **args}


@patch.object(module_under_test, "AnsibleModule")
@patch.object(module_under_test.VmwareRestCrudModule, "_create_client")
def test_update_vm_home_specified_policy(
    mock_create_client, mock_ansible_module, mock_client
):
    # PATCH /vcenter/vm/{vm}/storage/policy — Vcenter.Vm.Storage.Policy_update — 204
    mock_create_client.return_value = mock_client
    mock_module = MagicMock()
    mock_ansible_module.return_value = mock_module
    mock_module.check_mode = False
    mock_module.params = set_module_args(
        {
            "state": "present",
            "vm": VM,
            "vm_home": {
                "type": "USE_SPECIFIED_POLICY",
                "policy": "policy-789",
            },
        }
    )
    mock_module.exit_json.side_effect = exit_json

    mock_client.get.side_effect = [
        _response(200, CURRENT_POLICY),
        _response(200, UPDATED_VM_HOME_POLICY),
    ]
    mock_client.patch.return_value = _response(204, None)

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_client.get.assert_has_calls([call(POLICY_PATH), call(POLICY_PATH)])
    mock_client.patch.assert_called_once_with(
        POLICY_PATH,
        data={
            "vm_home": {
                "type": "USE_SPECIFIED_POLICY",
                "policy": "policy-789",
            },
        },
    )
    mock_module.exit_json.assert_called_once()
    assert exc.value.kwargs == {
        "changed": True,
        "value": UPDATED_VM_HOME_POLICY,
    }


@patch.object(module_under_test, "AnsibleModule")
@patch.object(module_under_test.VmwareRestCrudModule, "_create_client")
def test_update_disk_specified_policy(
    mock_create_client, mock_ansible_module, mock_client
):
    # PATCH with Vcenter.Vm.Storage.Policy.UpdateSpec.disks — 204
    mock_create_client.return_value = mock_client
    mock_module = MagicMock()
    mock_ansible_module.return_value = mock_module
    mock_module.check_mode = False
    mock_module.params = set_module_args(
        {
            "state": "present",
            "vm": VM,
            "disks": {
                "2000": {
                    "type": "USE_SPECIFIED_POLICY",
                    "policy": "policy-999",
                },
            },
        }
    )
    mock_module.exit_json.side_effect = exit_json

    mock_client.get.side_effect = [
        _response(200, CURRENT_POLICY),
        _response(200, UPDATED_DISK_POLICY),
    ]
    mock_client.patch.return_value = _response(204, None)

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_client.get.assert_has_calls([call(POLICY_PATH), call(POLICY_PATH)])
    mock_client.patch.assert_called_once_with(
        POLICY_PATH,
        data={
            "disks": {
                "2000": {
                    "type": "USE_SPECIFIED_POLICY",
                    "policy": "policy-999",
                },
            },
        },
    )
    assert exc.value.kwargs == {
        "changed": True,
        "value": UPDATED_DISK_POLICY,
    }


@patch.object(module_under_test, "AnsibleModule")
@patch.object(module_under_test.VmwareRestCrudModule, "_create_client")
def test_no_change(mock_create_client, mock_ansible_module, mock_client):
    # GET 200 — current policy matches desired; no PATCH
    mock_create_client.return_value = mock_client
    mock_module = MagicMock()
    mock_ansible_module.return_value = mock_module
    mock_module.check_mode = False
    mock_module.params = set_module_args(
        {
            "state": "present",
            "vm": VM,
            "vm_home": {
                "type": "USE_SPECIFIED_POLICY",
                "policy": "policy-123",
            },
        }
    )
    mock_module.exit_json.side_effect = exit_json

    mock_client.get.return_value = _response(200, CURRENT_POLICY)

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_client.get.assert_called_once_with(POLICY_PATH)
    mock_client.patch.assert_not_called()
    assert exc.value.kwargs == {
        "changed": False,
        "value": CURRENT_POLICY,
    }


@patch.object(module_under_test, "AnsibleModule")
@patch.object(module_under_test.VmwareRestCrudModule, "_create_client")
def test_vm_not_found(mock_create_client, mock_ansible_module, mock_client):
    # GET 404 — virtual machine not found
    mock_create_client.return_value = mock_client
    mock_module = MagicMock()
    mock_ansible_module.return_value = mock_module
    mock_module.check_mode = False
    mock_module.params = set_module_args(
        {
            "state": "present",
            "vm": VM,
            "vm_home": {"type": "USE_DEFAULT_POLICY"},
        }
    )
    mock_module.fail_json.side_effect = fail_json

    mock_client.get.return_value = _response(404, None)

    with pytest.raises(AnsibleFailJson) as exc:
        module_under_test.main()

    mock_client.get.assert_called_once_with(POLICY_PATH)
    mock_client.patch.assert_not_called()
    assert exc.value.kwargs == {
        "msg": "Virtual machine not found: {0}".format(VM),
    }


@patch.object(module_under_test, "AnsibleModule")
@patch.object(module_under_test.VmwareRestCrudModule, "_create_client")
def test_state_absent(mock_create_client, mock_ansible_module, mock_client):
    # state=absent — no API delete operation; changed=False
    mock_create_client.return_value = mock_client
    mock_module = MagicMock()
    mock_ansible_module.return_value = mock_module
    mock_module.check_mode = False
    mock_module.params = set_module_args(
        {
            "state": "absent",
            "vm": VM,
        }
    )
    mock_module.exit_json.side_effect = exit_json

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_client.get.assert_not_called()
    mock_client.patch.assert_not_called()
    assert exc.value.kwargs == {"changed": False}


@patch.object(module_under_test, "AnsibleModule")
@patch.object(module_under_test.VmwareRestCrudModule, "_create_client")
def test_present_without_params_fails(
    mock_create_client, mock_ansible_module, mock_client
):
    # state=present requires vm_home or disks
    mock_create_client.return_value = mock_client
    mock_module = MagicMock()
    mock_ansible_module.return_value = mock_module
    mock_module.check_mode = False
    mock_module.params = set_module_args(
        {
            "state": "present",
            "vm": VM,
        }
    )
    mock_module.fail_json.side_effect = fail_json

    with pytest.raises(AnsibleFailJson) as exc:
        module_under_test.main()

    mock_client.get.assert_not_called()
    mock_client.patch.assert_not_called()
    assert exc.value.kwargs == {
        "msg": "At least one of vm_home or disks must be specified when state is present",
    }
