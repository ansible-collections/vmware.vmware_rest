# -*- coding: utf-8 -*-
# Copyright: (c) 2026, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Reference unit tests for vcenter_resourcepool CRUD module.

This file demonstrates the testing pattern for CRUD modules using the
new OperationConfig-based architecture. Use this as a template when
generating tests for other CRUD modules.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import pytest
from unittest.mock import MagicMock, patch

from ansible_collections.vmware.vmware_rest.plugins.module_utils._operation_configs import (
    OperationConfig,
)
from ansible_collections.vmware.vmware_rest.plugins.module_utils._crud_module import (
    VmwareRestCrudModuleBase,
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
def crud_module(mock_module, mock_client):
    """
    Create CRUD module instance with resource pool operation configs.

    This fixture demonstrates how to instantiate VmwareRestCrudModuleBase
    with the OperationConfig objects that match the actual module.
    """
    # Define operation configs matching vcenter_resourcepool module
    get_operation = OperationConfig(
        name="get",
        uri="/vcenter/resource-pool/{resource_pool}",
        http_method="GET",
    )

    list_operation = OperationConfig(
        name="list",
        uri="/vcenter/resource-pool",
        http_method="GET",
    )

    create_operation = OperationConfig(
        name="create",
        uri="/vcenter/resource-pool",
        http_method="POST",
        body_spec={
            "name": {"required": True},
            "parent": {"required": True},
            "cpu_allocation": {
                "required": False,
                "subspec": {
                    "reservation": {"required": False},
                    "expandable_reservation": {"required": False},
                    "limit": {"required": False},
                    "shares": {
                        "required": False,
                        "subspec": {
                            "level": {"required": True},
                            "shares": {"required": False},
                        },
                    },
                },
            },
            "memory_allocation": {
                "required": False,
                "subspec": {
                    "reservation": {"required": False},
                    "expandable_reservation": {"required": False},
                    "limit": {"required": False},
                    "shares": {
                        "required": False,
                        "subspec": {
                            "level": {"required": True},
                            "shares": {"required": False},
                        },
                    },
                },
            },
        },
    )

    update_operation = OperationConfig(
        name="update",
        uri="/vcenter/resource-pool/{resource_pool}",
        http_method="PATCH",
        body_spec={
            "name": {"required": False},
            "cpu_allocation": {
                "required": False,
                "subspec": {
                    "reservation": {"required": False},
                    "expandable_reservation": {"required": False},
                    "limit": {"required": False},
                    "shares": {
                        "required": False,
                        "subspec": {
                            "level": {"required": True},
                            "shares": {"required": False},
                        },
                    },
                },
            },
            "memory_allocation": {
                "required": False,
                "subspec": {
                    "reservation": {"required": False},
                    "expandable_reservation": {"required": False},
                    "limit": {"required": False},
                    "shares": {
                        "required": False,
                        "subspec": {
                            "level": {"required": True},
                            "shares": {"required": False},
                        },
                    },
                },
            },
        },
    )

    delete_operation = OperationConfig(
        name="delete",
        uri="/vcenter/resource-pool/{resource_pool}",
        http_method="DELETE",
    )

    # Patch Client to return our mock
    with patch(
        "ansible_collections.vmware.vmware_rest.plugins.module_utils._module_base.Client",
        return_value=mock_client,
    ):
        module = VmwareRestCrudModuleBase(
            module=mock_module,
            get_operation_config=get_operation,
            list_operation_config=list_operation,
            create_operation_config=create_operation,
            update_operation_config=update_operation,
            delete_operation_config=delete_operation,
            moid_parameter_hints=["resource_pool"],
        )
        yield module


# ============================================================================
# ensure_present() Tests - CREATE
# ============================================================================


def test_ensure_present_creates_resource(crud_module, mock_client):
    """
    Test creating a new resource.
    """
    crud_module.params["name"] = "new_pool"
    crud_module.params["parent"] = "parent-pool-1"

    # Resource not found, will create
    with patch.object(crud_module, "_resolve_resource_context", return_value=None):
        create_response = MagicMock()
        create_response.status = 201
        create_response.json = "pool-1"
        mock_client.post.return_value = create_response

        result = crud_module.ensure_present()

    assert result["changed"] is True
    assert result["id"] == "pool-1"
    mock_client.post.assert_called_once()


def test_ensure_present_creates_resource_with_nested_params(crud_module, mock_client):
    """
    Test creating a resource with nested parameters.
    """
    crud_module.params["name"] = "new_pool"
    crud_module.params["parent"] = "parent-pool-1"
    crud_module.params["cpu_allocation"] = {
        "reservation": 1000,
        "limit": 2000,
        "shares": {
            "level": "HIGH",
        },
    }
    crud_module.params["memory_allocation"] = {
        "reservation": 512,
        "limit": 1024,
    }

    # Resource not found, will create
    with patch.object(crud_module, "_resolve_resource_context", return_value=None):
        create_response = MagicMock()
        create_response.status = 201
        create_response.json = "pool-1"
        mock_client.post.return_value = create_response

        result = crud_module.ensure_present()

    assert result["changed"] is True
    assert result["id"] == "pool-1"

    # Verify POST was called with correct body
    mock_client.post.assert_called_once()
    call_args = mock_client.post.call_args
    body = call_args[0][1] if len(call_args[0]) > 1 else call_args[1]["json"]

    assert body["name"] == "new_pool"
    assert body["parent"] == "parent-pool-1"
    assert body["cpu_allocation"]["reservation"] == 1000
    assert body["memory_allocation"]["limit"] == 1024


# ============================================================================
# ensure_present() Tests - UPDATE
# ============================================================================


def test_ensure_present_updates_resource(crud_module, mock_client):
    """
    Test updating an existing resource when changes detected.
    """
    crud_module.params["resource_pool"] = "pool-1"
    crud_module.params["name"] = "updated_pool"

    # Resource found with different name
    existing_resource = {"resource_pool": "pool-1", "name": "old_pool"}

    with patch.object(
        crud_module, "_resolve_resource_context", return_value=existing_resource
    ):
        update_response = MagicMock()
        update_response.status = 200
        mock_client.patch.return_value = update_response

        result = crud_module.ensure_present()

    assert result["changed"] is True
    assert result["id"] == "pool-1"
    assert result["diff"] == {"name": {"before": "old_pool", "after": "updated_pool"}}
    mock_client.patch.assert_called_once()


def test_ensure_present_updates_nested_params(crud_module, mock_client):
    """
    Test updating nested resource allocation parameters.
    """
    crud_module.params["resource_pool"] = "pool-1"
    crud_module.params["name"] = "my_pool"
    crud_module.params["cpu_allocation"] = {
        "reservation": 1500,
        "limit": 2000,
    }

    # Resource found with different CPU reservation
    existing_resource = {
        "resource_pool": "pool-1",
        "name": "my_pool",
        "cpu_allocation": {
            "reservation": 1000,
            "limit": 2000,
        },
    }

    with patch.object(
        crud_module, "_resolve_resource_context", return_value=existing_resource
    ):
        update_response = MagicMock()
        update_response.status = 200
        mock_client.patch.return_value = update_response

        result = crud_module.ensure_present()

    assert result["changed"] is True
    assert result["id"] == "pool-1"
    assert "cpu_allocation" in result["diff"]
    assert result["diff"]["cpu_allocation"]["reservation"] == {
        "before": 1000,
        "after": 1500,
    }
    mock_client.patch.assert_called_once()


def test_ensure_present_no_changes(crud_module, mock_client):
    """
    Test no changes when resource already in desired state (idempotent).
    """
    crud_module.params["resource_pool"] = "pool-1"
    crud_module.params["name"] = "my_pool"
    crud_module.params["cpu_allocation"] = {
        "reservation": 1000,
        "limit": 2000,
    }

    # Resource found with same state
    existing_resource = {
        "resource_pool": "pool-1",
        "name": "my_pool",
        "cpu_allocation": {
            "reservation": 1000,
            "limit": 2000,
        },
    }

    with patch.object(
        crud_module, "_resolve_resource_context", return_value=existing_resource
    ):
        result = crud_module.ensure_present()

    assert result["changed"] is False
    assert result["id"] == "pool-1"
    mock_client.patch.assert_not_called()


# ============================================================================
# ensure_absent() Tests
# ============================================================================


def test_ensure_absent_deletes_resource(crud_module, mock_client):
    """
    Test deleting an existing resource.
    """
    crud_module.params["resource_pool"] = "pool-1"

    # Resource exists
    existing_resource = {"resource_pool": "pool-1", "name": "my_pool"}

    with patch.object(
        crud_module, "_resolve_resource_context", return_value=existing_resource
    ):
        delete_response = MagicMock()
        delete_response.status = 204
        mock_client.delete.return_value = delete_response

        result = crud_module.ensure_absent()

    assert result["changed"] is True
    mock_client.delete.assert_called_once()


def test_ensure_absent_by_name(crud_module, mock_client):
    """
    Test deleting a resource by name (requires lookup).
    """
    crud_module.params["name"] = "my_pool"
    # No resource_pool param provided

    # Search finds the resource by name
    existing_resource = {"resource_pool": "pool-1", "name": "my_pool"}

    with patch.object(
        crud_module, "_resolve_resource_context", return_value=existing_resource
    ):
        delete_response = MagicMock()
        delete_response.status = 204
        mock_client.delete.return_value = delete_response

        result = crud_module.ensure_absent()

    assert result["changed"] is True
    mock_client.delete.assert_called_once()


def test_ensure_absent_already_absent(crud_module, mock_client):
    """
    Test deleting a resource that doesn't exist (idempotent).
    """
    crud_module.params["resource_pool"] = "pool-999"

    # Resource not found
    with patch.object(crud_module, "_resolve_resource_context", return_value=None):
        result = crud_module.ensure_absent()

    assert result["changed"] is False
    mock_client.delete.assert_not_called()


# ============================================================================
# Helper Method Tests
# ============================================================================


def test_resolve_resource_context_by_id(crud_module, mock_client):
    """
    Test searching for a resource by its ID.
    """
    crud_module.params["resource_pool"] = "pool-1"

    get_response = MagicMock()
    get_response.status = 200
    get_response.json = {
        "resource_pool": "pool-1",
        "name": "my_pool",
        "cpu_allocation": {"reservation": 1000},
    }
    mock_client.get.return_value = get_response

    result = crud_module._resolve_resource_context()

    assert result is not None
    assert result["resource_pool"] == "pool-1"
    assert result["name"] == "my_pool"


def test_resolve_resource_context_by_name(crud_module, mock_client):
    """
    Test searching for a resource by name when ID not provided.
    """
    crud_module.params["name"] = "my_pool"
    # No resource_pool param

    list_response = MagicMock()
    list_response.status = 200
    list_response.json = [
        {"resource_pool": "pool-1", "name": "my_pool"},
        {"resource_pool": "pool-2", "name": "other_pool"},
    ]
    mock_client.get.return_value = list_response

    result = crud_module._resolve_resource_context()

    assert result is not None
    assert result["resource_pool"] == "pool-1"
    assert result["name"] == "my_pool"


def test_resolve_resource_context_not_found_by_id(crud_module, mock_client):
    """
    Test searching for a resource by ID that doesn't exist.
    """
    crud_module.params["resource_pool"] = "pool-999"

    get_response = MagicMock()
    get_response.status = 404
    mock_client.get.return_value = get_response

    result = crud_module._resolve_resource_context()

    assert result == {}


def test_resolve_resource_context_not_found_by_name(crud_module, mock_client):
    """
    Test searching for a resource by name that doesn't exist.
    """
    crud_module.params["name"] = "nonexistent_pool"

    list_response = MagicMock()
    list_response.status = 200
    list_response.json = [
        {"resource_pool": "pool-1", "name": "pool1"},
        {"resource_pool": "pool-2", "name": "pool2"},
    ]
    mock_client.get.return_value = list_response

    result = crud_module._resolve_resource_context()

    assert result == {}


def test_calculate_resource_diff_simple(crud_module):
    """
    Test diff calculation with simple parameters.
    """
    current = {"name": "old_name", "parent": "parent-1"}
    desired = {"name": "new_name", "parent": "parent-1"}

    diff = crud_module._calculate_resource_diff(current, desired)

    assert diff == {"name": {"before": "old_name", "after": "new_name"}}


def test_calculate_resource_diff_nested(crud_module):
    """
    Test diff calculation with nested parameters.
    """
    current = {
        "name": "pool",
        "cpu_allocation": {"reservation": 1000, "limit": 2000},
    }
    desired = {
        "name": "pool",
        "cpu_allocation": {"reservation": 1500, "limit": 2000},
    }

    diff = crud_module._calculate_resource_diff(current, desired)

    assert diff == {"cpu_allocation": {"reservation": {"before": 1000, "after": 1500}}}


def test_calculate_resource_diff_deeply_nested(crud_module):
    """
    Test diff calculation with deeply nested parameters.
    """
    current = {
        "name": "pool",
        "cpu_allocation": {
            "reservation": 1000,
            "shares": {"level": "NORMAL"},
        },
    }
    desired = {
        "name": "pool",
        "cpu_allocation": {
            "reservation": 1000,
            "shares": {"level": "HIGH"},
        },
    }

    diff = crud_module._calculate_resource_diff(current, desired)

    assert diff == {
        "cpu_allocation": {"shares": {"level": {"before": "NORMAL", "after": "HIGH"}}}
    }


def test_calculate_resource_diff_no_changes(crud_module):
    """
    Test diff calculation when no changes detected.
    """
    current = {
        "name": "pool",
        "cpu_allocation": {"reservation": 1000, "limit": 2000},
    }
    desired = {
        "name": "pool",
        "cpu_allocation": {"reservation": 1000, "limit": 2000},
    }

    diff = crud_module._calculate_resource_diff(current, desired)

    assert diff == {}


# ============================================================================
# Check Mode Tests
# ============================================================================


def test_ensure_present_check_mode_create(crud_module, mock_client):
    """
    Test creating a resource in check mode.
    """
    crud_module.params["name"] = "new_pool"
    crud_module.params["parent"] = "parent-1"
    crud_module.module.check_mode = True

    with patch.object(crud_module, "_resolve_resource_context", return_value=None):
        result = crud_module.ensure_present()

    assert result["changed"] is True
    # No actual POST should occur in check mode
    mock_client.post.assert_not_called()


def test_ensure_present_check_mode_update(crud_module, mock_client):
    """
    Test updating a resource in check mode.
    """
    crud_module.params["resource_pool"] = "pool-1"
    crud_module.params["name"] = "updated_pool"
    crud_module.module.check_mode = True

    existing_resource = {"resource_pool": "pool-1", "name": "old_pool"}

    with patch.object(
        crud_module, "_resolve_resource_context", return_value=existing_resource
    ):
        result = crud_module.ensure_present()

    assert result["changed"] is True
    assert result["diff"] == {"name": {"before": "old_pool", "after": "updated_pool"}}
    # No actual PATCH should occur in check mode
    mock_client.patch.assert_not_called()


def test_ensure_absent_check_mode(crud_module, mock_client):
    """
    Test deleting a resource in check mode.
    """
    crud_module.params["resource_pool"] = "pool-1"
    crud_module.module.check_mode = True

    existing_resource = {"resource_pool": "pool-1", "name": "my_pool"}

    with patch.object(
        crud_module, "_resolve_resource_context", return_value=existing_resource
    ):
        result = crud_module.ensure_absent()

    assert result["changed"] is True
    # No actual DELETE should occur in check mode
    mock_client.delete.assert_not_called()


# ============================================================================
# OperationConfig Tests
# ============================================================================


def test_operation_config_build_path():
    """
    Test that OperationConfig builds paths with parameters.
    """
    config = OperationConfig(
        name="get",
        uri="/vcenter/resource-pool/{resource_pool}",
        http_method="GET",
    )

    params = {"resource_pool": "pool-1"}
    path = config.build_path(params)

    assert path == "/vcenter/resource-pool/pool-1"


def test_operation_config_build_body_simple():
    """
    Test that OperationConfig builds request bodies from simple params.
    """
    config = OperationConfig(
        name="create",
        uri="/vcenter/resource-pool",
        http_method="POST",
        body_spec={
            "name": {"required": True},
            "parent": {"required": True},
        },
    )

    params = {"name": "my_pool", "parent": "parent-1"}
    body = config.build_body(params)

    assert body == {"name": "my_pool", "parent": "parent-1"}


def test_operation_config_build_body_nested():
    """
    Test that OperationConfig builds nested request bodies.
    """
    config = OperationConfig(
        name="create",
        uri="/vcenter/resource-pool",
        http_method="POST",
        body_spec={
            "name": {"required": True},
            "cpu_allocation": {
                "required": False,
                "subspec": {
                    "reservation": {"required": False},
                    "limit": {"required": False},
                },
            },
        },
    )

    params = {
        "name": "my_pool",
        "cpu_allocation": {"reservation": 1000, "limit": 2000},
    }
    body = config.build_body(params)

    assert body == {
        "name": "my_pool",
        "cpu_allocation": {"reservation": 1000, "limit": 2000},
    }


def test_operation_config_build_body_optional_params():
    """
    Test that optional params are omitted if not provided.
    """
    config = OperationConfig(
        name="create",
        uri="/vcenter/resource-pool",
        http_method="POST",
        body_spec={
            "name": {"required": True},
            "parent": {"required": True},
            "cpu_allocation": {"required": False},
        },
    )

    params = {"name": "my_pool", "parent": "parent-1"}
    # cpu_allocation not provided
    body = config.build_body(params)

    assert body == {"name": "my_pool", "parent": "parent-1"}
    assert "cpu_allocation" not in body
