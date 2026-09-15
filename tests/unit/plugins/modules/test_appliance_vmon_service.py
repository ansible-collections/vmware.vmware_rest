# -*- coding: utf-8 -*-
# Copyright: (c) 2026, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Unit tests for appliance_vmon_service module.

Tests validate the module behavior using the OperationConfig-based
architecture with mocked HTTP clients. The tests drive the module's main()
entrypoint so the real routing, argument spec, and operation configs are
exercised.

This module manages a vCenter appliance service (vMon). It is addressed by the
required C(service) MOID and supports:
  - C(state=start) / C(state=stop): non-idempotent POST actions against the
    per-service action endpoints.
  - C(state=present): manage the service's startup_type via a PATCH update.

The endpoints backing this module only exist in the vSphere 8.0.2 API spec
(content_generation/api_specs/8.0.2/appliance.json), which is the source of
truth for these tests. In 8.0.2 these endpoints are only published in the
legacy "/rest" form, whose bodies are wrapped in a top-level "value" key:
    GET   /appliance/vmon/service                 -> {"value": [{"key", "value"}]}
    GET   /appliance/vmon/service/{service}        -> {"value": {info}}
    PATCH /appliance/vmon/service/{service}        (update, 200 empty body)
    POST  /appliance/vmon/service/{service}/start  (action, 200 empty body)
    POST  /appliance/vmon/service/{service}/stop   (action, 200 empty body)
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import pytest
from unittest.mock import patch, MagicMock

from ansible_collections.vmware.vmware_rest.plugins.modules import (
    appliance_vmon_service as module_under_test,
)

from ...common.utils import (
    AnsibleExitJson,
    AnsibleFailJson,
    exit_json,
    fail_json,
    set_module_args,
    _response,
)

SERVICE_ID = "vpxd"

# A realistic single-service body as returned by GET
# /appliance/vmon/service/{service} in the 8.0.2 "/rest" form (wrapped in
# "value"). The base class does not unwrap single-GET responses, so this whole
# dict becomes the resolved live resource.
SERVICE_INFO = {
    "name_key": "cis.vpxd.ServiceName",
    "description_key": "cis.vpxd.ServiceDescription",
    "startup_type": "AUTOMATIC",
    "state": "STARTED",
    "health": "HEALTHY",
    "health_messages": [],
}
GET_SERVICE_BODY = {"value": SERVICE_INFO}


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
# Test state=start / state=stop - ACTIONS
# ============================================================================


