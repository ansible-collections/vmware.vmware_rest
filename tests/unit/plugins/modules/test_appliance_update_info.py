# -*- coding: utf-8 -*-
# Copyright: (c) 2026, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Unit tests for appliance_update_info module.

Tests validate the Info module behavior using the OperationConfig-based
architecture with mocked HTTP clients. This endpoint is a singleton that
returns the appliance's current update status as a structured object.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import pytest
from unittest.mock import patch, MagicMock

from ansible_collections.vmware.vmware_rest.plugins.modules import (
    appliance_update_info as module_under_test,
)

from ...common.utils import (
    AnsibleExitJson,
    exit_json,
    set_module_args,
    _response,
)

UPDATE_STATUS = {
    "state": "UP_TO_DATE",
    "version": "9.1.0.10000",
    "latest_query_time": "2024-07-31T18:18:32.000Z",
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
        module_under_test.VmwareRestInfoModuleBase, "_create_client"
    ) as mock:
        yield mock


def _run_module(patch_ansible_module, mock_client, module_args, status, body):
    """Helper: wire up the mocked module/client and run main()."""
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module
    mock_module.params = set_module_args(module_args)
    mock_module.exit_json.side_effect = exit_json
    mock_module.check_mode = False
    mock_client.get.return_value = _response(status, body)
    return mock_module


# ============================================================================
# Test GET Operations (Singleton returning an update status struct)
# ============================================================================


def test_get_update_status(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test getting the appliance update status."""
    patch_create_client.return_value = mock_client
    mock_module = _run_module(
        patch_ansible_module, mock_client, module_args, 200, UPDATE_STATUS
    )

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_module.exit_json.assert_called_once()
    result = exc.value.kwargs
    assert result["value"] == UPDATE_STATUS
    assert result["info"] == [UPDATE_STATUS]
    assert result["value"]["state"] == "UP_TO_DATE"
    assert result["value"]["version"] == "9.1.0.10000"
    # An update status struct has no MOID attribute, so no id should be reported.
    assert "id" not in result


def test_get_update_status_not_found(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test getting the update status when the endpoint returns 404."""
    patch_create_client.return_value = mock_client
    mock_module = _run_module(patch_ansible_module, mock_client, module_args, 404, None)

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
        """Test getting the update status in check mode."""
        patch_create_client.return_value = mock_client
        mock_module = MagicMock()
        patch_ansible_module.return_value = mock_module
        mock_module.params = set_module_args(module_args)
        mock_module.exit_json.side_effect = exit_json
        mock_module.check_mode = True

        mock_client.get.return_value = _response(200, UPDATE_STATUS)

        with pytest.raises(AnsibleExitJson) as exc:
            module_under_test.main()

        result = exc.value.kwargs
        assert result["value"] == UPDATE_STATUS
        mock_client.get.assert_called_once()


# ============================================================================
# Test API Call Path
# ============================================================================


class TestAPICallPath:
    """Test that the correct API path is called."""

    def test_get_api_path(
        self, patch_create_client, patch_ansible_module, mock_client, module_args
    ):
        """Test that GET uses the correct API path."""
        patch_create_client.return_value = mock_client
        _run_module(patch_ansible_module, mock_client, module_args, 200, UPDATE_STATUS)

        with pytest.raises(AnsibleExitJson):
            module_under_test.main()

        mock_client.get.assert_called_once()
        call_args = mock_client.get.call_args
        assert call_args[0][0] == "/appliance/update"


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
        assert module_under_test.ITEM_ENDPOINT == "/appliance/update"

    def test_get_operation_config(self):
        """Test that the GET operation config targets the item endpoint."""
        assert module_under_test.GET_OPERATION.uri == "/appliance/update"
        assert module_under_test.GET_OPERATION.http_method == "get"


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

    def test_create_module_argument_spec_no_state(self):
        """Test that info module has no state parameter."""
        spec = module_under_test.create_module_argument_spec()

        assert "state" not in spec
