# -*- coding: utf-8 -*-
# Copyright: (c) 2026, Eco Ansible Content Team <@eco-ansible-content>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ._module_base import (
    VmwareRestModuleBase,
)
from ._errors import RequiredPathParameterError
from ._operation_configs import OperationConfig


class VmwareRestInfoModuleBase(VmwareRestModuleBase):
    def __init__(
        self,
        module,
        moid_parameter_hints: list,
        get_operation_config: OperationConfig,
        list_operation_config: OperationConfig = None,
    ):
        super().__init__(
            module=module,
            moid_parameter_hints=moid_parameter_hints,
            get_operation_config=get_operation_config,
            list_operation_config=list_operation_config,
        )

    def get_resource_info(self) -> dict:
        """
        Gather information about one or more resources, based on the module parameters.
        Uses the get endpoint when possible, otherwise falls back to the list endpoint.
        """
        try:
            resource = self._perform_get_operation()
            return self.normalize_info_results(
                query_results=[resource] if resource else [],
                single_resource=True,
            )
        except RequiredPathParameterError:
            if self.list_operation_config is None:
                raise

        return self.normalize_info_results(
            query_results=self._list_resource_details(),
            single_resource=False,
        )

    def _list_resource_details(self) -> list:
        result = []
        http_method = getattr(self.client, self.get_operation_config.http_method)
        for resource in self._perform_list_operation():
            path = self.get_operation_config.build_path(
                params={**self.params, **resource}
            )
            response = http_method(path)
            if not response:
                self.module.fail_json(
                    "Error while looking up more details about a resource: %s" % path
                )

            if response.status == 404:
                self.module.warn(
                    "Resource at %s could not be queried. It may have been deleted or modified during this operation."
                    % path
                )
                continue

            result.append({**resource, **response.json})
        return result

    def normalize_info_results(
        self, query_results: list, single_resource: bool = False
    ) -> dict:
        """
        Takes a query result from an INFO module query, and formats it
        to be consistent with expected INFO module outputs.
        Always returns info (list[dict]) and value in the result.
        - info is always a list[dict], regardless of the query type.
        - value preserves the shape of the query: a dict when a single resource
          was fetched by ID (single_resource=True), a list[dict] when listing.
        - id (str) is added when a single resource was fetched and has a
          recognizable MOID attribute.
        """
        if not isinstance(query_results, list):
            self.module.fail_json(
                "Module got unexpected non-list results from an INFO endpoint. This is an unsupported response, and a bug.",
                result_type=str(type(query_results)),
            )

        results = {"info": query_results}

        if single_resource:
            results["value"] = query_results[0] if query_results else {}
            if query_results:
                resource_id = self._get_moid_attribute_value_from_resource(
                    resource=query_results[0]
                )
                if resource_id:
                    results["id"] = resource_id
        else:
            results["value"] = query_results

        return results
