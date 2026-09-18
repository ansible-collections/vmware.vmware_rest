# -*- coding: utf-8 -*-
# Copyright: (c) 2026, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Unit tests for appliance_vmon_service_info module.

Tests validate the Info module behavior using the OperationConfig-based
architecture with mocked HTTP clients. The tests drive the module's main()
entrypoint so the real routing, argument spec, and operation configs are
exercised.

This info module reports the state of one or more vCenter appliance services
(vMon). When C(service) is supplied it GETs that single service; when it is
omitted it falls back to the list endpoint and returns every service.

The endpoints backing this module only exist in the vSphere 8.0.2 API spec
(content_generation/api_specs/8.0.2/appliance.json), which is the source of
truth for these tests. In 8.0.2 these endpoints are only published in the
legacy "/rest" form, whose bodies are wrapped in a top-level "value" key:
    GET /appliance/vmon/service          -> {"value": [{"key", "value"}]}
    GET /appliance/vmon/service/{service} -> {"value": {info}}

The base class unwraps the outer "value" for list responses (so each element is
a {"key": <service id>, "value": {info}} mapping, matching the module's RETURN
docs), but it does not unwrap single-GET responses.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import pytest
from unittest.mock import patch, MagicMock

from ansible_collections.vmware.vmware_rest.plugins.modules import (
    appliance_vmon_service_info as module_under_test,
)

from ...common.utils import (
    AnsibleExitJson,
    exit_json,
    fail_json,
    set_module_args,
    _response,
)

SERVICE_ID = "vpxd"

# A realistic service Info structure (the "value" of a list entry / the inner
# object of a single GET response).
VPXD_INFO = {
    "name_key": "cis.vpxd.ServiceName",
    "description_key": "cis.vpxd.ServiceDescription",
    "startup_type": "AUTOMATIC",
    "state": "STARTED",
    "health": "HEALTHY",
    "health_messages": [],
}
VPOSTGRES_INFO = {
    "name_key": "cis.vmware-vpostgres.ServiceName",
    "description_key": "cis.vmware-vpostgres.ServiceDescription",
    "startup_type": "AUTOMATIC",
    "state": "STARTED",
    "health": "HEALTHY",
    "health_messages": [],
}

# GET /appliance/vmon/service/{service} (8.0.2 "/rest" form, wrapped in "value").
GET_SERVICE_BODY = {"value": VPXD_INFO}

# GET /appliance/vmon/service (list_details: map of service id -> Info).
LIST_SERVICES_BODY = {
    "value": [
        {"key": "vpxd", "value": VPXD_INFO},
        {"key": "vmware-vpostgres", "value": VPOSTGRES_INFO},
    ]
}


@pytest.fixture(autouse=True)
def patch_ansible_module():
    """Automatically patch AnsibleModule for all tests."""
    with patch.object(module_under_test, "AnsibleModule") as mock:
        yield mock


@pytest.fixture(autouse=True)
def patch_create_client():
    """Automatically patch _create_client for all tests."""
    with patch.object(
        module_under_test.VmwareRestInfoModuleBase, "_create_client"
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
# Test GET a single service (service supplied)
# ============================================================================


def test_get_single_service(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test getting a single service by its identifier."""
    mock_client.get.return_value = _response(200, GET_SERVICE_BODY)

    module_args.update({"service": SERVICE_ID})
    mock_module, result = _run_module(
        patch_create_client, patch_ansible_module, mock_client, module_args
    )

    mock_module.exit_json.assert_called_once()
    # Single-GET responses are returned as-is (wrapped in "value").
    assert result["value"] == GET_SERVICE_BODY
    assert result["value"]["value"]["state"] == "STARTED"
    assert result["info"] == [GET_SERVICE_BODY]
    # The wrapped body carries no MOID attribute, so no id is reported.
    assert "id" not in result

    # The GET targets the per-service item endpoint.
    mock_client.get.assert_called_once()
    assert mock_client.get.call_args[0][0] == "/appliance/vmon/service/vpxd"


def test_get_single_service_not_found(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test getting a service that does not exist (404) yields empty results."""
    mock_client.get.return_value = _response(404, None)

    module_args.update({"service": "does-not-exist"})
    _, result = _run_module(  # pylint: disable=disallowed-name
        patch_create_client, patch_ansible_module, mock_client, module_args
    )

    assert result["info"] == []
    assert result["value"] == {}
    assert "id" not in result


# ============================================================================
# Test LIST all services (service omitted)
# ============================================================================


def test_list_all_services(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test listing every service when no identifier is supplied."""
    mock_client.get.return_value = _response(200, LIST_SERVICES_BODY)

    # No service param -> fall back to the list endpoint.
    _, result = _run_module(  # pylint: disable=disallowed-name
        patch_create_client, patch_ansible_module, mock_client, module_args
    )

    assert len(result["info"]) == 2
    assert result["info"][0]["key"] == "vpxd"
    assert result["info"][0]["value"]["state"] == "STARTED"
    assert result["info"][1]["key"] == "vmware-vpostgres"
    # For a list query, value mirrors the info list.
    assert result["value"] == result["info"]

    # The list query targets the collection endpoint.
    mock_client.get.assert_called_once()
    assert mock_client.get.call_args[0][0] == "/appliance/vmon/service"


def test_list_all_services_empty(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test listing when no services are reported."""
    mock_client.get.return_value = _response(200, {"value": []})

    _, result = _run_module(  # pylint: disable=disallowed-name
        patch_create_client, patch_ansible_module, mock_client, module_args
    )

    assert result["info"] == []
    assert result["value"] == []


# ============================================================================
# Test Check Mode (info modules always execute normally)
# ============================================================================


class TestCheckMode:
    """Test check mode behavior: read-only, so it executes normally."""

    def test_get_check_mode(
        self, patch_create_client, patch_ansible_module, mock_client, module_args
    ):
        """Test getting a single service in check mode still performs the GET."""
        mock_client.get.return_value = _response(200, GET_SERVICE_BODY)

        module_args.update({"service": SERVICE_ID})
        _, result = _run_module(  # pylint: disable=disallowed-name
            patch_create_client,
            patch_ansible_module,
            mock_client,
            module_args,
            check_mode=True,
        )

        assert result["value"] == GET_SERVICE_BODY
        mock_client.get.assert_called_once()

    def test_list_check_mode(
        self, patch_create_client, patch_ansible_module, mock_client, module_args
    ):
        """Test listing services in check mode still performs the list query."""
        mock_client.get.return_value = _response(200, LIST_SERVICES_BODY)

        _, result = _run_module(  # pylint: disable=disallowed-name
            patch_create_client,
            patch_ansible_module,
            mock_client,
            module_args,
            check_mode=True,
        )

        assert len(result["info"]) == 2
        mock_client.get.assert_called_once()


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

    def test_no_state_parameter(self):
        """Test that the info module has no state parameter."""
        spec = module_under_test.create_module_argument_spec()

        assert "state" not in spec

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
    """Test that the module's operation configs build paths correctly."""

    def test_get_operation(self):
        """Test that the GET operation targets the item endpoint."""
        config = module_under_test.GET_OPERATION

        assert config.uri == "/appliance/vmon/service/{service}"
        assert config.http_method == "get"
        assert (
            config.build_path(params={"service": SERVICE_ID})
            == "/appliance/vmon/service/vpxd"
        )

    def test_list_operation(self):
        """Test that the LIST operation targets the collection endpoint."""
        config = module_under_test.LIST_OPERATION

        assert config.uri == "/appliance/vmon/service"
        assert config.http_method == "get"
        assert config.build_path(params={}) == "/appliance/vmon/service"
