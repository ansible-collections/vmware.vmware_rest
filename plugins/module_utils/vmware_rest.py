def gen_args(params, in_query_parameter):
    args = ''
    for i in in_query_parameter:
        v = params.get(i)
        if (not v):
            continue
        if (not args):
            args = '?'
        else:
            args += '&'
        if isinstance(v, list):
            for j in v:
                args += ((i + '=') + j)
        elif (isinstance(v, bool) and v):
            args += (i + '=true')
        else:
            args += ((i + '=') + v)
    return args

async def update_changed_flag(data, status, operation):
    if operation == "create" and status == 201:
        data["failed"] = False
        data["changed"] = True
    elif operation == "delete" and status == 204:
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
    elif data.get("type") == "com.vmware.vapi.std.errors.internal_server_error" and data["value"] and data["value"]["messages"] and data["value"]["messages"][0]["args"] == [
                "com.vmware.vim.binding.vim.fault.DuplicateName cannot be cast to com.vmware.vim.binding.vim.fault.AlreadyConnected"]:
        # NOTE: another one for vcenter_host
        data["failed"] = False
        data["changed"] = False
    elif data.get("type", "").startswith("com.vmware.vapi.std.errors"):
        data["failed"] = True

    print("Answer: %s" % data)
    return data