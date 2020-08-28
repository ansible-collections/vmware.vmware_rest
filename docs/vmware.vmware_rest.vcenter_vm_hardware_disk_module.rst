.. _vmware.vmware_rest.vcenter_vm_hardware_disk_module:


*******************************************
vmware.vmware_rest.vcenter_vm_hardware_disk
*******************************************

**Handle resource of type vcenter_vm_hardware_disk**


Version added: 1.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- Handle resource of type vcenter_vm_hardware_disk



Requirements
------------
The below requirements are needed on the host that executes this module.

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
                    <b>backing</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Existing physical resource backing for the virtual disk. Exactly one of Disk.CreateSpec.backing or Disk.CreateSpec.new-vmdk must be specified.</div>
                        <div>If unset, the virtual disk will not be connected to an existing backing.</div>
                        <div>Validate attributes are:</div>
                        <div>- <code>type</code> (str): The Disk.BackingType enumerated type defines the valid backing types for a virtual disk.</div>
                        <div>- <code>vmdk_file</code> (str): Path of the VMDK file backing the virtual disk.</div>
                        <div>This field is optional and it is only relevant when the value of Disk.BackingSpec.type is VMDK_FILE.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>disk</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Virtual disk identifier.</div>
                        <div>The parameter must be an identifier for the resource type: vcenter.vm.hardware.Disk. Required with <em>state=[&#x27;delete&#x27;, &#x27;update&#x27;]</em></div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>ide</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Address for attaching the device to a virtual IDE adapter.</div>
                        <div>If unset, the server will choose an available address; if none is available, the request will fail.</div>
                        <div>Validate attributes are:</div>
                        <div>- <code>master</code> (bool): Flag specifying whether the device should be the master or slave device on the IDE adapter.</div>
                        <div>If unset, the server will choose an available connection type. If no IDE connections are available, the request will be rejected.</div>
                        <div>- <code>primary</code> (bool): Flag specifying whether the device should be attached to the primary or secondary IDE adapter of the virtual machine.</div>
                        <div>If unset, the server will choose a adapter with an available connection. If no IDE connections are available, the request will be rejected.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>new_vmdk</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Specification for creating a new VMDK backing for the virtual disk. Exactly one of Disk.CreateSpec.backing or Disk.CreateSpec.new-vmdk must be specified.</div>
                        <div>If unset, a new VMDK backing will not be created.</div>
                        <div>Validate attributes are:</div>
                        <div>- <code>capacity</code> (int): Capacity of the virtual disk backing in bytes.</div>
                        <div>If unset, defaults to a guest-specific capacity.</div>
                        <div>- <code>name</code> (str): Base name of the VMDK file. The name should not include the &#x27;.vmdk&#x27; file extension.</div>
                        <div>If unset, a name (derived from the name of the virtual machine) will be chosen by the server.</div>
                        <div>- <code>storage_policy</code> (dict): The Disk.StoragePolicySpec structure contains information about the storage policy that is to be associated the with VMDK file.</div>
                        <div>If unset the default storage policy of the target datastore (if applicable) is applied. Currently a default storage policy is only supported by object based datastores : VVol &amp; vSAN. For non- object datastores, if unset then no storage policy would be associated with the VMDK file.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>sata</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Address for attaching the device to a virtual SATA adapter.</div>
                        <div>If unset, the server will choose an available address; if none is available, the request will fail.</div>
                        <div>Validate attributes are:</div>
                        <div>- <code>bus</code> (int): Bus number of the adapter to which the device should be attached.</div>
                        <div>- <code>unit</code> (int): Unit number of the device.</div>
                        <div>If unset, the server will choose an available unit number on the specified adapter. If there are no available connections on the adapter, the request will be rejected.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>scsi</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Address for attaching the device to a virtual SCSI adapter.</div>
                        <div>If unset, the server will choose an available address; if none is available, the request will fail.</div>
                        <div>Validate attributes are:</div>
                        <div>- <code>bus</code> (int): Bus number of the adapter to which the device should be attached.</div>
                        <div>- <code>unit</code> (int): Unit number of the device.</div>
                        <div>If unset, the server will choose an available unit number on the specified adapter. If there are no available connections on the adapter, the request will be rejected.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>state</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>absent</li>
                                    <li>present</li>
                                    <li>present</li>
                        </ul>
                </td>
                <td>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>type</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>IDE</li>
                                    <li>SATA</li>
                                    <li>SCSI</li>
                        </ul>
                </td>
                <td>
                        <div>The Disk.HostBusAdapterType enumerated type defines the valid types of host bus adapters that may be used for attaching a virtual storage device to a virtual machine.</div>
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
                        <div>The vSphere vCenter username</div>
                        <div>If the value is not specified in the task, the value of environment variable <code>VMWARE_PASSWORD</code> will be used instead.</div>
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
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Virtual machine identifier.</div>
                        <div>The parameter must be an identifier for the resource type: VirtualMachine.</div>
                </td>
            </tr>
    </table>
    <br/>








Status
------


Authors
~~~~~~~

- Goneri Le Bouder (@goneri) <goneri@lebouder.net>
