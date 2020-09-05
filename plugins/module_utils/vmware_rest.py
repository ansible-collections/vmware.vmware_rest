import hashlib
import importlib


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
        from ansible_collections.cloud.common.plugins.module_utils.turbo.exceptions import (
            EmbeddedModuleFailure,
        )

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
                        "Authentication failure. code: {0}, json: {1}".format(
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
    if operation == "create" and status in [200, 201]:
        data["failed"] = False
        data["changed"] = True
    elif operation == "update" and status in [200]:
        data["failed"] = False
        data["changed"] = True
    elif operation == "upgrade" and status in [200]:
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


async def list_devices(params, session, url):
    existing_entries = []
    async with session.get(url) as resp:
        _json = await resp.json()
        devices = _json["value"]
    device_type = get_device_type(url)
    subdevice_type = get_subdevice_type(url)

    for device in devices:
        _id = device.get(device_type) or device.get(subdevice_type)
        if not _id:
            raise Exception("Cannot find the id key of the device!")
        existing_entries.append((await get_device_info(params, session, url, _id)))
    return existing_entries


async def get_device_info(params, session, url, _id):
    async with session.get(url + "/" + _id) as resp:
        _json = await resp.json()
        _json["id"] = str(_id)
        return _json


async def exists(params, session, url, unicity_keys=None):
    if not unicity_keys:
        unicity_keys = []

    unicity_keys += ["pci_slot_number", "sata"]

    devices = await list_devices(params, session, url)

    for device in devices:
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
        if isinstance(params[i], dict):
            for k, v in params[i].items():
                path = payload_format["body"][i][k]
                set_subkey(payload, path, v)
        else:
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
    else:
        return device_type
