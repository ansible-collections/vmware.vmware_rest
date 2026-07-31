# -*- coding: utf-8 -*-
# Copyright: (c) 2026, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Unit tests for vcenter_ovf_libraryitem module.

Tests validate the action-based module behavior (deploy, filter) using the
OperationConfig-based architecture with mocked HTTP clients.
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
from ansible_collections.vmware.vmware_rest.plugins.modules import (
    vcenter_ovf_libraryitem as module_under_test,
)
from ansible_collections.vmware.vmware_rest.plugins.modules.vcenter_ovf_libraryitem import (
    ACTION_OPERATIONS,
    MOID_PARAMETER_HINTS,
    create_module_argument_spec,
)

from ...common.utils import (
    AnsibleExitJson,
    CONNECTION_PARAMS,
    exit_json,
    fail_json,
    set_module_args,
    _response,
)


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
def get_operation():
    return OperationConfig(
        name="get",
        uri="/vcenter/ovf/library-item/{ovf_library_item_id}",
        http_method="GET",
    )


@pytest.fixture
def action_module(mock_module, mock_client, get_operation):
    """
    Create a CRUD module instance configured for action operations (deploy/filter).

    Note: mock_client is provided by conftest.py - do not redefine it.
    """
    with patch(
        "ansible_collections.vmware.vmware_rest.plugins.module_utils._module_base.Client",
        return_value=mock_client,
    ):
        module = VmwareRestCrudModuleBase(
            module=mock_module,
            moid_parameter_hints=MOID_PARAMETER_HINTS,
            get_operation_config=get_operation,
            action_operations=ACTION_OPERATIONS,
        )
        yield module


# ============================================================================
# perform_action() Tests - DEPLOY
# ============================================================================


def test_perform_action_deploy_success(action_module, mock_client):
    """
    Test deploying an OVF library item.
    """
    action_module.params["state"] = "deploy"
    action_module.params["ovf_library_item_id"] = "lib-item-1"
    action_module.params["target"] = {"library_id": "lib-1"}
    action_module.params["deployment_spec"] = {
        "name": "my-deployed-vm",
        "accept_all_eula": True,
        "storage_provisioning": "thin",
    }

    existing_resource = {
        "ovf_library_item_id": "lib-item-1",
        "name": "my-ovf-item",
    }

    with patch.object(
        action_module, "_resolve_resource_context", return_value=existing_resource
    ):
        deploy_response = MagicMock()
        deploy_response.status = 200
        deploy_response.data = b'{"succeeded": true}'
        deploy_response.json = {"succeeded": True}
        mock_client.post.return_value = deploy_response

        result = action_module.perform_action()

    assert result["changed"] is True
    assert result["id"] == "lib-item-1"
    assert result["value"] == {"succeeded": True}
    mock_client.post.assert_called_once()


def test_perform_action_deploy_resource_not_found(action_module, mock_client):
    """
    Test deploy fails when the library item is not found.
    """
    action_module.params["state"] = "deploy"
    action_module.params["ovf_library_item_id"] = "lib-item-999"

    with patch.object(action_module, "_resolve_resource_context", return_value=None):
        with pytest.raises(Exception):
            action_module.perform_action()

    mock_client.post.assert_not_called()


def test_perform_action_deploy_builds_correct_path(action_module, mock_client):
    """
    Test that deploy builds the correct API path with the library item ID.
    """
    action_module.params["state"] = "deploy"
    action_module.params["ovf_library_item_id"] = "lib-item-42"
    action_module.params["target"] = {"library_id": "lib-1"}
    action_module.params["deployment_spec"] = {"accept_all_eula": True}

    existing_resource = {
        "ovf_library_item_id": "lib-item-42",
        "name": "test-ovf",
    }

    with patch.object(
        action_module, "_resolve_resource_context", return_value=existing_resource
    ):
        deploy_response = MagicMock()
        deploy_response.status = 200
        deploy_response.data = b'{"succeeded": true}'
        deploy_response.json = {"succeeded": True}
        mock_client.post.return_value = deploy_response

        action_module.perform_action()

    call_kwargs = mock_client.post.call_args
    assert "lib-item-42" in call_kwargs[1]["path"]


