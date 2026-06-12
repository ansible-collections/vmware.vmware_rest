# -*- coding: utf-8 -*-
# Copyright: (c) 2026, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible_collections.vmware.vmware_rest.plugins.module_utils._module_base import (
    find_summary_id,
    normalize_list_response,
    params_differ,
    payload_body_subset,
    values_equal,
)


def test_normalize_list_response_bare_list():
    assert normalize_list_response([{"id": "a"}]) == [{"id": "a"}]


def test_normalize_list_response_value_envelope():
    assert normalize_list_response({"value": [{"id": "a"}]}) == [{"id": "a"}]


def test_normalize_list_response_empty_envelope():
    assert normalize_list_response({"value": []}) == []


def test_values_equal_partial_dict():
    current = {"cpu_allocation": {"limit": 4000, "reservation": 1000}}
    desired = {"cpu_allocation": {"limit": 8000}}
    assert values_equal(current["cpu_allocation"], desired["cpu_allocation"]) is False


def test_params_differ_detects_change():
    current = {"name": "pool", "cpu_allocation": {"limit": 4000}}
    desired = {"cpu_allocation": {"limit": 8000}}
    assert params_differ(current, desired) is True


def test_params_differ_no_change():
    current = {"name": "pool", "cpu_allocation": {"limit": 8000}}
    desired = {"cpu_allocation": {"limit": 8000}}
    assert params_differ(current, desired) is False


def test_payload_body_subset_excludes_fields():
    body = {"name": "name", "parent": "parent", "cpu_allocation": "cpu_allocation"}
    assert payload_body_subset(body, exclude=("parent",)) == {
        "name": "name",
        "cpu_allocation": "cpu_allocation",
    }


def test_find_summary_id():
    summaries = [{"name": "my_pool", "resource_pool": "resgroup-1"}]
    assert find_summary_id(summaries, "my_pool", id_key="resource_pool") == "resgroup-1"
    assert find_summary_id(summaries, "missing", id_key="resource_pool") is None
