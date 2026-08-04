# -*- coding: utf-8 -*-
# Copyright: (c) 2026, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Unit tests for appliance_shutdown module.

Tests validate the action-only CRUD module behavior using the OperationConfig-based
architecture with mocked HTTP clients. The appliance_shutdown module supports
cancel, poweroff, and reboot actions via perform_action().
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import pytest
from unittest.mock import MagicMock, patch

from ansible_collections.vmware.vmware_rest.plugins.module_utils._operation_configs import (
    OperationConfig,
)
from ansible_collections.vmware.vmware_rest.plugins.module_utils._crud_module import (
    VmwareRestCrudModuleBase,
)

from ...common.utils import CONNECTION_PARAMS, fail_json


@pytest.fixture
def mock_module():
    """
    Mock Ansible module object.
    """
    module = MagicMock()
    module.params = CONNECTION_PARAMS.copy()
    module.check_mode = False
    module.fail_json = fail_json
    return module


@pytest.fixture
def crud_module(mock_module, mock_client):
    """
    Create CRUD module instance with appliance shutdown operation configs.

    Note: mock_client is provided by conftest.py - do not redefine it.
    """
    get_operation = OperationConfig(
        name="get",
        uri="/appliance/shutdown",
        http_method="GET",
    )

    action_operations = {
        "cancel": OperationConfig(
            name="cancel",
            uri="/appliance/shutdown?action=cancel",
            http_method="POST",
        ),
        "poweroff": OperationConfig(
            name="poweroff",
            uri="/appliance/shutdown?action=poweroff",
            http_method="POST",
            body_spec={
                "delay": {"required": True},
                "reason": {"required": True},
            },
        ),
        "reboot": OperationConfig(
            name="reboot",
            uri="/appliance/shutdown?action=reboot",
            http_method="POST",
            body_spec={
                "delay": {"required": True},
                "reason": {"required": True},
            },
        ),
    }

    with patch(
        "ansible_collections.vmware.vmware_rest.plugins.module_utils._module_base.Client",
        return_value=mock_client,
    ):
        module = VmwareRestCrudModuleBase(
            module=mock_module,
            moid_parameter_hints=[],
            get_operation_config=get_operation,
            action_operations=action_operations,
        )
        yield module


# ============================================================================
# perform_action() Tests - REBOOT
# ============================================================================


def test_perform_action_reboot(crud_module, mock_client):
    """
    Test performing a reboot action.
    """
    crud_module.params["state"] = "reboot"
    crud_module.params["delay"] = 10
    crud_module.params["reason"] = "Scheduled maintenance"

    get_response = MagicMock()
    get_response.status = 200
    get_response.json = {"action": "", "shutdown_time": ""}
    get_response.data = b'{"action": "", "shutdown_time": ""}'

    post_response = MagicMock()
    post_response.status = 200
    post_response.json = {}
    post_response.data = b"{}"

    mock_client.get.return_value = get_response
    mock_client.post.return_value = post_response

    result = crud_module.perform_action()

    assert result["changed"] is True
    mock_client.post.assert_called_once()
    call_kwargs = mock_client.post.call_args
    assert call_kwargs.kwargs["data"]["delay"] == 10
    assert call_kwargs.kwargs["data"]["reason"] == "Scheduled maintenance"


# ============================================================================
# perform_action() Tests - POWEROFF
# ============================================================================


def test_perform_action_poweroff(crud_module, mock_client):
    """
    Test performing a poweroff action.
    """
    crud_module.params["state"] = "poweroff"
    crud_module.params["delay"] = 0
    crud_module.params["reason"] = "Emergency shutdown"

    get_response = MagicMock()
    get_response.status = 200
    get_response.json = {"action": "", "shutdown_time": ""}
    get_response.data = b'{"action": "", "shutdown_time": ""}'

    post_response = MagicMock()
    post_response.status = 200
    post_response.json = {}
    post_response.data = b"{}"

    mock_client.get.return_value = get_response
    mock_client.post.return_value = post_response

    result = crud_module.perform_action()

    assert result["changed"] is True
    mock_client.post.assert_called_once()
    call_kwargs = mock_client.post.call_args
    assert call_kwargs.kwargs["data"]["delay"] == 0
    assert call_kwargs.kwargs["data"]["reason"] == "Emergency shutdown"


def test_perform_action_poweroff_with_delay(crud_module, mock_client):
    """
    Test performing a poweroff action with a non-zero delay.
    """
    crud_module.params["state"] = "poweroff"
    crud_module.params["delay"] = 30
    crud_module.params["reason"] = "Hardware maintenance"

    get_response = MagicMock()
    get_response.status = 200
    get_response.json = {"action": "", "shutdown_time": ""}
    get_response.data = b'{"action": "", "shutdown_time": ""}'

    post_response = MagicMock()
    post_response.status = 200
    post_response.json = {}
    post_response.data = b"{}"

    mock_client.get.return_value = get_response
    mock_client.post.return_value = post_response

    result = crud_module.perform_action()

    assert result["changed"] is True
    call_kwargs = mock_client.post.call_args
    assert call_kwargs.kwargs["data"]["delay"] == 30


# ============================================================================
# perform_action() Tests - CANCEL
# ============================================================================


