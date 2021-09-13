.. _vmware.vmware_rest.vcenter_vm_guest_filesystem_module:


**********************************************
vmware.vmware_rest.vcenter_vm_guest_filesystem
**********************************************

**Initiates an operation to transfer a file to or from the guest**


Version added: 2.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- Initiates an operation to transfer a file to or from the guest. <p> If the power state of the Virtual Machine is changed when the file transfer is in progress, or the Virtual Machine is migrated, then the transfer operation is aborted. <p> When transferring a file into the guest and overwriting an existing file, the old file attributes are not preserved. <p> In order to ensure a secure connection to the host when transferring a file using HTTPS, the X.509 certificate for the host must be used to authenticate the remote end of the connection. The certificate of the host that the virtual machine is running on can be retrieved using the following fields: XXX insert link to certificate in Host config XXX <p>



Requirements
------------
The below requirements are needed on the host that executes this module.

- vSphere 7.0.2 or greater
- python >= 3.6
- aiohttp


Parameters
----------

.. raw:: html

    <table  border=0 cellpadding=0 class="documentation-table">
        <tr>
            <th colspan="1">Parameter</th>
            <th>Choices/<font color="blue">Defaults</font></th>
            <th width="100%">Comments</th>
        </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>attributes</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Details about the file to be transferred into the guest.</div>
                        <div>Valid attributes are:</div>
                        <div>- <code>size</code> (int): The size in bytes of the file to be transferred into the guest. ([&#x27;present&#x27;])</div>
                        <div>- <code>overwrite</code> (bool): Whether an existing file should be overwritten. ([&#x27;present&#x27;])</div>
                        <div>- <code>last_modified</code> (str): The date and time the file was last modified. ([&#x27;present&#x27;])</div>
                        <div>- <code>last_accessed</code> (str): The date and time the file was last accessed. ([&#x27;present&#x27;])</div>
                        <div>- <code>windows</code> (dict): Windows-specific file creation information. ([&#x27;present&#x27;])</div>
                        <div>- Accepted keys:</div>
                        <div>- hidden (boolean): The file is hidden.</div>
                        <div>- read_only (boolean): The file is read-only.</div>
                        <div>- <code>posix</code> (dict): Posix-specific file creation information. ([&#x27;present&#x27;])</div>
                        <div>- Accepted keys:</div>
                        <div>- owner_id (integer): The owner ID. If this property is not specified when passing a {@link PosixFileAttributesCreateSpec} object to {@link Transfers#create}, the default value will be the owner Id of the user who invoked the file transfer operation.</div>
                        <div>- group_id (integer): The group ID. If this property is not specified when passing a {@link PosixFileAttributesCreateSpec} object to {@link Transfers#create}, the default value will be the group Id of the user who invoked the file transfer operation.</div>
                        <div>- permissions (string): The file permissions in chmod(2) format. If this property is not specified when passing a {@link PosixFileAttributesCreateSpec} object to {@link Transfers#create}, the file will be created with 0644 permissions. This field is interpreted as octal.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>path</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The complete destination path in the guest to transfer the file to or from the client.  It cannot be a path to a directory or a symbolic link. This parameter is mandatory.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>session_timeout</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">float</span>
                    </div>
                    <div style="font-style: italic; font-size: small; color: darkgreen">added in 2.1.0</div>
                </td>
                <td>
                </td>
                <td>
                        <div>Timeout settings for client session.</div>
                        <div>The maximal number of seconds for the whole operation including connection establishment, request sending and response.</div>
                        <div>The default value is 300s.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>vcenter_hostname</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The hostname or IP address of the vSphere vCenter</div>
                        <div>If the value is not specified in the task, the value of environment variable <code>VMWARE_HOST</code> will be used instead.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>vcenter_password</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The vSphere vCenter password</div>
                        <div>If the value is not specified in the task, the value of environment variable <code>VMWARE_PASSWORD</code> will be used instead.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>vcenter_rest_log_file</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>You can use this optional parameter to set the location of a log file.</div>
                        <div>This file will be used to record the HTTP REST interaction.</div>
                        <div>The file will be stored on the host that run the module.</div>
                        <div>If the value is not specified in the task, the value of</div>
                        <div>environment variable <code>VMWARE_REST_LOG_FILE</code> will be used instead.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>vcenter_username</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The vSphere vCenter username</div>
                        <div>If the value is not specified in the task, the value of environment variable <code>VMWARE_USER</code> will be used instead.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>vcenter_validate_certs</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">boolean</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>no</li>
                                    <li><div style="color: blue"><b>yes</b>&nbsp;&larr;</div></li>
                        </ul>
                </td>
                <td>
                        <div>Allows connection when SSL certificates are not valid. Set to <code>false</code> when certificates are not trusted.</div>
                        <div>If the value is not specified in the task, the value of environment variable <code>VMWARE_VALIDATE_CERTS</code> will be used instead.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>vm</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Virtual Machine to perform the operation on. This parameter is mandatory.</div>
                </td>
            </tr>
    </table>
    <br/>


Notes
-----

.. note::
   - Tested on vSphere 7.0.2







Status
------


Authors
~~~~~~~

- Ansible Cloud Team (@ansible-collections)
