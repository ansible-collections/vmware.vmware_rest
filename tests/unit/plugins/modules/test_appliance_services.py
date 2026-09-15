# -*- coding: utf-8 -*-
# Copyright: (c) 2026, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Unit tests for appliance_services module.

Tests validate the module behavior using the OperationConfig-based
architecture with mocked HTTP clients. The tests drive the module's main()
entrypoint so the real routing, argument spec, and operation configs are
exercised.

This module performs lifecycle actions on a vCenter appliance service. It is
addressed by the C(service) MOID and is intentionally non-idempotent: the
requested action is always performed. The supported actions are:
  - C(state=restart): POST /appliance/services/{service}?action=restart
  - C(state=start):   POST /appliance/services/{service}?action=start
  - C(state=stop):    POST /appliance/services/{service}?action=stop

The endpoints backing this module come from the vSphere 9.1.0 API spec
(content_generation/api_specs/9.1.0/automation/vcenter.json), which is the
source of truth for these tests. Each action is published in the modern "/api"
form where the action selector is carried as an C(?action=...) query in the URI
template, and the action responses carry no body.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import pytest
from unittest.mock import patch, MagicMock

from ansible_collections.vmware.vmware_rest.plugins.modules import (
    appliance_services as module_under_test,
)

from ...common.utils import (
    AnsibleExitJson,
    AnsibleFailJson,
    exit_json,
    fail_json,
    set_module_args,
    _response,
)

SERVICE_ID = "ntpd"


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


def _run_module(
    patch_create_client, patch_ansible_module, mock_client, args, check_mode=False
):
    """
    Configure the mocked AnsibleModule/client, run main(), and return the
    mocked module plus the kwargs passed to exit_json.
    """
    patch_create_client.return_value = mock_client
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module
    mock_module.params = set_module_args(args)
    mock_module.exit_json.side_effect = exit_json
    mock_module.fail_json.side_effect = fail_json
    mock_module.check_mode = check_mode

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    return mock_module, exc.value.kwargs


# ============================================================================
# Test state=restart / state=start / state=stop - ACTIONS
# ============================================================================


