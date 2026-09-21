# -*- coding: utf-8 -*-
# Copyright: (c) 2026, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Unit tests for vcenter_vm_hardware module.

Tests validate the CRUD module behavior using the OperationConfig-based
architecture with mocked HTTP clients. The tests drive the module's main()
entrypoint so the real routing, argument spec, and operation configs are
exercised.

This module manages the top-level virtual hardware settings of a per-VM
singleton addressed by the required C(vm) MOID. It supports GET and UPDATE
(PATCH) for O(state=present) and an C(upgrade) POST action for O(state=upgrade).
There is no create, delete, or list operation, so the tests focus on the
update/idempotency paths, the upgrade action, and the "resource cannot be
created" behavior.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import pytest
from unittest.mock import patch, MagicMock

from ansible_collections.vmware.vmware_rest.plugins.modules import (
    vcenter_vm_hardware as module_under_test,
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

# A realistic hardware settings response for GET /vcenter/vm/{vm}/hardware.
# The Vcenter.Vm.Hardware.Info schema always reports version, upgrade_policy,
# and upgrade_status; upgrade_version is only present once one is scheduled.
HARDWARE_INFO = {
    "version": "VMX_19",
    "upgrade_policy": "NEVER",
    "upgrade_status": "NONE",
}

# A hardware settings response with a scheduled upgrade already configured.
HARDWARE_INFO_SCHEDULED = {
    "version": "VMX_19",
    "upgrade_policy": "AFTER_CLEAN_SHUTDOWN",
    "upgrade_version": "VMX_21",
    "upgrade_status": "READY",
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


def test_ensure_present_schedules_upgrade(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test scheduling an upgrade policy/version sends only the requested changes."""
    mock_client.get.return_value = _response(200, HARDWARE_INFO)
    mock_client.patch.return_value = _response(204, None)

    module_args.update(
        {
            "state": "present",
            "vm": VM_ID,
            "upgrade_policy": "AFTER_CLEAN_SHUTDOWN",
            "upgrade_version": "VMX_21",
        }
    )
    mock_module, result = _run_module(
        patch_create_client, patch_ansible_module, mock_client, module_args
    )

    mock_module.exit_json.assert_called_once()
    assert result["changed"] is True
    assert result["id"] == VM_ID
    assert result["diff"]["upgrade_policy"] == {
        "before": "NEVER",
        "after": "AFTER_CLEAN_SHUTDOWN",
    }
    # upgrade_version is not reported for a NEVER policy, so before is None.
    assert result["diff"]["upgrade_version"] == {"before": None, "after": "VMX_21"}
    mock_client.patch.assert_called_once()
    call_args = mock_client.patch.call_args
    assert call_args[0][0] == "/vcenter/vm/vm-1001/hardware"
    assert call_args[1]["data"] == {
        "upgrade_policy": "AFTER_CLEAN_SHUTDOWN",
        "upgrade_version": "VMX_21",
    }


def test_ensure_present_updates_policy_only(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test disabling scheduled upgrades updates only the policy."""
    mock_client.get.return_value = _response(200, HARDWARE_INFO_SCHEDULED)
    mock_client.patch.return_value = _response(204, None)

    module_args.update(
        {
            "state": "present",
            "vm": VM_ID,
            "upgrade_policy": "NEVER",
        }
    )
    _, result = _run_module(  # pylint: disable=disallowed-name
        patch_create_client, patch_ansible_module, mock_client, module_args
    )

    assert result["changed"] is True
    assert result["id"] == VM_ID
    assert result["diff"]["upgrade_policy"] == {
        "before": "AFTER_CLEAN_SHUTDOWN",
        "after": "NEVER",
    }
    assert "upgrade_version" not in result["diff"]
    mock_client.patch.assert_called_once()
    call_args = mock_client.patch.call_args
    assert call_args[1]["data"] == {"upgrade_policy": "NEVER"}


def test_ensure_present_no_changes(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """
    Test no changes when the requested settings already match the current
    state (idempotent). Read-only fields reported by the API must not register
    as a change because only the keys the user specified are compared.
    """
    mock_client.get.return_value = _response(200, HARDWARE_INFO_SCHEDULED)

    module_args.update(
        {
            "state": "present",
            "vm": VM_ID,
            "upgrade_policy": "AFTER_CLEAN_SHUTDOWN",
            "upgrade_version": "VMX_21",
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
    Test that omitting all hardware settings results in no update, since the
    update body is empty and nothing is requested to change.
    """
    mock_client.get.return_value = _response(200, HARDWARE_INFO)

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
    Test that when the VM's hardware resource cannot be resolved and the module
    has no create operation, it fails rather than attempting a create.
    """
    patch_create_client.return_value = mock_client
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module
    module_args.update(
        {
            "state": "present",
            "vm": "vm-missing",
            "upgrade_policy": "ALWAYS",
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
# Test state=upgrade - ACTION
# ============================================================================


def test_upgrade_action_with_version(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test the upgrade action POSTs to the action endpoint with the version."""
    mock_client.post.return_value = _response(204, None)

    module_args.update(
        {
            "state": "upgrade",
            "vm": VM_ID,
            "version": "VMX_22",
        }
    )
    mock_module, result = _run_module(
        patch_create_client, patch_ansible_module, mock_client, module_args
    )

    mock_module.exit_json.assert_called_once()
    assert result["changed"] is True
    assert result["id"] == VM_ID
    mock_client.post.assert_called_once()
    call_args = mock_client.post.call_args
    assert call_args[1]["path"] == "/vcenter/vm/vm-1001/hardware?action=upgrade"
    assert call_args[1]["data"] == {"version": "VMX_22"}
    # An action never inspects current state, so no GET is issued.
    mock_client.get.assert_not_called()


def test_upgrade_action_without_version(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test the upgrade action omits the version to use the server default."""
    mock_client.post.return_value = _response(204, None)

    module_args.update(
        {
            "state": "upgrade",
            "vm": VM_ID,
        }
    )
    _, result = _run_module(  # pylint: disable=disallowed-name
        patch_create_client, patch_ansible_module, mock_client, module_args
    )

    assert result["changed"] is True
    assert result["id"] == VM_ID
    mock_client.post.assert_called_once()
    call_args = mock_client.post.call_args
    assert call_args[1]["path"] == "/vcenter/vm/vm-1001/hardware?action=upgrade"
    assert call_args[1]["data"] == {}


# ============================================================================
# Test Check Mode
# ============================================================================


class TestCheckMode:
    """Test check mode behavior: report a change but make no write HTTP call."""

    def test_update_check_mode(
        self, patch_create_client, patch_ansible_module, mock_client, module_args
    ):
        """Test updating the upgrade policy in check mode issues no PATCH."""
        mock_client.get.return_value = _response(200, HARDWARE_INFO)

        module_args.update(
            {
                "state": "present",
                "vm": VM_ID,
                "upgrade_policy": "ALWAYS",
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
        assert result["diff"]["upgrade_policy"] == {
            "before": "NEVER",
            "after": "ALWAYS",
        }
        mock_client.patch.assert_not_called()

    def test_no_change_check_mode(
        self, patch_create_client, patch_ansible_module, mock_client, module_args
    ):
        """Test check mode reports no change when settings already match."""
        mock_client.get.return_value = _response(200, HARDWARE_INFO)

        module_args.update(
            {
                "state": "present",
                "vm": VM_ID,
                "upgrade_policy": "NEVER",
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

    def test_upgrade_action_check_mode(
        self, patch_create_client, patch_ansible_module, mock_client, module_args
    ):
        """Test the upgrade action reports a change but issues no POST in check mode."""
        module_args.update(
            {
                "state": "upgrade",
                "vm": VM_ID,
                "version": "VMX_22",
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
        assert result["id"] == VM_ID
        mock_client.post.assert_not_called()


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
        assert module_under_test.ITEM_ENDPOINT == "/vcenter/vm/{vm}/hardware"


# ============================================================================
# Test Argument Spec
# ============================================================================


class TestArgumentSpec:
    """Test the module argument specification."""

    def test_state_parameter(self):
        """Test that state supports present (default) and upgrade."""
        spec = module_under_test.create_module_argument_spec()

        assert spec["state"]["type"] == "str"
        assert spec["state"]["default"] == "present"
        assert spec["state"]["choices"] == ["present", "upgrade"]

    def test_vm_parameter_required(self):
        """Test that the vm parameter is required."""
        spec = module_under_test.create_module_argument_spec()

        assert spec["vm"]["type"] == "str"
        assert spec["vm"]["required"] is True

    def test_optional_scalar_parameters(self):
        """Test the optional hardware settings and their types."""
        spec = module_under_test.create_module_argument_spec()

        assert spec["upgrade_policy"]["type"] == "str"
        assert spec["upgrade_version"]["type"] == "str"
        assert spec["version"]["type"] == "str"

        # None of the hardware settings are required.
        for name in ("upgrade_policy", "upgrade_version", "version"):
            assert spec[name].get("required", False) is False


# ============================================================================
# Test OperationConfig Building
# ============================================================================


class TestOperationConfig:
    """Test that the module's operation configs build paths and bodies."""

    def test_get_operation(self):
        """Test that the GET operation targets the item endpoint."""
        assert module_under_test.GET_OPERATION.uri == "/vcenter/vm/{vm}/hardware"
        assert module_under_test.GET_OPERATION.http_method == "get"

    def test_update_is_patch(self):
        """Test that the update operation uses the PATCH method."""
        assert module_under_test.UPDATE_OPERATION.http_method == "patch"

    def test_update_build_path(self):
        """Test that the update operation interpolates the vm into the path."""
        path = module_under_test.UPDATE_OPERATION.build_path(params={"vm": VM_ID})
        assert path == "/vcenter/vm/vm-1001/hardware"

    def test_update_build_body(self):
        """Test that the update body carries set params and omits unset ones."""
        config = module_under_test.UPDATE_OPERATION

        assert config.build_body(
            params={"upgrade_policy": "ALWAYS", "upgrade_version": "VMX_21"}
        ) == {"upgrade_policy": "ALWAYS", "upgrade_version": "VMX_21"}
        # Optional params omitted -> empty body (not None, since a body_spec exists).
        assert config.build_body(params={"vm": VM_ID}) == {}

    def test_upgrade_action_operation(self):
        """Test that the upgrade action posts to the action endpoint."""
        action = module_under_test.ACTION_OPERATIONS["upgrade"]

        assert action.http_method == "post"
        assert (
            action.build_path(params={"vm": VM_ID})
            == "/vcenter/vm/vm-1001/hardware?action=upgrade"
        )
        assert action.build_body(params={"version": "VMX_22"}) == {"version": "VMX_22"}
        # version is optional -> empty body when omitted.
        assert action.build_body(params={"vm": VM_ID}) == {}
