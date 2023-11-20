.. _vmware.vmware_rest.vcenter_vm_info_module:


**********************************
vmware.vmware_rest.vcenter_vm_info
**********************************

**Returns information about a virtual machine.**


Version added: 0.1.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- Returns information about a virtual machine.



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
                    <b>clusters</b>
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
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>datacenters</b>
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
                        <div style="font-size: small; color: darkgreen"><br/>aliases: filter_datacenters</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>folders</b>
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
                        <div style="font-size: small; color: darkgreen"><br/>aliases: filter_folders</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>hosts</b>
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
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>names</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Names that virtual machines must have to match the filter (see {@link Info#name}).</div>
                        <div style="font-size: small; color: darkgreen"><br/>aliases: filter_names</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>power_states</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Power states that a virtual machine must be in to match the filter (see {@link <em>info</em>#state}.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>resource_pools</b>
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
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Virtual machine identifier. Required with <em>state=[&#x27;get&#x27;]</em></div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>vms</b>
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
                </td>
            </tr>
    </table>
    <br/>


Notes
-----

.. note::
   - Tested on vSphere 7.0.2



Examples
--------

.. code-block:: yaml

    - name: Create a VM
      vmware.vmware_rest.vcenter_vm:
        placement:
          cluster: "{{ lookup('vmware.vmware_rest.cluster_moid', '/my_dc/host/my_cluster') }}"
          datastore: "{{ lookup('vmware.vmware_rest.datastore_moid', '/my_dc/datastore/local') }}"
          folder: "{{ lookup('vmware.vmware_rest.folder_moid', '/my_dc/vm') }}"
          resource_pool: "{{ lookup('vmware.vmware_rest.resource_pool_moid', '/my_dc/host/my_cluster/Resources') }}"
        name: test_vm1
        guest_OS: RHEL_7_64
        hardware_version: VMX_11
        memory:
          hot_add_enabled: true
          size_MiB: 1024
        disks:
        - type: SATA
          backing:
            type: VMDK_FILE
            vmdk_file: '[local] test_vm1/{{ disk_name }}.vmdk'
        - type: SATA
          new_vmdk:
            name: second_disk
            capacity: 32000000000
        cdroms:
        - type: SATA
          sata:
            bus: 0
            unit: 2
        nics:
        - backing:
            type: STANDARD_PORTGROUP
            network: "{{ lookup('vmware.vmware_rest.network_moid', '/my_dc/network/VM Network') }}"
      register: my_vm

    - name: Wait until my VM is off
      vmware.vmware_rest.vcenter_vm_info:
        vm: '{{ my_vm.id }}'
      register: vm_info
      until:
      - vm_info is not failed
      - vm_info.value.power_state == "POWERED_OFF"
      retries: 60
      delay: 5

    - register: _should_be_empty
      name: Search with an invalid filter
      vmware.vmware_rest.vcenter_vm_info:
        filter_names: test_vm1_does_not_exists

    - name: Look up the VM called test_vm1 in the inventory
      register: search_result
      vmware.vmware_rest.vcenter_vm_info:
        filter_names:
        - test_vm1

    - name: Collect information about a specific VM
      vmware.vmware_rest.vcenter_vm_info:
        vm: '{{ search_result.value[0].vm }}'
      register: test_vm1_info



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
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">vm-1049</div>
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
                            <div>Wait until my VM is off</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">{&#x27;boot&#x27;: {&#x27;delay&#x27;: 0, &#x27;enter_setup_mode&#x27;: 0, &#x27;retry&#x27;: 0, &#x27;retry_delay&#x27;: 10000, &#x27;type&#x27;: &#x27;BIOS&#x27;}, &#x27;boot_devices&#x27;: [], &#x27;cdroms&#x27;: {&#x27;16002&#x27;: {&#x27;allow_guest_control&#x27;: 0, &#x27;backing&#x27;: {&#x27;auto_detect&#x27;: 1, &#x27;device_access_type&#x27;: &#x27;EMULATION&#x27;, &#x27;type&#x27;: &#x27;HOST_DEVICE&#x27;}, &#x27;label&#x27;: &#x27;CD/DVD drive 1&#x27;, &#x27;sata&#x27;: {&#x27;bus&#x27;: 0, &#x27;unit&#x27;: 2}, &#x27;start_connected&#x27;: 0, &#x27;state&#x27;: &#x27;NOT_CONNECTED&#x27;, &#x27;type&#x27;: &#x27;SATA&#x27;}}, &#x27;cpu&#x27;: {&#x27;cores_per_socket&#x27;: 1, &#x27;count&#x27;: 1, &#x27;hot_add_enabled&#x27;: 0, &#x27;hot_remove_enabled&#x27;: 0}, &#x27;disks&#x27;: {&#x27;16000&#x27;: {&#x27;backing&#x27;: {&#x27;type&#x27;: &#x27;VMDK_FILE&#x27;, &#x27;vmdk_file&#x27;: &#x27;[local] test_vm1/rhel-8.5.vmdk&#x27;}, &#x27;capacity&#x27;: 16106127360, &#x27;label&#x27;: &#x27;Hard disk 1&#x27;, &#x27;sata&#x27;: {&#x27;bus&#x27;: 0, &#x27;unit&#x27;: 0}, &#x27;type&#x27;: &#x27;SATA&#x27;}, &#x27;16001&#x27;: {&#x27;backing&#x27;: {&#x27;type&#x27;: &#x27;VMDK_FILE&#x27;, &#x27;vmdk_file&#x27;: &#x27;[local] test_vm1_1/second_disk.vmdk&#x27;}, &#x27;capacity&#x27;: 32000000000, &#x27;label&#x27;: &#x27;Hard disk 2&#x27;, &#x27;sata&#x27;: {&#x27;bus&#x27;: 0, &#x27;unit&#x27;: 1}, &#x27;type&#x27;: &#x27;SATA&#x27;}}, &#x27;floppies&#x27;: {}, &#x27;guest_OS&#x27;: &#x27;RHEL_7_64&#x27;, &#x27;hardware&#x27;: {&#x27;upgrade_policy&#x27;: &#x27;NEVER&#x27;, &#x27;upgrade_status&#x27;: &#x27;NONE&#x27;, &#x27;version&#x27;: &#x27;VMX_11&#x27;}, &#x27;identity&#x27;: {&#x27;bios_uuid&#x27;: &#x27;4231943a-a1b5-9d24-1e05-d447e9ff0396&#x27;, &#x27;instance_uuid&#x27;: &#x27;5031e081-01a7-d61a-31f8-4bc54057ec60&#x27;, &#x27;name&#x27;: &#x27;test_vm1&#x27;}, &#x27;instant_clone_frozen&#x27;: 0, &#x27;memory&#x27;: {&#x27;hot_add_enabled&#x27;: 1, &#x27;size_MiB&#x27;: 1024}, &#x27;name&#x27;: &#x27;test_vm1&#x27;, &#x27;nics&#x27;: {&#x27;4000&#x27;: {&#x27;allow_guest_control&#x27;: 0, &#x27;backing&#x27;: {&#x27;network&#x27;: &#x27;network-1041&#x27;, &#x27;network_name&#x27;: &#x27;VM Network&#x27;, &#x27;type&#x27;: &#x27;STANDARD_PORTGROUP&#x27;}, &#x27;label&#x27;: &#x27;Network adapter 1&#x27;, &#x27;mac_address&#x27;: &#x27;00:50:56:b1:22:7d&#x27;, &#x27;mac_type&#x27;: &#x27;ASSIGNED&#x27;, &#x27;pci_slot_number&#x27;: 160, &#x27;start_connected&#x27;: 0, &#x27;state&#x27;: &#x27;NOT_CONNECTED&#x27;, &#x27;type&#x27;: &#x27;VMXNET3&#x27;, &#x27;upt_compatibility_enabled&#x27;: 0, &#x27;wake_on_lan_enabled&#x27;: 0}}, &#x27;nvme_adapters&#x27;: {}, &#x27;parallel_ports&#x27;: {}, &#x27;power_state&#x27;: &#x27;POWERED_OFF&#x27;, &#x27;sata_adapters&#x27;: {&#x27;15000&#x27;: {&#x27;bus&#x27;: 0, &#x27;label&#x27;: &#x27;SATA controller 0&#x27;, &#x27;pci_slot_number&#x27;: 32, &#x27;type&#x27;: &#x27;AHCI&#x27;}}, &#x27;scsi_adapters&#x27;: {}, &#x27;serial_ports&#x27;: {}}</div>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Ansible Cloud Team (@ansible-collections)
