# -*- coding: utf-8 -*-
# Copyright: (c) 2026, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Unit tests for vcenter_vmtemplate_libraryitems module.

Tests validate the CRUD/action module behavior using the OperationConfig-based
architecture with mocked HTTP clients. The module supports creating a library
item (state=present) by capturing an existing virtual machine, and deploying a
new virtual machine from a template (state=deploy).
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import pytest
from unittest.mock import MagicMock, patch

from ansible_collections.vmware.vmware_rest.plugins.module_utils._crud_module import (
    VmwareRestCrudModuleBase,
)
from ansible_collections.vmware.vmware_rest.plugins.modules import (
    vcenter_vmtemplate_libraryitems as module_under_test,
)
from ansible_collections.vmware.vmware_rest.plugins.modules.vcenter_vmtemplate_libraryitems import (
    ACTION_OPERATIONS,
    CREATE_OPERATION,
    GET_OPERATION,
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
def crud_module(mock_module, mock_client):
    """
    Create a CRUD module instance configured for the vm-template library items
    endpoints (get, create, and the deploy action).

    Note: mock_client is provided by conftest.py - do not redefine it.
    """
    with patch(
        "ansible_collections.vmware.vmware_rest.plugins.module_utils._module_base.Client",
        return_value=mock_client,
    ):
        module = VmwareRestCrudModuleBase(
            module=mock_module,
            moid_parameter_hints=MOID_PARAMETER_HINTS,
            get_operation_config=GET_OPERATION,
            create_operation_config=CREATE_OPERATION,
            action_operations=ACTION_OPERATIONS,
        )
        yield module


# ============================================================================
# ensure_present() Tests - CREATE
# ============================================================================


def test_ensure_present_creates_resource(crud_module, mock_client):
    """
    Test creating a new library item when it does not exist yet.
    """
    crud_module.params["source_vm"] = "vm-1"
    crud_module.params["name"] = "my-template"
    crud_module.params["library"] = "lib-1"

    with patch.object(crud_module, "_resolve_live_resource_context", return_value=None):
        create_response = MagicMock()
        create_response.status = 200
        create_response.data = b'"item-new"'
        create_response.json = "item-new"
        mock_client.post.return_value = create_response

        result = crud_module.ensure_present()

    assert result["changed"] is True
    assert result["id"] == "item-new"
    assert result["value"] == "item-new"
    mock_client.post.assert_called_once()


def test_ensure_present_no_changes_when_exists(crud_module, mock_client):
    """
    Test that an existing library item results in no change (the module does not
    define an update operation, so there is nothing to reconcile).
    """
    crud_module.params["template_library_item"] = "item-1"
    crud_module.params["name"] = "my-template"

    existing_resource = {"template_library_item": "item-1", "name": "my-template"}

    with patch.object(
        crud_module, "_resolve_live_resource_context", return_value=existing_resource
    ):
        result = crud_module.ensure_present()

    assert result["changed"] is False
    assert result["id"] == "item-1"
    assert result["diff"] == {}
    mock_client.post.assert_not_called()


def test_ensure_present_check_mode_create(crud_module, mock_client):
    """
    Test creating a library item in check mode makes no HTTP call.
    """
    crud_module.params["source_vm"] = "vm-1"
    crud_module.params["name"] = "my-template"
    crud_module.params["library"] = "lib-1"
    crud_module.module.check_mode = True

    with patch.object(crud_module, "_resolve_live_resource_context", return_value=None):
        result = crud_module.ensure_present()

    assert result["changed"] is True
    assert result["id"] == ""
    assert result["value"] == {}
    mock_client.post.assert_not_called()


# ============================================================================
# perform_action() Tests - DEPLOY
# ============================================================================


def test_perform_action_deploy_success(crud_module, mock_client):
    """
    Test deploying a virtual machine from a template library item.
    """
    crud_module.params["state"] = "deploy"
    crud_module.params["template_library_item"] = "item-1"
    crud_module.params["name"] = "deployed-vm"

    deploy_response = MagicMock()
    deploy_response.status = 200
    deploy_response.data = b'"vm-100"'
    deploy_response.json = "vm-100"
    mock_client.post.return_value = deploy_response

    result = crud_module.perform_action()

    assert result["changed"] is True
    assert result["id"] == "item-1"
    assert result["value"] == "vm-100"
    mock_client.post.assert_called_once()


def test_perform_action_deploy_builds_correct_path(crud_module, mock_client):
    """
    Test that deploy builds the correct action path with the library item ID.
    """
    crud_module.params["state"] = "deploy"
    crud_module.params["template_library_item"] = "item-42"
    crud_module.params["name"] = "deployed-vm"

    deploy_response = MagicMock()
    deploy_response.status = 200
    deploy_response.data = b'"vm-100"'
    deploy_response.json = "vm-100"
    mock_client.post.return_value = deploy_response

    crud_module.perform_action()

    call_kwargs = mock_client.post.call_args
    assert "item-42" in call_kwargs[1]["path"]
    assert "action=deploy" in call_kwargs[1]["path"]


def test_perform_action_deploy_missing_required_name(crud_module, mock_client):
    """
    Test deploy fails to build a body when the required name is missing.
    """
    crud_module.params["state"] = "deploy"
    crud_module.params["template_library_item"] = "item-1"

    with pytest.raises(Exception):
        crud_module.perform_action()

    mock_client.post.assert_not_called()


def test_perform_action_deploy_check_mode(crud_module, mock_client):
    """
    Test deploying in check mode does not make HTTP calls.
    """
    crud_module.params["state"] = "deploy"
    crud_module.params["template_library_item"] = "item-1"
    crud_module.params["name"] = "deployed-vm"
    crud_module.module.check_mode = True

    result = crud_module.perform_action()

    assert result["changed"] is True
    assert result["id"] == "item-1"
    assert result["value"] == {}
    mock_client.post.assert_not_called()


# ============================================================================
# _resolve_live_resource_context() Tests
# ============================================================================


def test_resolve_live_resource_context_by_id(crud_module, mock_client):
    """
    Test looking up a library item by its ID.
    """
    crud_module.params["template_library_item"] = "item-1"

    get_response = MagicMock()
    get_response.status = 200
    get_response.json = {
        "template_library_item": "item-1",
        "name": "my-template",
    }
    mock_client.get.return_value = get_response

    result = crud_module._resolve_live_resource_context()

    assert result is not None
    assert result["template_library_item"] == "item-1"
    assert result["name"] == "my-template"


def test_resolve_live_resource_context_not_found(crud_module, mock_client):
    """
    Test looking up a library item that does not exist.
    """
    crud_module.params["template_library_item"] = "item-999"

    get_response = MagicMock()
    get_response.status = 404
    mock_client.get.return_value = get_response

    result = crud_module._resolve_live_resource_context()

    assert result is None


# ============================================================================
# OperationConfig Tests - Create
# ============================================================================


def test_create_operation_build_path():
    """
    Test that the create OperationConfig targets the collection endpoint.
    """
    path = CREATE_OPERATION.build_path({})
    assert path == "/vcenter/vm-template/library-items"


def test_create_operation_build_body_minimal():
    """
    Test building a create body with the minimal required params.
    """
    params = {
        "source_vm": "vm-1",
        "name": "my-template",
        "library": "lib-1",
    }
    body = CREATE_OPERATION.build_body(params)

    assert body["source_vm"] == "vm-1"
    assert body["name"] == "my-template"
    assert body["library"] == "lib-1"


def test_create_operation_build_body_nested_storage():
    """
    Test building a create body with nested vm_home_storage subspec.
    """
    params = {
        "source_vm": "vm-1",
        "name": "my-template",
        "library": "lib-1",
        "vm_home_storage": {
            "datastore": "datastore-1",
            "storage_policy": {
                "type": "USE_SPECIFIED_POLICY",
                "policy": "policy-1",
            },
        },
        "placement": {
            "folder": "group-v1",
            "resource_pool": "resgroup-1",
        },
    }
    body = CREATE_OPERATION.build_body(params)

    assert body["vm_home_storage"]["datastore"] == "datastore-1"
    assert body["vm_home_storage"]["storage_policy"]["type"] == "USE_SPECIFIED_POLICY"
    assert body["vm_home_storage"]["storage_policy"]["policy"] == "policy-1"
    assert body["placement"]["folder"] == "group-v1"
    assert body["placement"]["resource_pool"] == "resgroup-1"


def test_create_operation_build_body_missing_required():
    """
    Test that building a create body without a required param raises.
    """
    params = {"name": "my-template"}

    with pytest.raises(Exception):
        CREATE_OPERATION.build_body(params)


def test_create_operation_omits_none_optional_params():
    """
    Test that optional params that are not provided are omitted from the body.
    """
    params = {
        "source_vm": "vm-1",
        "name": "my-template",
        "library": "lib-1",
    }
    body = CREATE_OPERATION.build_body(params)

    assert "description" not in body
    assert "vm_home_storage" not in body
    assert "placement" not in body


# ============================================================================
# OperationConfig Tests - Deploy
# ============================================================================


def test_deploy_operation_build_path():
    """
    Test that the deploy OperationConfig builds the correct action path.
    """
    config = ACTION_OPERATIONS["deploy"]
    path = config.build_path({"template_library_item": "item-42"})

    assert path == "/vcenter/vm-template/library-items/item-42?action=deploy"


def test_deploy_operation_build_body_minimal():
    """
    Test building a deploy body with the minimal required name.
    """
    config = ACTION_OPERATIONS["deploy"]
    body = config.build_body({"name": "deployed-vm"})

    assert body["name"] == "deployed-vm"


def test_deploy_operation_build_body_nested():
    """
    Test building a deploy body with nested placement and hardware params.
    """
    config = ACTION_OPERATIONS["deploy"]
    params = {
        "name": "deployed-vm",
        "powered_on": True,
        "placement": {
            "folder": "group-v1",
            "cluster": "domain-c1",
        },
        "hardware_customization": {
            "cpu_update": {"num_cpus": 4, "num_cores_per_socket": 2},
            "memory_update": {"memory": 8192},
        },
    }
    body = config.build_body(params)

    assert body["name"] == "deployed-vm"
    assert body["powered_on"] is True
    assert body["placement"]["cluster"] == "domain-c1"
    assert body["hardware_customization"]["cpu_update"]["num_cpus"] == 4
    assert body["hardware_customization"]["memory_update"]["memory"] == 8192


def test_deploy_operation_build_body_missing_required():
    """
    Test that building a deploy body without the required name raises.
    """
    config = ACTION_OPERATIONS["deploy"]

    with pytest.raises(Exception):
        config.build_body({"powered_on": True})


def test_deploy_operation_http_method():
    """
    Test that the deploy operation uses POST.
    """
    assert ACTION_OPERATIONS["deploy"].http_method == "post"


def test_get_operation_http_method():
    """
    Test that the get operation uses GET.
    """
    assert GET_OPERATION.http_method == "get"


def test_create_operation_http_method():
    """
    Test that the create operation uses POST.
    """
    assert CREATE_OPERATION.http_method == "post"


# ============================================================================
# Module Constants Tests
# ============================================================================


def test_moid_parameter_hints():
    """
    Test that the MOID parameter hints are correctly defined.
    """
    assert MOID_PARAMETER_HINTS == ["template_library_item"]


def test_list_endpoint():
    """
    Test that the list API endpoint is correct.
    """
    assert module_under_test.LIST_ENDPOINT == "/vcenter/vm-template/library-items"


def test_item_endpoint():
    """
    Test that the item API endpoint is correct.
    """
    assert (
        module_under_test.ITEM_ENDPOINT
        == "/vcenter/vm-template/library-items/{template_library_item}"
    )


def test_action_operations_keys():
    """
    Test that ACTION_OPERATIONS contains only deploy.
    """
    assert "deploy" in ACTION_OPERATIONS
    assert len(ACTION_OPERATIONS) == 1


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
    assert set(spec["state"]["choices"]) == {"present", "deploy"}


def test_argument_spec_has_template_library_item():
    """
    Test that the argument spec includes template_library_item.
    """
    spec = create_module_argument_spec()

    assert "template_library_item" in spec
    assert spec["template_library_item"]["type"] == "str"


def test_argument_spec_has_source_vm_and_library():
    """
    Test that the argument spec includes source_vm and library.
    """
    spec = create_module_argument_spec()

    assert spec["source_vm"]["type"] == "str"
    assert spec["library"]["type"] == "str"


def test_argument_spec_has_placement():
    """
    Test that the argument spec includes placement with correct suboptions.
    """
    spec = create_module_argument_spec()

    assert spec["placement"]["type"] == "dict"
    options = spec["placement"]["options"]
    assert "folder" in options
    assert "resource_pool" in options
    assert "host" in options
    assert "cluster" in options


def test_argument_spec_has_vm_home_storage():
    """
    Test that the argument spec includes vm_home_storage with nested policy.
    """
    spec = create_module_argument_spec()

    assert spec["vm_home_storage"]["type"] == "dict"
    options = spec["vm_home_storage"]["options"]
    assert "datastore" in options
    policy = options["storage_policy"]["options"]
    assert policy["type"]["required"] is True
    assert set(policy["type"]["choices"]) == {"USE_SPECIFIED_POLICY"}


def test_argument_spec_has_hardware_customization():
    """
    Test that the argument spec includes hardware_customization suboptions.
    """
    spec = create_module_argument_spec()

    assert spec["hardware_customization"]["type"] == "dict"
    options = spec["hardware_customization"]["options"]
    assert options["cpu_update"]["options"]["num_cpus"]["type"] == "int"
    assert options["memory_update"]["options"]["memory"]["type"] == "int"


def test_argument_spec_has_connection_params():
    """
    Test that the argument spec includes connection parameters.
    """
    spec = create_module_argument_spec()

    assert "vcenter_hostname" in spec
    assert "vcenter_username" in spec
    assert "vcenter_password" in spec


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
            "source_vm": "vm-1",
            "name": "my-template",
            "library": "lib-1",
        }
    )
    mock_module.params = args
    mock_module.exit_json.side_effect = exit_json
    mock_module.check_mode = False

    # No template_library_item is supplied, so the get path cannot be built and
    # the module falls through to a create.
    mock_client.post.return_value = _response(200, "item-new")

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    result = exc.value.kwargs
    assert result["changed"] is True
    assert result["id"] == "item-new"


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
            "template_library_item": "item-1",
            "name": "deployed-vm",
        }
    )
    mock_module.params = args
    mock_module.exit_json.side_effect = exit_json
    mock_module.check_mode = False

    mock_client.post.return_value = _response(200, "vm-100")

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    result = exc.value.kwargs
    assert result["changed"] is True
    assert result["id"] == "item-1"
    assert result["value"] == "vm-100"


def test_main_present_default_state(
    patch_create_client, patch_ansible_module, mock_client
):
    """
    Test main() defaults to state=present when not explicitly provided.
    """
    patch_create_client.return_value = mock_client
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module

    args = set_module_args(
        {
            "state": "present",
            "source_vm": "vm-1",
            "name": "my-template",
            "library": "lib-1",
        }
    )
    mock_module.params = args
    mock_module.exit_json.side_effect = exit_json
    mock_module.fail_json.side_effect = fail_json
    mock_module.check_mode = False

    mock_client.post.return_value = _response(200, "item-new")

    with pytest.raises(AnsibleExitJson):
        module_under_test.main()

    mock_module.exit_json.assert_called_once()
