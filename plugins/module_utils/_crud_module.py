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
        get_operation_config: OperationConfig,
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

    def ensure_absent(self) -> dict:
        result = {"changed": False}
        resource = self._search_for_resource()
        if not resource:
            # Object is already absent, nothing to do
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
            http_operation(path, query=query)

        return result

    def _search_for_resource(self) -> Union[dict, None]:
        """
        Get a resource using the module params. Enrich the resulting dict with
        params or the resource summary to ensure the MOID is present.
        """
        try:
            resource = self._perform_get_operation()
        except RequiredPathParameterError:
            if not self.params.get("name"):
                raise
        else:
            if resource:
                return {**self.params, **resource}
            else:
                return resource

        for summary in self._perform_list_operation():
            if summary.get("name") == self.params.get("name"):
                resource = self._perform_get_operation(resource=summary)
                return {**summary, **resource}

        return None

    def perform_action(self) -> dict:
        """
        This is the primary entrypoint when state == some action (connect, disconnect, deploy).
        It will always attempt to perform the action as requested.
        """
        action_value = self.params["state"]
        action_operation = self.action_operations[action_value]
        result = {"changed": False, "id": ""}
        resource = self._search_for_resource()

        if not resource:
            self.module.fail_json(
                "No matching resource was found. Use the present state to create the module before"
                " attempting to perform the %s action." % action_value
            )

        resource_id = self._get_moid_attribute_value_from_resource(resource)
        result["id"] = resource_id
        result["changed"] = True
        path = action_operation.build_path(params={**self.params, **resource})
        http_method = getattr(self.client, action_operation.http_method)
        if not self.module.check_mode:
            http_method(path=path)

        return result

    def ensure_present(self) -> dict:
        """
        This is the primary routing entrypoint for state == present. It should call and route to
        self._create or self._update, as appropriate.
        """
        result = {"changed": False, "id": ""}
        resource = self._search_for_resource()

        if not resource:
            result["id"] = self._create()
            result["changed"] = True
        else:
            result["id"] = self._get_moid_attribute_value_from_resource(resource)
            result["diff"] = self._update_if_needed(resource)
            result["changed"] = bool(result["diff"])

        return result

    def _create(self) -> str:
        path = self.create_operation_config.build_path(params=self.params)
        body = self.create_operation_config.build_body(params=self.params)
        http_method = getattr(self.client, self.create_operation_config.http_method)
        new_id = ""
        if not self.module.check_mode:
            response = http_method(path, data=body)
            new_id = response.json

        return new_id

    def _update_if_needed(self, resource: dict) -> dict:
        if self.update_operation_config is None:
            # update operations are not supported for this resource
            return {}

        desired_body = self.update_operation_config.build_body(params=self.params)
        diff = self._calculate_resource_diff(current=resource, desired=desired_body)
        if not diff:
            return {}

        # Build the path using the path mapping from update_operation_config or fallback to _path_mapping
        path = self.update_operation_config.build_path(
            params={**self.params, **resource}
        )
        update_method = getattr(self.client, self.update_operation_config.http_method)
        if not self.module.check_mode:
            update_method(path, data=desired_body)

        return diff

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
