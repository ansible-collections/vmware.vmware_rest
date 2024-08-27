# Copyright: (c) 2021, Alina Buzachis <@alinabuzachis>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function

__metaclass__ = type


import asyncio
import urllib

from ansible.errors import AnsibleLookupError
from ansible.module_utils._text import to_native
from ansible_collections.vmware.vmware_rest.plugins.module_utils.vmware_rest import (
    gen_args,
    open_session,
)

FILTER_MAPPINGS = {
    "resource_pool": {
        "parent_resource_pools": "parent_resource_pools",
        "resource_pools": "resource_pools",
    },
    "datacenter": {
        "parent_folders": "folders",
    },
    "folder": {},
    "cluster": {
        "parent_folders": "folders",
    },
    "host": {
        "parent_folders": "folders",
    },
    "datastore": {
        "parent_folders": "folders",
    },
    "vm": {
        "parent_folders": "folders",
    },
    "network": {"parent_folders": "folders"},
}


class VcenterApi:
    def __init__(self, hostname, session):
        self.hostname = hostname
        self.session = session

    async def fetch(self, url):
        async with self.session.get(url) as response:
            result = await response.json()
            return result

    def build_url(self, object_type, filters):
        corrected_filters_for_query = self.correct_filter_names(filters, object_type)
        if object_type == "resource_pool":
            object_type = object_type.replace("_", "-")

        return (f"https://{self.hostname}/api/vcenter/{object_type}") + gen_args(
            corrected_filters_for_query, corrected_filters_for_query.keys()
        )

    def correct_filter_names(self, filters, object_type):
        """
        Objects in vSphere have slightly different filter names. For example, some use 'parent_folders' and some use 'folders'.
        Its easier to read the code if we do all of the filter corrections at the end using a map.
        Params:
            filters: dict, The active filters that should be applied to the REST request
        """
        if object_type not in FILTER_MAPPINGS.keys():
            raise AnsibleLookupError(
                "object_type must be one of [%s]."
                % ", ".join(list(FILTER_MAPPINGS.keys()))
            )
        corrected_filters = {}
        for filter_key, filter_value in filters.items():
            try:
                corrected_filters[FILTER_MAPPINGS[object_type][filter_key]] = (
                    filter_value
                )
            except KeyError:
                corrected_filters[filter_key] = filter_value

        return corrected_filters

    async def fetch_object_with_filters(self, object_type, filters):
        _url = self.build_url(object_type, filters)
        res = await self.fetch(_url)
        return await self.fetch(_url)


