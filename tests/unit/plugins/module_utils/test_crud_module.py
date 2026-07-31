# -*- coding: utf-8 -*-
# Copyright: (c) 2026, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from unittest.mock import MagicMock, patch

import pytest

from ansible_collections.vmware.vmware_rest.plugins.module_utils._crud_module import (
    VmwareRestCrudModuleBase,
)
from ansible_collections.vmware.vmware_rest.plugins.module_utils._operation_configs import (
    OperationConfig,
)
from ...common.utils import (  # pylint: disable=unused-import
    AnsibleFailJson,
    CONNECTION_PARAMS,
    fail_json,
    mock_client,
)


@pytest.fixture
def mock_module():
    module = MagicMock()
    module.params = CONNECTION_PARAMS
    module.check_mode = False
    module.fail_json = fail_json
    return module


@pytest.fixture
def crud_module(mock_module, mock_client):
    get_operation_config = OperationConfig(
        name="get",
        uri="/vcenter/resource-pool/{resource_pool}",
        http_method="get",
    )

    list_operation_config = OperationConfig(
        name="list",
        uri="/vcenter/resource-pool",
        http_method="get",
    )

    create_operation_config = OperationConfig(
        name="create",
        uri="/vcenter/resource-pool",
        http_method="post",
        body_spec={
            "name": {"required": True},
            "parent": {"required": True},
        },
    )

    update_operation_config = OperationConfig(
        name="update",
        uri="/vcenter/resource-pool/{resource_pool}",
        http_method="patch",
        body_spec={
            "name": {"required": False},
            "cpu_allocation": {"required": False},
        },
    )

    delete_operation_config = OperationConfig(
        name="delete",
        uri="/vcenter/resource-pool/{resource_pool}",
        http_method="delete",
    )

    with patch(
        "ansible_collections.vmware.vmware_rest.plugins.module_utils._module_base.Client",
        return_value=mock_client,
    ):
        module_instance = VmwareRestCrudModuleBase(
            module=mock_module,
            moid_parameter_hints=["resource_pool"],
            get_operation_config=get_operation_config,
            list_operation_config=list_operation_config,
            create_operation_config=create_operation_config,
            update_operation_config=update_operation_config,
            delete_operation_config=delete_operation_config,
        )

    return module_instance


def test_crud_module_initialization(crud_module):
    assert crud_module.create_operation_config is not None
    assert crud_module.update_operation_config is not None
    assert crud_module.delete_operation_config is not None
    assert crud_module.action_operations == {}


def test_search_for_resource_by_id(crud_module, mock_client):
    crud_module.params["resource_pool"] = "pool-1"
    mock_response = MagicMock()
    mock_response.status = 200
    mock_response.json = {"resource_pool": "pool-1", "name": "my_pool"}
    mock_client.get.return_value = mock_response

    resource = crud_module._search_for_resource()

    assert resource == {
        **CONNECTION_PARAMS,
        **{"resource_pool": "pool-1", "name": "my_pool"},
    }


def test_search_for_resource_by_name(crud_module, mock_client):
    crud_module.params["name"] = "my_pool"

    # Mock detailed get response
    get_response = MagicMock()
    get_response.status = 200
    get_response.json = {
        "resource_pool": "pool-1",
        "name": "my_pool",
        "parent": "resgroup-8",
    }

    mock_client.get.return_value = get_response

    with patch.object(
        crud_module,
        "_perform_list_operation",
        return_value=[{"resource_pool": "pool-1", "name": "my_pool"}],
    ):
        resource = crud_module._search_for_resource()

    # The method returns the result from _perform_get_operation(resource=summary)
    assert resource == {
        "resource_pool": "pool-1",
        "name": "my_pool",
        "parent": "resgroup-8",
    }


def test_search_for_resource_not_found(crud_module, mock_client):
    crud_module.params["resource_pool"] = "pool-nonexistent"
    mock_response = MagicMock()
    mock_response.status = 404
    mock_client.get.return_value = mock_response

    resource = crud_module._search_for_resource()

    assert resource is None


def test_ensure_absent_already_absent(crud_module):
    with patch.object(crud_module, "_search_for_resource", return_value=None):
        result = crud_module.ensure_absent()

    assert result == {"changed": False}


