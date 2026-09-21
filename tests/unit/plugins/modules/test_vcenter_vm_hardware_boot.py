# -*- coding: utf-8 -*-
# Copyright: (c) 2026, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Unit tests for vcenter_vm_hardware_boot module.

Tests validate the CRUD module behavior using the OperationConfig-based
architecture with mocked HTTP clients. The tests drive the module's main()
entrypoint so the real routing, argument spec, and operation configs are
exercised.

This module is an update-only CRUD module: the boot configuration is a per-VM
singleton addressed by the required C(vm) MOID. It only supports GET and UPDATE
(PATCH) operations (there is no create, delete, list, or action). The tests
therefore focus on the update/idempotency paths and the "resource cannot be
created" behavior.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import pytest
from unittest.mock import patch, MagicMock

from ansible_collections.vmware.vmware_rest.plugins.modules import (
    vcenter_vm_hardware_boot as module_under_test,
)

from ...common.utils import (
    AnsibleExitJson,
    AnsibleFailJson,
    exit_json,
    fail_json,
    set_module_args,
    _response,
)

VM_ID = "vm-1001"

# A realistic boot config response for GET /vcenter/vm/{vm}/hardware/boot.
BOOT_CONFIG = {
    "type": "BIOS",
    "delay": 0,
    "retry": False,
    "retry_delay": 10000,
    "enter_setup_mode": False,
}


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


def _run_module(
    patch_create_client, patch_ansible_module, mock_client, args, check_mode=False
):
    """
    Configure the mocked AnsibleModule/client, run main(), and return the
    mocked module plus the kwargs passed to exit_json.
    """
    patch_create_client.return_value = mock_client
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module
    mock_module.params = set_module_args(args)
    mock_module.exit_json.side_effect = exit_json
    mock_module.fail_json.side_effect = fail_json
    mock_module.check_mode = check_mode

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    return mock_module, exc.value.kwargs


# ============================================================================
# Test state=present - UPDATE
# ============================================================================


