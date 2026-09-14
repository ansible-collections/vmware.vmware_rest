# -*- coding: utf-8 -*-
# Copyright: (c) 2026, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Unit tests for vcenter_vm_storage_policy_info module.

Tests validate the info module behavior using the OperationConfig-based
architecture with mocked HTTP clients.

This info module only exposes a GET operation (there is no list endpoint):
the storage policy is a per-VM singleton addressed by the ``vm`` MOID.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import pytest
from unittest.mock import MagicMock, patch

from ansible_collections.vmware.vmware_rest.plugins.module_utils._operation_configs import (
    OperationConfig,
)
from ansible_collections.vmware.vmware_rest.plugins.module_utils._info_module import (
    VmwareRestInfoModuleBase,
)
from ansible_collections.vmware.vmware_rest.plugins.module_utils._errors import (
    RequiredPathParameterError,
    VmwareModuleError,
)
from ansible_collections.vmware.vmware_rest.plugins.modules import (
    vcenter_vm_storage_policy_info as module_under_test,
)

from ...common.utils import (
    CONNECTION_PARAMS,
    AnsibleExitJson,
    AnsibleFailJson,
    exit_json,
    fail_json,
    set_module_args,
    _response,
)

ITEM_ENDPOINT = "/vcenter/vm/{vm}/storage/policy"


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
def info_module(mock_module, mock_client):
    """
    Create info module instance with vm storage policy operation configs.

    Note: mock_client is provided by conftest.py - do not redefine it.
    """
    get_operation = OperationConfig(
        name="get",
        uri=ITEM_ENDPOINT,
        http_method="GET",
    )

    with patch(
        "ansible_collections.vmware.vmware_rest.plugins.module_utils._module_base.Client",
        return_value=mock_client,
    ):
        module = VmwareRestInfoModuleBase(
            module=mock_module,
            get_operation_config=get_operation,
            moid_parameter_hints=["vm"],
        )
        yield module


# ============================================================================
# get_resource_info() Tests - GET by VM
# ============================================================================


def test_get_resource_info_by_vm(info_module, mock_client):
    """
    Test getting the storage policy for a specific VM.
    """
    info_module.params["vm"] = "vm-1"

    get_response = MagicMock()
    get_response.status = 200
    get_response.json = {
        "vm_home": {"type": "USE_DEFAULT_POLICY"},
        "disks": {"disk-1": {"type": "USE_SPECIFIED_POLICY", "policy": "policy-1"}},
    }
    mock_client.get.return_value = get_response

    result = info_module.get_resource_info()

    assert "info" in result
    assert len(result["info"]) == 1
    assert "value" in result
    assert result["value"]["vm_home"] == {"type": "USE_DEFAULT_POLICY"}
    assert result["value"]["disks"]["disk-1"]["policy"] == "policy-1"
    mock_client.get.assert_called_once_with(
        "/vcenter/vm/vm-1/storage/policy", query=None
    )


def test_get_resource_info_not_found(info_module, mock_client):
    """
    Test getting the storage policy for a VM that does not exist (404).
    """
    info_module.params["vm"] = "vm-missing"

    get_response = MagicMock()
    get_response.status = 404
    mock_client.get.return_value = get_response

    result = info_module.get_resource_info()

    assert "info" in result
    assert len(result["info"]) == 0
    assert result["value"] == {}


def test_get_resource_info_missing_vm_raises(info_module, mock_client):
    """
    Test that omitting the required vm parameter raises, since there is no
    list operation to fall back to.
    """
    # No vm param provided
    with pytest.raises(RequiredPathParameterError):
        info_module.get_resource_info()

    mock_client.get.assert_not_called()


# ============================================================================
# normalize_info_results() Tests
# ============================================================================


def test_normalize_info_results_single_resource(info_module):
    """
    Test normalize_info_results with a single resource that carries a
    recognizable MOID attribute.
    """
    resource = {
        "vm": "vm-1",
        "vm_home": {"type": "USE_DEFAULT_POLICY"},
    }

    result = info_module.normalize_info_results(
        query_results=[resource], single_resource=True
    )

    assert result["id"] == "vm-1"
    assert result["value"] == resource
    assert len(result["info"]) == 1


def test_normalize_info_results_single_resource_without_moid(info_module):
    """
    Test normalize_info_results when the resource has no MOID attribute
    (the storage policy GET response does not include the vm id).
    """
    resource = {"vm_home": {"type": "USE_DEFAULT_POLICY"}}

    result = info_module.normalize_info_results(
        query_results=[resource], single_resource=True
    )

    assert "id" not in result
    assert result["value"] == resource
    assert len(result["info"]) == 1


def test_normalize_info_results_empty(info_module):
    """
    Test normalize_info_results with an empty result set.
    """
    result = info_module.normalize_info_results(query_results=[], single_resource=True)

    assert result["info"] == []
    assert result["value"] == {}
    assert "id" not in result


# ============================================================================
# Check Mode Tests
# ============================================================================


def test_get_resource_info_check_mode(info_module, mock_client):
    """
    Test getting the storage policy in check mode still executes the read.

    Info modules are read-only, so check mode does not prevent execution.
    """
    info_module.params["vm"] = "vm-1"
    info_module.module.check_mode = True

    get_response = MagicMock()
    get_response.status = 200
    get_response.json = {"vm_home": {"type": "USE_DEFAULT_POLICY"}}
    mock_client.get.return_value = get_response

    result = info_module.get_resource_info()

    assert len(result["info"]) == 1
    mock_client.get.assert_called_once()


