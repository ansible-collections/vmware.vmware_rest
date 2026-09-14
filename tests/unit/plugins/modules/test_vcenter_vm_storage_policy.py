# -*- coding: utf-8 -*-
# Copyright: (c) 2026, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Unit tests for vcenter_vm_storage_policy module.

Tests validate the CRUD module behavior using the OperationConfig-based
architecture with mocked HTTP clients.

This module is an unusual CRUD module: the storage policy is a per-VM
singleton addressed by the ``vm`` MOID. It only supports GET and UPDATE
operations (there is no create, delete, or list), so the tests focus on
the update/idempotency paths and on the "resource cannot be created"
behavior.
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

from ...common.utils import CONNECTION_PARAMS, fail_json, AnsibleFailJson

ITEM_ENDPOINT = "/vcenter/vm/{vm}/storage/policy"


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
    Create CRUD module instance with vm storage policy operation configs.

    Note: mock_client is provided by conftest.py - do not redefine it.
    """
    get_operation = OperationConfig(
        name="get",
        uri=ITEM_ENDPOINT,
        http_method="GET",
    )

    update_operation = OperationConfig(
        name="update",
        uri=ITEM_ENDPOINT,
        http_method="PATCH",
        body_spec={
            "vm_home": {
                "required": False,
                "subspec": {
                    "type": {"required": False},
                    "policy": {"required": False},
                },
            },
            "disks": {"required": False},
        },
    )

    with patch(
        "ansible_collections.vmware.vmware_rest.plugins.module_utils._module_base.Client",
        return_value=mock_client,
    ):
        module = VmwareRestCrudModuleBase(
            module=mock_module,
            get_operation_config=get_operation,
            update_operation_config=update_operation,
            moid_parameter_hints=["vm"],
        )
        yield module


# ============================================================================
# ensure_present() Tests - UPDATE
# ============================================================================


def test_ensure_present_updates_vm_home(crud_module, mock_client):
    """
    Test updating the vm_home storage policy when a change is detected.

    The GET endpoint reports the current vm_home policy as a bare policy-MOID
    string, while the desired body is a {type, policy} dict.
    """
    crud_module.params["vm"] = "vm-1"
    crud_module.params["vm_home"] = {
        "type": "USE_SPECIFIED_POLICY",
        "policy": "policy-new",
    }

    existing_resource = {
        "vm_home": "policy-old",
    }

    with patch.object(
        crud_module, "_resolve_live_resource_context", return_value=existing_resource
    ):
        update_response = MagicMock()
        update_response.status = 200
        update_response.json = {}
        mock_client.patch.return_value = update_response

        result = crud_module.ensure_present()

    assert result["changed"] is True
    assert result["id"] == "vm-1"
    assert result["diff"]["vm_home"] == {
        "before": "policy-old",
        "after": {"type": "USE_SPECIFIED_POLICY", "policy": "policy-new"},
    }
    mock_client.patch.assert_called_once()


def test_ensure_present_updates_disks(crud_module, mock_client):
    """
    Test updating a per-disk storage policy when a change is detected.

    The GET endpoint reports the current disks as a map keyed by disk MOID whose
    values are bare policy-MOID strings, while the desired body maps each disk to
    a {type, policy} dict.
    """
    crud_module.params["vm"] = "vm-1"
    crud_module.params["disks"] = {
        "disk-1": {"type": "USE_SPECIFIED_POLICY", "policy": "policy-new"},
    }

    existing_resource = {
        "disks": {"disk-1": "policy-old"},
    }

    with patch.object(
        crud_module, "_resolve_live_resource_context", return_value=existing_resource
    ):
        update_response = MagicMock()
        update_response.status = 200
        update_response.json = {}
        mock_client.patch.return_value = update_response

        result = crud_module.ensure_present()

    assert result["changed"] is True
    assert result["id"] == "vm-1"
    assert "disks" in result["diff"]
    mock_client.patch.assert_called_once()


def test_ensure_present_no_changes_when_nothing_requested(crud_module, mock_client):
    """
    The only idempotent no-op path: neither vm_home nor disks is supplied, so
    the desired update body is empty, nothing is diffed, and no PATCH is issued.

    A no-op is impossible whenever vm_home or disks *is* supplied, because the
    GET reports those as bare policy-MOID strings while the desired body is a
    {type, policy} dict (see test_ensure_present_vm_home_always_changes).
    """
    crud_module.params["vm"] = "vm-1"

    existing_resource = {
        "vm_home": "policy-existing",
        "disks": {"disk-1": "policy-existing"},
    }

    with patch.object(
        crud_module, "_resolve_live_resource_context", return_value=existing_resource
    ):
        result = crud_module.ensure_present()

    assert result["changed"] is False
    assert result["id"] == "vm-1"
    assert result["diff"] == {}
    mock_client.patch.assert_not_called()


def test_ensure_present_vm_home_always_changes(crud_module, mock_client):
    """
    Supplying vm_home is never idempotent: the GET reports the current policy as
    a bare policy-MOID string while the desired body is a {type, policy} dict, so
    the two can never compare equal even when the effective policy is unchanged.
    Every run therefore registers a change and re-issues the PATCH.
    """
    crud_module.params["vm"] = "vm-1"
    crud_module.params["vm_home"] = {
        "type": "USE_SPECIFIED_POLICY",
        "policy": "policy-existing",
    }

    existing_resource = {
        "vm_home": "policy-existing",
    }

    with patch.object(
        crud_module, "_resolve_live_resource_context", return_value=existing_resource
    ):
        update_response = MagicMock()
        update_response.status = 200
        update_response.json = {}
        mock_client.patch.return_value = update_response

        result = crud_module.ensure_present()

    assert result["changed"] is True
    assert result["diff"]["vm_home"]["before"] == "policy-existing"
    mock_client.patch.assert_called_once()


def test_ensure_present_resource_not_found_cannot_create(crud_module, mock_client):
    """
    Test that when the VM's storage policy cannot be resolved and the module
    has no create operation, it fails rather than attempting a create.
    """
    crud_module.params["vm"] = "vm-missing"

    with patch.object(crud_module, "_resolve_live_resource_context", return_value={}):
        with pytest.raises(AnsibleFailJson):
            crud_module.ensure_present()

    mock_client.post.assert_not_called()
    mock_client.patch.assert_not_called()


# ============================================================================
# Check Mode Tests
# ============================================================================


def test_ensure_present_check_mode_update(crud_module, mock_client):
    """
    Test updating the storage policy in check mode reports the change without
    issuing the PATCH request.
    """
    crud_module.params["vm"] = "vm-1"
    crud_module.params["vm_home"] = {
        "type": "USE_SPECIFIED_POLICY",
        "policy": "policy-new",
    }
    crud_module.module.check_mode = True

    existing_resource = {
        "vm_home": "policy-old",
    }

    with patch.object(
        crud_module, "_resolve_live_resource_context", return_value=existing_resource
    ):
        result = crud_module.ensure_present()

    assert result["changed"] is True
    assert result["diff"]["vm_home"] == {
        "before": "policy-old",
        "after": {"type": "USE_SPECIFIED_POLICY", "policy": "policy-new"},
    }
    mock_client.patch.assert_not_called()


# ============================================================================
# Helper Method Tests
# ============================================================================


def test_resolve_live_resource_context_by_id(crud_module, mock_client):
    """
    Test resolving the live storage policy for a VM via the GET endpoint.
    """
    crud_module.params["vm"] = "vm-1"

    get_response = MagicMock()
    get_response.status = 200
    get_response.json = {
        "vm_home": {"type": "USE_DEFAULT_POLICY"},
        "disks": {"disk-1": {"type": "USE_DEFAULT_POLICY"}},
    }
    mock_client.get.return_value = get_response

    result = crud_module._resolve_live_resource_context()

    assert result is not None
    assert result["vm_home"] == {"type": "USE_DEFAULT_POLICY"}
    mock_client.get.assert_called_once_with(
        "/vcenter/vm/vm-1/storage/policy", query=None
    )


def test_resolve_live_resource_context_not_found(crud_module, mock_client):
    """
    Test resolving the storage policy for a VM that does not exist (404).
    """
    crud_module.params["vm"] = "vm-missing"

    get_response = MagicMock()
    get_response.status = 404
    mock_client.get.return_value = get_response

    result = crud_module._resolve_live_resource_context()

    assert result == {}


def test_calculate_resource_diff_simple(crud_module):
    """
    Test diff calculation with a simple changed value.
    """
    current = {"vm_home": {"type": "USE_DEFAULT_POLICY"}}
    desired = {"vm_home": {"type": "USE_SPECIFIED_POLICY"}}

    diff = crud_module._calculate_resource_diff(current, desired)

    assert diff == {
        "vm_home": {
            "before": {"type": "USE_DEFAULT_POLICY"},
            "after": {"type": "USE_SPECIFIED_POLICY"},
        }
    }


def test_calculate_resource_diff_nested(crud_module):
    """
    Test diff calculation with nested per-disk policy values.
    """
    current = {
        "disks": {"disk-1": {"type": "USE_SPECIFIED_POLICY", "policy": "p-old"}},
    }
    desired = {
        "disks": {"disk-1": {"type": "USE_SPECIFIED_POLICY", "policy": "p-new"}},
    }

    diff = crud_module._calculate_resource_diff(current, desired)

    assert diff == {
        "disks": {
            "before": {"disk-1": {"type": "USE_SPECIFIED_POLICY", "policy": "p-old"}},
            "after": {"disk-1": {"type": "USE_SPECIFIED_POLICY", "policy": "p-new"}},
        }
    }


def test_calculate_resource_diff_no_changes(crud_module):
    """
    Test diff calculation ignores API-only keys not present in the desired
    body (subset comparison).
    """
    current = {
        "vm_home": {"type": "USE_DEFAULT_POLICY", "policy": "read-only-value"},
    }
    desired = {"vm_home": {"type": "USE_DEFAULT_POLICY"}}

    diff = crud_module._calculate_resource_diff(current, desired)

    assert diff == {}


# ============================================================================
# OperationConfig Tests
# ============================================================================


def test_operation_config_build_path():
    """
    Test that OperationConfig builds the item path from the vm parameter.
    """
    config = OperationConfig(
        name="get",
        uri=ITEM_ENDPOINT,
        http_method="GET",
    )

    path = config.build_path({"vm": "vm-1"})

    assert path == "/vcenter/vm/vm-1/storage/policy"


def test_operation_config_build_body():
    """
    Test that the update OperationConfig builds a nested request body and
    omits optional params that were not provided.
    """
    config = OperationConfig(
        name="update",
        uri=ITEM_ENDPOINT,
        http_method="PATCH",
        body_spec={
            "vm_home": {
                "required": False,
                "subspec": {
                    "type": {"required": False},
                    "policy": {"required": False},
                },
            },
            "disks": {"required": False},
        },
    )

    params = {
        "vm": "vm-1",
        "vm_home": {"type": "USE_SPECIFIED_POLICY", "policy": "policy-1"},
    }
    body = config.build_body(params)

    assert body == {
        "vm_home": {"type": "USE_SPECIFIED_POLICY", "policy": "policy-1"},
    }
    assert "disks" not in body
