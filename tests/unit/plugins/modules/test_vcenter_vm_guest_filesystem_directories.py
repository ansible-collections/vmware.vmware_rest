# -*- coding: utf-8 -*-
# Copyright: (c) 2026, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Unit tests for vcenter_vm_guest_filesystem_directories module.

Tests validate the action-based module behavior using the OperationConfig-based
architecture with mocked HTTP clients. This module drives guest directory
operations (create, createTemporary, delete, move) through VMware Tools, so every
state is an action performed against the ``{vm}`` endpoint.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import pytest
from unittest.mock import patch, MagicMock

from ansible_collections.vmware.vmware_rest.plugins.modules import (
    vcenter_vm_guest_filesystem_directories as module_under_test,
)

from ...common.utils import (
    AnsibleExitJson,
    exit_json,
    set_module_args,
    _response,
)

VM_ID = "vm-42"

USERNAME_PASSWORD_CREDENTIALS = {
    "type": "USERNAME_PASSWORD",
    "user_name": "root",
    "password": "vmware",
    "interactive_session": None,
    "saml_token": None,
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
        module_under_test.VmwareRestCrudModuleBase, "_create_client"
    ) as mock:
        yield mock


def _run_module(
    patch_create_client, patch_ansible_module, mock_client, args, check_mode=False
):
    """
    Configure the mocked AnsibleModule/client, run main(), and return the
    kwargs passed to exit_json.
    """
    patch_create_client.return_value = mock_client
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module
    mock_module.params = set_module_args(args)
    mock_module.exit_json.side_effect = exit_json
    mock_module.check_mode = check_mode

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    return mock_module, exc.value.kwargs


# ============================================================================
# Test ACTION Operations - create
# ============================================================================


