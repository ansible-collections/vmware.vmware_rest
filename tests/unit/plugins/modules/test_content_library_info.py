# -*- coding: utf-8 -*-
# Copyright: (c) 2026, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Unit tests for content_library_info module.

Tests validate the Info module behavior using the OperationConfig-based
architecture with mocked HTTP clients. The GET endpoint requires a library_id
path parameter; when it is omitted the module falls back to the LIST endpoint
and enriches each listed library with a per-item GET.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import pytest
from unittest.mock import patch, MagicMock

from ansible_collections.vmware.vmware_rest.plugins.modules import (
    content_library_info as module_under_test,
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


SAMPLE_LIBRARY = {
    "id": "lib-1001",
    "name": "my_local_library",
    "type": "LOCAL",
    "description": "A local content library",
    "storage_backings": [
        {"type": "DATASTORE", "datastore_id": "datastore-42"},
    ],
}


# ============================================================================
# Test GET Operations (Single Resource by library_id)
# ============================================================================


def test_get_library_by_id(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test getting a specific content library by its library_id."""
    patch_create_client.return_value = mock_client
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module

    module_args.update({"library_id": "lib-1001"})
    mock_module.params = set_module_args(module_args)
    mock_module.exit_json.side_effect = exit_json
    mock_module.check_mode = False

    mock_client.get.return_value = _response(200, SAMPLE_LIBRARY)

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_module.exit_json.assert_called_once()
    result = exc.value.kwargs
    # A single resource fetched by id yields a dict value and a one-item info list.
    assert result["value"] == SAMPLE_LIBRARY
    assert result["info"] == [SAMPLE_LIBRARY]

    # GET should target the item endpoint with the library_id substituted in.
    mock_client.get.assert_called_once()
    assert mock_client.get.call_args[0][0] == "/content/library/lib-1001"


def test_get_library_not_found(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test getting a content library that doesn't exist (404)."""
    patch_create_client.return_value = mock_client
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module

    module_args.update({"library_id": "lib-9999"})
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
# Test LIST Operations (Fallback when library_id is omitted)
# ============================================================================


def test_list_all_libraries(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test listing all libraries when no library_id is provided.

    The list endpoint returns bare identifier strings, so the module performs a
    per-item GET to enrich each entry with its full details.
    """
    patch_create_client.return_value = mock_client
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module

    mock_module.params = set_module_args(module_args)
    mock_module.exit_json.side_effect = exit_json
    mock_module.check_mode = False

    list_response = ["lib-1001", "lib-1002"]
    detail_1 = {"id": "lib-1001", "name": "library-a", "type": "LOCAL"}
    detail_2 = {"id": "lib-1002", "name": "library-b", "type": "SUBSCRIBED"}

    mock_client.get.side_effect = [
        _response(200, list_response),
        _response(200, detail_1),
        _response(200, detail_2),
    ]

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_module.exit_json.assert_called_once()
    result = exc.value.kwargs
    assert "info" in result
    assert len(result["info"]) == 2
    # Each enriched entry carries the library_id used to look it up.
    assert result["info"][0]["library_id"] == "lib-1001"
    assert result["info"][0]["name"] == "library-a"
    assert result["info"][1]["library_id"] == "lib-1002"
    assert result["info"][1]["name"] == "library-b"

    # First call lists the collection, the remaining calls fetch each detail.
    assert mock_client.get.call_count == 3
    assert mock_client.get.call_args_list[0][0][0] == "/content/library"
    assert mock_client.get.call_args_list[1][0][0] == "/content/library/lib-1001"
    assert mock_client.get.call_args_list[2][0][0] == "/content/library/lib-1002"


def test_list_libraries_summaries_used_as_is(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test listing when the list endpoint returns complete summary dicts.

    When a listed summary does not supply the library_id path parameter needed
    for a detail lookup, it is treated as already complete and used as-is.
    """
    patch_create_client.return_value = mock_client
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module

    mock_module.params = set_module_args(module_args)
    mock_module.exit_json.side_effect = exit_json
    mock_module.check_mode = False

    list_response = [
        {"id": "lib-1001", "name": "library-a"},
        {"id": "lib-1002", "name": "library-b"},
    ]
    mock_client.get.return_value = _response(200, list_response)

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_module.exit_json.assert_called_once()
    result = exc.value.kwargs
    assert len(result["info"]) == 2
    assert result["info"] == list_response
    # No per-item enrichment is needed, so only the list call is made.
    mock_client.get.assert_called_once()
    assert mock_client.get.call_args[0][0] == "/content/library"


def test_list_libraries_empty(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test listing libraries when none exist."""
    patch_create_client.return_value = mock_client
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module

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
        """Test getting a library by id in check mode."""
        patch_create_client.return_value = mock_client
        mock_module = MagicMock()
        patch_ansible_module.return_value = mock_module

        module_args.update({"library_id": "lib-1001"})
        mock_module.params = set_module_args(module_args)
        mock_module.exit_json.side_effect = exit_json
        mock_module.check_mode = True

        mock_client.get.return_value = _response(200, SAMPLE_LIBRARY)

        with pytest.raises(AnsibleExitJson) as exc:
            module_under_test.main()

        result = exc.value.kwargs
        assert result["value"] == SAMPLE_LIBRARY
        mock_client.get.assert_called_once()

    def test_list_check_mode(
        self, patch_create_client, patch_ansible_module, mock_client, module_args
    ):
        """Test listing libraries in check mode."""
        patch_create_client.return_value = mock_client
        mock_module = MagicMock()
        patch_ansible_module.return_value = mock_module

        mock_module.params = set_module_args(module_args)
        mock_module.exit_json.side_effect = exit_json
        mock_module.check_mode = True

        mock_client.get.side_effect = [
            _response(200, ["lib-1001"]),
            _response(200, {"id": "lib-1001", "name": "library-a"}),
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
        assert module_under_test.MOID_PARAMETER_HINTS == ["library_id"]

    def test_list_endpoint(self):
        """Test that the list API endpoint is correct."""
        assert module_under_test.LIST_ENDPOINT == "/content/library"

    def test_item_endpoint(self):
        """Test that the item API endpoint is correct."""
        assert module_under_test.ITEM_ENDPOINT == "/content/library/{library_id}"

    def test_get_operation_config(self):
        """Test that the GET operation config targets the item endpoint."""
        assert module_under_test.GET_OPERATION.uri == "/content/library/{library_id}"
        assert module_under_test.GET_OPERATION.http_method == "get"

    def test_list_operation_config(self):
        """Test that the LIST operation config targets the list endpoint."""
        assert module_under_test.LIST_OPERATION.uri == "/content/library"
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

    def test_create_module_argument_spec_library_id(self):
        """Test that the library_id parameter is correctly defined."""
        spec = module_under_test.create_module_argument_spec()

        assert "library_id" in spec
        assert spec["library_id"]["type"] == "str"
        # library_id is optional; omitting it triggers the list fallback.
        assert not spec["library_id"].get("required", False)

    def test_create_module_argument_spec_no_state(self):
        """Test that the info module has no state parameter."""
        spec = module_under_test.create_module_argument_spec()

        assert "state" not in spec