# ============================================================================
# perform_action() Tests - FILTER
# ============================================================================


def test_perform_action_filter_success(action_module, mock_client):
    """
    Test filtering an OVF library item to get deployment information.
    """
    action_module.params["state"] = "filter"
    action_module.params["ovf_library_item_id"] = "lib-item-1"
    action_module.params["target"] = {"library_id": "lib-1"}

    existing_resource = {
        "ovf_library_item_id": "lib-item-1",
        "name": "my-ovf-item",
    }

    with patch.object(
        action_module, "_resolve_resource_context", return_value=existing_resource
    ):
        filter_response = MagicMock()
        filter_response.status = 200
        filter_response.data = b'{"name": "my-ovf-item"}'
        filter_response.json = {"name": "my-ovf-item"}
        mock_client.post.return_value = filter_response

        result = action_module.perform_action()

    assert result["changed"] is True
    assert result["id"] == "lib-item-1"
    assert result["value"] == {"name": "my-ovf-item"}
    mock_client.post.assert_called_once()


def test_perform_action_filter_resource_not_found(action_module, mock_client):
    """
    Test filter fails when the library item is not found.
    """
    action_module.params["state"] = "filter"
    action_module.params["ovf_library_item_id"] = "lib-item-999"

    with patch.object(action_module, "_resolve_resource_context", return_value=None):
        with pytest.raises(Exception):
            action_module.perform_action()

    mock_client.post.assert_not_called()


# ============================================================================
# Check Mode Tests
# ============================================================================


def test_perform_action_deploy_check_mode(action_module, mock_client):
    """
    Test deploying in check mode does not make HTTP calls.
    """
    action_module.params["state"] = "deploy"
    action_module.params["ovf_library_item_id"] = "lib-item-1"
    action_module.params["target"] = {"library_id": "lib-1"}
    action_module.params["deployment_spec"] = {"accept_all_eula": True}
    action_module.module.check_mode = True

    existing_resource = {
        "ovf_library_item_id": "lib-item-1",
        "name": "my-ovf-item",
    }

    with patch.object(
        action_module, "_resolve_resource_context", return_value=existing_resource
    ):
        result = action_module.perform_action()

    assert result["changed"] is True
    assert result["id"] == "lib-item-1"
    assert result["value"] == {}
    mock_client.post.assert_not_called()


def test_perform_action_filter_check_mode(action_module, mock_client):
    """
    Test filtering in check mode does not make HTTP calls.
    """
    action_module.params["state"] = "filter"
    action_module.params["ovf_library_item_id"] = "lib-item-1"
    action_module.params["target"] = {"library_id": "lib-1"}
    action_module.module.check_mode = True

    existing_resource = {
        "ovf_library_item_id": "lib-item-1",
        "name": "my-ovf-item",
    }

    with patch.object(
        action_module, "_resolve_resource_context", return_value=existing_resource
    ):
        result = action_module.perform_action()

    assert result["changed"] is True
    assert result["id"] == "lib-item-1"
    assert result["value"] == {}
    mock_client.post.assert_not_called()


# ============================================================================
# _resolve_resource_context() Tests
# ============================================================================


def test_resolve_resource_context_by_id(action_module, mock_client):
    """
    Test searching for a library item by its ID.
    """
    action_module.params["ovf_library_item_id"] = "lib-item-1"

    get_response = MagicMock()
    get_response.status = 200
    get_response.json = {
        "ovf_library_item_id": "lib-item-1",
        "name": "my-ovf-package",
    }
    mock_client.get.return_value = get_response

    result = action_module._resolve_resource_context()

    assert result is not None
    assert result["ovf_library_item_id"] == "lib-item-1"


