# -*- coding: utf-8 -*-
# Copyright: (c) 2026, Eco Ansible Content Team <@eco-ansible-content>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from abc import ABC, abstractmethod

from ansible_collections.vmware.vmware_rest.plugins.module_utils._client import (
    Client,
    ClientRequestErrorHandler,
)


def normalize_list_response(data):
    """Return a list from a vSphere API list response (bare list or value envelope)."""
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        value = data.get("value", [])
        return value if isinstance(value, list) else []
    return []


def values_equal(current_value, desired_value):
    """Compare desired vs current values, recursing into partial dict updates."""
    if isinstance(desired_value, dict):
        if not isinstance(current_value, dict):
            return False
        for key, value in desired_value.items():
            if not values_equal(current_value.get(key), value):
                return False
        return True
    return current_value == desired_value


def params_differ(current, desired):
    """Return True when any desired key differs from current state."""
    for key, desired_value in desired.items():
        if not values_equal(current.get(key), desired_value):
            return True
    return False


def payload_body_subset(body, exclude=()):
    """Build a PAYLOAD_FORMAT body map omitting excluded API fields."""
    excluded = set(exclude)
    return {
        api_field: module_param
        for api_field, module_param in body.items()
        if api_field not in excluded
    }


def find_summary_id(summaries, name, name_key="name", id_key="resource_pool"):
    """Return the resource id from a list summary matching name, or None."""
    for summary in summaries:
        if summary.get(name_key) == name:
            return summary.get(id_key)
    return None


class VmwareRestModuleBase(ABC):
    PAYLOAD_FORMAT = {
        "get": {"query": {}, "body": {}, "path": {}},
        "post": {"query": {}, "body": {}, "path": {}},
        "put": {"query": {}, "body": {}, "path": {}},
        "patch": {"query": {}, "body": {}, "path": {}},
        "delete": {"query": {}, "body": {}, "path": {}},
    }

    def __init__(self, module):
        self.module = module
        self.params = module.params
        self.client = self._create_client()

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

    def build_path(self, path_template: str, params: dict = None) -> str:
        # Substitute path parameters from module params into the API path template.
        # Example: "/vcenter/datacenter/{datacenter}" with params["datacenter"] = "dc-1"
        # returns "/vcenter/datacenter/dc-1"
        if params is None:
            params = self.params

        path = path_template
        for key, value in params.items():
            path = path.replace("{" + key + "}", str(value))
        return path

    def build_payload(self, payload_format: dict, params: dict = None) -> dict:
        # Build request body from module params using PAYLOAD_FORMAT body mapping.
        # The payload_format parameter is the PAYLOAD_FORMAT entry for the operation being performed.
        if params is None:
            params = self.params

        body = {}
        for api_field, module_param in payload_format.get("body", {}).items():
            if module_param in params and params[module_param] is not None:
                body[api_field] = params[module_param]
        return body

    def build_query(self, payload_format: dict, params: dict = None) -> dict:
        # Build query parameters from module params using PAYLOAD_FORMAT query mapping.
        # The payload_format parameter is the PAYLOAD_FORMAT entry for the operation being performed.
        if params is None:
            params = self.params
        query = {}
        for api_param, module_param in payload_format.get("query", {}).items():
            if module_param in params and params[module_param] is not None:
                query[api_param] = params[module_param]
        return query

    def fetch_list(self, list_path, list_payload_format):
        """GET a collection path and return a normalized list (empty on 404)."""
        query = self.build_query(list_payload_format)
        response = self.client.get(list_path, query=query or None)
        if response.status == 404:
            return []
        return normalize_list_response(response.json)


class VmwareRestCrudModuleBase(VmwareRestModuleBase):
    UPDATABLE_PARAMS = ()

    @abstractmethod
    def ensure_present(self):
        pass

    @abstractmethod
    def ensure_absent(self):
        pass

    def build_updatable_payload(self, updatable_params=None):
        """Build a PATCH body from user-set params listed in updatable_params."""
        keys = self.UPDATABLE_PARAMS if updatable_params is None else updatable_params
        payload = {}
        for param in keys:
            if self.params.get(param) is not None:
                payload[param] = self.params[param]
        return payload

    def resolve_resource_id(self, id_param, name_param, find_by_name, fail_msg=None):
        """
        Resolve a resource MOID from an id param or by name lookup.

        When fail_msg is set and name is provided but not found, fail the module.
        Otherwise return None when the resource cannot be resolved.
        """
        resource_id = self.params.get(id_param)
        if resource_id:
            return resource_id

        name = self.params.get(name_param)
        if not name:
            return None

        found_id = find_by_name(name)
        if found_id:
            return found_id

        if fail_msg:
            self.module.fail_json(msg=fail_msg.format(name))
        return None

    def delete_if_exists(self, item_path_template, path_params):
        """DELETE a resource when present; return changed=False on 404."""
        path = self.build_path(item_path_template, path_params)
        response = self.client.get(path)
        if response.status == 404:
            return {"changed": False}

        if not self.module.check_mode:
            self.client.delete(path)
        return {"changed": True}

    def update_if_changed(self, path, current, update_body):
        """PATCH when update_body differs from current; re-fetch after update."""
        if not update_body:
            return {"changed": False, "value": current}

        if not params_differ(current, update_body):
            return {"changed": False, "value": current}

        if not self.module.check_mode:
            updated = self.client.patch(path, data=update_body)
            if updated.status in (200, 204) and not updated.data:
                value = self.client.get(path).json
            else:
                value = updated.json
        else:
            value = current
        return {"changed": True, "value": value}


class VmwareRestInfoModuleBase(VmwareRestModuleBase):
    @abstractmethod
    def get_info(self):
        pass
