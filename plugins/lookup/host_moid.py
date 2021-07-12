#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2021, Alina Buzachis <@alinabuzachis>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = r'''
lookup: host_moid
short_description: Look up MoID for vSphere objects using vCenter REST API
description:
    - Returns Managed Object Reference (MoID) of the object contained in the specified path.
options:
    _terms:
        description: paths to query.
        required: true
    vcenter_hostname:
        description:
            - The hostname or IP address of the vSphere vCenter.
            - If the value is not specified in the task, the value of environment variable
              C(VMWARE_HOST) will be used instead.
        required: true
        type: str
    vcenter_password:
        description:
            - The vSphere vCenter password.
            - If the value is not specified in the task, the value of environment variable
              C(VMWARE_PASSWORD) will be used instead.
        required: true
        type: str
    vcenter_rest_log_file:
        description:
            - You can use this optional parameter to set the location of a log file.
            - This file will be used to record the HTTP REST interaction.
            - The file will be stored on the host that run the module.
            - If the value is not specified in the task, the value of environment variable
              C(VMWARE_REST_LOG_FILE) will be used instead.
        type: str
    vcenter_username:
        description:
            - The vSphere vCenter username.
            - If the value is not specified in the task, the value of environment variable
              C(VMWARE_USER) will be used instead.
        required: true
        type: str
    vcenter_validate_certs:
        default: true
        description:
            - Allows connection when SSL certificates are not valid. Set to C(false) when
              certificates are not trusted.
            - If the value is not specified in the task, the value of environment variable
              C(VMWARE_VALIDATE_CERTS) will be used instead.
        type: bool
author:
    - Alina Buzachis <@alinabuzachis>
version_added: 2.0.1
requirements:
    - vSphere 7.0.2 or greater
    - python >= 3.6
    - aiohttp
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
  debug: msg="{{ lookup('vmware.vmware_rest.host_moid', '/my_dc/host/my_cluster/esxi1.test'},
                        **connection_args) }}"

- name: lookup MoID of the object inside the path
  debug: msg="{{ lookup('vmware.vmware_rest.host_moid', '/my_dc/host/my_cluster/'}) }}"
'''


RETURN = r'''
_list:
    description: list of the MoIDs
    type: list
    elements: str
'''


import asyncio
import os

from ansible.errors import AnsibleError
from ansible.plugins.lookup import LookupBase
from ansible.module_utils._text import to_native

from ansible_collections.cloud.common.plugins.module_utils.turbo.exceptions import EmbeddedModuleFailure
from ansible_collections.vmware.vmware_rest.plugins.module_utils.vmware_rest import open_session
from ansible_collections.vmware.vmware_rest.plugins.module_utils.lookup import Lookup
from ansible_collections.vmware.vmware_rest.plugins.module_utils.lookup import get_credentials


class LookupModule(LookupBase):
    def run(self, terms, variables, **kwargs):
        self.set_options(var_options=variables, direct=get_credentials(**kwargs))
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(asyncio.gather(self.entry_point(terms)))

    async def entry_point(self, terms):
        session = None
        self._options['object_type'] = 'host'

        if not self.get_option("vcenter_hostname"):
            raise AnsibleError("vcenter_hostname cannot be empty")
        if not self.get_option("vcenter_username"):
            raise AnsibleError("vcenter_username cannot be empty")
        if not self.get_option("vcenter_password"):
            raise AnsibleError("vcenter_password cannot be empty")

        try:
            session = await open_session(
                vcenter_hostname=self.get_option("vcenter_hostname"),
                vcenter_username=self.get_option("vcenter_username"),
                vcenter_password=self.get_option("vcenter_password"),
                validate_certs=bool(self.get_option("vcenter_validate_certs")),
                log_file=self.get_option("vcenter_rest_log_file"),
            )
        except EmbeddedModuleFailure as e:
            raise AnsibleError("Error connecting: %s" % to_native(e))

        self._options["session"] = session
        lookup = Lookup(self._options)

        if not terms:
            raise AnsibleError("No object has been specified.")

        tasks = [
            asyncio.ensure_future(lookup.moid(term)) for term in terms
        ]

        return [await i for i in tasks]
