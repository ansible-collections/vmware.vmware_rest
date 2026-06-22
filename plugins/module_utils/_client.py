# -*- coding: utf-8 -*-
# Copyright: (c) 2026, Eco Ansible Content Team <@eco-ansible-content>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import json
import time
import logging

from typing import Optional, Union

from urllib.error import URLError, HTTPError
from urllib.parse import urlencode
from ansible.module_utils.urls import Request, basic_auth_header

from ansible_collections.vmware.vmware_rest.plugins.module_utils._errors import (
    UnexpectedAPIResponse,
    ApiCommunicationError,
    VmwareModuleError,
)

logger = logging.getLogger(__name__)


DEFAULT_HEADERS = dict(Accept="application/json")


class Response:
    def __init__(self, status, data, headers=None):
        self.status = status
        self.data = data
        # [('h1', 'v1'), ('H2', 'V2')] -> {'h1': 'v1', 'h2': 'V2'}
        self.headers = (
            dict((k.lower(), v) for k, v in dict(headers).items()) if headers else {}
        )

    @property
    def text(self):
        return self.data.decode("utf-8")

    @property
    def json(self):
        try:
            return json.loads(self.data)
        except ValueError as exc:
            raise Exception(f"Received invalid JSON response: {self.data}") from exc

    def log_to_file(self, log_file):
        with open(log_file, "a+", encoding="utf-8") as fd:
            fd.write(
                f"{self.method}: {self.url}\n"
                f"headers: {self.headers}\n"
                f"  status: {self.status}\n"
                f"  answer: {self.text}\n\n"
            )


class Client:
    def __init__(
        self,
        error_handler: "ClientRequestErrorHandler",
        host,
        username=None,
        password=None,
        port=None,
        timeout=None,
        validate_certs=None,
        log_file=None,
    ):
        if not host or host.startswith(("https://", "http://")):
            raise Exception(
                f"Invalid vCenter host value: '{host}'. "
                "Value should be the hostname of the vCenter server, not including the 'https://' or 'http://'"
            )

        self.error_handler = error_handler
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.timeout = timeout
        self.validate_certs = validate_certs
        self.log_file = log_file

        self._auth_headers = {}
        self._client = Request()

    def _is_oauth_token_expired(self):
        if self._token_expiry_time is None:
            return False
        return time.time() >= (self._token_expiry_time - self._token_refresh_margin)

    @property
    def auth_headers(self):
        if not self._auth_headers:
            self._auth_headers = self._login()
        return self._auth_headers

    def _login(self):
        try:
            headers = dict(
                **DEFAULT_HEADERS,
                Authorization=basic_auth_header(self.username, self.password),
            )
            response = self._do_request(
                method="POST",
                path=self._build_url("/rest/com/vmware/cis/session"),
                headers=headers,
            )
        except Exception as e:
            raise Exception(f"Authentication failure: {e}")

        if response.status != 200:
            raise Exception(
                f"Authentication failure. code: {response.status}, json: {response.json}"
            )

        return {
            "vmware-api-session-id": response.json["value"],
            "content-type": "application/json",
        }

    def _do_request(self, method, path, data=None, headers=None):
        request_kwargs = {
            "data": data,
            "headers": headers,
            "timeout": self.timeout,
            "validate_certs": self.validate_certs,
        }

        try:
            raw_resp = self._client.open(method, path, **request_kwargs)
        except HTTPError as e:
            # An HTTP error occurred, but that might be a valid response from the API.
            # The caller should handle it
            response = Response(e.code, e.read(), e.headers)

        except Exception as e:
            self.error_handler.handle_request_error(
                exception=e,
                method=method,
                path=path,
                request_kwargs=request_kwargs,
            )
        else:
            response = Response(raw_resp.status, raw_resp.read(), raw_resp.headers)

        if self.log_file:
            response.log_to_file(self.log_file)

        return response

    def request(self, method, path, query=None, data=None, headers=None, bytes=None):
        # Make sure we only have one kind of payload
        if data is not None and bytes is not None:
            raise AssertionError(
                "Cannot have JSON and binary payload in a single request."
            )

        url = self._build_url(path, query)
        headers = dict(headers or DEFAULT_HEADERS, **self.auth_headers)

        if data is not None:
            data = json.dumps(data, separators=(",", ":"))
            headers["Content-type"] = "application/json"

        elif bytes is not None:
            data = bytes

        return self._do_request(method, url, data=data, headers=headers)

    def _normalize_api_path(self, path):
        """
        Normalize an API path for URL construction.

        OpenAPI 3 YAML specs declare servers with base URL https://{host}/api and
        paths relative to that base (e.g. /vcenter/resource-pool). Swagger 2 JSON
        specs store fully qualified paths (e.g. /api/vcenter/resource-pool).
        Session authentication uses /rest/... paths outside the /api prefix.
        """
        normalized = path.strip("/")
        if normalized.startswith("api/") or normalized.startswith("rest/"):
            return normalized
        return "api/{0}".format(normalized)

    def _build_url(self, path, query=None):
        if self.port:
            host = f"{self.host}:{self.port}"
        else:
            host = self.host
        url = f"https://{host}/{self._normalize_api_path(path)}"
        if query:
            url = "{0}?{1}".format(url, urlencode(query, doseq=True))
        return url

    def get(self, path, query=None):
        resp = self.request("GET", path, query=query)
        if resp.status in (200, 404):
            return resp
        self.error_handler.handle_request_error(
            exception=UnexpectedAPIResponse(resp.status, resp.data),
            method="GET",
            path=path,
            request_kwargs=dict(query=query),
        )

    def post(self, path, data, query=None):
        resp = self.request("POST", path, data=data, query=query)
        if resp.status in (200, 201):
            return resp
        self.error_handler.handle_request_error(
            exception=UnexpectedAPIResponse(resp.status, resp.data),
            method="POST",
            path=path,
            request_kwargs=dict(data=data, query=query),
        )

    def patch(self, path, data, query=None):
        resp = self.request("PATCH", path, data=data, query=query)
        if resp.status in (200, 204):
            return resp
        self.error_handler.handle_request_error(
            exception=UnexpectedAPIResponse(resp.status, resp.data),
            method="PATCH",
            path=path,
            request_kwargs=dict(data=data, query=query),
        )

    def put(self, path, data, query=None):
        resp = self.request("PUT", path, data=data, query=query)
        if resp.status == 200:
            return resp
        self.error_handler.handle_request_error(
            exception=UnexpectedAPIResponse(resp.status, resp.data),
            method="PUT",
            path=path,
            request_kwargs=dict(data=data, query=query),
        )

    def delete(self, path, query=None):
        resp = self.request("DELETE", path, query=query)
        if resp.status in (200, 204):
            return resp
        self.error_handler.handle_request_error(
            exception=UnexpectedAPIResponse(resp.status, resp.data),
            method="DELETE",
            path=path,
            request_kwargs=dict(query=query),
        )