def test_action_start(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test that state=start POSTs to the service start endpoint."""
    mock_client.post.return_value = _response(200, {})

    module_args.update({"state": "start", "service": SERVICE_ID})
    mock_module, result = _run_module(
        patch_create_client, patch_ansible_module, mock_client, module_args
    )

    mock_module.exit_json.assert_called_once()
    # The start action is not idempotent; it always reports a change.
    assert result["changed"] is True
    assert result["id"] == SERVICE_ID
    mock_client.post.assert_called_once()
    call_args = mock_client.post.call_args
    assert call_args[1]["path"] == "/appliance/vmon/service/vpxd/start"
    # No body or query spec is defined for the action.
    assert "data" not in call_args[1]
    assert "query" not in call_args[1]


def test_action_stop(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test that state=stop POSTs to the service stop endpoint."""
    mock_client.post.return_value = _response(200, {})

    module_args.update({"state": "stop", "service": SERVICE_ID})
    _, result = _run_module(  # pylint: disable=disallowed-name
        patch_create_client, patch_ansible_module, mock_client, module_args
    )

    assert result["changed"] is True
    assert result["id"] == SERVICE_ID
    mock_client.post.assert_called_once()
    call_args = mock_client.post.call_args
    assert call_args[1]["path"] == "/appliance/vmon/service/vpxd/stop"


def test_action_start_no_content_response(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test that an empty (204) action response yields an empty value."""
    mock_client.post.return_value = _response(204, None)

    module_args.update({"state": "start", "service": SERVICE_ID})
    _, result = _run_module(  # pylint: disable=disallowed-name
        patch_create_client, patch_ansible_module, mock_client, module_args
    )

    assert result["changed"] is True
    assert result["value"] == {}


# ============================================================================
# Test state=present - UPDATE (manage startup_type)
# ============================================================================


def test_present_updates_startup_type(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """
    Test that state=present PATCHes the service to manage its startup_type.

    The module resolves the current service state with a GET and then, when the
    update body differs, issues a PATCH to the item endpoint. The update body
    nests startup_type under request_body.
    """
    mock_client.get.return_value = _response(200, GET_SERVICE_BODY)
    mock_client.patch.return_value = _response(200, {})

    module_args.update(
        {
            "state": "present",
            "service": SERVICE_ID,
            "request_body": {"startup_type": "DISABLED"},
        }
    )
    _, result = _run_module(  # pylint: disable=disallowed-name
        patch_create_client, patch_ansible_module, mock_client, module_args
    )

    assert result["changed"] is True
    assert result["id"] == SERVICE_ID
    assert "request_body" in result["diff"]
    assert result["diff"]["request_body"]["after"] == {"startup_type": "DISABLED"}

    mock_client.patch.assert_called_once()
    call_args = mock_client.patch.call_args
    assert call_args[0][0] == "/appliance/vmon/service/vpxd"
    assert call_args[1]["data"] == {"request_body": {"startup_type": "DISABLED"}}


def test_present_requires_request_body(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """
    Test that state=present without request_body fails, since the update body
    requires request_body (and its startup_type suboption) to be provided.
    """
    patch_create_client.return_value = mock_client
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module
    module_args.update({"state": "present", "service": SERVICE_ID})
    mock_module.params = set_module_args(module_args)
    mock_module.check_mode = False
    mock_module.fail_json.side_effect = fail_json

    mock_client.get.return_value = _response(200, GET_SERVICE_BODY)

    with pytest.raises(AnsibleFailJson):
        module_under_test.main()

    mock_client.patch.assert_not_called()


def test_present_not_found_cannot_create(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """
    Test that when the service cannot be resolved and the module has no create
    operation, present fails rather than attempting a create.
    """
    patch_create_client.return_value = mock_client
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module
    module_args.update(
        {
            "state": "present",
            "service": "does-not-exist",
            "request_body": {"startup_type": "AUTOMATIC"},
        }
    )
    mock_module.params = set_module_args(module_args)
    mock_module.check_mode = False
    mock_module.fail_json.side_effect = fail_json

    mock_client.get.return_value = _response(404, None)

    with pytest.raises(AnsibleFailJson):
        module_under_test.main()

    mock_client.post.assert_not_called()
    mock_client.patch.assert_not_called()


# ============================================================================
# Test Check Mode
# ============================================================================


class TestCheckMode:
    """Test check mode behavior: report a change but make no write HTTP call."""

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
        assert result["id"] == SERVICE_ID
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

    def test_present_check_mode(
        self, patch_create_client, patch_ansible_module, mock_client, module_args
    ):
        """Test updating startup_type in check mode reports a change but issues no PATCH."""
        mock_client.get.return_value = _response(200, GET_SERVICE_BODY)

        module_args.update(
            {
                "state": "present",
                "service": SERVICE_ID,
                "request_body": {"startup_type": "DISABLED"},
            }
        )
        _, result = _run_module(  # pylint: disable=disallowed-name
            patch_create_client,
            patch_ansible_module,
            mock_client,
            module_args,
            check_mode=True,
        )

        assert result["changed"] is True
        assert "request_body" in result["diff"]
        mock_client.patch.assert_not_called()


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
        assert module_under_test.LIST_ENDPOINT == "/appliance/vmon/service"

    def test_item_endpoint(self):
        """Test that the item API endpoint is correct."""
        assert module_under_test.ITEM_ENDPOINT == "/appliance/vmon/service/{service}"

    def test_action_operations_keys(self):
        """Test that only the start and stop actions are defined."""
        assert set(module_under_test.ACTION_OPERATIONS.keys()) == {"start", "stop"}


# ============================================================================
# Test Argument Spec
# ============================================================================


class TestArgumentSpec:
    """Test the module argument specification."""

    def test_service_parameter_required(self):
        """Test that the service parameter is a required string."""
        spec = module_under_test.create_module_argument_spec()

        assert spec["service"]["type"] == "str"
        assert spec["service"]["required"] is True

    def test_state_parameter(self):
        """Test that the state parameter is correctly defined."""
        spec = module_under_test.create_module_argument_spec()

        assert spec["state"]["type"] == "str"
        assert spec["state"]["default"] == "present"
        assert spec["state"]["choices"] == ["present", "start", "stop"]

    def test_request_body_parameter(self):
        """Test that request_body is a dict with a startup_type suboption."""
        spec = module_under_test.create_module_argument_spec()

        assert spec["request_body"]["type"] == "dict"
        startup_type = spec["request_body"]["options"]["startup_type"]
        assert startup_type["type"] == "str"
        assert startup_type["choices"] == ["AUTOMATIC", "DISABLED", "MANUAL"]
        assert startup_type["required"] is True


# ============================================================================
# Test OperationConfig Building
# ============================================================================


class TestOperationConfig:
    """Test that the module's operation configs build paths and bodies."""

    def test_get_operation(self):
        """Test that the GET operation targets the item endpoint."""
        assert (
            module_under_test.GET_OPERATION.uri == "/appliance/vmon/service/{service}"
        )
        assert module_under_test.GET_OPERATION.http_method == "get"

    def test_list_operation(self):
        """Test that the LIST operation targets the collection endpoint."""
        assert module_under_test.LIST_OPERATION.uri == "/appliance/vmon/service"
        assert module_under_test.LIST_OPERATION.http_method == "get"

    def test_start_action(self):
        """Test that the start action POSTs to the per-service start endpoint."""
        config = module_under_test.ACTION_OPERATIONS["start"]

        assert config.http_method == "post"
        assert (
            config.build_path(params={"service": SERVICE_ID})
            == "/appliance/vmon/service/vpxd/start"
        )
        # No body or query spec is defined for the action.
        assert config.build_body(params={"service": SERVICE_ID}) is None
        assert config.build_query(params={"service": SERVICE_ID}) is None

    def test_stop_action(self):
        """Test that the stop action POSTs to the per-service stop endpoint."""
        config = module_under_test.ACTION_OPERATIONS["stop"]

        assert config.http_method == "post"
        assert (
            config.build_path(params={"service": SERVICE_ID})
            == "/appliance/vmon/service/vpxd/stop"
        )

    def test_update_is_patch(self):
        """Test that the update operation uses the PATCH method."""
        assert module_under_test.UPDATE_OPERATION.http_method == "patch"

    def test_update_build_path(self):
        """Test that the update operation interpolates the service into the path."""
        path = module_under_test.UPDATE_OPERATION.build_path(
            params={"service": SERVICE_ID}
        )
        assert path == "/appliance/vmon/service/vpxd"

    def test_update_build_body(self):
        """Test that the update body nests startup_type under request_body."""
        config = module_under_test.UPDATE_OPERATION

        body = config.build_body(params={"request_body": {"startup_type": "AUTOMATIC"}})
        assert body == {"request_body": {"startup_type": "AUTOMATIC"}}
