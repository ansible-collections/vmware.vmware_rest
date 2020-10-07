.. _vmware.vmware_rest.vcenter_vm_hardware_serial_module:


*********************************************
vmware.vmware_rest.vcenter_vm_hardware_serial
*********************************************

**Manage the serial of a VM**


Version added: 1.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- Manage the serial of a VM



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
                        <div>Physical resource backing for the virtual serial port.</div>
                        <div>If unset, defaults to automatic detection of a suitable host device.</div>
                        <div>Valide attributes are:</div>
                        <div>- <code>file</code> (str): Path of the file backing the virtual serial port.</div>
                        <div>This field is optional and it is only relevant when the value of <em>type</em> is FILE.</div>
                        <div>- <code>host_device</code> (str): Name of the device backing the virtual serial port.</div>
                        <div></div>
                        <div></div>
                        <div>If unset, the virtual serial port will be configured to automatically detect a suitable host device.</div>
                        <div>- <code>network_location</code> (str): URI specifying the location of the network service backing the virtual serial port.</div>
                        <div>- If <em>type</em> is NETWORK_SERVER, this field is the location used by clients to connect to this server. The hostname part of the URI should either be empty or should specify the address of the host on which the virtual machine is running.</div>
                        <div>- If <em>type</em> is NETWORK_CLIENT, this field is the location used by the virtual machine to connect to the remote server.</div>
                        <div></div>
                        <div>This field is optional and it is only relevant when the value of <em>type</em> is one of NETWORK_SERVER or NETWORK_CLIENT.</div>
                        <div>- <code>no_rx_loss</code> (bool): Flag that enables optimized data transfer over the pipe. When the value is true, the host buffers data to prevent data overrun. This allows the virtual machine to read all of the data transferred over the pipe with no data loss.</div>
                        <div>If unset, defaults to false.</div>
                        <div>- <code>pipe</code> (str): Name of the pipe backing the virtual serial port.</div>
                        <div>This field is optional and it is only relevant when the value of <em>type</em> is one of PIPE_SERVER or PIPE_CLIENT.</div>
                        <div>- <code>proxy</code> (str): Proxy service that provides network access to the network backing. If set, the virtual machine initiates a connection with the proxy service and forwards the traffic to the proxy.</div>
                        <div>If unset, no proxy service should be used.</div>
                        <div>- <code>type</code> (str): This option defines the valid backing types for a virtual serial port.</div>
                        <div>- Accepted values:</div>
                        <div>- FILE</div>
                        <div>- HOST_DEVICE</div>
                        <div>- PIPE_SERVER</div>
                        <div>- PIPE_CLIENT</div>
                        <div>- NETWORK_SERVER</div>
                        <div>- NETWORK_CLIENT</div>
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
                    <b>port</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Virtual serial port identifier.</div>
                        <div>The parameter must be the id of a resource returned by <span class='module'>vcenter_vm_hardware_serial</span>. Required with <em>state=[&#x27;absent&#x27;, &#x27;connect&#x27;, &#x27;disconnect&#x27;]</em></div>
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
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>yield_on_poll</b>
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
                        <div>CPU yield behavior. If set to true, the virtual machine will periodically relinquish the processor if its sole task is polling the virtual serial port. The amount of time it takes to regain the processor will depend on the degree of other virtual machine activity on the host.</div>
                        <div>This field may be modified at any time, and changes applied to a connected virtual serial port take effect immediately.</div>
                        <div></div>
                        <div>If unset, the value is unchanged.</div>
                </td>
            </tr>
    </table>
    <br/>




Examples
--------

.. code-block:: yaml+jinja

    - name: Get an existing serial port (label)
      vcenter_vm_hardware_serial_info:
        vm: '{{ test_vm1_info.id }}'
        label: Serial port 1
      register: serial_port_1
    - name: Collect information about a specific VM
      vcenter_vm_info:
        vm: '{{ search_result.value[0].vm }}'
      register: test_vm1_info
    - name: Create a new serial port
      vcenter_vm_hardware_serial:
        vm: '{{ test_vm1_info.id }}'
        label: Serial port 2
        allow_guest_control: true
    - name: Create an existing serial port (label)
      vcenter_vm_hardware_serial:
        vm: '{{ test_vm1_info.id }}'
        label: Serial port 1
        allow_guest_control: true
    - name: Create another serial port with a label
      vcenter_vm_hardware_serial:
        vm: '{{ test_vm1_info.id }}'
        label: Serial port 2
        allow_guest_control: true
    - name: Delete an existing serial port (label)
      vcenter_vm_hardware_serial:
        vm: '{{ test_vm1_info.id }}'
        label: Serial port 2
        state: absent
    - name: Delete an existing serial port (port id)
      vcenter_vm_hardware_serial:
        vm: '{{ test_vm1_info.id }}'
        port: '{{ serial_port_1.id }}'
        state: absent




Status
------


Authors
~~~~~~~

- Goneri Le Bouder (@goneri) <goneri@lebouder.net>
