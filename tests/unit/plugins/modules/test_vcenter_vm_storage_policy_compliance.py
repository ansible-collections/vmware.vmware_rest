# -*- coding: utf-8 -*-
# Copyright: (c) 2026, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Unit tests for vcenter_vm_storage_policy_compliance module.

Tests validate the action-based module behavior using the OperationConfig-based
architecture with mocked HTTP clients. This module exposes a single C(check)
action that forces a fresh storage policy compliance evaluation against the
``{vm}`` endpoint, so the operation is never idempotent.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import pytest
from unittest.mock import patch, MagicMock

from ansible_collections.vmware.vmware_rest.plugins.modules import (
    vcenter_vm_storage_policy_compliance as module_under_test,
)

from ...common.utils import (
    AnsibleExitJson,
    AnsibleFailJson,
    exit_json,
    fail_json,
    set_module_args,
    _response,
)

VM_ID = "vm-42"

# A realistic response for the check action (Compliance.Info schema).
COMPLIANCE_INFO = {
    "overall_compliance": "COMPLIANT",
    "vm_home": "COMPLIANT",
    "disks": {"disk-2000": "COMPLIANT"},
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
    kwargs passed to exit_json.
    """
    patch_create_client.return_value = mock_client
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module
    mock_module.params = set_module_args(args)
    mock_module.exit_json.side_effect = exit_json
    mock_module.check_mode = check_mode

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    return mock_module, exc.value.kwargs


# ============================================================================
# Test ACTION Operations - check
# ============================================================================


def test_action_check(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test running a compliance check on the VM home directory."""
    mock_client.post.return_value = _response(200, COMPLIANCE_INFO)

    module_args.update(
        {
            "state": "check",
            "vm": VM_ID,
            "vm_home": True,
        }
    )
    mock_module, result = _run_module(
        patch_create_client, patch_ansible_module, mock_client, module_args
    )

    mock_module.exit_json.assert_called_once()
    # The check action is not idempotent; it always reports a change.
    assert result["changed"] is True
    assert result["id"] == VM_ID
    assert result["value"] == COMPLIANCE_INFO
    mock_client.post.assert_called_once()

    call_args = mock_client.post.call_args
    assert (
        call_args[1]["path"]
        == "/vcenter/vm/vm-42/storage/policy/compliance?action=check"
    )
    assert call_args[1]["data"] == {"vm_home": True}
    # No query spec is defined; the action is encoded in the URI.
    assert "query" not in call_args[1]


def test_action_check_with_disks(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test running a compliance check scoped to specific disks."""
    mock_client.post.return_value = _response(200, COMPLIANCE_INFO)

    module_args.update(
        {
            "state": "check",
            "vm": VM_ID,
            "vm_home": False,
            "disks": ["disk-2000", "disk-2001"],
        }
    )
    _run_module(patch_create_client, patch_ansible_module, mock_client, module_args)

    call_args = mock_client.post.call_args
    assert call_args[1]["data"] == {
        "vm_home": False,
        "disks": ["disk-2000", "disk-2001"],
    }


def test_action_check_omits_unset_disks(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test that the optional disks parameter is excluded when not provided."""
    mock_client.post.return_value = _response(200, COMPLIANCE_INFO)

    module_args.update(
        {
            "state": "check",
            "vm": VM_ID,
            "vm_home": True,
            "disks": None,
        }
    )
    _run_module(patch_create_client, patch_ansible_module, mock_client, module_args)

    call_args = mock_client.post.call_args
    assert "disks" not in call_args[1]["data"]


def test_action_check_requires_vm_home(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test that omitting the API-required vm_home parameter fails cleanly."""
    patch_create_client.return_value = mock_client
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module
    module_args.update(
        {
            "state": "check",
            "vm": VM_ID,
        }
    )
    mock_module.params = set_module_args(module_args)
    mock_module.check_mode = False
    mock_module.fail_json.side_effect = fail_json

    with pytest.raises(AnsibleFailJson) as exc:
        module_under_test.main()

    # vm_home is required by the API CheckSpec, so no request should be sent.
    mock_client.post.assert_not_called()
    assert exc.value.kwargs["module_param_name"] == "vm_home"


# ============================================================================
# Test Check Mode
# ============================================================================


class TestCheckMode:
    """Test check mode behavior: the action reports a change but makes no HTTP call."""

    def test_check_check_mode(
        self, patch_create_client, patch_ansible_module, mock_client, module_args
    ):
        """Test the check action in check mode."""
        module_args.update(
            {
                "state": "check",
                "vm": VM_ID,
                "vm_home": True,
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
        assert result["value"] == {}
        mock_client.post.assert_not_called()


# ============================================================================
# Test Module Constants
# ============================================================================


class TestModuleConstants:
    """Test that module constants are correctly defined."""

    def test_moid_parameter_hints(self):
        """Test that MOID parameter hints are correct."""
        assert module_under_test.MOID_PARAMETER_HINTS == ["vm"]

    def test_list_endpoint(self):
        """Test that the list API endpoint is empty (action-only endpoint)."""
        assert module_under_test.LIST_ENDPOINT == ""

    def test_item_endpoint(self):
        """Test that the item API endpoint is correct."""
        assert (
            module_under_test.ITEM_ENDPOINT
            == "/vcenter/vm/{vm}/storage/policy/compliance"
        )

    def test_action_operations_keys(self):
        """Test that only the check action is defined."""
        assert set(module_under_test.ACTION_OPERATIONS.keys()) == {"check"}


# ============================================================================
# Test Argument Spec
# ============================================================================


class TestArgumentSpec:
    """Test the module argument specification."""

    def test_state_parameter(self):
        """Test that the state parameter is correctly defined."""
        spec = module_under_test.create_module_argument_spec()

        assert spec["state"]["type"] == "str"
        assert spec["state"]["required"] is True
        assert spec["state"]["choices"] == ["check"]

    def test_vm_parameter_required(self):
        """Test that the vm parameter is required."""
        spec = module_under_test.create_module_argument_spec()

        assert spec["vm"]["type"] == "str"
        assert spec["vm"]["required"] is True

    def test_vm_home_parameter(self):
        """Test that vm_home is an optional bool parameter."""
        spec = module_under_test.create_module_argument_spec()

        assert spec["vm_home"]["type"] == "bool"
        assert spec["vm_home"].get("required", False) is False

    def test_disks_parameter(self):
        """Test that disks is an optional list of strings."""
        spec = module_under_test.create_module_argument_spec()

        assert spec["disks"]["type"] == "list"
        assert spec["disks"]["elements"] == "str"
        assert spec["disks"].get("required", False) is False


# ============================================================================
# Test OperationConfig Building
# ============================================================================


class TestOperationConfig:
    """Test that the check OperationConfig builds paths and bodies correctly."""

    def test_check_is_post(self):
        """Test that the check action uses the POST method."""
        assert module_under_test.ACTION_OPERATIONS["check"].http_method == "post"

    def test_check_build_path(self):
        """Test that the check action interpolates the vm into the path."""
        config = module_under_test.ACTION_OPERATIONS["check"]

        assert (
            config.build_path(params={"vm": VM_ID})
            == "/vcenter/vm/vm-42/storage/policy/compliance?action=check"
        )

    def test_check_build_body(self):
        """Test that the check action builds a body with vm_home and disks."""
        config = module_under_test.ACTION_OPERATIONS["check"]

        body = config.build_body(params={"vm_home": True, "disks": ["disk-2000"]})

        assert body == {"vm_home": True, "disks": ["disk-2000"]}

    def test_check_has_no_query(self):
        """Test that the check action defines no query spec (action is in the URI)."""
        assert (
            module_under_test.ACTION_OPERATIONS["check"].build_query(params={}) is None
        )
