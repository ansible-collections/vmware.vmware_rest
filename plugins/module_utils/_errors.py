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


class UnexpectedAPIResponse(VmwareModuleError):
    def __init__(self, status, data):
        self.message = "Unexpected response - {0} {1}".format(status, data)
        super(UnexpectedAPIResponse, self).__init__(self.message)


class ApiCommunicationError(VmwareModuleError):
    def __init__(self, exception, message=None, method=None, path=None, **kwargs):
        self.message = (
            message
            or "An unexpected error occurred while communicating with the ServiceNow API."
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
