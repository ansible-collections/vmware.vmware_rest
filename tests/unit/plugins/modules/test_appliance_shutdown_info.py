# -*- coding: utf-8 -*-
# Copyright: (c) 2026, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Unit tests for appliance_shutdown_info module.

Tests validate the get-only Info module behavior using the OperationConfig-based
architecture with mocked HTTP clients. The appliance_shutdown_info module is a
singleton GET endpoint with no list operation and no MOID parameters.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import pytest
from unittest.mock import MagicMock, patch

from ansible_collections.vmware.vmware_rest.plugins.module_utils._operation_configs import (
    OperationConfig,
)
from ansible_collections.vmware.vmware_rest.plugins.module_utils._info_module import (
    VmwareRestInfoModuleBase,
)

from ...common.utils import CONNECTION_PARAMS, fail_json


@pytest.fixture
def mock_module():
    """
    Mock Ansible module object.
    """
    module = MagicMock()
    module.params = CONNECTION_PARAMS.copy()
    module.check_mode = False
    module.fail_json = fail_json
    return module


@pytest.fixture
def info_module(mock_module, mock_client):
    """
    Create info module instance with appliance shutdown operation configs.

    Note: mock_client is provided by conftest.py - do not redefine it.
    """
    get_operation = OperationConfig(
        name="get",
        uri="/appliance/shutdown",
        http_method="GET",
    )

    with patch(
        "ansible_collections.vmware.vmware_rest.plugins.module_utils._module_base.Client",
        return_value=mock_client,
    ):
        module = VmwareRestInfoModuleBase(
            module=mock_module,
            moid_parameter_hints=[],
            get_operation_config=get_operation,
        )
        yield module


# ============================================================================
# get_resource_info() Tests - GET Singleton
# ============================================================================


def test_get_resource_info_pending_reboot(info_module, mock_client):
    """
    Test getting shutdown info when a reboot is pending.
    """
    get_response = MagicMock()
    get_response.status = 200
    get_response.json = {
        "action": "reboot",
        "shutdown_time": "2026-08-03T12:00:00Z",
        "reason": "Scheduled maintenance window",
    }
    mock_client.get.return_value = get_response

    result = info_module.get_resource_info()

    assert "value" in result
    assert result["value"]["action"] == "reboot"
    assert result["value"]["shutdown_time"] == "2026-08-03T12:00:00Z"
    assert result["value"]["reason"] == "Scheduled maintenance window"
    assert "info" in result
    assert len(result["info"]) == 1


def test_get_resource_info_pending_poweroff(info_module, mock_client):
    """
    Test getting shutdown info when a poweroff is pending.
    """
    get_response = MagicMock()
    get_response.status = 200
    get_response.json = {
        "action": "poweroff",
        "shutdown_time": "2026-08-03T14:00:00Z",
        "reason": "Emergency shutdown for hardware maintenance",
    }
    mock_client.get.return_value = get_response

    result = info_module.get_resource_info()

    assert "value" in result
    assert result["value"]["action"] == "poweroff"
    assert result["value"]["reason"] == "Emergency shutdown for hardware maintenance"
    assert "info" in result
    assert len(result["info"]) == 1


def test_get_resource_info_no_pending_action(info_module, mock_client):
    """
    Test getting shutdown info when no shutdown is pending.
    """
    get_response = MagicMock()
    get_response.status = 200
    get_response.json = {
        "action": "",
        "shutdown_time": "",
        "reason": "",
    }
    mock_client.get.return_value = get_response

    result = info_module.get_resource_info()

    assert "value" in result
    assert result["value"]["action"] == ""
    assert "info" in result
    assert len(result["info"]) == 1


def test_get_resource_info_not_found(info_module, mock_client):
    """
    Test getting shutdown info when endpoint returns 404.
    """
    get_response = MagicMock()
    get_response.status = 404
    mock_client.get.return_value = get_response

    result = info_module.get_resource_info()

    assert "info" in result
    assert len(result["info"]) == 0
    assert result["value"] == {}


# ============================================================================
# normalize_info_results() Tests
# ============================================================================


def test_normalize_info_results_single_resource(info_module):
    """
    Test normalize_info_results with a single shutdown status resource.
    """
    resource = {
        "action": "reboot",
        "shutdown_time": "2026-08-03T12:00:00Z",
        "reason": "Maintenance",
    }

    result = info_module.normalize_info_results(
        query_results=[resource], single_resource=True
    )

    assert "value" in result
    assert result["value"]["action"] == "reboot"
    assert "info" in result
    assert len(result["info"]) == 1


def test_normalize_info_results_empty(info_module):
    """
    Test normalize_info_results with empty result list.
    """
    result = info_module.normalize_info_results(query_results=[], single_resource=True)

    assert "info" in result
    assert len(result["info"]) == 0
    assert result["value"] == {}


# ============================================================================
# Check Mode Tests
# ============================================================================


def test_get_resource_info_check_mode(info_module, mock_client):
    """
    Test getting shutdown info in check mode (should execute normally).

    Info modules are read-only, so check mode doesn't prevent execution.
    """
    info_module.module.check_mode = True

    get_response = MagicMock()
    get_response.status = 200
    get_response.json = {
        "action": "reboot",
        "shutdown_time": "2026-08-03T12:00:00Z",
        "reason": "Maintenance",
    }
    mock_client.get.return_value = get_response

    result = info_module.get_resource_info()

    assert result["value"]["action"] == "reboot"
    mock_client.get.assert_called_once()


# ============================================================================
# OperationConfig Tests
# ============================================================================


def test_operation_config_build_path_singleton():
    """
    Test that GET OperationConfig builds the correct static path.
    """
    config = OperationConfig(
        name="get",
        uri="/appliance/shutdown",
        http_method="GET",
    )

    path = config.build_path(params={})

    assert path == "/appliance/shutdown"


# ============================================================================
# _perform_get_operation() Tests
# ============================================================================


def test_perform_get_operation(info_module, mock_client):
    """
    Test the base _perform_get_operation method for shutdown endpoint.
    """
    get_response = MagicMock()
    get_response.status = 200
    get_response.json = {
        "action": "reboot",
        "shutdown_time": "2026-08-03T12:00:00Z",
        "reason": "Maintenance",
    }
    mock_client.get.return_value = get_response

    result = info_module._perform_get_operation()

    assert result is not None
    assert result["action"] == "reboot"
    assert result["reason"] == "Maintenance"


def test_perform_get_operation_not_found(info_module, mock_client):
    """
    Test _perform_get_operation when endpoint returns 404.
    """
    get_response = MagicMock()
    get_response.status = 404
    mock_client.get.return_value = get_response

    result = info_module._perform_get_operation()

    assert result is None
