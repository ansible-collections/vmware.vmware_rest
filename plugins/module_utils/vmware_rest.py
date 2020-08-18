import aiohttp
import functools
import hashlib
import importlib


from ansible_collections.cloud.common.plugins.module_utils.turbo.exceptions import (
    EmbeddedModuleFailure,
)


async def open_session(
    vcenter_hostname=None,
    vcenter_username=None,
    vcenter_password=None,
    validate_certs=True,
):

    m = hashlib.sha256()
    m.update(vcenter_hostname.encode())
    m.update(vcenter_username.encode())
    m.update(vcenter_password.encode())
    m.update(b"yes" if validate_certs else b"no")
    digest = m.hexdigest()
    # TODO: Handle session timeout
    if digest in open_session._pool:
        return open_session._pool[digest]

    aiohttp = importlib.import_module("aiohttp")
    if not aiohttp:
        raise EmbeddedModuleFailure()

    auth = aiohttp.BasicAuth(vcenter_username, vcenter_password)
    connector = aiohttp.TCPConnector(limit=20, ssl=validate_certs)
    async with aiohttp.ClientSession(
        connector=connector, connector_owner=False
    ) as session:
        async with session.post(
            "https://{hostname}/rest/com/vmware/cis/session".format(
                hostname=vcenter_hostname
            ),
            auth=auth,
        ) as resp:
            if resp.status != 200:
                try:
                    raise EmbeddedModuleFailure(
                        "Authentication failure. code: {}, json: {}".format(
                            resp.status, await resp.text()
                        )
                    )
                except ImportError:
                    pass
            json = await resp.json()
            session_id = json["value"]
            session = aiohttp.ClientSession(
                connector=connector,
                headers={
                    "vmware-api-session-id": session_id,
                    "content-type": "application/json",
                },
                connector_owner=False,
            )
            open_session._pool[digest] = session
            return session


open_session._pool = {}


def gen_args(params, in_query_parameter):
    args = ""
    for i in in_query_parameter:
        v = params.get(i)
        if not v:
            continue
        if not args:
            args = "?"
        else:
            args += "&"
        if isinstance(v, list):
            for j in v:
                args += (i + "=") + j
        elif isinstance(v, bool) and v:
            args += i + "=true"
        else:
            args += (i + "=") + v
    return args


async def update_changed_flag(data, status, operation):
    if operation == "create" and status in [200, 201]:
        data["failed"] = False
        data["changed"] = True
    elif operation == "delete" and status in [200, 204]:
        data["failed"] = False
        data["changed"] = True
    elif data.get("type") == "com.vmware.vapi.std.errors.already_in_desired_state":
        data["failed"] = False
        data["changed"] = False
    elif data.get("type") == "com.vmware.vapi.std.errors.already_exists":
        data["failed"] = False
        data["changed"] = False
    elif data.get("type") == "com.vmware.vapi.std.errors.resource_in_use":
        # NOTE: this is a shortcut/hack. We get this issue if a CDROM already exists
        data["failed"] = False
        data["changed"] = False
    elif (
        data.get("type") == "com.vmware.vapi.std.errors.internal_server_error"
        and data["value"]
        and data["value"]["messages"]
        and data["value"]["messages"][0]["args"]
        == [
            "com.vmware.vim.binding.vim.fault.DuplicateName cannot be cast to com.vmware.vim.binding.vim.fault.AlreadyConnected"
        ]
    ):
        # NOTE: another one for vcenter_host
        data["failed"] = False
        data["changed"] = False
    elif data.get("type", "").startswith("com.vmware.vapi.std.errors"):
        data["failed"] = True

    data["_debug_info"] = {"status": status, "operation": operation}
    return data
