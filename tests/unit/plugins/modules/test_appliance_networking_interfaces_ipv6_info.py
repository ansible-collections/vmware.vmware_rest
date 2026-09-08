# -*- coding: utf-8 -*-
# Copyright: (c) 2026, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Unit tests for appliance_networking_interfaces_ipv6_info module.

Tests validate the Info module behavior using the OperationConfig-based
architecture with mocked HTTP clients.

``appliance_networking_interfaces_ipv6_info`` is a read-only module that returns
the IPv6 configuration of a single named appliance interface. It performs a GET
against ``/appliance/networking/interfaces/{interface_name}/ipv6`` (there is no
LIST endpoint), so the configuration is always returned as a single resource.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import pytest
from unittest.mock import patch, MagicMock

from ansible_collections.vmware.vmware_rest.plugins.modules import (
    appliance_networking_interfaces_ipv6_info as module_under_test,
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


ITEM_PATH = "/appliance/networking/interfaces/nic0/ipv6"

# A representative GET response for the interface's IPv6 configuration.
SAMPLE_CONFIG = {
    "dhcp": False,
    "autoconf": False,
    "addresses": [{"address": "fc00:10:20:83:20c:29ff:fe94:bb5a", "prefix": 64}],
    "default_gateway": "fc00:10:20:83::1",
}


# ============================================================================
# Test GET Operations
# ============================================================================


def test_get_ipv6_info(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test retrieving the IPv6 configuration of an interface."""
    patch_create_client.return_value = mock_client
    module_args.update({"interface_name": "nic0"})
    mock_module = _run_module(patch_ansible_module, module_args)
    mock_client.get.return_value = _response(200, SAMPLE_CONFIG)

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_module.exit_json.assert_called_once()
    result = exc.value.kwargs
    # value preserves the single-resource dict shape.
    assert result["value"] == SAMPLE_CONFIG
    # info is always a list; the singleton yields exactly one element.
    assert result["info"] == [SAMPLE_CONFIG]
    # The IPv6 config has no recognizable MOID attribute, so no top-level id.
    assert "id" not in result


def test_get_ipv6_info_not_found(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test that a 404 yields empty results instead of failing."""
    patch_create_client.return_value = mock_client
    module_args.update({"interface_name": "nic0"})
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
        mock_client.get.return_value = _response(200, SAMPLE_CONFIG)

        with pytest.raises(AnsibleExitJson) as exc:
            module_under_test.main()

        result = exc.value.kwargs
        assert result["value"] == SAMPLE_CONFIG
        mock_client.get.assert_called_once()


# ============================================================================
# Test API Call Path
# ============================================================================


class TestAPICallPath:
    """Test that the correct API path is called."""

    def test_get_api_path(
        self, patch_create_client, patch_ansible_module, mock_client, module_args
    ):
        """Test that GET uses the interface's IPv6 item path with no query."""
        patch_create_client.return_value = mock_client
        module_args.update({"interface_name": "nic0"})
        _run_module(patch_ansible_module, module_args)
        mock_client.get.return_value = _response(200, SAMPLE_CONFIG)

        with pytest.raises(AnsibleExitJson):
            module_under_test.main()

        mock_client.get.assert_called_once()
        call_args = mock_client.get.call_args
        assert call_args[0][0] == ITEM_PATH
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
        """Test that there is no list API endpoint."""
        assert module_under_test.LIST_ENDPOINT == ""

    def test_item_endpoint(self):
        """Test that the item API endpoint is correct."""
        assert (
            module_under_test.ITEM_ENDPOINT
            == "/appliance/networking/interfaces/{interface_name}/ipv6"
        )

    def test_get_operation_config(self):
        """Test that the GET operation config targets the item endpoint."""
        assert (
            module_under_test.GET_OPERATION.uri
            == "/appliance/networking/interfaces/{interface_name}/ipv6"
        )
        assert module_under_test.GET_OPERATION.http_method == "get"


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

    def test_create_module_argument_spec_interface_name_required(self):
        """Test that interface_name is defined and required."""
        spec = module_under_test.create_module_argument_spec()

        assert spec["interface_name"]["type"] == "str"
        assert spec["interface_name"]["required"] is True

    def test_create_module_argument_spec_no_state(self):
        """Test that the info module has no state parameter."""
        spec = module_under_test.create_module_argument_spec()

        assert "state" not in spec
