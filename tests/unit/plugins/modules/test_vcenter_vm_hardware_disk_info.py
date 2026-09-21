# -*- coding: utf-8 -*-
# Copyright: (c) 2026, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Unit tests for vcenter_vm_hardware_disk_info module.

Tests validate the info module behavior using the OperationConfig-based
architecture with mocked HTTP clients.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import pytest
from unittest.mock import patch, MagicMock

from ansible_collections.vmware.vmware_rest.plugins.modules import (
    vcenter_vm_hardware_disk_info as module_under_test,
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


def test_get_disk_by_id(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test getting a specific virtual disk by ID."""
    patch_create_client.return_value = mock_client
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module

    module_args.update(
        {
            "vm": "vm-1001",
            "disk": "2000",
        }
    )
    mock_module.params = set_module_args(module_args)
    mock_module.exit_json.side_effect = exit_json
    mock_module.check_mode = False

    get_response = {
        "label": "Hard disk 1",
        "type": "SCSI",
        "scsi": {"bus": 0, "unit": 0},
        "backing": {
            "type": "VMDK_FILE",
            "vmdk_file": "[datastore1] my_vm/my_vm.vmdk",
        },
        "capacity": 17179869184,
    }

    mock_client.get.return_value = _response(200, get_response)

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_module.exit_json.assert_called_once()
    result = exc.value.kwargs
    # The disk GET response body carries no identifier (it is only a path
    # parameter), so no id is derived from it.
    assert "id" not in result
    assert "value" in result
    assert result["value"]["label"] == "Hard disk 1"
    assert result["value"]["type"] == "SCSI"
    assert result["value"]["scsi"]["bus"] == 0
    assert result["value"]["scsi"]["unit"] == 0
    assert result["value"]["backing"]["type"] == "VMDK_FILE"
    assert result["value"]["backing"]["vmdk_file"] == "[datastore1] my_vm/my_vm.vmdk"
    assert result["value"]["capacity"] == 17179869184


def test_get_disk_sata_backing(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test getting a virtual disk attached to a SATA adapter."""
    patch_create_client.return_value = mock_client
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module

    module_args.update(
        {
            "vm": "vm-1001",
            "disk": "16000",
        }
    )
    mock_module.params = set_module_args(module_args)
    mock_module.exit_json.side_effect = exit_json
    mock_module.check_mode = False

    get_response = {
        "label": "Hard disk 2",
        "type": "SATA",
        "sata": {"bus": 0, "unit": 1},
        "backing": {
            "type": "VMDK_FILE",
            "vmdk_file": "[datastore1] my_vm/my_vm_1.vmdk",
        },
        "capacity": 42949672960,
    }

    mock_client.get.return_value = _response(200, get_response)

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_module.exit_json.assert_called_once()
    result = exc.value.kwargs
    assert "id" not in result
    assert result["value"]["type"] == "SATA"
    assert result["value"]["sata"]["bus"] == 0
    assert result["value"]["sata"]["unit"] == 1
    assert result["value"]["backing"]["type"] == "VMDK_FILE"
    assert result["value"]["capacity"] == 42949672960


def test_get_disk_not_found(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test getting a virtual disk that doesn't exist."""
    patch_create_client.return_value = mock_client
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module

    module_args.update(
        {
            "vm": "vm-1001",
            "disk": "2999",
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


def test_list_all_disks(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test listing all virtual disks on a VM."""
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
        {"disk": "2000"},
        {"disk": "2001"},
    ]
    detail_response_1 = {
        "label": "Hard disk 1",
        "type": "SCSI",
        "scsi": {"bus": 0, "unit": 0},
        "backing": {
            "type": "VMDK_FILE",
            "vmdk_file": "[datastore1] my_vm/my_vm.vmdk",
        },
        "capacity": 17179869184,
    }
    detail_response_2 = {
        "label": "Hard disk 2",
        "type": "SATA",
        "sata": {"bus": 0, "unit": 0},
        "backing": {
            "type": "VMDK_FILE",
            "vmdk_file": "[datastore1] my_vm/my_vm_1.vmdk",
        },
        "capacity": 42949672960,
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
    assert result["info"][0]["disk"] == "2000"
    assert result["info"][0]["label"] == "Hard disk 1"
    assert result["info"][0]["type"] == "SCSI"
    assert result["info"][0]["backing"]["type"] == "VMDK_FILE"
    assert result["info"][0]["capacity"] == 17179869184
    assert result["info"][1]["disk"] == "2001"
    assert result["info"][1]["type"] == "SATA"
    assert result["info"][1]["capacity"] == 42949672960


def test_list_disks_empty(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test listing virtual disks when none exist on the VM."""
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


def test_list_single_disk(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test listing when only one virtual disk exists."""
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
        {"disk": "2000"},
    ]
    detail_response = {
        "label": "Hard disk 1",
        "type": "SCSI",
        "scsi": {"bus": 0, "unit": 0},
        "backing": {
            "type": "VMDK_FILE",
            "vmdk_file": "[datastore1] my_vm/my_vm.vmdk",
        },
        "capacity": 17179869184,
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
    assert result["info"][0]["disk"] == "2000"
    assert result["info"][0]["label"] == "Hard disk 1"


# ============================================================================
# Test Check Mode
# ============================================================================


class TestCheckMode:
    """Test check mode behavior."""

    def test_get_check_mode(
        self, patch_create_client, patch_ansible_module, mock_client, module_args
    ):
        """Test getting a virtual disk in check mode (should execute normally)."""
        patch_create_client.return_value = mock_client
        mock_module = MagicMock()
        patch_ansible_module.return_value = mock_module

        module_args.update(
            {
                "vm": "vm-1001",
                "disk": "2000",
            }
        )
        mock_module.params = set_module_args(module_args)
        mock_module.exit_json.side_effect = exit_json
        mock_module.check_mode = True

        get_response = {
            "label": "Hard disk 1",
            "type": "SCSI",
            "scsi": {"bus": 0, "unit": 0},
            "backing": {
                "type": "VMDK_FILE",
                "vmdk_file": "[datastore1] my_vm/my_vm.vmdk",
            },
            "capacity": 17179869184,
        }

        mock_client.get.return_value = _response(200, get_response)

        with pytest.raises(AnsibleExitJson) as exc:
            module_under_test.main()

        result = exc.value.kwargs
        # The disk GET response body carries no identifier, so no id is set.
        assert "id" not in result
        assert "value" in result
        mock_client.get.assert_called_once()

    def test_list_check_mode(
        self, patch_create_client, patch_ansible_module, mock_client, module_args
    ):
        """Test listing virtual disks in check mode (should execute normally)."""
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
            {"disk": "2000"},
        ]
        detail_response = {
            "label": "Hard disk 1",
            "type": "SCSI",
            "scsi": {"bus": 0, "unit": 0},
            "backing": {
                "type": "VMDK_FILE",
                "vmdk_file": "[datastore1] my_vm/my_vm.vmdk",
            },
            "capacity": 17179869184,
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
        assert module_under_test.MOID_PARAMETER_HINTS == ["vm", "disk"]

    def test_list_endpoint(self):
        """Test that list API endpoint is correct."""
        assert module_under_test.LIST_ENDPOINT == "/vcenter/vm/{vm}/hardware/disk"

    def test_item_endpoint(self):
        """Test that item API endpoint is correct."""
        assert (
            module_under_test.ITEM_ENDPOINT == "/vcenter/vm/{vm}/hardware/disk/{disk}"
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

    def test_create_module_argument_spec_disk(self):
        """Test that disk parameter is correctly defined."""
        spec = module_under_test.create_module_argument_spec()

        assert "disk" in spec
        assert spec["disk"]["type"] == "str"

    def test_create_module_argument_spec_no_state(self):
        """Test that info module has no state parameter."""
        spec = module_under_test.create_module_argument_spec()

        assert "state" not in spec