def test_action_create(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test creating a directory in the guest."""
    mock_client.post.return_value = _response(200, {})

    module_args.update(
        {
            "state": "create",
            "vm": VM_ID,
            "credentials": USERNAME_PASSWORD_CREDENTIALS,
            "path": "/tmp/new_dir",
            "create_parents": True,
        }
    )
    mock_module, result = _run_module(
        patch_create_client, patch_ansible_module, mock_client, module_args
    )

    mock_module.exit_json.assert_called_once()
    assert result["changed"] is True
    assert result["id"] == VM_ID
    mock_client.post.assert_called_once()

    call_args = mock_client.post.call_args
    assert (
        call_args[1]["path"]
        == "/vcenter/vm/vm-42/guest/filesystem/directories?action=create"
    )
    assert call_args[1]["data"]["path"] == "/tmp/new_dir"
    assert call_args[1]["data"]["create_parents"] is True
    assert call_args[1]["data"]["credentials"] == {
        "type": "USERNAME_PASSWORD",
        "user_name": "root",
        "password": "vmware",
    }
    # No query spec is defined; the action is encoded in the URI.
    assert "query" not in call_args[1]


def test_action_create_omits_unset_optionals(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test that unset optional parameters are excluded from the request body."""
    mock_client.post.return_value = _response(200, {})

    module_args.update(
        {
            "state": "create",
            "vm": VM_ID,
            "credentials": USERNAME_PASSWORD_CREDENTIALS,
            "path": "/tmp/new_dir",
            "create_parents": None,
        }
    )
    _run_module(patch_create_client, patch_ansible_module, mock_client, module_args)

    call_args = mock_client.post.call_args
    assert "create_parents" not in call_args[1]["data"]
    # Unset credential suboptions are also dropped.
    assert "saml_token" not in call_args[1]["data"]["credentials"]
    assert "interactive_session" not in call_args[1]["data"]["credentials"]


# ============================================================================
# Test ACTION Operations - createTemporary
# ============================================================================


def test_action_create_temporary(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test creating a uniquely named temporary directory in the guest."""
    mock_client.post.return_value = _response(200, "/tmp/ansible_ab12cd")

    module_args.update(
        {
            "state": "createTemporary",
            "vm": VM_ID,
            "credentials": USERNAME_PASSWORD_CREDENTIALS,
            "prefix": "ansible_",
            "suffix": ".tmp",
            "parent_path": "/tmp",
        }
    )
    mock_module, result = _run_module(
        patch_create_client, patch_ansible_module, mock_client, module_args
    )

    assert result["changed"] is True
    assert result["id"] == VM_ID
    assert result["value"] == "/tmp/ansible_ab12cd"
    mock_client.post.assert_called_once()

    call_args = mock_client.post.call_args
    assert (
        call_args[1]["path"]
        == "/vcenter/vm/vm-42/guest/filesystem/directories?action=createTemporary"
    )
    assert call_args[1]["data"]["prefix"] == "ansible_"
    assert call_args[1]["data"]["suffix"] == ".tmp"
    assert call_args[1]["data"]["parent_path"] == "/tmp"


# ============================================================================
# Test ACTION Operations - delete
# ============================================================================


def test_action_delete(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test deleting a directory in the guest."""
    mock_client.post.return_value = _response(200, {})

    module_args.update(
        {
            "state": "delete",
            "vm": VM_ID,
            "credentials": USERNAME_PASSWORD_CREDENTIALS,
            "path": "/tmp/old_dir",
            "recursive": True,
        }
    )
    mock_module, result = _run_module(
        patch_create_client, patch_ansible_module, mock_client, module_args
    )

    assert result["changed"] is True
    assert result["id"] == VM_ID
    mock_client.post.assert_called_once()

    call_args = mock_client.post.call_args
    assert (
        call_args[1]["path"]
        == "/vcenter/vm/vm-42/guest/filesystem/directories?action=delete"
    )
    assert call_args[1]["data"]["path"] == "/tmp/old_dir"
    assert call_args[1]["data"]["recursive"] is True


# ============================================================================
# Test ACTION Operations - move
# ============================================================================


def test_action_move(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test moving or renaming a directory in the guest."""
    mock_client.post.return_value = _response(200, {})

    module_args.update(
        {
            "state": "move",
            "vm": VM_ID,
            "credentials": USERNAME_PASSWORD_CREDENTIALS,
            "path": "/tmp/old_name",
            "new_path": "/tmp/new_name",
        }
    )
    mock_module, result = _run_module(
        patch_create_client, patch_ansible_module, mock_client, module_args
    )

    assert result["changed"] is True
    assert result["id"] == VM_ID
    mock_client.post.assert_called_once()

    call_args = mock_client.post.call_args
    assert (
        call_args[1]["path"]
        == "/vcenter/vm/vm-42/guest/filesystem/directories?action=move"
    )
    assert call_args[1]["data"]["path"] == "/tmp/old_name"
    assert call_args[1]["data"]["new_path"] == "/tmp/new_name"


# ============================================================================
# Test Check Mode
# ============================================================================


class TestCheckMode:
    """Test check mode behavior: actions report a change but make no HTTP call."""

    def test_create_check_mode(
        self, patch_create_client, patch_ansible_module, mock_client, module_args
    ):
        """Test create action in check mode."""
        module_args.update(
            {
                "state": "create",
                "vm": VM_ID,
                "credentials": USERNAME_PASSWORD_CREDENTIALS,
                "path": "/tmp/new_dir",
                "create_parents": True,
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
        assert result["id"] == VM_ID
        mock_client.post.assert_not_called()

    def test_delete_check_mode(
        self, patch_create_client, patch_ansible_module, mock_client, module_args
    ):
        """Test delete action in check mode."""
        module_args.update(
            {
                "state": "delete",
                "vm": VM_ID,
                "credentials": USERNAME_PASSWORD_CREDENTIALS,
                "path": "/tmp/old_dir",
                "recursive": True,
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
        mock_client.post.assert_not_called()

    def test_move_check_mode(
        self, patch_create_client, patch_ansible_module, mock_client, module_args
    ):
        """Test move action in check mode."""
        module_args.update(
            {
                "state": "move",
                "vm": VM_ID,
                "credentials": USERNAME_PASSWORD_CREDENTIALS,
                "path": "/tmp/old_name",
                "new_path": "/tmp/new_name",
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
        mock_client.post.assert_not_called()


# ============================================================================
# Test Module Constants
# ============================================================================


class TestModuleConstants:
    """Test that module constants are correctly defined."""

    def test_moid_parameter_hints(self):
        """Test that MOID parameter hints are correct."""
        assert module_under_test.MOID_PARAMETER_HINTS == ["vm"]

    def test_list_endpoint(self):
        """Test that the list API endpoint is empty (action-only endpoint)."""
        assert module_under_test.LIST_ENDPOINT == ""

    def test_item_endpoint(self):
        """Test that the item API endpoint is empty (action-only endpoint)."""
        assert module_under_test.ITEM_ENDPOINT == ""

    def test_action_operations_keys(self):
        """Test that action operations are correctly defined."""
        assert set(module_under_test.ACTION_OPERATIONS.keys()) == {
            "create",
            "createTemporary",
            "delete",
            "move",
        }


# ============================================================================
# Test Argument Spec
# ============================================================================


class TestArgumentSpec:
    """Test the module argument specification."""

    def test_state_parameter(self):
        """Test that the state parameter is correctly defined."""
        spec = module_under_test.create_module_argument_spec()

        assert spec["state"]["type"] == "str"
        assert spec["state"]["required"] is True
        assert spec["state"]["choices"] == [
            "create",
            "createTemporary",
            "delete",
            "move",
        ]

    def test_vm_parameter_required(self):
        """Test that the vm parameter is required."""
        spec = module_under_test.create_module_argument_spec()

        assert spec["vm"]["type"] == "str"
        assert spec["vm"]["required"] is True

    def test_credentials_parameter(self):
        """Test that the credentials parameter and its suboptions are defined."""
        spec = module_under_test.create_module_argument_spec()

        assert spec["credentials"]["type"] == "dict"
        suboptions = spec["credentials"]["options"]
        assert set(suboptions.keys()) == {
            "interactive_session",
            "type",
            "user_name",
            "password",
            "saml_token",
        }
        assert suboptions["type"]["choices"] == [
            "USERNAME_PASSWORD",
            "SAML_BEARER_TOKEN",
        ]

    def test_credentials_password_no_log(self):
        """Test that the guest password is flagged no_log to avoid leaking secrets."""
        spec = module_under_test.create_module_argument_spec()

        assert spec["credentials"]["options"]["password"]["no_log"] is True

    def test_optional_parameters(self):
        """Test that the optional string/bool parameters are defined and optional."""
        spec = module_under_test.create_module_argument_spec()

        for name in ("path", "prefix", "suffix", "parent_path", "new_path"):
            assert spec[name]["type"] == "str"
            assert spec[name].get("required", False) is False

        for name in ("create_parents", "recursive"):
            assert spec[name]["type"] == "bool"
            assert spec[name].get("required", False) is False


# ============================================================================
# Test OperationConfig Building
# ============================================================================


class TestOperationConfig:
    """Test that the action OperationConfig objects build paths and bodies correctly."""

    def test_all_actions_are_post(self):
        """Test that every action operation uses the POST method."""
        for config in module_under_test.ACTION_OPERATIONS.values():
            assert config.http_method == "post"

    def test_create_build_path(self):
        """Test that the create action interpolates the vm into the path."""
        config = module_under_test.ACTION_OPERATIONS["create"]

        assert (
            config.build_path(params={"vm": VM_ID})
            == "/vcenter/vm/vm-42/guest/filesystem/directories?action=create"
        )

    def test_create_build_body(self):
        """Test that the create action builds a nested body with credentials."""
        config = module_under_test.ACTION_OPERATIONS["create"]

        body = config.build_body(
            params={
                "credentials": USERNAME_PASSWORD_CREDENTIALS,
                "path": "/tmp/dir",
                "create_parents": True,
            }
        )

        assert body == {
            "credentials": {
                "type": "USERNAME_PASSWORD",
                "user_name": "root",
                "password": "vmware",
            },
            "path": "/tmp/dir",
            "create_parents": True,
        }

    def test_create_temporary_build_body(self):
        """Test that the createTemporary action builds prefix/suffix/parent_path."""
        config = module_under_test.ACTION_OPERATIONS["createTemporary"]

        body = config.build_body(
            params={
                "credentials": USERNAME_PASSWORD_CREDENTIALS,
                "prefix": "ansible_",
                "suffix": ".tmp",
                "parent_path": "/tmp",
            }
        )

        assert body["prefix"] == "ansible_"
        assert body["suffix"] == ".tmp"
        assert body["parent_path"] == "/tmp"

    def test_move_build_body(self):
        """Test that the move action builds path and new_path."""
        config = module_under_test.ACTION_OPERATIONS["move"]

        body = config.build_body(
            params={
                "credentials": USERNAME_PASSWORD_CREDENTIALS,
                "path": "/tmp/old",
                "new_path": "/tmp/new",
            }
        )

        assert body["path"] == "/tmp/old"
        assert body["new_path"] == "/tmp/new"

    def test_actions_have_no_query(self):
        """Test that action operations define no query spec (action is in the URI)."""
        for config in module_under_test.ACTION_OPERATIONS.values():
            assert config.build_query(params={}) is None
