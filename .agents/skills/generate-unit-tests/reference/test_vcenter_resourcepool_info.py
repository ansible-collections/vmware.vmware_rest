# -*- coding: utf-8 -*-
# Copyright: (c) 2026, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Reference unit tests for vcenter_resourcepool_info module.

This file demonstrates the testing pattern for info modules using the
new OperationConfig-based architecture. Use this as a template when
generating tests for other info modules.
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
def mock_client():
    """
    Mock HTTP client.
    """
    return MagicMock()


@pytest.fixture
def info_module(mock_module, mock_client):
    """
    Create info module instance with resource pool operation configs.

    This fixture demonstrates how to instantiate VmwareRestInfoModuleBase
    with the OperationConfig objects that match the actual module.
    """
    # Define operation configs matching vcenter_resourcepool_info module
    get_operation = OperationConfig(
        name="get",
        uri="/vcenter/resource-pool/{resource_pool}",
        http_method="GET",
    )

    list_operation = OperationConfig(
        name="list",
        uri="/vcenter/resource-pool",
        http_method="GET",
        query_spec={
            "resource_pools": {"required": False},
            "names": {"required": False},
            "parent_resource_pools": {"required": False},
            "datacenters": {"required": False},
            "hosts": {"required": False},
            "clusters": {"required": False},
        },
    )

    # Patch Client to return our mock
    with patch(
        "ansible_collections.vmware.vmware_rest.plugins.module_utils._module_base.Client",
        return_value=mock_client,
    ):
        module = VmwareRestInfoModuleBase(
            module=mock_module,
            get_operation_config=get_operation,
            list_operation_config=list_operation,
            moid_parameter_hints=["resource_pool"],
        )
        yield module


# ============================================================================
# get_resource_info() Tests - GET by ID
# ============================================================================


def test_get_resource_info_by_id(info_module, mock_client):
    """
    Test getting a specific resource by ID.
    """
    info_module.params["resource_pool"] = "pool-1"

    get_response = MagicMock()
    get_response.status = 200
    get_response.json = {
        "resource_pool": "pool-1",
        "name": "my_pool",
        "cpu_allocation": {
            "reservation": 1000,
            "limit": 2000,
        },
        "memory_allocation": {
            "reservation": 512,
            "limit": 1024,
        },
    }
    mock_client.get.return_value = get_response

    result = info_module.get_resource_info()

    assert result["id"] == "pool-1"
    assert "value" in result
    assert result["value"]["name"] == "my_pool"
    assert result["value"]["cpu_allocation"]["reservation"] == 1000


def test_get_resource_info_by_id_with_nested_data(info_module, mock_client):
    """
    Test getting a resource with deeply nested data.
    """
    info_module.params["resource_pool"] = "pool-1"

    get_response = MagicMock()
    get_response.status = 200
    get_response.json = {
        "resource_pool": "pool-1",
        "name": "my_pool",
        "cpu_allocation": {
            "reservation": 1000,
            "limit": 2000,
            "shares": {
                "level": "HIGH",
                "shares": 2000,
            },
        },
    }
    mock_client.get.return_value = get_response

    result = info_module.get_resource_info()

    assert result["id"] == "pool-1"
    assert result["value"]["cpu_allocation"]["shares"]["level"] == "HIGH"


def test_get_resource_info_not_found(info_module, mock_client):
    """
    Test getting a resource that doesn't exist (404).
    """
    info_module.params["resource_pool"] = "pool-999"

    get_response = MagicMock()
    get_response.status = 404
    mock_client.get.return_value = get_response

    result = info_module.get_resource_info()

    # Info modules return empty list when resource not found
    assert "info" in result
    assert len(result["info"]) == 0


# ============================================================================
# get_resource_info() Tests - LIST All
# ============================================================================


def test_get_resource_info_list_all(info_module, mock_client):
    """
    Test listing all resources.
    """
    # No resource_pool param = list all

    list_response = MagicMock()
    list_response.status = 200
    list_response.json = [
        {"resource_pool": "pool-1", "name": "pool1"},
        {"resource_pool": "pool-2", "name": "pool2"},
        {"resource_pool": "pool-3", "name": "pool3"},
    ]
    mock_client.get.return_value = list_response

    result = info_module.get_resource_info()

    assert "info" in result
    assert len(result["info"]) == 3
    assert result["info"][0]["resource_pool"] == "pool-1"
    assert result["info"][1]["resource_pool"] == "pool-2"
    assert result["info"][2]["resource_pool"] == "pool-3"


def test_get_resource_info_list_empty(info_module, mock_client):
    """
    Test listing when no resources exist.
    """
    list_response = MagicMock()
    list_response.status = 200
    list_response.json = []
    mock_client.get.return_value = list_response

    result = info_module.get_resource_info()

    assert "info" in result
    assert len(result["info"]) == 0