def test_ensure_absent_deletes_resource(crud_module, mock_client):
    mock_resource = {"resource_pool": "pool-1", "name": "my_pool"}
    delete_response = MagicMock()
    delete_response.status = 204
    mock_client.delete.return_value = delete_response

    with patch.object(crud_module, "_search_for_resource", return_value=mock_resource):
        result = crud_module.ensure_absent()

    assert result["changed"] is True
    assert result["id"] == "pool-1"
    mock_client.delete.assert_called_once()


def test_ensure_absent_check_mode(crud_module, mock_client, mock_module):
    mock_module.check_mode = True
    mock_resource = {"resource_pool": "pool-1", "name": "my_pool"}

    with patch.object(crud_module, "_search_for_resource", return_value=mock_resource):
        result = crud_module.ensure_absent()

    assert result["changed"] is True
    assert result["id"] == "pool-1"
    mock_client.delete.assert_not_called()


def test_ensure_present_creates_resource(crud_module, mock_client):
    crud_module.params["name"] = "new_pool"
    crud_module.params["parent"] = "resgroup-8"

    create_response = MagicMock()
    create_response.status = 201
    create_response.json = "pool-new"
    mock_client.post.return_value = create_response

    with patch.object(crud_module, "_search_for_resource", return_value=None):
        result = crud_module.ensure_present()

    assert result["changed"] is True
    assert result["id"] == "pool-new"
    # diff is not included when creating a new resource
    assert "diff" not in result
    mock_client.post.assert_called_once()


def test_ensure_present_creates_resource_check_mode(
    crud_module, mock_client, mock_module
):
    mock_module.check_mode = True
    crud_module.params["name"] = "new_pool"
    crud_module.params["parent"] = "resgroup-8"

    with patch.object(crud_module, "_search_for_resource", return_value=None):
        result = crud_module.ensure_present()

    assert result["changed"] is True
    assert result["id"] == ""
    mock_client.post.assert_not_called()


def test_ensure_present_no_changes_needed(crud_module, mock_client):
    crud_module.params["resource_pool"] = "pool-1"
    crud_module.params["name"] = "my_pool"
    mock_resource = {"resource_pool": "pool-1", "name": "my_pool"}

    with patch.object(crud_module, "_search_for_resource", return_value=mock_resource):
        result = crud_module.ensure_present()

    assert result["changed"] is False
    assert result["id"] == "pool-1"
    assert result["diff"] == {}
    mock_client.patch.assert_not_called()


def test_ensure_present_updates_resource(crud_module, mock_client):
    crud_module.params["resource_pool"] = "pool-1"
    crud_module.params["name"] = "updated_pool"
    mock_resource = {"resource_pool": "pool-1", "name": "my_pool"}

    update_response = MagicMock()
    update_response.status = 200
    mock_client.patch.return_value = update_response

    with patch.object(crud_module, "_search_for_resource", return_value=mock_resource):
        result = crud_module.ensure_present()

    assert result["changed"] is True
    assert result["id"] == "pool-1"
    assert result["diff"] == {"name": {"before": "my_pool", "after": "updated_pool"}}
    mock_client.patch.assert_called_once()


def test_ensure_present_updates_resource_check_mode(
    crud_module, mock_client, mock_module
):
    mock_module.check_mode = True
    crud_module.params["resource_pool"] = "pool-1"
    crud_module.params["name"] = "updated_pool"
    mock_resource = {"resource_pool": "pool-1", "name": "my_pool"}

    with patch.object(crud_module, "_search_for_resource", return_value=mock_resource):
        result = crud_module.ensure_present()

    assert result["changed"] is True
    assert result["id"] == "pool-1"
    assert result["diff"] == {"name": {"before": "my_pool", "after": "updated_pool"}}
    mock_client.patch.assert_not_called()


def test_calculate_resource_diff_no_changes(crud_module):
    current = {"name": "my_pool", "parent": "resgroup-8"}
    desired = {"name": "my_pool"}

    diff = crud_module._calculate_resource_diff(current, desired)

    assert diff == {}


