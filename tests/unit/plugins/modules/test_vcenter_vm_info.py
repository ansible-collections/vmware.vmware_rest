# -*- coding: utf-8 -*-
# Copyright: (c) 2026, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Unit tests for vcenter_vm_info module.

Tests validate the info module behavior using the OperationConfig-based
architecture with mocked HTTP clients. Assertions describe the desired
state the module should report for a given mocked API response.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import pytest
from unittest.mock import patch, MagicMock

from ansible_collections.vmware.vmware_rest.plugins.modules import (
    vcenter_vm_info as module_under_test,
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


def test_get_vm_by_id(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test getting a specific virtual machine by ID."""
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

    # Mock GET response returns full vm info
    get_response = {
        "vm": "vm-1001",
        "name": "test-vm-1",
        "power_state": "POWERED_ON",
        "cpu": {"count": 2},
        "memory": {"size_MiB": 4096},
    }

    mock_client.get.return_value = _response(200, get_response)

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_module.exit_json.assert_called_once()
    result = exc.value.kwargs
    assert result["id"] == "vm-1001"
    assert "value" in result
    assert result["value"]["vm"] == "vm-1001"
    assert result["value"]["name"] == "test-vm-1"
    assert result["value"]["power_state"] == "POWERED_ON"
    assert result["value"]["cpu"]["count"] == 2
    # A single GET by ID should not hit the list endpoint
    mock_client.get.assert_called_once()


def test_get_vm_not_found(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test getting a virtual machine that doesn't exist."""
    patch_create_client.return_value = mock_client
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module

    module_args.update(
        {
            "vm": "vm-9999",
        }
    )
    mock_module.params = set_module_args(module_args)
    mock_module.exit_json.side_effect = exit_json
    mock_module.check_mode = False

    # Mock GET response returns 404
    mock_client.get.return_value = _response(404, None)

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_module.exit_json.assert_called_once()
    result = exc.value.kwargs
    # Info modules return an empty info list when the resource is not found
    assert "info" in result
    assert len(result["info"]) == 0
    assert result["value"] == {}


# ============================================================================
# Test LIST Operations (Multiple Resources)
# ============================================================================


def test_list_all_vms(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test listing all virtual machines."""
    patch_create_client.return_value = mock_client
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module

    module_args.update({})  # No filters
    mock_module.params = set_module_args(module_args)
    mock_module.exit_json.side_effect = exit_json
    mock_module.check_mode = False

    # The list endpoint returns summaries; each item is then enriched via GET.
    list_response = [
        {"vm": "vm-1001", "name": "test-vm-1", "power_state": "POWERED_ON"},
        {"vm": "vm-1002", "name": "test-vm-2", "power_state": "POWERED_OFF"},
    ]
    detail_response_1 = {
        "vm": "vm-1001",
        "name": "test-vm-1",
        "power_state": "POWERED_ON",
        "cpu": {"count": 2},
    }
    detail_response_2 = {
        "vm": "vm-1002",
        "name": "test-vm-2",
        "power_state": "POWERED_OFF",
        "cpu": {"count": 4},
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
    assert result["info"][0]["vm"] == "vm-1001"
    assert result["info"][0]["cpu"]["count"] == 2
    assert result["info"][1]["vm"] == "vm-1002"
    assert result["info"][1]["cpu"]["count"] == 4


def test_list_vms_empty(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test listing virtual machines when none exist."""
    patch_create_client.return_value = mock_client
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module

    module_args.update({})
    mock_module.params = set_module_args(module_args)
    mock_module.exit_json.side_effect = exit_json
    mock_module.check_mode = False

    # Mock LIST response returns empty list
    mock_client.get.return_value = _response(200, [])

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_module.exit_json.assert_called_once()
    result = exc.value.kwargs
    assert "info" in result
    assert len(result["info"]) == 0


def test_list_vms_by_names(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test listing virtual machines filtered by names."""
    patch_create_client.return_value = mock_client
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module

    module_args.update(
        {
            "names": ["test-vm-1"],
        }
    )
    mock_module.params = set_module_args(module_args)
    mock_module.exit_json.side_effect = exit_json
    mock_module.check_mode = False

    list_response = [
        {"vm": "vm-1001", "name": "test-vm-1", "power_state": "POWERED_ON"},
    ]
    detail_response = {
        "vm": "vm-1001",
        "name": "test-vm-1",
        "power_state": "POWERED_ON",
        "cpu": {"count": 2},
    }

    mock_client.get.side_effect = [
        _response(200, list_response),
        _response(200, detail_response),
    ]

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_module.exit_json.assert_called_once()
    result = exc.value.kwargs
    assert "info" in result
    assert len(result["info"]) == 1
    assert result["info"][0]["name"] == "test-vm-1"

    # The names filter should be passed through as a query parameter
    list_call = mock_client.get.call_args_list[0]
    assert list_call.kwargs["query"]["names"] == ["test-vm-1"]


def test_list_vms_by_power_states(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test listing virtual machines filtered by power state."""
    patch_create_client.return_value = mock_client
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module

    module_args.update(
        {
            "power_states": ["POWERED_ON"],
        }
    )
    mock_module.params = set_module_args(module_args)
    mock_module.exit_json.side_effect = exit_json
    mock_module.check_mode = False

    list_response = [
        {"vm": "vm-1001", "name": "test-vm-1", "power_state": "POWERED_ON"},
    ]
    detail_response = {
        "vm": "vm-1001",
        "name": "test-vm-1",
        "power_state": "POWERED_ON",
    }

    mock_client.get.side_effect = [
        _response(200, list_response),
        _response(200, detail_response),
    ]

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_module.exit_json.assert_called_once()
    result = exc.value.kwargs
    assert "info" in result
    assert len(result["info"]) == 1
    assert result["info"][0]["power_state"] == "POWERED_ON"

    list_call = mock_client.get.call_args_list[0]
    assert list_call.kwargs["query"]["power_states"] == ["POWERED_ON"]


def test_list_vms_by_vms_filter(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test listing virtual machines filtered by vm identifiers."""
    patch_create_client.return_value = mock_client
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module

    module_args.update(
        {
            "vms": ["vm-1001", "vm-1002"],
        }
    )
    mock_module.params = set_module_args(module_args)
    mock_module.exit_json.side_effect = exit_json
    mock_module.check_mode = False

    list_response = [
        {"vm": "vm-1001", "name": "test-vm-1", "power_state": "POWERED_ON"},
        {"vm": "vm-1002", "name": "test-vm-2", "power_state": "POWERED_OFF"},
    ]

    mock_client.get.side_effect = [
        _response(200, list_response),
        _response(200, {"vm": "vm-1001", "name": "test-vm-1"}),
        _response(200, {"vm": "vm-1002", "name": "test-vm-2"}),
    ]

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_module.exit_json.assert_called_once()
    result = exc.value.kwargs
    assert "info" in result
    assert len(result["info"]) == 2
    assert result["info"][0]["vm"] == "vm-1001"
    assert result["info"][1]["vm"] == "vm-1002"

    list_call = mock_client.get.call_args_list[0]
    assert list_call.kwargs["query"]["vms"] == ["vm-1001", "vm-1002"]


def test_list_vms_with_multiple_filters(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test listing virtual machines with multiple filters combined."""
    patch_create_client.return_value = mock_client
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module

    module_args.update(
        {
            "names": ["test-vm-1"],
            "clusters": ["domain-c1001"],
            "power_states": ["POWERED_ON"],
        }
    )
    mock_module.params = set_module_args(module_args)
    mock_module.exit_json.side_effect = exit_json
    mock_module.check_mode = False

    list_response = [
        {"vm": "vm-1001", "name": "test-vm-1", "power_state": "POWERED_ON"},
    ]
    detail_response = {
        "vm": "vm-1001",
        "name": "test-vm-1",
        "power_state": "POWERED_ON",
    }

    mock_client.get.side_effect = [
        _response(200, list_response),
        _response(200, detail_response),
    ]

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_module.exit_json.assert_called_once()
    result = exc.value.kwargs
    assert "info" in result
    assert len(result["info"]) == 1
    assert result["info"][0]["name"] == "test-vm-1"

    # All provided filters should be included in the list query
    list_query = mock_client.get.call_args_list[0].kwargs["query"]
    assert list_query["names"] == ["test-vm-1"]
    assert list_query["clusters"] == ["domain-c1001"]
    assert list_query["power_states"] == ["POWERED_ON"]


def test_list_vms_skips_item_deleted_during_enrichment(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test that a vm which 404s during detail enrichment is skipped."""
    patch_create_client.return_value = mock_client
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module

    module_args.update({})
    mock_module.params = set_module_args(module_args)
    mock_module.exit_json.side_effect = exit_json
    mock_module.check_mode = False

    list_response = [
        {"vm": "vm-1001", "name": "test-vm-1", "power_state": "POWERED_ON"},
        {"vm": "vm-1002", "name": "test-vm-2", "power_state": "POWERED_OFF"},
    ]

    # The second vm disappears between the list and the detail lookup.
    mock_client.get.side_effect = [
        _response(200, list_response),
        _response(200, {"vm": "vm-1001", "name": "test-vm-1"}),
        _response(404, None),
    ]

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_module.exit_json.assert_called_once()
    result = exc.value.kwargs
    # Only the vm that could be enriched should be returned
    assert "info" in result
    assert len(result["info"]) == 1
    assert result["info"][0]["vm"] == "vm-1001"


# ============================================================================
# Test Check Mode
# ============================================================================


class TestCheckMode:
    """Test check mode behavior."""

    def test_get_check_mode(
        self, patch_create_client, patch_ansible_module, mock_client, module_args
    ):
        """Test getting a vm in check mode (read-only executes normally)."""
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

        get_response = {
            "vm": "vm-1001",
            "name": "test-vm-1",
        }

        mock_client.get.return_value = _response(200, get_response)

        with pytest.raises(AnsibleExitJson) as exc:
            module_under_test.main()

        result = exc.value.kwargs
        # Info modules execute normally in check mode (read-only)
        assert result["id"] == "vm-1001"
        assert "value" in result
        mock_client.get.assert_called_once()

    def test_list_check_mode(
        self, patch_create_client, patch_ansible_module, mock_client, module_args
    ):
        """Test listing vms in check mode (read-only executes normally)."""
        patch_create_client.return_value = mock_client
        mock_module = MagicMock()
        patch_ansible_module.return_value = mock_module

        module_args.update({})
        mock_module.params = set_module_args(module_args)
        mock_module.exit_json.side_effect = exit_json
        mock_module.check_mode = True

        list_response = [
            {"vm": "vm-1001", "name": "test-vm-1"},
        ]
        detail_response = {
            "vm": "vm-1001",
            "name": "test-vm-1",
        }

        mock_client.get.side_effect = [
            _response(200, list_response),
            _response(200, detail_response),
        ]

        with pytest.raises(AnsibleExitJson) as exc:
            module_under_test.main()

        result = exc.value.kwargs
        # Info modules execute normally in check mode (read-only)
        assert "info" in result
        assert len(result["info"]) == 1


# ============================================================================
# Test Module Constants
# ============================================================================


class TestModuleConstants:
    """Test that module constants are correctly defined."""

    def test_moid_parameter_hints(self):
        """Test that MOID parameter hints are correct."""
        assert module_under_test.MOID_PARAMETER_HINTS == ["vm"]

    def test_list_endpoint(self):
        """Test that list API endpoint is correct."""
        assert module_under_test.LIST_ENDPOINT == "/vcenter/vm"

    def test_item_endpoint(self):
        """Test that item API endpoint is correct."""
        assert module_under_test.ITEM_ENDPOINT == "/vcenter/vm/{vm}"


# ============================================================================
# Test OperationConfig Behavior
# ============================================================================


class TestOperationConfig:
    """Test the module's operation configs build paths and queries correctly."""

    def test_get_operation_build_path(self):
        """Test that the GET operation builds the item path from params."""
        path = module_under_test.GET_OPERATION.build_path({"vm": "vm-1001"})
        assert path == "/vcenter/vm/vm-1001"

    def test_list_operation_build_path(self):
        """Test that the LIST operation returns the collection path."""
        path = module_under_test.LIST_OPERATION.build_path({})
        assert path == "/vcenter/vm"

    def test_list_operation_build_query_with_filters(self):
        """Test that provided filters are included in the list query."""
        query = module_under_test.LIST_OPERATION.build_query(
            {"names": ["test-vm-1"], "power_states": ["POWERED_ON"]}
        )
        assert query == {
            "names": ["test-vm-1"],
            "power_states": ["POWERED_ON"],
        }

    def test_list_operation_build_query_omits_unset(self):
        """Test that unset optional filters are omitted from the query."""
        query = module_under_test.LIST_OPERATION.build_query({})
        assert query == {}


# ============================================================================
# Test Argument Spec
# ============================================================================


class TestArgumentSpec:
    """Test the module argument specification."""

    def test_vm_parameter(self):
        """Test that the vm identifier parameter is correctly defined."""
        spec = module_under_test.create_module_argument_spec()
        assert spec["vm"]["type"] == "str"

    @pytest.mark.parametrize(
        "param",
        [
            "vms",
            "names",
            "folders",
            "datacenters",
            "hosts",
            "clusters",
            "resource_pools",
            "power_states",
        ],
    )
    def test_list_filter_parameters(self, param):
        """Test that filter parameters are lists of strings."""
        spec = module_under_test.create_module_argument_spec()
        assert spec[param]["type"] == "list"
        assert spec[param]["elements"] == "str"

    def test_filter_aliases(self):
        """Test that documented filter aliases are defined."""
        spec = module_under_test.create_module_argument_spec()
        assert spec["names"]["aliases"] == ["filter_names"]
        assert spec["folders"]["aliases"] == ["filter_folders"]
        assert spec["datacenters"]["aliases"] == ["filter_datacenters"]
