# -*- coding: utf-8 -*-
# Copyright: (c) 2026, Eco Ansible Content Team <@eco-ansible-content>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import json
import time
import logging

from urllib.error import URLError
from urllib.parse import quote, urlencode
from ansible.module_utils.urls import Request, basic_auth_header

from ansible_collections.vmware.vmware_rest.plugins.module_utils._errors import (
    UnexpectedAPIResponse,
    ApiCommunicationError,
)


logger = logging.getLogger(__name__)


DEFAULT_HEADERS = dict(Accept="application/json")


class Response:
    def __init__(
        self, status, data, headers=None
    ):
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
        host,
        username=None,
        password=None,
        timeout=None,
        validate_certs=None,
        log_file=None,
    ):
        if not host or host.startswith(("https://", "http://")):
            raise Exception(
                f"Invalid vCenter host value: '{host}'. "
                "Value should be the hostname of the vCenter server, not including the 'https://' or 'http://'"
            )

        self.host = host
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
            response = self.request(
                method="POST",
                path="/rest/com/vmware/cis/session",
                headers=basic_auth_header(self.username, self.password),
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
            "validate_certs": self.validate_certs
        }
        request_error_handler = ClientRequestErrorHandler(method, path, request_kwargs)

        try:
            raw_resp = self._client.open(method, path, **request_kwargs)
        except Exception as e:
            # An exception occurred, and we need to parse it to add additional context
            request_error_handler.handle_request_error(exception=e)

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

    def _build_url(self, path, query=None):
        escaped_path = quote(path.strip("/"))
        if escaped_path:
            escaped_path = f"/{escaped_path}"
        url = f"https://{self.host}{escaped_path}"
        if query:
            url = f"{url}?{urlencode(query)}"
        return url

    def get(self, path, query=None):
        resp = self.request("GET", path, query=query)
        if resp.status in (200, 404):
            return resp
        raise UnexpectedAPIResponse(resp.status, resp.data)

    def post(self, path, data, query=None):
        resp = self.request("POST", path, data=data, query=query)
        if resp.status in (200, 201):
            return resp
        raise UnexpectedAPIResponse(resp.status, resp.data)

    def patch(self, path, data, query=None):
        resp = self.request("PATCH", path, data=data, query=query)
        if resp.status == 200:
            return resp
        raise UnexpectedAPIResponse(resp.status, resp.data)

    def put(self, path, data, query=None):
        resp = self.request("PUT", path, data=data, query=query)
        if resp.status == 200:
            return resp
        raise UnexpectedAPIResponse(resp.status, resp.data)

    def delete(self, path, query=None):
        resp = self.request("DELETE", path, query=query)
        if resp.status in (200, 204):
            return resp
        raise UnexpectedAPIResponse(resp.status, resp.data)


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

    def __init__(self, method, path, request_kwargs):
        self.method = method
        self.path = path
        self.request_kwargs = request_kwargs

    def handle_request_error(self, exception, retry_is_allowed=False):
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
            self._handle_request_urlerror(exception, retry_is_allowed)
        else:
            self._raise_generic_communication_error(exception)

    def _raise_generic_communication_error(self, exception):
        """
        Raise a generic ApiCommunicationError for unexpected exceptions.
        """
        raise ApiCommunicationError(
            exception=exception,
            message="Unexpected error communicating with vCenter instance: %s"
            % exception,
            method=self.method,
            path=self.path,
            **self.request_kwargs,
        )

    def _handle_request_urlerror(self, exception, retry_is_allowed=False):
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
            raise ApiCommunicationError(
                exception=exception,
                message="The request to the vCenter instance timed out.",
                method=self.method,
                path=self.path,
                timeout_setting=self.request_kwargs.get("timeout", "unknown"),
            )

        if reason and reason.endswith("The handshake operation timed out"):
            if retry_is_allowed:
                return

            raise ApiCommunicationError(
                exception=exception,
                message="Failed to communicate with instance. The TLS handshake operation timed out.",
                method=self.method,
                path=self.path,
            )

        self._raise_generic_communication_error(exception)
