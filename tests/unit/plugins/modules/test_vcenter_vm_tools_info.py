# -*- coding: utf-8 -*-
# Copyright: (c) 2026, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Unit tests for vcenter_vm_tools_info module.

Tests validate the Info module behavior using the OperationConfig-based
architecture with mocked HTTP clients. This endpoint is a per-VM resource
(keyed on the required C(vm) path parameter) that returns a single VMware
Tools status object.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import pytest
from unittest.mock import patch, MagicMock

from ansible_collections.vmware.vmware_rest.plugins.modules import (
    vcenter_vm_tools_info as module_under_test,
)

from ...common.utils import (
    AnsibleExitJson,
    exit_json,
    set_module_args,
    _response,
)

# A realistic VMware Tools response for /vcenter/vm/{vm}/tools.
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
        module_under_test.VmwareRestInfoModuleBase, "_create_client"
    ) as mock:
        yield mock


def _run_module(patch_ansible_module, mock_client, module_args, status, body):
    """Helper: wire up the mocked module/client and run main()."""
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module
    mock_module.params = set_module_args({**module_args, "vm": "vm-42"})
    mock_module.exit_json.side_effect = exit_json
    mock_module.check_mode = False
    mock_client.get.return_value = _response(status, body)
    return mock_module


# ============================================================================
# Test GET Operations (per-VM tools status)
# ============================================================================


def test_get_vm_tools_found(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test getting VMware Tools status for a VM that reports one."""
    patch_create_client.return_value = mock_client
    mock_module = _run_module(
        patch_ansible_module, mock_client, module_args, 200, VM_TOOLS
    )

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_module.exit_json.assert_called_once()
    result = exc.value.kwargs
    # A single resource fetched by ID preserves its dict shape in "value".
    assert result["value"] == VM_TOOLS
    # "info" is always a list of dicts.
    assert result["info"] == [VM_TOOLS]
    # The tools payload carries no MOID attribute, so no id is set.
    assert "id" not in result


def test_get_vm_tools_not_found(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test getting VMware Tools status when the endpoint returns 404."""
    patch_create_client.return_value = mock_client
    mock_module = _run_module(patch_ansible_module, mock_client, module_args, 404, None)

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_module.exit_json.assert_called_once()
    result = exc.value.kwargs
    assert result["info"] == []
    assert result["value"] == {}
    assert "id" not in result


# ============================================================================
# Test Check Mode
# ============================================================================


class TestCheckMode:
    """Test check mode behavior (info modules always execute normally)."""

    def test_get_check_mode(
        self, patch_create_client, patch_ansible_module, mock_client, module_args
    ):
        """Test getting tools status in check mode still queries the API."""
        patch_create_client.return_value = mock_client
        mock_module = MagicMock()
        patch_ansible_module.return_value = mock_module
        mock_module.params = set_module_args({**module_args, "vm": "vm-42"})
        mock_module.exit_json.side_effect = exit_json
        mock_module.check_mode = True

        mock_client.get.return_value = _response(200, VM_TOOLS)

        with pytest.raises(AnsibleExitJson) as exc:
            module_under_test.main()

        result = exc.value.kwargs
        assert result["value"] == VM_TOOLS
        mock_client.get.assert_called_once()


# ============================================================================
# Test API Call Path
# ============================================================================


class TestAPICallPath:
    """Test that the correct API path is called."""

    def test_get_api_path(
        self, patch_create_client, patch_ansible_module, mock_client, module_args
    ):
        """Test that GET builds the per-VM path using the vm parameter."""
        patch_create_client.return_value = mock_client
        _run_module(patch_ansible_module, mock_client, module_args, 200, VM_TOOLS)

        with pytest.raises(AnsibleExitJson):
            module_under_test.main()

        mock_client.get.assert_called_once()
        call_args = mock_client.get.call_args
        assert call_args[0][0] == "/vcenter/vm/vm-42/tools"


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

    def test_get_operation_config(self):
        """Test that the GET operation config targets the item endpoint."""
        assert module_under_test.GET_OPERATION.uri == "/vcenter/vm/{vm}/tools"
        assert module_under_test.GET_OPERATION.http_method == "get"


# ============================================================================
# Test Argument Spec
# ============================================================================


class TestArgumentSpec:
    """Test the module argument specification."""

    def test_create_module_argument_spec_has_connection_params(self):
        """Test that connection parameters are included."""
        spec = module_under_test.create_module_argument_spec()

        assert "vcenter_hostname" in spec
        assert "vcenter_username" in spec
        assert "vcenter_password" in spec

    def test_create_module_argument_spec_vm_required(self):
        """Test that the vm identifier is a required string parameter."""
        spec = module_under_test.create_module_argument_spec()

        assert spec["vm"]["type"] == "str"
        assert spec["vm"]["required"] is True

    def test_create_module_argument_spec_no_state(self):
        """Test that info module has no state parameter."""
        spec = module_under_test.create_module_argument_spec()

        assert "state" not in spec
