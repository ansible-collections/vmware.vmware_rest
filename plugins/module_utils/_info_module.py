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
        list_operation_config: OperationConfig,
    ):
        super().__init__(
            module=module,
            moid_parameter_hints=moid_parameter_hints,
            get_operation_config=get_operation_config,
            list_operation_config=list_operation_config,
        )

    def get_resource_info(self) -> dict:
        """
        Gather infomation about one or more resources, based on the module parameters.
        Always returns a list of dictionaries.
        """
        result = []
        try:
            # prefer the item endpoint. It might not be possible to use the item endpoint,
            # and if that is the case we need to use the list endpoint
            resource = self._perform_get_operation()
            if resource:
                result = [resource]
        except RequiredPathParameterError:
            result = self._list_resource_details()

        return self.normalize_info_results(result)

    def _list_resource_details(self) -> list:
        result = []
        http_method = getattr(self.client, self.get_operation_config.http_method)
        for resource in self._perform_list_operation():
            path = self.get_operation_config.build_path(
                params={**self.params, **resource}
            )
            response = http_method(path)
            if response and response.status != 404:
                result.append(response.json)
            else:
                self.module.fail_json(
                    "Error while looking up more details about a resource: %s" % path
                )
        return result

    def normalize_info_results(self, query_results: list) -> dict:
        """
        Takes a query result from an INFO module query, and formats it
        to be consistent with expected INFO module outputs.
        Always returns info (list[dict]) and value in the result.
        - If the module has a moid_attribute_name (it could be None) and queried a single object,
          add id (str) to the return and value is a single dict.
        - If the results contain 0 or many items, value is a list[dict].
        """
        if not isinstance(query_results, list):
            self.module.fail_json(
                "Module got unexpected non-list results from an INFO endpoint. This is an unsupported response, and a bug.",
                result_type=str(type(query_results)),
            )

        results = {}

        if len(query_results) == 1:
            resource_id = self._get_moid_attribute_value_from_resource(
                resource=query_results[0]
            )
            if resource_id:
                results["id"] = resource_id
            results["value"] = query_results[0]

        else:
            results["value"] = query_results

        results["info"] = query_results

        return results
