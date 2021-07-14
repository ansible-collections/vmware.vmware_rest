# Copyright: (c) 2021, Alina Buzachis <@alinabuzachis>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = r'''
lookup: resource_pool_moid
short_description: Look up MoID for vSphere resource pool objects using vCenter REST API
description:
    - Returns Managed Object Reference (MoID) of the vSphere resource pool object contained in the specified path.
author:
    - Alina Buzachis <@alinabuzachis>
version_added: 2.0.1
requirements:
    - vSphere 7.0.2 or greater
    - python >= 3.6
    - aiohttp
extends_documentation_fragment:
- vmware.vmware_rest.moid
'''


EXAMPLES = r'''
# lookup sample
- name: set connection info
  set_fact:
    connection_args:
        vcenter_hostname: "vcenter.test"
        vcenter_username: "administrator@vsphere.local"
        vcenter_password: "1234"

- name: lookup MoID of the object
  debug: msg="{{ lookup('vmware.vmware_rest.resource_pool_moid', '/my_dc/host/my_cluster/Resources/my_resource_pool', **connection_args) }}"

- name: lookup MoID of the object inside the path
  debug: msg="{{ lookup('vmware.vmware_rest.resource_pool_moid', '/my_dc/host/my_cluster/Resources/') }}"
'''


RETURN = r'''
_raw:
    description: MoID of the vSphere resource pool object
    type: str
    sample: resgroup-1008
'''


import asyncio

from ansible.plugins.lookup import LookupBase

from ansible_collections.vmware.vmware_rest.plugins.module_utils.lookup import (
    Lookup,
    get_credentials
)


class LookupModule(LookupBase):
    def run(self, terms, variables, **kwargs):
        self.set_options(var_options=variables, direct=get_credentials(**kwargs))
        self.set_option('object_type', 'resource_pool')
        loop = asyncio.get_event_loop()

        return loop.run_until_complete(asyncio.gather(Lookup.entry_point(terms, self._options)))
