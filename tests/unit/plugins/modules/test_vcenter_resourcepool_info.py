# -*- coding: utf-8 -*-
# Copyright: (c) 2026, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#
# Unit tests for vcenter_resourcepool_info module
# Generated from vSphere API spec 9.1.0
# Run tests: make units UNIT_TARGETS='tests/unit/plugins/modules/test_vcenter_resourcepool_info.py'

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import pytest
from unittest.mock import patch, MagicMock

from ansible_collections.vmware.vmware_rest.plugins.modules import (
    vcenter_resourcepool_info as module_under_test,
)
from ...common.utils import (
    AnsibleExitJson,
    CONNECTION_PARAMS,
    exit_json,
    set_module_args,
    _response,
)


@pytest.fixture
def module_args():
    return dict(CONNECTION_PARAMS)


@patch.object(module_under_test, "AnsibleModule")
@patch.object(module_under_test.VmwareRestInfoModule, "_create_client")
def test_list_resource_pools_success(
    mock_create_client, mock_ansible_module, mock_client, module_args
):
    """Test listing resource pools - GET /vcenter/resource-pool returns 200 with list, then GET each pool returns 200"""
    mock_create_client.return_value = mock_client
    mock_module = MagicMock()
    mock_ansible_module.return_value = mock_module
    mock_module.params = set_module_args(module_args)
    mock_module.exit_json = exit_json

    # Mock responses based on spec schemas
    # List operation returns Summary objects (required: resource_pool, name)
    list_response = [
        {"resource_pool": "resgroup-1009", "name": "Production"},
        {"resource_pool": "resgroup-1010", "name": "Development"},
    ]

    # Get operation returns Info objects (required: name, resource_pools)
    get_response_1 = {
        "name": "Production",
        "resource_pools": ["resgroup-1011", "resgroup-1012"],
        "cpu_allocation": {
            "reservation": 1000,
            "expandable_reservation": True,
            "limit": -1,
            "shares": {"level": "NORMAL"},
        },
        "memory_allocation": {
            "reservation": 512,
            "expandable_reservation": True,
            "limit": -1,
            "shares": {"level": "NORMAL"},
        },
    }

    get_response_2 = {
        "name": "Development",
        "resource_pools": [],
        "cpu_allocation": {
            "reservation": 0,
            "expandable_reservation": True,
            "limit": -1,
            "shares": {"level": "LOW"},
        },
        "memory_allocation": {
            "reservation": 0,
            "expandable_reservation": True,
            "limit": -1,
            "shares": {"level": "LOW"},
        },
    }

    mock_client.get.side_effect = [
        _response(200, list_response),
        _response(200, get_response_1),
        _response(200, get_response_2),
    ]

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    result = exc.value.kwargs

    # Module wraps result in 'value' key
    assert "value" in result
    assert len(result["value"]) == 2
    assert result["value"][0]["resource_pool"] == "resgroup-1009"
    assert result["value"][0]["name"] == "Production"
    assert result["value"][1]["resource_pool"] == "resgroup-1010"
    assert result["value"][1]["name"] == "Development"


@patch.object(module_under_test, "AnsibleModule")
@patch.object(module_under_test.VmwareRestInfoModule, "_create_client")
def test_list_resource_pools_empty(
    mock_create_client, mock_ansible_module, mock_client, module_args
):
    """Test listing resource pools when none exist - GET /vcenter/resource-pool returns 200 with empty list"""
    mock_create_client.return_value = mock_client
    mock_module = MagicMock()
    mock_ansible_module.return_value = mock_module
    mock_module.params = set_module_args(module_args)
    mock_module.exit_json = exit_json

    mock_client.get.side_effect = [
        _response(200, []),
    ]

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    result = exc.value.kwargs

    assert "value" in result
    assert result["value"] == []


