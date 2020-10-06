.. _vmware.vmware_rest.vcenter_vm_hardware_cdrom_module:


********************************************
vmware.vmware_rest.vcenter_vm_hardware_cdrom
********************************************

**Manage the cdrom of a VM**


Version added: 1.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- Manage the cdrom of a VM



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
                    <b>allow_guest_control</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">boolean</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>no</li>
                                    <li>yes</li>
                        </ul>
                </td>
                <td>
                        <div>Flag indicating whether the guest can connect and disconnect the device.</div>
                        <div>If unset, the value is unchanged.</div>
                </td>
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
                        <div>Physical resource backing for the virtual CD-ROM device.</div>
                        <div>If unset, defaults to automatic detection of a suitable host device.</div>
                        <div>Valide attributes are:</div>
                        <div>- <code>device_access_type</code> (str): This option defines the valid device access types for a physical device packing of a virtual CD-ROM device.</div>
                        <div>- Accepted values:</div>
                        <div>- EMULATION</div>
                        <div>- PASSTHRU</div>
                        <div>- PASSTHRU_EXCLUSIVE</div>
                        <div>- <code>host_device</code> (str): Name of the device that should be used as the virtual CD-ROM device backing.</div>
                        <div>If unset, the virtual CD-ROM device will be configured to automatically detect a suitable host device.</div>
                        <div>- <code>iso_file</code> (str): Path of the image file that should be used as the virtual CD-ROM device backing.</div>
                        <div>This field is optional and it is only relevant when the value of <em>type</em> is ISO_FILE.</div>
                        <div>- <code>type</code> (str): This option defines the valid backing types for a virtual CD-ROM device.</div>
                        <div>- Accepted values:</div>
                        <div>- ISO_FILE</div>
                        <div>- HOST_DEVICE</div>
                        <div>- CLIENT_DEVICE</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>cdrom</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Virtual CD-ROM device identifier.</div>
                        <div>The parameter must be the id of a resource returned by <span class='module'>vcenter_vm_hardware_cdrom</span>. Required with <em>state=[&#x27;absent&#x27;, &#x27;connect&#x27;, &#x27;disconnect&#x27;]</em></div>
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
                        <div>Valide attributes are:</div>
                        <div>- <code>master</code> (bool): Flag specifying whether the device should be the master or slave device on the IDE adapter.</div>
                        <div>If unset, the server will choose an available connection type. If no IDE connections are available, the request will be rejected.</div>
                        <div>- <code>primary</code> (bool): Flag specifying whether the device should be attached to the primary or secondary IDE adapter of the virtual machine.</div>
                        <div>If unset, the server will choose a adapter with an available connection. If no IDE connections are available, the request will be rejected.</div>
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
                        <div>Valide attributes are:</div>
                        <div>- <code>bus</code> (int): Bus number of the adapter to which the device should be attached.</div>
                        <div>- <code>unit</code> (int): Unit number of the device.</div>
                        <div>If unset, the server will choose an available unit number on the specified adapter. If there are no available connections on the adapter, the request will be rejected.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>start_connected</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">boolean</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>no</li>
                                    <li>yes</li>
                        </ul>
                </td>
                <td>
                        <div>Flag indicating whether the virtual device should be connected whenever the virtual machine is powered on.</div>
                        <div>If unset, the value is unchanged.</div>
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
                                    <li>connect</li>
                                    <li>disconnect</li>
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
                                    <li>SATA</li>
                        </ul>
                </td>
                <td>
                        <div>The <em>host_bus_adapter_type</em> enumerated type defines the valid types of host bus adapters that may be used for attaching a Cdrom to a virtual machine.</div>
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
                        <div>The parameter must be the id of a resource returned by <span class='module'>vcenter_vm_info</span>.</div>
                </td>
            </tr>
    </table>
    <br/>




Examples
--------

.. code-block:: yaml+jinja

    - name: Collect information about a specific VM
      vcenter_vm_info:
        vm: '{{ search_result.value[0].vm }}'
      register: test_vm1_info
    - name: Attach an ISO image to a guest VM
      vcenter_vm_hardware_cdrom:
        vm: '{{ test_vm1_info.id }}'
        type: SATA
        sata:
          bus: 0
          unit: 2
        start_connected: true
        backing:
          iso_file: '[ro_datastore] fedora.iso'
          type: ISO_FILE




Status
------


Authors
~~~~~~~

- Goneri Le Bouder (@goneri) <goneri@lebouder.net>