def test_resolve_resource_context_not_found(action_module, mock_client):
    """
    Test searching for a library item that does not exist.
    """
    action_module.params["ovf_library_item_id"] = "lib-item-999"

    get_response = MagicMock()
    get_response.status = 404
    mock_client.get.return_value = get_response

    result = action_module._resolve_resource_context()

    assert result == {}


# ============================================================================
# OperationConfig Tests - Deploy
# ============================================================================


def test_deploy_operation_config_build_path():
    """
    Test that the deploy OperationConfig builds the correct path.
    """
    config = ACTION_OPERATIONS["deploy"]
    params = {"ovf_library_item_id": "lib-item-42"}
    path = config.build_path(params)

    assert path == "/vcenter/ovf/library-item/lib-item-42?action=deploy"


def test_deploy_operation_config_build_body_minimal():
    """
    Test building a deploy body with minimal required params.
    """
    config = ACTION_OPERATIONS["deploy"]
    params = {
        "target": {"library_id": "lib-1"},
        "deployment_spec": {"accept_all_eula": True},
    }
    body = config.build_body(params)

    assert body["target"]["library_id"] == "lib-1"
    assert body["deployment_spec"]["accept_all_eula"] is True


def test_deploy_operation_config_build_body_full():
    """
    Test building a deploy body with all parameters.
    """
    config = ACTION_OPERATIONS["deploy"]
    params = {
        "target": {
            "library_id": "lib-1",
            "library_item_id": "lib-item-1",
        },
        "deployment_spec": {
            "name": "my-vm",
            "annotation": "Test deployment",
            "accept_all_eula": True,
            "network_mappings": {"VM Network": "network-1"},
            "storage_provisioning": "thin",
            "storage_profile_id": "profile-1",
            "locale": "en_US",
            "flags": ["flag1"],
            "default_datastore_id": "ds-1",
        },
    }
    body = config.build_body(params)

    assert body["target"]["library_id"] == "lib-1"
    assert body["target"]["library_item_id"] == "lib-item-1"
    assert body["deployment_spec"]["name"] == "my-vm"
    assert body["deployment_spec"]["annotation"] == "Test deployment"
    assert body["deployment_spec"]["accept_all_eula"] is True
    assert body["deployment_spec"]["network_mappings"] == {"VM Network": "network-1"}
    assert body["deployment_spec"]["storage_provisioning"] == "thin"
    assert body["deployment_spec"]["default_datastore_id"] == "ds-1"


def test_deploy_operation_config_build_body_with_vm_config_spec():
    """
    Test building a deploy body with nested vm_config_spec.
    """
    config = ACTION_OPERATIONS["deploy"]
    params = {
        "target": {"library_id": "lib-1"},
        "deployment_spec": {
            "accept_all_eula": True,
            "vm_config_spec": {
                "provider": "XML",
                "xml": "base64-encoded-xml",
            },
        },
    }
    body = config.build_body(params)

    assert body["deployment_spec"]["vm_config_spec"]["provider"] == "XML"
    assert body["deployment_spec"]["vm_config_spec"]["xml"] == "base64-encoded-xml"


def test_deploy_operation_config_build_body_with_tag_params():
    """
    Test building a deploy body with nested tag_params.
    """
    config = ACTION_OPERATIONS["deploy"]
    params = {
        "target": {"library_id": "lib-1"},
        "deployment_spec": {
            "accept_all_eula": True,
            "tag_params": {
                "tags": [{"name": "tag1"}],
                "type": "TagConfigSpec",
            },
        },
    }
    body = config.build_body(params)

    assert body["deployment_spec"]["tag_params"]["tags"] == [{"name": "tag1"}]
    assert body["deployment_spec"]["tag_params"]["type"] == "TagConfigSpec"


