# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Red Hat | Ansible
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

# Options for specifying object state

__metaclass__ = type


class ModuleDocFragment(object):

    DOCUMENTATION = r"""
options:
  vcenter_rest_session_timeout:
    description:
    - Timeout settings for client session.
    - The maximal number of seconds for the whole operation including connection establishment, request sending and response reading.
    type: float
    default: 600
    version_added: 2.1.0
"""
