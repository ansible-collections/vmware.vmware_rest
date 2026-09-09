# -*- coding: utf-8 -*-
# Copyright: (c) 2026, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Unit tests for vcenter_folder_info module.

Tests validate the info module behavior using the OperationConfig-based
architecture with mocked HTTP clients. The module has no dedicated list
operation: its get operation targets the collection endpoint (/vcenter/folder)
and returns a list of folder summaries filtered by the supplied query
parameters.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import pytest
from unittest.mock import patch, MagicMock

from ansible_collections.vmware.vmware_rest.plugins.modules import (
    vcenter_folder_info as module_under_test,
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
# Test LIST Operations (Collection GET)
# ============================================================================


def test_list_all_folders(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test listing all folders."""
    patch_create_client.return_value = mock_client
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module

    module_args.update({})  # No filters
    mock_module.params = set_module_args(module_args)
    mock_module.exit_json.side_effect = exit_json
    mock_module.check_mode = False

    list_response = [
        {"folder": "group-v1", "name": "vm", "type": "VIRTUAL_MACHINE"},
        {"folder": "group-h1", "name": "host", "type": "HOST"},
    ]

    mock_client.get.return_value = _response(200, list_response)

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_module.exit_json.assert_called_once()
    result = exc.value.kwargs
    assert "info" in result
    assert isinstance(result["info"], list)
    assert len(result["info"]) == 2
    assert result["info"][0]["folder"] == "group-v1"
    assert result["info"][1]["folder"] == "group-h1"
    # A single collection GET returns the full list; no per-item enrichment.
    mock_client.get.assert_called_once()


def test_list_folders_empty(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test listing folders when none exist."""
    patch_create_client.return_value = mock_client
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module

    module_args.update({})
    mock_module.params = set_module_args(module_args)
    mock_module.exit_json.side_effect = exit_json
    mock_module.check_mode = False

    mock_client.get.return_value = _response(200, [])

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_module.exit_json.assert_called_once()
    result = exc.value.kwargs
    assert "info" in result
    assert len(result["info"]) == 0


def test_list_folders_single_result(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test listing folders when only one matches."""
    patch_create_client.return_value = mock_client
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module

    module_args.update(
        {
            "names": ["vm"],
        }
    )
    mock_module.params = set_module_args(module_args)
    mock_module.exit_json.side_effect = exit_json
    mock_module.check_mode = False

    list_response = [
        {"folder": "group-v1", "name": "vm", "type": "VIRTUAL_MACHINE"},
    ]

    mock_client.get.return_value = _response(200, list_response)

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_module.exit_json.assert_called_once()
    result = exc.value.kwargs
    assert "info" in result
    assert len(result["info"]) == 1
    # A single result also exposes the value as a dict.
    assert result["value"]["name"] == "vm"


def test_list_folders_by_type_filter(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test listing folders filtered by the nested filter.type option."""
    patch_create_client.return_value = mock_client
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module

    module_args.update(
        {
            "filter": {"type": "VIRTUAL_MACHINE"},
        }
    )
    mock_module.params = set_module_args(module_args)
    mock_module.exit_json.side_effect = exit_json
    mock_module.check_mode = False

    list_response = [
        {"folder": "group-v1", "name": "vm", "type": "VIRTUAL_MACHINE"},
        {"folder": "group-v2", "name": "templates", "type": "VIRTUAL_MACHINE"},
    ]

    mock_client.get.return_value = _response(200, list_response)

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_module.exit_json.assert_called_once()
    result = exc.value.kwargs
    assert "info" in result
    assert len(result["info"]) == 2
    assert all(f["type"] == "VIRTUAL_MACHINE" for f in result["info"])


def test_list_folders_with_multiple_filters(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test listing folders with multiple filters combined."""
    patch_create_client.return_value = mock_client
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module

    module_args.update(
        {
            "names": ["vm"],
            "parent_folders": ["group-d1"],
            "datacenters": ["datacenter-1001"],
        }
    )
    mock_module.params = set_module_args(module_args)
    mock_module.exit_json.side_effect = exit_json
    mock_module.check_mode = False

    list_response = [
        {"folder": "group-v1", "name": "vm", "type": "VIRTUAL_MACHINE"},
    ]

    mock_client.get.return_value = _response(200, list_response)

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_module.exit_json.assert_called_once()
    result = exc.value.kwargs
    assert "info" in result
    assert len(result["info"]) == 1
    assert result["info"][0]["name"] == "vm"


# ============================================================================
# Test Check Mode
# ============================================================================


class TestCheckMode:
    """Test check mode behavior."""

    def test_list_check_mode(
        self, patch_create_client, patch_ansible_module, mock_client, module_args
    ):
        """Test listing folders in check mode."""
        patch_create_client.return_value = mock_client
        mock_module = MagicMock()
        patch_ansible_module.return_value = mock_module

        module_args.update({})
        mock_module.params = set_module_args(module_args)
        mock_module.exit_json.side_effect = exit_json
        mock_module.check_mode = True

        list_response = [
            {"folder": "group-v1", "name": "vm"},
        ]

        mock_client.get.return_value = _response(200, list_response)

        with pytest.raises(AnsibleExitJson) as exc:
            module_under_test.main()

        result = exc.value.kwargs
        # Info modules execute normally in check mode (read-only)
        assert "info" in result
        assert len(result["info"]) == 1
        mock_client.get.assert_called_once()


# ============================================================================
# Test Module Constants
# ============================================================================


class TestModuleConstants:
    """Test that module constants are correctly defined."""

    def test_moid_parameter_hints(self):
        """Test that MOID parameter hints are correct."""
        assert module_under_test.MOID_PARAMETER_HINTS == []

    def test_item_endpoint(self):
        """Test that item API endpoint is correct."""
        assert module_under_test.ITEM_ENDPOINT == "/vcenter/folder"


# ============================================================================
# Test OperationConfig
# ============================================================================


class TestOperationConfig:
    """Test the OperationConfig definitions."""

    def test_get_operation_build_path(self):
        """Test that the GET operation targets the collection endpoint."""
        path = module_under_test.GET_OPERATION.build_path({})
        assert path == "/vcenter/folder"

    def test_get_operation_build_query(self):
        """Test that the GET operation builds query parameters from filters."""
        query = module_under_test.GET_OPERATION.build_query(
            {"names": ["vm"], "parent_folders": ["group-d1"]}
        )
        assert query["names"] == ["vm"]
        assert query["parent_folders"] == ["group-d1"]

    def test_get_operation_build_query_nested_filter(self):
        """Test that the nested filter.type subspec is built into the query."""
        query = module_under_test.GET_OPERATION.build_query(
            {"filter": {"type": "VIRTUAL_MACHINE"}}
        )
        assert query["filter"] == {"type": "VIRTUAL_MACHINE"}

    def test_get_operation_build_query_omits_unset(self):
        """Test that unset filters are omitted from the query."""
        query = module_under_test.GET_OPERATION.build_query({"names": ["vm"]})
        assert query == {"names": ["vm"]}


# ============================================================================
# Test Argument Spec
# ============================================================================


class TestArgumentSpec:
    """Test the module argument specification."""

    def test_create_module_argument_spec_names(self):
        """Test that names filter parameter is correctly defined."""
        spec = module_under_test.create_module_argument_spec()

        assert "names" in spec
        assert spec["names"]["type"] == "list"
        assert spec["names"]["elements"] == "str"
        assert "filter_names" in spec["names"]["aliases"]

    def test_create_module_argument_spec_folders(self):
        """Test that folders filter parameter is correctly defined."""
        spec = module_under_test.create_module_argument_spec()

        assert "folders" in spec
        assert spec["folders"]["type"] == "list"
        assert "filter_folders" in spec["folders"]["aliases"]

    def test_create_module_argument_spec_parent_folders(self):
        """Test that parent_folders filter parameter is correctly defined."""
        spec = module_under_test.create_module_argument_spec()

        assert "parent_folders" in spec
        assert spec["parent_folders"]["type"] == "list"
        assert spec["parent_folders"]["elements"] == "str"

    def test_create_module_argument_spec_datacenters(self):
        """Test that datacenters filter parameter is correctly defined."""
        spec = module_under_test.create_module_argument_spec()

        assert "datacenters" in spec
        assert spec["datacenters"]["type"] == "list"
        assert "filter_datacenters" in spec["datacenters"]["aliases"]

    def test_create_module_argument_spec_filter(self):
        """Test that the nested filter parameter and its type choices exist."""
        spec = module_under_test.create_module_argument_spec()

        assert "filter" in spec
        assert spec["filter"]["type"] == "dict"
        type_option = spec["filter"]["options"]["type"]
        assert set(type_option["choices"]) == {
            "DATACENTER",
            "DATASTORE",
            "HOST",
            "NETWORK",
            "VIRTUAL_MACHINE",
        }

    def test_create_module_argument_spec_connection_params(self):
        """Test that connection parameters are included."""
        spec = module_under_test.create_module_argument_spec()

        assert "vcenter_hostname" in spec
        assert "vcenter_username" in spec
        assert "vcenter_password" in spec
