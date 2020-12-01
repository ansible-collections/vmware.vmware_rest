import hashlib
import importlib
from ansible.module_utils.basic import missing_required_lib
from ansible.module_utils.parsing.convert_bool import boolean


async def open_session(
    vcenter_hostname=None,
    vcenter_username=None,
    vcenter_password=None,
    validate_certs=True,
    log_file=None,
):
    validate_certs = boolean(validate_certs)
    m = hashlib.sha256()
    m.update(vcenter_hostname.encode())
    m.update(vcenter_username.encode())
    m.update(vcenter_password.encode())
    if log_file:
        m.update(log_file.encode())
    m.update(b"yes" if validate_certs else b"no")
    digest = m.hexdigest()
    # TODO: Handle session timeout
    if digest in open_session._pool:
        return open_session._pool[digest]

    exceptions = importlib.import_module(
        "ansible_collections.cloud.common.plugins.module_utils.turbo.exceptions"
    )
    try:
        aiohttp = importlib.import_module("aiohttp")
    except ImportError:
        raise exceptions.EmbeddedModuleFailure(msg=missing_required_lib("aiohttp"))

    if not aiohttp:
        raise exceptions.EmbeddedModuleFailure(msg="Failed to import aiohttp")

    if log_file:
        trace_config = aiohttp.TraceConfig()

        async def on_request_end(session, trace_config_ctx, params):
            with open(log_file, "a+") as fd:
                answer = await params.response.text()
                fd.write(
                    f"{params.method}: {params.url}\n"
                    f"headers: {params.headers}\n"
                    f"  status: {params.response.status}\n"
                    f"  answer: {answer}\n\n"
                )

        trace_config.on_request_end.append(on_request_end)
        trace_configs = [trace_config]
    else:
        trace_configs = []

    auth = aiohttp.BasicAuth(vcenter_username, vcenter_password)
    if validate_certs:
        connector = aiohttp.TCPConnector(limit=20)
    else:
        connector = aiohttp.TCPConnector(limit=20, ssl=False)
    async with aiohttp.ClientSession(
        connector=connector, connector_owner=False, trace_configs=trace_configs
    ) as session:
        try:
            async with session.post(
                "https://{hostname}/rest/com/vmware/cis/session".format(
                    hostname=vcenter_hostname
                ),
                auth=auth,
            ) as resp:
                if resp.status != 200:
                    raise exceptions.EmbeddedModuleFailure(
                        "Authentication failure. code: {0}, json: {1}".format(
                            resp.status, await resp.text()
                        )
                    )
                json = await resp.json()
        except aiohttp.client_exceptions.ClientConnectorError as e:
            raise exceptions.EmbeddedModuleFailure(f"Authentication failure: {e}")

    session_id = json["value"]
    session = aiohttp.ClientSession(
        connector=connector,
        headers={
            "vmware-api-session-id": session_id,
            "content-type": "application/json",
        },
        connector_owner=False,
        trace_configs=trace_configs,
    )
    open_session._pool[digest] = session
    return session


open_session._pool = {}


def gen_args(params, in_query_parameter):
    args = ""
    for i in in_query_parameter:
        if i.startswith("filter."):
            v = params.get("filter_" + i[7:])
        else:
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
    if not data:
        data = {}
    if operation == "create" and status in [200, 201]:
        data["failed"] = False
        data["changed"] = True
    elif operation == "update" and status in [200]:
        data["failed"] = False
        data["changed"] = True
    elif operation == "upgrade" and status in [200]:
        data["failed"] = False
        data["changed"] = True
    elif operation == "set" and status in [200]:
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


async def list_devices(session, url):
    existing_entries = []

    async with session.get(url) as resp:
        _json = await resp.json()
        return _json


async def build_full_device_list(session, url, device_list):
    import asyncio

    device_ids = []
    for i in device_list["value"]:
        fields = list(i.values())
        key = list(i.keys())[0]
        if len(fields) != 1:
            # The list already comes with all the details
            return device_list
        device_ids.append(fields[0])

    tasks = [
        asyncio.ensure_future(get_device_info(session, url, _id)) for _id in device_ids
    ]

    return [await i for i in tasks]


async def get_device_info(session, url, _id):
    async with session.get(url + "/" + _id) as resp:
        if resp.status == 200:
            _json = await resp.json()
            _json["id"] = str(_id)
            return _json


async def exists(params, session, url, unicity_keys=None):
    if not unicity_keys:
        unicity_keys = []

    unicity_keys += ["label", "pci_slot_number", "sata"]

    devices = await list_devices(session, url)
    full_devices = await build_full_device_list(session, url, devices)

    for device in full_devices:
        for k in unicity_keys:
            if not params.get(k):
                continue
            v = device["value"].get(k)
            if isinstance(k, int) or isinstance(v, str):
                k = str(k)
                v = str(v)
            if v == params.get(k):
                return device


def set_subkey(root, path, value):
    cur_loc = root
    splitted = path.split("/")
    for j in splitted[:-1]:
        if j not in cur_loc:
            cur_loc[j] = {}
        cur_loc = cur_loc[j]
    cur_loc[splitted[-1]] = value


def prepare_payload(params, payload_format):
    payload = {}
    for i in payload_format["body"].keys():
        if params[i] is None:
            continue

        path = payload_format["body"][i]
        set_subkey(payload, path, params[i])
    return payload


def get_subdevice_type(url):
    """If url needs a subkey, return its name."""
    candidates = []
    for i in url.split("/"):
        if i.startswith("{"):
            candidates.append(i[1:-1])
    if len(candidates) != 2:
        return
    return candidates[-1]


def get_device_type(url):
    device_type = url.split("/")[-1]
    # NOTE: This mapping can be extracted from the delete end-point of the
    # resource, e.g:
    # /rest/vcenter/vm/{vm}/hardware/ethernet/{nic} -> nic
    # Also, it sounds like we can use "list_index" instead
    if device_type == "ethernet":
        return "nic"
    elif device_type in ["sata", "scsi"]:
        return "adapter"
    elif device_type in ["parallel", "serial"]:
        return "port"
    else:
        return device_type
