# -*- coding: utf-8 -*-
# Copyright: (c) 2026, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Unit tests for vcenter_vm_tools module.

Tests validate the CRUD module behavior using the OperationConfig-based
architecture with mocked HTTP clients. The tests drive the module's main()
entrypoint so the real routing, argument spec, and operation configs are
exercised.

This module is an unusual CRUD module: VMware Tools is a per-VM singleton
addressed by the required C(vm) MOID. It only supports GET and UPDATE
operations (there is no create, delete, or list) plus an C(upgrade) action.
The tests therefore focus on the update/idempotency paths, the upgrade
action, and the "resource cannot be created" behavior.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import pytest
from unittest.mock import patch, MagicMock

from ansible_collections.vmware.vmware_rest.plugins.modules import (
    vcenter_vm_tools as module_under_test,
)

from ...common.utils import (
    AnsibleExitJson,
    AnsibleFailJson,
    exit_json,
    fail_json,
    set_module_args,
    _response,
)

VM_ID = "vm-42"

# A realistic VMware Tools response for GET /vcenter/vm/{vm}/tools.
VM_TOOLS = {
    "version_status": "CURRENT",
    "run_state": "RUNNING",
    "version": "12352",
    "install_type": "OPEN_VM_TOOLS",
    "upgrade_policy": "MANUAL",
    "auto_update_supported": False,
}


@pytest.fixture(autouse=True)
def patch_ansible_module():
    """Automatically patch AnsibleModule for all tests."""
    with patch.object(module_under_test, "AnsibleModule") as mock:
        yield mock


@pytest.fixture(autouse=True)
def patch_create_client():
    """Automatically patch _create_client for all tests."""
    with patch.object(
        module_under_test.VmwareRestCrudModuleBase, "_create_client"
    ) as mock:
        yield mock


def _run_module(
    patch_create_client, patch_ansible_module, mock_client, args, check_mode=False
):
    """
    Configure the mocked AnsibleModule/client, run main(), and return the
    mocked module plus the kwargs passed to exit_json.
    """
    patch_create_client.return_value = mock_client
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module
    mock_module.params = set_module_args(args)
    mock_module.exit_json.side_effect = exit_json
    mock_module.fail_json.side_effect = fail_json
    mock_module.check_mode = check_mode

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    return mock_module, exc.value.kwargs


# ============================================================================
# Test state=present - UPDATE
# ============================================================================


