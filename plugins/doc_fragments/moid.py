# Copyright: (c) 2021, Alina Buzachis <@alinabuzachis>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


class ModuleDocFragment(object):
    # Parameters for the Lookup Managed Object Reference (MoID) plugins
    DOCUMENTATION = r"""
    options:
        _terms:
            description: Path to query.
            required: True
            type: string
        vcenter_hostname:
            description:
                - The hostname or IP address of the vSphere vCenter.
            env:
                - name: VMWARE_HOST
            required: True
            type: string
        vcenter_password:
            description:
                - The vSphere vCenter password.
            env:
                - name: VMWARE_PASSWORD
            required: True
            type: string
        vcenter_rest_log_file:
            description:
                - You can use this optional parameter to set the location of a log file.
                - This file will be used to record the HTTP REST interactions.
                - The file will be stored on the host that runs the module.
            env:
                - name: VMWARE_REST_LOG_FILE
            type: string
        vcenter_username:
            description:
                - The vSphere vCenter username.
            env:
                - name: VMWARE_USER
            required: True
            type: string
        vcenter_validate_certs:
            description:
                - Allows connection when SSL certificates are not valid. Set to V(false) when
                  certificates are not trusted.
            default: true
            env:
                - name: VMWARE_VALIDATE_CERTS
            type: boolean
"""
