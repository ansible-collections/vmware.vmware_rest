# -*- coding: utf-8 -*-
# Copyright: (c) 2026, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Unit tests for content_library_subscriptions_info module.

Tests validate the Info module behavior using the OperationConfig-based
architecture with mocked HTTP clients. Both endpoints are scoped to a required
library path parameter. The GET endpoint additionally requires a subscription
id; when it is omitted the module falls back to the LIST endpoint and enriches
each listed subscription with a per-item GET.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import pytest
from unittest.mock import patch, MagicMock

from ansible_collections.vmware.vmware_rest.plugins.modules import (
    content_library_subscriptions_info as module_under_test,
)

from ...common.utils import (
    AnsibleExitJson,
    exit_json,
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
        module_under_test.VmwareRestInfoModuleBase, "_create_client"
    ) as mock:
        yield mock


SAMPLE_SUBSCRIPTION = {
    "subscription": "sub-1001",
    "subscribed_library": "lib-2002",
    "subscribed_library_vcenter_hostname": "vcenter.example.com",
    "subscribed_library_placement": {
        "cluster": "domain-c1007",
        "folder": "group-v1",
    },
}


# ============================================================================
# Test GET Operations (Single Resource by subscription)
# ============================================================================


def test_get_subscription_by_id(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test getting a specific subscription by library and subscription id."""
    patch_create_client.return_value = mock_client
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module

    module_args.update({"library": "lib-1001", "subscription": "sub-1001"})
    mock_module.params = set_module_args(module_args)
    mock_module.exit_json.side_effect = exit_json
    mock_module.check_mode = False

    mock_client.get.return_value = _response(200, SAMPLE_SUBSCRIPTION)

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_module.exit_json.assert_called_once()
    result = exc.value.kwargs
    assert result["value"] == SAMPLE_SUBSCRIPTION
    assert result["info"] == [SAMPLE_SUBSCRIPTION]
    # The response carries the subscription MOID, so an id is reported.
    assert result["id"] == "sub-1001"

    # GET should target the item endpoint with both path params substituted in.
    mock_client.get.assert_called_once()
    assert (
        mock_client.get.call_args[0][0]
        == "/content/library/lib-1001/subscriptions/sub-1001"
    )


def test_get_subscription_not_found(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test getting a subscription that doesn't exist (404)."""
    patch_create_client.return_value = mock_client
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module

    module_args.update({"library": "lib-1001", "subscription": "sub-9999"})
    mock_module.params = set_module_args(module_args)
    mock_module.exit_json.side_effect = exit_json
    mock_module.check_mode = False

    mock_client.get.return_value = _response(404, None)

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_module.exit_json.assert_called_once()
    result = exc.value.kwargs
    assert result["info"] == []
    assert result["value"] == {}
    assert "id" not in result


# ============================================================================
# Test LIST Operations (Fallback when subscription is omitted)
# ============================================================================


def test_list_all_subscriptions(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test listing all subscriptions for a library.

    The list endpoint returns summary dicts; each is enriched with a per-item
    GET keyed on the subscription id.
    """
    patch_create_client.return_value = mock_client
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module

    module_args.update({"library": "lib-1001"})
    mock_module.params = set_module_args(module_args)
    mock_module.exit_json.side_effect = exit_json
    mock_module.check_mode = False

    list_response = [
        {"subscription": "sub-1001"},
        {"subscription": "sub-1002"},
    ]
    detail_1 = {"subscription": "sub-1001", "subscribed_library": "lib-2002"}
    detail_2 = {"subscription": "sub-1002", "subscribed_library": "lib-3003"}

    mock_client.get.side_effect = [
        _response(200, list_response),
        _response(200, detail_1),
        _response(200, detail_2),
    ]

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_module.exit_json.assert_called_once()
    result = exc.value.kwargs
    assert len(result["info"]) == 2
    assert result["info"][0]["subscription"] == "sub-1001"
    assert result["info"][0]["subscribed_library"] == "lib-2002"
    assert result["info"][1]["subscription"] == "sub-1002"

    # First call lists the collection, the rest fetch each subscription detail.
    assert mock_client.get.call_count == 3
    assert (
        mock_client.get.call_args_list[0][0][0]
        == "/content/library/lib-1001/subscriptions"
    )
    assert (
        mock_client.get.call_args_list[1][0][0]
        == "/content/library/lib-1001/subscriptions/sub-1001"
    )
    assert (
        mock_client.get.call_args_list[2][0][0]
        == "/content/library/lib-1001/subscriptions/sub-1002"
    )


def test_list_subscriptions_from_string_ids(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test listing when the list endpoint returns bare identifier strings.

    Each identifier is mapped onto the subscription path parameter for the
    detail lookup.
    """
    patch_create_client.return_value = mock_client
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module

    module_args.update({"library": "lib-1001"})
    mock_module.params = set_module_args(module_args)
    mock_module.exit_json.side_effect = exit_json
    mock_module.check_mode = False

    mock_client.get.side_effect = [
        _response(200, ["sub-1001"]),
        _response(200, {"subscribed_library": "lib-2002"}),
    ]

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_module.exit_json.assert_called_once()
    result = exc.value.kwargs
    assert len(result["info"]) == 1
    # The bare id is folded into the enriched entry.
    assert result["info"][0]["subscription"] == "sub-1001"
    assert result["info"][0]["subscribed_library"] == "lib-2002"
    assert (
        mock_client.get.call_args_list[1][0][0]
        == "/content/library/lib-1001/subscriptions/sub-1001"
    )


def test_list_subscriptions_empty(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test listing subscriptions when none exist."""
    patch_create_client.return_value = mock_client
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module

    module_args.update({"library": "lib-1001"})
    mock_module.params = set_module_args(module_args)
    mock_module.exit_json.side_effect = exit_json
    mock_module.check_mode = False

    mock_client.get.return_value = _response(200, [])

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_module.exit_json.assert_called_once()
    result = exc.value.kwargs
    assert result["info"] == []


# ============================================================================
# Test Check Mode
# ============================================================================


class TestCheckMode:
    """Test check mode behavior (info modules always execute normally)."""

    def test_get_check_mode(
        self, patch_create_client, patch_ansible_module, mock_client, module_args
    ):
        """Test getting a subscription by id in check mode."""
        patch_create_client.return_value = mock_client
        mock_module = MagicMock()
        patch_ansible_module.return_value = mock_module

        module_args.update({"library": "lib-1001", "subscription": "sub-1001"})
        mock_module.params = set_module_args(module_args)
        mock_module.exit_json.side_effect = exit_json
        mock_module.check_mode = True

        mock_client.get.return_value = _response(200, SAMPLE_SUBSCRIPTION)

        with pytest.raises(AnsibleExitJson) as exc:
            module_under_test.main()

        result = exc.value.kwargs
        assert result["value"] == SAMPLE_SUBSCRIPTION
        mock_client.get.assert_called_once()

    def test_list_check_mode(
        self, patch_create_client, patch_ansible_module, mock_client, module_args
    ):
        """Test listing subscriptions in check mode."""
        patch_create_client.return_value = mock_client
        mock_module = MagicMock()
        patch_ansible_module.return_value = mock_module

        module_args.update({"library": "lib-1001"})
        mock_module.params = set_module_args(module_args)
        mock_module.exit_json.side_effect = exit_json
        mock_module.check_mode = True

        mock_client.get.side_effect = [
            _response(200, [{"subscription": "sub-1001"}]),
            _response(200, {"subscription": "sub-1001"}),
        ]

        with pytest.raises(AnsibleExitJson) as exc:
            module_under_test.main()

        result = exc.value.kwargs
        assert len(result["info"]) == 1


# ============================================================================
# Test Module Constants
# ============================================================================


class TestModuleConstants:
    """Test that module constants are correctly defined."""

    def test_moid_parameter_hints(self):
        """Test that MOID parameter hints are correct."""
        assert module_under_test.MOID_PARAMETER_HINTS == ["library", "subscription"]

    def test_list_endpoint(self):
        """Test that the list API endpoint is correct."""
        assert (
            module_under_test.LIST_ENDPOINT
            == "/content/library/{library}/subscriptions"
        )

    def test_item_endpoint(self):
        """Test that the item API endpoint is correct."""
        assert (
            module_under_test.ITEM_ENDPOINT
            == "/content/library/{library}/subscriptions/{subscription}"
        )

    def test_get_operation_config(self):
        """Test that the GET operation config targets the item endpoint."""
        assert (
            module_under_test.GET_OPERATION.uri
            == "/content/library/{library}/subscriptions/{subscription}"
        )
        assert module_under_test.GET_OPERATION.http_method == "get"

    def test_list_operation_config(self):
        """Test that the LIST operation config targets the list endpoint."""
        assert (
            module_under_test.LIST_OPERATION.uri
            == "/content/library/{library}/subscriptions"
        )
        assert module_under_test.LIST_OPERATION.http_method == "get"


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

    def test_create_module_argument_spec_library_required(self):
        """Test that the library parameter is required."""
        spec = module_under_test.create_module_argument_spec()

        assert "library" in spec
        assert spec["library"]["type"] == "str"
        assert spec["library"]["required"] is True

    def test_create_module_argument_spec_subscription_optional(self):
        """Test that the subscription parameter is optional."""
        spec = module_under_test.create_module_argument_spec()

        assert "subscription" in spec
        assert spec["subscription"]["type"] == "str"
        assert not spec["subscription"].get("required", False)

    def test_create_module_argument_spec_no_state(self):
        """Test that the info module has no state parameter."""
        spec = module_under_test.create_module_argument_spec()

        assert "state" not in spec
