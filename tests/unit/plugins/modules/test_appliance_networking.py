# -*- coding: utf-8 -*-
# Copyright: (c) 2026, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Unit tests for appliance_networking module.

Tests validate the CRUD module behavior using the OperationConfig-based
architecture with mocked HTTP clients.

``appliance_networking`` manages a singleton resource (there is no MOID and no
LIST endpoint). It supports two states:

- ``present`` - PATCH ``/appliance/networking`` whenever ``ipv6_enabled`` is
  supplied. The GET response (``Appliance.Networking.Info``) only ever contains
  ``dns`` and ``interfaces`` -- ``ipv6_enabled`` is write-only and lives solely
  in the PATCH ``UpdateSpec``. Because the current value can never be read back,
  the module cannot prove a no-op and must always write when ``ipv6_enabled`` is
  requested.
- ``reset``   - POST ``/appliance/networking?action=reset`` to reset and restart
  the network configuration on all interfaces.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import pytest
from unittest.mock import patch, MagicMock

from ansible_collections.vmware.vmware_rest.plugins.modules import (
    appliance_networking as module_under_test,
)

from ...common.utils import (
    AnsibleExitJson,
    exit_json,
    fail_json,
    set_module_args,
    _response,
)


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


def _run_module(patch_ansible_module, module_args, check_mode=False):
    """Helper: wire up the mocked module and return the mock module."""
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module
    mock_module.params = set_module_args(module_args)
    mock_module.exit_json.side_effect = exit_json
    mock_module.fail_json.side_effect = fail_json
    mock_module.check_mode = check_mode
    return mock_module


# A representative GET /appliance/networking response. The real
# ``Appliance.Networking.Info`` schema is ``required: [dns, interfaces]`` with
# exactly those two properties -- ``ipv6_enabled`` never appears here, so the
# fixture must not invent it.
CURRENT_CONFIG = {
    "dns": {
        "mode": "STATIC",
        "hostname": "vcenter.example.com",
        "servers": ["10.20.80.1"],
    },
    "interfaces": {
        "nic0": {"name": "nic0", "status": "up"},
    },
}


# ============================================================================
# Test state=present (UPDATE) Operations
# ============================================================================


