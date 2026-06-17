# -*- coding: utf-8 -*-
# Copyright: (c) 2026, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible.module_utils.basic import env_fallback

from ansible_collections.vmware.vmware_rest.plugins.module_utils._argument_spec import (
    connection_params_argument_spec,
)


def test_connection_params_argument_spec_returns_expected_keys():
    spec = connection_params_argument_spec()
    assert set(spec) == {
        "vcenter_hostname",
        "vcenter_username",
        "vcenter_password",
        "vcenter_port",
        "vcenter_validate_certs",
        "vcenter_rest_log_file",
        "session_timeout",
    }


def test_connection_params_argument_spec_required_credentials():
    spec = connection_params_argument_spec()
    for param in ("vcenter_hostname", "vcenter_username", "vcenter_password"):
        assert spec[param]["required"] is True
        assert spec[param]["type"] == "str"


def test_connection_params_argument_spec_password_is_no_log():
    spec = connection_params_argument_spec()
    assert spec["vcenter_password"]["no_log"] is True


def test_connection_params_argument_spec_optional_fields():
    spec = connection_params_argument_spec()
    assert spec["vcenter_port"]["required"] is False
    assert spec["vcenter_port"]["type"] == "int"
    assert spec["vcenter_validate_certs"]["required"] is False
    assert spec["vcenter_validate_certs"]["type"] == "bool"
    assert spec["vcenter_validate_certs"]["default"] is True
    assert spec["vcenter_rest_log_file"]["required"] is False
    assert spec["session_timeout"]["required"] is False
    assert spec["session_timeout"]["type"] == "float"


def test_connection_params_argument_spec_env_fallbacks():
    spec = connection_params_argument_spec()
    expected = {
        "vcenter_hostname": ["VMWARE_HOST"],
        "vcenter_username": ["VMWARE_USER"],
        "vcenter_password": ["VMWARE_PASSWORD"],
        "vcenter_port": ["VMWARE_PORT"],
        "vcenter_validate_certs": ["VMWARE_VALIDATE_CERTS"],
        "vcenter_rest_log_file": ["VMWARE_REST_LOG_FILE"],
        "session_timeout": ["VMWARE_SESSION_TIMEOUT"],
    }
    for param, env_vars in expected.items():
        fallback = spec[param]["fallback"]
        assert fallback[0] is env_fallback
        assert fallback[1] == env_vars