def test_perform_action_cancel(crud_module, mock_client):
    """
    Test performing a cancel action (no body required).
    """
    crud_module.params["state"] = "cancel"

    get_response = MagicMock()
    get_response.status = 200
    get_response.json = {"action": "reboot", "shutdown_time": "2026-08-03T12:00:00Z"}
    get_response.data = b'{"action": "reboot", "shutdown_time": "2026-08-03T12:00:00Z"}'

    post_response = MagicMock()
    post_response.status = 200
    post_response.json = {}
    post_response.data = b"{}"

    mock_client.get.return_value = get_response
    mock_client.post.return_value = post_response

    result = crud_module.perform_action()

    assert result["changed"] is True
    mock_client.post.assert_called_once()


# ============================================================================
# Check Mode Tests
# ============================================================================


def test_perform_action_reboot_check_mode(crud_module, mock_client):
    """
    Test reboot action in check mode - no POST should be made.
    """
    crud_module.params["state"] = "reboot"
    crud_module.params["delay"] = 10
    crud_module.params["reason"] = "Scheduled maintenance"
    crud_module.module.check_mode = True

    get_response = MagicMock()
    get_response.status = 200
    get_response.json = {"action": "", "shutdown_time": ""}
    get_response.data = b'{"action": "", "shutdown_time": ""}'
    mock_client.get.return_value = get_response

    result = crud_module.perform_action()

    assert result["changed"] is True
    mock_client.post.assert_not_called()


def test_perform_action_poweroff_check_mode(crud_module, mock_client):
    """
    Test poweroff action in check mode - no POST should be made.
    """
    crud_module.params["state"] = "poweroff"
    crud_module.params["delay"] = 0
    crud_module.params["reason"] = "Emergency shutdown"
    crud_module.module.check_mode = True

    get_response = MagicMock()
    get_response.status = 200
    get_response.json = {"action": "", "shutdown_time": ""}
    get_response.data = b'{"action": "", "shutdown_time": ""}'
    mock_client.get.return_value = get_response

    result = crud_module.perform_action()

    assert result["changed"] is True
    mock_client.post.assert_not_called()


def test_perform_action_cancel_check_mode(crud_module, mock_client):
    """
    Test cancel action in check mode - no POST should be made.
    """
    crud_module.params["state"] = "cancel"
    crud_module.module.check_mode = True

    get_response = MagicMock()
    get_response.status = 200
    get_response.json = {"action": "reboot", "shutdown_time": "2026-08-03T12:00:00Z"}
    get_response.data = b'{"action": "reboot", "shutdown_time": "2026-08-03T12:00:00Z"}'
    mock_client.get.return_value = get_response

    result = crud_module.perform_action()

    assert result["changed"] is True
    mock_client.post.assert_not_called()


# ============================================================================
# OperationConfig Tests
# ============================================================================


def test_operation_config_build_path_no_placeholders():
    """
    Test that OperationConfig builds paths without placeholders (static URI).
    """
    config = OperationConfig(
        name="cancel",
        uri="/appliance/shutdown?action=cancel",
        http_method="POST",
    )

    path = config.build_path(params={})

    assert path == "/appliance/shutdown?action=cancel"


def test_operation_config_build_body_reboot():
    """
    Test that OperationConfig builds body for reboot action.
    """
    config = OperationConfig(
        name="reboot",
        uri="/appliance/shutdown?action=reboot",
        http_method="POST",
        body_spec={
            "delay": {"required": True},
            "reason": {"required": True},
        },
    )

    params = {"delay": 10, "reason": "Scheduled maintenance"}
    body = config.build_body(params)

    assert body == {"delay": 10, "reason": "Scheduled maintenance"}


def test_operation_config_build_body_poweroff():
    """
    Test that OperationConfig builds body for poweroff action.
    """
    config = OperationConfig(
        name="poweroff",
        uri="/appliance/shutdown?action=poweroff",
        http_method="POST",
        body_spec={
            "delay": {"required": True},
            "reason": {"required": True},
        },
    )

    params = {"delay": 0, "reason": "Emergency shutdown"}
    body = config.build_body(params)

    assert body == {"delay": 0, "reason": "Emergency shutdown"}


def test_operation_config_cancel_no_body():
    """
    Test that cancel OperationConfig has no body spec (returns None).
    """
    config = OperationConfig(
        name="cancel",
        uri="/appliance/shutdown?action=cancel",
        http_method="POST",
    )

    body = config.build_body(params={})

    assert body is None


# ============================================================================
# _resolve_resource_context() Tests
# ============================================================================


def test_resolve_resource_context_returns_get_data(crud_module, mock_client):
    """
    Test that _resolve_resource_context returns the GET response for a
    singleton endpoint (no path parameters needed).
    """
    get_response = MagicMock()
    get_response.status = 200
    get_response.json = {
        "action": "reboot",
        "shutdown_time": "2026-08-03T12:00:00Z",
        "reason": "Maintenance",
    }
    mock_client.get.return_value = get_response

    result = crud_module._resolve_resource_context()

    assert result is not None
    assert result["action"] == "reboot"
    assert result["shutdown_time"] == "2026-08-03T12:00:00Z"
