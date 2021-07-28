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
"""
