from typing import Union
import re
from ._errors import (
    RequiredParameterError,
    RequiredPathParameterError,
    OperationFormatError,
)


class OperationConfig:
    def __init__(
        self,
        name: str,
        uri: str,
        http_method: str,
        body_spec: dict = None,
        query_spec: dict = None,
    ):
        self.name = name
        self.uri = uri
        self.http_method = http_method.lower()
        self._body_spec = body_spec
        self._query_spec = query_spec

    def build_path(self, params: dict) -> str:
        """
        Use the parans to populate a path template.
        Given a template like '/foo/bar/{datacenter}', this method will use the
        params to search for values to replace "{datacenter}" and create
        a path like '/foo/bar/dc01'
        """
        if "{" not in self.uri:
            return self.uri

        path = self.uri
        for template_placeholder in re.findall(r"\{\w+\}", self.uri):
            param_key = template_placeholder[1:-1]
            if not params.get(param_key):
                raise RequiredPathParameterError(
                    api_template=template_placeholder,
                    param_name=param_key,
                    uri=self.uri,
                    operation=self.name,
                    http_method=self.http_method,
                )
            path = path.replace(template_placeholder, params[param_key])
        return path

    def build_query(self, params: dict) -> Union[dict, None]:
        if not self._query_spec:
            return None

        try:
            return self._build_dict_with_params(params=params, spec=self._query_spec)
        except RequiredParameterError:
            raise
        except Exception as e:
            raise OperationFormatError(
                f"Failed to build query parameters for operation '{self.name}': {e}"
            )

    def build_body(self, params: dict) -> Union[dict, None]:
        if not self._body_spec:
            return None

        try:
            return self._build_dict_with_params(params=params, spec=self._body_spec)
        except RequiredParameterError:
            raise
        except Exception as e:
            raise OperationFormatError(
                f"Failed to build request body for operation '{self.name}': {e}"
            )

    def _build_dict_with_params(self, params: dict, spec: dict):
        out = {}
        for param_key, spec_value in spec.items():
            is_required = spec_value.get("required", False)
            subspec = spec_value.get("subspec", {})
            param_value = params.get(param_key)
            if subspec and param_value:
                # there is a subspec dict, indicating we need to recurse
                out[param_key] = self._build_dict_with_params(
                    params=param_value, spec=subspec
                )
                continue

            if param_value is not None:
                # we found a param value, so add it to the return
                out[param_key] = param_value
                continue

            if is_required:
                # we didnt find a value, and we need a value, so raise an error
                raise RequiredParameterError(
                    param_name=param_key,
                    uri=self.uri,
                    operation=self.name,
                    http_method=self.http_method,
                )
        return out