def test_deploy_operation_config_omits_none_optional_params():
    """
    Test that optional parameters set to None are excluded from the body.
    """
    config = ACTION_OPERATIONS["deploy"]
    params = {
        "target": {"library_id": "lib-1"},
        "deployment_spec": {
            "accept_all_eula": True,
        },
    }
    body = config.build_body(params)

    assert "name" not in body["deployment_spec"]
    assert "annotation" not in body["deployment_spec"]
    assert "network_mappings" not in body["deployment_spec"]
    assert "storage_provisioning" not in body["deployment_spec"]


# ============================================================================
# OperationConfig Tests - Filter
# ============================================================================


def test_filter_operation_config_build_path():
    """
    Test that the filter OperationConfig builds the correct path.
    """
    config = ACTION_OPERATIONS["filter"]
    params = {"ovf_library_item_id": "lib-item-42"}
    path = config.build_path(params)

    assert path == "/vcenter/ovf/library-item/lib-item-42?action=filter"


def test_filter_operation_config_build_body():
    """
    Test building a filter body with target params.
    """
    config = ACTION_OPERATIONS["filter"]
    params = {
        "target": {
            "library_id": "lib-1",
            "library_item_id": "lib-item-1",
        },
    }
    body = config.build_body(params)

    assert body["target"]["library_id"] == "lib-1"
    assert body["target"]["library_item_id"] == "lib-item-1"


def test_filter_operation_config_build_body_minimal():
    """
    Test building a filter body with only library_id.
    """
    config = ACTION_OPERATIONS["filter"]
    params = {
        "target": {"library_id": "lib-1"},
    }
    body = config.build_body(params)

    assert body["target"]["library_id"] == "lib-1"
    assert "library_item_id" not in body["target"]


# ============================================================================
# Module Argument Spec Tests
# ============================================================================


def test_argument_spec_has_state():
    """
    Test that the argument spec has state with correct choices and default.
    """
    spec = create_module_argument_spec()

    assert "state" in spec
    assert spec["state"]["default"] == "present"
    assert set(spec["state"]["choices"]) == {"present", "deploy", "filter"}


def test_argument_spec_has_ovf_library_item_id():
    """
    Test that the argument spec includes ovf_library_item_id.
    """
    spec = create_module_argument_spec()

    assert "ovf_library_item_id" in spec
    assert spec["ovf_library_item_id"]["type"] == "str"


def test_argument_spec_has_deployment_spec():
    """
    Test that the argument spec includes deployment_spec with correct suboptions.
    """
    spec = create_module_argument_spec()

    assert "deployment_spec" in spec
    assert spec["deployment_spec"]["type"] == "dict"
    options = spec["deployment_spec"]["options"]
    assert "name" in options
    assert "accept_all_eula" in options
    assert options["accept_all_eula"]["required"] is True
    assert "network_mappings" in options
    assert "storage_provisioning" in options
    assert set(options["storage_provisioning"]["choices"]) == {
        "thin",
        "thick",
        "eagerZeroedThick",
    }


def test_argument_spec_has_target():
    """
    Test that the argument spec includes target with correct suboptions.
    """
    spec = create_module_argument_spec()

    assert "target" in spec
    assert spec["target"]["type"] == "dict"
    options = spec["target"]["options"]
    assert "library_id" in options
    assert "library_item_id" in options


def test_argument_spec_has_source():
    """
    Test that the argument spec includes source with correct suboptions.
    """
    spec = create_module_argument_spec()

    assert "source" in spec
    assert spec["source"]["type"] == "dict"
    options = spec["source"]["options"]
    assert options["type"]["required"] is True
    assert options["id"]["required"] is True


def test_argument_spec_has_create_spec():
    """
    Test that the argument spec includes create_spec with correct suboptions.
    """
    spec = create_module_argument_spec()

    assert "create_spec" in spec
    assert spec["create_spec"]["type"] == "dict"
    options = spec["create_spec"]["options"]
    assert "name" in options
    assert "description" in options
    assert "flags" in options
    assert "library_item_source_id" in options


def test_argument_spec_has_connection_params():
    """
    Test that the argument spec includes connection parameters.
    """
    spec = create_module_argument_spec()

    assert "vcenter_hostname" in spec
    assert "vcenter_username" in spec
    assert "vcenter_password" in spec


