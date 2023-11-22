# Copyright: (c) 2021, Alina Buzachis <@alinabuzachis>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function

__metaclass__ = type


import asyncio
import os
import urllib

from ansible.module_utils._text import to_native
from ansible.errors import AnsibleLookupError

from ansible_collections.cloud.common.plugins.module_utils.turbo.exceptions import (
    EmbeddedModuleFailure,
)
from ansible_collections.vmware.vmware_rest.plugins.module_utils.vmware_rest import (
    open_session,
    gen_args,
)


INVENTORY = {
    "resource_pool": {
        "list": {
            "query": {
                "clusters": "clusters",
                "datacenters": "datacenters",
                "hosts": "hosts",
                "names": "names",
                "parent_resource_pools": "parent_resource_pools",
                "resource_pools": "resource_pools",
            }
        }
    },
    "datacenter": {
        "list": {
            "query": {
                "datacenters": "datacenters",
                "folders": "folders",
                "names": "names",
            }
        }
    },
    "folder": {
        "list": {
            "query": {
                "datacenters": "datacenters",
                "folders": "folders",
                "names": "names",
                "parent_folders": "parent_folders",
                "type": "type",
            }
        }
    },
    "cluster": {
        "list": {
            "query": {
                "clusters": "clusters",
                "datacenters": "datacenters",
                "folders": "folders",
                "names": "names",
            }
        }
    },
    "host": {
        "list": {
            "query": {
                "clusters": "clusters",
                "datacenters": "datacenters",
                "folders": "folders",
                "hosts": "hosts",
                "names": "names",
            }
        }
    },
    "datastore": {
        "list": {
            "query": {
                "datacenters": "datacenters",
                "datastores": "datastores",
                "folders": "folders",
                "names": "names",
                "types": "types",
            }
        }
    },
    "vm": {
        "list": {
            "query": {
                "clusters": "clusters",
                "datacenters": "datacenters",
                "folders": "folders",
                "hosts": "hosts",
                "names": "names",
                "resource_pools": "resource_pools",
                "vms": "vms",
            }
        }
    },
    "network": {
        "list": {
            "query": {
                "datacenters": "datacenters",
                "folders": "folders",
                "names": "names",
                "networks": "networks",
                "types": "types",
            }
        }
    },
}


def get_credentials(**options):
    credentials = {}
    credentials["vcenter_hostname"] = options.get("vcenter_hostname") or os.getenv(
        "VMWARE_HOST"
    )
    credentials["vcenter_username"] = options.get("vcenter_username") or os.getenv(
        "VMWARE_USER"
    )
    credentials["vcenter_password"] = options.get("vcenter_password") or os.getenv(
        "VMWARE_PASSWORD"
    )
    credentials["vcenter_validate_certs"] = options.get(
        "vcenter_validate_certs"
    ) or os.getenv("VMWARE_VALIDATE_CERTS")
    credentials["vcenter_rest_log_file"] = options.get(
        "vcenter_rest_log_file"
    ) or os.getenv("VMWARE_REST_LOG_FILE")
    return credentials


class VcenterResource:
    def __init__(self, raw, api):
        self.raw = raw
        self._api = api

    @property
    def moid(self):
        return self.raw[self.object_type]

    @property
    def name(self):
        return self.raw["name"]


class VcenterCluster(VcenterResource):
    object_type = "cluster"
    api_type = "cluster"

    @property
    def child_resources(self):
        return [
            VcenterHost,
            VcenterResourcePool,
        ]

    async def get_child(self, resource, name):
        if resource not in self.child_resources:
            return None

        if resource == VcenterResourcePool:
            # We can't filter for resource_pools which are direct children of a cluster.
            # Instead, fetch cluster directly which contains the root resource_pool.
            # See: https://developer.vmware.com/apis/vsphere-automation/latest/vcenter/api/vcenter/cluster/cluster/get/
            cluster = await self._api.get_resource(VcenterCluster, self.moid)
            resource_pool_moid = cluster.raw["resource_pool"]

            # Now we can fetch the resource_pool
            return await self._api.list_resource_one(
                resource=VcenterResourcePool,
                filters={
                    "resource_pools": resource_pool_moid,
                },
            )
        else:
            child_resources = [
                i for i in self.child_resources if i != VcenterResourcePool
            ]
            for child_resource in child_resources:
                child = await self._api.list_resource_one(
                    resource=child_resource,
                    filters={
                        "clusters": self.moid,
                        "names": name,
                    },
                )

                if child:
                    return child

                return None


