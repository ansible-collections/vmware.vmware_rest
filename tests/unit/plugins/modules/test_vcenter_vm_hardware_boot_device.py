# -*- coding: utf-8 -*-
# Copyright: (c) 2026, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Unit tests for vcenter_vm_hardware_boot_device CRUD module.

This endpoint is a singleton whose GET returns a bare JSON array (the ordered
boot device list) while PUT expects a ``{"devices": [...]}`` body. Because a
list cannot be diffed against the desired body, the module always writes the
requested order and reports ``changed`` with an empty diff.

Tests validate the module behavior using the OperationConfig-based
architecture with mocked HTTP clients.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import pytest
from unittest.mock import patch, MagicMock

from ansible_collections.vmware.vmware_rest.plugins.modules import (
    vcenter_vm_hardware_boot_device as module_under_test,
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
        module_under_test.VmwareRestCrudModuleBase, "_create_client"
    ) as mock:
        yield mock


# ============================================================================
# Test UPDATE (set boot device order) Operations
# ============================================================================


def test_set_boot_device_order(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test setting a multi-device boot order writes the desired list via PUT."""
    patch_create_client.return_value = mock_client
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module

    devices = [
        {"type": "CDROM", "nic": None, "disks": None},
        {"type": "DISK", "nic": None, "disks": ["16000"]},
        {"type": "ETHERNET", "nic": "4000", "disks": None},
    ]
    module_args.update(
        {
            "state": "present",
            "vm": "vm-1001",
            "devices": devices,
        }
    )
    mock_module.params = set_module_args(module_args)
    mock_module.exit_json.side_effect = exit_json
    mock_module.check_mode = False

    # GET returns the current order as a bare list
    mock_client.get.return_value = _response(200, [{"type": "CDROM"}])
    mock_client.put.return_value = _response(204, None)

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_module.exit_json.assert_called_once()
    result = exc.value.kwargs
    assert result["changed"] is True
    assert result["id"] == "vm-1001"

    mock_client.put.assert_called_once()
    put_call = mock_client.put.call_args
    assert put_call[0][0] == "/vcenter/vm/vm-1001/hardware/boot/device"
    assert put_call[1]["data"] == {"devices": devices}


def test_set_boot_device_single_device(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test setting a boot order with a single CD-ROM device."""
    patch_create_client.return_value = mock_client
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module

    devices = [{"type": "CDROM", "nic": None, "disks": None}]
    module_args.update(
        {
            "state": "present",
            "vm": "vm-1001",
            "devices": devices,
        }
    )
    mock_module.params = set_module_args(module_args)
    mock_module.exit_json.side_effect = exit_json
    mock_module.check_mode = False

    mock_client.get.return_value = _response(200, [{"type": "DISK"}])
    mock_client.put.return_value = _response(204, None)

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    result = exc.value.kwargs
    assert result["changed"] is True
    assert result["id"] == "vm-1001"
    mock_client.put.assert_called_once()
    put_call = mock_client.put.call_args
    assert put_call[1]["data"] == {"devices": devices}


def test_set_boot_device_always_reports_changed(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test the order is written even when the current order already matches.

    The endpoint returns a bare list that cannot be diffed, so the module is
    intentionally non-idempotent: it always writes and always reports changed.
    """
    patch_create_client.return_value = mock_client
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module

    devices = [{"type": "CDROM", "nic": None, "disks": None}]
    module_args.update(
        {
            "state": "present",
            "vm": "vm-1001",
            "devices": devices,
        }
    )
    mock_module.params = set_module_args(module_args)
    mock_module.exit_json.side_effect = exit_json
    mock_module.check_mode = False

    # Current order already equals the desired order
    mock_client.get.return_value = _response(200, [{"type": "CDROM"}])
    mock_client.put.return_value = _response(204, None)

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    result = exc.value.kwargs
    assert result["changed"] is True
    mock_client.put.assert_called_once()


# ============================================================================
# Test Check Mode
# ============================================================================


class TestCheckMode:
    """Test check mode behavior."""

    def test_set_boot_device_check_mode(
        self, patch_create_client, patch_ansible_module, mock_client, module_args
    ):
        """Test setting the boot order in check mode makes no PUT call."""
        patch_create_client.return_value = mock_client
        mock_module = MagicMock()
        patch_ansible_module.return_value = mock_module

        module_args.update(
            {
                "state": "present",
                "vm": "vm-1001",
                "devices": [{"type": "CDROM", "nic": None, "disks": None}],
            }
        )
        mock_module.params = set_module_args(module_args)
        mock_module.exit_json.side_effect = exit_json
        mock_module.check_mode = True

        mock_client.get.return_value = _response(200, [{"type": "DISK"}])

        with pytest.raises(AnsibleExitJson) as exc:
            module_under_test.main()

        result = exc.value.kwargs
        assert result["changed"] is True
        assert result["id"] == "vm-1001"
        mock_client.put.assert_not_called()


# ============================================================================
# Test Module Constants
# ============================================================================


class TestModuleConstants:
    """Test that module constants are correctly defined."""

    def test_moid_parameter_hints(self):
        """Test that MOID parameter hints are correct."""
        assert module_under_test.MOID_PARAMETER_HINTS == ["vm"]

    def test_list_endpoint(self):
        """Test that the list API endpoint is empty (no collection endpoint)."""
        assert module_under_test.LIST_ENDPOINT == ""

    def test_item_endpoint(self):
        """Test that the item API endpoint is correct."""
        assert (
            module_under_test.ITEM_ENDPOINT == "/vcenter/vm/{vm}/hardware/boot/device"
        )


# ============================================================================
# Test OperationConfig Definitions
# ============================================================================


class TestOperationConfigs:
    """Test the module's operation config definitions."""

    def test_get_operation(self):
        """Test the GET operation config."""
        assert module_under_test.GET_OPERATION.http_method == "get"
        assert (
            module_under_test.GET_OPERATION.uri
            == "/vcenter/vm/{vm}/hardware/boot/device"
        )

    def test_update_operation_method(self):
        """Test the UPDATE operation uses PUT."""
        assert module_under_test.UPDATE_OPERATION.http_method == "put"

    def test_update_operation_build_path(self):
        """Test the UPDATE operation builds the singleton path from the vm id."""
        path = module_under_test.UPDATE_OPERATION.build_path({"vm": "vm-1001"})
        assert path == "/vcenter/vm/vm-1001/hardware/boot/device"

    def test_update_operation_build_body(self):
        """Test the UPDATE operation wraps the devices list in a body object."""
        devices = [{"type": "CDROM"}, {"type": "DISK", "disks": ["16000"]}]
        body = module_under_test.UPDATE_OPERATION.build_body({"devices": devices})
        assert body == {"devices": devices}


# ============================================================================
# Test Argument Spec
# ============================================================================


class TestArgumentSpec:
    """Test the module argument specification."""

    def test_create_module_argument_spec_state(self):
        """Test that state parameter is correctly defined."""
        spec = module_under_test.create_module_argument_spec()

        assert "state" in spec
        assert spec["state"]["type"] == "str"
        assert spec["state"]["choices"] == ["present"]
        assert spec["state"]["default"] == "present"

    def test_create_module_argument_spec_vm(self):
        """Test that vm parameter is correctly defined."""
        spec = module_under_test.create_module_argument_spec()

        assert "vm" in spec
        assert spec["vm"]["type"] == "str"
        assert spec["vm"]["required"] is True

    def test_create_module_argument_spec_devices(self):
        """Test that devices parameter and its suboptions are correctly defined."""
        spec = module_under_test.create_module_argument_spec()

        assert "devices" in spec
        assert spec["devices"]["type"] == "list"
        assert spec["devices"]["elements"] == "dict"

        options = spec["devices"]["options"]
        assert options["type"]["type"] == "str"
        assert options["type"]["required"] is True
        assert options["type"]["choices"] == ["CDROM", "DISK", "ETHERNET", "FLOPPY"]
        assert options["nic"]["type"] == "str"
        assert options["disks"]["type"] == "list"
        assert options["disks"]["elements"] == "str"
