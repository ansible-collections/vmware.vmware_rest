# -*- coding: utf-8 -*-
# Copyright: (c) 2026, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#
# Unit tests for vcenter_resourcepool module
# Generated from vSphere API spec 9.1.0
# Run tests: make units UNIT_TARGETS='tests/unit/plugins/modules/test_vcenter_resourcepool.py'

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import pytest
from unittest.mock import patch, MagicMock

from ansible_collections.vmware.vmware_rest.plugins.modules import (
    vcenter_resourcepool as module_under_test,
)
from ...common.utils import (
    AnsibleExitJson,
    AnsibleFailJson,
    CONNECTION_PARAMS,
    exit_json,
    fail_json,
    set_module_args,
    _response,
)


@pytest.fixture
def module_args():
    return dict(CONNECTION_PARAMS)


@patch.object(module_under_test, "AnsibleModule")
@patch.object(module_under_test.VmwareRestCrudModule, "_create_client")
def test_create_resource_pool_success(
    mock_create_client, mock_ansible_module, mock_client, module_args
):
    """Test creating a new resource pool - POST /vcenter/resource-pool returns 201 with resource ID"""
    mock_create_client.return_value = mock_client
    mock_module = MagicMock()
    mock_ansible_module.return_value = mock_module

    create_args = dict(module_args)
    create_args["state"] = "present"
    create_args["name"] = "TestPool"
    create_args["parent"] = "resgroup-1000"
    create_args["cpu_allocation"] = {
        "reservation": 1000,
        "expandable_reservation": True,
        "limit": 4000,
        "shares": {"level": "NORMAL"},
    }
    create_args["memory_allocation"] = {
        "reservation": 512,
        "expandable_reservation": True,
        "limit": 2048,
        "shares": {"level": "HIGH"},
    }
    mock_module.params = set_module_args(create_args)
    mock_module.check_mode = False
    mock_module.exit_json = exit_json
    mock_module.fail_json = fail_json

    # POST returns 201 with resource ID as a string
    mock_client.post.return_value = _response(201, "resgroup-1234")

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    result = exc.value.kwargs

    assert result["changed"] is True
    assert result["id"] == "resgroup-1234"

    # Verify POST was called with correct body
    call_args = mock_client.post.call_args
    assert call_args[0][0] == "/vcenter/resource-pool"
    post_data = call_args[1]["data"]
    assert post_data["name"] == "TestPool"
    assert post_data["parent"] == "resgroup-1000"
    assert post_data["cpu_allocation"]["reservation"] == 1000
    assert post_data["memory_allocation"]["shares"]["level"] == "HIGH"


@patch.object(module_under_test, "AnsibleModule")
@patch.object(module_under_test.VmwareRestCrudModule, "_create_client")
def test_create_resource_pool_minimal(
    mock_create_client, mock_ansible_module, mock_client, module_args
):
    """Test creating resource pool with minimal required parameters only"""
    mock_create_client.return_value = mock_client
    mock_module = MagicMock()
    mock_ansible_module.return_value = mock_module

    create_args = dict(module_args)
    create_args["state"] = "present"
    create_args["name"] = "MinimalPool"
    create_args["parent"] = "resgroup-1000"
    mock_module.params = set_module_args(create_args)
    mock_module.check_mode = False
    mock_module.exit_json = exit_json
    mock_module.fail_json = fail_json

    mock_client.post.return_value = _response(201, "resgroup-1235")

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    result = exc.value.kwargs
    assert result["changed"] is True
    assert result["id"] == "resgroup-1235"

    # Verify POST body has only required fields
    call_args = mock_client.post.call_args
    post_data = call_args[1]["data"]
    assert post_data["name"] == "MinimalPool"
    assert post_data["parent"] == "resgroup-1000"
    # cpu_allocation and memory_allocation are optional


