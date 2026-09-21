# -*- coding: utf-8 -*-
# Copyright: (c) 2026, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Unit tests for vcenter_vm_hardware_parallel module.

Tests validate the CRUD module behavior using the OperationConfig-based
architecture with mocked HTTP clients. The tests drive the module's main()
entrypoint so the real routing, argument spec, and operation configs are
exercised.

This module manages virtual parallel ports on a VM. Ports live in a per-VM
collection: creating a port POSTs to the collection endpoint and returns the
new port's MOID, while a specific port is addressed by both the C(vm) and
C(port) MOIDs. In addition to create/update/delete the module supports the
non-idempotent C(connect) and C(disconnect) actions, which always issue their
POST regardless of current state.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import pytest
from unittest.mock import patch, MagicMock

from ansible_collections.vmware.vmware_rest.plugins.modules import (
    vcenter_vm_hardware_parallel as module_under_test,
)

from ...common.utils import (
    AnsibleExitJson,
    exit_json,
    fail_json,
    set_module_args,
    _response,
)

VM_ID = "vm-1001"
PORT_ID = "13000"

# A realistic parallel port response for
# GET /vcenter/vm/{vm}/hardware/parallel/{port}.
PARALLEL_PORT = {
    "label": "Parallel port 1",
    "backing": {
        "type": "FILE",
        "file": "[datastore1] parallel/port1.log",
    },
    "state": "CONNECTED",
    "start_connected": True,
    "allow_guest_control": True,
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
# Test state=present - CREATE
# ============================================================================


def test_ensure_present_creates_file_backed_port(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test creating a file-backed parallel port POSTs to the collection."""
    # Create returns the new port's MOID as a bare JSON string.
    mock_client.post.return_value = _response(200, PORT_ID)

    module_args.update(
        {
            "state": "present",
            "vm": VM_ID,
            "backing": {
                "type": "FILE",
                "file": "[datastore1] parallel/port1.log",
            },
            "start_connected": True,
            "allow_guest_control": True,
        }
    )
    mock_module, result = _run_module(
        patch_create_client, patch_ansible_module, mock_client, module_args
    )

    mock_module.exit_json.assert_called_once()
    assert result["changed"] is True
    assert result["id"] == PORT_ID

    # No port MOID was provided, so no GET/PATCH/DELETE should be attempted.
    mock_client.patch.assert_not_called()
    mock_client.delete.assert_not_called()

    mock_client.post.assert_called_once()
    post_call = mock_client.post.call_args
    assert post_call[0][0] == "/vcenter/vm/vm-1001/hardware/parallel"
    assert post_call[1]["data"] == {
        "backing": {
            "type": "FILE",
            "file": "[datastore1] parallel/port1.log",
        },
        "start_connected": True,
        "allow_guest_control": True,
    }


def test_ensure_present_creates_host_device_backed_port(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test creating a host-device-backed parallel port builds the right body."""
    mock_client.post.return_value = _response(200, PORT_ID)

    module_args.update(
        {
            "state": "present",
            "vm": VM_ID,
            "backing": {
                "type": "HOST_DEVICE",
                "host_device": "/dev/parport0",
            },
        }
    )
    _, result = _run_module(  # pylint: disable=disallowed-name
        patch_create_client, patch_ansible_module, mock_client, module_args
    )

    assert result["changed"] is True
    assert result["id"] == PORT_ID
    mock_client.post.assert_called_once()
    post_call = mock_client.post.call_args
    # Only the keys the user provided are sent; unset optionals are omitted.
    assert post_call[1]["data"] == {
        "backing": {
            "type": "HOST_DEVICE",
            "host_device": "/dev/parport0",
        }
    }


# ============================================================================
# Test state=present - UPDATE
# ============================================================================


def test_ensure_present_updates_port(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test updating an existing port PATCHes only the changed settings."""
    mock_client.get.return_value = _response(200, PARALLEL_PORT)
    mock_client.patch.return_value = _response(204, None)

    module_args.update(
        {
            "state": "present",
            "vm": VM_ID,
            "port": PORT_ID,
            "allow_guest_control": False,
        }
    )
    _, result = _run_module(  # pylint: disable=disallowed-name
        patch_create_client, patch_ansible_module, mock_client, module_args
    )

    assert result["changed"] is True
    assert result["id"] == PORT_ID
    assert result["diff"]["allow_guest_control"] == {"before": True, "after": False}

    mock_client.patch.assert_called_once()
    patch_call = mock_client.patch.call_args
    assert patch_call[0][0] == "/vcenter/vm/vm-1001/hardware/parallel/13000"
    assert patch_call[1]["data"] == {"allow_guest_control": False}
    mock_client.post.assert_not_called()


def test_ensure_present_no_changes(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """
    Test no changes when the requested settings already match current state
    (idempotent). Only the keys the user specified are compared, so read-only
    fields the API reports must not register as a change.
    """
    mock_client.get.return_value = _response(200, PARALLEL_PORT)

    module_args.update(
        {
            "state": "present",
            "vm": VM_ID,
            "port": PORT_ID,
            "start_connected": True,
            "allow_guest_control": True,
        }
    )
    _, result = _run_module(  # pylint: disable=disallowed-name
        patch_create_client, patch_ansible_module, mock_client, module_args
    )

    assert result["changed"] is False
    assert result["id"] == PORT_ID
    assert result["diff"] == {}
    mock_client.patch.assert_not_called()


# ============================================================================
# Test state=absent - DELETE
# ============================================================================


def test_ensure_absent_deletes_port(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test deleting an existing parallel port issues a DELETE."""
    mock_client.get.return_value = _response(200, PARALLEL_PORT)
    mock_client.delete.return_value = _response(204, None)

    module_args.update(
        {
            "state": "absent",
            "vm": VM_ID,
            "port": PORT_ID,
        }
    )
    _, result = _run_module(  # pylint: disable=disallowed-name
        patch_create_client, patch_ansible_module, mock_client, module_args
    )

    assert result["changed"] is True
    assert result["id"] == PORT_ID

    mock_client.delete.assert_called_once()
    delete_call = mock_client.delete.call_args
    assert delete_call[0][0] == "/vcenter/vm/vm-1001/hardware/parallel/13000"


def test_ensure_absent_already_absent(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test deleting a port that does not exist is a no-op (idempotent)."""
    mock_client.get.return_value = _response(404, None)

    module_args.update(
        {
            "state": "absent",
            "vm": VM_ID,
            "port": "13999",
        }
    )
    _, result = _run_module(  # pylint: disable=disallowed-name
        patch_create_client, patch_ansible_module, mock_client, module_args
    )

    assert result["changed"] is False
    mock_client.delete.assert_not_called()


# ============================================================================
# Test action states - connect / disconnect
# ============================================================================


def test_state_connect_posts_action(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test state=connect POSTs the connect action for the given port."""
    mock_client.post.return_value = _response(204, None)

    module_args.update(
        {
            "state": "connect",
            "vm": VM_ID,
            "port": PORT_ID,
        }
    )
    _, result = _run_module(  # pylint: disable=disallowed-name
        patch_create_client, patch_ansible_module, mock_client, module_args
    )

    assert result["changed"] is True
    assert result["id"] == PORT_ID

    mock_client.post.assert_called_once()
    post_call = mock_client.post.call_args
    assert (
        post_call[1]["path"]
        == "/vcenter/vm/vm-1001/hardware/parallel/13000?action=connect"
    )
    # Actions do not consult current state, so no GET is performed.
    mock_client.get.assert_not_called()


def test_state_disconnect_posts_action(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test state=disconnect POSTs the disconnect action for the given port."""
    mock_client.post.return_value = _response(204, None)

    module_args.update(
        {
            "state": "disconnect",
            "vm": VM_ID,
            "port": PORT_ID,
        }
    )
    _, result = _run_module(  # pylint: disable=disallowed-name
        patch_create_client, patch_ansible_module, mock_client, module_args
    )

    assert result["changed"] is True
    assert result["id"] == PORT_ID

    mock_client.post.assert_called_once()
    post_call = mock_client.post.call_args
    assert (
        post_call[1]["path"]
        == "/vcenter/vm/vm-1001/hardware/parallel/13000?action=disconnect"
    )


# ============================================================================
# Test Check Mode
# ============================================================================


class TestCheckMode:
    """Test check mode reports a change but makes no write HTTP call."""

    def test_create_check_mode(
        self, patch_create_client, patch_ansible_module, mock_client, module_args
    ):
        """Test creating a port in check mode makes no POST."""
        module_args.update(
            {
                "state": "present",
                "vm": VM_ID,
                "backing": {"type": "HOST_DEVICE"},
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

    def test_update_check_mode(
        self, patch_create_client, patch_ansible_module, mock_client, module_args
    ):
        """Test updating a port in check mode reports the diff but no PATCH."""
        mock_client.get.return_value = _response(200, PARALLEL_PORT)

        module_args.update(
            {
                "state": "present",
                "vm": VM_ID,
                "port": PORT_ID,
                "allow_guest_control": False,
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
        assert result["diff"]["allow_guest_control"] == {
            "before": True,
            "after": False,
        }
        mock_client.patch.assert_not_called()

    def test_delete_check_mode(
        self, patch_create_client, patch_ansible_module, mock_client, module_args
    ):
        """Test deleting a port in check mode makes no DELETE."""
        mock_client.get.return_value = _response(200, PARALLEL_PORT)

        module_args.update(
            {
                "state": "absent",
                "vm": VM_ID,
                "port": PORT_ID,
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
        assert result["id"] == PORT_ID
        mock_client.delete.assert_not_called()

    def test_connect_check_mode(
        self, patch_create_client, patch_ansible_module, mock_client, module_args
    ):
        """Test the connect action in check mode makes no POST."""
        module_args.update(
            {
                "state": "connect",
                "vm": VM_ID,
                "port": PORT_ID,
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
        assert result["id"] == PORT_ID
        mock_client.post.assert_not_called()


# ============================================================================
# Test Module Constants
# ============================================================================


class TestModuleConstants:
    """Test that module constants are correctly defined."""

    def test_moid_parameter_hints(self):
        """Test that the MOID parameter hints cover the vm and port ids."""
        assert module_under_test.MOID_PARAMETER_HINTS == ["vm", "port"]

    def test_list_endpoint(self):
        """Test that the list API endpoint is the per-VM collection."""
        assert module_under_test.LIST_ENDPOINT == "/vcenter/vm/{vm}/hardware/parallel"

    def test_item_endpoint(self):
        """Test that the item API endpoint is correct."""
        assert (
            module_under_test.ITEM_ENDPOINT
            == "/vcenter/vm/{vm}/hardware/parallel/{port}"
        )


# ============================================================================
# Test OperationConfig Definitions
# ============================================================================


class TestOperationConfigs:
    """Test the module's operation config definitions."""

    def test_get_operation(self):
        """Test the GET operation targets the item endpoint."""
        assert module_under_test.GET_OPERATION.http_method == "get"
        assert (
            module_under_test.GET_OPERATION.uri
            == "/vcenter/vm/{vm}/hardware/parallel/{port}"
        )

    def test_create_operation_method_and_path(self):
        """Test the CREATE operation POSTs to the collection endpoint."""
        assert module_under_test.CREATE_OPERATION.http_method == "post"
        path = module_under_test.CREATE_OPERATION.build_path({"vm": VM_ID})
        assert path == "/vcenter/vm/vm-1001/hardware/parallel"

    def test_create_operation_build_body(self):
        """Test the CREATE body carries set params and omits unset ones."""
        body = module_under_test.CREATE_OPERATION.build_body(
            {
                "backing": {"type": "FILE", "file": "[ds] p.log"},
                "start_connected": True,
            }
        )
        assert body == {
            "backing": {"type": "FILE", "file": "[ds] p.log"},
            "start_connected": True,
        }

    def test_update_operation_method_and_path(self):
        """Test the UPDATE operation PATCHes the item endpoint."""
        assert module_under_test.UPDATE_OPERATION.http_method == "patch"
        path = module_under_test.UPDATE_OPERATION.build_path(
            {"vm": VM_ID, "port": PORT_ID}
        )
        assert path == "/vcenter/vm/vm-1001/hardware/parallel/13000"

    def test_delete_operation_method(self):
        """Test the DELETE operation uses the DELETE method."""
        assert module_under_test.DELETE_OPERATION.http_method == "delete"

    def test_action_operations(self):
        """Test the connect/disconnect action configs build action paths."""
        connect = module_under_test.ACTION_OPERATIONS["connect"]
        disconnect = module_under_test.ACTION_OPERATIONS["disconnect"]
        assert connect.http_method == "post"
        assert disconnect.http_method == "post"
        assert (
            connect.build_path({"vm": VM_ID, "port": PORT_ID})
            == "/vcenter/vm/vm-1001/hardware/parallel/13000?action=connect"
        )
        assert (
            disconnect.build_path({"vm": VM_ID, "port": PORT_ID})
            == "/vcenter/vm/vm-1001/hardware/parallel/13000?action=disconnect"
        )


# ============================================================================
# Test Argument Spec
# ============================================================================


class TestArgumentSpec:
    """Test the module argument specification."""

    def test_state_parameter(self):
        """Test that state supports present/absent/connect/disconnect."""
        spec = module_under_test.create_module_argument_spec()

        assert spec["state"]["type"] == "str"
        assert spec["state"]["default"] == "present"
        assert spec["state"]["choices"] == [
            "present",
            "absent",
            "connect",
            "disconnect",
        ]

    def test_vm_parameter_required(self):
        """Test that the vm parameter is required."""
        spec = module_under_test.create_module_argument_spec()

        assert spec["vm"]["type"] == "str"
        assert spec["vm"]["required"] is True

    def test_port_parameter_optional(self):
        """Test that the port parameter is an optional string."""
        spec = module_under_test.create_module_argument_spec()

        assert spec["port"]["type"] == "str"
        assert spec["port"].get("required", False) is False

    def test_scalar_parameters(self):
        """Test the optional boolean settings."""
        spec = module_under_test.create_module_argument_spec()

        assert spec["start_connected"]["type"] == "bool"
        assert spec["allow_guest_control"]["type"] == "bool"

    def test_backing_parameter(self):
        """Test the backing dict parameter and its suboptions."""
        spec = module_under_test.create_module_argument_spec()

        assert spec["backing"]["type"] == "dict"
        options = spec["backing"]["options"]
        assert options["type"]["type"] == "str"
        assert options["type"]["choices"] == ["FILE", "HOST_DEVICE"]
        assert options["file"]["type"] == "str"
        assert options["host_device"]["type"] == "str"