class VcenterDatacenter(VcenterResource):
    object_type = "datacenter"
    api_type = "datacenter"

    async def get_child(self, resource, name):
        # We can't filter for folders which are direct children of a datacenter.
        # Instead, fetch datacenter directly which contains the root folder moids for each object_type.
        # See: https://developer.vmware.com/apis/vsphere-automation/latest/vcenter/api/vcenter/datacenter/datacenter/get/
        datacenter = await self._api.get_resource(VcenterDatacenter, self.moid)
        key = f"{name}_folder"
        folder_moid = datacenter.raw[key]

        # Now we can fetch the folder
        return await self._api.list_resource_one(
            resource=VcenterFolder,
            filters={
                "folders": folder_moid,
            },
        )


class VcenterDatastore(VcenterResource):
    object_type = "datastore"
    api_type = "datastore"

    async def get_child(self, resource, name):
        return None


class VcenterFolder(VcenterResource):
    object_type = "folder"
    api_type = "folder"

    @property
    def folder_type(self):
        return self.raw["type"]

    @property
    def child_resources(self):
        lookup = {
            "DATACENTER": [
                VcenterFolder,
                VcenterDatacenter,
            ],
            "DATASTORE": [
                VcenterFolder,
                VcenterDatastore,
            ],
            "HOST": [
                VcenterFolder,
                VcenterHost,
                VcenterCluster,
            ],
            "NETWORK": [
                VcenterFolder,
                VcenterNetwork,
            ],
            "VIRTUAL_MACHINE": [
                VcenterFolder,
                VcenterVm,
            ],
        }

        return lookup[self.folder_type]

    async def get_child(self, resource, name):
        # We don't check if the requested resource is a valid child_resource, because all possible children implement this behaviour.
        # Checking here would make the code more complex than it needs to be. Of course, we sacrifice performance for simplicity here.

        for child_resource in self.child_resources:
            if child_resource == VcenterFolder:
                filters = {
                    "parent_folders": self.moid,
                    "names": name,
                }
            else:
                filters = {
                    "folders": self.moid,
                    "names": name,
                }

            child = await self._api.list_resource_one(child_resource, filters)

            if child:
                return child

        return None


class VcenterHost(VcenterResource):
    object_type = "host"
    api_type = "host"

    @property
    def child_resources(self):
        return [
            VcenterResourcePool,
        ]

    async def get_child(self, resource, name):
        if resource not in self.child_resources:
            return None

        # Unlike in clusters, there is no way to get the root resource_pool of a host.
        # So we fetch all resource_pools on this host.
        potential_roots = await self._api.list_resource(
            resource=VcenterResourcePool,
            filters={
                "hosts": self.moid,
            },
        )

        result = potential_roots.copy()
        for root in potential_roots:
            children = await self._api.list_resource(
                resource=VcenterResourcePool,
                filters={
                    "hosts": self.moid,
                    "parent_resource_pools": root.moid,
                },
            )
            moids = [i.moid for i in children]
            # We identify our root by deleting all resource_pools which appear as a child of another resource_pool.
            # Our root will be the last one left because it is no child of another resource_pool.
            result = [i for i in result if i.moid not in moids]

        result = result[0]

        if result.name != name:
            return None

        return result


class VcenterNetwork(VcenterResource):
    object_type = "network"
    api_type = "network"

    async def get_child(self, resource, name):
        return None


class VcenterResourcePool(VcenterResource):
    object_type = "resource_pool"
    api_type = "resource-pool"

    @property
    def child_resources(self):
        return [
            VcenterResourcePool,
        ]

    async def get_child(self, resource, name):
        if resource not in self.child_resources:
            return None

        for child_resource in self.child_resources:
            child = await self._api.list_resource_one(
                resource=child_resource,
                filters={
                    "parent_resource_pools": self.moid,
                    "names": name,
                },
            )

            if child:
                return child

            return None


