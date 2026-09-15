# -*- coding: utf-8 -*-
# Copyright: (c) 2026, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Unit tests for appliance_services_info module.

Tests validate the Info module behavior using the OperationConfig-based
architecture with mocked HTTP clients. The tests drive the module's main()
entrypoint so the real routing, argument spec, and operation configs are
exercised.

This info module reports the state of one or more vCenter appliance services.
When C(service) is supplied it GETs that single service; when it is omitted it
falls back to the list endpoint and returns every service.

The endpoints backing this module come from the vSphere 9.1.0 API spec
(content_generation/api_specs/9.1.0/automation/vcenter.json), which is the
source of truth for these tests. In 9.1.0 these endpoints are published in the
modern "/api" form with unwrapped bodies:
    GET /appliance/services           -> {<service id>: Info, ...}  (a map)
    GET /appliance/services/{service}  -> Info                       (a dict)
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import pytest
from unittest.mock import patch, MagicMock

from ansible_collections.vmware.vmware_rest.plugins.modules import (
    appliance_services_info as module_under_test,
)

from ...common.utils import (
    AnsibleExitJson,
    exit_json,
    fail_json,
    set_module_args,
    _response,
)

SERVICE_ID = "ntpd"

# A single Appliance.Services.Info structure as returned by
# GET /appliance/services/{service} in the modern 9.1.0 "/api" form.
NTPD_INFO = {
    "description": "NTP daemon",
    "state": "STARTED",
}
SSHD_INFO = {
    "description": "SSH daemon",
    "state": "STOPPED",
}

# GET /appliance/services (9.1.0 map keyed by service identifier).
LIST_SERVICES_BODY = {
    "ntpd": NTPD_INFO,
    "sshd": SSHD_INFO,
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
    mock_client.get.return_value = _response(200, NTPD_INFO)

    module_args.update({"service": SERVICE_ID})
    mock_module, result = _run_module(
        patch_create_client, patch_ansible_module, mock_client, module_args
    )

    mock_module.exit_json.assert_called_once()
    # A single-GET response is returned as-is under "value".
    assert result["value"] == NTPD_INFO
    assert result["value"]["state"] == "STARTED"
    assert result["info"] == [NTPD_INFO]
    # The Info body carries no MOID attribute, so no id is reported.
    assert "id" not in result

    # The GET targets the per-service item endpoint.
    mock_client.get.assert_called_once()
    assert mock_client.get.call_args[0][0] == "/appliance/services/ntpd"


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


def test_list_all_services_returns_empty(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """
    Test listing every service when no identifier is supplied.

    The 9.1.0 collection endpoint returns a map keyed by service identifier.
    The shared base class does not transform a map into a list (it only handles
    a bare array or a "value"-wrapped array), so the module currently returns
    empty results for the list case. This test documents that behavior.
    """
    mock_client.get.return_value = _response(200, LIST_SERVICES_BODY)

    # No service param -> fall back to the list endpoint.
    _, result = _run_module(  # pylint: disable=disallowed-name
        patch_create_client, patch_ansible_module, mock_client, module_args
    )

    assert result["info"] == []
    assert result["value"] == []

    # The list query targets the collection endpoint.
    mock_client.get.assert_called_once()
    assert mock_client.get.call_args[0][0] == "/appliance/services"


# ============================================================================
# Test Check Mode (info modules always execute normally)
# ============================================================================


class TestCheckMode:
    """Test check mode behavior: read-only, so it executes normally."""

    def test_get_check_mode(
        self, patch_create_client, patch_ansible_module, mock_client, module_args
    ):
        """Test getting a single service in check mode still performs the GET."""
        mock_client.get.return_value = _response(200, NTPD_INFO)

        module_args.update({"service": SERVICE_ID})
        _, result = _run_module(  # pylint: disable=disallowed-name
            patch_create_client,
            patch_ansible_module,
            mock_client,
            module_args,
            check_mode=True,
        )

        assert result["value"] == NTPD_INFO
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
        assert module_under_test.LIST_ENDPOINT == "/appliance/services"

    def test_item_endpoint(self):
        """Test that the item API endpoint is correct."""
        assert module_under_test.ITEM_ENDPOINT == "/appliance/services/{service}"


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

        assert config.uri == "/appliance/services/{service}"
        assert config.http_method == "get"
        assert (
            config.build_path(params={"service": SERVICE_ID})
            == "/appliance/services/ntpd"
        )

    def test_list_operation(self):
        """Test that the LIST operation targets the collection endpoint."""
        config = module_under_test.LIST_OPERATION

        assert config.uri == "/appliance/services"
        assert config.http_method == "get"
        assert config.build_path(params={}) == "/appliance/services"
