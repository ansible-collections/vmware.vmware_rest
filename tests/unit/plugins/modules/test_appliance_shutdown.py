# -*- coding: utf-8 -*-
# Copyright: (c) 2026, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import pytest
from unittest.mock import patch, MagicMock

from ansible_collections.vmware.vmware_rest.plugins.modules import (
    appliance_shutdown as module_under_test,
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
# Test ACTION Operations - Reboot
# ============================================================================


def test_action_reboot(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test performing a reboot action."""
    patch_create_client.return_value = mock_client
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module

    module_args.update(
        {
            "state": "reboot",
            "delay": 10,
            "reason": "Scheduled maintenance",
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
    assert call_args[1]["path"] == "/appliance/shutdown?action=reboot"
    assert call_args[1]["data"]["delay"] == 10
    assert call_args[1]["data"]["reason"] == "Scheduled maintenance"


def test_action_reboot_immediate(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test performing an immediate reboot with zero delay."""
    patch_create_client.return_value = mock_client
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module

    module_args.update(
        {
            "state": "reboot",
            "delay": 0,
            "reason": "Emergency reboot",
        }
    )
    mock_module.params = set_module_args(module_args)
    mock_module.exit_json.side_effect = exit_json
    mock_module.check_mode = False

    mock_client.post.return_value = _response(200, {})

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    result = exc.value.kwargs
    assert result["changed"] is True
    call_args = mock_client.post.call_args
    assert call_args[1]["data"]["delay"] == 0


# ============================================================================
# Test ACTION Operations - Poweroff
# ============================================================================


def test_action_poweroff(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test performing a poweroff action."""
    patch_create_client.return_value = mock_client
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module

    module_args.update(
        {
            "state": "poweroff",
            "delay": 5,
            "reason": "Hardware maintenance",
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
    assert call_args[1]["path"] == "/appliance/shutdown?action=poweroff"
    assert call_args[1]["data"]["delay"] == 5
    assert call_args[1]["data"]["reason"] == "Hardware maintenance"


def test_action_poweroff_immediate(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test performing an immediate poweroff with zero delay."""
    patch_create_client.return_value = mock_client
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module

    module_args.update(
        {
            "state": "poweroff",
            "delay": 0,
            "reason": "Emergency shutdown",
        }
    )
    mock_module.params = set_module_args(module_args)
    mock_module.exit_json.side_effect = exit_json
    mock_module.check_mode = False

    mock_client.post.return_value = _response(200, {})

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    result = exc.value.kwargs
    assert result["changed"] is True
    call_args = mock_client.post.call_args
    assert call_args[1]["data"]["delay"] == 0
    assert call_args[1]["data"]["reason"] == "Emergency shutdown"


# ============================================================================
# Test ACTION Operations - Cancel
# ============================================================================


def test_action_cancel(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test cancelling a pending shutdown (no body required)."""
    patch_create_client.return_value = mock_client
    mock_module = MagicMock()
    patch_ansible_module.return_value = mock_module

    module_args.update(
        {
            "state": "cancel",
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
    assert call_args[1]["path"] == "/appliance/shutdown?action=cancel"
    assert "data" not in call_args[1]


# ============================================================================
# Test Check Mode
# ============================================================================


class TestCheckMode:
    """Test check mode behavior."""

    def test_reboot_check_mode(
        self, patch_create_client, patch_ansible_module, mock_client, module_args
    ):
        """Test reboot action in check mode."""
        patch_create_client.return_value = mock_client
        mock_module = MagicMock()
        patch_ansible_module.return_value = mock_module

        module_args.update(
            {
                "state": "reboot",
                "delay": 10,
                "reason": "Scheduled maintenance",
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

    def test_poweroff_check_mode(
        self, patch_create_client, patch_ansible_module, mock_client, module_args
    ):
        """Test poweroff action in check mode."""
        patch_create_client.return_value = mock_client
        mock_module = MagicMock()
        patch_ansible_module.return_value = mock_module

        module_args.update(
            {
                "state": "poweroff",
                "delay": 0,
                "reason": "Emergency shutdown",
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

    def test_cancel_check_mode(
        self, patch_create_client, patch_ansible_module, mock_client, module_args
    ):
        """Test cancel action in check mode."""
        patch_create_client.return_value = mock_client
        mock_module = MagicMock()
        patch_ansible_module.return_value = mock_module

        module_args.update(
            {
                "state": "cancel",
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
        assert module_under_test.ITEM_ENDPOINT == "/appliance/shutdown"

    def test_action_operations_keys(self):
        """Test that action operations are correctly defined."""
        assert set(module_under_test.ACTION_OPERATIONS.keys()) == {
            "cancel",
            "poweroff",
            "reboot",
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
        assert spec["state"]["choices"] == ["cancel", "poweroff", "reboot"]
        assert spec["state"]["required"] is True

    def test_create_module_argument_spec_delay(self):
        """Test that delay parameter is correctly defined."""
        spec = module_under_test.create_module_argument_spec()

        assert "delay" in spec
        assert spec["delay"]["type"] == "int"

    def test_create_module_argument_spec_reason(self):
        """Test that reason parameter is correctly defined."""
        spec = module_under_test.create_module_argument_spec()

        assert "reason" in spec
        assert spec["reason"]["type"] == "str"