@patch.object(module_under_test, "AnsibleModule")
@patch.object(module_under_test.VmwareRestCrudModule, "_create_client")
def test_create_resource_pool_missing_name(
    mock_create_client, mock_ansible_module, mock_client, module_args
):
    """Test creating resource pool without required 'name' parameter fails"""
    mock_create_client.return_value = mock_client
    mock_module = MagicMock()
    mock_ansible_module.return_value = mock_module
    mock_module.fail_json = fail_json

    create_args = dict(module_args)
    create_args["state"] = "present"
    create_args["parent"] = "resgroup-1000"
    # Missing 'name'
    mock_module.params = set_module_args(create_args)
    mock_module.check_mode = False

    with pytest.raises(AnsibleFailJson) as exc:
        module_under_test.main()

    assert "name" in str(exc.value.kwargs.get("msg", "")).lower()


@patch.object(module_under_test, "AnsibleModule")
@patch.object(module_under_test.VmwareRestCrudModule, "_create_client")
def test_create_resource_pool_missing_parent(
    mock_create_client, mock_ansible_module, mock_client, module_args
):
    """Test creating resource pool without required 'parent' parameter fails"""
    mock_create_client.return_value = mock_client
    mock_module = MagicMock()
    mock_ansible_module.return_value = mock_module
    mock_module.fail_json = fail_json

    create_args = dict(module_args)
    create_args["state"] = "present"
    create_args["name"] = "TestPool"
    # Missing 'parent'
    mock_module.params = set_module_args(create_args)
    mock_module.check_mode = False

    with pytest.raises(AnsibleFailJson) as exc:
        module_under_test.main()

    assert "parent" in str(exc.value.kwargs.get("msg", "")).lower()


@patch.object(module_under_test, "AnsibleModule")
@patch.object(module_under_test.VmwareRestCrudModule, "_create_client")
def test_update_resource_pool_success(
    mock_create_client, mock_ansible_module, mock_client, module_args
):
    """Test updating an existing resource pool - GET 200, PATCH 204, then GET updated state"""
    mock_create_client.return_value = mock_client
    mock_module = MagicMock()
    mock_ansible_module.return_value = mock_module

    update_args = dict(module_args)
    update_args["state"] = "present"
    update_args["resource_pool"] = "resgroup-1234"
    update_args["name"] = "RenamedPool"
    update_args["cpu_allocation"] = {"limit": 8000}
    mock_module.params = set_module_args(update_args)
    mock_module.check_mode = False
    mock_module.exit_json = exit_json
    mock_module.fail_json = fail_json

    # Current state from GET
    current_state = {
        "name": "OldName",
        "resource_pools": [],
        "cpu_allocation": {
            "reservation": 1000,
            "expandable_reservation": True,
            "limit": 4000,
            "shares": {"level": "NORMAL"},
        },
        "memory_allocation": {
            "reservation": 512,
            "expandable_reservation": True,
            "limit": -1,
            "shares": {"level": "NORMAL"},
        },
    }

    # Updated state after PATCH
    updated_state = {
        "name": "RenamedPool",
        "resource_pools": [],
        "cpu_allocation": {
            "reservation": 1000,
            "expandable_reservation": True,
            "limit": 8000,
            "shares": {"level": "NORMAL"},
        },
        "memory_allocation": {
            "reservation": 512,
            "expandable_reservation": True,
            "limit": -1,
            "shares": {"level": "NORMAL"},
        },
    }

    mock_client.get.side_effect = [
        _response(200, current_state),
        _response(200, updated_state),
    ]
    mock_client.patch.return_value = _response(204, None)

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    result = exc.value.kwargs
    assert result["changed"] is True

    # Verify PATCH was called with correct path and body
    patch_call = mock_client.patch.call_args
    assert "/vcenter/resource-pool/resgroup-1234" in patch_call[0][0]
    patch_data = patch_call[1]["data"]
    assert patch_data["name"] == "RenamedPool"
    assert patch_data["cpu_allocation"]["limit"] == 8000