def test_present_enables_ipv6(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test enabling IPv6 patches the resource.

    The GET response never carries ``ipv6_enabled``, so the current value is
    unknown and the module must issue the PATCH. The diff ``before`` is
    therefore ``None`` (unknown), not the requested value read back out of the
    user's own params.
    """
    patch_create_client.return_value = mock_client
    module_args.update({"state": "present", "ipv6_enabled": True})
    mock_module = _run_module(patch_ansible_module, module_args)

    mock_client.get.return_value = _response(200, CURRENT_CONFIG)
    mock_client.patch.return_value = _response(200, {})

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_module.exit_json.assert_called_once()
    result = exc.value.kwargs
    assert result["changed"] is True
    assert result["diff"] == {"ipv6_enabled": {"before": None, "after": True}}

    mock_client.patch.assert_called_once()
    call_args = mock_client.patch.call_args
    assert call_args[0][0] == "/appliance/networking"
    assert call_args[1]["data"] == {"ipv6_enabled": True}


def test_present_disables_ipv6(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test disabling IPv6 patches the resource.

    As with enabling, the current value is not readable from GET, so the module
    always writes and reports ``before: None``.
    """
    patch_create_client.return_value = mock_client
    module_args.update({"state": "present", "ipv6_enabled": False})
    mock_module = _run_module(patch_ansible_module, module_args)

    mock_client.get.return_value = _response(200, CURRENT_CONFIG)
    mock_client.patch.return_value = _response(200, {})

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    result = exc.value.kwargs
    assert result["changed"] is True
    assert result["diff"] == {"ipv6_enabled": {"before": None, "after": False}}
    mock_client.patch.assert_called_once()
    assert mock_client.patch.call_args[1]["data"] == {"ipv6_enabled": False}


def test_present_ipv6_always_writes_when_state_unknown(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test that ipv6_enabled cannot be idempotent.

    ``Appliance.Networking.Info`` never reports ``ipv6_enabled``, so the module
    can never prove the requested value already matches. Requesting it must
    therefore always PATCH, even when the value happens to already be applied on
    the appliance.
    """
    patch_create_client.return_value = mock_client
    module_args.update({"state": "present", "ipv6_enabled": False})
    mock_module = _run_module(patch_ansible_module, module_args)

    mock_client.get.return_value = _response(200, CURRENT_CONFIG)
    mock_client.patch.return_value = _response(200, {})

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_module.exit_json.assert_called_once()
    result = exc.value.kwargs
    assert result["changed"] is True
    assert result["diff"] == {"ipv6_enabled": {"before": None, "after": False}}
    mock_client.patch.assert_called_once()


def test_present_without_ipv6_param_makes_no_changes(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test that omitting ipv6_enabled leaves the configuration unchanged."""
    patch_create_client.return_value = mock_client
    module_args.update({"state": "present"})
    mock_module = _run_module(patch_ansible_module, module_args)

    mock_client.get.return_value = _response(200, CURRENT_CONFIG)

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    result = exc.value.kwargs
    assert result["changed"] is False
    assert result["diff"] == {}
    # The current state is still read, but nothing is patched.
    mock_client.get.assert_called_once()
    mock_client.patch.assert_not_called()


# ============================================================================
# Test state=reset (ACTION) Operations
# ============================================================================


def test_reset_action(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test resetting the network configuration posts to the reset action."""
    patch_create_client.return_value = mock_client
    module_args.update({"state": "reset"})
    mock_module = _run_module(patch_ansible_module, module_args)

    mock_client.post.return_value = _response(200, {})

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_module.exit_json.assert_called_once()
    result = exc.value.kwargs
    assert result["changed"] is True

    mock_client.post.assert_called_once()
    call_args = mock_client.post.call_args
    assert call_args[1]["path"] == "/appliance/networking?action=reset"
    # The reset action has no body or query parameters.
    assert "data" not in call_args[1]
    assert "query" not in call_args[1]
    # A reset must never issue a GET or PATCH against the resource.
    mock_client.get.assert_not_called()
    mock_client.patch.assert_not_called()


# ============================================================================
# Test Check Mode
# ============================================================================


class TestCheckMode:
    """Test check mode behavior."""

    def test_present_check_mode(
        self, patch_create_client, patch_ansible_module, mock_client, module_args
    ):
        """Test that an update in check mode reports change without patching."""
        patch_create_client.return_value = mock_client
        module_args.update({"state": "present", "ipv6_enabled": True})
        mock_module = _run_module(patch_ansible_module, module_args, check_mode=True)

        mock_client.get.return_value = _response(200, CURRENT_CONFIG)

        with pytest.raises(AnsibleExitJson) as exc:
            module_under_test.main()

        result = exc.value.kwargs
        assert result["changed"] is True
        assert result["diff"] == {"ipv6_enabled": {"before": None, "after": True}}
        mock_client.patch.assert_not_called()

    def test_reset_check_mode(
        self, patch_create_client, patch_ansible_module, mock_client, module_args
    ):
        """Test that a reset in check mode reports change without posting."""
        patch_create_client.return_value = mock_client
        module_args.update({"state": "reset"})
        mock_module = _run_module(patch_ansible_module, module_args, check_mode=True)

        with pytest.raises(AnsibleExitJson) as exc:
            module_under_test.main()

        result = exc.value.kwargs
        assert result["changed"] is True
        mock_client.post.assert_not_called()


# ============================================================================
# Test Module Constants
# ============================================================================


class TestModuleConstants:
    """Test that module constants are correctly defined."""

    def test_moid_parameter_hints(self):
        """Test that MOID parameter hints are empty for this singleton."""
        assert module_under_test.MOID_PARAMETER_HINTS == []

    def test_list_endpoint(self):
        """Test that there is no list API endpoint."""
        assert module_under_test.LIST_ENDPOINT == ""

    def test_item_endpoint(self):
        """Test that the item API endpoint is correct."""
        assert module_under_test.ITEM_ENDPOINT == "/appliance/networking"

    def test_get_operation_config(self):
        """Test that the GET operation config targets the item endpoint."""
        assert module_under_test.GET_OPERATION.uri == "/appliance/networking"
        assert module_under_test.GET_OPERATION.http_method == "get"

    def test_update_operation_config(self):
        """Test that the UPDATE operation config is a PATCH on the item endpoint."""
        assert module_under_test.UPDATE_OPERATION.uri == "/appliance/networking"
        assert module_under_test.UPDATE_OPERATION.http_method == "patch"

    def test_action_operations_keys(self):
        """Test that the reset action operation is defined."""
        assert set(module_under_test.ACTION_OPERATIONS.keys()) == {"reset"}
        assert module_under_test.ACTION_OPERATIONS["reset"].http_method == "post"


# ============================================================================
# Test OperationConfig path/body building
# ============================================================================


class TestOperationConfig:
    """Test OperationConfig path and body building for this module."""

    def test_get_build_path_is_static(self):
        """GET path has no template parameters."""
        assert module_under_test.GET_OPERATION.build_path({}) == "/appliance/networking"

    def test_update_build_body_with_ipv6(self):
        """UPDATE body contains ipv6_enabled when supplied."""
        body = module_under_test.UPDATE_OPERATION.build_body({"ipv6_enabled": True})
        assert body == {"ipv6_enabled": True}

    def test_update_build_body_omits_unset_ipv6(self):
        """UPDATE body is empty when ipv6_enabled is not supplied."""
        assert module_under_test.UPDATE_OPERATION.build_body({}) == {}

    def test_reset_build_path_is_static(self):
        """The reset action path carries the action query in the URI."""
        assert (
            module_under_test.ACTION_OPERATIONS["reset"].build_path({})
            == "/appliance/networking?action=reset"
        )


# ============================================================================
# Test Argument Spec
# ============================================================================


class TestArgumentSpec:
    """Test the module argument specification."""

    def test_create_module_argument_spec_has_connection_params(self):
        """Test that connection parameters are included."""
        spec = module_under_test.create_module_argument_spec()

        assert "vcenter_hostname" in spec
        assert "vcenter_username" in spec
        assert "vcenter_password" in spec

    def test_create_module_argument_spec_state(self):
        """Test that the state parameter is correctly defined."""
        spec = module_under_test.create_module_argument_spec()

        assert spec["state"]["type"] == "str"
        assert spec["state"]["choices"] == ["present", "reset"]
        assert spec["state"]["default"] == "present"

    def test_create_module_argument_spec_ipv6_enabled(self):
        """Test that the ipv6_enabled parameter is defined and optional."""
        spec = module_under_test.create_module_argument_spec()

        assert spec["ipv6_enabled"]["type"] == "bool"
        assert not spec["ipv6_enabled"].get("required", False)
