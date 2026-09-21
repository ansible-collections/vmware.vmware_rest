# -*- coding: utf-8 -*-
# Copyright: (c) 2026, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Unit tests for vcenter_vm_hardware_info module.

Tests validate the info module behavior using the OperationConfig-based
architecture with mocked HTTP clients.

This module has no list endpoint. A single GET against
/vcenter/vm/{vm}/hardware returns the top-level virtual hardware settings of
the virtual machine as a single object.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import pytest
from unittest.mock import patch, MagicMock

from ansible_collections.vmware.vmware_rest.plugins.modules import (
    vcenter_vm_hardware_info as module_under_test,
)

from ...common.utils import (
    AnsibleExitJson,
    exit_json,
    set_module_args,
    _response,
)


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


# ============================================================================
# Test GET Operations (Virtual Hardware Settings)
# ============================================================================


def test_get_hardware_settings(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test getting the virtual hardware settings of a virtual machine."""
    patch_create_client.return_value = mock_client
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module

    module_args.update(
        {
            "vm": "vm-1013",
        }
    )
    mock_module.params = set_module_args(module_args)
    mock_module.exit_json.side_effect = exit_json
    mock_module.check_mode = False

    get_response = {
        "version": "VMX_21",
        "upgrade_policy": "NEVER",
        "upgrade_status": "NONE",
    }

    mock_client.get.return_value = _response(200, get_response)

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_module.exit_json.assert_called_once()
    result = exc.value.kwargs
    # A single GET response is wrapped into a one-element info list.
    assert "info" in result
    assert isinstance(result["info"], list)
    assert len(result["info"]) == 1
    assert result["info"][0] == get_response
    # value mirrors the single hardware settings object.
    assert result["value"] == get_response
    assert result["value"]["version"] == "VMX_21"
    assert result["value"]["upgrade_policy"] == "NEVER"
    assert result["value"]["upgrade_status"] == "NONE"
    # The hardware settings carry no MOID attribute, so no id is set.
    assert "id" not in result


def test_get_hardware_settings_pending_upgrade(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test getting the hardware settings for a VM with a pending upgrade."""
    patch_create_client.return_value = mock_client
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module

    module_args.update(
        {
            "vm": "vm-1013",
        }
    )
    mock_module.params = set_module_args(module_args)
    mock_module.exit_json.side_effect = exit_json
    mock_module.check_mode = False

    get_response = {
        "version": "VMX_19",
        "upgrade_policy": "AFTER_CLEAN_SHUTDOWN",
        "upgrade_status": "PENDING",
        "upgrade_version": "VMX_21",
    }

    mock_client.get.return_value = _response(200, get_response)

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_module.exit_json.assert_called_once()
    result = exc.value.kwargs
    assert len(result["info"]) == 1
    assert result["value"]["version"] == "VMX_19"
    assert result["value"]["upgrade_policy"] == "AFTER_CLEAN_SHUTDOWN"
    assert result["value"]["upgrade_status"] == "PENDING"
    assert result["value"]["upgrade_version"] == "VMX_21"
    assert "id" not in result


def test_get_hardware_settings_not_found(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test getting the hardware settings for a VM that doesn't exist."""
    patch_create_client.return_value = mock_client
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module

    module_args.update(
        {
            "vm": "vm-9999",
        }
    )
    mock_module.params = set_module_args(module_args)
    mock_module.exit_json.side_effect = exit_json
    mock_module.check_mode = False

    mock_client.get.return_value = _response(404, None)

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_module.exit_json.assert_called_once()
    result = exc.value.kwargs
    # A missing resource collapses to an empty info list and empty value.
    assert "info" in result
    assert len(result["info"]) == 0
    assert result["value"] == {}
    assert "id" not in result


# ============================================================================
# Test Check Mode
# ============================================================================


class TestCheckMode:
    """Test check mode behavior."""

    def test_get_check_mode(
        self, patch_create_client, patch_ansible_module, mock_client, module_args
    ):
        """Test getting the hardware settings in check mode (should execute normally)."""
        patch_create_client.return_value = mock_client
        mock_module = MagicMock()
        patch_ansible_module.return_value = mock_module

        module_args.update(
            {
                "vm": "vm-1013",
            }
        )
        mock_module.params = set_module_args(module_args)
        mock_module.exit_json.side_effect = exit_json
        mock_module.check_mode = True

        get_response = {
            "version": "VMX_21",
            "upgrade_policy": "NEVER",
            "upgrade_status": "NONE",
        }

        mock_client.get.return_value = _response(200, get_response)

        with pytest.raises(AnsibleExitJson) as exc:
            module_under_test.main()

        result = exc.value.kwargs
        assert result["value"]["version"] == "VMX_21"
        # Even in check mode, GET should be called (read-only operation).
        mock_client.get.assert_called_once()


# ============================================================================
# Test Module Constants
# ============================================================================


class TestModuleConstants:
    """Test that module constants are correctly defined."""

    def test_moid_parameter_hints(self):
        """Test that MOID parameter hints are correct."""
        assert module_under_test.MOID_PARAMETER_HINTS == ["vm"]

    def test_list_endpoint(self):
        """Test that the list API endpoint is empty (no list operation)."""
        assert module_under_test.LIST_ENDPOINT == ""

    def test_item_endpoint(self):
        """Test that item API endpoint is correct."""
        assert module_under_test.ITEM_ENDPOINT == "/vcenter/vm/{vm}/hardware"


# ============================================================================
# Test Argument Spec
# ============================================================================


class TestArgumentSpec:
    """Test the module argument specification."""

    def test_create_module_argument_spec_vm(self):
        """Test that vm parameter is correctly defined."""
        spec = module_under_test.create_module_argument_spec()

        assert "vm" in spec
        assert spec["vm"]["type"] == "str"
        assert spec["vm"]["required"] is True

    def test_create_module_argument_spec_no_state(self):
        """Test that info module has no state parameter."""
        spec = module_under_test.create_module_argument_spec()

        assert "state" not in spec
