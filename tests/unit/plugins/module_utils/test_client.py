# -*- coding: utf-8 -*-
# Copyright: (c) 2026, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import json
from io import BytesIO
from unittest.mock import MagicMock, patch
from urllib.error import HTTPError, URLError

import pytest

from ansible_collections.vmware.vmware_rest.plugins.module_utils._client import (
    Client,
    ClientRequestErrorHandler,
    Response,
)
from ansible_collections.vmware.vmware_rest.plugins.module_utils._errors import (
    ApiCommunicationError,
    UnexpectedAPIResponse,
    VmwareModuleError,
)


class AnsibleFailJson(Exception):
    def __init__(self, kwargs):
        self.kwargs = kwargs


def fail_json(*args, **kwargs):
    if args:
        kwargs.update(args[0])
    raise AnsibleFailJson(kwargs)


@pytest.fixture
def error_handler():
    return MagicMock()


@pytest.fixture
def client(error_handler):
    return Client(
        error_handler=error_handler,
        host="vcenter.example.com",
        username="admin",
        password="secret",
        port=443,
        timeout=30,
        validate_certs=False,
    )


def test_response_text_and_json():
    body = b'{"value": "session-id"}'
    response = Response(200, body, headers=[("Content-Type", "application/json")])
    assert response.text == '{"value": "session-id"}'
    assert response.json == {"value": "session-id"}
    assert response.headers == {"content-type": "application/json"}


def test_response_json_invalid_raises():
    response = Response(200, b"not-json")
    with pytest.raises(Exception, match="invalid JSON"):
        _ = response.json


def test_response_log_to_file(tmp_path):
    log_file = tmp_path / "rest.log"
    response = Response(200, b'{"ok": true}')
    response.method = "GET"
    response.url = "https://vcenter.example.com/api/test"
    response.log_to_file(str(log_file))
    content = log_file.read_text(encoding="utf-8")
    assert "GET: https://vcenter.example.com/api/test" in content
    assert '"ok": true' in content


@pytest.mark.parametrize(
    "host",
    ["", "https://vcenter.example.com", "http://vcenter.example.com"],
)
def test_client_rejects_invalid_host(error_handler, host):
    with pytest.raises(Exception, match="Invalid vCenter host value"):
        Client(error_handler=error_handler, host=host)


def test_client_normalize_api_path(client):
    assert client._normalize_api_path("/vcenter/vm") == "api/vcenter/vm"
    assert client._normalize_api_path("api/vcenter/vm") == "api/vcenter/vm"
    assert client._normalize_api_path("/rest/com/vmware/cis/session") == (
        "rest/com/vmware/cis/session"
    )


def test_client_build_url_with_port_and_query(client):
    url = client._build_url("/vcenter/vm", query={"filter": "poweredOn"})
    assert url == "https://vcenter.example.com:443/api/vcenter/vm?filter=poweredOn"


def test_client_build_url_without_port(error_handler):
    client = Client(error_handler=error_handler, host="vcenter.example.com")
    url = client._build_url("/rest/com/vmware/cis/session")
    assert url == "https://vcenter.example.com/rest/com/vmware/cis/session"


def test_client_auth_headers_login_once(client):
    login_response = Response(200, json.dumps({"value": "session-abc"}).encode("utf-8"))
    with patch.object(client, "_do_request", return_value=login_response):
        headers = client.auth_headers
        assert headers == {
            "vmware-api-session-id": "session-abc",
            "content-type": "application/json",
        }
        assert client.auth_headers is headers
        client._do_request.assert_called_once()


def test_client_login_failure_on_non_200(client):
    login_response = Response(401, b'{"error":"unauthorized"}')
    with patch.object(client, "_do_request", return_value=login_response):
        with pytest.raises(Exception, match="Authentication failure"):
            _ = client.auth_headers


def test_client_request_rejects_data_and_bytes(client):
    with patch.object(client, "_do_request"):
        with pytest.raises(AssertionError, match="Cannot have JSON and binary"):
            client.request("POST", "/vcenter/vm", data={"name": "vm"}, bytes=b"raw")


def test_client_request_serializes_json_payload(client):
    api_response = Response(200, b"{}")
    client._auth_headers = {
        "vmware-api-session-id": "sid",
        "content-type": "application/json",
    }
    with patch.object(
        client, "_do_request", return_value=api_response
    ) as mock_do_request:
        client.request("POST", "/vcenter/vm", data={"name": "vm-1"})
    _, kwargs = mock_do_request.call_args
    assert kwargs["data"] == '{"name":"vm-1"}'
    assert kwargs["headers"]["Content-type"] == "application/json"


def test_client_do_request_handles_http_error(client, error_handler):
    http_error = HTTPError(
        url="https://vcenter.example.com/api/test",
        code=404,
        msg="Not Found",
        hdrs={"Content-Type": "application/json"},
        fp=BytesIO(b'{"error": "missing"}'),
    )
    with patch.object(client._client, "open", side_effect=http_error):
        response = client._do_request(
            "GET",
            "https://vcenter.example.com/api/test",
            headers={"Accept": "application/json"},
        )
    assert response.status == 404
    assert response.json == {"error": "missing"}
    error_handler.handle_request_error.assert_not_called()