def test_action_restart(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test that state=restart POSTs to the service restart action endpoint."""
    mock_client.post.return_value = _response(200, {})

    module_args.update({"state": "restart", "service": SERVICE_ID})
    mock_module, result = _run_module(
        patch_create_client, patch_ansible_module, mock_client, module_args
    )

    mock_module.exit_json.assert_called_once()
    # The action is not idempotent; it always reports a change.
    assert result["changed"] is True
    assert result["id"] == SERVICE_ID
    mock_client.post.assert_called_once()
    call_args = mock_client.post.call_args
    assert call_args[1]["path"] == "/appliance/services/ntpd?action=restart"
    # No body or query spec is defined for the action.
    assert "data" not in call_args[1]
    assert "query" not in call_args[1]


def test_action_start(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test that state=start POSTs to the service start action endpoint."""
    mock_client.post.return_value = _response(200, {})

    module_args.update({"state": "start", "service": SERVICE_ID})
    _, result = _run_module(  # pylint: disable=disallowed-name
        patch_create_client, patch_ansible_module, mock_client, module_args
    )

    assert result["changed"] is True
    assert result["id"] == SERVICE_ID
    mock_client.post.assert_called_once()
    assert (
        mock_client.post.call_args[1]["path"] == "/appliance/services/ntpd?action=start"
    )


def test_action_stop(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test that state=stop POSTs to the service stop action endpoint."""
    mock_client.post.return_value = _response(200, {})

    module_args.update({"state": "stop", "service": SERVICE_ID})
    _, result = _run_module(  # pylint: disable=disallowed-name
        patch_create_client, patch_ansible_module, mock_client, module_args
    )

    assert result["changed"] is True
    assert result["id"] == SERVICE_ID
    assert (
        mock_client.post.call_args[1]["path"] == "/appliance/services/ntpd?action=stop"
    )


def test_action_no_content_response(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test that an empty (204) action response yields an empty value."""
    mock_client.post.return_value = _response(204, None)

    module_args.update({"state": "restart", "service": SERVICE_ID})
    _, result = _run_module(  # pylint: disable=disallowed-name
        patch_create_client, patch_ansible_module, mock_client, module_args
    )

    assert result["changed"] is True
    assert result["value"] == {}


def test_action_missing_service_fails(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """
    Test that an action without a service fails, since the action path template
    requires the service identifier and cannot be built without it.
    """
    patch_create_client.return_value = mock_client
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module
    module_args.update({"state": "restart"})
    mock_module.params = set_module_args(module_args)
    mock_module.check_mode = False
    mock_module.fail_json.side_effect = fail_json

    with pytest.raises(AnsibleFailJson):
        module_under_test.main()

    mock_client.post.assert_not_called()


# ============================================================================
# Test Check Mode
# ============================================================================


class TestCheckMode:
    """Test check mode behavior: report a change but make no write HTTP call."""

    def test_restart_check_mode(
        self, patch_create_client, patch_ansible_module, mock_client, module_args
    ):
        """Test the restart action in check mode issues no POST."""
        module_args.update({"state": "restart", "service": SERVICE_ID})
        _, result = _run_module(  # pylint: disable=disallowed-name
            patch_create_client,
            patch_ansible_module,
            mock_client,
            module_args,
            check_mode=True,
        )

        assert result["changed"] is True
        assert result["id"] == SERVICE_ID
        mock_client.post.assert_not_called()

    def test_start_check_mode(
        self, patch_create_client, patch_ansible_module, mock_client, module_args
    ):
        """Test the start action in check mode issues no POST."""
        module_args.update({"state": "start", "service": SERVICE_ID})
        _, result = _run_module(  # pylint: disable=disallowed-name
            patch_create_client,
            patch_ansible_module,
            mock_client,
            module_args,
            check_mode=True,
        )

        assert result["changed"] is True
        mock_client.post.assert_not_called()

    def test_stop_check_mode(
        self, patch_create_client, patch_ansible_module, mock_client, module_args
    ):
        """Test the stop action in check mode issues no POST."""
        module_args.update({"state": "stop", "service": SERVICE_ID})
        _, result = _run_module(  # pylint: disable=disallowed-name
            patch_create_client,
            patch_ansible_module,
            mock_client,
            module_args,
            check_mode=True,
        )

        assert result["changed"] is True
        mock_client.post.assert_not_called()


# ============================================================================
# Test Module Constants
# ============================================================================


class TestModuleConstants:
    """Test that module constants are correctly defined."""

    def test_moid_parameter_hints(self):
        """Test that the MOID parameter hint is the service identifier."""
        assert module_under_test.MOID_PARAMETER_HINTS == ["service"]

    def test_list_endpoint(self):
        """Test that the list API endpoint is correct."""
        assert module_under_test.LIST_ENDPOINT == "/appliance/services"

    def test_item_endpoint(self):
        """Test that the item API endpoint is correct."""
        assert module_under_test.ITEM_ENDPOINT == "/appliance/services/{service}"

    def test_action_operations_keys(self):
        """Test that the restart, start, and stop actions are defined."""
        assert set(module_under_test.ACTION_OPERATIONS.keys()) == {
            "restart",
            "start",
            "stop",
        }


# ============================================================================
# Test Argument Spec
# ============================================================================


class TestArgumentSpec:
    """Test the module argument specification."""

    def test_service_parameter_optional(self):
        """Test that the service parameter is an optional string."""
        spec = module_under_test.create_module_argument_spec()

        assert spec["service"]["type"] == "str"
        assert spec["service"].get("required", False) is False

    def test_state_parameter(self):
        """Test that the state parameter is a required action selector."""
        spec = module_under_test.create_module_argument_spec()

        assert spec["state"]["type"] == "str"
        assert spec["state"]["required"] is True
        assert spec["state"]["choices"] == ["restart", "start", "stop"]

    def test_has_connection_params(self):
        """Test that connection parameters are included."""
        spec = module_under_test.create_module_argument_spec()

        assert "vcenter_hostname" in spec
        assert "vcenter_username" in spec
        assert "vcenter_password" in spec


# ============================================================================
# Test OperationConfig Building
# ============================================================================


class TestOperationConfig:
    """Test that the module's operation configs build paths and bodies."""

    def test_get_operation(self):
        """Test that the GET operation targets the item endpoint."""
        assert module_under_test.GET_OPERATION.uri == "/appliance/services/{service}"
        assert module_under_test.GET_OPERATION.http_method == "get"

    def test_list_operation(self):
        """Test that the LIST operation targets the collection endpoint."""
        assert module_under_test.LIST_OPERATION.uri == "/appliance/services"
        assert module_under_test.LIST_OPERATION.http_method == "get"

    @pytest.mark.parametrize("action", ["restart", "start", "stop"])
    def test_action_operation(self, action):
        """Test that each action POSTs to the per-service action endpoint."""
        config = module_under_test.ACTION_OPERATIONS[action]

        assert config.http_method == "post"
        assert (
            config.build_path(params={"service": SERVICE_ID})
            == "/appliance/services/ntpd?action=%s" % action
        )
        # No body or query spec is defined for the action.
        assert config.build_body(params={"service": SERVICE_ID}) is None
        assert config.build_query(params={"service": SERVICE_ID}) is None