# ============================================================================
# _perform_get_operation() Tests
# ============================================================================


def test_perform_get_operation(info_module, mock_client):
    """
    Test the base _perform_get_operation method returns the policy dict.
    """
    info_module.params["vm"] = "vm-1"

    get_response = MagicMock()
    get_response.status = 200
    get_response.json = {"vm_home": {"type": "USE_DEFAULT_POLICY"}}
    mock_client.get.return_value = get_response

    result = info_module._perform_get_operation()

    assert result == {"vm_home": {"type": "USE_DEFAULT_POLICY"}}


def test_perform_get_operation_not_found(info_module, mock_client):
    """
    Test _perform_get_operation returns None on a 404 response.
    """
    info_module.params["vm"] = "vm-missing"

    get_response = MagicMock()
    get_response.status = 404
    mock_client.get.return_value = get_response

    result = info_module._perform_get_operation()

    assert result is None


# ============================================================================
# OperationConfig Tests
# ============================================================================


def test_operation_config_build_path():
    """
    Test that OperationConfig builds the item path from the vm parameter.
    """
    config = OperationConfig(
        name="get",
        uri=ITEM_ENDPOINT,
        http_method="GET",
    )

    path = config.build_path({"vm": "vm-1"})

    assert path == "/vcenter/vm/vm-1/storage/policy"


def test_operation_config_build_path_missing_vm_raises():
    """
    Test that building the path without the vm parameter raises.
    """
    config = OperationConfig(
        name="get",
        uri=ITEM_ENDPOINT,
        http_method="GET",
    )

    with pytest.raises(RequiredPathParameterError):
        config.build_path({})


# ============================================================================
# Argument Spec Tests
# ============================================================================


class TestArgumentSpec:
    """Test the module argument specification."""

    def test_create_module_argument_spec_has_connection_params(self):
        """Test that connection parameters are included."""
        spec = module_under_test.create_module_argument_spec()

        assert "vcenter_hostname" in spec
        assert "vcenter_username" in spec
        assert "vcenter_password" in spec

    def test_create_module_argument_spec_vm_required(self):
        """Test that the vm identifier is a required string parameter."""
        spec = module_under_test.create_module_argument_spec()

        assert spec["vm"]["type"] == "str"
        assert spec["vm"]["required"] is True

    def test_create_module_argument_spec_no_state(self):
        """Test that info module has no state parameter."""
        spec = module_under_test.create_module_argument_spec()

        assert "state" not in spec


# ============================================================================
# main() Tests - end-to-end module entrypoint
# ============================================================================


def _run_main_with_params(params, get_response=None, get_status=200):
    """
    Drive module_under_test.main() with a mocked AnsibleModule and HTTP client.

    Patches AnsibleModule and _create_client inline (rather than via fixtures) so
    these end-to-end tests do not interfere with the base-class-level fixtures
    used elsewhere in this file. Returns the exit_json kwargs.
    """
    mock_module = MagicMock()
    mock_module.params = set_module_args(params)
    mock_module.exit_json.side_effect = exit_json
    mock_module.fail_json.side_effect = fail_json
    mock_module.check_mode = False

    mock_client = MagicMock()
    if get_response is not None or get_status != 200:
        mock_client.get.return_value = _response(get_status, get_response)

    with patch.object(module_under_test, "AnsibleModule", return_value=mock_module):
        with patch.object(
            module_under_test.VmwareRestInfoModuleBase,
            "_create_client",
            return_value=mock_client,
        ):
            module_under_test.main()


def test_main_returns_policy_for_vm():
    """main() returns the storage policy for a VM on success."""
    get_response = {
        "vm_home": {"type": "USE_DEFAULT_POLICY"},
        "disks": {"disk-1": {"type": "USE_SPECIFIED_POLICY", "policy": "policy-1"}},
    }

    with pytest.raises(AnsibleExitJson) as exc:
        _run_main_with_params({"vm": "vm-1"}, get_response=get_response)

    result = exc.value.kwargs
    assert len(result["info"]) == 1
    assert result["value"]["vm_home"] == {"type": "USE_DEFAULT_POLICY"}


def test_main_returns_empty_when_not_found():
    """main() returns an empty result when the VM's policy is not found (404)."""
    with pytest.raises(AnsibleExitJson) as exc:
        _run_main_with_params({"vm": "vm-missing"}, get_status=404)

    result = exc.value.kwargs
    assert result["info"] == []
    assert result["value"] == {}


def test_main_handles_vmware_module_error():
    """main() converts a VmwareModuleError into a module failure."""
    mock_module = MagicMock()
    mock_module.params = set_module_args({"vm": "vm-1"})
    mock_module.exit_json.side_effect = exit_json
    mock_module.fail_json.side_effect = fail_json
    mock_module.check_mode = False

    with patch.object(module_under_test, "AnsibleModule", return_value=mock_module):
        with patch.object(module_under_test.VmwareRestInfoModuleBase, "_create_client"):
            with patch.object(
                module_under_test.VmwareRestInfoModuleBase,
                "get_resource_info",
                side_effect=VmwareModuleError("boom"),
            ):
                with pytest.raises(AnsibleFailJson) as exc:
                    module_under_test.main()

    assert exc.value.kwargs["msg"] == "boom"
