# -*- coding: utf-8 -*-
# Copyright: (c) 2026, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import pytest
from unittest.mock import patch, MagicMock

from ansible_collections.vmware.vmware_rest.plugins.modules import (
    vcenter_vm_tools_installer_info as module_under_test,
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
# Test GET Operations (Item-Only Module)
# ============================================================================


def test_get_installer_info(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test getting installer information for a VM."""
    patch_create_client.return_value = mock_client
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module

    module_args.update({"vm": "vm-1009"})
    mock_module.params = set_module_args(module_args)
    mock_module.exit_json.side_effect = exit_json
    mock_module.check_mode = False

    # Mock GET response
    get_response = {
        "is_connected": True,
    }

    mock_client.get.return_value = _response(200, get_response)

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_module.exit_json.assert_called_once()
    result = exc.value.kwargs
    assert result["id"] == "vm-1009"
    assert "value" in result
    assert result["value"]["is_connected"] is True


def test_get_installer_info_not_connected(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test getting installer information when not connected."""
    patch_create_client.return_value = mock_client
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module

    module_args.update({"vm": "vm-1009"})
    mock_module.params = set_module_args(module_args)
    mock_module.exit_json.side_effect = exit_json
    mock_module.check_mode = False

    # Mock GET response
    get_response = {
        "is_connected": False,
    }

    mock_client.get.return_value = _response(200, get_response)

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    result = exc.value.kwargs
    assert result["id"] == "vm-1009"
    assert "value" in result
    assert result["value"]["is_connected"] is False


def test_get_installer_not_found(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test getting installer information for a VM that doesn't exist."""
    patch_create_client.return_value = mock_client
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module

    module_args.update({"vm": "vm-9999"})
    mock_module.params = set_module_args(module_args)
    mock_module.exit_json.side_effect = exit_json
    mock_module.check_mode = False

    # Mock 404 response
    mock_client.get.return_value = _response(404, None)

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    result = exc.value.kwargs
    # When resource not found, module returns empty result
    assert "value" not in result or result.get("value") is None


# ============================================================================
# Test Module Constants
# ============================================================================


class TestModuleConstants:
    """Test that module constants are correctly defined."""

    def test_moid_attribute_name(self):
        """Test that MOID attribute name is correct."""
        assert module_under_test.MOID_ATTRIBUTE_NAME == "vm"

    def test_item_path(self):
        """Test that item API path is correct."""
        assert module_under_test.ITEM_PATH == "/vcenter/vm/{vm}/tools/installer"

    def test_no_list_path(self):
        """Test that LIST_PATH is not defined (item-only module)."""
        assert not hasattr(module_under_test, "LIST_PATH")

    def test_payload_format_structure(self):
        """Test that payload format constants exist."""
        assert hasattr(module_under_test, "GET_PAYLOAD_MAP")

        # Verify GET operation has path mapping
        assert module_under_test.GET_PAYLOAD_MAP._path is not None

    def test_no_list_payload_map(self):
        """Test that LIST_PAYLOAD_MAP is not defined (item-only module)."""
        assert not hasattr(module_under_test, "LIST_PAYLOAD_MAP")


# ============================================================================
# Test PayloadMap Configurations
# ============================================================================


class TestPayloadMappings:
    """Test PayloadMap configurations for the module."""

    def test_get_path_mapping(self):
        """Test GET path mapping."""
        payload_map = module_under_test.GET_PAYLOAD_MAP

        params = {"vm": "vm-1009"}

        result = payload_map._path.params_to_payload(params)
        assert result["vm"] == "vm-1009"

    def test_get_path_mapping_uri_construction(self):
        """Test that GET payload map constructs correct URI."""
        payload_map = module_under_test.GET_PAYLOAD_MAP

        # Verify the URI template
        assert payload_map.uri == "/vcenter/vm/{vm}/tools/installer"

        # Verify operation type
        assert payload_map.operation == "get"


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

    def test_create_module_argument_spec_no_list_filters(self):
        """Test that list filter parameters are not defined (item-only module)."""
        spec = module_under_test.create_module_argument_spec()

        # Item-only modules should not have list filter parameters
        assert "names" not in spec
        assert "folders" not in spec
        assert "datacenters" not in spec


# ============================================================================
# Test Check Mode
# ============================================================================


class TestCheckMode:
    """Test check mode behavior (info modules are always check mode safe)."""

    def test_get_in_check_mode(
        self, patch_create_client, patch_ansible_module, mock_client, module_args
    ):
        """Test that getting a specific resource works in check mode."""
        patch_create_client.return_value = mock_client
        mock_module = MagicMock()
        patch_ansible_module.return_value = mock_module

        module_args.update({"vm": "vm-1009"})
        mock_module.params = set_module_args(module_args)
        mock_module.exit_json.side_effect = exit_json
        mock_module.check_mode = True

        get_response = {
            "is_connected": True,
        }

        mock_client.get.return_value = _response(200, get_response)

        with pytest.raises(AnsibleExitJson) as exc:
            module_under_test.main()

        result = exc.value.kwargs
        assert result["id"] == "vm-1009"
        assert "value" in result
        assert result["value"]["is_connected"] is True


# ============================================================================
# Test API Call Paths
# ============================================================================


class TestAPICallPaths:
    """Test that correct API paths are called."""

    def test_get_api_path(
        self, patch_create_client, patch_ansible_module, mock_client, module_args
    ):
        """Test that GET uses correct API path."""
        patch_create_client.return_value = mock_client
        mock_module = MagicMock()
        patch_ansible_module.return_value = mock_module

        module_args.update({"vm": "vm-1009"})
        mock_module.params = set_module_args(module_args)
        mock_module.exit_json.side_effect = exit_json
        mock_module.check_mode = False

        get_response = {
            "is_connected": True,
        }

        mock_client.get.return_value = _response(200, get_response)

        with pytest.raises(AnsibleExitJson):
            module_under_test.main()

        # Verify GET was called with correct path
        mock_client.get.assert_called()
        call_args = mock_client.get.call_args
        assert call_args[0][0] == "/vcenter/vm/vm-1009/tools/installer"
