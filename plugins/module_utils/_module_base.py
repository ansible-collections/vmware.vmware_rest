# -*- coding: utf-8 -*-
# Copyright: (c) 2026, Eco Ansible Content Team <@eco-ansible-content>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from abc import ABC
from typing import Union

from ._client import (
    Client,
    ClientRequestErrorHandler,
)
from ._operation_configs import OperationConfig


class VmwareRestModuleBase(ABC):
    def __init__(
        self,
        module,
        moid_parameter_hints: list,
        get_operation_config: OperationConfig,
        list_operation_config: OperationConfig = None,
    ):
        self.module = module
        self.params = module.params
        self.client = self._create_client()

        self.moid_parameter_hints = ["resource_id"]
        if moid_parameter_hints:
            self.moid_parameter_hints.extend(moid_parameter_hints)
        self.get_operation_config = get_operation_config
        self.list_operation_config = list_operation_config

    def _create_client(self):
        """
        This creates an HTTP client for the module, which can be used to make API calls to the vCenter server.
        """
        return Client(
            error_handler=ClientRequestErrorHandler(self.module),
            host=self.module.params["vcenter_hostname"],
            username=self.module.params["vcenter_username"],
            password=self.module.params["vcenter_password"],
            port=self.module.params["vcenter_port"],
            validate_certs=self.module.params["vcenter_validate_certs"],
            timeout=self.module.params["session_timeout"],
            log_file=self.module.params["vcenter_rest_log_file"],
        )

    def _perform_list_operation(self):
        """GET a collection path and return a normalized list (empty on 404)."""
        path = self.list_operation_config.build_path(params=self.params)
        query = self.list_operation_config.build_query(params=self.params)
        http_method = getattr(self.client, self.list_operation_config.http_method)
        response = http_method(path, query=query)
        if response.status == 404:
            return []

        data = response.json
        if isinstance(data, list):
            return data

        if isinstance(data, dict):
            value = data.get("value", [])
            return value if isinstance(value, list) else []

        return []

    def _perform_get_operation(self, resource: dict = None) -> Union[dict, None]:
        """
        Get information about a singular resource
        Returns:
            None if nothing was found
            dict if resource was found
        """
        if resource:
            params = {**self.params, **resource}
        else:
            params = self.params
        path = self.get_operation_config.build_path(params=params)
        http_method = getattr(self.client, self.get_operation_config.http_method)
        response = http_method(path)
        if response.status == 404:
            return None

        return response.json

    def _get_moid_attribute_value_from_resource(self, resource):
        for moid_parameter_hint in self.moid_parameter_hints:
            moid_value = resource.get(moid_parameter_hint)
            if moid_value:
                return moid_value

        return None
