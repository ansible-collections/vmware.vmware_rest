# -*- coding: utf-8 -*-
# Copyright: (c) 2026, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Unit tests for appliance_monitoring_info module.

Tests validate the Info module behavior using the OperationConfig-based
architecture with mocked HTTP clients.

This module supports two access patterns:
- GET a single monitored item by ``stat_id`` (``/appliance/monitoring/{stat_id}``).
- LIST all monitored items (``/appliance/monitoring``) when no ``stat_id`` is given.

Unlike endpoints that return bare identifier strings, ``GET /appliance/monitoring``
returns an array of full ``MonitoredItem`` dicts whose identifier field is named
``id`` (not ``stat_id``). Because those dicts don't supply the get operation's
``{stat_id}`` path parameter, ``_list_resource_details()`` treats them as already
complete and returns them as-is, without a redundant per-item detail lookup.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import pytest
from unittest.mock import patch, MagicMock

from ansible_collections.vmware.vmware_rest.plugins.modules import (
    appliance_monitoring_info as module_under_test,
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
        module_under_test.VmwareRestInfoModuleBase, "_create_client"
    ) as mock:
        yield mock


def _run_module(patch_ansible_module, mock_client, module_args, check_mode=False):
    """Helper: wire up the mocked module/client and return the mock module."""
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module
    mock_module.params = set_module_args(module_args)
    mock_module.exit_json.side_effect = exit_json
    mock_module.fail_json.side_effect = fail_json
    mock_module.check_mode = check_mode
    return mock_module


SAMPLE_ITEM = {
    "id": "cpu.util",
    "name": "CPU utilization",
    "units": "%",
    "category": "cpu",
    "instance": "",
    "description": "com.vmware.applmgmt.mon.descr.cpu.util",
}


# ============================================================================
# Test GET Operations (single monitored item by stat_id)
# ============================================================================