class ClientRequestErrorHandler:
    """
    Handles exceptions that occur during HTTP requests to the ServiceNow instance.

    This class centralizes error handling logic for network and SSL-related errors,
    providing consistent error messages and determining whether errors are retryable.
    It is used by the Client class's retry mechanism to handle transient network
    issues such as SSL handshake timeouts.

    Args:
        method (str): The HTTP method used for the request (e.g., 'GET', 'POST').
        path (str): The URL path that was requested.
        request_kwargs (dict): Dictionary containing request parameters such as
            timeout, validate_certs, client_cert, etc. Used for error context.
    """

    def __init__(self, module):
        self.module = module

    def handle_request_error(self, exception, method, path, request_kwargs):
        """
        Route exception to the appropriate handler based on exception type.

        This method categorizes exceptions and delegates to specific functions.
        For retryable errors (like SSL handshake timeouts), if retry_is_allowed
        is True, the method returns None to allow the caller's loop to continue.
        Otherwise, it raises an appropriate exception.

        Args:
            exception (Exception): The exception that occurred during the request.
            retry_is_allowed (bool): Whether retries are still allowed. If True
                and the error is retryable (e.g., TLS handshake timeout), the
                method returns None instead of raising, allowing the retry loop
                to continue. Defaults to False.

        Raises:
            ServiceNowError or subclass thereof: For non-retryable errors.

        Returns:
            None: When retry_is_allowed is True and the error is retryable
                (specifically TLS handshake timeouts). This signals the caller
                to retry the request.
        """
        if isinstance(exception, URLError):
            self._handle_request_urlerror(exception, method, path, request_kwargs)
        else:
            self._raise_generic_communication_error(
                exception, method, path, request_kwargs
            )

    def _raise_generic_communication_error(
        self, exception, method, path, request_kwargs
    ):
        """
        Raise a generic ApiCommunicationError for unexpected exceptions.
        """
        e = ApiCommunicationError(
            exception=exception,
            message="Unexpected error communicating with vCenter instance: %s"
            % exception,
            method=method,
            path=path,
            **request_kwargs,
        )
        self.fail_module_with_error(e)

    def _handle_request_urlerror(self, exception, method, path, request_kwargs):
        """
        Handle URLError exceptions, including timeouts and handshake failures.

        This method handles various URL-related errors:
          - General request timeouts: Always raises an error with timeout info.
          - TLS handshake timeouts: Returns None if retry_is_allowed is True,
            otherwise raises an error. This allows the retry mechanism to handle
            intermittent SSL handshake issues.
          - Other URLErrors: Raises a generic communication error.

        Args:
            exception (URLError): The URLError that occurred.
            retry_is_allowed (bool): Whether retries are still allowed. If True
                and the error is a TLS handshake timeout, returns None to allow
                retry. Defaults to False.

        Raises:
            ApiCommunicationError: For non-retryable errors or when retries are
                exhausted. Includes timeout settings for timeout errors.

        Returns:
            None: When retry_is_allowed is True and the error is a TLS handshake
                timeout. This allows the retry loop to continue.
        """
        try:
            reason = str(exception.reason)
        except AttributeError:
            reason = None

        if reason == "timed out":
            e = ApiCommunicationError(
                exception=exception,
                message="The request to the vCenter instance timed out.",
                method=method,
                path=path,
                timeout_setting=request_kwargs.get("timeout", "unknown"),
            )
            self.fail_module_with_error(e)

        if reason and reason.endswith("The handshake operation timed out"):
            e = ApiCommunicationError(
                exception=exception,
                message="Failed to communicate with instance. The TLS handshake operation timed out.",
                method=method,
                path=path,
            )
            self.fail_module_with_error(e)

        self._raise_generic_communication_error(exception, method, path, request_kwargs)

    def fail_module_with_error(
        self, error: Union[Exception, VmwareModuleError], message: Optional[str] = None
    ):
        """
        Helper method to fail the module with an error.
        If the error is an instance of VmwareModuleError, it will be used to format the error message.
        Otherwise, a generic error message will be used.

        The fail_json method is used to terminate the module execution and return a structured error to the user.
        """
        if isinstance(error, VmwareModuleError):
            self.module.fail_json(**error.to_module_fail_json_output())
        else:
            if message is None:
                message = f"An unexpected error occurred: {str(error)}"
            self.module.fail_json(msg=message)
