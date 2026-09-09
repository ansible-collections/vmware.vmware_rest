# -*- coding: utf-8 -*-
# Copyright: (c) 2026, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Unit tests for vcenter_datastore_info module.

Tests validate the info module behavior using the OperationConfig-based
architecture with mocked HTTP clients. The module supports both a get-by-id
operation (/vcenter/datastore/{datastore}) and a list operation
(/vcenter/datastore) whose summaries are enriched with per-item detail lookups.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import pytest
from unittest.mock import patch, MagicMock

from ansible_collections.vmware.vmware_rest.plugins.modules import (
    vcenter_datastore_info as module_under_test,
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


def test_get_datastore_by_id(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test getting a specific datastore by ID."""
    patch_create_client.return_value = mock_client
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module

    module_args.update(
        {
            "datastore": "datastore-1009",
        }
    )
    mock_module.params = set_module_args(module_args)
    mock_module.exit_json.side_effect = exit_json
    mock_module.check_mode = False

    get_response = {
        "datastore": "datastore-1009",
        "name": "my_datastore",
        "type": "VMFS",
        "free_space": 1024,
        "capacity": 4096,
    }

    mock_client.get.return_value = _response(200, get_response)

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_module.exit_json.assert_called_once()
    result = exc.value.kwargs
    assert result["id"] == "datastore-1009"
    assert "value" in result
    assert result["value"]["datastore"] == "datastore-1009"
    assert result["value"]["name"] == "my_datastore"
    assert result["value"]["type"] == "VMFS"


def test_get_datastore_not_found(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test getting a datastore that doesn't exist."""
    patch_create_client.return_value = mock_client
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module

    module_args.update(
        {
            "datastore": "datastore-9999",
        }
    )
    mock_module.params = set_module_args(module_args)
    mock_module.exit_json.side_effect = exit_json
    mock_module.check_mode = False

    mock_client.get.return_value = _response(404, None)

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_module.exit_json.assert_called_once()
    result = exc.value.kwargs
    # Info modules return empty info list when not found
    assert "info" in result
    assert len(result["info"]) == 0


# ============================================================================
# Test LIST Operations (Multiple Resources)
# ============================================================================


def test_list_all_datastores(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test listing all datastores."""
    patch_create_client.return_value = mock_client
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module

    module_args.update({})  # No filters
    mock_module.params = set_module_args(module_args)
    mock_module.exit_json.side_effect = exit_json
    mock_module.check_mode = False

    list_response = [
        {"datastore": "datastore-1001", "name": "ds-prod", "type": "VMFS"},
        {"datastore": "datastore-1002", "name": "ds-dev", "type": "NFS"},
    ]
    detail_response_1 = {
        "datastore": "datastore-1001",
        "name": "ds-prod",
        "type": "VMFS",
        "capacity": 4096,
    }
    detail_response_2 = {
        "datastore": "datastore-1002",
        "name": "ds-dev",
        "type": "NFS",
        "capacity": 2048,
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
    assert result["info"][0]["datastore"] == "datastore-1001"
    assert result["info"][1]["datastore"] == "datastore-1002"


def test_list_datastores_empty(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test listing datastores when none exist."""
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


def test_list_datastores_by_names(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test listing datastores filtered by names."""
    patch_create_client.return_value = mock_client
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module

    module_args.update(
        {
            "names": ["ds-prod", "ds-dev"],
        }
    )
    mock_module.params = set_module_args(module_args)
    mock_module.exit_json.side_effect = exit_json
    mock_module.check_mode = False

    list_response = [
        {"datastore": "datastore-1001", "name": "ds-prod"},
        {"datastore": "datastore-1002", "name": "ds-dev"},
    ]

    mock_client.get.side_effect = [
        _response(200, list_response),
        _response(200, {"datastore": "datastore-1001", "name": "ds-prod"}),
        _response(200, {"datastore": "datastore-1002", "name": "ds-dev"}),
    ]

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_module.exit_json.assert_called_once()
    result = exc.value.kwargs
    assert "info" in result
    assert isinstance(result["info"], list)
    assert mock_client.get.called


def test_list_datastores_by_types(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test listing datastores filtered by type."""
    patch_create_client.return_value = mock_client
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module

    module_args.update(
        {
            "types": ["VMFS"],
        }
    )
    mock_module.params = set_module_args(module_args)
    mock_module.exit_json.side_effect = exit_json
    mock_module.check_mode = False

    list_response = [
        {"datastore": "datastore-1001", "name": "ds-prod", "type": "VMFS"},
    ]
    detail_response = {
        "datastore": "datastore-1001",
        "name": "ds-prod",
        "type": "VMFS",
        "capacity": 4096,
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
    assert result["info"][0]["type"] == "VMFS"


def test_list_datastores_by_datastores_filter(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test listing datastores filtered by datastore IDs."""
    patch_create_client.return_value = mock_client
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module

    module_args.update(
        {
            "datastores": ["datastore-1001", "datastore-1002"],
        }
    )
    mock_module.params = set_module_args(module_args)
    mock_module.exit_json.side_effect = exit_json
    mock_module.check_mode = False

    list_response = [
        {"datastore": "datastore-1001", "name": "ds1"},
        {"datastore": "datastore-1002", "name": "ds2"},
    ]

    mock_client.get.side_effect = [
        _response(200, list_response),
        _response(200, {"datastore": "datastore-1001", "name": "ds1"}),
        _response(200, {"datastore": "datastore-1002", "name": "ds2"}),
    ]

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_module.exit_json.assert_called_once()
    result = exc.value.kwargs
    assert "info" in result
    assert len(result["info"]) == 2
    assert result["info"][0]["datastore"] == "datastore-1001"
    assert result["info"][1]["datastore"] == "datastore-1002"


def test_list_datastores_with_multiple_filters(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test listing datastores with multiple filters."""
    patch_create_client.return_value = mock_client
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module

    module_args.update(
        {
            "names": ["ds-prod"],
            "folders": ["group-s1"],
            "datacenters": ["datacenter-1001"],
        }
    )
    mock_module.params = set_module_args(module_args)
    mock_module.exit_json.side_effect = exit_json
    mock_module.check_mode = False

    list_response = [
        {"datastore": "datastore-1001", "name": "ds-prod"},
    ]
    detail_response = {
        "datastore": "datastore-1001",
        "name": "ds-prod",
        "type": "VMFS",
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
    assert result["info"][0]["name"] == "ds-prod"


# ============================================================================
# Test Check Mode
# ============================================================================


class TestCheckMode:
    """Test check mode behavior."""

    def test_get_check_mode(
        self, patch_create_client, patch_ansible_module, mock_client, module_args
    ):
        """Test getting a datastore in check mode."""
        patch_create_client.return_value = mock_client
        mock_module = MagicMock()
        patch_ansible_module.return_value = mock_module

        module_args.update(
            {
                "datastore": "datastore-1009",
            }
        )
        mock_module.params = set_module_args(module_args)
        mock_module.exit_json.side_effect = exit_json
        mock_module.check_mode = True

        get_response = {
            "datastore": "datastore-1009",
            "name": "my_datastore",
        }

        mock_client.get.return_value = _response(200, get_response)

        with pytest.raises(AnsibleExitJson) as exc:
            module_under_test.main()

        result = exc.value.kwargs
        # Info modules execute normally in check mode (read-only)
        assert result["id"] == "datastore-1009"
        assert "value" in result
        mock_client.get.assert_called_once()

    def test_list_check_mode(
        self, patch_create_client, patch_ansible_module, mock_client, module_args
    ):
        """Test listing datastores in check mode."""
        patch_create_client.return_value = mock_client
        mock_module = MagicMock()
        patch_ansible_module.return_value = mock_module

        module_args.update({})
        mock_module.params = set_module_args(module_args)
        mock_module.exit_json.side_effect = exit_json
        mock_module.check_mode = True

        list_response = [
            {"datastore": "datastore-1001", "name": "ds1"},
        ]
        detail_response = {
            "datastore": "datastore-1001",
            "name": "ds1",
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
        assert module_under_test.MOID_PARAMETER_HINTS == ["datastore"]

    def test_list_endpoint(self):
        """Test that list API endpoint is correct."""
        assert module_under_test.LIST_ENDPOINT == "/vcenter/datastore"

    def test_item_endpoint(self):
        """Test that item API endpoint is correct."""
        assert module_under_test.ITEM_ENDPOINT == "/vcenter/datastore/{datastore}"


# ============================================================================
# Test OperationConfig
# ============================================================================


class TestOperationConfig:
    """Test the OperationConfig definitions."""

    def test_get_operation_build_path(self):
        """Test that the GET operation builds the item path."""
        path = module_under_test.GET_OPERATION.build_path(
            {"datastore": "datastore-1009"}
        )
        assert path == "/vcenter/datastore/datastore-1009"

    def test_list_operation_build_path(self):
        """Test that the LIST operation builds the collection path."""
        path = module_under_test.LIST_OPERATION.build_path({})
        assert path == "/vcenter/datastore"

    def test_list_operation_build_query(self):
        """Test that the LIST operation builds query parameters from filters."""
        query = module_under_test.LIST_OPERATION.build_query(
            {"names": ["ds-prod"], "types": ["VMFS"]}
        )
        assert query["names"] == ["ds-prod"]
        assert query["types"] == ["VMFS"]

    def test_list_operation_build_query_omits_unset(self):
        """Test that unset filters are omitted from the query."""
        query = module_under_test.LIST_OPERATION.build_query({"names": ["ds-prod"]})
        assert query == {"names": ["ds-prod"]}


# ============================================================================
# Test Argument Spec
# ============================================================================


class TestArgumentSpec:
    """Test the module argument specification."""

    def test_create_module_argument_spec_datastore(self):
        """Test that datastore parameter is correctly defined."""
        spec = module_under_test.create_module_argument_spec()

        assert "datastore" in spec
        assert spec["datastore"]["type"] == "str"

    def test_create_module_argument_spec_datastores(self):
        """Test that datastores filter parameter is correctly defined."""
        spec = module_under_test.create_module_argument_spec()

        assert "datastores" in spec
        assert spec["datastores"]["type"] == "list"
        assert spec["datastores"]["elements"] == "str"

    def test_create_module_argument_spec_names(self):
        """Test that names filter parameter is correctly defined."""
        spec = module_under_test.create_module_argument_spec()

        assert "names" in spec
        assert spec["names"]["type"] == "list"
        assert spec["names"]["elements"] == "str"
        assert "filter_names" in spec["names"]["aliases"]

    def test_create_module_argument_spec_types(self):
        """Test that types filter parameter is correctly defined."""
        spec = module_under_test.create_module_argument_spec()

        assert "types" in spec
        assert spec["types"]["type"] == "list"
        assert "filter_types" in spec["types"]["aliases"]

    def test_create_module_argument_spec_folders(self):
        """Test that folders filter parameter is correctly defined."""
        spec = module_under_test.create_module_argument_spec()

        assert "folders" in spec
        assert spec["folders"]["type"] == "list"
        assert "filter_folders" in spec["folders"]["aliases"]

    def test_create_module_argument_spec_datacenters(self):
        """Test that datacenters filter parameter is correctly defined."""
        spec = module_under_test.create_module_argument_spec()

        assert "datacenters" in spec
        assert spec["datacenters"]["type"] == "list"
        assert "filter_datacenters" in spec["datacenters"]["aliases"]

    def test_create_module_argument_spec_connection_params(self):
        """Test that connection parameters are included."""
        spec = module_under_test.create_module_argument_spec()

        assert "vcenter_hostname" in spec
        assert "vcenter_username" in spec
        assert "vcenter_password" in spec