@patch.object(module_under_test, "AnsibleModule")
@patch.object(module_under_test.VmwareRestInfoModule, "_create_client")
def test_list_resource_pools_not_found(
    mock_create_client, mock_ansible_module, mock_client, module_args
):
    """Test listing resource pools - GET /vcenter/resource-pool returns 404"""
    mock_create_client.return_value = mock_client
    mock_module = MagicMock()
    mock_ansible_module.return_value = mock_module
    mock_module.params = set_module_args(module_args)
    mock_module.exit_json = exit_json

    mock_client.get.side_effect = [
        _response(404, None),
    ]

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    result = exc.value.kwargs

    assert "value" in result
    assert result["value"] == []


@patch.object(module_under_test, "AnsibleModule")
@patch.object(module_under_test.VmwareRestInfoModule, "_create_client")
def test_list_resource_pools_filtered_by_name(
    mock_create_client, mock_ansible_module, mock_client, module_args
):
    """Test filtering resource pools by name - GET /vcenter/resource-pool?names=Production returns filtered results"""
    mock_create_client.return_value = mock_client
    mock_module = MagicMock()
    mock_ansible_module.return_value = mock_module

    # Add filter parameters
    filter_args = dict(module_args)
    filter_args["names"] = ["Production"]
    mock_module.params = set_module_args(filter_args)
    mock_module.exit_json = exit_json

    list_response = [{"resource_pool": "resgroup-1009", "name": "Production"}]

    get_response = {
        "name": "Production",
        "resource_pools": [],
        "cpu_allocation": {
            "reservation": 0,
            "expandable_reservation": True,
            "limit": -1,
            "shares": {"level": "NORMAL"},
        },
        "memory_allocation": {
            "reservation": 0,
            "expandable_reservation": True,
            "limit": -1,
            "shares": {"level": "NORMAL"},
        },
    }

    mock_client.get.side_effect = [
        _response(200, list_response),
        _response(200, get_response),
    ]

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    result = exc.value.kwargs

    assert "value" in result
    assert len(result["value"]) == 1
    assert result["value"][0]["name"] == "Production"

    # Verify query parameters were passed correctly
    call_args = mock_client.get.call_args_list[0]
    assert call_args[1]["path"] == "/vcenter/resource-pool"
    assert "query" in call_args[1]


@patch.object(module_under_test, "AnsibleModule")
@patch.object(module_under_test.VmwareRestInfoModule, "_create_client")
def test_get_resource_pool_detail_not_found(
    mock_create_client, mock_ansible_module, mock_client, module_args
):
    """Test when detail GET returns 404 for a resource pool - should skip that pool"""
    mock_create_client.return_value = mock_client
    mock_module = MagicMock()
    mock_ansible_module.return_value = mock_module
    mock_module.params = set_module_args(module_args)
    mock_module.exit_json = exit_json

    list_response = [{"resource_pool": "resgroup-1009", "name": "Production"}]

    mock_client.get.side_effect = [
        _response(200, list_response),
        _response(404, None),  # Detail GET returns 404
    ]

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    result = exc.value.kwargs

    # Pool should not be in results since detail GET failed
    assert "value" in result
    assert result["value"] == []


@patch.object(module_under_test, "AnsibleModule")
@patch.object(module_under_test.VmwareRestInfoModule, "_create_client")
def test_list_resource_pools_with_minimal_info(
    mock_create_client, mock_ansible_module, mock_client, module_args
):
    """Test resource pool with minimal required fields only - name and resource_pools"""
    mock_create_client.return_value = mock_client
    mock_module = MagicMock()
    mock_ansible_module.return_value = mock_module
    mock_module.params = set_module_args(module_args)
    mock_module.exit_json = exit_json

    list_response = [{"resource_pool": "resgroup-1009", "name": "MinimalPool"}]

    # Minimal Info schema (only required fields)
    get_response = {
        "name": "MinimalPool",
        "resource_pools": [],
        # cpu_allocation and memory_allocation are optional
    }

    mock_client.get.side_effect = [
        _response(200, list_response),
        _response(200, get_response),
    ]

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    result = exc.value.kwargs

    assert "value" in result
    assert len(result["value"]) == 1
    assert result["value"][0]["name"] == "MinimalPool"
    assert result["value"][0]["resource_pools"] == []
