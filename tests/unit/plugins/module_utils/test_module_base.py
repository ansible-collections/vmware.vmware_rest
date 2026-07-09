# -*- coding: utf-8 -*-
# Copyright: (c) 2026, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from unittest.mock import MagicMock, patch

import pytest

from ansible_collections.vmware.vmware_rest.plugins.module_utils._module_base import (
    VmwareRestModuleBase,
)
from ansible_collections.vmware.vmware_rest.plugins.module_utils._operation_configs import (
    OperationConfig,
)
from ...common.utils import (  # pylint: disable=unused-import
    CONNECTION_PARAMS,
    mock_client,
)


@pytest.fixture
def mock_module():
    module = MagicMock()
    module.params = CONNECTION_PARAMS
    return module


@pytest.fixture
def base_module(mock_module, mock_client):
    list_path = "/vcenter/resource-pool"
    item_path = "/vcenter/resource-pool/{resource_pool}"

    get_operation_config = OperationConfig(
        name="get",
        uri=item_path,
        http_method="get",
    )

    list_operation_config = OperationConfig(
        name="list",
        uri=list_path,
        http_method="get",
    )

    with patch(
        "ansible_collections.vmware.vmware_rest.plugins.module_utils._module_base.Client",
        return_value=mock_client,
    ):
        module_instance = VmwareRestModuleBase(
            module=mock_module,
            moid_parameter_hints=["resource_pool"],
            get_operation_config=get_operation_config,
            list_operation_config=list_operation_config,
        )

    return module_instance


def test_module_base_initialization(base_module):
    assert base_module.list_operation_config.uri == "/vcenter/resource-pool"
    assert (
        base_module.get_operation_config.uri == "/vcenter/resource-pool/{resource_pool}"
    )
    assert "resource_pool" in base_module.moid_parameter_hints
    assert "resource_id" in base_module.moid_parameter_hints


def test_create_client(base_module, mock_module):
    assert base_module.client is not None
    assert base_module.params == mock_module.params


def test_perform_list_operation_returns_list(base_module, mock_client):
    mock_response = MagicMock()
    mock_response.status = 200
    mock_response.json = [
        {"resource_pool": "pool-1", "name": "pool_1"},
        {"resource_pool": "pool-2", "name": "pool_2"},
    ]
    mock_client.get.return_value = mock_response

    result = base_module._perform_list_operation()

    assert len(result) == 2
    assert result[0]["resource_pool"] == "pool-1"
    assert result[1]["resource_pool"] == "pool-2"


def test_perform_list_operation_returns_empty_on_404(base_module, mock_client):
    mock_response = MagicMock()
    mock_response.status = 404
    mock_client.get.return_value = mock_response

    result = base_module._perform_list_operation()

    assert result == []


def test_perform_list_operation_extracts_value_from_dict(base_module, mock_client):
    mock_response = MagicMock()
    mock_response.status = 200
    mock_response.json = {
        "value": [
            {"resource_pool": "pool-1", "name": "pool_1"},
        ]
    }
    mock_client.get.return_value = mock_response

    result = base_module._perform_list_operation()

    assert len(result) == 1
    assert result[0]["resource_pool"] == "pool-1"


def test_perform_list_operation_handles_invalid_response(base_module, mock_client):
    mock_response = MagicMock()
    mock_response.status = 200
    mock_response.json = "not a list or dict"
    mock_client.get.return_value = mock_response

    result = base_module._perform_list_operation()

    assert result == []


def test_perform_get_operation_returns_resource(base_module, mock_client):
    base_module.params["resource_pool"] = "pool-1"
    mock_response = MagicMock()
    mock_response.status = 200
    mock_response.json = {"resource_pool": "pool-1", "name": "my_pool"}
    mock_client.get.return_value = mock_response

    result = base_module._perform_get_operation()

    assert result == {"resource_pool": "pool-1", "name": "my_pool"}
    mock_client.get.assert_called_once()


def test_perform_get_operation_returns_none_on_404(base_module, mock_client):
    base_module.params["resource_pool"] = "pool-nonexistent"
    mock_response = MagicMock()
    mock_response.status = 404
    mock_client.get.return_value = mock_response

    result = base_module._perform_get_operation()

    assert result is None


def test_perform_get_operation_with_resource_dict(base_module, mock_client):
    mock_response = MagicMock()
    mock_response.status = 200
    mock_response.json = {"resource_pool": "pool-1", "name": "my_pool"}
    mock_client.get.return_value = mock_response

    resource = {"resource_pool": "pool-1"}
    result = base_module._perform_get_operation(resource=resource)

    assert result == {"resource_pool": "pool-1", "name": "my_pool"}


def test_get_moid_attribute_value_from_resource_finds_first_hint(base_module):
    resource = {"resource_pool": "pool-1", "name": "my_pool"}
    moid = base_module._get_moid_attribute_value_from_resource(resource)
    assert moid == "pool-1"


def test_get_moid_attribute_value_from_resource_tries_multiple_hints(base_module):
    resource = {"other_id": "some-id", "name": "my_pool"}
    # resource_id is in the default hints
    resource["resource_id"] = "res-123"
    moid = base_module._get_moid_attribute_value_from_resource(resource)
    assert moid == "res-123"


def test_get_moid_attribute_value_from_resource_returns_none_when_not_found(
    base_module,
):
    resource = {"name": "my_pool"}
    moid = base_module._get_moid_attribute_value_from_resource(resource)
    assert moid is None
