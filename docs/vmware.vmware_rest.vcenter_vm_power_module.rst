.. _vmware.vmware_rest.vcenter_vm_power_module:


***********************************
vmware.vmware_rest.vcenter_vm_power
***********************************

**Resets a powered-on virtual machine.**


Version added: 0.1.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- Resets a powered-on virtual machine.



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
                    <b>state</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>reset</li>
                                    <li>start</li>
                                    <li>stop</li>
                                    <li>suspend</li>
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
                    <b>vcenter_rest_session_timeout</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">float</span>
                    </div>
                    <div style="font-style: italic; font-size: small; color: darkgreen">added in 2.1.0</div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">"300"</div>
                </td>
                <td>
                        <div>Timeout settings for client session.</div>
                        <div>The maximal number of seconds for the whole operation including connection establishment, request sending and response.</div>
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
                        <div>Virtual machine identifier. This parameter is mandatory.</div>
                </td>
            </tr>
    </table>
    <br/>




Examples
--------

.. code-block:: yaml

    - name: Collect the list of the existing VM
      vmware.vmware_rest.vcenter_vm_info:
      register: existing_vms
      until: existing_vms is not failed

    - name: Turn off the VM
      vmware.vmware_rest.vcenter_vm_power:
        state: stop
        vm: '{{ item.vm }}'
      with_items: '{{ existing_vms.value }}'
      ignore_errors: yes

    - name: Look up the VM called test_vm1 in the inventory
      register: search_result
      vmware.vmware_rest.vcenter_vm_info:
        filter_names:
        - test_vm1

    - name: Collect information about a specific VM
      vmware.vmware_rest.vcenter_vm_info:
        vm: '{{ search_result.value[0].vm }}'
      register: test_vm1_info

    - name: Turn the power of the VM on
      vmware.vmware_rest.vcenter_vm_power:
        state: start
        vm: '{{ test_vm1_info.id }}'



Return Values
-------------
Common return values are documented `here <https://docs.ansible.com/ansible/latest/reference_appendices/common_return_values.html#common-return-values>`_, the following are the fields unique to this module:

.. raw:: html

    <table border=0 cellpadding=0 class="documentation-table">
        <tr>
            <th colspan="1">Key</th>
            <th>Returned</th>
            <th width="100%">Description</th>
        </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>msg</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">string</span>
                    </div>
                </td>
                <td>On success</td>
                <td>
                            <div>Turn off the VM</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">All items completed</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>results</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">list</span>
                    </div>
                </td>
                <td>On success</td>
                <td>
                            <div>Turn off the VM</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[{&#x27;_ansible_item_label&#x27;: {&#x27;cpu_count&#x27;: 1, &#x27;memory_size_MiB&#x27;: 128, &#x27;name&#x27;: &#x27;vCLS (1)&#x27;, &#x27;power_state&#x27;: &#x27;POWERED_OFF&#x27;, &#x27;vm&#x27;: &#x27;vm-1478&#x27;}, &#x27;_ansible_no_log&#x27;: 0, &#x27;ansible_loop_var&#x27;: &#x27;item&#x27;, &#x27;changed&#x27;: 0, &#x27;failed&#x27;: 0, &#x27;invocation&#x27;: {&#x27;module_args&#x27;: {&#x27;state&#x27;: &#x27;stop&#x27;, &#x27;vcenter_hostname&#x27;: &#x27;vcenter.test&#x27;, &#x27;vcenter_password&#x27;: &#x27;VALUE_SPECIFIED_IN_NO_LOG_PARAMETER&#x27;, &#x27;vcenter_rest_log_file&#x27;: None, &#x27;vcenter_rest_session_timeout&#x27;: None, &#x27;vcenter_username&#x27;: &#x27;administrator@vsphere.local&#x27;, &#x27;vcenter_validate_certs&#x27;: 0, &#x27;vm&#x27;: &#x27;vm-1478&#x27;}}, &#x27;item&#x27;: {&#x27;cpu_count&#x27;: 1, &#x27;memory_size_MiB&#x27;: 128, &#x27;name&#x27;: &#x27;vCLS (1)&#x27;, &#x27;power_state&#x27;: &#x27;POWERED_OFF&#x27;, &#x27;vm&#x27;: &#x27;vm-1478&#x27;}, &#x27;value&#x27;: {&#x27;error_type&#x27;: &#x27;ALREADY_IN_DESIRED_STATE&#x27;, &#x27;messages&#x27;: [{&#x27;args&#x27;: [], &#x27;default_message&#x27;: &#x27;Virtual machine is already powered off.&#x27;, &#x27;id&#x27;: &#x27;com.vmware.api.vcenter.vm.power.already_powered_off&#x27;}, {&#x27;args&#x27;: [], &#x27;default_message&#x27;: &#x27;The attempted operation cannot be performed in the current state (Powered off).&#x27;, &#x27;id&#x27;: &#x27;vmsg.InvalidPowerState.summary&#x27;}]}}, {&#x27;_ansible_item_label&#x27;: {&#x27;cpu_count&#x27;: 1, &#x27;memory_size_MiB&#x27;: 1080, &#x27;name&#x27;: &#x27;test_vm1&#x27;, &#x27;power_state&#x27;: &#x27;POWERED_ON&#x27;, &#x27;vm&#x27;: &#x27;vm-1482&#x27;}, &#x27;_ansible_no_log&#x27;: 0, &#x27;ansible_loop_var&#x27;: &#x27;item&#x27;, &#x27;changed&#x27;: 0, &#x27;failed&#x27;: 0, &#x27;invocation&#x27;: {&#x27;module_args&#x27;: {&#x27;state&#x27;: &#x27;stop&#x27;, &#x27;vcenter_hostname&#x27;: &#x27;vcenter.test&#x27;, &#x27;vcenter_password&#x27;: &#x27;VALUE_SPECIFIED_IN_NO_LOG_PARAMETER&#x27;, &#x27;vcenter_rest_log_file&#x27;: None, &#x27;vcenter_rest_session_timeout&#x27;: None, &#x27;vcenter_username&#x27;: &#x27;administrator@vsphere.local&#x27;, &#x27;vcenter_validate_certs&#x27;: 0, &#x27;vm&#x27;: &#x27;vm-1482&#x27;}}, &#x27;item&#x27;: {&#x27;cpu_count&#x27;: 1, &#x27;memory_size_MiB&#x27;: 1080, &#x27;name&#x27;: &#x27;test_vm1&#x27;, &#x27;power_state&#x27;: &#x27;POWERED_ON&#x27;, &#x27;vm&#x27;: &#x27;vm-1482&#x27;}, &#x27;value&#x27;: {}}]</div>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Ansible Cloud Team (@ansible-collections)