def test_get_resource_info_list_single_resource(info_module, mock_client):
    """
    Test listing when only one resource exists.
    """
    list_response = MagicMock()
    list_response.status = 200
    list_response.json = [
        {"resource_pool": "pool-1", "name": "single_pool"},
    ]
    mock_client.get.return_value = list_response

    result = info_module.get_resource_info()

    assert "info" in result
    assert len(result["info"]) == 1
    assert result["info"][0]["name"] == "single_pool"


# ============================================================================
# get_resource_info() Tests - LIST with Filters
# ============================================================================


def test_get_resource_info_list_with_names_filter(info_module, mock_client):
    """
    Test listing with names filter.
    """
    info_module.params["names"] = ["pool1", "pool2"]

    list_response = MagicMock()
    list_response.status = 200
    list_response.json = [
        {"resource_pool": "pool-1", "name": "pool1"},
        {"resource_pool": "pool-2", "name": "pool2"},
    ]
    mock_client.get.return_value = list_response

    result = info_module.get_resource_info()

    assert "info" in result
    assert len(result["info"]) == 2

    # Verify query params were built correctly
    # The actual call would include query params
    mock_client.get.assert_called_once()


def test_get_resource_info_list_with_parent_filter(info_module, mock_client):
    """
    Test listing with parent resource pools filter.
    """
    info_module.params["parent_resource_pools"] = ["parent-pool-1"]

    list_response = MagicMock()
    list_response.status = 200
    list_response.json = [
        {"resource_pool": "pool-1", "name": "child1", "parent": "parent-pool-1"},
        {"resource_pool": "pool-2", "name": "child2", "parent": "parent-pool-1"},
    ]
    mock_client.get.return_value = list_response

    result = info_module.get_resource_info()

    assert "info" in result
    assert len(result["info"]) == 2


def test_get_resource_info_list_with_clusters_filter(info_module, mock_client):
    """
    Test listing with clusters filter.
    """
    info_module.params["clusters"] = ["cluster-1"]

    list_response = MagicMock()
    list_response.status = 200
    list_response.json = [
        {"resource_pool": "pool-1", "name": "cluster_pool", "cluster": "cluster-1"},
    ]
    mock_client.get.return_value = list_response

    result = info_module.get_resource_info()

    assert "info" in result
    assert len(result["info"]) == 1


def test_get_resource_info_list_with_multiple_filters(info_module, mock_client):
    """
    Test listing with multiple filters combined.
    """
    info_module.params["names"] = ["pool1"]
    info_module.params["clusters"] = ["cluster-1"]

    list_response = MagicMock()
    list_response.status = 200
    list_response.json = [
        {"resource_pool": "pool-1", "name": "pool1", "cluster": "cluster-1"},
    ]
    mock_client.get.return_value = list_response

    result = info_module.get_resource_info()

    assert "info" in result
    assert len(result["info"]) == 1
    assert result["info"][0]["name"] == "pool1"


# ============================================================================
# normalize_info_results() Tests
# ============================================================================


def test_normalize_info_results_single_resource(info_module):
    """
    Test normalize_info_results with a single resource.
    """
    resource = {
        "resource_pool": "pool-1",
        "name": "my_pool",
        "cpu_allocation": {"reservation": 1000},
    }

    result = info_module.normalize_info_results([resource])

    assert result["id"] == "pool-1"
    assert "value" in result
    assert result["value"]["name"] == "my_pool"
    assert "info" in result
    assert len(result["info"]) == 1


def test_normalize_info_results_multiple_resources(info_module):
    """
    Test normalize_info_results with multiple resources.
    """
    resources = [
        {"resource_pool": "pool-1", "name": "pool1"},
        {"resource_pool": "pool-2", "name": "pool2"},
        {"resource_pool": "pool-3", "name": "pool3"},
    ]

    result = info_module.normalize_info_results(resources)

    assert "info" in result
    assert len(result["info"]) == 3
    # With multiple resources, no single 'id' or 'value'
    assert "id" not in result or result.get("value") is None


def test_normalize_info_results_empty_list(info_module):
    """
    Test normalize_info_results with empty list.
    """
    result = info_module.normalize_info_results([])

    assert "info" in result
    assert len(result["info"]) == 0


# ============================================================================
# Check Mode Tests
# ============================================================================


def test_get_resource_info_check_mode_get(info_module, mock_client):
    """
    Test getting a resource in check mode (should execute normally).

    Info modules are read-only, so check mode doesn't prevent execution.
    """
    info_module.params["resource_pool"] = "pool-1"
    info_module.module.check_mode = True

    get_response = MagicMock()
    get_response.status = 200
    get_response.json = {
        "resource_pool": "pool-1",
        "name": "my_pool",
    }
    mock_client.get.return_value = get_response

    result = info_module.get_resource_info()

    # Even in check mode, GET should be called (read-only operation)
    assert result["id"] == "pool-1"
    mock_client.get.assert_called_once()


