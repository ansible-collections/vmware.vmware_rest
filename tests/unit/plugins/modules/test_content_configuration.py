# -*- coding: utf-8 -*-
# Copyright: (c) 2026, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Unit tests for content_configuration module.

Tests validate the CRUD module behavior using the OperationConfig-based
architecture with mocked HTTP clients. This endpoint is a singleton: it
supports GET (read the current global Content Library configuration) and
PATCH (update the configuration). There is no create, delete, list, or MOID
parameter, so ensure_present() always resolves the existing singleton and
updates it only when the desired values differ from the current state.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import pytest
from unittest.mock import patch, MagicMock

from ansible_collections.vmware.vmware_rest.plugins.modules import (
    content_configuration as module_under_test,
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


def _run_module(patch_ansible_module, module_args, check_mode=False):
    """Helper: wire up the mocked Ansible module and return it."""
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module
    mock_module.params = set_module_args(module_args)
    mock_module.exit_json.side_effect = exit_json
    mock_module.check_mode = check_mode
    return mock_module


# ============================================================================
# Test UPDATE Operations
# ============================================================================


def test_update_configuration(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test updating the configuration when the desired values differ."""
    patch_create_client.return_value = mock_client
    module_args.update(
        {
            "state": "present",
            "automatic_sync_enabled": True,
            "automatic_sync_start_hour": 22,
            "maximum_concurrent_item_syncs": 10,
        }
    )
    mock_module = _run_module(patch_ansible_module, module_args)

    # Current configuration differs from the desired values.
    mock_client.get.return_value = _response(
        200,
        {
            "automatic_sync_enabled": False,
            "automatic_sync_start_hour": 20,
            "maximum_concurrent_item_syncs": 5,
        },
    )
    mock_client.patch.return_value = _response(200, None)

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_module.exit_json.assert_called_once()
    result = exc.value.kwargs
    assert result["changed"] is True
    assert result["diff"] == {
        "automatic_sync_enabled": {"before": False, "after": True},
        "automatic_sync_start_hour": {"before": 20, "after": 22},
        "maximum_concurrent_item_syncs": {"before": 5, "after": 10},
    }
    mock_client.patch.assert_called_once()


def test_update_configuration_idempotent(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test that no update happens when the configuration already matches."""
    patch_create_client.return_value = mock_client
    module_args.update(
        {
            "state": "present",
            "automatic_sync_enabled": True,
            "automatic_sync_start_hour": 22,
            "maximum_concurrent_item_syncs": 10,
        }
    )
    mock_module = _run_module(patch_ansible_module, module_args)

    # Current configuration already matches the desired values.
    mock_client.get.return_value = _response(
        200,
        {
            "automatic_sync_enabled": True,
            "automatic_sync_start_hour": 22,
            "maximum_concurrent_item_syncs": 10,
        },
    )

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_module.exit_json.assert_called_once()
    result = exc.value.kwargs
    assert result["changed"] is False
    assert result["diff"] == {}
    mock_client.patch.assert_not_called()


def test_update_configuration_partial(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test updating only a subset of the configuration fields."""
    patch_create_client.return_value = mock_client
    module_args.update(
        {
            "state": "present",
            "transfer_threads_pool_size": 30,
        }
    )
    mock_module = _run_module(patch_ansible_module, module_args)

    mock_client.get.return_value = _response(
        200,
        {
            "automatic_sync_enabled": True,
            "automatic_sync_start_hour": 20,
            "transfer_threads_pool_size": 20,
        },
    )
    mock_client.patch.return_value = _response(200, None)

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    result = exc.value.kwargs
    assert result["changed"] is True
    assert result["diff"] == {"transfer_threads_pool_size": {"before": 20, "after": 30}}
    # Only the supplied field is sent in the PATCH body.
    mock_client.patch.assert_called_once()
    call_args = mock_client.patch.call_args
    assert call_args[1]["data"] == {"transfer_threads_pool_size": 30}


def test_update_configuration_bandwidth_and_transfers(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test updating bandwidth and transfer related fields together."""
    patch_create_client.return_value = mock_client
    module_args.update(
        {
            "state": "present",
            "transfer_throttling_bandwidth_total": 100,
            "transfer_nfc_max_concurrent_transfers_per_host": 16,
            "priority_transfer_threads_pool_size": 8,
            "automatic_sync_refresh_interval": 120,
        }
    )
    mock_module = _run_module(patch_ansible_module, module_args)

    mock_client.get.return_value = _response(
        200,
        {
            "transfer_throttling_bandwidth_total": 0,
            "transfer_nfc_max_concurrent_transfers_per_host": 8,
            "priority_transfer_threads_pool_size": 5,
            "automatic_sync_refresh_interval": 240,
        },
    )
    mock_client.patch.return_value = _response(200, None)

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    result = exc.value.kwargs
    assert result["changed"] is True
    assert result["diff"] == {
        "transfer_throttling_bandwidth_total": {"before": 0, "after": 100},
        "transfer_nfc_max_concurrent_transfers_per_host": {"before": 8, "after": 16},
        "priority_transfer_threads_pool_size": {"before": 5, "after": 8},
        "automatic_sync_refresh_interval": {"before": 240, "after": 120},
    }
    mock_client.patch.assert_called_once()


def test_update_configuration_nested_setting(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test updating a nested *_setting dict and computing a nested diff."""
    patch_create_client.return_value = mock_client
    module_args.update(
        {
            "state": "present",
            "automatic_sync_enabled_setting": {
                "name": "automatic_sync_enabled",
                "reboot_required": True,
                "constraints": [],
            },
        }
    )
    mock_module = _run_module(patch_ansible_module, module_args)

    current_setting = {
        "name": "automatic_sync_enabled",
        "reboot_required": False,
        "constraints": [],
    }
    desired_setting = {
        "name": "automatic_sync_enabled",
        "reboot_required": True,
        "constraints": [],
    }
    mock_client.get.return_value = _response(
        200, {"automatic_sync_enabled_setting": current_setting}
    )
    mock_client.patch.return_value = _response(200, None)

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    result = exc.value.kwargs
    assert result["changed"] is True
    # The diff records the whole nested setting dict, not a per-field diff.
    assert result["diff"] == {
        "automatic_sync_enabled_setting": {
            "before": current_setting,
            "after": desired_setting,
        }
    }
    # The nested setting dict is sent in the PATCH body.
    mock_client.patch.assert_called_once()
    call_args = mock_client.patch.call_args
    assert call_args[1]["data"] == {
        "automatic_sync_enabled_setting": {
            "name": "automatic_sync_enabled",
            "reboot_required": True,
            "constraints": [],
        }
    }


def test_update_configuration_disable_sync(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test that a boolean flag set to False is treated as a real change."""
    patch_create_client.return_value = mock_client
    module_args.update(
        {
            "state": "present",
            "automatic_sync_enabled": False,
        }
    )
    mock_module = _run_module(patch_ansible_module, module_args)

    mock_client.get.return_value = _response(200, {"automatic_sync_enabled": True})
    mock_client.patch.return_value = _response(200, None)

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    result = exc.value.kwargs
    assert result["changed"] is True
    assert result["diff"] == {
        "automatic_sync_enabled": {"before": True, "after": False}
    }
    mock_client.patch.assert_called_once()


# ============================================================================
# Test Check Mode
# ============================================================================


class TestCheckMode:
    """Test check mode behavior."""

    def test_update_check_mode(
        self, patch_create_client, patch_ansible_module, mock_client, module_args
    ):
        """Test updating the configuration in check mode reports change without PATCH."""
        patch_create_client.return_value = mock_client
        module_args.update(
            {
                "state": "present",
                "automatic_sync_start_hour": 22,
            }
        )
        _run_module(patch_ansible_module, module_args, check_mode=True)

        mock_client.get.return_value = _response(200, {"automatic_sync_start_hour": 20})

        with pytest.raises(AnsibleExitJson) as exc:
            module_under_test.main()

        result = exc.value.kwargs
        assert result["changed"] is True
        assert result["diff"] == {
            "automatic_sync_start_hour": {"before": 20, "after": 22}
        }
        # In check mode, no actual PATCH should occur.
        mock_client.patch.assert_not_called()

    def test_no_change_check_mode(
        self, patch_create_client, patch_ansible_module, mock_client, module_args
    ):
        """Test check mode with no changes reports no change."""
        patch_create_client.return_value = mock_client
        module_args.update(
            {
                "state": "present",
                "automatic_sync_start_hour": 20,
            }
        )
        _run_module(patch_ansible_module, module_args, check_mode=True)

        mock_client.get.return_value = _response(200, {"automatic_sync_start_hour": 20})

        with pytest.raises(AnsibleExitJson) as exc:
            module_under_test.main()

        result = exc.value.kwargs
        assert result["changed"] is False
        mock_client.patch.assert_not_called()


# ============================================================================
# Test API Call Paths
# ============================================================================


class TestAPICallPath:
    """Test that the correct API paths are called."""

    def test_get_api_path(
        self, patch_create_client, patch_ansible_module, mock_client, module_args
    ):
        """Test that GET uses the singleton item endpoint."""
        patch_create_client.return_value = mock_client
        module_args.update({"state": "present", "automatic_sync_start_hour": 20})
        _run_module(patch_ansible_module, module_args)

        mock_client.get.return_value = _response(200, {"automatic_sync_start_hour": 20})

        with pytest.raises(AnsibleExitJson):
            module_under_test.main()

        mock_client.get.assert_called_once()
        call_args = mock_client.get.call_args
        assert call_args[0][0] == "/content/configuration"

    def test_patch_api_path(
        self, patch_create_client, patch_ansible_module, mock_client, module_args
    ):
        """Test that PATCH uses the singleton item endpoint."""
        patch_create_client.return_value = mock_client
        module_args.update({"state": "present", "automatic_sync_start_hour": 22})
        _run_module(patch_ansible_module, module_args)

        mock_client.get.return_value = _response(200, {"automatic_sync_start_hour": 20})
        mock_client.patch.return_value = _response(200, None)

        with pytest.raises(AnsibleExitJson):
            module_under_test.main()

        mock_client.patch.assert_called_once()
        call_args = mock_client.patch.call_args
        assert call_args[0][0] == "/content/configuration"


# ============================================================================
# Test Module Constants
# ============================================================================


class TestModuleConstants:
    """Test that module constants are correctly defined."""

    def test_moid_parameter_hints(self):
        """Test that MOID parameter hints are empty for this singleton."""
        assert module_under_test.MOID_PARAMETER_HINTS == []

    def test_list_endpoint(self):
        """Test that there is no list endpoint."""
        assert module_under_test.LIST_ENDPOINT == ""

    def test_item_endpoint(self):
        """Test that the item API endpoint is correct."""
        assert module_under_test.ITEM_ENDPOINT == "/content/configuration"

    def test_get_operation_config(self):
        """Test that the GET operation config targets the item endpoint."""
        assert module_under_test.GET_OPERATION.uri == "/content/configuration"
        assert module_under_test.GET_OPERATION.http_method == "get"

    def test_update_operation_config(self):
        """Test that the UPDATE operation config targets the item endpoint."""
        assert module_under_test.UPDATE_OPERATION.uri == "/content/configuration"
        assert module_under_test.UPDATE_OPERATION.http_method == "patch"


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

    @pytest.mark.parametrize(
        "param_name",
        [
            "automatic_sync_start_hour",
            "automatic_sync_stop_hour",
            "automatic_sync_refresh_interval",
            "automatic_sync_setting_refresh_interval",
            "maximum_concurrent_item_syncs",
            "transfer_throttling_bandwidth_total",
            "transfer_nfc_max_concurrent_transfers_per_host",
            "priority_transfer_threads_pool_size",
            "transfer_threads_pool_size",
        ],
    )
    def test_int_params(self, param_name):
        """Test that the integer configuration parameters are correctly defined."""
        spec = module_under_test.create_module_argument_spec()

        assert param_name in spec
        assert spec[param_name]["type"] == "int"

    def test_automatic_sync_enabled_param(self):
        """Test that automatic_sync_enabled parameter is a boolean."""
        spec = module_under_test.create_module_argument_spec()

        assert "automatic_sync_enabled" in spec
        assert spec["automatic_sync_enabled"]["type"] == "bool"

    @pytest.mark.parametrize(
        "param_name",
        [
            "automatic_sync_enabled_setting",
            "automatic_sync_start_hour_setting",
            "maximum_concurrent_item_syncs_setting",
            "transfer_threads_pool_size_setting",
        ],
    )
    def test_setting_params(self, param_name):
        """Test that the *_setting parameters are dicts with the expected options."""
        spec = module_under_test.create_module_argument_spec()

        assert param_name in spec
        assert spec[param_name]["type"] == "dict"
        options = spec[param_name]["options"]
        assert options["name"]["type"] == "str"
        assert options["reboot_required"]["type"] == "bool"
        assert options["constraints"]["type"] == "list"
        assert options["constraints"]["elements"] == "dict"

    def test_create_module_argument_spec_has_connection_params(self):
        """Test that connection parameters are included."""
        spec = module_under_test.create_module_argument_spec()

        assert "vcenter_hostname" in spec
        assert "vcenter_username" in spec
        assert "vcenter_password" in spec
