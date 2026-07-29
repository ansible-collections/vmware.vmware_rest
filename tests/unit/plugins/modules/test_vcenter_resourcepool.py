# -*- coding: utf-8 -*-
# Copyright: (c) 2026, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import pytest
from unittest.mock import patch, MagicMock

from ansible_collections.vmware.vmware_rest.plugins.modules import (
    vcenter_resourcepool as module_under_test,
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
        module_under_test.VmwareRestCrudModuleBase, "_create_client"
    ) as mock:
        yield mock


# ============================================================================
# Test CREATE Operations
# ============================================================================


def test_create_resource_pool(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test creating a new resource pool."""
    patch_create_client.return_value = mock_client
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module

    module_args.update(
        {
            "state": "present",
            "name": "my_resource_pool",
            "parent": "resgroup-1001",
        }
    )
    mock_module.params = set_module_args(module_args)
    mock_module.exit_json.side_effect = exit_json
    mock_module.check_mode = False

    mock_client.get.return_value = _response(200, [])
    mock_client.post.return_value = _response(201, "resgroup-1009")

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_module.exit_json.assert_called_once()
    result = exc.value.kwargs
    assert result["changed"] is True
    assert result["id"] == "resgroup-1009"
    mock_client.post.assert_called_once()


def test_create_resource_pool_with_allocations(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test creating a resource pool with CPU and memory allocations."""
    patch_create_client.return_value = mock_client
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module

    module_args.update(
        {
            "state": "present",
            "name": "limited_pool",
            "parent": "resgroup-1001",
            "cpu_allocation": {
                "reservation": 2000,
                "limit": 8000,
                "expandable_reservation": False,
                "shares": {
                    "level": "CUSTOM",
                    "shares": 4000,
                },
            },
            "memory_allocation": {
                "reservation": 1024,
                "limit": 4096,
            },
        }
    )
    mock_module.params = set_module_args(module_args)
    mock_module.exit_json.side_effect = exit_json
    mock_module.check_mode = False

    mock_client.get.return_value = _response(200, [])
    mock_client.post.return_value = _response(201, "resgroup-1010")

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    result = exc.value.kwargs
    assert result["changed"] is True
    assert result["id"] == "resgroup-1010"
    mock_client.post.assert_called_once()


def test_create_resource_pool_idempotent(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test creating a resource pool that already exists (idempotent)."""
    patch_create_client.return_value = mock_client
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module

    module_args.update(
        {
            "state": "present",
            "name": "existing_pool",
            "parent": "resgroup-1001",
        }
    )
    mock_module.params = set_module_args(module_args)
    mock_module.exit_json.side_effect = exit_json
    mock_module.check_mode = False

    list_response = [
        {"resource_pool": "resgroup-1009", "name": "existing_pool"},
    ]
    current_state = {
        "name": "existing_pool",
    }

    mock_client.get.side_effect = [
        _response(200, list_response),
        _response(200, current_state),
    ]

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_module.exit_json.assert_called_once()
    result = exc.value.kwargs
    assert result["changed"] is False
    assert result["id"] == "resgroup-1009"
    mock_client.post.assert_not_called()


# ============================================================================
# Test UPDATE Operations
# ============================================================================


def test_update_resource_pool_name(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test updating a resource pool name."""
    patch_create_client.return_value = mock_client
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module

    module_args.update(
        {
            "state": "present",
            "resource_pool": "resgroup-1009",
            "name": "renamed_pool",
        }
    )
    mock_module.params = set_module_args(module_args)
    mock_module.exit_json.side_effect = exit_json
    mock_module.check_mode = False

    current_state = {
        "name": "old_pool",
    }

    mock_client.get.return_value = _response(200, current_state)
    mock_client.patch.return_value = _response(200, None)

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_module.exit_json.assert_called_once()
    result = exc.value.kwargs
    assert result["changed"] is True
    assert result["id"] == "resgroup-1009"
    assert result["diff"] == {"name": {"before": "old_pool", "after": "renamed_pool"}}
    mock_client.patch.assert_called_once()


def test_update_resource_pool_cpu_allocation(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test updating resource pool CPU allocation."""
    patch_create_client.return_value = mock_client
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module

    module_args.update(
        {
            "state": "present",
            "resource_pool": "resgroup-1009",
            "name": "my_pool",
            "cpu_allocation": {
                "reservation": 1500,
                "limit": 2000,
            },
        }
    )
    mock_module.params = set_module_args(module_args)
    mock_module.exit_json.side_effect = exit_json
    mock_module.check_mode = False

    current_state = {
        "name": "my_pool",
        "cpu_allocation": {
            "reservation": 1000,
            "limit": 2000,
        },
    }

    mock_client.get.return_value = _response(200, current_state)
    mock_client.patch.return_value = _response(200, None)

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    result = exc.value.kwargs
    assert result["changed"] is True
    assert result["id"] == "resgroup-1009"
    assert "diff" in result
    mock_client.patch.assert_called_once()


def test_update_resource_pool_no_changes(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test updating a resource pool with no changes (idempotent)."""
    patch_create_client.return_value = mock_client
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module

    module_args.update(
        {
            "state": "present",
            "resource_pool": "resgroup-1009",
            "name": "my_pool",
            "cpu_allocation": {
                "reservation": 1000,
                "limit": 2000,
            },
        }
    )
    mock_module.params = set_module_args(module_args)
    mock_module.exit_json.side_effect = exit_json
    mock_module.check_mode = False

    current_state = {
        "name": "my_pool",
        "cpu_allocation": {
            "reservation": 1000,
            "limit": 2000,
        },
    }

    mock_client.get.return_value = _response(200, current_state)

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    result = exc.value.kwargs
    assert result["changed"] is False
    assert result["id"] == "resgroup-1009"
    mock_client.patch.assert_not_called()


# ============================================================================
# Test DELETE Operations
# ============================================================================


def test_delete_resource_pool(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test deleting a resource pool."""
    patch_create_client.return_value = mock_client
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module

    module_args.update(
        {
            "state": "absent",
            "resource_pool": "resgroup-1009",
            "name": "my_pool",
        }
    )
    mock_module.params = set_module_args(module_args)
    mock_module.exit_json.side_effect = exit_json
    mock_module.check_mode = False

    current_state = {
        "name": "my_pool",
    }

    mock_client.get.return_value = _response(200, current_state)
    mock_client.delete.return_value = _response(204, None)

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_module.exit_json.assert_called_once()
    result = exc.value.kwargs
    assert result["changed"] is True
    mock_client.delete.assert_called_once()
    call_args = mock_client.delete.call_args
    assert call_args[0][0] == "/vcenter/resource-pool/resgroup-1009"


def test_delete_resource_pool_not_found(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test deleting a resource pool that doesn't exist (idempotent)."""
    patch_create_client.return_value = mock_client
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module

    module_args.update(
        {
            "state": "absent",
            "resource_pool": "resgroup-9999",
            "name": "nonexistent_pool",
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
    assert result["changed"] is False
    mock_client.delete.assert_not_called()


def test_delete_by_name(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test deleting a resource pool by name."""
    patch_create_client.return_value = mock_client
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module

    module_args.update(
        {
            "state": "absent",
            "name": "my_pool",
        }
    )
    mock_module.params = set_module_args(module_args)
    mock_module.exit_json.side_effect = exit_json
    mock_module.check_mode = False

    list_response = [
        {"resource_pool": "resgroup-1009", "name": "my_pool"},
    ]
    current_state = {
        "name": "my_pool",
    }

    mock_client.get.side_effect = [
        _response(200, list_response),
        _response(200, current_state),
    ]
    mock_client.delete.return_value = _response(204, None)

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_module.exit_json.assert_called_once()
    result = exc.value.kwargs
    assert result["changed"] is True
    mock_client.delete.assert_called_once()
    call_args = mock_client.delete.call_args
    assert call_args[0][0] == "/vcenter/resource-pool/resgroup-1009"


# ============================================================================
# Test Check Mode
# ============================================================================


class TestCheckMode:
    """Test check mode behavior."""

    def test_create_check_mode(
        self, patch_create_client, patch_ansible_module, mock_client, module_args
    ):
        """Test creating a resource pool in check mode."""
        patch_create_client.return_value = mock_client
        mock_module = MagicMock()
        patch_ansible_module.return_value = mock_module

        module_args.update(
            {
                "state": "present",
                "name": "new_pool",
                "parent": "resgroup-1001",
            }
        )
        mock_module.params = set_module_args(module_args)
        mock_module.exit_json.side_effect = exit_json
        mock_module.check_mode = True

        mock_client.get.return_value = _response(200, [])

        with pytest.raises(AnsibleExitJson) as exc:
            module_under_test.main()

        result = exc.value.kwargs
        assert result["changed"] is True
        mock_client.post.assert_not_called()

    def test_update_check_mode(
        self, patch_create_client, patch_ansible_module, mock_client, module_args
    ):
        """Test updating a resource pool in check mode."""
        patch_create_client.return_value = mock_client
        mock_module = MagicMock()
        patch_ansible_module.return_value = mock_module

        module_args.update(
            {
                "state": "present",
                "resource_pool": "resgroup-1009",
                "name": "updated_pool",
            }
        )
        mock_module.params = set_module_args(module_args)
        mock_module.exit_json.side_effect = exit_json
        mock_module.check_mode = True

        current_state = {
            "name": "old_pool",
        }

        mock_client.get.return_value = _response(200, current_state)

        with pytest.raises(AnsibleExitJson) as exc:
            module_under_test.main()

        result = exc.value.kwargs
        assert result["changed"] is True
        assert result["diff"] == {
            "name": {"before": "old_pool", "after": "updated_pool"}
        }
        mock_client.patch.assert_not_called()

    def test_delete_check_mode(
        self, patch_create_client, patch_ansible_module, mock_client, module_args
    ):
        """Test deleting a resource pool in check mode."""
        patch_create_client.return_value = mock_client
        mock_module = MagicMock()
        patch_ansible_module.return_value = mock_module

        module_args.update(
            {
                "state": "absent",
                "resource_pool": "resgroup-1009",
                "name": "my_pool",
            }
        )
        mock_module.params = set_module_args(module_args)
        mock_module.exit_json.side_effect = exit_json
        mock_module.check_mode = True

        current_state = {
            "name": "my_pool",
        }

        mock_client.get.return_value = _response(200, current_state)

        with pytest.raises(AnsibleExitJson) as exc:
            module_under_test.main()

        result = exc.value.kwargs
        assert result["changed"] is True
        mock_client.delete.assert_not_called()


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

    def test_create_module_argument_spec_state(self):
        """Test that state parameter is correctly defined."""
        spec = module_under_test.create_module_argument_spec()

        assert "state" in spec
        assert spec["state"]["type"] == "str"
        assert spec["state"]["choices"] == ["present", "absent"]
        assert spec["state"]["default"] == "present"

    def test_create_module_argument_spec_resource_pool(self):
        """Test that resource_pool parameter is correctly defined."""
        spec = module_under_test.create_module_argument_spec()

        assert "resource_pool" in spec
        assert spec["resource_pool"]["type"] == "str"

    def test_create_module_argument_spec_name(self):
        """Test that name parameter is correctly defined."""
        spec = module_under_test.create_module_argument_spec()

        assert "name" in spec
        assert spec["name"]["type"] == "str"

    def test_create_module_argument_spec_parent(self):
        """Test that parent parameter is correctly defined."""
        spec = module_under_test.create_module_argument_spec()

        assert "parent" in spec
        assert spec["parent"]["type"] == "str"

    def test_create_module_argument_spec_cpu_allocation(self):
        """Test that cpu_allocation parameter is correctly defined."""
        spec = module_under_test.create_module_argument_spec()

        assert "cpu_allocation" in spec
        assert spec["cpu_allocation"]["type"] == "dict"
        assert "options" in spec["cpu_allocation"]
        assert "reservation" in spec["cpu_allocation"]["options"]
        assert "limit" in spec["cpu_allocation"]["options"]
        assert "shares" in spec["cpu_allocation"]["options"]

    def test_create_module_argument_spec_memory_allocation(self):
        """Test that memory_allocation parameter is correctly defined."""
        spec = module_under_test.create_module_argument_spec()

        assert "memory_allocation" in spec
        assert spec["memory_allocation"]["type"] == "dict"
        assert "options" in spec["memory_allocation"]
        assert "reservation" in spec["memory_allocation"]["options"]
        assert "limit" in spec["memory_allocation"]["options"]
        assert "shares" in spec["memory_allocation"]["options"]
