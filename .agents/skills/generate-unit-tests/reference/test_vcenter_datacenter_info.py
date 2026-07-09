# -*- coding: utf-8 -*-
# Copyright: (c) 2026, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import pytest
from unittest.mock import patch, MagicMock

from ansible_collections.vmware.vmware_rest.plugins.modules import (
    vcenter_datacenter_info as module_under_test,
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
# Test LIST Operations
# ============================================================================


def test_list_all_datacenters(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test listing all datacenters."""
    patch_create_client.return_value = mock_client
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module

    module_args.update({})
    mock_module.params = set_module_args(module_args)
    mock_module.exit_json.side_effect = exit_json
    mock_module.check_mode = False

    # Mock list response (summary)
    list_response = [
        {"datacenter": "datacenter-1001", "name": "datacenter1"},
        {"datacenter": "datacenter-1002", "name": "datacenter2"},
    ]

    # Mock individual GET responses (detailed info for each datacenter)
    get_response_1 = {
        "datacenter": "datacenter-1001",
        "name": "datacenter1",
        "datastore_folder": "group-s5",
        "host_folder": "group-h4",
        "network_folder": "group-n6",
        "vm_folder": "group-v3",
    }

    get_response_2 = {
        "datacenter": "datacenter-1002",
        "name": "datacenter2",
        "datastore_folder": "group-s5",
        "host_folder": "group-h4",
        "network_folder": "group-n6",
        "vm_folder": "group-v3",
    }

    # First call: LIST, then GET for each datacenter
    mock_client.get.side_effect = [
        _response(200, list_response),
        _response(200, get_response_1),
        _response(200, get_response_2),
    ]

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_module.exit_json.assert_called_once()
    result = exc.value.kwargs
    assert "datacenters" in result
    assert len(result["datacenters"]) == 2
    assert result["datacenters"][0]["datacenter"] == "datacenter-1001"
    assert result["datacenters"][0]["name"] == "datacenter1"
    assert result["datacenters"][1]["datacenter"] == "datacenter-1002"
    assert result["datacenters"][1]["name"] == "datacenter2"


def test_list_datacenters_empty(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test listing datacenters when none exist."""
    patch_create_client.return_value = mock_client
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module

    module_args.update({})
    mock_module.params = set_module_args(module_args)
    mock_module.exit_json.side_effect = exit_json
    mock_module.check_mode = False

    # Mock empty list response
    list_response = []

    mock_client.get.return_value = _response(200, list_response)

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_module.exit_json.assert_called_once()
    result = exc.value.kwargs
    assert "datacenters" in result
    assert len(result["datacenters"]) == 0


def test_list_datacenters_with_name_filter(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test listing datacenters filtered by name."""
    patch_create_client.return_value = mock_client
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module

    module_args.update({"names": ["datacenter1"]})
    mock_module.params = set_module_args(module_args)
    mock_module.exit_json.side_effect = exit_json
    mock_module.check_mode = False

    # Mock filtered list response
    list_response = [
        {"datacenter": "datacenter-1001", "name": "datacenter1"},
    ]

    # Mock GET for detailed info
    get_response = {
        "datacenter": "datacenter-1001",
        "name": "datacenter1",
        "datastore_folder": "group-s5",
    }

    mock_client.get.side_effect = [
        _response(200, list_response),
        _response(200, get_response),
    ]

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    result = exc.value.kwargs
    assert "datacenters" in result
    assert len(result["datacenters"]) == 1
    assert result["datacenters"][0]["name"] == "datacenter1"


def test_list_datacenters_with_folder_filter(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test listing datacenters filtered by folder."""
    patch_create_client.return_value = mock_client
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module

    module_args.update({"folders": ["group-d1"]})
    mock_module.params = set_module_args(module_args)
    mock_module.exit_json.side_effect = exit_json
    mock_module.check_mode = False

    # Mock filtered list response
    list_response = [
        {"datacenter": "datacenter-1001", "name": "datacenter1"},
    ]

    # Mock GET for detailed info
    get_response = {
        "datacenter": "datacenter-1001",
        "name": "datacenter1",
        "datastore_folder": "group-s5",
    }

    mock_client.get.side_effect = [
        _response(200, list_response),
        _response(200, get_response),
    ]

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    result = exc.value.kwargs
    assert "datacenters" in result
    assert len(result["datacenters"]) == 1


# ============================================================================
# Test GET Operations
# ============================================================================


def test_get_datacenter_by_id(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test getting a specific datacenter by ID."""
    patch_create_client.return_value = mock_client
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module

    module_args.update({"datacenter": "datacenter-1001"})
    mock_module.params = set_module_args(module_args)
    mock_module.exit_json.side_effect = exit_json
    mock_module.check_mode = False

    # Mock GET response
    get_response = {
        "name": "my_datacenter",
        "datastore_folder": "group-s5",
        "host_folder": "group-h4",
        "network_folder": "group-n6",
        "vm_folder": "group-v3",
    }

    # Mock list response for enrichment
    list_response = [
        {"datacenter": "datacenter-1001", "name": "my_datacenter"},
    ]

    mock_client.get.side_effect = [
        _response(200, get_response),
        _response(200, list_response),
    ]

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_module.exit_json.assert_called_once()
    result = exc.value.kwargs
    assert result["id"] == "datacenter-1001"
    assert "value" in result
    assert result["value"]["name"] == "my_datacenter"
    assert result["value"]["datastore_folder"] == "group-s5"
    assert "datacenters" in result
    assert len(result["datacenters"]) == 1
    assert result["datacenters"][0]["datacenter"] == "datacenter-1001"


def test_get_datacenter_not_found(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test getting a datacenter that doesn't exist."""
    patch_create_client.return_value = mock_client
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module

    module_args.update({"datacenter": "datacenter-9999"})
    mock_module.params = set_module_args(module_args)
    mock_module.exit_json.side_effect = exit_json
    mock_module.check_mode = False

    # Mock 404 response
    mock_client.get.return_value = _response(404, None)

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    result = exc.value.kwargs
    # When resource not found, module returns empty result
    assert "datacenters" in result
    assert len(result["datacenters"]) == 0


# ============================================================================
# Test Module Constants
# ============================================================================


class TestModuleConstants:
    """Test that module constants are correctly defined."""

    def test_moid_attribute_name(self):
        """Test that MOID attribute name is correct."""
        assert module_under_test.MOID_ATTRIBUTE_NAME == "datacenter"

    def test_list_path(self):
        """Test that list API path is correct."""
        assert module_under_test.LIST_PATH == "/vcenter/datacenter"

    def test_item_path(self):
        """Test that item API path is correct."""
        assert module_under_test.ITEM_PATH == "/vcenter/datacenter/{datacenter}"

    def test_payload_format_structure(self):
        """Test that payload format constants exist."""
        assert hasattr(module_under_test, "GET_PAYLOAD_MAP")
        assert hasattr(module_under_test, "LIST_PAYLOAD_MAP")

        # Verify GET operation has path mapping
        assert module_under_test.GET_PAYLOAD_MAP._path is not None

        # Verify list operation has query mapping
        assert module_under_test.LIST_PAYLOAD_MAP._query is not None


# ============================================================================
# Test PayloadMap Configurations
# ============================================================================


class TestPayloadMappings:
    """Test PayloadMap configurations for the module."""

    def test_get_path_mapping(self):
        """Test GET path mapping."""
        payload_map = module_under_test.GET_PAYLOAD_MAP

        params = {"datacenter": "datacenter-1001"}

        result = payload_map._path.params_to_payload(params)
        assert result["datacenter"] == "datacenter-1001"

    def test_list_query_mapping_all_filters(self):
        """Test LIST query mapping with all filter parameters."""
        payload_map = module_under_test.LIST_PAYLOAD_MAP

        params = {
            "datacenters": ["datacenter-1001", "datacenter-1002"],
            "names": ["dc1", "dc2"],
            "folders": ["group-d1"],
        }

        result = payload_map._query.params_to_payload(params)
        assert result["datacenters"] == ["datacenter-1001", "datacenter-1002"]
        assert result["names"] == ["dc1", "dc2"]
        assert result["folders"] == ["group-d1"]

    def test_list_query_mapping_partial_filters(self):
        """Test LIST query mapping with partial filter parameters."""
        payload_map = module_under_test.LIST_PAYLOAD_MAP

        params = {
            "names": ["dc1"],
        }

        result = payload_map._query.params_to_payload(params)
        assert result["names"] == ["dc1"]
        assert "datacenters" not in result
        assert "folders" not in result


# ============================================================================
# Test Argument Spec
# ============================================================================


class TestArgumentSpec:
    """Test the module argument specification."""

    def test_create_module_argument_spec_datacenter(self):
        """Test that datacenter parameter is correctly defined."""
        spec = module_under_test.create_module_argument_spec()

        assert "datacenter" in spec
        assert spec["datacenter"]["type"] == "str"

    def test_create_module_argument_spec_datacenters_filter(self):
        """Test that datacenters filter parameter is correctly defined."""
        spec = module_under_test.create_module_argument_spec()

        assert "datacenters" in spec
        assert spec["datacenters"]["type"] == "list"
        assert spec["datacenters"]["elements"] == "str"
        assert "filter_datacenters" in spec["datacenters"]["aliases"]

    def test_create_module_argument_spec_names_filter(self):
        """Test that names filter parameter is correctly defined."""
        spec = module_under_test.create_module_argument_spec()

        assert "names" in spec
        assert spec["names"]["type"] == "list"
        assert spec["names"]["elements"] == "str"
        assert "filter_names" in spec["names"]["aliases"]

    def test_create_module_argument_spec_folders_filter(self):
        """Test that folders filter parameter is correctly defined."""
        spec = module_under_test.create_module_argument_spec()

        assert "folders" in spec
        assert spec["folders"]["type"] == "list"
        assert spec["folders"]["elements"] == "str"
        assert "filter_folders" in spec["folders"]["aliases"]


# ============================================================================
# Test Check Mode
# ============================================================================


class TestCheckMode:
    """Test check mode behavior (info modules are always check mode safe)."""

    def test_list_in_check_mode(
        self, patch_create_client, patch_ansible_module, mock_client, module_args
    ):
        """Test that listing works in check mode."""
        patch_create_client.return_value = mock_client
        mock_module = MagicMock()
        patch_ansible_module.return_value = mock_module

        module_args.update({})
        mock_module.params = set_module_args(module_args)
        mock_module.exit_json.side_effect = exit_json
        mock_module.check_mode = True

        list_response = [
            {"datacenter": "datacenter-1001", "name": "datacenter1"},
        ]

        # Mock GET for detailed info
        get_response = {
            "datacenter": "datacenter-1001",
            "name": "datacenter1",
            "datastore_folder": "group-s5",
        }

        mock_client.get.side_effect = [
            _response(200, list_response),
            _response(200, get_response),
        ]

        with pytest.raises(AnsibleExitJson) as exc:
            module_under_test.main()

        result = exc.value.kwargs
        assert "datacenters" in result
        assert len(result["datacenters"]) == 1

    def test_get_in_check_mode(
        self, patch_create_client, patch_ansible_module, mock_client, module_args
    ):
        """Test that getting a specific resource works in check mode."""
        patch_create_client.return_value = mock_client
        mock_module = MagicMock()
        patch_ansible_module.return_value = mock_module

        module_args.update({"datacenter": "datacenter-1001"})
        mock_module.params = set_module_args(module_args)
        mock_module.exit_json.side_effect = exit_json
        mock_module.check_mode = True

        get_response = {
            "name": "my_datacenter",
            "datastore_folder": "group-s5",
        }

        list_response = [
            {"datacenter": "datacenter-1001", "name": "my_datacenter"},
        ]

        mock_client.get.side_effect = [
            _response(200, get_response),
            _response(200, list_response),
        ]

        with pytest.raises(AnsibleExitJson) as exc:
            module_under_test.main()

        result = exc.value.kwargs
        assert result["id"] == "datacenter-1001"
        assert "value" in result