class Lookup:
    def __init__(self, options, session):
        self._options = options
        self.api = VcenterApi(options["vcenter_hostname"], session)
        self.active_filters = {}
        self.object_type = options["object_type"]

    @classmethod
    async def entry_point(cls, terms, options):
        if not terms or not terms[0]:
            raise AnsibleLookupError(
                "Option _terms is required but no object has been specified"
            )
        session = None
        try:
            session = await open_session(
                vcenter_hostname=options["vcenter_hostname"],
                vcenter_username=options["vcenter_username"],
                vcenter_password=options["vcenter_password"],
                validate_certs=options.get("vcenter_validate_certs"),
                log_file=options.get("vcenter_rest_log_file"),
            )
        except Exception as e:
            raise AnsibleLookupError(
                f'Unable to connect to vCenter or ESXi API at {options["vcenter_hostname"]}: {to_native(e)}'
            )

        lookup = cls(options, session)
        lookup._options["_terms"] = terms[0]

        task = asyncio.create_task(lookup.search_for_object_moid_top_down())
        return await task

    async def search_for_object_moid_top_down(self):
        """
        Searches for the lookup term in VSphere. Uses a top down approach to progress
        through the path (for example /datacenter/vm/foo/bar/my-vm) until it reaches the
        desired object. This guarantees we find the correct object even if multiple have the
        same name, possibly at the cost of performance.
        """
        object_path = self._options["_terms"]
        return_all_children = object_path.endswith("/")
        path_parts = [_part for _part in object_path.split("/") if _part]

        for index, path_part in enumerate(path_parts):
            if not self.active_filters.get("datacenters"):
                datacenter_moid = await self.get_object_moid_by_name_and_type(
                    path_part, "datacenter"
                )
                if self.object_type == "datacenter" or not datacenter_moid:
                    return datacenter_moid
                self.active_filters["datacenters"] = datacenter_moid
                continue

            if index == len(path_parts) - 1:
                # were at the end of the object path. Either return the object, or return
                # all of the objects it contains (for example, the children inside of a folder)
                if return_all_children:
                    await self.process_intermediate_path_part(path_part)
                    return await self.get_all_children_in_object()
                else:
                    return await self.get_object_moid_by_name_and_type(path_part)

            else:
                # were in the middle of an object path, lookup the object at this level
                # and add it to the filters for the next round of searching
                await self.process_intermediate_path_part(path_part)
                continue

        raise Exception("here4")

    async def process_intermediate_path_part(self, intermediate_object_name):
        """
        Finds and returns the MoID for an object in the middle of a search path. Different vSphere objects can be
        children of other types of vSphere objects.
          - VMs could be in a resource pool, a host, or a folder
          - Networks could be in a host, or in a folder
          - Hosts could be in a cluster, or in a folder
          - Datastores could in a host, or in a folder
          - Resource pools could be in a cluster, or a host
        We start with the most restrictive searches and progressively expand the search area until something is found.
        We also update the filters to include the proper object filter for the next round of searches.
        Params:
            intermediate_object_name: str, The name of the current object to search for
        Returns:
            str or None, a single MoID or none if nothing was found
        """
        if self.object_type == "vm":
            result = await self.get_object_moid_by_name_and_type(
                intermediate_object_name, "resource_pool"
            )
            if result:
                self.set_new_filters_with_datacenter({"resource_pools": result})
                return result

        if self.object_type in ("host", "resource_pool"):
            result = await self.get_object_moid_by_name_and_type(
                intermediate_object_name, "cluster"
            )
            if result:
                self.set_new_filters_with_datacenter({"clusters": result})
                return result

        if self.object_type in ("vm", "network", "datastore", "resource_pool"):
            result = await self.get_object_moid_by_name_and_type(
                intermediate_object_name, "host"
            )
            if result:
                self.set_new_filters_with_datacenter({"hosts": result})
                return result

        # resource pools cant continue past this point
        if self.object_type == "resource_pool":
            return None

        result = await self.get_object_moid_by_name_and_type(
            intermediate_object_name, "folder"
        )
        self.set_new_filters_with_datacenter({"parent_folders": result})
        return result

    async def get_object_moid_by_name_and_type(self, object_name, _object_type=None):
        """
        Returns a single object MoID with a specific type, name, and filter set. If more than one object
        is found, and error is thrown.
        Params:
            object_name: str, the name of the object to search for
            _object_type: str, Optional name of the object type to search for. Defaults to the lookup plugin type
        Returns:
            str, a single MoID
        """
        if not _object_type:
            _object_type = self.object_type

        if _object_type == "datacenter":
            _filters = {"folders": "group-d1"}
        else:
            _filters = self.active_filters

        _filters["names"] = object_name
        _result = await self.api.fetch_object_with_filters(_object_type, _filters)

        object_moid = self.get_single_moid_from_result(
            _result, _object_type, object_name
        )
        return object_moid

    @staticmethod
    def get_single_moid_from_result(result, object_type, object_name=None):
        """
        Parses vSphere returns query results as a json list, validates the results and extracts
        the correct MoID
        Params:
            object_type: str, The type of object to search the results for
            object_name: str, The name of the object to search the results for
        Returns:
            str or None, a single MoID or none if nothing was found
        """
        if not result or not object_name:
            return None

        object_name_decoded = urllib.parse.unquote(object_name)
        if object_name_decoded not in result[0].values():
            return None

        results_with_decoded_names = []
        for obj in result:
            if "%2f" in obj["name"]:
                continue
            results_with_decoded_names.append((obj["name"], obj[object_type]))

        if len(results_with_decoded_names) > 1:
            raise AnsibleLookupError(
                "More than one object found with matching name: [%s]."
                % ", ".join(
                    [f"{item[0]} => {item[1]}" for item in results_with_decoded_names]
                )
            )

        try:
            return results_with_decoded_names[0][1]
        except (TypeError, KeyError, IndexError) as e:
            raise AnsibleLookupError(to_native(e))

    async def get_all_children_in_object(self):
        results = await self.api.fetch_object_with_filters(
            self.object_type, self.active_filters
        )

        try:
            return [result[self.object_type] for result in results]
        except KeyError:
            return None

    def set_new_filters_with_datacenter(self, new_filters):
        """
        Deletes filter key value pairs from the active filter dict and replaces them with the new filters.
        It will leave the datacenter filter since that is always used.
        Params:
            new_filters: dict, The new filters you want to apply as active
        """
        _dc = self.active_filters.get("datacenters")
        self.active_filters = new_filters
        if _dc:
            self.active_filters["datacenters"] = _dc