def test_ensure_present_updates_delay(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test updating the boot delay when a change is detected."""
    mock_client.get.return_value = _response(200, BOOT_CONFIG)
    mock_client.patch.return_value = _response(204, None)

    module_args.update(
        {
            "state": "present",
            "vm": VM_ID,
            "delay": 10000,
        }
    )
    mock_module, result = _run_module(
        patch_create_client, patch_ansible_module, mock_client, module_args
    )

    mock_module.exit_json.assert_called_once()
    assert result["changed"] is True
    assert result["id"] == VM_ID
    assert result["diff"]["delay"] == {"before": 0, "after": 10000}
    mock_client.patch.assert_called_once()
    call_args = mock_client.patch.call_args
    assert call_args[0][0] == "/vcenter/vm/vm-1001/hardware/boot"
    assert call_args[1]["data"] == {"delay": 10000}


def test_ensure_present_updates_multiple_fields(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test updating several boot settings sends only the requested changes."""
    mock_client.get.return_value = _response(200, BOOT_CONFIG)
    mock_client.patch.return_value = _response(204, None)

    module_args.update(
        {
            "state": "present",
            "vm": VM_ID,
            "type": "EFI",
            "network_protocol": "IPV4",
            "retry": True,
            "retry_delay": 15000,
        }
    )
    mock_module, result = _run_module(
        patch_create_client, patch_ansible_module, mock_client, module_args
    )

    assert result["changed"] is True
    assert result["id"] == VM_ID
    assert result["diff"]["type"] == {"before": "BIOS", "after": "EFI"}
    assert result["diff"]["retry"] == {"before": False, "after": True}
    assert result["diff"]["retry_delay"] == {"before": 10000, "after": 15000}
    # network_protocol is not reported by the BIOS config, so before is None.
    assert result["diff"]["network_protocol"] == {"before": None, "after": "IPV4"}
    mock_client.patch.assert_called_once()
    call_args = mock_client.patch.call_args
    assert call_args[1]["data"] == {
        "type": "EFI",
        "network_protocol": "IPV4",
        "retry": True,
        "retry_delay": 15000,
    }


def test_ensure_present_no_changes(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """
    Test no changes when the requested settings already match the current
    state (idempotent). Read-only fields reported by the API must not register
    as a change because only the keys the user specified are compared.
    """
    mock_client.get.return_value = _response(200, BOOT_CONFIG)

    module_args.update(
        {
            "state": "present",
            "vm": VM_ID,
            "type": "BIOS",
            "delay": 0,
            "retry": False,
        }
    )
    _, result = _run_module(  # pylint: disable=disallowed-name
        patch_create_client, patch_ansible_module, mock_client, module_args
    )

    assert result["changed"] is False
    assert result["id"] == VM_ID
    assert result["diff"] == {}
    mock_client.patch.assert_not_called()


def test_ensure_present_omit_all_settings_noop(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """
    Test that omitting all boot settings results in no update, since the update
    body is empty and nothing is requested to change.
    """
    mock_client.get.return_value = _response(200, BOOT_CONFIG)

    module_args.update({"state": "present", "vm": VM_ID})
    _, result = _run_module(  # pylint: disable=disallowed-name
        patch_create_client, patch_ansible_module, mock_client, module_args
    )

    assert result["changed"] is False
    assert result["diff"] == {}
    mock_client.patch.assert_not_called()


def test_ensure_present_not_found_cannot_create(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """
    Test that when the VM's boot resource cannot be resolved and the module has
    no create operation, it fails rather than attempting a create.
    """
    patch_create_client.return_value = mock_client
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module
    module_args.update(
        {
            "state": "present",
            "vm": "vm-missing",
            "delay": 10000,
        }
    )
    mock_module.params = set_module_args(module_args)
    mock_module.check_mode = False
    mock_module.fail_json.side_effect = fail_json

    mock_client.get.return_value = _response(404, None)

    with pytest.raises(AnsibleFailJson):
        module_under_test.main()

    mock_client.post.assert_not_called()
    mock_client.patch.assert_not_called()


# ============================================================================
# Test Check Mode
# ============================================================================


class TestCheckMode:
    """Test check mode behavior: report a change but make no write HTTP call."""

    def test_update_check_mode(
        self, patch_create_client, patch_ansible_module, mock_client, module_args
    ):
        """Test updating the boot delay in check mode issues no PATCH."""
        mock_client.get.return_value = _response(200, BOOT_CONFIG)

        module_args.update(
            {
                "state": "present",
                "vm": VM_ID,
                "delay": 10000,
            }
        )
        _, result = _run_module(  # pylint: disable=disallowed-name
            patch_create_client,
            patch_ansible_module,
            mock_client,
            module_args,
            check_mode=True,
        )

        assert result["changed"] is True
        assert result["diff"]["delay"] == {"before": 0, "after": 10000}
        mock_client.patch.assert_not_called()

    def test_no_change_check_mode(
        self, patch_create_client, patch_ansible_module, mock_client, module_args
    ):
        """Test check mode reports no change when settings already match."""
        mock_client.get.return_value = _response(200, BOOT_CONFIG)

        module_args.update(
            {
                "state": "present",
                "vm": VM_ID,
                "delay": 0,
            }
        )
        _, result = _run_module(  # pylint: disable=disallowed-name
            patch_create_client,
            patch_ansible_module,
            mock_client,
            module_args,
            check_mode=True,
        )

        assert result["changed"] is False
        assert result["diff"] == {}
        mock_client.patch.assert_not_called()


# ============================================================================
# Test Module Constants
# ============================================================================


class TestModuleConstants:
    """Test that module constants are correctly defined."""

    def test_moid_parameter_hints(self):
        """Test that the MOID parameter hint is the vm identifier."""
        assert module_under_test.MOID_PARAMETER_HINTS == ["vm"]

    def test_list_endpoint(self):
        """Test that there is no list endpoint for this per-VM resource."""
        assert module_under_test.LIST_ENDPOINT == ""

    def test_item_endpoint(self):
        """Test that the item API endpoint is correct."""
        assert module_under_test.ITEM_ENDPOINT == "/vcenter/vm/{vm}/hardware/boot"


# ============================================================================
# Test Argument Spec
# ============================================================================


class TestArgumentSpec:
    """Test the module argument specification."""

    def test_state_parameter(self):
        """Test that the state parameter only supports present."""
        spec = module_under_test.create_module_argument_spec()

        assert spec["state"]["type"] == "str"
        assert spec["state"]["default"] == "present"
        assert spec["state"]["choices"] == ["present"]

    def test_vm_parameter_required(self):
        """Test that the vm parameter is required."""
        spec = module_under_test.create_module_argument_spec()

        assert spec["vm"]["type"] == "str"
        assert spec["vm"]["required"] is True

    def test_optional_scalar_parameters(self):
        """Test the optional boot settings and their types."""
        spec = module_under_test.create_module_argument_spec()

        assert spec["type"]["type"] == "str"
        assert spec["network_protocol"]["type"] == "str"
        assert spec["delay"]["type"] == "int"
        assert spec["retry_delay"]["type"] == "int"
        assert spec["efi_legacy_boot"]["type"] == "bool"
        assert spec["retry"]["type"] == "bool"
        assert spec["enter_setup_mode"]["type"] == "bool"

        # None of the boot settings are required.
        for name in (
            "type",
            "network_protocol",
            "delay",
            "retry_delay",
            "efi_legacy_boot",
            "retry",
            "enter_setup_mode",
        ):
            assert spec[name].get("required", False) is False


# ============================================================================
# Test OperationConfig Building
# ============================================================================


class TestOperationConfig:
    """Test that the module's operation configs build paths and bodies."""

    def test_get_operation(self):
        """Test that the GET operation targets the item endpoint."""
        assert module_under_test.GET_OPERATION.uri == "/vcenter/vm/{vm}/hardware/boot"
        assert module_under_test.GET_OPERATION.http_method == "get"

    def test_update_is_patch(self):
        """Test that the update operation uses the PATCH method."""
        assert module_under_test.UPDATE_OPERATION.http_method == "patch"

    def test_update_build_path(self):
        """Test that the update operation interpolates the vm into the path."""
        path = module_under_test.UPDATE_OPERATION.build_path(params={"vm": VM_ID})
        assert path == "/vcenter/vm/vm-1001/hardware/boot"

    def test_update_build_body(self):
        """Test that the update body carries set params and omits unset ones."""
        config = module_under_test.UPDATE_OPERATION

        assert config.build_body(
            params={"type": "EFI", "delay": 5000, "retry": True}
        ) == {"type": "EFI", "delay": 5000, "retry": True}
        # Optional params omitted -> empty body (not None, since a body_spec exists).
        assert config.build_body(params={"vm": VM_ID}) == {}