class VcenterVm(VcenterResource):
    object_type = "vm"
    api_type = "vm"

    async def get_child(self, resource, name):
        return None


def get_vcenter_object_type(raw):
    for cls in VcenterResource.__subclasses__():
        if cls.object_type in raw:
            return cls.object_type

    if "vm_folder" in raw:
        return VcenterDatacenter.object_type

    return None


def make_vcenter_resource(raw, api):
    object_type = get_vcenter_object_type(raw)
    resource = get_vcenter_resource(object_type)
    return resource(raw, api)


def get_vcenter_resource(object_type):
    for cls in VcenterResource.__subclasses__():
        if cls.object_type == object_type:
            return cls

    return None


class VcenterApi:
    def __init__(self, hostname, session):
        self.hostname = hostname
        self._session = session

    def build_url(self, resource, params):
        try:
            _in_query_parameters = INVENTORY[resource.object_type]["list"][
                "query"
            ].keys()
        except KeyError:
            raise AnsibleLookupError(
                "object_type must be one of [%s]." % ", ".join(list(INVENTORY.keys()))
            )

        return (f"https://{self.hostname}/api/vcenter/{resource.api_type}") + gen_args(
            params, _in_query_parameters
        )

    async def fetch(self, url):
        async with self._session.get(url) as response:
            result = await response.json()
            return result

    async def get_resource(self, resource, moid):
        url = f"https://{self.hostname}/api/vcenter/{resource.api_type}/{moid}"
        result = await self.fetch(url)
        if result:
            return make_vcenter_resource(result, self)
        return None

    async def list_resource(self, resource, filters):
        url = self.build_url(resource, filters)
        result = await self.fetch(url)
        return [make_vcenter_resource(i, self) for i in result]

    async def list_resource_one(self, resource, filters):
        result = await self.list_resource(resource, filters)
        if result:
            return result[0]
        return None


class Lookup:
    def __init__(self, options, api):
        self._options = options
        self._api = api

    @classmethod
    async def entry_point(cls, terms, options):
        if not options.get("vcenter_hostname"):
            raise AnsibleLookupError("vcenter_hostname cannot be empty")
        if not options.get("vcenter_username"):
            raise AnsibleLookupError("vcenter_username cannot be empty")
        if not options.get("vcenter_password"):
            raise AnsibleLookupError("vcenter_password cannot be empty")

        try:
            session = await open_session(
                vcenter_hostname=options.get("vcenter_hostname"),
                vcenter_username=options.get("vcenter_username"),
                vcenter_password=options.get("vcenter_password"),
                validate_certs=bool(options.get("vcenter_validate_certs")),
                log_file=options.get("vcenter_rest_log_file"),
            )
        except EmbeddedModuleFailure as e:
            raise AnsibleLookupError(
                f'Unable to connect to vCenter or ESXi API at {options.get("vcenter_hostname")}: {to_native(e)}'
            )

        api = VcenterApi(options.get("vcenter_hostname"), session)
        lookup = cls(options, api)

        if not terms:
            raise AnsibleLookupError("No object has been specified.")

        task = asyncio.ensure_future(lookup.moid(terms[0]))

        return await task

    async def moid(
        self,
        object_path,
    ):
        if not object_path:
            return ""

        # Split object_path for traversal
        self._options["_terms"] = object_path
        object_path = tuple(filter(None, object_path.split("/")))
        resource = get_vcenter_resource(self._options["object_type"])

        # We start our search with the root folder in vCenter
        obj = make_vcenter_resource(
            raw={
                "folder": "group-d1",
                "type": "DATACENTER",
            },
            api=self._api,
        )

        while True:
            name = object_path[0]
            obj = await obj.get_child(resource, name)

            if not obj:
                return ""

            if len(object_path) == 1:
                if resource.object_type == obj.object_type:
                    return obj.moid
                else:
                    return ""

            object_path = object_path[1:]
