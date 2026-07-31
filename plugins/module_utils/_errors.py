# -*- coding: utf-8 -*-
# Copyright: (c) 2021, XLAB Steampunk <steampunk@xlab.si>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import json


class VmwareModuleError(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message

    def to_module_fail_json_output(self):
        return {
            "msg": str(self),
        }

    def _is_jsonable(self, x):
        try:
            _ = json.dumps(x)  # pylint: disable=disallowed-name
            return True
        except Exception:
            return False


class AuthError(VmwareModuleError):
    pass


class OperationFormatError(VmwareModuleError):
    pass


class RequiredParameterError(VmwareModuleError):
    def __init__(self, param_name, uri, operation, http_method):
        super().__init__(
            "Missing required module parameter when building the request body or query: %s"
            % param_name
        )
        self.operation = operation
        self.param_name = param_name
        self.uri = uri
        self.http_method = http_method

    def to_module_fail_json_output(self):
        return {
            "msg": self.message,
            "module_param_name": self.param_name,
            "operation": self.operation,
            "uri": self.uri,
            "http_method": self.http_method,
        }


class RequiredPathParameterError(RequiredParameterError):
    def __init__(self, api_template, param_name, uri, operation, http_method):
        super().__init__(param_name, uri, operation, http_method)
        self.message = (
            "Missing required module parameter when building the request path: %s"
            % self.param_name
        )
        self.path_template_placeholder = api_template

    def to_module_fail_json_output(self):
        out = super().to_module_fail_json_output()
        out["path_template_placeholder"] = self.path_template_placeholder
        return out


class UnexpectedAPIResponse(VmwareModuleError):
    def __init__(self, status, data):
        self.message = "Unexpected response - {0} {1}".format(status, data)
        super(UnexpectedAPIResponse, self).__init__(self.message)


class ApiCommunicationError(VmwareModuleError):
    def __init__(self, exception, message=None, method=None, path=None, **kwargs):
        self.message = (
            message
            or "An unexpected error occurred while communicating with the vSphere REST API."
        )
        super().__init__(self.message)
        self.exception = exception
        self.method = method
        self.path = path
        self.kwargs = kwargs

    def to_module_fail_json_output(self):
        return {
            "msg": self.message,
            "exception_info": {
                "message": str(self.exception),
                "type": self.exception.__class__.__name__,
            },
            "debug_info": {
                "method": self.method,
                "path": self.path,
                **{k: v for k, v in self.kwargs.items() if self._is_jsonable(v)},
            },
        }
