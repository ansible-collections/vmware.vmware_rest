#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright: (c) 2026, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#
# This module is generated using LLM agents and skills defined in the vmware.vmware_rest repository.
# See: https://github.com/ansible-collections/vmware.vmware_rest
#

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
module: content_library_subscriptions_info
short_description: List subscriptions of a published content library.
description:
  - Lists subscriptions of a published local content library.
  - When I(subscription) is specified, returns detailed information for that subscription only.
  - When I(subscription) is omitted, returns summary information for all subscriptions of the
    published library.
  - Requires the published library specified by I(library) to be a local library with publishing
    enabled.
author:
  - Ansible Eco Content Team (@eco-ansible-content)
extends_documentation_fragment:
  - vmware.vmware_rest.connection_params
options:
  library:
    description:
      - Identifier of the published local content library.
      - Must be an identifier (MOID) for a C(com.vmware.content.Library) resource.
    type: str
    required: true
  subscription:
    description:
      - Identifier of the subscription to retrieve.
      - Must be an identifier (MOID) for a C(com.vmware.content.library.Subscriptions) resource.
      - When specified, only that subscription is returned.
    type: str
version_added: 4.11.0
requirements: []
notes:
  - Generated from vSphere API spec 9.1.0.
  - Has support for vSphere API 7.0.3.
  - Has support for vSphere API 8.0.2.
"""

EXAMPLES = r"""
- name: List subscriptions of a published content library
  vmware.vmware_rest.content_library_subscriptions_info:
    library: "{{ published_library_id }}"
  register: library_subscriptions

- name: Get a specific content library subscription
  vmware.vmware_rest.content_library_subscriptions_info:
    library: "{{ published_library_id }}"
    subscription: "{{ subscription_id }}"
  register: library_subscription
"""

RETURN = r"""
value:
  description:
    - Content library subscription information.
    - Returns a list of subscription summary dictionaries when I(subscription) is omitted.
    - Returns a single subscription dictionary when I(subscription) is specified.
  returned: On success
  type: raw
  sample:
    - subscribed_library: subscribed-lib-id
      subscribed_library_name: my-subscribed-library
      subscription: subscription-id
  contains:
    subscription:
      description:
        - Identifier of the subscription.
        - Must be an identifier (MOID) for a C(com.vmware.content.library.Subscriptions) resource.
      type: str
      sample: subscription-id
    subscribed_library:
      description:
        - Identifier of the subscribed library associated with the subscription.
        - Must be an identifier (MOID) for a C(com.vmware.content.Library) resource.
      type: str
      sample: subscribed-lib-id
    subscribed_library_name:
      description:
        - Name of the subscribed library associated with the subscription.
      type: str
      sample: my-subscribed-library
    subscribed_library_vcenter_hostname:
      description:
        - Hostname of the vCenter Server instance where the subscribed library exists.
        - This property is absent when the subscribed library is on the same vCenter Server
          instance as the published library.
      type: str
    subscribed_library_location:
      description:
        - Location of the subscribed library relative to the published library.
      type: str
      choices:
        - LOCAL
        - REMOTE
    subscribed_library_vcenter:
      description:
        - Information about the vCenter Server instance where the subscribed library exists.
        - This property is relevant when I(subscribed_library_location) is C(REMOTE).
      type: dict
    subscribed_library_placement:
      description:
        - Placement information for virtual machine template items of the subscribed library.
      type: dict
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.vmware.vmware_rest.plugins.module_utils._argument_spec import (
    connection_params_argument_spec,
)
from ansible_collections.vmware.vmware_rest.plugins.module_utils._module_base import (
    VmwareRestInfoModuleBase,
    normalize_list_response,
)

LIST_PATH = "/content/library/{library}/subscriptions"
SUBSCRIPTION_PATH = "/content/library/{library}/subscriptions/{subscription}"


class VmwareRestInfoModule(VmwareRestInfoModuleBase):
    PAYLOAD_FORMAT = {
        "list": {"query": {}, "body": {}, "path": {"library": "library"}},
        "get": {
            "query": {},
            "body": {},
            "path": {"library": "library", "subscription": "subscription"},
        },
    }

    def _get_subscription(self, library, subscription):
        path = self.build_path(
            SUBSCRIPTION_PATH,
            {"library": library, "subscription": subscription},
        )
        response = self.client.get(path)
        if response.status == 404:
            return None
        result = response.json
        result["subscription"] = subscription
        return result

    def get_info(self):
        library = self.params["library"]
        subscription = self.params.get("subscription")

        if subscription:
            result = self._get_subscription(library, subscription)
            if result is None:
                self.module.fail_json(
                    msg="Subscription not found: {0}".format(subscription)
                )
            return result

        list_path = self.build_path(LIST_PATH, {"library": library})
        response = self.client.get(list_path)
        if response.status == 404:
            return []
        return normalize_list_response(response.json)


def main():
    module_args = connection_params_argument_spec()
    module_args["library"] = {"type": "str", "required": True}
    module_args["subscription"] = {"type": "str"}

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
    )

    info_module = VmwareRestInfoModule(module)
    result = info_module.get_info()
    module.exit_json(value=result)


if __name__ == "__main__":
    main()