def test_get_item_by_stat_id(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test getting a specific monitored item by stat_id."""
    patch_create_client.return_value = mock_client
    module_args.update({"stat_id": "cpu.util"})
    mock_module = _run_module(patch_ansible_module, mock_client, module_args)
    mock_client.get.return_value = _response(200, SAMPLE_ITEM)

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_module.exit_json.assert_called_once()
    result = exc.value.kwargs
    # value preserves the single-resource dict shape.
    assert result["value"] == SAMPLE_ITEM
    # info is always a list; the single item yields exactly one element.
    assert result["info"] == [SAMPLE_ITEM]
    # The base class derives the top-level id from the payload's "id" field.
    assert result["id"] == "cpu.util"


def test_get_item_not_found(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test getting a monitored item when the endpoint returns 404."""
    patch_create_client.return_value = mock_client
    module_args.update({"stat_id": "does.not.exist"})
    mock_module = _run_module(patch_ansible_module, mock_client, module_args)
    mock_client.get.return_value = _response(404, None)

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_module.exit_json.assert_called_once()
    result = exc.value.kwargs
    assert result["info"] == []
    assert result["value"] == {}
    assert "id" not in result


# ============================================================================
# Test LIST Operations
# ============================================================================


def test_list_all_monitored_items(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test listing all monitored items when no stat_id is given.

    ``GET /appliance/monitoring`` already returns full item dicts, so they are
    returned directly without a per-item detail lookup. This is the module's
    primary documented use case.
    """
    patch_create_client.return_value = mock_client
    # No stat_id -> falls back to the LIST endpoint.
    mock_module = _run_module(patch_ansible_module, mock_client, module_args)

    mem_item = {
        "id": "mem.util",
        "name": "Memory utilization",
        "units": "KB",
        "category": "memory",
        "instance": "",
        "description": "com.vmware.applmgmt.mon.descr.mem.util",
    }
    mock_client.get.return_value = _response(200, [SAMPLE_ITEM, mem_item])

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    result = exc.value.kwargs
    # Listing yields a list for both info and value.
    assert result["info"] == [SAMPLE_ITEM, mem_item]
    assert result["value"] == result["info"]
    assert "id" not in result

    # The full items come straight from the list endpoint; no per-item detail
    # lookups are made.
    mock_client.get.assert_called_once()
    assert mock_client.get.call_args[0][0] == "/appliance/monitoring"


def test_list_monitored_items_empty(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test listing when no monitored items exist."""
    patch_create_client.return_value = mock_client
    mock_module = _run_module(patch_ansible_module, mock_client, module_args)
    mock_client.get.return_value = _response(200, [])

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_module.exit_json.assert_called_once()
    result = exc.value.kwargs
    assert result["info"] == []
    assert result["value"] == []
    assert "id" not in result


# ============================================================================
# Test Check Mode
# ============================================================================


class TestCheckMode:
    """Test check mode behavior (info modules always execute normally)."""

    def test_get_check_mode(
        self, patch_create_client, patch_ansible_module, mock_client, module_args
    ):
        """Test getting an item in check mode still performs the read."""
        patch_create_client.return_value = mock_client
        module_args.update({"stat_id": "cpu.util"})
        mock_module = _run_module(
            patch_ansible_module, mock_client, module_args, check_mode=True
        )
        mock_client.get.return_value = _response(200, SAMPLE_ITEM)

        with pytest.raises(AnsibleExitJson) as exc:
            module_under_test.main()

        result = exc.value.kwargs
        assert result["value"] == SAMPLE_ITEM
        mock_client.get.assert_called_once()


# ============================================================================
# Test API Call Path
# ============================================================================


class TestAPICallPath:
    """Test that the correct API path is called."""

    def test_get_api_path(
        self, patch_create_client, patch_ansible_module, mock_client, module_args
    ):
        """Test that GET uses the correct item API path."""
        patch_create_client.return_value = mock_client
        module_args.update({"stat_id": "cpu.util"})
        _run_module(patch_ansible_module, mock_client, module_args)
        mock_client.get.return_value = _response(200, SAMPLE_ITEM)

        with pytest.raises(AnsibleExitJson):
            module_under_test.main()

        mock_client.get.assert_called_once()
        call_args = mock_client.get.call_args
        assert call_args[0][0] == "/appliance/monitoring/cpu.util"


# ============================================================================
# Test Module Constants
# ============================================================================


class TestModuleConstants:
    """Test that module constants are correctly defined."""

    def test_moid_parameter_hints(self):
        """Test that the MOID parameter hint is the stat_id."""
        assert module_under_test.MOID_PARAMETER_HINTS == ["stat_id"]

    def test_list_endpoint(self):
        """Test that the list API endpoint is correct."""
        assert module_under_test.LIST_ENDPOINT == "/appliance/monitoring"

    def test_item_endpoint(self):
        """Test that the item API endpoint is correct."""
        assert module_under_test.ITEM_ENDPOINT == "/appliance/monitoring/{stat_id}"

    def test_get_operation_config(self):
        """Test that the GET operation config targets the item endpoint."""
        assert module_under_test.GET_OPERATION.uri == "/appliance/monitoring/{stat_id}"
        assert module_under_test.GET_OPERATION.http_method == "get"

    def test_list_operation_config(self):
        """Test that the LIST operation config targets the list endpoint."""
        assert module_under_test.LIST_OPERATION.uri == "/appliance/monitoring"
        assert module_under_test.LIST_OPERATION.http_method == "get"


# ============================================================================
# Test OperationConfig path building
# ============================================================================


class TestOperationConfig:
    """Test OperationConfig path building for this module."""

    def test_get_build_path_with_stat_id(self):
        """GET path is populated from the stat_id parameter."""
        path = module_under_test.GET_OPERATION.build_path({"stat_id": "cpu.util"})
        assert path == "/appliance/monitoring/cpu.util"

    def test_get_build_path_missing_stat_id_raises(self):
        """GET path building requires the stat_id path parameter."""
        from ansible_collections.vmware.vmware_rest.plugins.module_utils._errors import (
            RequiredPathParameterError,
        )

        with pytest.raises(RequiredPathParameterError):
            module_under_test.GET_OPERATION.build_path({})

    def test_list_build_path_is_static(self):
        """LIST path has no template parameters."""
        assert (
            module_under_test.LIST_OPERATION.build_path({}) == "/appliance/monitoring"
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

    def test_create_module_argument_spec_stat_id(self):
        """Test that the stat_id parameter is defined and optional."""
        spec = module_under_test.create_module_argument_spec()

        assert "stat_id" in spec
        assert spec["stat_id"]["type"] == "str"
        assert not spec["stat_id"].get("required", False)

    def test_create_module_argument_spec_no_state(self):
        """Test that info module has no state parameter."""
        spec = module_under_test.create_module_argument_spec()

        assert "state" not in spec
