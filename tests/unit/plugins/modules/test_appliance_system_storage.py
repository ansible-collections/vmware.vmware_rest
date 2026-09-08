# -*- coding: utf-8 -*-
# Copyright: (c) 2026, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import pytest
from unittest.mock import patch, MagicMock

from ansible_collections.vmware.vmware_rest.plugins.modules import (
    appliance_system_storage as module_under_test,
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
        module_under_test.VmwareRestCrudModuleBase, "_create_client"
    ) as mock:
        yield mock


# ============================================================================
# Test ACTION Operations - Resize
# ============================================================================


def test_action_resize(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test performing a resize action."""
    patch_create_client.return_value = mock_client
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module

    module_args.update(
        {
            "state": "resize",
        }
    )
    mock_module.params = set_module_args(module_args)
    mock_module.exit_json.side_effect = exit_json
    mock_module.check_mode = False

    mock_client.post.return_value = _response(200, {})

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_module.exit_json.assert_called_once()
    result = exc.value.kwargs
    assert result["changed"] is True
    mock_client.post.assert_called_once()
    call_args = mock_client.post.call_args
    assert call_args[1]["path"] == "/appliance/system/storage?action=resize"
    # No body is sent for the resize action
    assert "data" not in call_args[1]


# ============================================================================
# Test ACTION Operations - Resize-ex
# ============================================================================


def test_action_resize_ex(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test performing a resize-ex action."""
    patch_create_client.return_value = mock_client
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module

    module_args.update(
        {
            "state": "resize-ex",
        }
    )
    mock_module.params = set_module_args(module_args)
    mock_module.exit_json.side_effect = exit_json
    mock_module.check_mode = False

    mock_client.post.return_value = _response(200, {})

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_module.exit_json.assert_called_once()
    result = exc.value.kwargs
    assert result["changed"] is True
    mock_client.post.assert_called_once()
    call_args = mock_client.post.call_args
    assert call_args[1]["path"] == "/appliance/system/storage?action=resize-ex"
    assert "data" not in call_args[1]


# ============================================================================
# Test Check Mode
# ============================================================================


class TestCheckMode:
    """Test check mode behavior."""

    def test_resize_check_mode(
        self, patch_create_client, patch_ansible_module, mock_client, module_args
    ):
        """Test resize action in check mode."""
        patch_create_client.return_value = mock_client
        mock_module = MagicMock()
        patch_ansible_module.return_value = mock_module

        module_args.update(
            {
                "state": "resize",
            }
        )
        mock_module.params = set_module_args(module_args)
        mock_module.exit_json.side_effect = exit_json
        mock_module.check_mode = True

        with pytest.raises(AnsibleExitJson) as exc:
            module_under_test.main()

        result = exc.value.kwargs
        assert result["changed"] is True
        mock_client.post.assert_not_called()

    def test_resize_ex_check_mode(
        self, patch_create_client, patch_ansible_module, mock_client, module_args
    ):
        """Test resize-ex action in check mode."""
        patch_create_client.return_value = mock_client
        mock_module = MagicMock()
        patch_ansible_module.return_value = mock_module

        module_args.update(
            {
                "state": "resize-ex",
            }
        )
        mock_module.params = set_module_args(module_args)
        mock_module.exit_json.side_effect = exit_json
        mock_module.check_mode = True

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
        """Test that MOID parameter hints are correct."""
        assert module_under_test.MOID_PARAMETER_HINTS == []

    def test_list_endpoint(self):
        """Test that list API endpoint is correct."""
        assert module_under_test.LIST_ENDPOINT == ""

    def test_item_endpoint(self):
        """Test that item API endpoint is correct."""
        assert module_under_test.ITEM_ENDPOINT == "/appliance/system/storage"

    def test_action_operations_keys(self):
        """Test that action operations are correctly defined."""
        assert set(module_under_test.ACTION_OPERATIONS.keys()) == {
            "resize",
            "resize-ex",
        }


# ============================================================================
# Test Argument Spec
# ============================================================================


class TestArgumentSpec:
    """Test the module argument specification."""

    def test_create_module_argument_spec_state(self):
        """Test that state parameter is correctly defined."""
        spec = module_under_test.create_module_argument_spec()

        assert "state" in spec
        assert spec["state"]["type"] == "str"
        assert spec["state"]["choices"] == ["resize", "resize-ex"]
        assert spec["state"]["required"] is True

    def test_create_module_argument_spec_has_connection_params(self):
        """Test that connection parameters are included."""
        spec = module_under_test.create_module_argument_spec()

        assert "vcenter_hostname" in spec
        assert "vcenter_username" in spec
        assert "vcenter_password" in spec


# ============================================================================
# Test OperationConfig Building
# ============================================================================


class TestOperationConfig:
    """Test that the action OperationConfig objects build paths and bodies correctly."""

    def test_get_operation_build_path(self):
        """Test that the get operation builds the item endpoint path."""
        config = module_under_test.GET_OPERATION

        assert config.http_method == "get"
        assert config.build_path(params={}) == "/appliance/system/storage"

    def test_resize_build_path(self):
        """Test that the resize action builds the correct path with the action query."""
        config = module_under_test.ACTION_OPERATIONS["resize"]

        assert config.http_method == "post"
        assert config.build_path(params={}) == "/appliance/system/storage?action=resize"

    def test_resize_ex_build_path(self):
        """Test that the resize-ex action builds the correct path."""
        config = module_under_test.ACTION_OPERATIONS["resize-ex"]

        assert config.http_method == "post"
        assert (
            config.build_path(params={}) == "/appliance/system/storage?action=resize-ex"
        )

    def test_actions_build_body_none(self):
        """Test that the resize actions have no request body."""
        for config in module_under_test.ACTION_OPERATIONS.values():
            assert config.build_body(params={}) is None

    def test_actions_build_query_none(self):
        """Test that action operations have no query spec (query embedded in the URI)."""
        for config in module_under_test.ACTION_OPERATIONS.values():
            assert config.build_query(params={}) is None
