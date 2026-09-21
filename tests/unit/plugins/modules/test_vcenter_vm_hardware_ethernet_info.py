# -*- coding: utf-8 -*-
# Copyright: (c) 2026, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Unit tests for vcenter_vm_hardware_ethernet_info module.

Tests validate the info module behavior using the OperationConfig-based
architecture with mocked HTTP clients.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import pytest
from unittest.mock import patch, MagicMock

from ansible_collections.vmware.vmware_rest.plugins.modules import (
    vcenter_vm_hardware_ethernet_info as module_under_test,
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
# Test GET Operations (Single Resource)
# ============================================================================


def test_get_ethernet_by_id(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test getting a specific Ethernet adapter by ID."""
    patch_create_client.return_value = mock_client
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module

    module_args.update(
        {
            "vm": "vm-1001",
            "nic": "4000",
        }
    )
    mock_module.params = set_module_args(module_args)
    mock_module.exit_json.side_effect = exit_json
    mock_module.check_mode = False

    get_response = {
        "label": "Network adapter 1",
        "type": "VMXNET3",
        "mac_type": "ASSIGNED",
        "mac_address": "00:50:56:8a:1b:2c",
        "pci_slot_number": 160,
        "state": "CONNECTED",
        "start_connected": True,
        "allow_guest_control": True,
        "wake_on_lan_enabled": False,
        "backing": {
            "type": "STANDARD_PORTGROUP",
            "network": "network-1002",
        },
    }

    mock_client.get.return_value = _response(200, get_response)

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_module.exit_json.assert_called_once()
    result = exc.value.kwargs
    # The Ethernet GET response body carries no identifier (it is only a path
    # parameter), so no id is derived from it.
    assert "id" not in result
    assert "value" in result
    assert result["value"]["label"] == "Network adapter 1"
    assert result["value"]["type"] == "VMXNET3"
    assert result["value"]["mac_type"] == "ASSIGNED"
    assert result["value"]["mac_address"] == "00:50:56:8a:1b:2c"
    assert result["value"]["pci_slot_number"] == 160
    assert result["value"]["state"] == "CONNECTED"
    assert result["value"]["start_connected"] is True
    assert result["value"]["allow_guest_control"] is True
    assert result["value"]["wake_on_lan_enabled"] is False
    assert result["value"]["backing"]["type"] == "STANDARD_PORTGROUP"
    assert result["value"]["backing"]["network"] == "network-1002"


def test_get_ethernet_distributed_portgroup_backing(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test getting an Ethernet adapter backed by a distributed portgroup."""
    patch_create_client.return_value = mock_client
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module

    module_args.update(
        {
            "vm": "vm-1001",
            "nic": "4001",
        }
    )
    mock_module.params = set_module_args(module_args)
    mock_module.exit_json.side_effect = exit_json
    mock_module.check_mode = False

    get_response = {
        "label": "Network adapter 2",
        "type": "E1000E",
        "mac_type": "MANUAL",
        "mac_address": "00:50:56:8a:33:44",
        "state": "NOT_CONNECTED",
        "start_connected": False,
        "allow_guest_control": True,
        "wake_on_lan_enabled": True,
        "backing": {
            "type": "DISTRIBUTED_PORTGROUP",
            "network": "dvportgroup-2005",
            "distributed_port": "12",
        },
    }

    mock_client.get.return_value = _response(200, get_response)

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_module.exit_json.assert_called_once()
    result = exc.value.kwargs
    assert "id" not in result
    assert result["value"]["type"] == "E1000E"
    assert result["value"]["mac_type"] == "MANUAL"
    assert result["value"]["state"] == "NOT_CONNECTED"
    assert result["value"]["start_connected"] is False
    assert result["value"]["backing"]["type"] == "DISTRIBUTED_PORTGROUP"
    assert result["value"]["backing"]["network"] == "dvportgroup-2005"
    assert result["value"]["backing"]["distributed_port"] == "12"


def test_get_ethernet_not_found(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test getting an Ethernet adapter that doesn't exist."""
    patch_create_client.return_value = mock_client
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module

    module_args.update(
        {
            "vm": "vm-1001",
            "nic": "4999",
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
    assert "info" in result
    assert len(result["info"]) == 0


# ============================================================================
# Test LIST Operations (Multiple Resources)
# ============================================================================


def test_list_all_ethernet(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test listing all Ethernet adapters on a VM."""
    patch_create_client.return_value = mock_client
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module

    module_args.update(
        {
            "vm": "vm-1001",
        }
    )
    mock_module.params = set_module_args(module_args)
    mock_module.exit_json.side_effect = exit_json
    mock_module.check_mode = False

    list_response = [
        {"nic": "4000"},
        {"nic": "4001"},
    ]
    detail_response_1 = {
        "label": "Network adapter 1",
        "type": "VMXNET3",
        "mac_address": "00:50:56:8a:1b:2c",
        "state": "CONNECTED",
        "start_connected": True,
        "allow_guest_control": True,
        "backing": {
            "type": "STANDARD_PORTGROUP",
            "network": "network-1002",
        },
    }
    detail_response_2 = {
        "label": "Network adapter 2",
        "type": "E1000E",
        "mac_address": "00:50:56:8a:33:44",
        "state": "NOT_CONNECTED",
        "start_connected": False,
        "allow_guest_control": True,
        "backing": {
            "type": "DISTRIBUTED_PORTGROUP",
            "network": "dvportgroup-2005",
        },
    }

    mock_client.get.side_effect = [
        _response(200, list_response),
        _response(200, detail_response_1),
        _response(200, detail_response_2),
    ]

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_module.exit_json.assert_called_once()
    result = exc.value.kwargs
    assert "info" in result
    assert isinstance(result["info"], list)
    assert len(result["info"]) == 2
    assert result["info"][0]["nic"] == "4000"
    assert result["info"][0]["label"] == "Network adapter 1"
    assert result["info"][0]["type"] == "VMXNET3"
    assert result["info"][0]["backing"]["type"] == "STANDARD_PORTGROUP"
    assert result["info"][1]["nic"] == "4001"
    assert result["info"][1]["type"] == "E1000E"
    assert result["info"][1]["state"] == "NOT_CONNECTED"


def test_list_ethernet_empty(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test listing Ethernet adapters when none exist on the VM."""
    patch_create_client.return_value = mock_client
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module

    module_args.update(
        {
            "vm": "vm-1001",
        }
    )
    mock_module.params = set_module_args(module_args)
    mock_module.exit_json.side_effect = exit_json
    mock_module.check_mode = False

    mock_client.get.return_value = _response(200, [])

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_module.exit_json.assert_called_once()
    result = exc.value.kwargs
    assert "info" in result
    assert len(result["info"]) == 0


def test_list_single_ethernet(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test listing when only one Ethernet adapter exists."""
    patch_create_client.return_value = mock_client
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module

    module_args.update(
        {
            "vm": "vm-1001",
        }
    )
    mock_module.params = set_module_args(module_args)
    mock_module.exit_json.side_effect = exit_json
    mock_module.check_mode = False

    list_response = [
        {"nic": "4000"},
    ]
    detail_response = {
        "label": "Network adapter 1",
        "type": "VMXNET3",
        "mac_address": "00:50:56:8a:1b:2c",
        "state": "CONNECTED",
        "start_connected": True,
        "allow_guest_control": True,
        "backing": {
            "type": "STANDARD_PORTGROUP",
            "network": "network-1002",
        },
    }

    mock_client.get.side_effect = [
        _response(200, list_response),
        _response(200, detail_response),
    ]

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    result = exc.value.kwargs
    assert "info" in result
    assert len(result["info"]) == 1
    assert result["info"][0]["nic"] == "4000"
    assert result["info"][0]["label"] == "Network adapter 1"


# ============================================================================
# Test Check Mode
# ============================================================================


class TestCheckMode:
    """Test check mode behavior."""

    def test_get_check_mode(
        self, patch_create_client, patch_ansible_module, mock_client, module_args
    ):
        """Test getting an Ethernet adapter in check mode (should execute normally)."""
        patch_create_client.return_value = mock_client
        mock_module = MagicMock()
        patch_ansible_module.return_value = mock_module

        module_args.update(
            {
                "vm": "vm-1001",
                "nic": "4000",
            }
        )
        mock_module.params = set_module_args(module_args)
        mock_module.exit_json.side_effect = exit_json
        mock_module.check_mode = True

        get_response = {
            "label": "Network adapter 1",
            "type": "VMXNET3",
            "mac_address": "00:50:56:8a:1b:2c",
            "state": "CONNECTED",
            "start_connected": True,
            "allow_guest_control": True,
            "backing": {
                "type": "STANDARD_PORTGROUP",
                "network": "network-1002",
            },
        }

        mock_client.get.return_value = _response(200, get_response)

        with pytest.raises(AnsibleExitJson) as exc:
            module_under_test.main()

        result = exc.value.kwargs
        # The Ethernet GET response body carries no identifier, so no id is set.
        assert "id" not in result
        assert "value" in result
        mock_client.get.assert_called_once()

    def test_list_check_mode(
        self, patch_create_client, patch_ansible_module, mock_client, module_args
    ):
        """Test listing Ethernet adapters in check mode (should execute normally)."""
        patch_create_client.return_value = mock_client
        mock_module = MagicMock()
        patch_ansible_module.return_value = mock_module

        module_args.update(
            {
                "vm": "vm-1001",
            }
        )
        mock_module.params = set_module_args(module_args)
        mock_module.exit_json.side_effect = exit_json
        mock_module.check_mode = True

        list_response = [
            {"nic": "4000"},
        ]
        detail_response = {
            "label": "Network adapter 1",
            "type": "VMXNET3",
            "mac_address": "00:50:56:8a:1b:2c",
            "state": "CONNECTED",
            "start_connected": True,
            "allow_guest_control": True,
            "backing": {
                "type": "STANDARD_PORTGROUP",
                "network": "network-1002",
            },
        }

        mock_client.get.side_effect = [
            _response(200, list_response),
            _response(200, detail_response),
        ]

        with pytest.raises(AnsibleExitJson) as exc:
            module_under_test.main()

        result = exc.value.kwargs
        assert "info" in result
        assert len(result["info"]) == 1


# ============================================================================
# Test Module Constants
# ============================================================================


class TestModuleConstants:
    """Test that module constants are correctly defined."""

    def test_moid_parameter_hints(self):
        """Test that MOID parameter hints are correct."""
        assert module_under_test.MOID_PARAMETER_HINTS == ["vm", "nic"]

    def test_list_endpoint(self):
        """Test that list API endpoint is correct."""
        assert module_under_test.LIST_ENDPOINT == "/vcenter/vm/{vm}/hardware/ethernet"

    def test_item_endpoint(self):
        """Test that item API endpoint is correct."""
        assert (
            module_under_test.ITEM_ENDPOINT
            == "/vcenter/vm/{vm}/hardware/ethernet/{nic}"
        )


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

    def test_create_module_argument_spec_nic(self):
        """Test that nic parameter is correctly defined."""
        spec = module_under_test.create_module_argument_spec()

        assert "nic" in spec
        assert spec["nic"]["type"] == "str"

    def test_create_module_argument_spec_no_state(self):
        """Test that info module has no state parameter."""
        spec = module_under_test.create_module_argument_spec()

        assert "state" not in spec
