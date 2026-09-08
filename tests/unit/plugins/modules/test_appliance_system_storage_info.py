# -*- coding: utf-8 -*-
# Copyright: (c) 2026, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import pytest
from unittest.mock import patch, MagicMock

from ansible_collections.vmware.vmware_rest.plugins.modules import (
    appliance_system_storage_info as module_under_test,
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
# Test GET Operations (Singleton returning a disk to partition mapping list)
# ============================================================================


def test_get_storage_info_multiple_partitions(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test getting the storage mapping when multiple partitions exist."""
    patch_create_client.return_value = mock_client
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module

    module_args.update({})
    mock_module.params = set_module_args(module_args)
    mock_module.exit_json.side_effect = exit_json
    mock_module.check_mode = False

    get_response = [
        {
            "disk": "1",
            "partition": "/",
            "description": {
                "default_message": "Root partition",
                "id": "com.vmware.applmgmt.storage.root",
            },
        },
        {
            "disk": "2",
            "partition": "/storage/log",
            "description": {
                "default_message": "Log partition",
                "id": "com.vmware.applmgmt.storage.log",
            },
        },
    ]

    mock_client.get.return_value = _response(200, get_response)

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_module.exit_json.assert_called_once()
    result = exc.value.kwargs
    assert "info" in result
    assert len(result["info"]) == 2
    assert result["info"][0]["disk"] == "1"
    assert result["info"][1]["partition"] == "/storage/log"
    # More than one resource, so value preserves the list shape
    assert "value" in result
    assert result["value"] == get_response


def test_get_storage_info_single_partition(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test getting the storage mapping when a single partition exists."""
    patch_create_client.return_value = mock_client
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module

    module_args.update({})
    mock_module.params = set_module_args(module_args)
    mock_module.exit_json.side_effect = exit_json
    mock_module.check_mode = False

    get_response = [
        {
            "disk": "1",
            "partition": "/",
            "description": {
                "default_message": "Root partition",
                "id": "com.vmware.applmgmt.storage.root",
            },
        },
    ]

    mock_client.get.return_value = _response(200, get_response)

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_module.exit_json.assert_called_once()
    result = exc.value.kwargs
    assert "info" in result
    assert len(result["info"]) == 1
    # Single resource, so value preserves the dict shape
    assert "value" in result
    assert result["value"]["disk"] == "1"
    assert result["value"]["partition"] == "/"


def test_get_storage_info_empty(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test getting the storage mapping when the endpoint returns an empty list."""
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
    assert result["value"] == {}


def test_get_storage_info_not_found(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test getting the storage mapping when the endpoint returns 404."""
    patch_create_client.return_value = mock_client
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module

    module_args.update({})
    mock_module.params = set_module_args(module_args)
    mock_module.exit_json.side_effect = exit_json
    mock_module.check_mode = False

    mock_client.get.return_value = _response(404, None)

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_module.exit_json.assert_called_once()
    result = exc.value.kwargs
    assert "info" in result
    assert len(result["info"]) == 0
    assert result["value"] == {}


# ============================================================================
# Test Check Mode
# ============================================================================


class TestCheckMode:
    """Test check mode behavior."""

    def test_get_check_mode(
        self, patch_create_client, patch_ansible_module, mock_client, module_args
    ):
        """Test getting storage info in check mode (read-only, still executes)."""
        patch_create_client.return_value = mock_client
        mock_module = MagicMock()
        patch_ansible_module.return_value = mock_module

        module_args.update({})
        mock_module.params = set_module_args(module_args)
        mock_module.exit_json.side_effect = exit_json
        mock_module.check_mode = True

        get_response = [
            {
                "disk": "1",
                "partition": "/",
                "description": {
                    "default_message": "Root partition",
                    "id": "com.vmware.applmgmt.storage.root",
                },
            },
        ]

        mock_client.get.return_value = _response(200, get_response)

        with pytest.raises(AnsibleExitJson) as exc:
            module_under_test.main()

        result = exc.value.kwargs
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

    def test_list_endpoint(self):
        """Test that list API endpoint is correct."""
        assert module_under_test.LIST_ENDPOINT == ""

    def test_item_endpoint(self):
        """Test that item API endpoint is correct."""
        assert module_under_test.ITEM_ENDPOINT == "/appliance/system/storage"


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


# ============================================================================
# Test OperationConfig Building
# ============================================================================


class TestOperationConfig:
    """Test that the get OperationConfig builds paths correctly."""

    def test_get_operation_build_path(self):
        """Test that the get operation builds the item endpoint path."""
        config = module_under_test.GET_OPERATION

        assert config.http_method == "get"
        assert config.build_path(params={}) == "/appliance/system/storage"

    def test_get_operation_build_query_none(self):
        """Test that the get operation has no query spec."""
        config = module_under_test.GET_OPERATION

        assert config.build_query(params={}) is None