def test_calculate_resource_diff_with_changes(crud_module):
    current = {"name": "my_pool", "parent": "resgroup-8"}
    desired = {"name": "updated_pool"}

    diff = crud_module._calculate_resource_diff(current, desired)

    assert diff == {"name": {"before": "my_pool", "after": "updated_pool"}}


def test_calculate_resource_diff_ignores_none_values(crud_module):
    current = {"name": "my_pool", "parent": "resgroup-8"}
    desired = {"name": None, "parent": "resgroup-8"}

    diff = crud_module._calculate_resource_diff(current, desired)

    assert diff == {}


def test_calculate_resource_diff_nested_dict(crud_module):
    current = {"name": "my_pool", "cpu_allocation": {"reservation": 100, "limit": 500}}
    desired = {"cpu_allocation": {"reservation": 200}}

    diff = crud_module._calculate_resource_diff(current, desired)

    assert diff == {
        "cpu_allocation": {
            "before": {"reservation": 100, "limit": 500},
            "after": {"reservation": 200},
        }
    }


def test_values_equal_scalars(crud_module):
    assert crud_module._values_equal("foo", "foo") is True
    assert crud_module._values_equal("foo", "bar") is False
    assert crud_module._values_equal(100, 100) is True
    assert crud_module._values_equal(100, 200) is False


def test_values_equal_dicts(crud_module):
    current = {"a": 1, "b": 2, "c": 3}
    desired = {"a": 1, "b": 2}
    assert crud_module._values_equal(current, desired) is True

    current = {"a": 1, "b": 2}
    desired = {"a": 1, "b": 3}
    assert crud_module._values_equal(current, desired) is False


def test_values_equal_nested_dicts(crud_module):
    current = {"a": {"x": 1, "y": 2}, "b": 3}
    desired = {"a": {"x": 1}}
    assert crud_module._values_equal(current, desired) is True

    current = {"a": {"x": 1, "y": 2}, "b": 3}
    desired = {"a": {"x": 2}}
    assert crud_module._values_equal(current, desired) is False


def test_perform_action_resource_not_found(crud_module, mock_module):
    crud_module.params["state"] = "connect"
    crud_module.action_operations["connect"] = OperationConfig(
        name="connect",
        uri="/vcenter/resource-pool/{resource_pool}~action=connect",
        http_method="post",
    )

    with patch.object(crud_module, "_search_for_resource", return_value=None):
        with pytest.raises(AnsibleFailJson) as exc_info:
            crud_module.perform_action()

    assert "No matching resource was found" in exc_info.value.kwargs["msg"]


def test_perform_action_success(crud_module, mock_client):
    crud_module.params["state"] = "connect"
    crud_module.params["resource_pool"] = "pool-1"
    crud_module.action_operations["connect"] = OperationConfig(
        name="connect",
        uri="/vcenter/resource-pool/{resource_pool}~action=connect",
        http_method="post",
    )

    mock_resource = {"resource_pool": "pool-1", "name": "my_pool"}
    action_response = MagicMock()
    action_response.status = 200
    mock_client.post.return_value = action_response

    with patch.object(crud_module, "_search_for_resource", return_value=mock_resource):
        result = crud_module.perform_action()

    assert result["changed"] is True
    assert result["id"] == "pool-1"
    mock_client.post.assert_called_once()


def test_perform_action_check_mode(crud_module, mock_client, mock_module):
    mock_module.check_mode = True
    crud_module.params["state"] = "connect"
    crud_module.params["resource_pool"] = "pool-1"
    crud_module.action_operations["connect"] = OperationConfig(
        name="connect",
        uri="/vcenter/resource-pool/{resource_pool}~action=connect",
        http_method="post",
    )

    mock_resource = {"resource_pool": "pool-1", "name": "my_pool"}

    with patch.object(crud_module, "_search_for_resource", return_value=mock_resource):
        result = crud_module.perform_action()

    assert result["changed"] is True
    assert result["id"] == "pool-1"
    mock_client.post.assert_not_called()


def test_update_if_needed_no_update_config(crud_module):
    crud_module.update_operation_config = None
    resource = {"resource_pool": "pool-1", "name": "my_pool"}

    diff = crud_module._update_if_needed(resource)

    assert diff == {}
