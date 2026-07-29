# -*- coding: utf-8 -*-
# Copyright: (c) 2026, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import pytest
from unittest.mock import patch, MagicMock

from ansible_collections.vmware.vmware_rest.plugins.modules import (
    vcenter_resourcepool_info as module_under_test,
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


def test_get_resource_pool_by_id(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test getting a specific resource pool by ID."""
    patch_create_client.return_value = mock_client
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module

    module_args.update(
        {
            "resource_pool": "resgroup-1009",
        }
    )
    mock_module.params = set_module_args(module_args)
    mock_module.exit_json.side_effect = exit_json
    mock_module.check_mode = False

    get_response = {
        "resource_pool": "resgroup-1009",
        "name": "my_resource_pool",
        "cpu_allocation": {
            "reservation": 0,
            "expandable_reservation": True,
            "limit": -1,
            "shares": {
                "level": "NORMAL",
                "shares": 4000,
            },
        },
        "memory_allocation": {
            "reservation": 0,
            "expandable_reservation": True,
            "limit": -1,
            "shares": {
                "level": "NORMAL",
                "shares": 163840,
            },
        },
    }

    mock_client.get.return_value = _response(200, get_response)

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_module.exit_json.assert_called_once()
    result = exc.value.kwargs
    assert result["id"] == "resgroup-1009"
    assert "value" in result
    assert result["value"]["name"] == "my_resource_pool"
    assert result["value"]["cpu_allocation"]["shares"]["level"] == "NORMAL"


def test_get_resource_pool_not_found(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test getting a resource pool that doesn't exist."""
    patch_create_client.return_value = mock_client
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module

    module_args.update(
        {
            "resource_pool": "resgroup-9999",
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
    assert "info" in result
    assert len(result["info"]) == 0


# ============================================================================
# Test LIST Operations (Multiple Resources)
# ============================================================================


def test_list_all_resource_pools(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test listing all resource pools."""
    patch_create_client.return_value = mock_client
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module

    module_args.update({})
    mock_module.params = set_module_args(module_args)
    mock_module.exit_json.side_effect = exit_json
    mock_module.check_mode = False

    list_response = [
        {"resource_pool": "resgroup-1001", "name": "pool-a"},
        {"resource_pool": "resgroup-1002", "name": "pool-b"},
    ]
    detail_response_1 = {
        "resource_pool": "resgroup-1001",
        "name": "pool-a",
        "cpu_allocation": {"reservation": 0, "limit": -1},
    }
    detail_response_2 = {
        "resource_pool": "resgroup-1002",
        "name": "pool-b",
        "cpu_allocation": {"reservation": 1000, "limit": 4000},
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
    assert result["info"][0]["resource_pool"] == "resgroup-1001"
    assert result["info"][1]["resource_pool"] == "resgroup-1002"


def test_list_resource_pools_empty(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test listing resource pools when none exist."""
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


def test_list_resource_pools_by_names(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test listing resource pools filtered by names."""
    patch_create_client.return_value = mock_client
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module

    module_args.update(
        {
            "names": ["pool-a", "pool-b"],
        }
    )
    mock_module.params = set_module_args(module_args)
    mock_module.exit_json.side_effect = exit_json
    mock_module.check_mode = False

    list_response = [
        {"resource_pool": "resgroup-1001", "name": "pool-a"},
        {"resource_pool": "resgroup-1002", "name": "pool-b"},
    ]

    mock_client.get.return_value = _response(200, list_response)

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_module.exit_json.assert_called_once()
    result = exc.value.kwargs
    assert "info" in result
    assert isinstance(result["info"], list)
    assert mock_client.get.called


def test_list_resource_pools_by_clusters(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test listing resource pools filtered by clusters."""
    patch_create_client.return_value = mock_client
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module

    module_args.update(
        {
            "clusters": ["domain-c1007"],
        }
    )
    mock_module.params = set_module_args(module_args)
    mock_module.exit_json.side_effect = exit_json
    mock_module.check_mode = False

    list_response = [
        {"resource_pool": "resgroup-1001", "name": "cluster-pool"},
    ]
    detail_response = {
        "resource_pool": "resgroup-1001",
        "name": "cluster-pool",
        "cpu_allocation": {"reservation": 0, "limit": -1},
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
    assert result["info"][0]["resource_pool"] == "resgroup-1001"


def test_list_resource_pools_by_datacenters(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test listing resource pools filtered by datacenters."""
    patch_create_client.return_value = mock_client
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module

    module_args.update(
        {
            "datacenters": ["datacenter-1001"],
        }
    )
    mock_module.params = set_module_args(module_args)
    mock_module.exit_json.side_effect = exit_json
    mock_module.check_mode = False

    list_response = [
        {"resource_pool": "resgroup-1001", "name": "dc-pool"},
        {"resource_pool": "resgroup-1002", "name": "dc-pool-2"},
    ]
    detail_response_1 = {
        "resource_pool": "resgroup-1001",
        "name": "dc-pool",
    }
    detail_response_2 = {
        "resource_pool": "resgroup-1002",
        "name": "dc-pool-2",
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
    assert len(result["info"]) == 2


def test_list_resource_pools_with_multiple_filters(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test listing resource pools with multiple filters."""
    patch_create_client.return_value = mock_client
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module

    module_args.update(
        {
            "names": ["production-pool"],
            "clusters": ["domain-c1007"],
        }
    )
    mock_module.params = set_module_args(module_args)
    mock_module.exit_json.side_effect = exit_json
    mock_module.check_mode = False

    list_response = [
        {"resource_pool": "resgroup-1001", "name": "production-pool"},
    ]
    detail_response = {
        "resource_pool": "resgroup-1001",
        "name": "production-pool",
        "cpu_allocation": {"reservation": 2000, "limit": 8000},
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
    assert result["info"][0]["name"] == "production-pool"


# ============================================================================
# Test Check Mode
# ============================================================================


class TestCheckMode:
    """Test check mode behavior."""

    def test_get_check_mode(
        self, patch_create_client, patch_ansible_module, mock_client, module_args
    ):
        """Test getting a resource pool in check mode."""
        patch_create_client.return_value = mock_client
        mock_module = MagicMock()
        patch_ansible_module.return_value = mock_module

        module_args.update(
            {
                "resource_pool": "resgroup-1009",
            }
        )
        mock_module.params = set_module_args(module_args)
        mock_module.exit_json.side_effect = exit_json
        mock_module.check_mode = True

        get_response = {
            "resource_pool": "resgroup-1009",
            "name": "my_resource_pool",
        }

        mock_client.get.return_value = _response(200, get_response)

        with pytest.raises(AnsibleExitJson) as exc:
            module_under_test.main()

        result = exc.value.kwargs
        assert result["id"] == "resgroup-1009"
        assert "value" in result
        mock_client.get.assert_called_once()

    def test_list_check_mode(
        self, patch_create_client, patch_ansible_module, mock_client, module_args
    ):
        """Test listing resource pools in check mode."""
        patch_create_client.return_value = mock_client
        mock_module = MagicMock()
        patch_ansible_module.return_value = mock_module

        module_args.update({})
        mock_module.params = set_module_args(module_args)
        mock_module.exit_json.side_effect = exit_json
        mock_module.check_mode = True

        list_response = [
            {"resource_pool": "resgroup-1001", "name": "pool-a"},
        ]
        detail_response = {
            "resource_pool": "resgroup-1001",
            "name": "pool-a",
        }

        mock_client.get.side_effect = [
            _response(200, list_response),
            _response(200, detail_response),
        ]

        with pytest.raises(AnsibleExitJson) as exc:
            module_under_test.main()

        result = exc.value.kwargs
        assert "info" in result
        assert len(result["info"]) == 1


# ============================================================================
# Test Module Constants
# ============================================================================


class TestModuleConstants:
    """Test that module constants are correctly defined."""

    def test_moid_parameter_hints(self):
        """Test that MOID parameter hints are correct."""
        assert module_under_test.MOID_PARAMETER_HINTS == ["resource_pool"]

    def test_list_endpoint(self):
        """Test that list API endpoint is correct."""
        assert module_under_test.LIST_ENDPOINT == "/vcenter/resource-pool"

    def test_item_endpoint(self):
        """Test that item API endpoint is correct."""
        assert (
            module_under_test.ITEM_ENDPOINT == "/vcenter/resource-pool/{resource_pool}"
        )


# ============================================================================
# Test Argument Spec
# ============================================================================


class TestArgumentSpec:
    """Test the module argument specification."""

    def test_create_module_argument_spec_resource_pool(self):
        """Test that resource_pool parameter is correctly defined."""
        spec = module_under_test.create_module_argument_spec()

        assert "resource_pool" in spec
        assert spec["resource_pool"]["type"] == "str"

    def test_create_module_argument_spec_resource_pools(self):
        """Test that resource_pools filter parameter is correctly defined."""
        spec = module_under_test.create_module_argument_spec()

        assert "resource_pools" in spec
        assert spec["resource_pools"]["type"] == "list"
        assert spec["resource_pools"]["elements"] == "str"

    def test_create_module_argument_spec_names(self):
        """Test that names filter parameter is correctly defined."""
        spec = module_under_test.create_module_argument_spec()

        assert "names" in spec
        assert spec["names"]["type"] == "list"
        assert spec["names"]["elements"] == "str"
        assert spec["names"]["aliases"] == ["filter_names"]

    def test_create_module_argument_spec_parent_resource_pools(self):
        """Test that parent_resource_pools parameter is correctly defined."""
        spec = module_under_test.create_module_argument_spec()

        assert "parent_resource_pools" in spec
        assert spec["parent_resource_pools"]["type"] == "list"
        assert spec["parent_resource_pools"]["elements"] == "str"

    def test_create_module_argument_spec_datacenters(self):
        """Test that datacenters filter parameter is correctly defined."""
        spec = module_under_test.create_module_argument_spec()

        assert "datacenters" in spec
        assert spec["datacenters"]["type"] == "list"
        assert spec["datacenters"]["elements"] == "str"
        assert spec["datacenters"]["aliases"] == ["filter_datacenters"]

    def test_create_module_argument_spec_hosts(self):
        """Test that hosts filter parameter is correctly defined."""
        spec = module_under_test.create_module_argument_spec()

        assert "hosts" in spec
        assert spec["hosts"]["type"] == "list"
        assert spec["hosts"]["elements"] == "str"

    def test_create_module_argument_spec_clusters(self):
        """Test that clusters filter parameter is correctly defined."""
        spec = module_under_test.create_module_argument_spec()

        assert "clusters" in spec
        assert spec["clusters"]["type"] == "list"
        assert spec["clusters"]["elements"] == "str"
