# -*- coding: utf-8 -*-
# Copyright: (c) 2026, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Unit tests for appliance_networking_interfaces_ipv4 module.

Tests validate the CRUD module behavior using the OperationConfig-based
architecture with mocked HTTP clients.

``appliance_networking_interfaces_ipv4`` manages the IPv4 configuration of a
single named appliance interface. The resource is addressed by the
``interface_name`` path parameter and there is no CREATE, DELETE or LIST
endpoint. It supports a single state:

- ``present`` - GET the current IPv4 configuration for the interface and PUT the
  desired configuration when it differs from the current state.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import pytest
from unittest.mock import patch, MagicMock

from ansible_collections.vmware.vmware_rest.plugins.modules import (
    appliance_networking_interfaces_ipv4 as module_under_test,
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
        module_under_test.VmwareRestCrudModuleBase, "_create_client"
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


ITEM_PATH = "/appliance/networking/interfaces/nic0/ipv4"

# A representative GET response for the interface's IPv4 configuration.
CURRENT_CONFIG = {
    "mode": "STATIC",
    "address": "10.20.80.191",
    "prefix": 24,
    "default_gateway": "10.20.80.1",
    "configurable": True,
}


# ============================================================================
# Test state=present (UPDATE) Operations
# ============================================================================


def test_present_updates_address(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test changing the static address puts the desired configuration."""
    patch_create_client.return_value = mock_client
    module_args.update(
        {
            "state": "present",
            "interface_name": "nic0",
            "mode": "STATIC",
            "address": "10.20.80.200",
            "prefix": 24,
            "default_gateway": "10.20.80.1",
        }
    )
    mock_module = _run_module(patch_ansible_module, module_args)

    mock_client.get.return_value = _response(200, CURRENT_CONFIG)
    mock_client.put.return_value = _response(200, {})

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_module.exit_json.assert_called_once()
    result = exc.value.kwargs
    assert result["changed"] is True
    assert result["id"] == "nic0"
    assert result["diff"] == {
        "address": {"before": "10.20.80.191", "after": "10.20.80.200"}
    }

    mock_client.put.assert_called_once()
    call_args = mock_client.put.call_args
    assert call_args[0][0] == ITEM_PATH
    assert call_args[1]["data"] == {
        "mode": "STATIC",
        "address": "10.20.80.200",
        "prefix": 24,
        "default_gateway": "10.20.80.1",
    }


def test_present_switches_to_dhcp(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test switching the address assignment mode to DHCP puts the change."""
    patch_create_client.return_value = mock_client
    module_args.update(
        {
            "state": "present",
            "interface_name": "nic0",
            "mode": "DHCP",
        }
    )
    _run_module(patch_ansible_module, module_args)

    mock_client.get.return_value = _response(200, CURRENT_CONFIG)
    mock_client.put.return_value = _response(200, {})

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    result = exc.value.kwargs
    assert result["changed"] is True
    assert result["diff"] == {"mode": {"before": "STATIC", "after": "DHCP"}}

    mock_client.put.assert_called_once()
    # Only the supplied mode is sent; unset optional fields are omitted.
    assert mock_client.put.call_args[1]["data"] == {"mode": "DHCP"}


def test_present_idempotent(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test no change when the configuration already matches the request."""
    patch_create_client.return_value = mock_client
    module_args.update(
        {
            "state": "present",
            "interface_name": "nic0",
            "mode": "STATIC",
            "address": "10.20.80.191",
            "prefix": 24,
            "default_gateway": "10.20.80.1",
        }
    )
    mock_module = _run_module(patch_ansible_module, module_args)

    mock_client.get.return_value = _response(200, CURRENT_CONFIG)

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_module.exit_json.assert_called_once()
    result = exc.value.kwargs
    assert result["changed"] is False
    assert result["id"] == "nic0"
    assert result["diff"] == {}
    # The current state is read, but nothing is written.
    mock_client.get.assert_called_once()
    mock_client.put.assert_not_called()


# ============================================================================
# Test Check Mode
# ============================================================================


class TestCheckMode:
    """Test check mode behavior."""

    def test_present_check_mode(
        self, patch_create_client, patch_ansible_module, mock_client, module_args
    ):
        """Test that an update in check mode reports change without writing."""
        patch_create_client.return_value = mock_client
        module_args.update(
            {
                "state": "present",
                "interface_name": "nic0",
                "mode": "STATIC",
                "address": "10.20.80.200",
                "prefix": 24,
                "default_gateway": "10.20.80.1",
            }
        )
        _run_module(patch_ansible_module, module_args, check_mode=True)

        mock_client.get.return_value = _response(200, CURRENT_CONFIG)

        with pytest.raises(AnsibleExitJson) as exc:
            module_under_test.main()

        result = exc.value.kwargs
        assert result["changed"] is True
        assert result["diff"] == {
            "address": {"before": "10.20.80.191", "after": "10.20.80.200"}
        }
        mock_client.put.assert_not_called()


# ============================================================================
# Test API Call Path
# ============================================================================


class TestAPICallPath:
    """Test that the correct API paths are called."""

    def test_get_and_put_api_path(
        self, patch_create_client, patch_ansible_module, mock_client, module_args
    ):
        """Test that GET and PUT target the interface's IPv4 item path."""
        patch_create_client.return_value = mock_client
        module_args.update(
            {
                "state": "present",
                "interface_name": "nic0",
                "mode": "STATIC",
                "address": "10.20.80.200",
            }
        )
        _run_module(patch_ansible_module, module_args)

        mock_client.get.return_value = _response(200, CURRENT_CONFIG)
        mock_client.put.return_value = _response(200, {})

        with pytest.raises(AnsibleExitJson):
            module_under_test.main()

        assert mock_client.get.call_args[0][0] == ITEM_PATH
        assert mock_client.put.call_args[0][0] == ITEM_PATH


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
            == "/appliance/networking/interfaces/{interface_name}/ipv4"
        )

    def test_get_operation_config(self):
        """Test that the GET operation config targets the item endpoint."""
        assert (
            module_under_test.GET_OPERATION.uri
            == "/appliance/networking/interfaces/{interface_name}/ipv4"
        )
        assert module_under_test.GET_OPERATION.http_method == "get"

    def test_update_operation_config(self):
        """Test that the UPDATE operation config is a PUT on the item endpoint."""
        assert (
            module_under_test.UPDATE_OPERATION.uri
            == "/appliance/networking/interfaces/{interface_name}/ipv4"
        )
        assert module_under_test.UPDATE_OPERATION.http_method == "put"


# ============================================================================
# Test OperationConfig path/body building
# ============================================================================


class TestOperationConfig:
    """Test OperationConfig path and body building for this module."""

    def test_get_build_path_with_interface(self):
        """GET path is built from the interface_name parameter."""
        assert (
            module_under_test.GET_OPERATION.build_path({"interface_name": "nic0"})
            == ITEM_PATH
        )

    def test_update_build_body_full(self):
        """UPDATE body contains every supplied field."""
        body = module_under_test.UPDATE_OPERATION.build_body(
            {
                "mode": "STATIC",
                "address": "10.20.80.200",
                "prefix": 24,
                "default_gateway": "10.20.80.1",
            }
        )
        assert body == {
            "mode": "STATIC",
            "address": "10.20.80.200",
            "prefix": 24,
            "default_gateway": "10.20.80.1",
        }

    def test_update_build_body_omits_unset_optionals(self):
        """UPDATE body only contains the required mode when optionals are unset."""
        body = module_under_test.UPDATE_OPERATION.build_body({"mode": "DHCP"})
        assert body == {"mode": "DHCP"}


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

    def test_create_module_argument_spec_state(self):
        """Test that the state parameter is correctly defined."""
        spec = module_under_test.create_module_argument_spec()

        assert spec["state"]["type"] == "str"
        assert spec["state"]["choices"] == ["present"]
        assert spec["state"]["default"] == "present"

    def test_create_module_argument_spec_interface_name_required(self):
        """Test that interface_name is defined and required."""
        spec = module_under_test.create_module_argument_spec()

        assert spec["interface_name"]["type"] == "str"
        assert spec["interface_name"]["required"] is True

    def test_create_module_argument_spec_optional_params(self):
        """Test that the IPv4 configuration parameters are defined and optional."""
        spec = module_under_test.create_module_argument_spec()

        assert spec["mode"]["type"] == "str"
        assert spec["address"]["type"] == "str"
        assert spec["prefix"]["type"] == "int"
        assert spec["default_gateway"]["type"] == "str"
        for name in ("mode", "address", "prefix", "default_gateway"):
            assert not spec[name].get("required", False)
