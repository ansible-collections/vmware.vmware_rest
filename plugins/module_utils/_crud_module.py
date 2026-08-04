# -*- coding: utf-8 -*-
# Copyright: (c) 2026, Eco Ansible Content Team <@eco-ansible-content>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from typing import Union

from ._module_base import (
    VmwareRestModuleBase,
)
from ._operation_configs import OperationConfig
from ._errors import RequiredPathParameterError


class VmwareRestCrudModuleBase(VmwareRestModuleBase):
    def __init__(
        self,
        module,
        moid_parameter_hints: list,
        get_operation_config: OperationConfig = None,
        list_operation_config: OperationConfig = None,
        create_operation_config: OperationConfig = None,
        delete_operation_config: OperationConfig = None,
        update_operation_config: OperationConfig = None,
        action_operations: dict = None,
    ):
        super().__init__(
            module,
            moid_parameter_hints=moid_parameter_hints,
            get_operation_config=get_operation_config,
            list_operation_config=list_operation_config,
        )
        self.create_operation_config = create_operation_config
        self.delete_operation_config = delete_operation_config
        self.update_operation_config = update_operation_config
        self.action_operations = (
            action_operations if action_operations is not None else {}
        )

    @staticmethod
    def _get_response_value(response):
        if not response.data:
            return {}
        return response.json

    def ensure_absent(self) -> dict:
        result = {"changed": False}
        resource = self._resolve_resource_context()
        if not resource:
            return result

        result["changed"] = True
        resource_id = self._get_moid_attribute_value_from_resource(resource=resource)
        result["id"] = resource_id

        path = self.delete_operation_config.build_path(
            params={**self.params, **resource}
        )
        query = self.delete_operation_config.build_query(params=self.params)
        http_operation = getattr(self.client, self.delete_operation_config.http_method)
        if not self.module.check_mode:
            response = http_operation(path, query=query)
            result["value"] = self._get_response_value(response)
        else:
            result["value"] = {}

        self._handle_errors_in_the_response(result)
        return result

    def _resolve_resource_context(self) -> Union[dict, None]:
        """
        Get a resource using the module params. Enrich the resulting dict with
        params or the resource summary to ensure the MOID is present.
        """
        if self.get_operation_config is None and self.list_operation_config is None:
            # This is an action only endpoint. There is no resource to lookup, and all the resource
            # context should be in the params
            return self.params

        # try to 'get' a resource, either using the resource ID from the params or a singleton api endpoint.
        # For example, get a specific VM or get the vCenter appliance
        try:
            resource = self._perform_get_operation()
            if resource:
                return {**self.params, **resource}
            else:
                return {}
        except RequiredPathParameterError:
            if not self.params.get("name") or not self.list_operation_config:
                raise

        # the get operation failed for whatever reason but we have a name parameter. So we can
        # use the list operation and look for the resource using the name
        for summary in self._perform_list_operation():
            if summary.get("name") == self.params.get("name"):
                resource = self._perform_get_operation(resource=summary)
                if resource is None:
                    self.module.warn(
                        "Resource with name %s could not be queried. It may have been deleted or modified during this operation."
                        % self.params.get("name")
                    )
                    continue
                return {**summary, **resource}

        return {}

    def perform_action(self) -> dict:
        """
        This is the primary entrypoint when state == some action (connect, disconnect, deploy).
        It will always attempt to perform the action as requested.
        """
        action_value = self.params["state"]
        action_operation = self.action_operations[action_value]
        result = {"changed": False, "id": ""}
        resource = self.params
        resource_id = self._get_moid_attribute_value_from_resource(resource)
        result["id"] = resource_id
        result["changed"] = True
        kwargs = {
            "path": action_operation.build_path(params={**self.params, **resource}),
            "data": action_operation.build_body(params=self.params),
            "query": action_operation.build_query(params=self.params),
        }
        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        http_method = getattr(self.client, action_operation.http_method)
        if not self.module.check_mode:
            response = http_method(**kwargs)
            result["value"] = self._get_response_value(response)
        else:
            result["value"] = {}

        self._handle_errors_in_the_response(result)
        return result

    def ensure_present(self) -> dict:
        """
        This is the primary routing entrypoint for state == present. It should call and route to
        self._create or self._update, as appropriate.
        Validation of MOIDs in the URI (does this resource even exist?) are left up to the vSphere API
        to simplify code. It can provide better information than we can in the current context.
        """
        result = {"changed": False, "id": ""}
        resource = self._resolve_resource_context()

        if not resource or resource is self.params:
            new_id, value = self._create()
            result["id"] = new_id
            result["value"] = value
            result["changed"] = True
        else:
            result["id"] = self._get_moid_attribute_value_from_resource(resource)
            diff, value = self._update_if_needed(resource)
            result["diff"] = diff
            result["value"] = value
            result["changed"] = bool(result["diff"])

        self._handle_errors_in_the_response(result)
        return result

    def _handle_errors_in_the_response(self, result):
        """
        Some API endpoints (content library) return 200s and have errors in the response.
        """
        if not result["value"] or "succeeded" not in result["value"]:
            return

        if result["value"]["succeeded"]:
            return

        try:
            # brittle attempt at maintaining backwards compat idempotency. This really is an edge case, in an edge case,
            # that would be inconvinient if broken.
            error_type = result["value"]["error"]["errors"][0]["error"]["error_type"]
            if error_type == "ALREADY_EXISTS":
                result["diff"] = {}
                result["changed"] = False
                return

        except (KeyError, IndexError):
            pass

        self.module.fail_json(
            "The API operation failed. See the response return value for more details.",
            response=result["value"],
        )

    def _create(self) -> tuple:
        path = self.create_operation_config.build_path(params=self.params)
        body = self.create_operation_config.build_body(params=self.params)
        http_method = getattr(self.client, self.create_operation_config.http_method)
        new_id = ""
        value = {}
        if not self.module.check_mode:
            response = http_method(path, data=body)
            value = self._get_response_value(response)
            new_id = value

        return new_id, value

    def _update_if_needed(self, resource: dict) -> tuple:
        if self.update_operation_config is None:
            return {}, {}

        desired_body = self.update_operation_config.build_body(params=self.params)
        diff = self._calculate_resource_diff(current=resource, desired=desired_body)
        if not diff:
            return {}, {}

        path = self.update_operation_config.build_path(
            params={**self.params, **resource}
        )
        update_method = getattr(self.client, self.update_operation_config.http_method)
        value = {}
        if not self.module.check_mode:
            response = update_method(path, data=desired_body)
            value = self._get_response_value(response)

        return diff, value

    def _calculate_resource_diff(self, current: dict, desired: dict) -> dict:
        """Return True when any desired key differs from current state."""
        diff = {}
        for key, desired_value in desired.items():
            if desired_value is None:
                continue

            if not self._values_equal(current.get(key), desired_value):
                diff[key] = {"before": current.get(key), "after": desired_value}

        return diff

    def _values_equal(self, current_value, desired_value):
        """Compare desired vs current values, recursing into partial dict updates."""
        if isinstance(desired_value, dict):
            if not isinstance(current_value, dict):
                return False
            for key, value in desired_value.items():
                if not self._values_equal(current_value.get(key), value):
                    return False
            return True
        return current_value == desired_value