def test_get_resource_info_check_mode_list(info_module, mock_client):
    """
    Test listing resources in check mode (should execute normally).

    Info modules are read-only, so check mode doesn't prevent execution.
    """
    info_module.module.check_mode = True

    list_response = MagicMock()
    list_response.status = 200
    list_response.json = [
        {"resource_pool": "pool-1", "name": "pool1"},
        {"resource_pool": "pool-2", "name": "pool2"},
    ]
    mock_client.get.return_value = list_response

    result = info_module.get_resource_info()

    # Even in check mode, LIST should be called (read-only operation)
    assert len(result["info"]) == 2
    mock_client.get.assert_called_once()


# ============================================================================
# OperationConfig Tests
# ============================================================================


def test_operation_config_build_path_for_get():
    """
    Test that GET OperationConfig builds paths with parameters.
    """
    config = OperationConfig(
        name="get",
        uri="/vcenter/resource-pool/{resource_pool}",
        http_method="GET",
    )

    params = {"resource_pool": "pool-1"}
    path = config.build_path(params)

    assert path == "/vcenter/resource-pool/pool-1"


def test_operation_config_build_query_for_list():
    """
    Test that LIST OperationConfig builds query parameters.
    """
    config = OperationConfig(
        name="list",
        uri="/vcenter/resource-pool",
        http_method="GET",
        query_spec={
            "names": {"required": False},
            "parent_resource_pools": {"required": False},
            "clusters": {"required": False},
        },
    )

    params = {"names": ["pool1", "pool2"]}
    query = config.build_query(params)

    assert query == {"names": ["pool1", "pool2"]}


def test_operation_config_build_query_multiple_params():
    """
    Test building query with multiple filter parameters.
    """
    config = OperationConfig(
        name="list",
        uri="/vcenter/resource-pool",
        http_method="GET",
        query_spec={
            "names": {"required": False},
            "clusters": {"required": False},
            "datacenters": {"required": False},
        },
    )

    params = {
        "names": ["pool1"],
        "clusters": ["cluster-1"],
    }
    query = config.build_query(params)

    assert query == {
        "names": ["pool1"],
        "clusters": ["cluster-1"],
    }


def test_operation_config_build_query_optional_params():
    """
    Test that optional query params are omitted if not provided.
    """
    config = OperationConfig(
        name="list",
        uri="/vcenter/resource-pool",
        http_method="GET",
        query_spec={
            "names": {"required": False},
            "clusters": {"required": False},
        },
    )

    params = {}
    # No filters provided
    query = config.build_query(params)

    assert query == {}


# ============================================================================
# _perform_list_operation() Tests
# ============================================================================


def test_perform_list_operation(info_module, mock_client):
    """
    Test the base _perform_list_operation method.
    """
    list_response = MagicMock()
    list_response.status = 200
    list_response.json = [
        {"resource_pool": "pool-1", "name": "pool1"},
        {"resource_pool": "pool-2", "name": "pool2"},
    ]
    mock_client.get.return_value = list_response

    result = info_module._perform_list_operation()

    assert len(result) == 2
    assert result[0]["resource_pool"] == "pool-1"


def test_perform_list_operation_with_filters(info_module, mock_client):
    """
    Test _perform_list_operation with query filters.
    """
    info_module.params["names"] = ["pool1"]

    list_response = MagicMock()
    list_response.status = 200
    list_response.json = [
        {"resource_pool": "pool-1", "name": "pool1"},
    ]
    mock_client.get.return_value = list_response

    result = info_module._perform_list_operation()

    assert len(result) == 1
    assert result[0]["name"] == "pool1"


# ============================================================================
# _perform_get_operation() Tests
# ============================================================================


def test_perform_get_operation(info_module, mock_client):
    """
    Test the base _perform_get_operation method.
    """
    info_module.params["resource_pool"] = "pool-1"

    get_response = MagicMock()
    get_response.status = 200
    get_response.json = {
        "resource_pool": "pool-1",
        "name": "my_pool",
    }
    mock_client.get.return_value = get_response

    result = info_module._perform_get_operation()

    assert result is not None
    assert result["resource_pool"] == "pool-1"
    assert result["name"] == "my_pool"


def test_perform_get_operation_not_found(info_module, mock_client):
    """
    Test _perform_get_operation when resource doesn't exist.
    """
    info_module.params["resource_pool"] = "pool-999"

    get_response = MagicMock()
    get_response.status = 404
    mock_client.get.return_value = get_response

    result = info_module._perform_get_operation()

    assert result is None
