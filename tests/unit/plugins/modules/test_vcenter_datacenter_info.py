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
# Test GET Operations (Single Resource)
# ============================================================================


def test_get_datacenter_by_id(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test getting a specific datacenter by ID."""
    patch_create_client.return_value = mock_client
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module

    module_args.update(
        {
            "datacenter": "datacenter-1009",
        }
    )
    mock_module.params = set_module_args(module_args)
    mock_module.exit_json.side_effect = exit_json
    mock_module.check_mode = False

    # Mock GET response returns datacenter info
    get_response = {
        "datacenter": "datacenter-1009",
        "name": "my_datacenter",
    }

    mock_client.get.return_value = _response(200, get_response)

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_module.exit_json.assert_called_once()
    result = exc.value.kwargs
    assert result["id"] == "datacenter-1009"
    assert "value" in result
    assert result["value"]["datacenter"] == "datacenter-1009"
    assert result["value"]["name"] == "my_datacenter"


def test_get_datacenter_not_found(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test getting a datacenter that doesn't exist."""
    patch_create_client.return_value = mock_client
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module

    module_args.update(
        {
            "datacenter": "datacenter-9999",
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
    # Info modules return empty info list when not found
    assert "info" in result
    assert len(result["info"]) == 0


# ============================================================================
# Test LIST Operations (Multiple Resources)
# ============================================================================


def test_list_all_datacenters(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test listing all datacenters."""
    patch_create_client.return_value = mock_client
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module

    module_args.update({})  # No filters
    mock_module.params = set_module_args(module_args)
    mock_module.exit_json.side_effect = exit_json
    mock_module.check_mode = False

    # Mock LIST response returns all datacenters
    list_response = [
        {"datacenter": "datacenter-1001", "name": "production-dc"},
        {"datacenter": "datacenter-1002", "name": "development-dc"},
    ]

    mock_client.get.return_value = _response(200, list_response)

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_module.exit_json.assert_called_once()
    result = exc.value.kwargs
    assert "info" in result
    # The base class wraps list results
    assert isinstance(result["info"], list)


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

    # Mock LIST response returns empty list
    mock_client.get.return_value = _response(200, [])

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_module.exit_json.assert_called_once()
    result = exc.value.kwargs
    assert "info" in result
    assert len(result["info"]) == 0


def test_list_datacenters_by_names(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test listing datacenters filtered by names."""
    patch_create_client.return_value = mock_client
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module

    module_args.update(
        {
            "names": ["production-dc", "development-dc"],
        }
    )
    mock_module.params = set_module_args(module_args)
    mock_module.exit_json.side_effect = exit_json
    mock_module.check_mode = False

    # Mock LIST response with filter
    list_response = [
        {"datacenter": "datacenter-1001", "name": "production-dc"},
        {"datacenter": "datacenter-1002", "name": "development-dc"},
    ]

    mock_client.get.return_value = _response(200, list_response)

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_module.exit_json.assert_called_once()
    result = exc.value.kwargs
    assert "info" in result
    assert isinstance(result["info"], list)
    # Module may make multiple GET calls to fetch details
    assert mock_client.get.called


def test_list_datacenters_by_folders(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test listing datacenters filtered by folders."""
    patch_create_client.return_value = mock_client
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module

    module_args.update(
        {
            "folders": ["group-d1", "group-d2"],
        }
    )
    mock_module.params = set_module_args(module_args)
    mock_module.exit_json.side_effect = exit_json
    mock_module.check_mode = False

    # First GET returns the list summary, second GET fetches details for the item
    list_response = [
        {"datacenter": "datacenter-1001", "name": "dc1"},
    ]
    detail_response = {
        "datacenter": "datacenter-1001",
        "name": "dc1",
        "datastore_folder": "group-s1002",
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
    assert result["info"][0]["datacenter"] == "datacenter-1001"


def test_list_datacenters_by_datacenters_filter(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test listing datacenters filtered by datacenter IDs."""
    patch_create_client.return_value = mock_client
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module

    module_args.update(
        {
            "datacenters": ["datacenter-1001", "datacenter-1002"],
        }
    )
    mock_module.params = set_module_args(module_args)
    mock_module.exit_json.side_effect = exit_json
    mock_module.check_mode = False

    # Mock LIST response with filter
    list_response = [
        {"datacenter": "datacenter-1001", "name": "dc1"},
        {"datacenter": "datacenter-1002", "name": "dc2"},
    ]

    mock_client.get.return_value = _response(200, list_response)

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_module.exit_json.assert_called_once()
    result = exc.value.kwargs
    assert "info" in result
    assert isinstance(result["info"], list)
    # Module may make multiple GET calls to fetch details
    assert mock_client.get.called


def test_list_datacenters_with_multiple_filters(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test listing datacenters with multiple filters."""
    patch_create_client.return_value = mock_client
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module

    module_args.update(
        {
            "names": ["production-dc"],
            "folders": ["group-d1"],
        }
    )
    mock_module.params = set_module_args(module_args)
    mock_module.exit_json.side_effect = exit_json
    mock_module.check_mode = False

    # First GET returns the list summary, second GET fetches details for the item
    list_response = [
        {"datacenter": "datacenter-1001", "name": "production-dc"},
    ]
    detail_response = {
        "datacenter": "datacenter-1001",
        "name": "production-dc",
        "datastore_folder": "group-s1002",
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
    assert result["info"][0]["name"] == "production-dc"


# ============================================================================
# Test Check Mode
# ============================================================================


class TestCheckMode:
    """Test check mode behavior."""

    def test_get_check_mode(
        self, patch_create_client, patch_ansible_module, mock_client, module_args
    ):
        """Test getting a datacenter in check mode."""
        patch_create_client.return_value = mock_client
        mock_module = MagicMock()
        patch_ansible_module.return_value = mock_module

        module_args.update(
            {
                "datacenter": "datacenter-1009",
            }
        )
        mock_module.params = set_module_args(module_args)
        mock_module.exit_json.side_effect = exit_json
        mock_module.check_mode = True

        # Mock GET response
        get_response = {
            "datacenter": "datacenter-1009",
            "name": "my_datacenter",
        }

        mock_client.get.return_value = _response(200, get_response)

        with pytest.raises(AnsibleExitJson) as exc:
            module_under_test.main()

        result = exc.value.kwargs
        # Info modules execute normally in check mode (read-only)
        assert result["id"] == "datacenter-1009"
        assert "value" in result
        mock_client.get.assert_called_once()

    def test_list_check_mode(
        self, patch_create_client, patch_ansible_module, mock_client, module_args
    ):
        """Test listing datacenters in check mode."""
        patch_create_client.return_value = mock_client
        mock_module = MagicMock()
        patch_ansible_module.return_value = mock_module

        module_args.update({})
        mock_module.params = set_module_args(module_args)
        mock_module.exit_json.side_effect = exit_json
        mock_module.check_mode = True

        # First GET returns the list summary, second GET fetches details
        list_response = [
            {"datacenter": "datacenter-1001", "name": "dc1"},
        ]
        detail_response = {
            "datacenter": "datacenter-1001",
            "name": "dc1",
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
        assert module_under_test.MOID_PARAMETER_HINTS == ["datacenter"]

    def test_list_endpoint(self):
        """Test that list API endpoint is correct."""
        assert module_under_test.LIST_ENDPOINT == "/vcenter/datacenter"

    def test_item_endpoint(self):
        """Test that item API endpoint is correct."""
        assert module_under_test.ITEM_ENDPOINT == "/vcenter/datacenter/{datacenter}"


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

    def test_create_module_argument_spec_datacenters(self):
        """Test that datacenters filter parameter is correctly defined."""
        spec = module_under_test.create_module_argument_spec()

        assert "datacenters" in spec
        assert spec["datacenters"]["type"] == "list"
        assert spec["datacenters"]["elements"] == "str"

    def test_create_module_argument_spec_names(self):
        """Test that names filter parameter is correctly defined."""
        spec = module_under_test.create_module_argument_spec()

        assert "names" in spec
        assert spec["names"]["type"] == "list"
        assert spec["names"]["elements"] == "str"

    def test_create_module_argument_spec_folders(self):
        """Test that folders filter parameter is correctly defined."""
        spec = module_under_test.create_module_argument_spec()

        assert "folders" in spec
        assert spec["folders"]["type"] == "list"
        assert spec["folders"]["elements"] == "str"
