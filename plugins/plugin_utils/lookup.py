# Copyright: (c) 2021, Alina Buzachis <@alinabuzachis>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function

__metaclass__ = type


import asyncio
import os

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


class Lookup:
    def __init__(self, options):
        self._options = options

    @classmethod
    async def entry_point(cls, terms, options):
        session = None

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

        lookup = cls(options)
        lookup._options["session"] = session

        if not terms:
            raise AnsibleLookupError("No object has been specified.")

        task = asyncio.ensure_future(lookup.moid(terms[0]))

        return await task

    async def fetch(self, url):
        async with self._options["session"].get(url) as response:
            result = await response.json()
            return result

    def build_url(self, object_type, params):
        try:
            _in_query_parameters = INVENTORY[object_type]["list"]["query"].keys()
            if object_type == "resource_pool":
                object_type = object_type.replace("_", "-")
        except KeyError:
            raise AnsibleLookupError(
                "object_type must be one of [%s]." % ", ".join(list(INVENTORY.keys()))
            )

        return (
            f"https://{self._options['vcenter_hostname']}/api/vcenter/{object_type}"
        ) + gen_args(params, _in_query_parameters)

    async def _helper_fetch(self, object_type, filters):
        _url = self.build_url(object_type, filters)
        return await self.fetch(_url)

    @staticmethod
    def ensure_result(result, object_type, object_name=None):
        if not result or object_name and object_name not in result[0].values():
            return ""

        def _filter_result(result):
            return [obj for obj in result if "%2f" not in obj["name"]]

        result = _filter_result(result)
        if result and len(result) > 1:
            raise AnsibleLookupError(
                "More than one object available: [%s]."
                % ", ".join(
                    list(f"{item['name']} => {item[object_type]}" for item in result)
                )
            )
        try:
            object_moid = result[0][object_type]
        except (TypeError, KeyError, IndexError) as e:
            raise AnsibleLookupError(to_native(e))
        return object_moid

    def _init_filter(self):
        filters = {}
        filters["datacenters"] = self._options["dc_moid"]
        return filters

    async def _get_datacenter_moid(self, path):
        filters = {}
        dc_name = ""
        dc_moid = ""
        _result = ""
        folder_moid = ""
        _path = path

        # Retrieve folders MoID if any
        folder_moid, _path = await self._get_folder_moid(path, filters)

        if _path:
            dc_name = _path[0]

        filters["names"] = dc_name
        filters["folders"] = folder_moid
        _result = await self._helper_fetch("datacenter", filters)
        dc_moid = self.ensure_result(_result, "datacenter", dc_name)

        return dc_moid, _path

    async def _fetch_result(self, object_path, object_type, filters):
        _result = ""
        obj_moid = ""
        visited = []
        _object_path_list = list(object_path)

        _result = await self.recursive_folder_or_rp_moid_search(
            object_path, object_type, filters
        )
        if _result:
            if object_path:
                for obj in _result:
                    if _object_path_list:
                        if obj["name"] == _object_path_list[0]:
                            del _object_path_list[0]
                        else:
                            visited.append(obj)
                if not visited:
                    obj_moid = [_result[-1]]
            else:
                obj_moid = _result
        return obj_moid, _object_path_list

    async def _get_folder_moid(self, object_path, filters):
        object_name = ""
        result = ""
        _result = ""
        _object_path = []

        if object_path:
            _result, _object_path = await self._fetch_result(
                object_path, "folder", filters
            )
            result = self.ensure_result(_result, "folder")

        if _result and self._options["object_type"] == "folder":
            if isinstance(_result, list) and _object_path:
                obj_path_set = set(_object_path)
                path_set = set([elem["name"] for elem in _result])
                if path_set - obj_path_set and self._options["_terms"][-1] != "/":
                    return "", _object_path

            if self._options["_terms"][-1] != "/":
                object_name = object_path[-1]

            result = self.ensure_result([_result[-1]], "folder", object_name)

        if (
            self._options["_terms"][-1] == "/"
            and self._options["object_type"] == "folder"
        ):
            result = await self.look_inside(result, filters)

        return result, _object_path

    async def _get_host_moid(self, object_path, filters):
        host_moid = ""
        result = ""
        _object_path = []

        # Host might be inside a cluster
        if self._options["object_type"] in ("host", "vm", "network", "datastore"):
            filters["names"] = object_path[0]
            cluster_moid, _object_path = await self._get_cluster_moid(
                object_path, filters
            )
            if not cluster_moid:
                return "", object_path[1:]

            filters = self._init_filter()
            filters["clusters"] = cluster_moid
            if _object_path:
                filters["names"] = _object_path[0]
            else:
                filters["names"] = ""

        result = await self._helper_fetch("host", filters)
        host_moid = self.ensure_result(result, "host", filters["names"])

        return host_moid, _object_path[1:]

    async def _helper_get_resource_pool_moid(self, object_path, filters):
        result = ""
        rp_moid = ""
        _object_path = []

        # Resource pool might be inside a cluster
        filters["names"] = object_path[0]
        cluster_moid, _object_path = await self._get_cluster_moid(object_path, filters)
        if not cluster_moid:
            return "", _object_path

        filters = self._init_filter()
        filters["clusters"] = cluster_moid

        if _object_path:
            result, _object_path = await self._fetch_result(
                _object_path, "resource_pool", filters
            )
            rp_moid = self.ensure_result(result, "resource_pool")

        if not result and _object_path:
            filters = self._init_filter()
            filters["names"] = _object_path[0]
            filters["clusters"] = cluster_moid
            # Resource pool might be inside a host
            host_moid, _object_path = await self._get_host_moid(_object_path, filters)
            if not host_moid:
                return "", _object_path

            filters["hosts"] = host_moid
            if _object_path:
                filters["names"] = _object_path[0]
                result, _object_path = await self._fetch_result(
                    _object_path, "resource_pool", filters
                )

        if result and self._options["object_type"] == "resource_pool":
            if isinstance(result, list) and _object_path:
                obj_path_set = set(_object_path)
                path_set = set([elem["name"] for elem in result])
                if path_set - obj_path_set and self._options["_terms"][-1] != "/":
                    return "", _object_path

        if (
            self._options["_terms"][-1] == "/"
            and self._options["object_type"] == "resource_pool"
        ):
            result = await self.look_inside(rp_moid, filters)
            return result, _object_path

        result = self.ensure_result(result, "resource_pool")

        return result, _object_path

    async def look_inside(self, pre_object, filters):
        result = ""
        _result = ""
        filters["names"] = ""
        object_type = self._options["object_type"]

        if pre_object:
            if (object_type == "resource_pool" and "resgroup" in pre_object) or (
                object_type == "folder" and "group" in pre_object
            ):
                parent_key = f"parent_{object_type}s"
                filters[parent_key] = pre_object

        object_key = f"{object_type}s"
        filters[object_key] = ""
        _result = await self._helper_fetch(object_type, filters)
        result = self.ensure_result(_result, object_type)

        return result

    async def _get_subset_moid(self, object_path, filters):
        object_name = ""
        result = ""
        _result = ""
        _object_path = []

        if not object_path:
            if self._options["_terms"][-1] != "/":
                return "", object_path
        else:
            if self._options["_terms"][-1] != "/":
                object_name = object_path[-1]

        filters["names"] = object_name
        _result = await self._helper_fetch(self._options["object_type"], filters)
        result = self.ensure_result(_result, self._options["object_type"])
        if not result:
            filters["names"] = ""

            if self._options["object_type"] == "vm":
                # VM might be in a resource pool
                result, _object_path = await self._helper_get_resource_pool_moid(
                    object_path, filters
                )
                if result:
                    return result

            # Object might be inside a host
            host_moid, _object_path = await self._get_host_moid(object_path, filters)
            if not host_moid:
                return ""

            filters["hosts"] = host_moid
            filters["folders"] = ""
            filters["names"] = object_name
            _result = await self._helper_fetch(self._options["object_type"], filters)
            result = self.ensure_result(_result, self._options["object_type"])

        return result

    async def _get_cluster_moid(self, object_path, filters):
        cluster_moid = ""
        result = await self._helper_fetch("cluster", filters)
        cluster_moid = self.ensure_result(result, "cluster", filters["names"])

        return cluster_moid, object_path[1:]

    @staticmethod
    def replace_space(string):
        return string.replace(" ", "%20") if " " in string else string

    async def get_all_objects_path_moid(self, object_path, object_type, filters):
        # GET MoID of all the objects specified in the path
        filters["names"] = list(set(object_path))

        if self._options["object_type"] == "vm":
            filters["type"] = "VIRTUAL_MACHINE"
        elif self._options["object_type"] not in ("resource_pool", "cluster", "folder"):
            filters["type"] = self._options[
                "object_type"
            ].upper()  # HOST, DATASTORE, DATACENTER, NETWORK

        return await self._helper_fetch(object_type, filters)

    async def recursive_folder_or_rp_moid_search(
        self,
        object_path,
        object_type,
        filters,
        parent_object=None,
        objects_moid=None,
        result=None,
    ):
        if result is None:
            # GET MoID of all the objects specified in the path
            result = []
            objects_moid = await self.get_all_objects_path_moid(
                object_path, object_type, filters
            )
            if not objects_moid:
                return ""
            elif len(objects_moid) == 1:
                return objects_moid

            return await self.recursive_folder_or_rp_moid_search(
                object_path,
                object_type,
                filters,
                objects_moid=objects_moid,
                result=result,
            )
        parent_key = f"parent_{object_type}s"
        filters[parent_key] = ""

        if objects_moid and object_path and objects_moid[0]["name"] == object_path[0]:
            # There exists a folder MoID with this name
            filters["names"] = object_path[0]

            if parent_object is not None:
                filters[parent_key] = parent_object
                tasks = [
                    asyncio.ensure_future(self._helper_fetch(object_type, filters))
                    for parent_object_info in objects_moid
                    if parent_object_info["name"] == object_path[0]
                ]
                _result = [await i for i in tasks]
                [
                    result.append(elem[0])
                    for elem in _result
                    if elem
                    if _result and elem[0] not in result
                ]
            else:
                _result = await self._helper_fetch(object_type, filters)
                if not _result:
                    return ""
                [result.append(elem) for elem in _result if elem not in result]
                # Update parent_object
                parent_object = result[0][object_type]
                return await self.recursive_folder_or_rp_moid_search(
                    object_path[1:],
                    object_type,
                    filters,
                    parent_object,
                    objects_moid[1:],
                    result,
                )
        if not object_path or (objects_moid and len(objects_moid) == 0):
            # Return result and what left in the path
            if not result:
                result = objects_moid
            return result

        if result:
            # Update parent_object
            parent_object = result[-1][object_type]
        return await self.recursive_folder_or_rp_moid_search(
            object_path[1:],
            object_type,
            filters,
            parent_object,
            objects_moid[1:],
            result,
        )

    async def moid(self, object_path):
        folder_moid = ""
        result = ""
        filters = {}
        _path = []

        if not object_path:
            return ""

        # Split object_path for transversal
        self._options["_terms"] = object_path
        object_path = self.replace_space(object_path)
        object_type = self._options["object_type"]
        path = tuple(filter(None, object_path.split("/")))

        # Retrieve datacenter MoID
        dc_moid, _path = await self._get_datacenter_moid(path)
        if object_type == "datacenter" or not dc_moid:
            return dc_moid
        self._options["dc_moid"] = dc_moid
        filters["datacenters"] = self._options["dc_moid"]

        if _path:
            _path = _path[1:]

        # Retrieve folders MoID
        folder_moid, _path = await self._get_folder_moid(_path, filters)
        if object_type == "folder" or not folder_moid:
            return folder_moid
        filters["folders"] = folder_moid

        if object_type == "cluster":
            if object_path[-1] != "/":
                # Save object name
                filters["names"] = _path[-1]
            else:
                filters["names"] = ""
            result, _obj_path = await self._get_cluster_moid(_path, filters)

        if object_type in ("datastore", "network"):
            filters = self._init_filter()
            filters["folders"] = folder_moid
            result = await self._get_subset_moid(_path, filters)

        if object_type == "resource_pool":
            result, _obj_path = await self._helper_get_resource_pool_moid(
                _path, filters
            )

        if object_type == "vm":
            result = await self._get_subset_moid(_path, filters)

        if object_type == "host":
            result, _obj_path = await self._get_host_moid(_path, filters)

        return result