# ============================================================================
# Module Constants Tests
# ============================================================================


def test_moid_parameter_hints():
    """
    Test that the MOID parameter hints are correctly defined.
    """
    assert MOID_PARAMETER_HINTS == ["ovf_library_item_id"]


def test_action_operations_keys():
    """
    Test that ACTION_OPERATIONS contains deploy and filter.
    """
    assert "deploy" in ACTION_OPERATIONS
    assert "filter" in ACTION_OPERATIONS
    assert len(ACTION_OPERATIONS) == 2


def test_deploy_operation_http_method():
    """
    Test that the deploy operation uses POST.
    """
    assert ACTION_OPERATIONS["deploy"].http_method == "post"


def test_filter_operation_http_method():
    """
    Test that the filter operation uses POST.
    """
    assert ACTION_OPERATIONS["filter"].http_method == "post"


# ============================================================================
# main() Tests - via module entry point
# ============================================================================


@pytest.fixture
def patch_ansible_module():
    with patch.object(module_under_test, "AnsibleModule") as mock:
        yield mock


@pytest.fixture
def patch_create_client():
    with patch.object(
        module_under_test.VmwareRestCrudModuleBase, "_create_client"
    ) as mock:
        yield mock


def test_main_deploy(patch_create_client, patch_ansible_module, mock_client):
    """
    Test main() with state=deploy calls perform_action and exits.
    """
    patch_create_client.return_value = mock_client
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module

    args = set_module_args(
        {
            "state": "deploy",
            "ovf_library_item_id": "lib-item-1",
            "target": {"resource_pool_id": "resgroup-1"},
            "deployment_spec": {"accept_all_eula": True},
        }
    )
    mock_module.params = args
    mock_module.exit_json.side_effect = exit_json
    mock_module.check_mode = False

    mock_client.get.return_value = _response(
        200, {"ovf_library_item_id": "lib-item-1", "name": "test-ovf"}
    )
    mock_client.post.return_value = _response(200, {"id": "lib-item-1"})

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    result = exc.value.kwargs
    assert result["changed"] is True
    assert result["id"] == "lib-item-1"
    assert result["value"] == {"id": "lib-item-1"}


def test_main_filter(patch_create_client, patch_ansible_module, mock_client):
    """
    Test main() with state=filter calls perform_action and exits.
    """
    patch_create_client.return_value = mock_client
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module

    args = set_module_args(
        {
            "state": "filter",
            "ovf_library_item_id": "lib-item-1",
            "target": {"resource_pool_id": "resgroup-1"},
        }
    )
    mock_module.params = args
    mock_module.exit_json.side_effect = exit_json
    mock_module.check_mode = False

    mock_client.get.return_value = _response(
        200, {"ovf_library_item_id": "lib-item-1", "name": "test-ovf"}
    )
    mock_client.post.return_value = _response(200, {"id": "lib-item-1"})

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    result = exc.value.kwargs
    assert result["changed"] is True
    assert result["value"] == {"id": "lib-item-1"}


def test_main_present(patch_create_client, patch_ansible_module, mock_client):
    """
    Test main() with state=present calls ensure_present and exits.
    """
    patch_create_client.return_value = mock_client
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module

    args = set_module_args(
        {
            "state": "present",
            "source": {"type": "VirtualMachine", "id": "vm-1"},
            "target": {"resource_pool_id": "resgroup-1", "library_id": "lib-1"},
            "create_spec": {"name": "my-ovf"},
        }
    )
    mock_module.params = args
    mock_module.exit_json.side_effect = exit_json
    mock_module.check_mode = False

    mock_client.post.return_value = _response(
        200, {"value": {"ovf_library_item_id": "lib-item-new"}}
    )

    with pytest.raises(AnsibleExitJson):
        module_under_test.main()

    mock_module.exit_json.assert_called_once()
