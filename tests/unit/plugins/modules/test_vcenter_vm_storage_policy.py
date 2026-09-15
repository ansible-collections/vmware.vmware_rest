# -*- coding: utf-8 -*-
# Copyright: (c) 2026, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Unit tests for vcenter_vm_storage_policy module.

Tests validate the CRUD module behavior end-to-end by driving ``main()`` with a
mocked ``AnsibleModule`` and HTTP client, mirroring the pattern used by the other
CRUD module tests (e.g. test_vcenter_datacenter.py) so the module file itself is
exercised for coverage.

This module is an unusual CRUD module: the storage policy is a per-VM singleton
addressed by the ``vm`` MOID. It only supports GET and UPDATE operations (there
is no create, delete, or list), so the tests focus on the update/idempotency
paths and on the "resource cannot be created" behavior.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import pytest
from unittest.mock import MagicMock, patch

from ansible_collections.vmware.vmware_rest.plugins.module_utils._errors import (
    VmwareModuleError,
)
from ansible_collections.vmware.vmware_rest.plugins.modules import (
    vcenter_vm_storage_policy as module_under_test,
)

from ...common.utils import (
    AnsibleExitJson,
    AnsibleFailJson,
    exit_json,
    fail_json,
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


def _build_module(patch_ansible_module, mock_module, module_args, check_mode=False):
    """Wire up the mocked AnsibleModule with params and exit/fail handlers."""
    patch_ansible_module.return_value = mock_module
    mock_module.params = set_module_args(module_args)
    mock_module.exit_json.side_effect = exit_json
    mock_module.fail_json.side_effect = fail_json
    mock_module.check_mode = check_mode
    return mock_module


# ============================================================================
# Test UPDATE Operations
# ============================================================================


def test_update_vm_home(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Update the vm_home storage policy when a change is detected.

    The GET endpoint reports the current vm_home policy as a bare policy-MOID
    string, while the desired body is a {type, policy} dict.
    """
    patch_create_client.return_value = mock_client
    _build_module(
        patch_ansible_module,
        MagicMock(),
        {
            **module_args,
            "state": "present",
            "vm": "vm-1",
            "vm_home": {"type": "USE_SPECIFIED_POLICY", "policy": "policy-new"},
        },
    )

    mock_client.get.return_value = _response(200, {"vm_home": "policy-old"})
    mock_client.patch.return_value = _response(200, {})

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    result = exc.value.kwargs
    assert result["changed"] is True
    assert result["id"] == "vm-1"
    assert result["diff"]["vm_home"] == {
        "before": "policy-old",
        "after": {"type": "USE_SPECIFIED_POLICY", "policy": "policy-new"},
    }
    mock_client.patch.assert_called_once()


def test_update_disks(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Update a per-disk storage policy when a change is detected.

    The GET endpoint reports the current disks as a map keyed by disk MOID whose
    values are bare policy-MOID strings, while the desired body maps each disk to
    a {type, policy} dict.
    """
    patch_create_client.return_value = mock_client
    _build_module(
        patch_ansible_module,
        MagicMock(),
        {
            **module_args,
            "state": "present",
            "vm": "vm-1",
            "disks": {
                "disk-1": {"type": "USE_SPECIFIED_POLICY", "policy": "policy-new"}
            },
        },
    )

    mock_client.get.return_value = _response(200, {"disks": {"disk-1": "policy-old"}})
    mock_client.patch.return_value = _response(200, {})

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    result = exc.value.kwargs
    assert result["changed"] is True
    assert result["id"] == "vm-1"
    assert "disks" in result["diff"]
    mock_client.patch.assert_called_once()


def test_no_change_when_nothing_requested(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """The only idempotent no-op path: neither vm_home nor disks is supplied, so
    the desired update body is empty, nothing is diffed, and no PATCH is issued.
    """
    patch_create_client.return_value = mock_client
    _build_module(
        patch_ansible_module,
        MagicMock(),
        {**module_args, "state": "present", "vm": "vm-1"},
    )

    mock_client.get.return_value = _response(
        200, {"vm_home": "policy-existing", "disks": {"disk-1": "policy-existing"}}
    )

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    result = exc.value.kwargs
    assert result["changed"] is False
    assert result["id"] == "vm-1"
    assert result["diff"] == {}
    mock_client.patch.assert_not_called()


def test_vm_home_always_changes(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """Supplying vm_home is never idempotent: the GET reports the current policy as
    a bare policy-MOID string while the desired body is a {type, policy} dict, so
    the two can never compare equal even when the effective policy is unchanged.
    """
    patch_create_client.return_value = mock_client
    _build_module(
        patch_ansible_module,
        MagicMock(),
        {
            **module_args,
            "state": "present",
            "vm": "vm-1",
            "vm_home": {"type": "USE_SPECIFIED_POLICY", "policy": "policy-existing"},
        },
    )

    mock_client.get.return_value = _response(200, {"vm_home": "policy-existing"})
    mock_client.patch.return_value = _response(200, {})

    with pytest.raises(AnsibleExitJson) as exc:
        module_under_test.main()

    result = exc.value.kwargs
    assert result["changed"] is True
    assert result["diff"]["vm_home"]["before"] == "policy-existing"
    mock_client.patch.assert_called_once()


def test_resource_not_found_cannot_create(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """When the VM's storage policy cannot be resolved (404) and the module has no
    create operation, it fails rather than attempting a create.
    """
    patch_create_client.return_value = mock_client
    _build_module(
        patch_ansible_module,
        MagicMock(),
        {**module_args, "state": "present", "vm": "vm-missing"},
    )

    mock_client.get.return_value = _response(404, None)

    with pytest.raises(AnsibleFailJson):
        module_under_test.main()

    mock_client.post.assert_not_called()
    mock_client.patch.assert_not_called()


# ============================================================================
# Test Check Mode
# ============================================================================


class TestCheckMode:
    """Test check mode behavior."""

    def test_update_check_mode(
        self, patch_create_client, patch_ansible_module, mock_client, module_args
    ):
        """Updating the storage policy in check mode reports the change without
        issuing the PATCH request.
        """
        patch_create_client.return_value = mock_client
        _build_module(
            patch_ansible_module,
            MagicMock(),
            {
                **module_args,
                "state": "present",
                "vm": "vm-1",
                "vm_home": {"type": "USE_SPECIFIED_POLICY", "policy": "policy-new"},
            },
            check_mode=True,
        )

        mock_client.get.return_value = _response(200, {"vm_home": "policy-old"})

        with pytest.raises(AnsibleExitJson) as exc:
            module_under_test.main()

        result = exc.value.kwargs
        assert result["changed"] is True
        assert result["diff"]["vm_home"] == {
            "before": "policy-old",
            "after": {"type": "USE_SPECIFIED_POLICY", "policy": "policy-new"},
        }
        mock_client.patch.assert_not_called()


# ============================================================================
# Test State Routing
# ============================================================================


def test_unsupported_state_fails(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """A state other than 'present' is rejected with an explanatory failure."""
    patch_create_client.return_value = mock_client
    _build_module(
        patch_ansible_module,
        MagicMock(),
        {**module_args, "state": "absent", "vm": "vm-1"},
    )

    with pytest.raises(AnsibleFailJson) as exc:
        module_under_test.main()

    assert "Unsupported state" in exc.value.kwargs["msg"]
    mock_client.patch.assert_not_called()


def test_vmware_module_error_is_handled(
    patch_create_client, patch_ansible_module, mock_client, module_args
):
    """A VmwareModuleError raised during processing is converted to fail_json."""
    patch_create_client.return_value = mock_client
    _build_module(
        patch_ansible_module,
        MagicMock(),
        {**module_args, "state": "present", "vm": "vm-1"},
    )

    with patch.object(
        module_under_test.VmwareRestCrudModuleBase,
        "ensure_present",
        side_effect=VmwareModuleError("boom"),
    ):
        with pytest.raises(AnsibleFailJson) as exc:
            module_under_test.main()

    assert exc.value.kwargs["msg"] == "boom"


# ============================================================================
# Test Module Constants
# ============================================================================


class TestModuleConstants:
    """Test that module constants are correctly defined."""

    def test_moid_parameter_hints(self):
        assert module_under_test.MOID_PARAMETER_HINTS == ["vm"]

    def test_list_endpoint(self):
        assert module_under_test.LIST_ENDPOINT == ""

    def test_item_endpoint(self):
        assert module_under_test.ITEM_ENDPOINT == "/vcenter/vm/{vm}/storage/policy"


# ============================================================================
# Test Argument Spec
# ============================================================================


class TestArgumentSpec:
    """Test the module argument specification."""

    def test_create_module_argument_spec_has_connection_params(self):
        spec = module_under_test.create_module_argument_spec()

        assert "vcenter_hostname" in spec
        assert "vcenter_username" in spec
        assert "vcenter_password" in spec

    def test_create_module_argument_spec_state(self):
        spec = module_under_test.create_module_argument_spec()

        assert spec["state"]["type"] == "str"
        assert spec["state"]["choices"] == ["present"]
        assert spec["state"]["default"] == "present"

    def test_create_module_argument_spec_vm_required(self):
        spec = module_under_test.create_module_argument_spec()

        assert spec["vm"]["type"] == "str"
        assert spec["vm"]["required"] is True

    def test_create_module_argument_spec_disks(self):
        spec = module_under_test.create_module_argument_spec()

        assert spec["disks"]["type"] == "dict"

    def test_create_module_argument_spec_vm_home_suboptions(self):
        spec = module_under_test.create_module_argument_spec()

        assert spec["vm_home"]["type"] == "dict"
        suboptions = spec["vm_home"]["options"]
        assert suboptions["type"]["required"] is True
        assert suboptions["type"]["choices"] == [
            "USE_SPECIFIED_POLICY",
            "USE_DEFAULT_POLICY",
        ]
        assert suboptions["policy"]["type"] == "str"


# ============================================================================
# Test OperationConfig (using the module's actual configs)
# ============================================================================


class TestOperationConfig:
    """Exercise the operation configs defined by the module."""

    def test_get_operation_build_path(self):
        path = module_under_test.GET_OPERATION.build_path({"vm": "vm-1"})

        assert path == "/vcenter/vm/vm-1/storage/policy"

    def test_update_operation_build_body_omits_unset_optionals(self):
        body = module_under_test.UPDATE_OPERATION.build_body(
            {
                "vm": "vm-1",
                "vm_home": {"type": "USE_SPECIFIED_POLICY", "policy": "policy-1"},
            }
        )

        assert body == {
            "vm_home": {"type": "USE_SPECIFIED_POLICY", "policy": "policy-1"},
        }
        assert "disks" not in body
