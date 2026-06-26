#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright: (c) 2026, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


class ModuleDocFragment(object):
    # Parameters for authentication and connection arguments
    DOCUMENTATION = r"""
    options:
        vcenter_hostname:
            description:
                - The hostname or IP address of the vSphere vCenter.
                - If the value is not specified in the task, the value of environment variable
                    C(VMWARE_HOST) will be used instead.
            required: true
            type: str
        vcenter_username:
            description:
                - The vSphere vCenter username.
                - If the value is not specified in the task, the value of environment variable
                    C(VMWARE_USER) will be used instead.
            required: true
            type: str
        vcenter_password:
            description:
                - The vSphere vCenter password.
                - If the value is not specified in the task, the value of environment variable
                    C(VMWARE_PASSWORD) will be used instead.
            required: true
            type: str
        vcenter_validate_certs:
            description:
                - Allows connection when SSL certificates are not valid.
                - Set to C(false) when certificates are not trusted.
                - If the value is not specified in the task, the value of environment variable
                    C(VMWARE_VALIDATE_CERTS) will be used instead.
            default: true
            type: bool
        vcenter_port:
            description:
                - The port number of the vSphere vCenter.
                - If the value is not specified in the task, the value of environment variable
                    C(VMWARE_PORT) will be used instead.
            type: int
            required: false
        vcenter_rest_log_file:
            description:
                - Optional path to a log file for HTTP REST interaction.
                - If the value is not specified in the task, the value of environment variable
                    C(VMWARE_REST_LOG_FILE) will be used instead.
            type: str
        session_timeout:
            description:
                - Timeout in seconds for the whole operation including connection establishment,
                    request sending, and response.
            type: float
"""
