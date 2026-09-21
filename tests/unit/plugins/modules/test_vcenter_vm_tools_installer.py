# -*- coding: utf-8 -*-
# Copyright: (c) 2026, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Unit tests for vcenter_vm_tools_installer module.

Tests validate the CRUD module behavior using the OperationConfig-based
architecture with mocked HTTP clients. The tests drive the module's main()
entrypoint so the real routing, argument spec, and operation configs are
exercised.

This module is an action-only module: the VMware Tools installer CD-ROM of a
per-VM singleton (addressed by the required C(vm) MOID) is either connected or
disconnected. There is no create, update, delete, or list operation, and
neither action is idempotent. The tests therefore focus on the connect and
disconnect actions, check mode, and the module's static definitions.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import pytest
from unittest.mock import patch, MagicMock

from ansible_collections.vmware.vmware_rest.plugins.modules import (
    vcenter_vm_tools_installer as module_under_test,
)

from ...common.utils import (
    AnsibleExitJson,
    exit_json,
    fail_json,
    set_module_args,
    _response,
)

VM_ID = "vm-1013"


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
# Test state=connect - ACTION
# ============================================================================


def test_action_connect(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test that the connect action POSTs to the connect endpoint."""
    mock_client.post.return_value = _response(200, {})

    module_args.update({"state": "connect", "vm": VM_ID})
    mock_module, result = _run_module(
        patch_create_client, patch_ansible_module, mock_client, module_args
    )

    mock_module.exit_json.assert_called_once()
    # The connect action is not idempotent; it always reports a change.
    assert result["changed"] is True
    assert result["id"] == VM_ID
    mock_client.post.assert_called_once()
    call_args = mock_client.post.call_args
    assert call_args[1]["path"] == "/vcenter/vm/vm-1013/tools/installer?action=connect"
    # No body_spec/query_spec is defined; the action is encoded in the URI.
    assert "data" not in call_args[1]
    assert "query" not in call_args[1]
    # No other write HTTP calls should occur for the action.
    mock_client.patch.assert_not_called()
    mock_client.delete.assert_not_called()


# ============================================================================
# Test state=disconnect - ACTION
# ============================================================================


def test_action_disconnect(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test that the disconnect action POSTs to the disconnect endpoint."""
    mock_client.post.return_value = _response(200, {})

    module_args.update({"state": "disconnect", "vm": VM_ID})
    mock_module, result = _run_module(
        patch_create_client, patch_ansible_module, mock_client, module_args
    )

    mock_module.exit_json.assert_called_once()
    # The disconnect action is not idempotent; it always reports a change.
    assert result["changed"] is True
    assert result["id"] == VM_ID
    mock_client.post.assert_called_once()
    call_args = mock_client.post.call_args
    assert (
        call_args[1]["path"] == "/vcenter/vm/vm-1013/tools/installer?action=disconnect"
    )
    # No body_spec/query_spec is defined; the action is encoded in the URI.
    assert "data" not in call_args[1]
    assert "query" not in call_args[1]
    mock_client.patch.assert_not_called()
    mock_client.delete.assert_not_called()


def test_action_empty_response_value(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test that an empty API response body yields an empty value."""
    mock_client.post.return_value = _response(200, {})

    module_args.update({"state": "connect", "vm": VM_ID})
    _, result = _run_module(  # pylint: disable=disallowed-name
        patch_create_client, patch_ansible_module, mock_client, module_args
    )

    assert result["value"] == {}


# ============================================================================
# Test Check Mode
# ============================================================================


class TestCheckMode:
    """Test check mode behavior: report a change but make no write HTTP call."""

    def test_connect_check_mode(
        self, patch_create_client, patch_ansible_module, mock_client, module_args
    ):
        """Test the connect action in check mode issues no POST."""
        module_args.update({"state": "connect", "vm": VM_ID})
        _, result = _run_module(  # pylint: disable=disallowed-name
            patch_create_client,
            patch_ansible_module,
            mock_client,
            module_args,
            check_mode=True,
        )

        assert result["changed"] is True
        assert result["id"] == VM_ID
        assert result["value"] == {}
        mock_client.post.assert_not_called()

    def test_disconnect_check_mode(
        self, patch_create_client, patch_ansible_module, mock_client, module_args
    ):
        """Test the disconnect action in check mode issues no POST."""
        module_args.update({"state": "disconnect", "vm": VM_ID})
        _, result = _run_module(  # pylint: disable=disallowed-name
            patch_create_client,
            patch_ansible_module,
            mock_client,
            module_args,
            check_mode=True,
        )

        assert result["changed"] is True
        assert result["id"] == VM_ID
        assert result["value"] == {}
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
        assert module_under_test.ITEM_ENDPOINT == "/vcenter/vm/{vm}/tools/installer"

    def test_action_operations_keys(self):
        """Test that only the connect and disconnect actions are defined."""
        assert set(module_under_test.ACTION_OPERATIONS.keys()) == {
            "connect",
            "disconnect",
        }


# ============================================================================
# Test Argument Spec
# ============================================================================


class TestArgumentSpec:
    """Test the module argument specification."""

    def test_state_parameter(self):
        """Test that the state parameter is required with the expected choices."""
        spec = module_under_test.create_module_argument_spec()

        assert spec["state"]["type"] == "str"
        assert spec["state"]["required"] is True
        assert spec["state"]["choices"] == ["connect", "disconnect"]
        # There is no default; an action must be explicitly requested.
        assert "default" not in spec["state"]

    def test_vm_parameter_required(self):
        """Test that the vm parameter is required."""
        spec = module_under_test.create_module_argument_spec()

        assert spec["vm"]["type"] == "str"
        assert spec["vm"]["required"] is True


# ============================================================================
# Test OperationConfig Building
# ============================================================================


class TestOperationConfig:
    """Test that the module's operation configs build paths and methods."""

    def test_get_operation(self):
        """Test that the GET operation targets the item endpoint."""
        assert module_under_test.GET_OPERATION.uri == "/vcenter/vm/{vm}/tools/installer"
        assert module_under_test.GET_OPERATION.http_method == "get"

    def test_connect_is_post(self):
        """Test that the connect action uses the POST method."""
        assert module_under_test.ACTION_OPERATIONS["connect"].http_method == "post"

    def test_disconnect_is_post(self):
        """Test that the disconnect action uses the POST method."""
        assert module_under_test.ACTION_OPERATIONS["disconnect"].http_method == "post"

    def test_connect_build_path(self):
        """Test that the connect action preserves the query string in the URI."""
        config = module_under_test.ACTION_OPERATIONS["connect"]

        assert (
            config.build_path(params={"vm": VM_ID})
            == "/vcenter/vm/vm-1013/tools/installer?action=connect"
        )

    def test_disconnect_build_path(self):
        """Test that the disconnect action preserves the query string in the URI."""
        config = module_under_test.ACTION_OPERATIONS["disconnect"]

        assert (
            config.build_path(params={"vm": VM_ID})
            == "/vcenter/vm/vm-1013/tools/installer?action=disconnect"
        )

    def test_actions_have_no_body(self):
        """Test that the actions define no body; nothing is sent in the request."""
        assert (
            module_under_test.ACTION_OPERATIONS["connect"].build_body(
                params={"vm": VM_ID}
            )
            is None
        )
        assert (
            module_under_test.ACTION_OPERATIONS["disconnect"].build_body(
                params={"vm": VM_ID}
            )
            is None
        )
