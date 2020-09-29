.. _vmware.vmware_rest.vcenter_vm_storage_policy_module:


********************************************
vmware.vmware_rest.vcenter_vm_storage_policy
********************************************

**Manage the storage policy of a VM**


Version added: 1.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- Manage the storage policy of a VM



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
                    <b>disks</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Storage policy or policies to be used when reconfiguring virtual machine diks.</div>
                        <div>if unset the current storage policy is retained.</div>
                        <div>When clients pass a value of this structure as a parameter, the key in the field map must be the id of a resource returned by <span class='module'>vcenter_vm_hardware_disk</span>.</div>
                        <div>Valide attributes are:</div>
                        <div>- <code>key</code> (str):</div>
                        <div>- <code>value</code> (dict):</div>
                        <div>- Accepted keys:</div>
                        <div>- policy (string): Storage Policy identification.</div>
                        <div>This field is optional and it is only relevant when the value of <em>type</em> is USE_SPECIFIED_POLICY.</div>
                        <div>When clients pass a value of this structure as a parameter, the field must be the id of a resource returned by <span class='module'>vcenter_storage_policies</span>.</div>
                        <div>- type (string): This option defines the choices for how to specify the policy to be associated with a virtual disk.</div>
                        <div>Accepted value for this field:</div>
                        <div>- <code>USE_SPECIFIED_POLICY</code></div>
                        <div>- <code>USE_DEFAULT_POLICY</code></div>
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
                    <b>vm_home</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Storage policy to be used when reconfiguring the virtual machine home.</div>
                        <div>if unset the current storage policy is retained.</div>
                        <div>Valide attributes are:</div>
                        <div>- <code>policy</code> (str): Storage Policy identification.</div>
                        <div>This field is optional and it is only relevant when the value of <em>type</em> is USE_SPECIFIED_POLICY.</div>
                        <div>When clients pass a value of this structure as a parameter, the field must be the id of a resource returned by <span class='module'>vcenter_storage_policies</span>.</div>
                        <div>- <code>type</code> (str): This option defines the choices for how to specify the policy to be associated with the virtual machine home&#x27;s directory.</div>
                        <div>- Accepted values:</div>
                        <div>- USE_SPECIFIED_POLICY</div>
                        <div>- USE_DEFAULT_POLICY</div>
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
    - name: Adjust VM storage policy
      vcenter_vm_storage_policy:
        vm: '{{ test_vm1_info.id }}'
        disks:
        - key: '{{ my_new_disk.id }}'
          value:
            type: USE_DEFAULT_POLICY




Status
------


Authors
~~~~~~~

- Goneri Le Bouder (@goneri) <goneri@lebouder.net>
