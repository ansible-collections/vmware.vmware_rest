.. _vmware.vmware_rest.vcenter_vm_info_module:


**********************************
vmware.vmware_rest.vcenter_vm_info
**********************************

**Collect the  information from a VM**


Version added: 1.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- Collect the  information from a VM



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
                    <b>filter_clusters</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Clusters that must contain the virtual machine for the virtual machine to match the filter.</div>
                        <div>If unset or empty, virtual machines in any cluster match the filter.</div>
                        <div>When clients pass a value of this structure as a parameter, the field must contain the id of resources returned by <span class='module'>vcenter_cluster_info</span>.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>filter_datacenters</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Datacenters that must contain the virtual machine for the virtual machine to match the filter.</div>
                        <div>If unset or empty, virtual machines in any datacenter match the filter.</div>
                        <div>When clients pass a value of this structure as a parameter, the field must contain the id of resources returned by <span class='module'>vcenter_datacenter_info</span>.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>filter_folders</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Folders that must contain the virtual machine for the virtual machine to match the filter.</div>
                        <div>If unset or empty, virtual machines in any folder match the filter.</div>
                        <div>When clients pass a value of this structure as a parameter, the field must contain the id of resources returned by <span class='module'>vcenter_folder_info</span>.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>filter_hosts</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Hosts that must contain the virtual machine for the virtual machine to match the filter.</div>
                        <div>If unset or empty, virtual machines on any host match the filter.</div>
                        <div>When clients pass a value of this structure as a parameter, the field must contain the id of resources returned by <span class='module'>vcenter_host_info</span>.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>filter_names</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Names that virtual machines must have to match the filter (see <em>name</em>).</div>
                        <div>If unset or empty, virtual machines with any name match the filter.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>filter_power_states</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Power states that a virtual machine must be in to match the filter (see I()</div>
                        <div>If unset or empty, virtual machines in any power state match the filter.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>filter_resource_pools</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Resource pools that must contain the virtual machine for the virtual machine to match the filter.</div>
                        <div>If unset or empty, virtual machines in any resource pool match the filter.</div>
                        <div>When clients pass a value of this structure as a parameter, the field must contain the id of resources returned by <span class='module'>vcenter_resourcepool_info</span>.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>filter_vms</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Identifiers of virtual machines that can match the filter.</div>
                        <div>If unset or empty, virtual machines with any identifier match the filter.</div>
                        <div>When clients pass a value of this structure as a parameter, the field must contain the id of resources returned by <span class='module'>vcenter_vm_info</span>.</div>
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

    - name: Look up the VM called test_vm1 in the inventory
      register: search_result
      vmware.vmware_rest.vcenter_vm_info:
        filter_names:
        - test_vm1
    - name: Collect information about a specific VM
      vmware.vmware_rest.vcenter_vm_info:
        vm: '{{ search_result.value[0].vm }}'
      register: test_vm1_info
    - name: Collect the list of the existing VM
      vmware.vmware_rest.vcenter_vm_info:
      register: existing_vms
      until: existing_vms is not failed
    - name: Look up the VM called test_vm1 in the inventory
      register: search_result
      vmware.vmware_rest.vcenter_vm_info:
        filter_names:
        - test_vm1
    - name: Search with an invalid filter
      vmware.vmware_rest.vcenter_vm_info:
        filter_names: test_vm1_does_not_exists



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
                    <b>id</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">string</span>
                    </div>
                </td>
                <td>On success</td>
                <td>
                            <div>moid of the resource</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">vm-1334</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>value</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>On success</td>
                <td>
                            <div>Collect information about a specific VM</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">{&#x27;boot&#x27;: {&#x27;delay&#x27;: 0, &#x27;enter_setup_mode&#x27;: 0, &#x27;retry&#x27;: 0, &#x27;retry_delay&#x27;: 10000, &#x27;type&#x27;: &#x27;BIOS&#x27;}, &#x27;boot_devices&#x27;: [], &#x27;cdroms&#x27;: [], &#x27;cpu&#x27;: {&#x27;cores_per_socket&#x27;: 1, &#x27;count&#x27;: 1, &#x27;hot_add_enabled&#x27;: 0, &#x27;hot_remove_enabled&#x27;: 0}, &#x27;disks&#x27;: [{&#x27;key&#x27;: &#x27;2000&#x27;, &#x27;value&#x27;: {&#x27;backing&#x27;: {&#x27;type&#x27;: &#x27;VMDK_FILE&#x27;, &#x27;vmdk_file&#x27;: &#x27;[rw_datastore] test_vm1_13/test_vm1.vmdk&#x27;}, &#x27;capacity&#x27;: 17179869184, &#x27;label&#x27;: &#x27;Hard disk 1&#x27;, &#x27;scsi&#x27;: {&#x27;bus&#x27;: 0, &#x27;unit&#x27;: 0}, &#x27;type&#x27;: &#x27;SCSI&#x27;}}], &#x27;floppies&#x27;: [], &#x27;guest_OS&#x27;: &#x27;DEBIAN_8_64&#x27;, &#x27;hardware&#x27;: {&#x27;upgrade_policy&#x27;: &#x27;NEVER&#x27;, &#x27;upgrade_status&#x27;: &#x27;NONE&#x27;, &#x27;version&#x27;: &#x27;VMX_11&#x27;}, &#x27;identity&#x27;: {&#x27;bios_uuid&#x27;: &#x27;4233b639-9121-f34d-f95a-6c1437dd5255&#x27;, &#x27;instance_uuid&#x27;: &#x27;5033a4c3-29db-76cc-993c-1b034d8bdecb&#x27;, &#x27;name&#x27;: &#x27;test_vm1&#x27;}, &#x27;instant_clone_frozen&#x27;: 0, &#x27;memory&#x27;: {&#x27;hot_add_enabled&#x27;: 1, &#x27;size_MiB&#x27;: 1024}, &#x27;name&#x27;: &#x27;test_vm1&#x27;, &#x27;nics&#x27;: [], &#x27;nvme_adapters&#x27;: [], &#x27;parallel_ports&#x27;: [], &#x27;power_state&#x27;: &#x27;POWERED_OFF&#x27;, &#x27;sata_adapters&#x27;: [], &#x27;scsi_adapters&#x27;: [{&#x27;key&#x27;: &#x27;1000&#x27;, &#x27;value&#x27;: {&#x27;label&#x27;: &#x27;SCSI controller 0&#x27;, &#x27;scsi&#x27;: {&#x27;bus&#x27;: 0, &#x27;unit&#x27;: 7}, &#x27;sharing&#x27;: &#x27;NONE&#x27;, &#x27;type&#x27;: &#x27;PVSCSI&#x27;}}], &#x27;serial_ports&#x27;: []}</div>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Goneri Le Bouder (@goneri) <goneri@lebouder.net>