def test_client_do_request_delegates_other_exceptions(client, error_handler):
    def _handle_request_error(**kwargs):
        handler = ClientRequestErrorHandler(MagicMock())
        handler.module.fail_json.side_effect = fail_json
        handler.handle_request_error(**kwargs)

    error_handler.handle_request_error.side_effect = _handle_request_error
    with patch.object(client._client, "open", side_effect=OSError("network down")):
        with pytest.raises(AnsibleFailJson) as exc:
            client._do_request(
                "GET",
                "https://vcenter.example.com/api/test",
                headers={"Accept": "application/json"},
            )
    error_handler.handle_request_error.assert_called_once()
    assert error_handler.handle_request_error.call_args.kwargs["method"] == "GET"
    assert "Unexpected error communicating with vCenter" in exc.value.kwargs["msg"]


@pytest.mark.parametrize(
    "method_name,status,args",
    [
        ("get", 200, ("/vcenter/vm",)),
        ("get", 404, ("/vcenter/vm",)),
        ("post", 201, ("/vcenter/vm", {"name": "vm"})),
        ("patch", 204, ("/vcenter/vm/vm-1", {"name": "vm"})),
        ("put", 200, ("/vcenter/vm/vm-1", {"name": "vm"})),
        ("delete", 204, ("/vcenter/vm/vm-1",)),
    ],
)
def test_client_http_methods_success(client, method_name, status, args):
    with patch.object(client, "request", return_value=Response(status, b"")):
        result = getattr(client, method_name)(*args)
    assert result.status == status


@pytest.mark.parametrize(
    "method_name,status,args",
    [
        ("get", 500, ("/vcenter/vm",)),
        ("post", 400, ("/vcenter/vm", {"name": "vm"})),
        ("patch", 409, ("/vcenter/vm/vm-1", {"name": "vm"})),
        ("put", 403, ("/vcenter/vm/vm-1", {"name": "vm"})),
        ("delete", 500, ("/vcenter/vm/vm-1",)),
    ],
)
def test_client_http_methods_unexpected_status(
    client, error_handler, method_name, status, args
):
    body = b"error body"
    with patch.object(client, "request", return_value=Response(status, body)):
        getattr(client, method_name)(*args)
    error_handler.handle_request_error.assert_called_once()
    exc = error_handler.handle_request_error.call_args.kwargs["exception"]
    assert isinstance(exc, UnexpectedAPIResponse)
    assert exc.message == "Unexpected response - {0} {1}".format(status, body)


def test_client_request_error_handler_timeout():
    module = MagicMock()
    module.fail_json.side_effect = fail_json
    handler = ClientRequestErrorHandler(module)
    url_error = URLError("timed out")
    url_error.reason = "timed out"
    with pytest.raises(AnsibleFailJson) as exc:
        handler.handle_request_error(
            exception=url_error,
            method="GET",
            path="/api/vcenter/vm",
            request_kwargs={"timeout": 10},
        )
    error = exc.value.kwargs
    assert error["msg"] == "The request to the vCenter instance timed out."
    assert error["debug_info"]["timeout_setting"] == 10


def test_client_request_error_handler_handshake_timeout():
    module = MagicMock()
    module.fail_json.side_effect = fail_json
    handler = ClientRequestErrorHandler(module)
    url_error = URLError("handshake timed out")
    url_error.reason = "SSL: The handshake operation timed out"
    with pytest.raises(AnsibleFailJson) as exc:
        handler.handle_request_error(
            exception=url_error,
            method="GET",
            path="/api/vcenter/vm",
            request_kwargs={},
        )
    assert "TLS handshake operation timed out" in exc.value.kwargs["msg"]


def test_client_request_error_handler_generic_url_error():
    module = MagicMock()
    module.fail_json.side_effect = fail_json
    handler = ClientRequestErrorHandler(module)
    url_error = URLError("connection refused")
    url_error.reason = "connection refused"
    with pytest.raises(AnsibleFailJson) as exc:
        handler.handle_request_error(
            exception=url_error,
            method="POST",
            path="/api/vcenter/vm",
            request_kwargs={"validate_certs": False},
        )
    assert "Unexpected error communicating with vCenter" in exc.value.kwargs["msg"]


def test_client_request_error_handler_fail_with_vmware_module_error():
    module = MagicMock()
    handler = ClientRequestErrorHandler(module)
    error = VmwareModuleError("module-specific failure")
    handler.fail_module_with_error(error)
    module.fail_json.assert_called_once_with(msg="module-specific failure")


def test_client_request_error_handler_fail_with_plain_exception():
    module = MagicMock()
    handler = ClientRequestErrorHandler(module)
    handler.fail_module_with_error(ValueError("bad value"))
    module.fail_json.assert_called_once_with(
        msg="An unexpected error occurred: bad value"
    )


def test_client_request_error_handler_fail_with_api_communication_error():
    module = MagicMock()
    handler = ClientRequestErrorHandler(module)
    error = ApiCommunicationError(
        exception=OSError("broken pipe"),
        message="Communication failed",
        method="GET",
        path="/api/vcenter/vm",
    )
    handler.fail_module_with_error(error)
    module.fail_json.assert_called_once()
    output = module.fail_json.call_args.kwargs
    assert output["msg"] == "Communication failed"
    assert output["exception_info"]["type"] == "OSError"
