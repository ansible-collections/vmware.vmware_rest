# -*- coding: utf-8 -*-
# Copyright: (c) 2026, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Unit tests for appliance_networking_interfaces_info module.

Tests validate the Info module behavior using the OperationConfig-based
architecture with mocked HTTP clients.

``appliance_networking_interfaces_info`` is a read-only module that returns
information about the appliance network interfaces. When O(interface_name) is
supplied it performs a GET against
``/appliance/networking/interfaces/{interface_name}`` and returns a single
resource; otherwise it LISTs ``/appliance/networking/interfaces`` and returns
all interfaces.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import pytest
from unittest.mock import patch, MagicMock

from ansible_collections.vmware.vmware_rest.plugins.modules import (
    appliance_networking_interfaces_info as module_under_test,
)

from ...common.utils import (
    AnsibleExitJson,
    exit_json,
    fail_json,
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


def _run_module(patch_ansible_module, module_args, check_mode=False):
    """Helper: wire up the mocked module and return the mock module."""
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module
    mock_module.params = set_module_args(module_args)
    mock_module.exit_json.side_effect = exit_json
    mock_module.fail_json.side_effect = fail_json
    mock_module.check_mode = check_mode
    return mock_module


LIST_PATH = "/appliance/networking/interfaces"
ITEM_PATH = "/appliance/networking/interfaces/nic0"

# A representative GET response for a single interface.
SAMPLE_INTERFACE = {
    "name": "nic0",
    "mac": "00:0c:29:94:bb:5a",
    "status": "up",
    "ipv4": {
        "mode": "STATIC",
        "address": "192.168.123.8",
        "prefix": 24,
        "default_gateway": "192.168.123.1",
        "configurable": True,
    },
}

# A representative LIST response with multiple interfaces.
SAMPLE_INTERFACES = [
    SAMPLE_INTERFACE,
    {"name": "nic1", "mac": "00:0c:29:94:bb:5b", "status": "down"},
]


# ============================================================================
# Test GET Operations (by interface_name)
# ============================================================================


def test_get_interface_info(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test retrieving a single interface by name."""
    patch_create_client.return_value = mock_client
    module_args.update({"interface_name": "nic0"})
    mock_module = _run_module(patch_ansible_module, module_args)
    mock_client.get.return_value = _response(200, SAMPLE_INTERFACE)

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_module.exit_json.assert_called_once()
    result = exc.value.kwargs
    # value preserves the single-resource dict shape.
    assert result["value"] == SAMPLE_INTERFACE
    # info is always a list; the singleton yields exactly one element.
    assert result["info"] == [SAMPLE_INTERFACE]


def test_get_interface_info_not_found(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test that a 404 for a named interface yields empty results."""
    patch_create_client.return_value = mock_client
    module_args.update({"interface_name": "nic-missing"})
    mock_module = _run_module(patch_ansible_module, module_args)
    mock_client.get.return_value = _response(404, None)

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_module.exit_json.assert_called_once()
    result = exc.value.kwargs
    assert result["info"] == []
    assert result["value"] == {}
    assert "id" not in result


# ============================================================================
# Test LIST Operations (no interface_name)
# ============================================================================


def test_list_all_interfaces(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test listing all interfaces when interface_name is not provided."""
    patch_create_client.return_value = mock_client
    mock_module = _run_module(patch_ansible_module, module_args)
    mock_client.get.return_value = _response(200, SAMPLE_INTERFACES)

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_module.exit_json.assert_called_once()
    result = exc.value.kwargs
    assert result["info"] == SAMPLE_INTERFACES
    # For a listing, value preserves the list shape.
    assert result["value"] == SAMPLE_INTERFACES
    assert "id" not in result


def test_list_all_interfaces_empty(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test listing when no interfaces exist."""
    patch_create_client.return_value = mock_client
    _run_module(patch_ansible_module, module_args)
    mock_client.get.return_value = _response(200, [])

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    result = exc.value.kwargs
    assert result["info"] == []
    assert result["value"] == []


def test_list_all_interfaces_404(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test that a 404 on the collection endpoint yields empty results."""
    patch_create_client.return_value = mock_client
    _run_module(patch_ansible_module, module_args)
    mock_client.get.return_value = _response(404, None)

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    result = exc.value.kwargs
    assert result["info"] == []


# ============================================================================
# Test Check Mode
# ============================================================================


class TestCheckMode:
    """Test check mode behavior (info modules always execute normally)."""

    def test_get_check_mode(
        self, patch_create_client, patch_ansible_module, mock_client, module_args
    ):
        """Test that reading in check mode still performs the GET."""
        patch_create_client.return_value = mock_client
        module_args.update({"interface_name": "nic0"})
        _run_module(patch_ansible_module, module_args, check_mode=True)
        mock_client.get.return_value = _response(200, SAMPLE_INTERFACE)

        with pytest.raises(AnsibleExitJson) as exc:
            module_under_test.main()

        result = exc.value.kwargs
        assert result["value"] == SAMPLE_INTERFACE
        mock_client.get.assert_called_once()

    def test_list_check_mode(
        self, patch_create_client, patch_ansible_module, mock_client, module_args
    ):
        """Test that listing in check mode still performs the LIST."""
        patch_create_client.return_value = mock_client
        _run_module(patch_ansible_module, module_args, check_mode=True)
        mock_client.get.return_value = _response(200, SAMPLE_INTERFACES)

        with pytest.raises(AnsibleExitJson) as exc:
            module_under_test.main()

        result = exc.value.kwargs
        assert result["info"] == SAMPLE_INTERFACES
        mock_client.get.assert_called_once()


# ============================================================================
# Test API Call Path
# ============================================================================


class TestAPICallPath:
    """Test that the correct API path is called."""

    def test_get_api_path(
        self, patch_create_client, patch_ansible_module, mock_client, module_args
    ):
        """Test that GET uses the interface item path with no query."""
        patch_create_client.return_value = mock_client
        module_args.update({"interface_name": "nic0"})
        _run_module(patch_ansible_module, module_args)
        mock_client.get.return_value = _response(200, SAMPLE_INTERFACE)

        with pytest.raises(AnsibleExitJson):
            module_under_test.main()

        mock_client.get.assert_called_once()
        call_args = mock_client.get.call_args
        assert call_args[0][0] == ITEM_PATH
        assert call_args[1]["query"] is None

    def test_list_api_path(
        self, patch_create_client, patch_ansible_module, mock_client, module_args
    ):
        """Test that LIST uses the collection path with no query."""
        patch_create_client.return_value = mock_client
        _run_module(patch_ansible_module, module_args)
        mock_client.get.return_value = _response(200, SAMPLE_INTERFACES)

        with pytest.raises(AnsibleExitJson):
            module_under_test.main()

        mock_client.get.assert_called_once()
        call_args = mock_client.get.call_args
        assert call_args[0][0] == LIST_PATH
        assert call_args[1]["query"] is None


# ============================================================================
# Test Module Constants
# ============================================================================


class TestModuleConstants:
    """Test that module constants are correctly defined."""

    def test_moid_parameter_hints(self):
        """Test that the interface name is used as the MOID hint."""
        assert module_under_test.MOID_PARAMETER_HINTS == ["interface_name"]

    def test_list_endpoint(self):
        """Test that the list API endpoint is correct."""
        assert module_under_test.LIST_ENDPOINT == LIST_PATH

    def test_item_endpoint(self):
        """Test that the item API endpoint is correct."""
        assert (
            module_under_test.ITEM_ENDPOINT
            == "/appliance/networking/interfaces/{interface_name}"
        )

    def test_get_operation_config(self):
        """Test that the GET operation config targets the item endpoint."""
        assert (
            module_under_test.GET_OPERATION.uri
            == "/appliance/networking/interfaces/{interface_name}"
        )
        assert module_under_test.GET_OPERATION.http_method == "get"

    def test_list_operation_config(self):
        """Test that the LIST operation config targets the collection endpoint."""
        assert module_under_test.LIST_OPERATION.uri == LIST_PATH
        assert module_under_test.LIST_OPERATION.http_method == "get"


# ============================================================================
# Test OperationConfig path building
# ============================================================================


class TestOperationConfig:
    """Test OperationConfig path building for this module."""

    def test_get_build_path_with_interface(self):
        """GET path is built from the interface_name parameter."""
        assert (
            module_under_test.GET_OPERATION.build_path({"interface_name": "nic0"})
            == ITEM_PATH
        )

    def test_list_build_path_is_static(self):
        """LIST path is the static collection endpoint."""
        assert module_under_test.LIST_OPERATION.build_path({}) == LIST_PATH


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

    def test_create_module_argument_spec_interface_name_optional(self):
        """Test that interface_name is defined and optional."""
        spec = module_under_test.create_module_argument_spec()

        assert spec["interface_name"]["type"] == "str"
        assert spec["interface_name"].get("required") is not True

    def test_create_module_argument_spec_no_state(self):
        """Test that the info module has no state parameter."""
        spec = module_under_test.create_module_argument_spec()

        assert "state" not in spec
