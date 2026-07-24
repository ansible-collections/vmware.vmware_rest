# -*- coding: utf-8 -*-
# Copyright: (c) 2026, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import pytest

from ansible_collections.vmware.vmware_rest.plugins.module_utils._operation_configs import (
    OperationConfig,
)
from ansible_collections.vmware.vmware_rest.plugins.module_utils._errors import (
    RequiredParameterError,
    RequiredPathParameterError,
)


class TestOperationConfig:
    def test_operation_config_initialization(self):
        config = OperationConfig(
            name="get_resource_pool",
            uri="/vcenter/resource-pool/{resource_pool}",
            http_method="GET",
        )
        assert config.name == "get_resource_pool"
        assert config.uri == "/vcenter/resource-pool/{resource_pool}"
        assert config.http_method == "get"

    def test_build_path_no_placeholders(self):
        config = OperationConfig(
            name="list",
            uri="/vcenter/resource-pool",
            http_method="get",
        )
        path = config.build_path({})
        assert path == "/vcenter/resource-pool"

    def test_build_path_single_placeholder(self):
        config = OperationConfig(
            name="get",
            uri="/vcenter/resource-pool/{resource_pool}",
            http_method="get",
        )
        params = {"resource_pool": "resgroup-1009"}
        path = config.build_path(params)
        assert path == "/vcenter/resource-pool/resgroup-1009"

    def test_build_path_multiple_placeholders(self):
        config = OperationConfig(
            name="get",
            uri="/vcenter/datacenter/{datacenter}/vm/{vm}",
            http_method="get",
        )
        params = {"datacenter": "datacenter-1", "vm": "vm-123"}
        path = config.build_path(params)
        assert path == "/vcenter/datacenter/datacenter-1/vm/vm-123"

    def test_build_path_missing_required_param_raises(self):
        config = OperationConfig(
            name="get",
            uri="/vcenter/resource-pool/{resource_pool}",
            http_method="get",
        )
        params = {}
        with pytest.raises(RequiredPathParameterError) as exc:
            config.build_path(params)
        assert exc.value.param_name == "resource_pool"
        assert exc.value.uri == "/vcenter/resource-pool/{resource_pool}"
        assert exc.value.operation == "get"
        assert exc.value.http_method == "get"

    def test_build_query_no_spec_returns_none(self):
        config = OperationConfig(
            name="get",
            uri="/vcenter/resource-pool/{resource_pool}",
            http_method="get",
        )
        query = config.build_query({})
        assert query is None

    def test_build_query_with_optional_params(self):
        config = OperationConfig(
            name="list",
            uri="/vcenter/resource-pool",
            http_method="get",
            query_spec={
                "names": {"required": False},
                "clusters": {"required": False},
            },
        )
        params = {"names": ["pool1", "pool2"]}
        query = config.build_query(params)
        assert query == {"names": ["pool1", "pool2"]}

    def test_build_query_excludes_none_values(self):
        config = OperationConfig(
            name="list",
            uri="/vcenter/resource-pool",
            http_method="get",
            query_spec={
                "names": {"required": False},
                "clusters": {"required": False},
            },
        )
        params = {"names": ["pool1"], "clusters": None}
        query = config.build_query(params)
        assert query == {"names": ["pool1"]}

    def test_build_query_with_required_param(self):
        config = OperationConfig(
            name="list",
            uri="/vcenter/resource-pool",
            http_method="get",
            query_spec={
                "datacenter": {"required": True},
            },
        )
        params = {"datacenter": "datacenter-1"}
        query = config.build_query(params)
        assert query == {"datacenter": "datacenter-1"}

    def test_build_query_missing_required_param_raises(self):
        config = OperationConfig(
            name="list",
            uri="/vcenter/resource-pool",
            http_method="get",
            query_spec={
                "datacenter": {"required": True},
            },
        )
        params = {}
        with pytest.raises(RequiredParameterError) as exc:
            config.build_query(params)
        assert exc.value.param_name == "datacenter"
        assert exc.value.uri == "/vcenter/resource-pool"
        assert exc.value.operation == "list"

    def test_build_body_no_spec_returns_none(self):
        config = OperationConfig(
            name="get",
            uri="/vcenter/resource-pool/{resource_pool}",
            http_method="get",
        )
        body = config.build_body({})
        assert body is None

    def test_build_body_simple_params(self):
        config = OperationConfig(
            name="create",
            uri="/vcenter/resource-pool",
            http_method="post",
            body_spec={
                "name": {"required": True},
                "parent": {"required": True},
            },
        )
        params = {"name": "my_pool", "parent": "resgroup-8"}
        body = config.build_body(params)
        assert body == {"name": "my_pool", "parent": "resgroup-8"}

    def test_build_body_with_nested_subspec(self):
        config = OperationConfig(
            name="create",
            uri="/vcenter/resource-pool",
            http_method="post",
            body_spec={
                "name": {"required": True},
                "cpu_allocation": {
                    "required": False,
                    "subspec": {
                        "reservation": {"required": False},
                        "limit": {"required": False},
                    },
                },
            },
        )
        params = {
            "name": "my_pool",
            "cpu_allocation": {
                "reservation": 100,
                "limit": 500,
            },
        }
        body = config.build_body(params)
        assert body == {
            "name": "my_pool",
            "cpu_allocation": {
                "reservation": 100,
                "limit": 500,
            },
        }

    def test_build_body_with_deeply_nested_subspec(self):
        config = OperationConfig(
            name="create",
            uri="/vcenter/resource-pool",
            http_method="post",
            body_spec={
                "name": {"required": True},
                "cpu_allocation": {
                    "required": False,
                    "subspec": {
                        "reservation": {"required": False},
                        "shares": {
                            "required": False,
                            "subspec": {
                                "level": {"required": False},
                                "shares": {"required": False},
                            },
                        },
                    },
                },
            },
        )
        params = {
            "name": "my_pool",
            "cpu_allocation": {
                "reservation": 100,
                "shares": {
                    "level": "NORMAL",
                    "shares": 1000,
                },
            },
        }
        body = config.build_body(params)
        assert body == {
            "name": "my_pool",
            "cpu_allocation": {
                "reservation": 100,
                "shares": {
                    "level": "NORMAL",
                    "shares": 1000,
                },
            },
        }

    def test_build_body_partial_nested_data(self):
        config = OperationConfig(
            name="create",
            uri="/vcenter/resource-pool",
            http_method="post",
            body_spec={
                "name": {"required": True},
                "cpu_allocation": {
                    "required": False,
                    "subspec": {
                        "reservation": {"required": False},
                        "limit": {"required": False},
                        "shares": {
                            "required": False,
                            "subspec": {
                                "level": {"required": False},
                                "shares": {"required": False},
                            },
                        },
                    },
                },
            },
        )
        params = {
            "name": "my_pool",
            "cpu_allocation": {
                "reservation": 100,
                "shares": {
                    "level": "NORMAL",
                },
            },
        }
        body = config.build_body(params)
        assert body == {
            "name": "my_pool",
            "cpu_allocation": {
                "reservation": 100,
                "shares": {
                    "level": "NORMAL",
                },
            },
        }

    def test_build_body_excludes_none_values(self):
        config = OperationConfig(
            name="update",
            uri="/vcenter/resource-pool/{resource_pool}",
            http_method="patch",
            body_spec={
                "name": {"required": False},
                "cpu_allocation": {"required": False},
            },
        )
        params = {"name": "updated_pool", "cpu_allocation": None}
        body = config.build_body(params)
        assert body == {"name": "updated_pool"}

    def test_build_body_missing_required_param_raises(self):
        config = OperationConfig(
            name="create",
            uri="/vcenter/resource-pool",
            http_method="post",
            body_spec={
                "name": {"required": True},
            },
        )
        params = {}
        with pytest.raises(RequiredParameterError) as exc:
            config.build_body(params)
        assert exc.value.param_name == "name"

    def test_build_body_missing_nested_optional(self):
        config = OperationConfig(
            name="create",
            uri="/vcenter/resource-pool",
            http_method="post",
            body_spec={
                "name": {"required": True},
                "cpu_allocation": {
                    "required": False,
                    "subspec": {
                        "reservation": {"required": False},
                    },
                },
            },
        )
        params = {"name": "my_pool"}
        body = config.build_body(params)
        assert body == {"name": "my_pool"}

    def test_build_body_empty_nested_dict(self):
        config = OperationConfig(
            name="create",
            uri="/vcenter/resource-pool",
            http_method="post",
            body_spec={
                "name": {"required": True},
                "cpu_allocation": {
                    "required": False,
                    "subspec": {
                        "reservation": {"required": False},
                    },
                },
            },
        )
        params = {"name": "my_pool", "cpu_allocation": {}}
        body = config.build_body(params)
        assert body == {"name": "my_pool", "cpu_allocation": {}}

    def test_build_body_multiple_parallel_nested(self):
        config = OperationConfig(
            name="create",
            uri="/vcenter/resource-pool",
            http_method="post",
            body_spec={
                "name": {"required": True},
                "cpu_allocation": {
                    "required": False,
                    "subspec": {
                        "reservation": {"required": False},
                    },
                },
                "memory_allocation": {
                    "required": False,
                    "subspec": {
                        "reservation": {"required": False},
                    },
                },
            },
        )
        params = {
            "name": "my_pool",
            "cpu_allocation": {"reservation": 100},
            "memory_allocation": {"reservation": 200},
        }
        body = config.build_body(params)
        assert body == {
            "name": "my_pool",
            "cpu_allocation": {"reservation": 100},
            "memory_allocation": {"reservation": 200},
        }

    def test_build_query_with_module_param_remapping(self):
        config = OperationConfig(
            name="list",
            uri="/vcenter/datacenter",
            http_method="get",
            query_spec={
                "names": {"required": False, "module_param": "name"},
            },
        )
        params = {"name": "my_datacenter"}
        query = config.build_query(params)
        assert query == {"names": "my_datacenter"}

    def test_build_query_module_param_not_provided(self):
        config = OperationConfig(
            name="list",
            uri="/vcenter/datacenter",
            http_method="get",
            query_spec={
                "names": {"required": False, "module_param": "name"},
            },
        )
        params = {}
        query = config.build_query(params)
        assert query == {}

    def test_build_query_module_param_none_excluded(self):
        config = OperationConfig(
            name="list",
            uri="/vcenter/datacenter",
            http_method="get",
            query_spec={
                "names": {"required": False, "module_param": "name"},
                "folders": {"required": False, "module_param": "folder"},
            },
        )
        params = {"name": "my_dc", "folder": None}
        query = config.build_query(params)
        assert query == {"names": "my_dc"}

    def test_build_query_module_param_falls_back_to_param_key(self):
        config = OperationConfig(
            name="list",
            uri="/vcenter/datacenter",
            http_method="get",
            query_spec={
                "datacenter": {"required": False},
            },
        )
        params = {"datacenter": "datacenter-1"}
        query = config.build_query(params)
        assert query == {"datacenter": "datacenter-1"}

    def test_build_body_with_module_param_remapping(self):
        config = OperationConfig(
            name="create",
            uri="/vcenter/datacenter",
            http_method="post",
            body_spec={
                "api_name": {"required": True, "module_param": "name"},
            },
        )
        params = {"name": "my_datacenter"}
        body = config.build_body(params)
        assert body == {"api_name": "my_datacenter"}

    def test_build_body_module_param_required_raises(self):
        config = OperationConfig(
            name="create",
            uri="/vcenter/datacenter",
            http_method="post",
            body_spec={
                "api_name": {"required": True, "module_param": "name"},
            },
        )
        params = {}
        with pytest.raises(RequiredParameterError) as exc:
            config.build_body(params)
        assert exc.value.param_name == "name"
