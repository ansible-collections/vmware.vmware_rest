import aiohttp

import ansible_module.turbo.server
from ansible_module.turbo.module import AnsibleTurboModule
from ansible_module.turbo.exceptions import EmbeddedModuleFailure


initialize_params = [
    "vcenter_hostname",
    "vcenter_username",
    "vcenter_password",
]


async def initialize(
    vcenter_hostname=None, vcenter_username=None, vcenter_password=None
):
    auth = aiohttp.BasicAuth(vcenter_username, vcenter_password)
    print("Open session!")
    connector = aiohttp.TCPConnector(limit=20, ssl=False)
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
                raise EmbeddedModuleFailure(
                    "Authentication failure. code: {}, json: {}".format(
                        resp.status, await resp.text()
                    )
                )
            json = await resp.json()
            session_id = json["value"]
            session = aiohttp.ClientSession(
                connector=connector,
                headers={"vmware-api-session-id": session_id},
                connector_owner=False,
            )
            return {"session": session}
