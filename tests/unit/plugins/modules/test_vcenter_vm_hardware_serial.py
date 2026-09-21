# -*- coding: utf-8 -*-
# Copyright: (c) 2026, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Unit tests for vcenter_vm_hardware_serial CRUD module.

This module manages virtual serial ports on a VM. It is a full CRUD module
addressed by the required C(vm) MOID and an optional C(port) MOID: omitting
C(port) with C(state=present) creates a new serial port, while providing it
updates the existing one. It supports create (POST), update (PATCH), delete
(DELETE), and the C(connect)/C(disconnect) runtime actions (POST with an
C(action) query on the item endpoint). Only C(present) and C(absent) are
idempotent.

Tests validate the module behavior using the OperationConfig-based
architecture with mocked HTTP clients. The tests drive the module's main()
entrypoint so the real routing, argument spec, and operation configs are
exercised.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import pytest
from unittest.mock import patch, MagicMock

from ansible_collections.vmware.vmware_rest.plugins.modules import (
    vcenter_vm_hardware_serial as module_under_test,
)

from ...common.utils import (
    AnsibleExitJson,
    exit_json,
    fail_json,
    set_module_args,
    _response,
)

VM_ID = "vm-1001"
PORT_ID = "9000"

# A realistic serial port config response for
# GET /vcenter/vm/{vm}/hardware/serial/{port}.
SERIAL_CONFIG = {
    "label": "Serial port 1",
    "backing": {
        "type": "FILE",
        "file": "[datastore1] serial/port1.log",
    },
    "state": "CONNECTED",
    "yield_on_poll": False,
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


def test_ensure_present_creates_serial_port(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test that omitting port creates a new serial port and returns its id."""
    mock_client.post.return_value = _response(201, PORT_ID)

    module_args.update(
        {
            "state": "present",
            "vm": VM_ID,
            "backing": {
                "type": "FILE",
                "file": "[datastore1] serial/port1.log",
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

    # A create must never issue a GET (the port id is unknown), only a POST.
    mock_client.get.assert_not_called()
    mock_client.post.assert_called_once()
    call_args = mock_client.post.call_args
    assert call_args[0][0] == "/vcenter/vm/vm-1001/hardware/serial"
    assert call_args[1]["data"] == {
        "backing": {
            "type": "FILE",
            "file": "[datastore1] serial/port1.log",
        },
        "start_connected": True,
        "allow_guest_control": True,
    }


def test_ensure_present_creates_network_backed_port(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test creating a network-backed serial port sends the nested backing."""
    mock_client.post.return_value = _response(201, PORT_ID)

    module_args.update(
        {
            "state": "present",
            "vm": VM_ID,
            "backing": {
                "type": "NETWORK_SERVER",
                "network_location": "telnet://:12345",
            },
            "yield_on_poll": True,
        }
    )
    _, result = _run_module(  # pylint: disable=disallowed-name
        patch_create_client, patch_ansible_module, mock_client, module_args
    )

    assert result["changed"] is True
    assert result["id"] == PORT_ID
    mock_client.post.assert_called_once()
    call_args = mock_client.post.call_args
    assert call_args[1]["data"] == {
        "yield_on_poll": True,
        "backing": {
            "type": "NETWORK_SERVER",
            "network_location": "telnet://:12345",
        },
    }


# ============================================================================
# Test state=present - UPDATE
# ============================================================================


def test_ensure_present_updates_existing_port(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test updating an existing serial port sends only the changed field."""
    mock_client.get.return_value = _response(200, SERIAL_CONFIG)
    mock_client.patch.return_value = _response(204, None)

    module_args.update(
        {
            "state": "present",
            "vm": VM_ID,
            "port": PORT_ID,
            "allow_guest_control": False,
        }
    )
    mock_module, result = _run_module(
        patch_create_client, patch_ansible_module, mock_client, module_args
    )

    mock_module.exit_json.assert_called_once()
    assert result["changed"] is True
    assert result["id"] == PORT_ID
    assert result["diff"]["allow_guest_control"] == {"before": True, "after": False}
    mock_client.patch.assert_called_once()
    call_args = mock_client.patch.call_args
    assert call_args[0][0] == "/vcenter/vm/vm-1001/hardware/serial/9000"
    assert call_args[1]["data"] == {"allow_guest_control": False}


def test_ensure_present_no_changes(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """
    Test no changes when the requested settings already match the current
    state (idempotent). Read-only fields reported by the API must not register
    as a change because only the keys the user specified are compared.
    """
    mock_client.get.return_value = _response(200, SERIAL_CONFIG)

    module_args.update(
        {
            "state": "present",
            "vm": VM_ID,
            "port": PORT_ID,
            "yield_on_poll": False,
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


def test_ensure_absent_deletes_existing_port(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test deleting an existing serial port issues a DELETE."""
    mock_client.get.return_value = _response(200, SERIAL_CONFIG)
    mock_client.delete.return_value = _response(204, None)

    module_args.update(
        {
            "state": "absent",
            "vm": VM_ID,
            "port": PORT_ID,
        }
    )
    mock_module, result = _run_module(
        patch_create_client, patch_ansible_module, mock_client, module_args
    )

    mock_module.exit_json.assert_called_once()
    assert result["changed"] is True
    assert result["id"] == PORT_ID
    mock_client.delete.assert_called_once()
    call_args = mock_client.delete.call_args
    assert call_args[0][0] == "/vcenter/vm/vm-1001/hardware/serial/9000"


def test_ensure_absent_already_absent(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test deleting a serial port that does not exist is a no-op (idempotent)."""
    mock_client.get.return_value = _response(404, None)

    module_args.update(
        {
            "state": "absent",
            "vm": VM_ID,
            "port": "9999",
        }
    )
    _, result = _run_module(  # pylint: disable=disallowed-name
        patch_create_client, patch_ansible_module, mock_client, module_args
    )

    assert result["changed"] is False
    mock_client.delete.assert_not_called()


# ============================================================================
# Test state=connect / state=disconnect - ACTIONS
# ============================================================================


def test_connect_action(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test the connect action POSTs to the item endpoint with action=connect."""
    mock_client.post.return_value = _response(204, None)

    module_args.update(
        {
            "state": "connect",
            "vm": VM_ID,
            "port": PORT_ID,
        }
    )
    mock_module, result = _run_module(
        patch_create_client, patch_ansible_module, mock_client, module_args
    )

    mock_module.exit_json.assert_called_once()
    # Actions are not idempotent: they always report changed.
    assert result["changed"] is True
    assert result["id"] == PORT_ID
    mock_client.post.assert_called_once()
    call_args = mock_client.post.call_args
    assert (
        call_args[1]["path"]
        == "/vcenter/vm/vm-1001/hardware/serial/9000?action=connect"
    )


def test_disconnect_action(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Test the disconnect action POSTs with action=disconnect."""
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
    call_args = mock_client.post.call_args
    assert (
        call_args[1]["path"]
        == "/vcenter/vm/vm-1001/hardware/serial/9000?action=disconnect"
    )


# ============================================================================
# Test Check Mode
# ============================================================================


class TestCheckMode:
    """Test check mode behavior: report a change but make no write HTTP call."""

    def test_create_check_mode(
        self, patch_create_client, patch_ansible_module, mock_client, module_args
    ):
        """Test creating a serial port in check mode issues no POST."""
        module_args.update(
            {
                "state": "present",
                "vm": VM_ID,
                "backing": {"type": "HOST_DEVICE", "host_device": "/dev/ttyS0"},
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
        """Test updating a serial port in check mode issues no PATCH."""
        mock_client.get.return_value = _response(200, SERIAL_CONFIG)

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
        """Test deleting a serial port in check mode issues no DELETE."""
        mock_client.get.return_value = _response(200, SERIAL_CONFIG)

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
        """Test the connect action in check mode issues no POST."""
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
        """Test that MOID parameter hints are the vm and port identifiers."""
        assert module_under_test.MOID_PARAMETER_HINTS == ["vm", "port"]

    def test_list_endpoint(self):
        """Test that the list API endpoint is correct."""
        assert module_under_test.LIST_ENDPOINT == "/vcenter/vm/{vm}/hardware/serial"

    def test_item_endpoint(self):
        """Test that the item API endpoint is correct."""
        assert (
            module_under_test.ITEM_ENDPOINT == "/vcenter/vm/{vm}/hardware/serial/{port}"
        )


# ============================================================================
# Test OperationConfig Definitions
# ============================================================================


class TestOperationConfigs:
    """Test the module's operation config definitions."""

    def test_get_operation(self):
        """Test the GET operation config targets the item endpoint."""
        assert module_under_test.GET_OPERATION.http_method == "get"
        assert (
            module_under_test.GET_OPERATION.uri
            == "/vcenter/vm/{vm}/hardware/serial/{port}"
        )

    def test_list_operation(self):
        """Test the LIST operation config targets the collection endpoint."""
        assert module_under_test.LIST_OPERATION.http_method == "get"
        assert (
            module_under_test.LIST_OPERATION.uri == "/vcenter/vm/{vm}/hardware/serial"
        )

    def test_create_operation_method(self):
        """Test the CREATE operation uses POST on the collection endpoint."""
        assert module_under_test.CREATE_OPERATION.http_method == "post"
        assert (
            module_under_test.CREATE_OPERATION.uri == "/vcenter/vm/{vm}/hardware/serial"
        )

    def test_update_operation_method(self):
        """Test the UPDATE operation uses PATCH on the item endpoint."""
        assert module_under_test.UPDATE_OPERATION.http_method == "patch"
        assert (
            module_under_test.UPDATE_OPERATION.uri
            == "/vcenter/vm/{vm}/hardware/serial/{port}"
        )

    def test_delete_operation_method(self):
        """Test the DELETE operation uses DELETE on the item endpoint."""
        assert module_under_test.DELETE_OPERATION.http_method == "delete"
        assert (
            module_under_test.DELETE_OPERATION.uri
            == "/vcenter/vm/{vm}/hardware/serial/{port}"
        )

    def test_action_operations(self):
        """Test the connect/disconnect action configs POST to the item endpoint."""
        connect = module_under_test.ACTION_OPERATIONS["connect"]
        disconnect = module_under_test.ACTION_OPERATIONS["disconnect"]

        assert connect.http_method == "post"
        assert connect.uri == "/vcenter/vm/{vm}/hardware/serial/{port}?action=connect"
        assert disconnect.http_method == "post"
        assert (
            disconnect.uri
            == "/vcenter/vm/{vm}/hardware/serial/{port}?action=disconnect"
        )

    def test_create_build_path(self):
        """Test the CREATE operation interpolates the vm into the collection path."""
        path = module_under_test.CREATE_OPERATION.build_path(params={"vm": VM_ID})
        assert path == "/vcenter/vm/vm-1001/hardware/serial"

    def test_update_build_path(self):
        """Test the UPDATE operation interpolates the vm and port into the path."""
        path = module_under_test.UPDATE_OPERATION.build_path(
            params={"vm": VM_ID, "port": PORT_ID}
        )
        assert path == "/vcenter/vm/vm-1001/hardware/serial/9000"

    def test_create_build_body_nested(self):
        """Test the CREATE body carries set params (including nested backing)."""
        body = module_under_test.CREATE_OPERATION.build_body(
            params={
                "vm": VM_ID,
                "backing": {"type": "FILE", "file": "[ds] p.log"},
                "start_connected": True,
            }
        )
        assert body == {
            "backing": {"type": "FILE", "file": "[ds] p.log"},
            "start_connected": True,
        }

    def test_update_build_body_omits_unset(self):
        """Test the UPDATE body omits params the user did not set."""
        config = module_under_test.UPDATE_OPERATION

        assert config.build_body(params={"yield_on_poll": True}) == {
            "yield_on_poll": True
        }
        # Only path params provided -> empty body (not None, since a body_spec exists).
        assert config.build_body(params={"vm": VM_ID, "port": PORT_ID}) == {}


# ============================================================================
# Test Argument Spec
# ============================================================================


class TestArgumentSpec:
    """Test the module argument specification."""

    def test_state_parameter(self):
        """Test that the state parameter supports all four states."""
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

    def test_optional_scalar_parameters(self):
        """Test the optional boolean settings and their types."""
        spec = module_under_test.create_module_argument_spec()

        assert spec["yield_on_poll"]["type"] == "bool"
        assert spec["start_connected"]["type"] == "bool"
        assert spec["allow_guest_control"]["type"] == "bool"

        for name in ("yield_on_poll", "start_connected", "allow_guest_control"):
            assert spec[name].get("required", False) is False

    def test_backing_suboptions(self):
        """Test the backing dict parameter and its suboptions."""
        spec = module_under_test.create_module_argument_spec()

        assert spec["backing"]["type"] == "dict"
        options = spec["backing"]["options"]
        assert options["type"]["type"] == "str"
        assert options["type"]["choices"] == [
            "FILE",
            "HOST_DEVICE",
            "PIPE_SERVER",
            "PIPE_CLIENT",
            "NETWORK_SERVER",
            "NETWORK_CLIENT",
        ]
        assert options["file"]["type"] == "str"
        assert options["host_device"]["type"] == "str"
        assert options["pipe"]["type"] == "str"
        assert options["no_rx_loss"]["type"] == "bool"
        assert options["network_location"]["type"] == "str"
        assert options["proxy"]["type"] == "str"
