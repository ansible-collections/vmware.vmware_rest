# -*- coding: utf-8 -*-
# Copyright: (c) 2026, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import pytest
from unittest.mock import patch, MagicMock

from ansible_collections.vmware.vmware_rest.plugins.modules import (
    vcenter_datacenter as module_under_test,
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
# Test CREATE Operations
# ============================================================================


def test_create_datacenter(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test creating a new datacenter."""
    patch_create_client.return_value = mock_client
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module

    module_args.update(
        {
            "state": "present",
            "name": "my_datacenter",
            "folder": "group-d1",
        }
    )
    mock_module.params = set_module_args(module_args)
    mock_module.exit_json.side_effect = exit_json
    mock_module.check_mode = False

    # Mock list response returns empty (no existing datacenter)
    mock_client.get.return_value = _response(200, [])

    # Mock POST response returns the new datacenter ID
    create_response = "datacenter-1009"

    mock_client.post.return_value = _response(201, create_response)

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_module.exit_json.assert_called_once()
    result = exc.value.kwargs
    assert result["changed"] is True
    assert result["id"] == "datacenter-1009"
    mock_client.post.assert_called_once()


def test_create_datacenter_idempotent(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test creating a datacenter that already exists (idempotent)."""
    patch_create_client.return_value = mock_client
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module

    module_args.update(
        {
            "state": "present",
            "name": "existing_datacenter",
            "folder": "group-d1",
        }
    )
    mock_module.params = set_module_args(module_args)
    mock_module.exit_json.side_effect = exit_json
    mock_module.check_mode = False

    # Mock list response shows datacenter already exists
    list_response = [
        {"datacenter": "datacenter-1009", "name": "existing_datacenter"},
    ]

    # Mock GET response shows current state
    current_state = {
        "name": "existing_datacenter",
    }

    mock_client.get.side_effect = [
        _response(200, list_response),
        _response(200, current_state),
    ]

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_module.exit_json.assert_called_once()
    result = exc.value.kwargs
    assert result["changed"] is False
    assert result["id"] == "datacenter-1009"
    mock_client.post.assert_not_called()


def test_create_datacenter_name_only(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test creating a datacenter with only name (folder is optional)."""
    patch_create_client.return_value = mock_client
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module

    module_args.update(
        {
            "state": "present",
            "name": "my_datacenter",
        }
    )
    mock_module.params = set_module_args(module_args)
    mock_module.exit_json.side_effect = exit_json
    mock_module.check_mode = False

    # Mock list response returns empty (no existing datacenter)
    mock_client.get.return_value = _response(200, [])

    mock_client.post.return_value = _response(201, "datacenter-1009")

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    result = exc.value.kwargs
    assert result["changed"] is True
    assert result["id"] == "datacenter-1009"


# ============================================================================
# Test DELETE Operations
# ============================================================================


def test_delete_datacenter(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test deleting a datacenter."""
    patch_create_client.return_value = mock_client
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module

    module_args.update(
        {
            "state": "absent",
            "datacenter": "datacenter-1009",
            "name": "my_datacenter",
        }
    )
    mock_module.params = set_module_args(module_args)
    mock_module.exit_json.side_effect = exit_json
    mock_module.check_mode = False

    # Mock GET response shows datacenter exists
    current_state = {
        "name": "my_datacenter",
    }

    mock_client.get.return_value = _response(200, current_state)
    mock_client.delete.return_value = _response(204, None)

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_module.exit_json.assert_called_once()
    result = exc.value.kwargs
    assert result["changed"] is True
    # Verify delete was called with the correct path
    mock_client.delete.assert_called_once()
    call_args = mock_client.delete.call_args
    assert call_args[0][0] == "/vcenter/datacenter/datacenter-1009"
    assert call_args[1]["query"] == {}


def test_delete_datacenter_not_found(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test deleting a datacenter that doesn't exist (idempotent)."""
    patch_create_client.return_value = mock_client
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module

    module_args.update(
        {
            "state": "absent",
            "datacenter": "datacenter-9999",
            "name": "nonexistent_datacenter",
        }
    )
    mock_module.params = set_module_args(module_args)
    mock_module.exit_json.side_effect = exit_json
    mock_module.check_mode = False

    # Mock GET response shows datacenter doesn't exist
    mock_client.get.return_value = _response(404, None)

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_module.exit_json.assert_called_once()
    result = exc.value.kwargs
    assert result["changed"] is False
    mock_client.delete.assert_not_called()


def test_delete_by_name(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test deleting a datacenter by name."""
    patch_create_client.return_value = mock_client
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module

    module_args.update(
        {
            "state": "absent",
            "name": "my_datacenter",
        }
    )
    mock_module.params = set_module_args(module_args)
    mock_module.exit_json.side_effect = exit_json
    mock_module.check_mode = False

    # Mock list response to find datacenter by name
    list_response = [
        {"datacenter": "datacenter-1009", "name": "my_datacenter"},
    ]

    # Mock GET for existence check
    current_state = {
        "name": "my_datacenter",
    }

    mock_client.get.side_effect = [
        _response(200, list_response),
        _response(200, current_state),
    ]
    mock_client.delete.return_value = _response(204, None)

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_module.exit_json.assert_called_once()
    result = exc.value.kwargs
    assert result["changed"] is True
    # Verify delete was called with the correct path
    mock_client.delete.assert_called_once()
    call_args = mock_client.delete.call_args
    assert call_args[0][0] == "/vcenter/datacenter/datacenter-1009"
    assert call_args[1]["query"] == {}


def test_delete_with_force(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test force deleting a non-empty datacenter."""
    patch_create_client.return_value = mock_client
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module

    module_args.update(
        {
            "state": "absent",
            "datacenter": "datacenter-1009",
            "force": True,
        }
    )
    mock_module.params = set_module_args(module_args)
    mock_module.exit_json.side_effect = exit_json
    mock_module.check_mode = False

    # Mock GET response shows datacenter exists
    current_state = {
        "name": "my_datacenter",
    }

    mock_client.get.return_value = _response(200, current_state)
    mock_client.delete.return_value = _response(204, None)

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    mock_module.exit_json.assert_called_once()
    result = exc.value.kwargs
    assert result["changed"] is True
    # Verify delete was called with force in query params
    mock_client.delete.assert_called_once()
    call_args = mock_client.delete.call_args
    assert call_args[0][0] == "/vcenter/datacenter/datacenter-1009"
    assert call_args[1]["query"] == {"force": True}


# ============================================================================
# Test Check Mode
# ============================================================================


class TestCheckMode:
    """Test check mode behavior."""

    def test_create_check_mode(
        self, patch_create_client, patch_ansible_module, mock_client, module_args
    ):
        """Test creating a datacenter in check mode."""
        patch_create_client.return_value = mock_client
        mock_module = MagicMock()
        patch_ansible_module.return_value = mock_module

        module_args.update(
            {
                "state": "present",
                "name": "my_datacenter",
                "folder": "group-d1",
            }
        )
        mock_module.params = set_module_args(module_args)
        mock_module.exit_json.side_effect = exit_json
        mock_module.check_mode = True

        # Mock list response returns empty (no existing datacenter)
        mock_client.get.return_value = _response(200, [])

        with pytest.raises(AnsibleExitJson) as exc:
            module_under_test.main()

        result = exc.value.kwargs
        assert result["changed"] is True
        # In check mode, no actual POST should occur
        mock_client.post.assert_not_called()

    def test_delete_check_mode(
        self, patch_create_client, patch_ansible_module, mock_client, module_args
    ):
        """Test deleting a datacenter in check mode."""
        patch_create_client.return_value = mock_client
        mock_module = MagicMock()
        patch_ansible_module.return_value = mock_module

        module_args.update(
            {
                "state": "absent",
                "datacenter": "datacenter-1009",
                "name": "my_datacenter",
            }
        )
        mock_module.params = set_module_args(module_args)
        mock_module.exit_json.side_effect = exit_json
        mock_module.check_mode = True

        # Mock GET response shows datacenter exists
        current_state = {
            "name": "my_datacenter",
        }

        mock_client.get.return_value = _response(200, current_state)

        with pytest.raises(AnsibleExitJson) as exc:
            module_under_test.main()

        result = exc.value.kwargs
        assert result["changed"] is True
        # In check mode, no actual DELETE should occur
        mock_client.delete.assert_not_called()


# ============================================================================
# Test Module Constants
# ============================================================================


class TestModuleConstants:
    """Test that module constants are correctly defined."""

    def test_moid_parameter_hints(self):
        """Test that MOID parameter hints are correct."""
        assert module_under_test.MOID_PARAMETER_HINTS == ["datacenter"]

    def test_list_endpoint(self):
        """Test that list API endpoint is correct."""
        assert module_under_test.LIST_ENDPOINT == "/vcenter/datacenter"

    def test_item_endpoint(self):
        """Test that item API endpoint is correct."""
        assert module_under_test.ITEM_ENDPOINT == "/vcenter/datacenter/{datacenter}"


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
        assert spec["state"]["choices"] == ["present", "absent"]
        assert spec["state"]["default"] == "present"

    def test_create_module_argument_spec_datacenter(self):
        """Test that datacenter parameter is correctly defined."""
        spec = module_under_test.create_module_argument_spec()

        assert "datacenter" in spec
        assert spec["datacenter"]["type"] == "str"

    def test_create_module_argument_spec_name(self):
        """Test that name parameter is correctly defined."""
        spec = module_under_test.create_module_argument_spec()

        assert "name" in spec
        assert spec["name"]["type"] == "str"

    def test_create_module_argument_spec_folder(self):
        """Test that folder parameter is correctly defined."""
        spec = module_under_test.create_module_argument_spec()

        assert "folder" in spec
        assert spec["folder"]["type"] == "str"

    def test_create_module_argument_spec_force(self):
        """Test that force parameter is correctly defined."""
        spec = module_under_test.create_module_argument_spec()

        assert "force" in spec
        assert spec["force"]["type"] == "bool"
