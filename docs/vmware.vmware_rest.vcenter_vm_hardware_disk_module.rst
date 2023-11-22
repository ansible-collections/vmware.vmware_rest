.. _vmware.vmware_rest.vcenter_vm_hardware_disk_module:


*******************************************
vmware.vmware_rest.vcenter_vm_hardware_disk
*******************************************

**Adds a virtual disk to the virtual machine**


Version added: 2.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- Adds a virtual disk to the virtual machine. While adding the virtual disk, a new VMDK file may be created or an existing VMDK file may be used to back the virtual disk.



Requirements
------------
The below requirements are needed on the host that executes this module.

- vSphere 7.0.3 or greater
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
                        <div>Existing physical resource backing for the virtual disk. Exactly one of <em>backing</em> or <em>new_vmdk</em> must be specified.</div>
                        <div>If unset, the virtual disk will not be connected to an existing backing. Required with <em>state=[&#x27;present&#x27;]</em></div>
                        <div>Valid attributes are:</div>
                        <div>- <code>type</code> (str): This option defines the valid backing types for a virtual disk. ([&#x27;present&#x27;])</div>
                        <div>This key is required with [&#x27;present&#x27;].</div>
                        <div>- Accepted values:</div>
                        <div>- VMDK_FILE</div>
                        <div>- <code>vmdk_file</code> (str): Path of the VMDK file backing the virtual disk.</div>
                        <div>This field is optional and it is only relevant when the value of <em>type</em> is VMDK_FILE. ([&#x27;present&#x27;])</div>
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
                        <div>The parameter must be the id of a resource returned by <span class='module'>vmware.vmware_rest.vcenter_vm_hardware_disk</span>. Required with <em>state=[&#x27;absent&#x27;, &#x27;present&#x27;]</em></div>
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
                        <div>Valid attributes are:</div>
                        <div>- <code>primary</code> (bool): Flag specifying whether the device should be attached to the primary or secondary IDE adapter of the virtual machine.</div>
                        <div>If unset, the server will choose a adapter with an available connection. If no IDE connections are available, the request will be rejected. ([&#x27;present&#x27;])</div>
                        <div>- <code>master</code> (bool): Flag specifying whether the device should be the master or slave device on the IDE adapter.</div>
                        <div>If unset, the server will choose an available connection type. If no IDE connections are available, the request will be rejected. ([&#x27;present&#x27;])</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>label</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The name of the item</div>
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
                        <div>Specification for creating a new VMDK backing for the virtual disk. Exactly one of <em>backing</em> or <em>new_vmdk</em> must be specified.</div>
                        <div>If unset, a new VMDK backing will not be created.</div>
                        <div>Valid attributes are:</div>
                        <div>- <code>name</code> (str): Base name of the VMDK file. The name should not include the &#x27;.vmdk&#x27; file extension.</div>
                        <div>If unset, a name (derived from the name of the virtual machine) will be chosen by the server. ([&#x27;present&#x27;])</div>
                        <div>- <code>capacity</code> (int): Capacity of the virtual disk backing in bytes.</div>
                        <div>If unset, defaults to a guest-specific capacity. ([&#x27;present&#x27;])</div>
                        <div>- <code>storage_policy</code> (dict): The <em>storage_policy_spec</em> structure contains information about the storage policy that is to be associated the with VMDK file.</div>
                        <div>If unset the default storage policy of the target datastore (if applicable) is applied. Currently a default storage policy is only supported by object based datastores : VVol &amp; vSAN. For non- object datastores, if unset then no storage policy would be associated with the VMDK file. ([&#x27;present&#x27;])</div>
                        <div>- Accepted keys:</div>
                        <div>- policy (string): Identifier of the storage policy which should be associated with the VMDK file.</div>
                        <div>When clients pass a value of this structure as a parameter, the field must be the id of a resource returned by <span class='module'>vmware.vmware_rest.vcenter_storage_policies</span>.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>nvme</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Address for attaching the device to a virtual NVMe adapter.</div>
                        <div>If unset, the server will choose an available address; if none is available, the request will fail. Required with <em>state=[&#x27;present&#x27;]</em></div>
                        <div>Valid attributes are:</div>
                        <div>- <code>bus</code> (int): Bus number of the adapter to which the device should be attached. ([&#x27;present&#x27;])</div>
                        <div>This key is required with [&#x27;present&#x27;].</div>
                        <div>- <code>unit</code> (int): Unit number of the device.</div>
                        <div>If unset, the server will choose an available unit number on the specified adapter. If there are no available connections on the adapter, the request will be rejected. ([&#x27;present&#x27;])</div>
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
                        <div>If unset, the server will choose an available address; if none is available, the request will fail. Required with <em>state=[&#x27;present&#x27;]</em></div>
                        <div>Valid attributes are:</div>
                        <div>- <code>bus</code> (int): Bus number of the adapter to which the device should be attached. ([&#x27;present&#x27;])</div>
                        <div>This key is required with [&#x27;present&#x27;].</div>
                        <div>- <code>unit</code> (int): Unit number of the device.</div>
                        <div>If unset, the server will choose an available unit number on the specified adapter. If there are no available connections on the adapter, the request will be rejected. ([&#x27;present&#x27;])</div>
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
                        <div>If unset, the server will choose an available address; if none is available, the request will fail. Required with <em>state=[&#x27;present&#x27;]</em></div>
                        <div>Valid attributes are:</div>
                        <div>- <code>bus</code> (int): Bus number of the adapter to which the device should be attached. ([&#x27;present&#x27;])</div>
                        <div>This key is required with [&#x27;present&#x27;].</div>
                        <div>- <code>unit</code> (int): Unit number of the device.</div>
                        <div>If unset, the server will choose an available unit number on the specified adapter. If there are no available connections on the adapter, the request will be rejected. ([&#x27;present&#x27;])</div>
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
                    <b>state</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>absent</li>
                                    <li><div style="color: blue"><b>present</b>&nbsp;&larr;</div></li>
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
                                    <li>NVME</li>
                                    <li>SATA</li>
                                    <li>SCSI</li>
                        </ul>
                </td>
                <td>
                        <div>The <em>host_bus_adapter_type</em> enumerated type defines the valid types of host bus adapters that may be used for attaching a virtual storage device to a virtual machine.</div>
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
                        <div>Virtual machine identifier.</div>
                        <div>The parameter must be the id of a resource returned by <span class='module'>vmware.vmware_rest.vcenter_vm_info</span>. This parameter is mandatory.</div>
                </td>
            </tr>
    </table>
    <br/>


Notes
-----

.. note::
   - Tested on vSphere 7.0.3



Examples
--------

.. code-block:: yaml

    - name: Look up the VM called test_vm1 in the inventory
      register: search_result
      vmware.vmware_rest.vcenter_vm_info:
        filter_names:
        - test_vm1

    - name: Collect information about a specific VM
      vmware.vmware_rest.vcenter_vm_info:
        vm: '{{ search_result.value[0].vm }}'
      register: test_vm1_info

    - name: Create a new disk
      vmware.vmware_rest.vcenter_vm_hardware_disk:
        vm: '{{ test_vm1_info.id }}'
        type: SATA
        new_vmdk:
          capacity: 320000
      register: my_new_disk

    - name: Delete the disk
      vmware.vmware_rest.vcenter_vm_hardware_disk:
        vm: '{{ test_vm1_info.id }}'
        disk: '{{ my_new_disk.id }}'
        state: absent
      register: _result




Status
------


Authors
~~~~~~~

- Ansible Cloud Team (@ansible-collections)