def test_ensure_present_updates_upgrade_policy(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test updating the tools upgrade policy when a change is detected."""
    mock_client.get.return_value = _response(200, VM_TOOLS)
    mock_client.patch.return_value = _response(200, {})

    module_args.update(
        {
            "state": "present",
            "vm": VM_ID,
            "upgrade_policy": "UPGRADE_AT_POWER_CYCLE",
        }
    )
    mock_module, result = _run_module(
        patch_create_client, patch_ansible_module, mock_client, module_args
    )

    mock_module.exit_json.assert_called_once()
    assert result["changed"] is True
    assert result["id"] == VM_ID
    assert result["diff"]["upgrade_policy"] == {
        "before": "MANUAL",
        "after": "UPGRADE_AT_POWER_CYCLE",
    }
    mock_client.patch.assert_called_once()
    call_args = mock_client.patch.call_args
    assert call_args[0][0] == "/vcenter/vm/vm-42/tools"
    assert call_args[1]["data"] == {"upgrade_policy": "UPGRADE_AT_POWER_CYCLE"}


def test_ensure_present_no_changes(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """
    Test no changes when the upgrade policy already matches the desired state
    (idempotent). Read-only fields reported by the API must not register as a
    change because only the keys the user specified are compared.
    """
    mock_client.get.return_value = _response(200, VM_TOOLS)

    module_args.update(
        {
            "state": "present",
            "vm": VM_ID,
            "upgrade_policy": "MANUAL",
        }
    )
    _, result = _run_module(
        patch_create_client, patch_ansible_module, mock_client, module_args
    )

    assert result["changed"] is False
    assert result["id"] == VM_ID
    assert result["diff"] == {}
    mock_client.patch.assert_not_called()


def test_ensure_present_omit_upgrade_policy_noop(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """
    Test that omitting upgrade_policy results in no update, since the update
    body is empty and nothing is requested to change.
    """
    mock_client.get.return_value = _response(200, VM_TOOLS)

    module_args.update({"state": "present", "vm": VM_ID})
    _, result = _run_module(
        patch_create_client, patch_ansible_module, mock_client, module_args
    )

    assert result["changed"] is False
    assert result["diff"] == {}
    mock_client.patch.assert_not_called()


def test_ensure_present_not_found_cannot_create(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """
    Test that when the VM's tools resource cannot be resolved and the module
    has no create operation, it fails rather than attempting a create.
    """
    patch_create_client.return_value = mock_client
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module
    module_args.update(
        {
            "state": "present",
            "vm": "vm-missing",
            "upgrade_policy": "MANUAL",
        }
    )
    mock_module.params = set_module_args(module_args)
    mock_module.check_mode = False
    mock_module.fail_json.side_effect = fail_json

    mock_client.get.return_value = _response(404, None)

    with pytest.raises(AnsibleFailJson):
        module_under_test.main()

    mock_client.post.assert_not_called()
    mock_client.patch.assert_not_called()


# ============================================================================
# Test state=upgrade - ACTION
# ============================================================================


def test_action_upgrade(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test that the upgrade action POSTs to the upgrade endpoint."""
    mock_client.post.return_value = _response(200, {})

    module_args.update({"state": "upgrade", "vm": VM_ID})
    _, result = _run_module(
        patch_create_client, patch_ansible_module, mock_client, module_args
    )

    # The upgrade action is not idempotent; it always reports a change.
    assert result["changed"] is True
    assert result["id"] == VM_ID
    mock_client.post.assert_called_once()
    call_args = mock_client.post.call_args
    assert call_args[1]["path"] == "/vcenter/vm/vm-42/tools?action=upgrade"
    # No query spec is defined; the action is encoded in the URI.
    assert "query" not in call_args[1]
    # No write-side GET/PATCH should occur for the action.
    mock_client.patch.assert_not_called()


def test_action_upgrade_with_command_line_options(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test that command_line_options are sent in the upgrade action body."""
    mock_client.post.return_value = _response(200, {})

    module_args.update(
        {
            "state": "upgrade",
            "vm": VM_ID,
            "command_line_options": "/S /v/qn",
        }
    )
    _run_module(patch_create_client, patch_ansible_module, mock_client, module_args)

    call_args = mock_client.post.call_args
    assert call_args[1]["data"] == {"command_line_options": "/S /v/qn"}


# ============================================================================
# Test Check Mode
# ============================================================================


class TestCheckMode:
    """Test check mode behavior: report a change but make no write HTTP call."""

    def test_update_check_mode(
        self, patch_create_client, patch_ansible_module, mock_client, module_args
    ):
        """Test updating the upgrade policy in check mode issues no PATCH."""
        mock_client.get.return_value = _response(200, VM_TOOLS)

        module_args.update(
            {
                "state": "present",
                "vm": VM_ID,
                "upgrade_policy": "UPGRADE_AT_POWER_CYCLE",
            }
        )
        _, result = _run_module(
            patch_create_client,
            patch_ansible_module,
            mock_client,
            module_args,
            check_mode=True,
        )

        assert result["changed"] is True
        assert result["diff"]["upgrade_policy"] == {
            "before": "MANUAL",
            "after": "UPGRADE_AT_POWER_CYCLE",
        }
        mock_client.patch.assert_not_called()

    def test_upgrade_check_mode(
        self, patch_create_client, patch_ansible_module, mock_client, module_args
    ):
        """Test the upgrade action in check mode issues no POST."""
        module_args.update({"state": "upgrade", "vm": VM_ID})
        _, result = _run_module(
            patch_create_client,
            patch_ansible_module,
            mock_client,
            module_args,
            check_mode=True,
        )

        assert result["changed"] is True
        assert result["id"] == VM_ID
        mock_client.post.assert_not_called()


# ============================================================================
# Test Module Constants
# ============================================================================


class TestModuleConstants:
    """Test that module constants are correctly defined."""

    def test_moid_parameter_hints(self):
        """Test that the MOID parameter hint is the vm identifier."""
        assert module_under_test.MOID_PARAMETER_HINTS == ["vm"]

    def test_list_endpoint(self):
        """Test that there is no list endpoint for this per-VM resource."""
        assert module_under_test.LIST_ENDPOINT == ""

    def test_item_endpoint(self):
        """Test that the item API endpoint is correct."""
        assert module_under_test.ITEM_ENDPOINT == "/vcenter/vm/{vm}/tools"

    def test_action_operations_keys(self):
        """Test that only the upgrade action is defined."""
        assert set(module_under_test.ACTION_OPERATIONS.keys()) == {"upgrade"}


# ============================================================================
# Test Argument Spec
# ============================================================================


class TestArgumentSpec:
    """Test the module argument specification."""

    def test_state_parameter(self):
        """Test that the state parameter is correctly defined."""
        spec = module_under_test.create_module_argument_spec()

        assert spec["state"]["type"] == "str"
        assert spec["state"]["default"] == "present"
        assert spec["state"]["choices"] == ["present", "upgrade"]

    def test_vm_parameter_required(self):
        """Test that the vm parameter is required."""
        spec = module_under_test.create_module_argument_spec()

        assert spec["vm"]["type"] == "str"
        assert spec["vm"]["required"] is True

    def test_upgrade_policy_parameter(self):
        """Test that upgrade_policy is an optional string parameter."""
        spec = module_under_test.create_module_argument_spec()

        assert spec["upgrade_policy"]["type"] == "str"
        assert spec["upgrade_policy"].get("required", False) is False

    def test_command_line_options_parameter(self):
        """Test that command_line_options is an optional string parameter."""
        spec = module_under_test.create_module_argument_spec()

        assert spec["command_line_options"]["type"] == "str"
        assert spec["command_line_options"].get("required", False) is False


# ============================================================================
# Test OperationConfig Building
# ============================================================================


class TestOperationConfig:
    """Test that the module's operation configs build paths and bodies."""

    def test_get_operation(self):
        """Test that the GET operation targets the item endpoint."""
        assert module_under_test.GET_OPERATION.uri == "/vcenter/vm/{vm}/tools"
        assert module_under_test.GET_OPERATION.http_method == "get"

    def test_update_is_patch(self):
        """Test that the update operation uses the PATCH method."""
        assert module_under_test.UPDATE_OPERATION.http_method == "patch"

    def test_update_build_path(self):
        """Test that the update operation interpolates the vm into the path."""
        path = module_under_test.UPDATE_OPERATION.build_path(params={"vm": VM_ID})
        assert path == "/vcenter/vm/vm-42/tools"

    def test_update_build_body(self):
        """Test that the update body carries upgrade_policy and omits unset params."""
        config = module_under_test.UPDATE_OPERATION

        assert config.build_body(params={"upgrade_policy": "MANUAL"}) == {
            "upgrade_policy": "MANUAL"
        }
        # Optional param omitted -> empty body (not None, since a body_spec exists).
        assert config.build_body(params={"vm": VM_ID}) == {}

    def test_upgrade_is_post(self):
        """Test that the upgrade action uses the POST method."""
        assert module_under_test.ACTION_OPERATIONS["upgrade"].http_method == "post"

    def test_upgrade_build_path(self):
        """Test that the upgrade action preserves the query string in the URI."""
        config = module_under_test.ACTION_OPERATIONS["upgrade"]

        assert (
            config.build_path(params={"vm": VM_ID})
            == "/vcenter/vm/vm-42/tools?action=upgrade"
        )

    def test_upgrade_build_body(self):
        """Test that the upgrade action builds a body with command_line_options."""
        config = module_under_test.ACTION_OPERATIONS["upgrade"]

        assert config.build_body(params={"command_line_options": "/S"}) == {
            "command_line_options": "/S"
        }
