# -*- coding: utf-8 -*-
# Copyright: (c) 2026, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Unit tests for vcenter_vm_hardware_boot_info module.

Tests validate the info module behavior using the OperationConfig-based
architecture with mocked HTTP clients.

This module has no list endpoint. A single GET against
/vcenter/vm/{vm}/hardware/boot returns the boot configuration of the virtual
machine as a single object.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import pytest
from unittest.mock import patch, MagicMock

from ansible_collections.vmware.vmware_rest.plugins.modules import (
    vcenter_vm_hardware_boot_info as module_under_test,
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
# Test GET Operations (Boot Configuration)
# ============================================================================


def test_get_boot_config(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test getting the boot configuration of a virtual machine."""
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
        "delay": 0,
        "efi_legacy_boot": False,
        "enter_setup_mode": False,
        "network_protocol": "IPV4",
        "retry": False,
        "retry_delay": 10000,
        "type": "EFI",
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
    # value mirrors the single boot configuration object.
    assert result["value"] == get_response
    assert result["value"]["type"] == "EFI"
    assert result["value"]["network_protocol"] == "IPV4"
    assert result["value"]["retry_delay"] == 10000
    # The boot configuration carries no MOID attribute, so no id is set.
    assert "id" not in result


def test_get_boot_config_bios(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test getting the boot configuration of a BIOS firmware virtual machine."""
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
        "delay": 2000,
        "enter_setup_mode": True,
        "retry": True,
        "retry_delay": 5000,
        "type": "BIOS",
    }

    mock_client.get.return_value = _response(200, get_response)

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_module.exit_json.assert_called_once()
    result = exc.value.kwargs
    assert len(result["info"]) == 1
    assert result["value"]["type"] == "BIOS"
    assert result["value"]["delay"] == 2000
    assert result["value"]["enter_setup_mode"] is True
    assert result["value"]["retry"] is True
    assert "id" not in result


def test_get_boot_config_not_found(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test getting the boot configuration for a VM that doesn't exist."""
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
        """Test getting the boot configuration in check mode (should execute normally)."""
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
            "delay": 0,
            "type": "EFI",
        }

        mock_client.get.return_value = _response(200, get_response)

        with pytest.raises(AnsibleExitJson) as exc:
            module_under_test.main()

        result = exc.value.kwargs
        assert result["value"]["type"] == "EFI"
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
        assert module_under_test.ITEM_ENDPOINT == "/vcenter/vm/{vm}/hardware/boot"


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