@patch.object(module_under_test, "AnsibleModule")
@patch.object(module_under_test.VmwareRestCrudModule, "_create_client")
def test_update_resource_pool_no_change(
    mock_create_client, mock_ansible_module, mock_client, module_args
):
    """Test updating resource pool when current state matches desired state - no change"""
    mock_create_client.return_value = mock_client
    mock_module = MagicMock()
    mock_ansible_module.return_value = mock_module

    update_args = dict(module_args)
    update_args["state"] = "present"
    update_args["resource_pool"] = "resgroup-1234"
    update_args["name"] = "TestPool"
    mock_module.params = set_module_args(update_args)
    mock_module.check_mode = False
    mock_module.exit_json = exit_json
    mock_module.fail_json = fail_json

    current_state = {
        "name": "TestPool",
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

    mock_client.get.return_value = _response(200, current_state)

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    result = exc.value.kwargs
    assert result["changed"] is False

    # Verify PATCH was not called
    mock_client.patch.assert_not_called()


@patch.object(module_under_test, "AnsibleModule")
@patch.object(module_under_test.VmwareRestCrudModule, "_create_client")
def test_update_resource_pool_not_found_fails(
    mock_create_client, mock_ansible_module, mock_client, module_args
):
    """Test updating non-existent resource pool (GET 404) fails with error"""
    mock_create_client.return_value = mock_client
    mock_module = MagicMock()
    mock_ansible_module.return_value = mock_module

    update_args = dict(module_args)
    update_args["state"] = "present"
    update_args["resource_pool"] = "resgroup-9999"
    update_args["name"] = "NewPool"
    mock_module.params = set_module_args(update_args)
    mock_module.check_mode = False
    mock_module.exit_json = exit_json
    mock_module.fail_json = fail_json

    mock_client.get.return_value = _response(404, None)

    with pytest.raises(AnsibleFailJson) as exc:
        module_under_test.main()

    # Verify error message mentions the missing resource pool
    assert "resgroup-9999" in str(exc.value.kwargs.get("msg", ""))
    assert "not found" in str(exc.value.kwargs.get("msg", "")).lower()


@patch.object(module_under_test, "AnsibleModule")
@patch.object(module_under_test.VmwareRestCrudModule, "_create_client")
def test_delete_resource_pool_success(
    mock_create_client, mock_ansible_module, mock_client, module_args
):
    """Test deleting an existing resource pool - GET 200, DELETE returns success"""
    mock_create_client.return_value = mock_client
    mock_module = MagicMock()
    mock_ansible_module.return_value = mock_module

    delete_args = dict(module_args)
    delete_args["state"] = "absent"
    delete_args["resource_pool"] = "resgroup-1234"
    mock_module.params = set_module_args(delete_args)
    mock_module.check_mode = False
    mock_module.exit_json = exit_json
    mock_module.fail_json = fail_json

    current_state = {"name": "ToDelete", "resource_pools": []}

    mock_client.get.return_value = _response(200, current_state)
    mock_client.delete.return_value = _response(204, None)

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    result = exc.value.kwargs
    assert result["changed"] is True

    # Verify DELETE was called with correct path
    delete_call = mock_client.delete.call_args
    assert "/vcenter/resource-pool/resgroup-1234" in delete_call[0][0]


@patch.object(module_under_test, "AnsibleModule")
@patch.object(module_under_test.VmwareRestCrudModule, "_create_client")
def test_delete_resource_pool_not_found(
    mock_create_client, mock_ansible_module, mock_client, module_args
):
    """Test deleting non-existent resource pool - GET 404, no change"""
    mock_create_client.return_value = mock_client
    mock_module = MagicMock()
    mock_ansible_module.return_value = mock_module

    delete_args = dict(module_args)
    delete_args["state"] = "absent"
    delete_args["resource_pool"] = "resgroup-9999"
    mock_module.params = set_module_args(delete_args)
    mock_module.check_mode = False
    mock_module.exit_json = exit_json
    mock_module.fail_json = fail_json

    mock_client.get.return_value = _response(404, None)

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    result = exc.value.kwargs
    assert result["changed"] is False

    # Verify DELETE was not called
    mock_client.delete.assert_not_called()


@patch.object(module_under_test, "AnsibleModule")
@patch.object(module_under_test.VmwareRestCrudModule, "_create_client")
def test_delete_resource_pool_missing_id(
    mock_create_client, mock_ansible_module, mock_client, module_args
):
    """Test deleting without resource_pool parameter fails"""
    mock_create_client.return_value = mock_client
    mock_module = MagicMock()
    mock_ansible_module.return_value = mock_module
    mock_module.fail_json = fail_json

    delete_args = dict(module_args)
    delete_args["state"] = "absent"
    # Missing resource_pool
    mock_module.params = set_module_args(delete_args)
    mock_module.check_mode = False

    with pytest.raises(AnsibleFailJson) as exc:
        module_under_test.main()

    assert "resource_pool" in str(exc.value.kwargs.get("msg", "")).lower()


@patch.object(module_under_test, "AnsibleModule")
@patch.object(module_under_test.VmwareRestCrudModule, "_create_client")
def test_create_resource_pool_check_mode(
    mock_create_client, mock_ansible_module, mock_client, module_args
):
    """Test creating resource pool in check mode - no actual changes made"""
    mock_create_client.return_value = mock_client
    mock_module = MagicMock()
    mock_ansible_module.return_value = mock_module

    create_args = dict(module_args)
    create_args["state"] = "present"
    create_args["name"] = "TestPool"
    create_args["parent"] = "resgroup-1000"
    mock_module.params = set_module_args(create_args)
    mock_module.check_mode = True
    mock_module.exit_json = exit_json
    mock_module.fail_json = fail_json

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    result = exc.value.kwargs
    assert result["changed"] is True

    # Verify POST was not called in check mode
    mock_client.post.assert_not_called()


@patch.object(module_under_test, "AnsibleModule")
@patch.object(module_under_test.VmwareRestCrudModule, "_create_client")
def test_update_resource_pool_check_mode(
    mock_create_client, mock_ansible_module, mock_client, module_args
):
    """Test updating resource pool in check mode - no actual changes made"""
    mock_create_client.return_value = mock_client
    mock_module = MagicMock()
    mock_ansible_module.return_value = mock_module

    update_args = dict(module_args)
    update_args["state"] = "present"
    update_args["resource_pool"] = "resgroup-1234"
    update_args["name"] = "NewName"
    mock_module.params = set_module_args(update_args)
    mock_module.check_mode = True
    mock_module.exit_json = exit_json
    mock_module.fail_json = fail_json

    current_state = {"name": "OldName", "resource_pools": []}

    mock_client.get.return_value = _response(200, current_state)

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    result = exc.value.kwargs
    assert result["changed"] is True

    # Verify PATCH was not called in check mode
    mock_client.patch.assert_not_called()


@patch.object(module_under_test, "AnsibleModule")
@patch.object(module_under_test.VmwareRestCrudModule, "_create_client")
def test_delete_resource_pool_check_mode(
    mock_create_client, mock_ansible_module, mock_client, module_args
):
    """Test deleting resource pool in check mode - no actual changes made"""
    mock_create_client.return_value = mock_client
    mock_module = MagicMock()
    mock_ansible_module.return_value = mock_module

    delete_args = dict(module_args)
    delete_args["state"] = "absent"
    delete_args["resource_pool"] = "resgroup-1234"
    mock_module.params = set_module_args(delete_args)
    mock_module.check_mode = True
    mock_module.exit_json = exit_json
    mock_module.fail_json = fail_json

    current_state = {"name": "ToDelete", "resource_pools": []}

    mock_client.get.return_value = _response(200, current_state)

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    result = exc.value.kwargs
    assert result["changed"] is True

    # Verify DELETE was not called in check mode
    mock_client.delete.assert_not_called()
