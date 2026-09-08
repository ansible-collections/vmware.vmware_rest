# -*- coding: utf-8 -*-
# Copyright: (c) 2026, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Unit tests for appliance_networking_interfaces_ipv6 module.

Tests validate the CRUD module behavior using the OperationConfig-based
architecture with mocked HTTP clients.

``appliance_networking_interfaces_ipv6`` manages the IPv6 configuration of a
single named appliance interface. The resource is addressed by the
``interface_name`` path parameter and there is no CREATE, DELETE or LIST
endpoint. It supports a single state:

- ``present`` - GET the current IPv6 configuration for the interface and PUT the
  desired configuration when it differs from the current state.

Unlike the IPv4 module, every field in the UPDATE body (``dhcp``, ``autoconf``,
``addresses`` and ``default_gateway``) is required, so an update request must
supply all of them.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import pytest
from unittest.mock import patch, MagicMock

from ansible_collections.vmware.vmware_rest.plugins.modules import (
    appliance_networking_interfaces_ipv6 as module_under_test,
)
from ansible_collections.vmware.vmware_rest.plugins.module_utils._errors import (
    RequiredParameterError,
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


ITEM_PATH = "/appliance/networking/interfaces/nic0/ipv6"

# The desired addresses use the Ipv6.Address shape (address + prefix only),
# which is what the PUT body carries.
ADDRESSES = [{"address": "fc00:10:20:83:20c:29ff:fe94:bb5a", "prefix": 64}]

# The GET response uses the Ipv6.AddressInfo shape, which adds the read-only
# origin and status fields the API reports but that the module never sends.
CURRENT_ADDRESSES = [
    {
        "address": "fc00:10:20:83:20c:29ff:fe94:bb5a",
        "prefix": 64,
        "origin": "STATIC",
        "status": "PREFERRED",
    }
]

# A representative GET response for the interface's IPv6 configuration.
CURRENT_CONFIG = {
    "dhcp": False,
    "autoconf": False,
    "addresses": CURRENT_ADDRESSES,
    "default_gateway": "fc00:10:20:83::1",
}


# ============================================================================
# Test state=present (UPDATE) Operations
# ============================================================================


def test_present_updates_default_gateway(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test changing the default gateway puts the desired configuration."""
    patch_create_client.return_value = mock_client
    module_args.update(
        {
            "state": "present",
            "interface_name": "nic0",
            "dhcp": False,
            "autoconf": False,
            "addresses": ADDRESSES,
            "default_gateway": "fc00:10:20:83::254",
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
        "default_gateway": {
            "before": "fc00:10:20:83::1",
            "after": "fc00:10:20:83::254",
        }
    }

    mock_client.put.assert_called_once()
    call_args = mock_client.put.call_args
    assert call_args[0][0] == ITEM_PATH
    # All required fields are sent, even the unchanged ones.
    assert call_args[1]["data"] == {
        "dhcp": False,
        "autoconf": False,
        "addresses": ADDRESSES,
        "default_gateway": "fc00:10:20:83::254",
    }


def test_present_enables_dhcp(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test enabling DHCP is reported as a boolean change and written."""
    patch_create_client.return_value = mock_client
    module_args.update(
        {
            "state": "present",
            "interface_name": "nic0",
            "dhcp": True,
            "autoconf": False,
            "addresses": ADDRESSES,
            "default_gateway": "fc00:10:20:83::1",
        }
    )
    _run_module(patch_ansible_module, module_args)

    mock_client.get.return_value = _response(200, CURRENT_CONFIG)
    mock_client.put.return_value = _response(200, {})

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    result = exc.value.kwargs
    assert result["changed"] is True
    assert result["diff"] == {"dhcp": {"before": False, "after": True}}

    mock_client.put.assert_called_once()
    assert mock_client.put.call_args[1]["data"]["dhcp"] is True


def test_present_updates_addresses(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test replacing the statically assigned addresses puts the change."""
    patch_create_client.return_value = mock_client
    new_addresses = [{"address": "fc00:10:20:83:20c:29ff:fe94:0001", "prefix": 64}]
    module_args.update(
        {
            "state": "present",
            "interface_name": "nic0",
            "dhcp": False,
            "autoconf": False,
            "addresses": new_addresses,
            "default_gateway": "fc00:10:20:83::1",
        }
    )
    _run_module(patch_ansible_module, module_args)

    mock_client.get.return_value = _response(200, CURRENT_CONFIG)
    mock_client.put.return_value = _response(200, {})

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    result = exc.value.kwargs
    assert result["changed"] is True
    assert result["diff"] == {
        "addresses": {"before": CURRENT_ADDRESSES, "after": new_addresses}
    }
    mock_client.put.assert_called_once()


def test_present_idempotent(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test no change when the configuration already matches the request."""
    patch_create_client.return_value = mock_client
    module_args.update(
        {
            "state": "present",
            "interface_name": "nic0",
            "dhcp": False,
            "autoconf": False,
            "addresses": ADDRESSES,
            "default_gateway": "fc00:10:20:83::1",
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
                "dhcp": False,
                "autoconf": False,
                "addresses": ADDRESSES,
                "default_gateway": "fc00:10:20:83::254",
            }
        )
        _run_module(patch_ansible_module, module_args, check_mode=True)

        mock_client.get.return_value = _response(200, CURRENT_CONFIG)

        with pytest.raises(AnsibleExitJson) as exc:
            module_under_test.main()

        result = exc.value.kwargs
        assert result["changed"] is True
        assert result["diff"] == {
            "default_gateway": {
                "before": "fc00:10:20:83::1",
                "after": "fc00:10:20:83::254",
            }
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
        """Test that GET and PUT target the interface's IPv6 item path."""
        patch_create_client.return_value = mock_client
        module_args.update(
            {
                "state": "present",
                "interface_name": "nic0",
                "dhcp": False,
                "autoconf": False,
                "addresses": ADDRESSES,
                "default_gateway": "fc00:10:20:83::254",
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
            == "/appliance/networking/interfaces/{interface_name}/ipv6"
        )

    def test_get_operation_config(self):
        """Test that the GET operation config targets the item endpoint."""
        assert (
            module_under_test.GET_OPERATION.uri
            == "/appliance/networking/interfaces/{interface_name}/ipv6"
        )
        assert module_under_test.GET_OPERATION.http_method == "get"

    def test_update_operation_config(self):
        """Test that the UPDATE operation config is a PUT on the item endpoint."""
        assert (
            module_under_test.UPDATE_OPERATION.uri
            == "/appliance/networking/interfaces/{interface_name}/ipv6"
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
        """UPDATE body contains every required field."""
        body = module_under_test.UPDATE_OPERATION.build_body(
            {
                "dhcp": False,
                "autoconf": False,
                "addresses": ADDRESSES,
                "default_gateway": "fc00:10:20:83::1",
            }
        )
        assert body == {
            "dhcp": False,
            "autoconf": False,
            "addresses": ADDRESSES,
            "default_gateway": "fc00:10:20:83::1",
        }

    def test_update_build_body_missing_required_raises(self):
        """UPDATE body building fails when a required field is missing."""
        with pytest.raises(RequiredParameterError):
            module_under_test.UPDATE_OPERATION.build_body(
                {
                    "dhcp": False,
                    "autoconf": False,
                    "addresses": ADDRESSES,
                    # default_gateway omitted
                }
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
        """Test that the IPv6 configuration parameters are defined and optional."""
        spec = module_under_test.create_module_argument_spec()

        assert spec["dhcp"]["type"] == "bool"
        assert spec["autoconf"]["type"] == "bool"
        assert spec["default_gateway"]["type"] == "str"
        assert spec["addresses"]["type"] == "list"
        for name in ("dhcp", "autoconf", "default_gateway", "addresses"):
            assert not spec[name].get("required", False)

    def test_create_module_argument_spec_addresses_suboptions(self):
        """Test that the addresses element suboptions are defined and required."""
        spec = module_under_test.create_module_argument_spec()

        assert spec["addresses"]["elements"] == "dict"
        suboptions = spec["addresses"]["options"]
        assert suboptions["address"]["type"] == "str"
        assert suboptions["address"]["required"] is True
        assert suboptions["prefix"]["type"] == "int"
        assert suboptions["prefix"]["required"] is True
